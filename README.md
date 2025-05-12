# TLOPO Discord Bot
Public Discord bot that utilizes [TLOPO's APIs](https://thelegendofpiratesonline.github.io/documentation/).

## Commands
| Command | Description |
|---------|-------------|
| `!help` | Returns a list of all commands. |
| `!news` | Returns latest news articles. |
| `!releases` | Returns latest releases. |
| `!about` | Returns information about the bot. |
| `!status` | Returns current server status. |
| `!fullstatus` | Returns current server status with more details. |
| `!invasions` | Returns active invasions. |
| `!fleets` | Returns active fleets. |
| `!oceans` | Returns server populations. |
| `!notices` | Returns any server notices. |
| `!notifications` | Returns the current news banner on the TLOPO website. |

*Default command prefix used to show commands*

## Prerequisites
To run this Discord bot, you need to have Python 3 installed on your system. You can download the latest version [here](https://www.python.org/downloads/).

## Installation
The following procedure explains how to install the TLOPO Discord Bot:

1. Open a new instance of Terminal (UNIX/macOS) or Command Prompt (Windows).
2. Change your current working directory to the TLOPO Discord Bot source code.
3. Run the following command to install the dependencies required for the bot to run:

    `python3 setup.py`

## Setup
The following outlines how to configure `settings.json`:

1. Add your Discord Bot API token to the `appToken` field in `settings.json`.
2. Select the language the bot should use. To choose a language, enter the language abbreviation in the `language` field. Currently, the officially supported languages are:
    - English (`en-us`)
    - Portuguese (Portugal) (`pt-pt`)

    If you prefer the bot to output in a different language, it has a built-in auto-translate feature. Just enter the full language name into the `language` field, and set `autoTranslate` to `True`.
3. Set your desired command prefix by modifying the `commandPrefix` field.
4. If you want others to be able to add the bot to their Discord servers, set the installation link in the `link` field, and set `showLink` to `True`.  
   The link will be shown in the bot's `!about` command.
5. Set your desired maximum number of releases and news articles to be shown in the `maxReleaseNotes` and `maxNewsAricles` fields in `settings.json`.

## Starting the Bot
The following outlines how to start the bot:

*If you haven't closed your instance of Terminal (UNIX/macOS) or Command Prompt (Windows), you can skip steps 1 and 2.*

1. Open a new instance of Terminal (UNIX/macOS) or Command Prompt (Windows).
2. Change your current working directory to the TLOPO Discord Bot source code.
3. Run the following command to start the bot:

    `python3 -m bot.core.BotStart`

#### Notes on First Run
On first run the bot must generate a few files. This can take a few minutes depending on your settings.

After the first run this delay will not occur again unless:
- You change any of the following settings:
  - `autoTranslate`
  - `language`
  - `maxReleaseNotes`

- You delete any of the following files:
  - `BotLocalizer_<language>_AT.py`
  - `BotReleaseNotes_<language>_<version>.json`

- The system dectects a new release on startup.

## Additional Information
This project is still in active development.

See to see all planned updates read [WIP.md](WIP.md)

### For Developers
We recommend setting `debug` to `True` and `suppressWarnings` to `False` to enable debug logs and console warnings.

When debugging specific modules, see [BotGlobals.py](BotGlobals.py) for the DEBUG_MODULES list and comment out any module that you do not want a debug output for.

Documentation for API on [docs.tlopo.com](https://docs.tlopo.com/) is outdated, refer to [index.html.md](https://github.com/TheLegendofPiratesOnline/documentation/blob/master/source/index.html.md) in the API documentation repository source folder for the still outdated but more up to date documentation.

## License
This bot is currently available under the Modified BSD license (BSD 3-Clause). The terms of this license are available in the [LICENSE](LICENSE) file of this archive.
