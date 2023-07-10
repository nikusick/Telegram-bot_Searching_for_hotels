from typing import NoReturn

from telebot import TeleBot
from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS, CUSTOM_COMMANDS


def set_default_commands(bot: TeleBot) -> NoReturn:
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS + CUSTOM_COMMANDS]
    )
