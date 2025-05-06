# Filename: BotGlobals.py
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
The BotGlobals class will serve as a central location
of all global values in the TLOPO Discord Bot project.
"""

LOCAL_SETTINGS_FILENAME = 'local_settings.json'
SETTINGS_FILENAME = 'settings.json'
AUTHORS_FILENAME = 'authors.md'

# API Docs: https://tlopo.com/docs/
API_URLS = {
    'news_feed':'https://api.tlopo.com/news/feed/',
    'news_notification':'https://api.tlopo.com/news/notification',
    'shards':'https://api.tlopo.com/shards',
    'system_status':'https://api.tlopo.com/system/status'
}

SOURCE_URL = "https://github.com/TheLegendofPiratesOnline/discord-bot"

BOT_TASKS = {
    'task_shards': {
        'time': 25.0,
        'api_url': API_URLS.get('shards')
    },
    'task_system_status': {
        'time': 25.0,
        'api_url': API_URLS.get('system_status')
    },
    'task_news_feed': {
        'time': 25.0,
        'api_url': API_URLS.get('news_feed')
    },
    'task_news_notification': {
        'time': 25.0,
        'api_url': API_URLS.get('news_notification')
    }
}

BASE_CHANNEL_TO_NAME = {
    '401000000': 'Abassa',
    '402000000': 'Andaba',
    '414000000': 'Aventurado',
    '403000000': 'Bequermo',
    '404000000': 'Cortos',
    '405000000': 'Exuma',
    '406000000': 'Fragilles',
    '415000000': 'Jovencito',
    '407000000': 'Juntos',
    '408000000': 'Kokojillo',
    '409000000': 'Levanta',
    '413000000': 'Marineros',
    '410000000': 'Nocivo',
    '416000000': 'Poderoso',
    '411000000': 'Sabada',
    '412000000': 'Valor'
}

STATUS_ALIVE_SRV_EMOJI =   1
STATUS_MESSAGE_SRV_EMOJI = 2
STATUS_UPDATE_SRV_EMOJI = 4
STATUS_ERROR_SRV_EMOJI = 8
STATUS_FATAL_SRV_EMOJI = 16
STATUS_UNKNOWN_SRV_EMOJI = 32

SRV_CODE_TO_EMOJI = {
    STATUS_ALIVE_SRV_EMOJI:   ":green_circle:",
    STATUS_MESSAGE_SRV_EMOJI: ":yellow_circle:",
    STATUS_UPDATE_SRV_EMOJI:  ":yellow_circle:",
    STATUS_ERROR_SRV_EMOJI:   ":red_circle:",
    STATUS_FATAL_SRV_EMOJI:   ":red_circle:",
    STATUS_UNKNOWN_SRV_EMOJI: ":red_circle:"
}

STATUS_ALIVE_GLOB_EMOJI = 1
STATUS_MESSAGE_GLOB_EMOJI = 2
STATUS_UPDATE_GLOB_EMOJI = 3
STATUS_ERROR_GLOB_EMOJI = 4
STATUS_FATAL_GLOB_EMOJI = 5
STATUS_UNKNOWN_GLOB_EMOJI = 6

GLOB_CODE_TO_EMOJI = {
    STATUS_ALIVE_GLOB_EMOJI:   ":green_circle:",
    STATUS_MESSAGE_GLOB_EMOJI: ":yellow_circle:",
    STATUS_UPDATE_GLOB_EMOJI:  ":yellow_circle:",
    STATUS_ERROR_GLOB_EMOJI:   ":red_circle:",
    STATUS_FATAL_GLOB_EMOJI:   ":red_circle:",
    STATUS_UNKNOWN_GLOB_EMOJI: ":red_circle:"
}

EMBED_COLOR = {
    'help': 0x3498db,      # Blue
    'about': 0x9b59b6,     # Purple
    'status': 0x2ecc71,    # Green
    'fullstatus': 0x27ae60, # Dark Green
    'oceans': 0x1abc9c,    # Turquoise
    'fleets': 0xe67e22,    # Orange
    'invasions': 0xe74c3c, # Red
    'notices': 0xf1c40f,   # Yellow
    'error': 0xff0000,     # Bright Red
    'warning': 0xf39c12,   # Amber
    'offline': 0x95a5a6    # Gray
}

FORMAT_STRINGS = {
    'bold': '**%s**',
    'server_status': '**%s**:  %s\n',
    'notice_format': '\n**%s** | %s\n**%s:** *%s*\n'
}

PROTECTED_WORDS = [
    'BotLocalizer',                     #0
    'bot'                               #1
    'Discord',                          #2
    'TLOPO',                            #3
    'The Legend of Pirates Online',     #4
    'TLOPO Discord Bot',                #5
    '"""',                              #6
    'BotLocalizer_',                    #7
    '_AT',                              #8
    'APP_DESCRIPTION = ',               #9
    'OUT_OF_DATE = ',                   #10
    'FLEET_ITEM_INFO = ',               #11
    'INVASION_ITEM_INFO = ',            #12
    'SYSTEM_STATUS_INFO = ',            #13
    'OVER_ALL_STATUS = ',               #14
    'EMBED_TITLES = ',                  #15
    'FIELD_NAMES = ',                   #16
    'STATUS_MESSAGES = ',               #17
    'MISC = ',                          #18
    'STATUS_ALIVE_SRV = 1',             #19
    'STATUS_MESSAGE_SRV = 2',           #20
    'STATUS_UPDATE_SRV = 4',            #21
    'STATUS_ERROR_SRV = 8',             #22
    'STATUS_FATAL_SRV = 16',            #23
    'STATUS_UNKNOWN_SRV = 32',          #24
    'SRV_CODE_TO_STATUS = ',            #25
    'STATUS_ALIVE_GLOB = 1',            #26
    'STATUS_MESSAGE_GLOB = 2',          #27
    'STATUS_UPDATE_GLOB = 3',           #28
    'STATUS_ERROR_GLOB = 4',            #29
    'STATUS_FATAL_GLOB = 5',            #30
    'STATUS_UNKNOWN_GLOB = 6',          #31
    'GLOB_CODE_TO_STATUS = ',           #32
    '[',                                #33
    ']',                                #34
    '{',                                #35
    '}',                                #36
    '<3',                               #37
    r'%s',                              #38
    "'''",                              #39
    '**',                               #40
    '\\n',                              #41
    'https://tlopo.com/',               #42
    'https://github.com/TheLegendofPiratesOnline/discord-bot/issues',       #43
    'https://github.com/TheLegendofPiratesOnline/discord-bot',              #44
    '    ',                             #45
    'STATUS_ALIVE_SRV:',                #46
    'STATUS_MESSAGE_SRV:',              #47
    'STATUS_UPDATE_SRV:',               #48
    'STATUS_ERROR_SRV:',                #49
    'STATUS_FATAL_SRV:',                #50
    'STATUS_UNKNOWN_SRV:',              #51
    'STATUS_ALIVE_GLOB:',               #52
    'STATUS_MESSAGE_GLOB:',             #53
    'STATUS_UPDATE_GLOB:',              #54
    'STATUS_ERROR_GLOB:',               #55
    'STATUS_FATAL_GLOB:',               #56
    'STATUS_UNKNOWN_GLOB:',             #57
    'prod-gs-1.tlopo.com',              #58
    'AUTO_TRANSLATE_WARNING'            #59
]