"""
If language set in settings file is not found, the language will be translated using Google Translate.
This should only be used at the initialization of the bot to create a temporary language file.
"""

from deep_translator import GoogleTranslator
from bot.core import BotGlobals
import re

# Cant belive i learned regex for this at 3 am............ 
# POV: its 4am and you finally got regex somewhat working XP
def clean_translation_errors(file_path: str, debug: bool = False):
    """
    Cleans up common translation and formatting errors from the generated file.
    
    Args:
        file_path (str): Path to the translated file
        debug (bool): Enable debug output
    """
    cleanup_patterns = {
        # Compound placeholders with text between them
        r'__(\d+)__([a-z]+)__(\d+)__': r'__\1__ \2 __\3__',
        
        # Adjacent placeholders handling
        r'__(\d+)____(\d+)____(\d+)__': r'__\1__ __\2__ __\3__',
        r'__(\d+)____(\d+)__': r'__\1__ __\2__',
        
        # Numbers in placeholders
        r'__(\d+)__(\d+)__(\d+)__': r'__\1__ __\2__ __\3__',
        r'__(\d+)__(\d+)__': r'__\1__ __\2__',
        
        # Basic placeholder formatting
        r'_{3,}(\d+)_{1,}': r'__\1__',
        r'_{1,}(\d+)_{3,}': r'__\1__',
        r'_(\d+)_': r'__\1__',
        r'_{1,}(\d+)': r'__\1__',
        r'(\d+)_{1,}': r'__\1__',
        
        # Spacing issues
        r'__(\d+)\s+__': r'__\1__',
        r'__\s+(\d+)__': r'__\1__',
        
        # Quotes and general formatting
        r'"{2,}': '"',
        r"'{2,}": "'",
        r'"\s*,\s*"': '", "',
        r"'\s*,\s*'": "', '",
        r'\s*,\s*,+': ',',
        r'\s*\.\s*\.+': '.',
        r'\s+\n': '\n',
        r'\n{3,}': '\n\n'
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            if debug == True:
                print('[DEBUG] Reading file: %s' % file_path)
        
        for pattern, replacement in cleanup_patterns.items():
            file_content = re.sub(pattern, replacement, file_content, flags=re.MULTILINE)

            if debug == True:
                print('[DEBUG] Replacing pattern: %s with %s' % (pattern, replacement))
        
        # Write cleaned content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
            if debug == True:
                print('[DEBUG] Writing cleaned content to file: %s' % file_path)

        # Sanity pass ---------- bcs i swear im so close to throwing my computer out the window
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Special case fixes ------------- i present the reason i nearly threw my computer out the window
        # Enhanced final fixes with proper spacing between placeholders
        final_fixes = content
        # Fix cases where placeholders are touching
        final_fixes = re.sub(r'__(\d+)____(\d+)__', r'__\1__ __\2__', final_fixes)
        final_fixes = re.sub(r'__(\d+)____(\d+)____(\d+)__', r'__\1__ __\2__ __\3__', final_fixes)
        # Fix placeholders with text between them
        final_fixes = re.sub(r'__(\d+)__([a-z]+)__(\d+)__', r'__\1__ \2 __\3__', final_fixes)
        # Fix trailing/leading placeholder issues
        final_fixes = re.sub(r'[_]{2,}(\d+)[_]{0,3}([^_])', r'__\1__\2', final_fixes)
        final_fixes = re.sub(r'([^_])[_]{0,3}(\d+)[_]{2,}', r'\1__\2__', final_fixes)
        # One more pass on adjacent placeholders
        final_fixes = re.sub(r'__(\d+)__(\d+)__', r'__\1__ __\2__', final_fixes)

        if content != final_fixes:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(final_fixes)
                if debug:
                    print('[DEBUG] Applied final safety fixes')
    
    except Exception as e:
        print('[ERROR] Failed to clean translation errors: %s' % str(e))

def protect_words(line: str):
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
    return line

def restore_protected_words(file_path: str, debug: bool = False):
    """
    Restores protected words from their placeholders.

    Args:
        file_path (str): Path to the translated file
        debug (bool): Enable debug output
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            if debug == True:
                print('[DEBUG] Reading file: %s' % file_path)
        
        restored_file_content = file_content
        for i, word in enumerate(BotGlobals.PROTECTED_WORDS):
            POSSIBLE_PATTERNS = [
                '__%s__' % i
            ]
            for pattern in POSSIBLE_PATTERNS:
                if pattern in restored_file_content:
                    restored_file_content = restored_file_content.replace(pattern, word)

                    if debug == True:
                        print('[DEBUG] Replacing pattern: %s with %s' % (pattern, word))

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(restored_file_content)
            if debug == True:
                print('[DEBUG] Writing restored content to file: %s' % file_path)
    
    except Exception as e:
        print('[ERROR] Failed to restore protected words: %s' % str(e))


def final_fixes(file_path: str, debug: bool = False):
    """
    Apply manual fixes for very specific issues that regex can't handle well.
    
    Args:
        file_path (str): Path to the translated file
        debug (bool): Enable debug output
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Fix APP_DESCRIPTION line with broken placeholders
        content = re.sub(
            r'APP_DESCRIPTION\s*=\s*__\s*"([^"]+)"\s*__\s*__\s*', 
            r'APP_DESCRIPTION = "\\1"', 
            content
        )
        
        # Fix array items with placeholders inside quotes
        content = re.sub(
            r"__'__\s*([^']+)", 
            r"'\\1", 
            content
        )
        
        # Fix missing quotes in SYSTEM_STATUS_INFO
        if "SYSTEM_STATUS_INFO = '''" in content and not "SYSTEM_STATUS_INFO = '''%s" in content:
            content = content.replace(
                "SYSTEM_STATUS_INFO = '''", 
                "SYSTEM_STATUS_INFO = '''%s"
            )
            
        # Write fixed content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            if debug:
                print('[DEBUG] Applied manual fixes')
                
    except Exception as e:
        print('[ERROR] Failed to apply manual fixes: %s' % str(e))

def translate(target_language: str, debug: bool = False):
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

            if debug == True:
                print('[DEBUG] Adding line %s: %s to DATA_TO_BE_TRANSLATED' % (i, line))

    template_file.close()

    # Create the translated file
    with open(output_file, 'w', encoding='utf-8') as translated_file:
        for i, line in enumerate(DATA_TO_BE_TRANSLATED):
            if line == '':
                translated_file.write('\n')
            else:
                line = protect_words(line)
                translated_line = GoogleTranslator(source='en', target=target_language).translate(line)
                translated_file.write(translated_line + '\n')

            if debug == True:
                print('[DEBUG] Adding line %s: %s to file' % (i, translated_line))

    translated_file.close()
    
    # Post-processing to clean up translation artifacts
    clean_translation_errors(output_file, debug)
    restore_protected_words(output_file, debug)
    final_fixes(output_file, debug)  # its 5am. i want to cry. this is why i refused to learn regex.

translate('de', True)     #TESTING ONLY - REMOVE LATER
#clean_translation_errors('bot/language/BotLocalizer_DE_AT.py', debug=True)  #TESTING ONLY - REMOVE LATER