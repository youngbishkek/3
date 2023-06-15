#message_copy.py
import time
import re
from telethon import types
from message_utils import remove_md_links, remove_emojis, add_own_link

def contains_blacklisted_word(text, blacklist):
    for word in blacklist:
        if re.search(word, text, re.IGNORECASE):
            return True
    return False

async def handle_new_message(client, message, own_link, lightning_emoji, destination_channel, source_channel):
    blacklist = ["#реклама", "#Прямосейчас", "#ГлавныесобытияТАС", "#промо"]  # Список запрещенных слов

    new_message_text = message.text

    if contains_blacklisted_word(new_message_text, blacklist):
        print(f"Сообщение содержит запрещенное слово. Пропуск ID: {message.id}.")
        return

    # Удаляем Markdown ссылки из текста сообщения
    new_message_text = remove_md_links(new_message_text)

    # Проверяем наличие прямых ссылок на Telegram-каналы в тексте сообщения
    if re.search(r"(?:https?://)?t(?:elegram)?\.me/(?:joinchat/)?[a-zA-Z0-9_-]+", new_message_text):
        print(f"Сообщение содержит прямую ссылку на Telegram-канал. Пропуск ID: {message.id}.")
        return

    # Удаляем все emoji из текста сообщения
    new_message_text = remove_emojis(new_message_text)

    if new_message_text.strip() or message.media:
        # Удаляем пробел перед эмодзи молнии
        new_message_text_with_link = add_own_link(new_message_text.lstrip(), own_link)

        # Добавляем эмодзи молнии перед сообщением с уменьшенным пробелом
        new_message_text_with_emoji = f"{lightning_emoji} {new_message_text_with_link}"

        if isinstance(message, types.Message) and message.media:
            time.sleep(5)  # Задержка в 5 секунд перед копированием сообщения

            # Проверяем, существует ли сообщение после окончания таймера
            messages_after_delay = await client.get_messages(source_channel, ids=[message.id])
            if messages_after_delay and messages_after_delay[0] and messages_after_delay[0].media:
                if message.photo:
                    await client.send_file(destination_channel, message.photo, caption=new_message_text_with_emoji)
                elif message.video:
                    await client.send_file(destination_channel, message.video, caption=new_message_text_with_emoji)
                elif message.document:
                    await client.send_file(destination_channel, message.document, caption=new_message_text_with_emoji)
                else:
                    await client.send_message(destination_channel, new_message_text_with_emoji)
                print(f"Скопировано сообщение ID: {message.id}.")
            else:
                print(f"Сообщение удалено ID: {message.id}.")

        else:
            time.sleep(5)  # Задержка в 5 секунд перед копированием сообщения

            # Проверяем, существует ли сообщение после окончания таймера
            messages_after_delay = await client.get_messages(source_channel, ids=[message.id])
            if messages_after_delay and messages_after_delay[0] and messages_after_delay[0].media:
                await client.send_message(destination_channel, new_message_text_with_emoji)
                print(f"Скопировано сообщение ID: {message.id}.")
            else:
                print(f"Сообщение удалено ID: {message.id}.")
