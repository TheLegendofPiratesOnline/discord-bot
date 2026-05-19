# Concurrency smoke test for BotTasks.
#
# BotTasks is written by background threading.Timer callbacks and read
# by Discord command handlers on a different thread. The fix added
# threading.Lock around all setter/getter pairs. This test exercises
# that locked surface under heavy concurrent get/set load to confirm:
# - no exception escapes from any thread
# - every getter return value is one of the dicts the writer actually
#   put in (never a torn / half-written object)
# - the four dicts stay independent under interleaved writes
#
# Note: with the current "writers always replace, never mutate" pattern,
# the lock is primarily defensive against future mutating writes. This
# test catches a regression where someone removes the lock AND switches
# to a mutating setter (e.g. self.activeFleets[k] = v) without realising
# readers can no longer iterate safely.

import os
import sys
import threading
import time
import unittest

# Make the repo root importable when run as `python test_bot_tasks.py`.
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from bot.tasks.BotTasks import BotTasks


WRITER_ITERATIONS = 5000
READER_ITERATIONS = 5000


class TestBotTasksConcurrency(unittest.TestCase):
    def setUp(self):
        self.tasks = BotTasks()
        self.errors = []

    def _writer(self, setter_name, values):
        try:
            setter = getattr(self.tasks, setter_name)
            for i in range(WRITER_ITERATIONS):
                setter(values[i % len(values)])
        except Exception as exc:  # pragma: no cover - failure surface
            self.errors.append(('writer', setter_name, exc))

    def _reader(self, getter_name, allowed):
        try:
            getter = getattr(self.tasks, getter_name)
            for _ in range(READER_ITERATIONS):
                got = getter()
                # The returned dict must be one of the ones the writer
                # actually put in. With a torn read we'd see something
                # that doesn't match any allowed snapshot.
                if got not in allowed:
                    self.errors.append(
                        ('reader', getter_name, 'unexpected value: %r' % got))
                    return
                # Iterate too: catches a future mutating-setter regression
                # because iterating a mid-mutation dict raises RuntimeError.
                for _k, _v in got.items():
                    pass
        except Exception as exc:  # pragma: no cover - failure surface
            self.errors.append(('reader', getter_name, exc))

    def test_concurrent_get_set_across_all_four_dicts(self):
        fleet_values = [
            {'ocean1': {'name': 'fleet-a'}},
            {'ocean1': {'name': 'fleet-b'}, 'ocean2': {'name': 'fleet-c'}},
            {},
        ]
        invasion_values = [
            {'ocean1': {'state': 'active'}},
            {},
        ]
        population_values = [
            {'ocean1': 100},
            {'ocean1': 200, 'ocean2': 50},
            {'ocean1': 0},
        ]
        status_values = [
            {'status': 'green', 'outages': None},
            {'status': 'red', 'outages': ['game-server-1']},
        ]

        threads = [
            threading.Thread(target=self._writer,
                             args=('setActiveFleets', fleet_values)),
            threading.Thread(target=self._writer,
                             args=('setActiveInvasions', invasion_values)),
            threading.Thread(target=self._writer,
                             args=('setOceanPopulations', population_values)),
            threading.Thread(target=self._writer,
                             args=('setSystemStatus', status_values)),
            threading.Thread(target=self._reader,
                             args=('getActiveFleets', fleet_values)),
            threading.Thread(target=self._reader,
                             args=('getActiveInvasions', invasion_values)),
            threading.Thread(target=self._reader,
                             args=('getOceanPopulations', population_values)),
            threading.Thread(target=self._reader,
                             args=('getSystemStatus', status_values)),
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=30)

        self.assertEqual(self.errors, [], 'thread errors: %r' % self.errors)
        for t in threads:
            self.assertFalse(t.is_alive(), 'thread did not finish')

    def test_setter_getter_roundtrip(self):
        # Each setter/getter pair must round-trip a known value.
        fleet = {'oceanX': {'name': 'test-fleet'}}
        invasion = {'oceanY': {'state': 'wave-3'}}
        populations = {'oceanZ': 1234}
        status = {'status': 'green', 'outages': None, 'notices': 0, 'servers': {}}

        self.tasks.setActiveFleets(fleet)
        self.tasks.setActiveInvasions(invasion)
        self.tasks.setOceanPopulations(populations)
        self.tasks.setSystemStatus(status)

        self.assertEqual(self.tasks.getActiveFleets(), fleet)
        self.assertEqual(self.tasks.getActiveInvasions(), invasion)
        self.assertEqual(self.tasks.getOceanPopulations(), populations)
        self.assertEqual(self.tasks.getSystemStatus(), status)


if __name__ == '__main__':
    unittest.main()
