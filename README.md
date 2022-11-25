# TLOPO Discord Bot
Public discord bot that utilizes [TLOPO's APIs](https://thelegendofpiratesonline.github.io/documentation/).

## Prerequisites
In order to run this Discord bot, you need to have Python 3 installed on your system. You can grab the latest version from [here](https://www.python.org/downloads/).

## Installation
The following procedure documents how to set up the TLOPO Discord Bot.

1. Open a new instance of Terminal (UNIX/Mac) or Command Prompt (Windows).
2. Change your current working directory to the TLOPO Discord Bot source code.
3. Run the following command to install the dependencies that the bot needs to run: 
`python3 -m pip install -r requirements.txt`
4. Once that has completed, you're ready to start the bot. Use the following command to start:
`python3 -m bot.core.BotStart`
5. You'll be prompted to configure the bot. 
6. Make sure to edit `settings.json` and include the secret key for the App Bot User provided by Discord on the Discord Developers page. Other settings relating to the bot's operation can also be configured here.

## License
This bot is currently available under the Modified BSD license (BSD 3-Clause). The terms of this license are available in the "LICENSE" file of this archive.
