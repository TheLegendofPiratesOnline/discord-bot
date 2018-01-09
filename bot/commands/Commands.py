# Filename: Commands.py
# Author: mfwass
# Date: January 8th, 2017
#
# The Legend of Pirates Online Software
# Copyright (c) The Legend of Pirates Online. All rights reserved.
#
# All use of this software is subject to the terms of the revised BSD
# license.  You should have received a copy of this license along
# with this source code in a file named "LICENSE."

from discord.ext import commands

from bot.language import BotLocalizer

class Commands:
    """
    The Commands class will house all commands provided by the
    TLOPO Discord Bot.

    This will hopefully make it easier for any developers to add
    further commands to this bot.
    """

    def __init__(self):
        # Right now, this is really disgusting - but it works!
        # TODO: Rewrite.

        @self.bot.command()
        async def oceans(*args):
            """
            Returns server populations.
            """

            output = ""
            oceans = {} #self.taskMgr.getOceanPopulations()
            total = 0

            for i, k in sorted(oceans.items()):
                output += "%s: %s\n" % (i, k)
                total += k

            output += BotLocalizer.OCEANS_TOTAL % total

            # Response.
            await self.bot.say(output)

        @self.bot.command()
        async def fleets(*args):
            """
            Returns active fleets.
            """

            fleets = self.taskMgr.getActiveFleets()

            if fleets:
                output = ""
                for i, k in sorted(fleets.items()):
                    output += BotLocalizer.FLEET_ITEM_INFO % (i,
                                                            k.get('type'),
                                                            k.get('state'),
                                                            k.get('shipsRemaining'))
            else:
                output = "No active fleets."

            # Response.
            await self.bot.say(output)

        @self.bot.command()
        async def invasions(*args):
            """
            Returns active invasions.
            """

            invasions = self.taskMgr.getActiveInvasions()

            if invasions:
                # At the time of this writing, invasions haven't been
                # released. When they are released, this bot will
                # receive an update.
                output = BotLocalizer.OUT_OF_DATE
            else:
                output = "No active invasions."

            # Response.
            await self.bot.say(output)
