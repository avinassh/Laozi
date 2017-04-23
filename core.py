import json

import telegram

from goodreads_api import get_book_details_by_name, BookNotFound
from utils import get_formatted_book_data
from settings import (TELEGRAM_ACCESS_TOKEN, ALLOWED_CHAT_TYPES,
                      ALLOWED_CHAT_IDS)


def bot_handler(data):
    bot = telegram.Bot(token=TELEGRAM_ACCESS_TOKEN)
    try:
        message_id = data['message']['message_id']
        chat_id = data['message']['chat']['id']
        chat_type = data['message']['chat']['type']
        text = data['message']['text']
        print("Received message_id: {}, chat_id: {}, text: {}".format(
            message_id, chat_id, text))

        if chat_type not in ALLOWED_CHAT_TYPES:
            response = ("Laozi is not enabled for this chat type. Contact "
                        "the bot creator to enable.")
            response = response + '\n\n' + json.dumps(data)
            bot.sendMessage(reply_to_message_id=message_id,
                            chat_id=chat_id, text=response,
                            disable_web_page_preview=True,
                            parse_mode='Markdown')
            return

        if chat_id not in ALLOWED_CHAT_IDS:
            response = ("Laozi is now a paid bot and is not enabled for this "
                        "group. To enable, contact the bot creator.")
            response = response + '\n\n' + json.dumps(data)
            bot.sendMessage(reply_to_message_id=message_id,
                            chat_id=chat_id, text=response,
                            disable_web_page_preview=True,
                            parse_mode='Markdown')
            return

        response = parse_command(text=text)
        if response:
            bot.sendMessage(reply_to_message_id=message_id,
                            chat_id=chat_id, text=response,
                            disable_web_page_preview=True,
                            parse_mode='Markdown')
    except KeyError:
        pass
    except telegram.error.TelegramError as e:
        print(data)
        print(e)
    return


def parse_command(text):
    # The telegram usually sends the whole text as something like:
    # '/ping hello' or '/ping@botname hello'
    try:
        command, argument = text.split(' ', 1)
        if command == '/book' or command == '/book@goodreadsbot':
            return get_book_details(book_name=argument)
    except ValueError:
        pass
    return False


def get_book_details(book_name):
    try:
        book_data = get_book_details_by_name(book_name=book_name)
        return get_formatted_book_data(book_data=book_data)
    except BookNotFound:
        return "I couldn't find the book, can you be more precise?"
