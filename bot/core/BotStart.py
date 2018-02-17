# Filename: BotStart.py
# Author: mfwass
# Date: January 8th, 2017
#
# The Legend of Pirates Online Software
# Copyright (c) The Legend of Pirates Online. All rights reserved.
#
# All use of this software is subject to the terms of the revised BSD
# license.  You should have received a copy of this license along
# with this source code in a file named "LICENSE."

"""
The BotStart class will serve as the startup file
in the TLOPO Discord Bot project.

When this file is invoked, it will initialize the
bot and connect it to its respective Discord channel(s).
"""

from bot.core import BotCore

print(":BotStart: Initializing core...")

# Initialize BotCore.
core = BotCore.BotCore()

# Establish our connection with our appToken.
print(":BotStart: Connecting...")
core.bot.run(core.settings.getSetting('appToken'))
