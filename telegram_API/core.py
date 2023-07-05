import telebot

from settings import BotSettings


bot_settings = BotSettings()
TOKEN = bot_settings.bot_token.get_secret_value()
bot = telebot.TeleBot(TOKEN)
