from deep_translator import GoogleTranslator
from bot.core import BotGlobals
import re

class BotTranslate:
    """
    If language set in settings file is not found, the language will be translated using Google Translate.
    """
    
    def __init__(self, debug: bool = False):
        self.debug = debug

    def translate_localizer(self, target_language: str):
        """
        Translates the source language file to the target language using Google Translate.

        Args:
            target_language (str): The target language code (e.g., 'es', 'pt', 'fr', etc).
            debug (bool): If True, prints debug information.

        Returns:
            None: Creates a translated file at the specified output path
        """
        output_file = 'bot/language/BotLocalizer_%s_AT.py' % target_language.upper()

        # Set up header documentation
        DATA_TO_BE_TRANSLATED = [
            '"""',
            'The class BotLocalizer_%s_AT is used when providing responses' % target_language,
            'in Discord channels where %s is the spoken language.' % target_language,
            '',
            'All strings in this class have been automatically generated ',
            'into %s as no existing translation existed.' % target_language,
            'There may be some errors in the translation, that you can fix yourself below.',
            '',
            'During the translation some key symbols may be added by accident,',
            'please thoroughly check the translation for any errors after first launch',
            'and report them to https://github.com/TheLegendofPiratesOnline/discord-bot/issues', 
            '"""',
            ''
        ]

        # Add content from template file
        with open('bot/language/BotLocalizerTranslationTemplate.py', 'r', encoding='utf-8') as template_file:
            template_file_lines = template_file.readlines()

            for i, line in enumerate(template_file_lines):
                if line == '':
                    DATA_TO_BE_TRANSLATED.append('\n')
                else:
                    DATA_TO_BE_TRANSLATED.append(line)

                if self.debug == True:
                    print('[DEBUG] Adding line %s: %s to DATA_TO_BE_TRANSLATED' % (i, line))

        template_file.close()

        # Create the translated file
        with open(output_file, 'w', encoding='utf-8') as translated_file:
            for i, line in enumerate(DATA_TO_BE_TRANSLATED):
                if line == '':
                    translated_file.write('\n')
                else:
                    line = self.protect_words(line)
                    translated_line = GoogleTranslator(source='en', target=target_language).translate(line)
                    translated_file.write(translated_line + '\n')

                if self.debug == True:
                    print('[DEBUG] Adding line %s: %s to file' % (i, translated_line))

        translated_file.close()
        self.clean_translation_errors(output_file, 1)
        self.restore_protected_words(output_file)
        self.clean_translation_errors(output_file, 2)

    def clean_translation_errors(self, file_path: str,stage: int):
        """
        Cleans up common translation and formatting errors from the generated file.
        
        Args:
            file_path (str): Path to the translated file
            stage (int): What pattern stage to clean up
            debug (bool): Enable debug output
        """
        # Fix broken placeholders
        STAGE_ONE_REGEX = {
            r'\s*(\d+)\s*': r'\1'       # Removes spaces around digits
        }

        # Clean up syntax errors caused by translation - expand as more errors are reported
        # DO NOT REORDER
        STAGE_TWO_REGEX = {
            r'_{2,}': '',               # Removes extra underscores
            r',{2,}': ',',              # Replaces multiple commas with a single comma
            r'«': r"'",                 # Replaces left guillemet with single quote
            r'»': r"'",                 # Replaces right guillemet with single quote
            r'(?<!")".\n': r'",\n'      # Adds comma after quoted string at end of line if missing
        }


        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
                if self.debug:
                    print('[DEBUG] Reading file: %s' % file_path)

            # Stage 1: Basic placeholder fixes
            if stage == 1:
                for pattern, replacement in STAGE_ONE_REGEX.items():
                    file_content = re.sub(pattern, replacement, file_content, flags=re.MULTILINE)

                    if self.debug:
                        print('[DEBUG][STAGE 1] Replacing pattern: %s with %s' % (pattern, replacement))

            # Stage 2: More complex syntax fixes (run after protected words are restored)
            elif stage == 2:
                for pattern, replacement in STAGE_TWO_REGEX.items():
                    file_content = re.sub(pattern, replacement, file_content, flags=re.MULTILINE)

                    if self.debug:
                        print('[DEBUG][STAGE 2] Replacing pattern: %s with %s' % (pattern, replacement))
            else:
                print('[ERROR] Invalid stage number: %s' % stage)
                return
            
            # Write cleaned content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
                if self.debug:
                    print('[DEBUG] Writing cleaned content to file: %s' % file_path)

            f.close()

        except Exception as e:
            print('[ERROR] Failed to clean translation errors: %s' % str(e))

    def protect_words(self, line: str) -> str:
        """
        Protects words in the line by replacing them with placeholders.
        
        Args:
            line (str): The line containing words to protect
            
        Returns:
            str: Line with protected words replaced by placeholders
        """

        for i, word in enumerate(BotGlobals.PROTECTED_WORDS):
            if word in line:
                line = line.replace(word, '__%s__' % i)

                if self.debug:
                    print('[DEBUG] Protecting word: %s with placeholder: __%s__' % (word, i))
        return line

    def restore_protected_words(self, file_path: str):
        """
        Restores protected words from their placeholders.

        Args:
            file_path (str): Path to the translated file
            debug (bool): Enable debug output
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
                if self.debug:
                    print('[DEBUG] Reading file: %s' % file_path)
            
            restored_file_content = file_content
            for i, word in enumerate(BotGlobals.PROTECTED_WORDS):
                
                POSSIBLE_PATTERNS = [
                    '__%s__' % i
                ]

                for pattern in POSSIBLE_PATTERNS:
                    if pattern in restored_file_content:
                        restored_file_content = restored_file_content.replace(pattern, word)

                        if self.debug:
                            print('[DEBUG] Replacing pattern: %s with %s' % (pattern, word))

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(restored_file_content)
                if self.debug:
                    print('[DEBUG] Writing restored content to file: %s' % file_path)
            
            f.close()
        
        except Exception as e:
            print('[ERROR] Failed to restore protected words: %s' % str(e))