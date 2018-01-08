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

import builtins

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
        async def test(*args):
            """
            Simple test command.
            """

            await self.bot.say("alive")
