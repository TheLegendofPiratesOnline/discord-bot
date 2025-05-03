# Filename: BotLocalizerEnglish.py
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
The class BotLocalizerEnglish is used when providing responses
in Discord channels where English is the spoken language.

All strings in this class will be in English only.
"""

import discord

OUT_OF_DATE = "This bot is out of date. Please update by visiting https://github.com/TheLegendofPiratesOnline/discord-bot"

FLEET_ITEM_INFO = '''- Type: %s
- State:  %s
- Ships Remaining:  %s
'''

INVASION_ITEM_INFO = '''- State:  %s
- Phase:  %s
- Num Players:  %s
'''

SYSTEM_STATUS_INFO = '''%s
Reported Outages: %s
'''

OVER_ALL_STATUS = '''Overall Status: **%s**
'''

updateErrorEmbed = discord.Embed(title="**The Legend of Pirates Online is currently closed for an update**", description="**%s**", color=0xff0000)