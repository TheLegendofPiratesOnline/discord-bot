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

from bot.base import BotSettings
from bot.base import BotGlobals
from bot.commands import Commands

import json
import os

class BotCore(Commands.Commands):
    def __init__(self):
        self.settings = BotSettings.BotSettings()
        self.settings.loadSettings(BotGlobals.SETTINGS_FILENAME)

        if os.path.exists(BotGlobals.LOCAL_SETTINGS_FILENAME):
            # Load local settings. If we find a duplicate,
            # the local settings will override the regular.
            self.settings.loadSettings(BotGlobals.LOCAL_SETTINGS_FILENAME, override=True)

        self.bot = commands.Bot(description=BotGlobals.APP_DESCRIPTION,
                       command_prefix=self.settings.getSetting('commandPrefix'))

        Commands.Commands.__init__(self)

        @self.bot.event
        async def on_ready():
            print(':BotCore: Connected.')
            print(":BotCore: Logged in as user '%s' with ID '%s'" % (self.bot.user.name, self.bot.user.id))
            if len(self.bot.servers) == 0:
                print(":BotCore: To connect this bot to a server, please use the following url:\n")
                print('    https://discordapp.com/oauth2/authorize?client_id=%s&scope=bot&permissions=8' % self.bot.user.id)
            print(':BotCore: %s' % BotGlobals.APP_DESCRIPTION)
