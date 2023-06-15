#message_utils.py
import re
import unicodedata

def remove_md_links(text):
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', '', text)

def add_own_link(text, own_link):
    return f"{text}\n\n{own_link}"

def is_emoji(c):
    return unicodedata.category(c) in ["So", "Sm", "Sc", "Sk", "Pc"]

def remove_emojis(text):
    return ''.join(c for c in text if not is_emoji(c))
