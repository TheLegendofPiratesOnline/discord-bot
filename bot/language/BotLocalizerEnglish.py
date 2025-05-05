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


APP_DESCRIPTION = "Discord bot by TLOPO. <3 \n https://github.com/TheLegendofPiratesOnline/discord-bot"

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

MSG_CLOSED_SERVERS = discord.Embed(title="**The Legend of Pirates Online is currently closed for an update**", description="**%s**", color=0xff0000)

EMBED_TITLES = [
    'Commands',  # 0
    'About',  # 1
    'Ocean Populations',  # 2
    'Active Fleets',  # 3
    'No active fleets',  # 4
    'Active Invasions',  # 5
    'No active invasions',  # 6
    'Server Notices',  # 7
    'Server Status',  # 8
    'Server Status Unavailable',  # 9
    'Server Notices Unavailable'  # 10
]

FIELD_NAMES = [
    'Authors',  # 0
    'Total',  # 1
    'Web Servers',  # 2
    'Client Agents',  # 3
    'Oceans',  # 4
    'Gameserver Functions'  # 5
]

STATUS_MESSAGES = [
    'No description available',  # 0
    'No authors found.',  # 1
    'No active fleet',  # 2
    'No active invasion',  # 3
    'No known notices.',  # 4
    'Ocean population data is unavailable',  # 5
    'Fleet data is unavailable',  # 6
    'Invasion data is unavailable',  # 7
    'Visit https://tlopo.com/ for more information.',  # 8
    'Status of prod-gs-1.tlopo.com is being detected incorrectly.\nThis is an issue with the TLOPO API.',  # 9
    'Unknown',  # 10
    'No data available',  # 11
    'Add me to your server!' # 12
]

# WILL RENAME LIST WHEN MORE BITS ARE ADDED
MISC = [
    'Message',  # 0
]