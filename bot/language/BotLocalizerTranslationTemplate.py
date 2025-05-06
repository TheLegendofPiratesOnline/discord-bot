APP_DESCRIPTION = "Discord bot by TLOPO. <3 \n https://github.com/TheLegendofPiratesOnline/discord-bot"    

OUT_OF_DATE = "This bot is out of date. Please update by visiting https://github.com/TheLegendofPiratesOnline/discord-bot"

AUTO_TRANSLATE_WARNING = "This text has been auto-translated. There may be some errors"

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
    "Commands",
    "About",
    "Ocean Populations",
    "Active Fleets",
    "No active fleets",
    "Active Invasions",
    "No active invasions",
    "Server Notices",
    "Server Status",
    "Server Status Unavailable",
    "Server Notices Unavailable",
    "The Legend of Pirates Online is currently closed for an update"
]

FIELD_NAMES = [
    "Authors",
    "Total",
    "Web Servers",
    "Client Agents",
    "Oceans",
    "Gameserver Functions"
]

STATUS_MESSAGES = [
    "No description available",
    "No authors found.",
    "No active fleet",
    "No active invasion",
    "No known notices.",
    "Ocean population data is unavailable",
    "Fleet data is unavailable",
    "Invasion data is unavailable",
    "Visit https://tlopo.com/ for more information.",
    "Status of prod-gs-1.tlopo.com is being detected incorrectly.\nThis is an issue with the TLOPO API.",
    "Unknown",
    "No data available",
    "Add me to your server!"
]

MISC = [
    "Message",
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