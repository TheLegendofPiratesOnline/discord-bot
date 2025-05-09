from deep_translator import GoogleTranslator
from bot.core import BotGlobals
import re

class BotTranslate:
    """
    If language set in settings file is not found, the language will be translated using Google Translate.
    """
    
    def __init__(self, debug: bool = False, target_language: str = 'en'):
        self.debug = debug
        self.target_language = target_language

    def translate_string(self, text: str) -> str:
        """
        Translates a string to the target language using Google Translate.

        Args:
            text (str): The text to be translated.

        Returns:
            str: The translated text.
        """

        protected_line = self.protect_words(text)
        if self.debug and 'translate_string' in BotGlobals.DEBUG_MODULES:
            print('[DEBUG] Protecting line: %s' % protected_line)

        translated_text = GoogleTranslator(source='en', target=self.target_language).translate(protected_line)
        if self.debug and 'translate_string' in BotGlobals.DEBUG_MODULES:
            print('[DEBUG] Translated line: %s' % translated_text)

        cleaned_translation = self.clean_translation_errors(text=translated_text, stage=1)
        if self.debug and 'translate_string' in BotGlobals.DEBUG_MODULES:
            print('[DEBUG] Cleaned translation: %s' % cleaned_translation)

        restored_translation = self.restore_protected_words(text=cleaned_translation)
        if self.debug and 'translate_string' in BotGlobals.DEBUG_MODULES:
            print('[DEBUG] Restored translation: %s' % restored_translation)

        cleaned_translation= self.clean_translation_errors(text=restored_translation, stage=2)
        if self.debug and 'translate_string' in BotGlobals.DEBUG_MODULES:
            print('[DEBUG] Final cleaned translation: %s' % cleaned_translation)
        return cleaned_translation

    def translate_localizer(self):
        """
        Translates the source language file to the target language using Google Translate.

        Returns:
            None: Creates a translated file at the specified output path
        """
        output_file = 'bot/language/BotLocalizer_%s_AT.py' % self.target_language.upper()

        # Set up header documentation
        DATA_TO_BE_TRANSLATED = [
            '"""',
            'The class BotLocalizer_%s_AT is used when providing responses' % self.target_language,
            'in Discord channels where %s is the spoken language.' % self.target_language,
            '',
            'All strings in this class have been automatically generated ',
            'into %s as no existing translation existed.' % self.target_language,
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

                if self.debug and 'translate_localizer_add_items' in BotGlobals.DEBUG_MODULES:
                    print('[DEBUG] Adding line %s: %s to DATA_TO_BE_TRANSLATED' % (i, line))

        template_file.close()

        # Create the translated file
        with open(output_file, 'w', encoding='utf-8') as translated_file:
            for i, line in enumerate(DATA_TO_BE_TRANSLATED):
                if line == '':
                    translated_file.write('\n')
                else:
                    line = self.protect_words(line)
                    translated_line = GoogleTranslator(source='en', target=self.target_language).translate(line)
                    translated_file.write(translated_line + '\n')

                if self.debug and 'translate_localizer_translate_items' in BotGlobals.DEBUG_MODULES:
                    print('[DEBUG] Adding line %s: %s to file' % (i, translated_line))

        translated_file.close()
        self.clean_translation_errors(file_path=output_file, stage=1)
        self.restore_protected_words(file_path=output_file)
        self.clean_translation_errors(file_path=output_file, stage=2)

    def clean_translation_errors(self, file_path: str=None, text: str=None, stage: int=1) -> str|None:
        """
        Cleans up common translation and formatting errors from the generated file.
        
        Args:
            file_path (str): Path to the translated file
            text (str): Text to clean up
            stage (int): What pattern stage to clean up
        Returns:
            str: Cleaned text\n
            None: If file_path is provided or an error occurs
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

        # Clean up translation errors in the file
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    if self.debug and 'clean_translation_errors' in BotGlobals.DEBUG_MODULES:
                        print('[DEBUG] Reading file: %s' % file_path)

                # Stage 1: Basic placeholder fixes
                if stage == 1:
                    for pattern, replacement in STAGE_ONE_REGEX.items():
                        file_content = re.sub(pattern, replacement, file_content, flags=re.MULTILINE)

                        if self.debug and 'clean_translation_errors_stage_1' in BotGlobals.DEBUG_MODULES:
                            print('[DEBUG][STAGE 1] Replacing pattern: %s with %s' % (pattern, replacement))

                # Stage 2: More complex syntax fixes (run after protected words are restored)
                elif stage == 2:
                    for pattern, replacement in STAGE_TWO_REGEX.items():
                        file_content = re.sub(pattern, replacement, file_content, flags=re.MULTILINE)

                        if self.debug and 'clean_translation_errors_stage_2' in BotGlobals.DEBUG_MODULES:
                            print('[DEBUG][STAGE 2] Replacing pattern: %s with %s' % (pattern, replacement))
                else:
                    print('[ERROR] Invalid stage number: %s' % stage)
                    return
                
                # Write cleaned content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                    if self.debug and 'clean_translation_errors' in BotGlobals.DEBUG_MODULES:
                        print('[DEBUG] Writing cleaned content to file: %s' % file_path)

                f.close()

            except Exception as e:
                print('[ERROR] Failed to clean translation errors: %s' % str(e))
        
        elif text:
            # Stage 1: Basic placeholder fixes
            if stage == 1:
                for pattern, replacement in STAGE_ONE_REGEX.items():
                    text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

                    if self.debug and 'clean_translation_errors_stage_1' in BotGlobals.DEBUG_MODULES:
                        print('[DEBUG][STAGE 1] Replacing pattern: %s with %s' % (pattern, replacement))

                return text

            # Stage 2: More complex syntax fixes (run after protected words are restored)
            elif stage == 2:
                for pattern, replacement in STAGE_TWO_REGEX.items():
                    text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

                    if self.debug and 'clean_translation_errors_stage_2' in BotGlobals.DEBUG_MODULES:
                        print('[DEBUG][STAGE 2] Replacing pattern: %s with %s' % (pattern, replacement))

                return text
            
            else:
                raise ValueError('[ERROR] Invalid stage number: %s' % stage)
                
        elif file_path and text:
            raise ValueError('[ERROR] Both file path and text provided for cleaning. Please provide only one.')
        
        else:
            raise ValueError('[ERROR] No file path or text provided for cleaning. Please provide one.')

    def protect_words(self, line: str) -> str:
        """
        Protects words in the line by replacing them with placeholders.
        
        Args:
            line (str): The line containing words to protect.
            
        Returns:
            str: Line with protected words replaced by placeholders.
        """

        for i, word in enumerate(BotGlobals.PROTECTED_WORDS):
            if word in line:
                line = line.replace(word, '__%s__' % i)

                if self.debug and 'protect_words' in BotGlobals.DEBUG_MODULES:
                    print('[DEBUG] Protecting word: %s with placeholder: __%s__' % (word, i))
        return line

    def restore_protected_words(self, file_path: str=None, text: str=None) -> str|None:
        """
        Restores protected words from their placeholders.

        Args:
            file_path (str): Path to the translated file
            debug (bool): Enable debug output
        """
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    if self.debug and 'restore_protected_words' in BotGlobals.DEBUG_MODULES:
                        print('[DEBUG] Reading file: %s' % file_path)
                
                restored_file_content = file_content
                for i, word in enumerate(BotGlobals.PROTECTED_WORDS):
                    
                    POSSIBLE_PATTERNS = [
                        '__%s__' % i
                    ]

                    for pattern in POSSIBLE_PATTERNS:
                        if pattern in restored_file_content:
                            restored_file_content = restored_file_content.replace(pattern, word)

                            if self.debug and 'restore_protected_words_replacements' in BotGlobals.DEBUG_MODULES:
                                print('[DEBUG] Replacing pattern: %s with %s' % (pattern, word))

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(restored_file_content)
                    if self.debug and 'restore_protected_words' in BotGlobals.DEBUG_MODULES:
                        print('[DEBUG] Writing restored content to file: %s' % file_path)
                
                f.close()
            
            except Exception as e:
                print('[ERROR] Failed to restore protected words: %s' % str(e))
        
        elif text:
            for i, word in enumerate(BotGlobals.PROTECTED_WORDS):
                    
                POSSIBLE_PATTERNS = [
                    '__%s__' % i
                ]

                for pattern in POSSIBLE_PATTERNS:
                    if pattern in text:
                        text = text.replace(pattern, word)

                        if self.debug and 'restore_protected_words_replacements' in BotGlobals.DEBUG_MODULES:
                            print('[DEBUG] Replacing pattern: %s with %s' % (pattern, word))

            return text
        
        elif file_path and text:
            raise ValueError('[ERROR] Both file path and text provided for restoring. Please provide only one.')
        
        else:
            raise ValueError('[ERROR] No file path or text provided for restoring. Please provide one.')