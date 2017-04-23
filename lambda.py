import json

import telegram

from goodreads_api import get_book_details_by_name, BookNotFound
from utils import get_formatted_book_data
from settings import TELEGRAM_ACCESS_TOKEN


def lambda_handler(event, context):
    bot = telegram.Bot(token=TELEGRAM_ACCESS_TOKEN)
    data = json.loads(event['body'])

    try:
        message_id = data['message']['message_id']
        chat_id = data['message']['chat']['id']
        text = data['message']['text']
        print("Received message_id: {}, chat_id: {}, text: {}".format(
            message_id, chat_id, text))
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
