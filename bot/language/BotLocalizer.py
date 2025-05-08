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


from bot.language import BotTranslate

class BotLocalizer:
    """
    The class BotLocalizer will select which language
    to use when providing responses in Discord channels.

    There are corresponding files to this class which
    will contain the actual strings in their respective
    language.

    Those files will have the same name as this class +
    the language they are in.  For example, BotLocalizerEnglish.

    If the language is not found and autoTranslate is set to True,
    the BotTranslate class will be used to translate the 
    source language (english) into the target language.
    """

    def __init__(self, debug: bool = False, auto_translate: bool = False):
        self.debug = debug
        self.autoTranslate = auto_translate

    def importLanguageModule(self, module: str = 'en-us'):
        """
        Imports other language modules and places them
        into the globals.
        """

        translate = BotTranslate.BotTranslate(self.debug)

        global AUTOTRANSLATE_IN_USE
        AUTOTRANSLATE_IN_USE = False

        if self.autoTranslate:
            #check if the module is in the list of supported languages
            try:
                language_modules = {
                    'en-us': 'BotLocalizerEnglish',
                    'pt-pt': 'BotLocalizerPortuguese',
                }

                module_name = 'bot.language.%s' % language_modules.get(module)
                x = __import__(module_name, {}, {}, ['bot.language'])
            
            #check if a translation has already been generated
            except ImportError:
                print(":BotLocalizer: Failed to load %s language, checking for existing translation"  % module)
                try:
                    module_name = 'bot.language.BotLocalizer_%s_AT' % module.upper()
                    x = __import__(module_name, {}, {}, ['bot.language'])
                    AUTOTRANSLATE_IN_USE = True

                #generate a new translation life if one does not exist
                except ImportError:
                    print(":BotLocalizer: Failed to load %s language, generating new translation file" % module)
                    translate.translate_localizer(module)
                    try:
                        module_name = 'bot.language.BotLocalizer_%s_AT' % module.upper()
                        x = __import__(module_name, {}, {}, ['bot.language'])
                        AUTOTRANSLATE_IN_USE = True

                    #if the translation fails, fall back to English
                    except ImportError:
                        print(":BotLocalizer: Failed to load %s language, falling back to English" % module)
                        x = __import__('bot.language.BotLocalizerEnglish', {}, {}, ['bot.language'])
            globals().update(x.__dict__)

        else:
            try:
                language_modules = {
                    'en-us': 'BotLocalizerEnglish',
                    'pt-pt': 'BotLocalizerPortuguese',
                }

                module_name = 'bot.language.%s' % language_modules.get(module, 'BotLocalizerEnglish')
                x = __import__(module_name, {}, {}, ['bot.language'])
            except ImportError:
                print(":BotLocalizer: Failed to load %s language, falling back to English" % module)
                x = __import__('bot.language.BotLocalizerEnglish', {}, {}, ['bot.language'])
            globals().update(x.__dict__)


# Default to English initially
default_localizer = BotLocalizer(False, False)
default_localizer.importLanguageModule('en-us')
# The language will be properly set when BotCore initializes