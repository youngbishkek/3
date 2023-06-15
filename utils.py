# utils.py
import re

FORBIDDEN_WORDS = ['Замай', 'слово2', 'слово3']  # Замените на свои запрещенные слова

def remove_links(text):
    return re.sub(r'\[.*?\]\(.*?\)', '', text)

def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # смайлики эмодзи
                               u"\U0001F300-\U0001F5FF"  # символы и пиктограммы
                               u"\U0001F680-\U0001F6FF"  # транспорт и символы карт
                               u"\U0001F1E0-\U0001F1FF"  # национальные флаги
                               u"\U00002702-\U000027B0"  # родительные символы
                               u"\U000024C2-\U0001F251" 
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text)

def contains_channel_name(text):
    return re.search(r'(^|\s)(@[\w\d_]+|t.me/[\w\d_]+)', text)

def contains_moderated_content(text):
    return re.search(r'(@[\w\d_]+|t.me/[\w\d_]+)', text)

def contains_forbidden_words(text):
    for word in FORBIDDEN_WORDS:
        if re.search(r'\b{}\b'.format(re.escape(word)), text, re.IGNORECASE):
            return True
    return False
