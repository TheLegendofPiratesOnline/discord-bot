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
    def __init__(self):
        # This is really disgusting but works.
        # TODO: Rewrite.

        @self.bot.command()
        async def test(*args):
            """
            command: ping
            description: simple test command.
            """

            await self.bot.say("alive")
