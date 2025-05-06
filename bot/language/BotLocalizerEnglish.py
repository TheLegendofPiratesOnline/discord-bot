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

from bot.core import BotGlobals

APP_DESCRIPTION = "Discord bot by TLOPO. <3 \n %s" % BotGlobals.SOURCE_URL

OUT_OF_DATE = "This bot is out of date. Please update by visiting %s" % BotGlobals.SOURCE_URL

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
    'Server Notices Unavailable',  # 10
    'The Legend of Pirates Online is currently closed for an update'  # 11
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

STATUS_ALIVE_SRV = 1
STATUS_MESSAGE_SRV = 2
STATUS_UPDATE_SRV = 4
STATUS_ERROR_SRV = 8
STATUS_FATAL_SRV = 16
STATUS_UNKNOWN_SRV = 32

SRV_CODE_TO_STATUS = {
    STATUS_ALIVE_SRV:   "ALIVE",
    STATUS_MESSAGE_SRV: "MESSAGE",
    STATUS_UPDATE_SRV:  "UPDATE",
    STATUS_ERROR_SRV:   "ERROR",
    STATUS_FATAL_SRV:   "FATAL",
    STATUS_UNKNOWN_SRV: "UNKNOWN"
}

STATUS_ALIVE_GLOB = 1
STATUS_MESSAGE_GLOB = 2
STATUS_UPDATE_GLOB = 3
STATUS_ERROR_GLOB = 4
STATUS_FATAL_GLOB = 5
STATUS_UNKNOWN_GLOB = 6

GLOB_CODE_TO_STATUS = {
    STATUS_ALIVE_GLOB:   "ALIVE",
    STATUS_MESSAGE_GLOB: "MESSAGE",
    STATUS_UPDATE_GLOB:  "UPDATE",
    STATUS_ERROR_GLOB:   "ERROR",
    STATUS_FATAL_GLOB:   "FATAL",
    STATUS_UNKNOWN_GLOB: "UNKNOWN"
}