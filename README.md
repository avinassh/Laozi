# Laozi

Laozi is a Goodreads bot for Telegram and currently it powers `@goodreadsbot`.

## Deployment

Currently the bot can be hosted on Heroku. Set the following environment variables in Heroku app:

- `TELEGRAM_ACCESS_TOKEN` - Bot access token. You can get this from `@BotFather`
- `GOODREADS_API_KEY` - API key to access Goodreads
- `WEBHOOK_URL` - Set it as `https://your-app-name.herokuapp.com/duh`


Once deployed, visit `/setwebhook` like, `https://your-app-name.herokuapp.com/setwebhook`. You should see `Webhook has been successfully set`. 