import datetime

from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar

from states.custom_states import LowStates

from loader import bot

from site_API.rapidapi import get_cheapest_hotels

import telegram_bot_calendar

@bot.message_handler(state='*', commands=['low'])
def ask_city(message):
    """
    State 1. Will process when user's state is LowStates.city.
    """
    bot.set_state(message.from_user.id, LowStates.city, message.chat.id)
    bot.send_message(message.chat.id, 'Какой город Вас интересует?')


@bot.message_handler(state=LowStates.city)
def get_city(message):
    """
    State 2. Will process when user's state is LowStates.city.
    """
    bot.set_state(message.from_user.id, LowStates.count_of_notes, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
    bot.send_message(message.chat.id, 'Сколько номеров показать?')


@bot.message_handler(state=LowStates.count_of_notes, is_digit=True)
def get_count_of_notes(message):
    """
    State 3. Will process when user's state is LowStates.count_of_notes.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['count_of_notes'] = int(message.text)
    bot.set_state(message.from_user.id, LowStates.day_in, message.chat.id)
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(message.chat.id, 'Дата въезда', reply_markup=calendar)


'''@bot.message_handler(state=LowStates.day_in)
def get_day_in(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['day_in'] = datetime.datetime.strptime(message.text, "%d%m%Y").date()
    bot.set_state(message.from_user.id, LowStates.day_out, message.chat.id)
    bot.send_message(message.chat.id, 'Дата выезда')


@bot.message_handler(state=LowStates.day_out)
def get_day_out(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['day_out'] = datetime.datetime.strptime(message.text, "%d%m%Y").date()
    bot.set_state(message.from_user.id, LowStates.day_out, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        hotels = get_cheapest_hotels(city=data['city'], quantity_search=data['count_of_notes'], day_in=data['day_in'],
                                     day_out=data['day_out'])
        if hotels is None:
            bot.send_message(message.chat.id, 'По Вашему запросу ничего не найдено(')
        else:
            for hotel in hotels:
                caption = f'{hotel.get("name")}\n' \
                          f'Адрес: {hotel.get("address", "Не указан")}\n' \
                          f'Рейтинг: {hotel.get("rate", "Не указан")}'
                images = [types.InputMediaPhoto(img_url) for img_url in hotel.get('images')]
                images[0].caption = caption
                bot.send_media_group(message.chat.id, images)
    bot.delete_state(message.from_user.id, message.chat.id)
'''

@bot.message_handler(state=LowStates.count_of_notes, is_digit=False)
def age_incorrect(message):
    """
    Wrong response for LowStates.count_of_notes
    """
    bot.send_message(message.chat.id, 'Похоже, Вы ввели не число. Повторите, пожалуйста, ввод!')
