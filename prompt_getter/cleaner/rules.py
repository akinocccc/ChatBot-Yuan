import re

import emoji

def is_too_long(text):
    return len(text) > 200

def remove_wrap_symbol(text):
    return re.sub(r'\s+', '，', text)

def remove_emoji(text):
    for x in emoji.UNICODE_EMOJI:
        if x in text:
            text = text.replace(x, "")
    return text.strip()


MAX_LEN_EMOJI = max(len(x) for x in emoji.UNICODE_EMOJI.keys()) + 2


def remove_emoji2(utter):
    blacklist = set(emoji.UNICODE_EMOJI.keys())
    # max_len = max(len(x) for x in blacklist)
    all_gram = {
        utter[i: j + 1]
        for i in range(len(utter))
        for j in range(i, min(len(utter), i + MAX_LEN_EMOJI))
    }

    overlap = blacklist & all_gram
    if len(overlap) > 0:
        return overlap.pop()
    return None


def remove_emoji3(text):
    emoji_regex = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002500-\U00002BEF"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"
        "\u3030"
        "\\*\u20e3"
        "#\u20e3"
        "]+",
        flags=re.UNICODE,
    )
    text = emoji_regex.sub(r"", text)
    return text.strip()
