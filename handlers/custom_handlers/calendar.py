import datetime

from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from loader import bot
from site_API.rapidapi import get_cheapest_hotels
from states.custom_states import LowStates


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=LowStates.day_in)
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
            data['day_in'] = result
        bot.edit_message_text(f"Дата въезда: {result}",
                              c.message.chat.id,
                              c.message.message_id)
        bot.set_state(c.from_user.id, LowStates.day_out, c.message.chat.id)
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(c.message.chat.id, 'Дата выезда', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=LowStates.day_out)
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
            data['day_out'] = result
        bot.edit_message_text(f"Дата выезда: {result}",
                              c.message.chat.id,
                              c.message.message_id)
        with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
            hotels = get_cheapest_hotels(city=data['city'], quantity_search=data['count_of_notes'],
                                         day_in=data['day_in'],
                                         day_out=data['day_out'])
            if hotels is None:
                bot.send_message(c.message.chat.id, 'По Вашему запросу ничего не найдено(')
            else:
                for hotel in hotels:
                    caption = f'{hotel.get("name")}\n' \
                              f'Адрес: {hotel.get("address", "Не указан")}\n' \
                              f'Рейтинг: {hotel.get("rate", "Не указан")}\n' \
                              f'Цена за ночь: {hotel.get("price")}'
                    images = [types.InputMediaPhoto(img_url) for img_url in hotel.get('images')]
                    images[0].caption = caption
                    bot.send_media_group(c.message.chat.id, images)
        bot.delete_state(c.message.from_user.id, c.message.chat.id)
