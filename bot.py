#bot.py
import asyncio
import re
import unicodedata
from telethon.sync import TelegramClient
from telethon.events import NewMessage
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from config import api_id, api_hash, phone_number, source_channel_id, destination_channel_id, hidden_link_text, hidden_link_url, COPY_DELAY

def remove_md_links(text):
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', '', text)

def add_own_link(text, own_link):
    return f"{text}\n\n{own_link}"

def is_emoji(c):
    return unicodedata.category(c) in ["So", "Sm", "Sc", "Sk", "Pc"]

def remove_emojis(text):
    return ''.join(c for c in text if not is_emoji(c))

def contains_tg_link(text):
    return re.search(r'(https?:\/\/)?t\.me\/\w+', text) is not None

def contains_blacklisted_words(text):
    blacklist = ["#реклама", "#Прямосейчас", "#ГлавныесобытияТАС", "#промо"]
    return any(word in text for word in blacklist)

async def copy_messages():
    client = TelegramClient('session_name', api_id, api_hash)

    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            await client.sign_in(phone_number, input('Введите код подтверждения: '))

        source_channel = await client.get_entity(source_channel_id)
        destination_channel = await client.get_entity(destination_channel_id)

        own_link = f"[{hidden_link_text}]({hidden_link_url})"
        lightning_emoji = "⚡️"

        async def handle_new_message(event):
            message = event.message

            new_message_text = message.text

            new_message_text = remove_md_links(new_message_text)
            new_message_text = remove_emojis(new_message_text)

            if contains_tg_link(new_message_text) or contains_blacklisted_words(new_message_text):
                print(f"Пропущено сообщение ID: {message.id} с запрещенным содержимым.")
                return

            if new_message_text.strip() or message.media:
                new_message_text_with_link = add_own_link(new_message_text.lstrip(), own_link)
                new_message_text_with_emoji = f"{lightning_emoji} {new_message_text_with_link}"

                await asyncio.sleep(COPY_DELAY)

                if message.media:
                    if isinstance(message.media, MessageMediaPhoto):
                        await client.send_message(destination_channel, new_message_text_with_emoji, file=message.media.photo)
                    elif isinstance(message.media, MessageMediaDocument):
                        await client.send_message(destination_channel, new_message_text_with_emoji, file=message.media.document)
                    else:
                        await client.send_message(destination_channel, new_message_text_with_emoji)
                else:
                    await client.send_message(destination_channel, new_message_text_with_emoji)

                print(f"Скопировано сообщение ID: {message.id}.")
            else:
                print(f"Пропущено пустое сообщение ID: {message.id}.")

        client.add_event_handler(handle_new_message, NewMessage(chats=source_channel))

        try:
            await client.run_until_disconnected()
        finally:
            pass

    finally:
        await client.disconnect()

asyncio.run(copy_messages())
