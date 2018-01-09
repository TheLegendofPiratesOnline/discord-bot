# Filename: BotLocalizer.py
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
The class BotLocalizer will select which language
to use when providing responses in Discord channels.

There are corresponding files to this class which
will contain the actual strings in their respective
language.

Those files will have the same name as this class +
the language they are in.  For example, BotLocalizerEnglish.
"""

def importLanguageModule(module):
    """
    Imports other language modules and places them
    into the globals.
    """

    try:
        x = __import__(module, {}, {}, ['bot.language'])
    except ImportError:
        x = __import__('bot.language.BotLocalizerEnglish', {}, {}, ['bot.language'])
    globals().update(x.__dict__)

## TODO: Process other languages from settings.
importLanguageModule('English')
