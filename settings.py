import os

TELEGRAM_ACCESS_TOKEN = os.environ['TELEGRAM_ACCESS_TOKEN']
GOODREADS_API_KEY = os.environ['GOODREADS_API_KEY']
GOOGLE_DEV_API_KEY = os.environ['GOOGLE_DEV_API_KEY']
GOOGLE_CUSTOM_SEARCH_CX = os.environ['GOOGLE_CUSTOM_SEARCH_CX']

# Telegram Webhook settings
WEBHOOK_URL = os.environ['WEBHOOK_URL']

# Group restrictions
# Chat is either private message or group chat
# allowing Laozi only in groups but not in `private` or `channel`
ALLOWED_CHAT_TYPES = ['group', 'supergroup']
# Laozi will interact only with following Chat groups or private ids
ALLOWED_CHAT_IDS = [-1001091893296, -1001013427720, -1001015833661]
