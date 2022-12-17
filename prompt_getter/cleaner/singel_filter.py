from prompt_getter.cleaner.rules import *

def main_filter(text):
    if is_too_long(text):
        return ''
    text = remove_wrap_symbol(text)
    text = remove_emoji3(text)
    return text.strip()