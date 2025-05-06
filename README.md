# TLOPO Discord Bot
Public discord bot that utilizes [TLOPO's APIs](https://thelegendofpiratesonline.github.io/documentation/).

## Commands
| Command | Description |
|---------|-------------|
| !fullstatus | Returns current server status with more details. |
| !invasions | Returns active invasions. |
| !help | Returns a list of commands. |
| !about | Returns information about bot. |
| !status | Returns current server status. |
| !fleets | Returns active fleets. |
| !notices | Returns any server notices. |
| !oceans | Returns server populations. |

*default command prefix used to show commands*

## Prerequisites
In order to run this Discord bot, you need to have Python 3 installed on your system. You can grab the latest version from [here](https://www.python.org/downloads/).

## Installation
The following procedure documents how to install the TLOPO Discord Bot:

1. Open a new instance of Terminal (UNIX/Mac) or Command Prompt (Windows).
2. Change your current working directory to the TLOPO Discord Bot source code.
3. Run the following command to install the dependencies that the bot needs to run:

    `python3 -m pip install -r requirements.txt`

## Setup
The following outlines how to setup settings.json:

1. Add your Discord Bot API token to [appToken](settings.json)
2. Select the language the bot should output most text in. To select what language you want to use enter the language abreviation into [language](settings.json). Currently the officially supported languages are:
    - English (en-us)
    - Portuguese(Portugal) (pt-pt)

    If you would prefer the bot to output in a different language it does a have an auto-translate feature built in. Just enter the full language name into [language](settings.json), and set [autoTranslate](settings.json) to `True`.
3. Set what prefix you would like to use before each bot command by changing [commandPrefix](settings.json).
4. If you wish for others users to add the bot to their discord servers you can set the installation link in [link](settings.json), and set [showLink](settings.json) to `True`.
The link will be shown in the bots `!about` command.

### For developers
We recommend setting [debug](settings.json) to `True`, and setting [suppessWarnings](settings.json) to `False`, to output debug logs and warnings to the console.

## Starting the Bot
The following outlines how to start the bot:

*If you have not closed your instance of Terminal (UNIX/Mac) or Command Prompt (Windows) you can skip steps 1 and 3*

1. Open a new instance of Terminal (UNIX/Mac) or Command Prompt (Windows).
2. Change your current working directory to the TLOPO Discord Bot source code.
3. Run the following command to start the bot:

    `python3 -m bot.core.BotStart`

#### If using an auto-translated language for the first time
The start up will take longer than usual as it generates the new translation, so do not panic if it looks like nothing is happening, as it can take some time depending on the language.
This will only take a long time on the first run

## License
This bot is currently available under the Modified BSD license (BSD 3-Clause). The terms of this license are available in the [LICENSE](LICENSE) file of this archive.
