import telegram
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from settings import WEBHOOK_URL, TELEGRAM_ACCESS_TOKEN
from core import bot_handler

define("port", default=5000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('wink, wink')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('wink, wink')

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        self.set_status(200)
        return bot_handler(data=data)


class WebHookHandler(tornado.web.RequestHandler):
    def get(self):
        # one time only operation
        bot = telegram.Bot(token=TELEGRAM_ACCESS_TOKEN)
        response = bot.setWebhook(WEBHOOK_URL)
        if not response:
            return self.write('Setting up webhook has failed')
        return self.write('Webhook has been successfully set')


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
