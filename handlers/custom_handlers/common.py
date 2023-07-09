from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from loader import bot
from states.custom_states import CustomStates
from utils.get_query_result import get_result


@bot.message_handler(state='*', commands=['low', 'high', 'custom'])
def ask_city(message):
    bot.set_state(message.from_user.id, CustomStates.city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text
        data['user_id'] = message.from_user.id
    bot.send_message(message.chat.id, 'Какой город Вас интересует?')


@bot.message_handler(state=CustomStates.city)
def get_city_ask_count_of_notes(message):
    bot.set_state(message.from_user.id, CustomStates.count_of_notes, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
    bot.send_message(message.chat.id, 'Сколько номеров показать?')


@bot.message_handler(state=CustomStates.count_of_notes, is_digit=True)
def get_count_of_notes_ask_day_in(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['count_of_notes'] = int(message.text)
    bot.set_state(message.from_user.id, CustomStates.day_in, message.chat.id)
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(message.chat.id, 'Дата въезда', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=CustomStates.day_in)
def get_day_in_ask_day_out(c):
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
        bot.set_state(c.from_user.id, CustomStates.day_out, c.message.chat.id)
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(c.message.chat.id, 'Дата выезда', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=CustomStates.day_out)
def get_day_out(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Дата выезда: {result}",
                              c.message.chat.id,
                              c.message.message_id)
        with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
            data['day_out'] = result
            if data['command'] == '/custom':
                bot.set_state(c.from_user.id, CustomStates.min_price, c.message.chat.id)
                bot.send_message(c.message.chat.id, 'Минимальная цена')
                return
            result = get_result(data)
            if result is None:
                bot.send_message(c.message.chat.id, 'По Вашему запросу ничего не найдено(')
            else:
                for images in result:
                    bot.send_media_group(c.message.chat.id, images)
        bot.delete_state(c.message.from_user.id, c.message.chat.id)


@bot.message_handler(state=[CustomStates.count_of_notes, CustomStates.min_price,
                            CustomStates.max_price], is_digit=False)
def not_digit_input(message):
    bot.send_message(message.chat.id, 'Похоже, Вы ввели не число. Повторите, пожалуйста, ввод!')
