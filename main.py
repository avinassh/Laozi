import telegram
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from goodreads_api import get_book_details_by_name, BookNotFound
from utils import get_formatted_book_data
from settings import TELEGRAM_ACCESS_TOKEN, WEBHOOK_URL

define("port", default=5000, help="run on the given port", type=int)

bot = telegram.Bot(token=TELEGRAM_ACCESS_TOKEN)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('wink, wink')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('wink, wink')

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        try:
            message_id = data['message']['message_id']
            chat_id = data['message']['chat']['id']
            text = data['message']['text']
            chat_type = data['message']['chat']['type']

            if not chat_type == 'group':
                return

            response = parse_command(text=text)
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


class WebHookHandler(tornado.web.RequestHandler):
    def get(self):
        # one time only operation
        response = bot.setWebhook(WEBHOOK_URL)
        if not response:
            return self.write('Setting up webhook has failed')
        return self.write('Webhook has been successfully set')


def parse_command(text):
    # The telegram usually sends the whole text as something like:
    # '/ping hello' or '/ping@botname hello'
    try:
        command, argument = text.split(' ', 1)
        if command == '/book' or command == '/book@goodreadsbot':
            return get_book_details(book_name=argument)
    except ValueError:
        pass
    return 'Invalid command'


def get_book_details(book_name):
    try:
        book_data = get_book_details_by_name(book_name=book_name)
        return get_formatted_book_data(book_data=book_data)
    except BookNotFound:
        return "I couldn't find the book, can you be more precise?"


def make_app():
    return tornado.web.Application([
        (r'/', IndexHandler),
        (r'/duh', MainHandler),
        (r'/setwebhook', WebHookHandler)
    ])


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
