from . import cancel
from . import low
from . import custom
from . import high

from telebot import custom_filters
from loader import bot


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
