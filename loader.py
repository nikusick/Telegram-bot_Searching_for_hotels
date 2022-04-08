from dotenv import load_dotenv
import telebot

from pathlib import Path
import os

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
