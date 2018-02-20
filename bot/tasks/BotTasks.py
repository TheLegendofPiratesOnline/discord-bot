# Filename: BotTasks.py
# Author: mfwass
# Date: January 8th, 2017
#
# The Legend of Pirates Online Software
# Copyright (c) The Legend of Pirates Online. All rights reserved.
#
# All use of this software is subject to the terms of the revised BSD
# license.  You should have received a copy of this license along
# with this source code in a file named "LICENSE."

from bot.core import BotGlobals
import threading
import requests
import json

class BotTasks:
    """
    The BotTasks class will be responsible for
    keeping tabs on all looping tasks.
    """

    def __init__(self):
        self.activeFleets = {}
        self.activeInvasions = {}
        self.oceanPopulations = {}
        self.systemStatus = {}

    def initializeTasks(self, tasks):
        print(":BotTasks: Initializing tasks...")

        for task in tasks:
            getattr(self, task)(task, tasks.get(task))

    ## BOT TASKS
    """
    Example Task Function

    !!! Make sure you add any new tasks to BotGlobals!

    def task_example(self, name, task):
        # Required code to make the task repeat.
        threading.Timer(task.get('time'), getattr(self, name), args=[name, task]).start()

        # Task code here.

    """

    def task_news_notification(self, name, task):
        threading.Timer(task.get('time'), getattr(self, name), args=[name, task]).start()
        # TODO.

    def task_news_feed(self, name, task):
        threading.Timer(task.get('time'), getattr(self, name), args=[name, task]).start()
        # TODO.

    def task_system_status(self, name, task):
        threading.Timer(task.get('time'), getattr(self, name), args=[name, task]).start()
        resp = self.contactAPI(task.get('api_url'))
        if resp:
            servers = resp.get('servers')
            if servers:
                outages = [j.get('name', 'Error-NoName')
                           for i in servers.keys()
                           for j in servers.get(i)
                           if j.get('status') != BotGlobals.STATUS_ALIVE_SRV]
            else:
                outages = []

            out = {}
            out['status'] = resp.get('status')
            out['notices'] = resp.get('notices', 0) or None
            out['outages'] = outages or None
            self.setSystemStatus(out)

    def task_shards(self, name, task):
        threading.Timer(task.get('time'), getattr(self, name), args=[name, task]).start()
        resp = self.contactAPI(task.get('api_url'))
        if resp:
            fleets = {}
            invasions = {}
            populations = {}

            for shardId in resp.keys():
                # Get the information on the ocean.
                shardInfo = resp.get(shardId)
                available = shardInfo.get('available')

                if not available:
                    # Don't check the information on an offline ocean.
                    continue

                fleet = shardInfo.get('fleet')
                invasion = shardInfo.get('invasion')
                name = shardInfo.get('name')

                # Assign active fleets/invasions.
                if fleet:
                    fleets[name] = fleet

                if invasion:
                    invasions[name] = invasion

                # Set the population of this shard.
                populations[name] = shardInfo.get('population')

            # Set active fleets.
            self.setActiveFleets(fleets)
            self.setActiveInvasions(invasions)
            self.setOceanPopulations(populations)

    ## Other task functions.
    def contactAPI(self, apiUrl):
        """
        Contacts API and return its response in JSON format.
        """

        r = requests.get(apiUrl)

        try:
            # Just in case the API url dies, it's sanity check this.
            r = json.loads(r.text)
        except:
            print(":BotTasks(error): Failed to contact API.")
            r = None

        return r

    def setActiveFleets(self, fleets):
        """
        Set active fleets.
        """

        self.activeFleets = fleets

    def getActiveFleets(self):
        """
        Get active fleets.
        """

        return self.activeFleets

    def setSystemStatus(self, status):
        """
        Set system status.
        """

        self.systemStatus = status

    def getSystemStatus(self):
        """
        Get system status.
        """

        return self.systemStatus

    def setActiveInvasions(self, invasions):
        """
        Set active invasions.
        """

        self.activeInvasions = invasions

    def getActiveInvasions(self):
        """
        Get active invasions.
        """

        return self.activeInvasions

    def setOceanPopulations(self, populations):
        """
        Set ocean populations.
        """

        self.oceanPopulations = populations

    def getOceanPopulations(self):
        """
        Get ocean populations.
        """

        return self.oceanPopulations
