import json

from core import bot_handler


def lambda_handler(event, context):
    return bot_handler(data=json.loads(event['body']))
