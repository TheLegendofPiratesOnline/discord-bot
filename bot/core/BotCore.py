# Filename: BotCore.py
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

from bot.core import BotGlobals, BotSettings
from bot.tasks import BotTasks

from bot.commands import Commands

import json
import os

class BotCore(Commands.Commands):
    """
    The BotCore class will serve as the central location
    for all of the Discord Bot's central functions.

    This class will load the settings for the application
    and house the Bot.

    Ideally, all global calls will reference this class for
    further direction.
    """

    def __init__(self):
        # Initialize the BotSettings class.
        self.settings = BotSettings.BotSettings()

        # Load settings from the settings file.
        self.settings.loadSettings(BotGlobals.SETTINGS_FILENAME)

        # Check if we have a local settings file.
        if os.path.exists(BotGlobals.LOCAL_SETTINGS_FILENAME):
            # Load local settings. If we find a duplicate,
            # the local settings will override the regular.
            self.settings.loadSettings(BotGlobals.LOCAL_SETTINGS_FILENAME, override=True)

        # Create the bot using Discord's API.
        self.bot = commands.Bot(description=BotGlobals.APP_DESCRIPTION,
                       command_prefix=self.settings.getSetting('commandPrefix'))

        # Initialize taskMgr.
        self.taskMgr = BotTasks.BotTasks()
        self.taskMgr.initializeTasks(BotGlobals.BOT_TASKS)

        # Initialize the Commands class.
        Commands.Commands.__init__(self)

        @self.bot.event
        async def on_ready():
            """
            When the bot is connected to the server and is ready to
            process commands, this function will be ran.

            This will give some useful information to Discord
            channel admin who's running this bot.
            """

            print(':BotCore: Connected.')
            print(":BotCore: Logged in as user '%s' with ID '%s'" % (self.bot.user.name, self.bot.user.id))

            # This bot is not in any servers yet, let's print the URL that they would use
            # to add the bot to a server.  Just in case they don't know it.
            if len(self.bot.guilds) == 0:
                print(":BotCore: To connect this bot to a server, please use the following url:\n")
                print('    https://discordapp.com/oauth2/authorize?client_id=%s&scope=bot&permissions=8' % self.bot.user.id)

            print(':BotCore: %s' % BotGlobals.APP_DESCRIPTION)
