from states.custom_states import CustomStates

from loader import bot


@bot.message_handler(state='*', commands=['custom'])
def ask_city(message):
    """
    State 1. Will process when user's state is LowStates.city.
    """
    bot.set_state(message.from_user.id, CustomStates.city, message.chat.id)
    bot.send_message(message.chat.id, 'Какой город Вас интересует?')


@bot.message_handler(state=CustomStates.city, is_digit=True)
def get_city(message):
    """
    State 2. Will process when user's state is LowStates.city.
    """
    bot.set_state(message.from_user.id, CustomStates.low_price, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
    bot.send_message(message.chat.id, 'Минимальная цена')


@bot.message_handler(state=CustomStates.city, is_digit=False)
def min_price_incorrect(message):
    bot.send_message(message.chat.id, 'Похоже, Вы ввели не число. Повторите, пожалуйста, ввод!')


@bot.message_handler(state=CustomStates.low_price, is_digit=True)
def get_low_price(message):
    bot.set_state(message.from_user.id, CustomStates.high_price, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['low_price'] = message.text
    bot.send_message(message.chat.id, 'Максимальная цена')


@bot.message_handler(state=CustomStates.low_price, is_digit=False)
def max_price_incorrect(message):
    bot.send_message(message.chat.id, 'Похоже, Вы ввели не число. Повторите, пожалуйста, ввод!')


@bot.message_handler(state=CustomStates.high_price)
def get_low_price(message):
    bot.set_state(message.from_user.id, CustomStates.count_of_notes, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['high_price'] = message.text
    bot.send_message(message.chat.id, 'Сколько номеров показать?')


@bot.message_handler(state=CustomStates.count_of_notes, is_digit=True)
def get_count_of_notes(message):
    """
    State 3. Will process when user's state is LowStates.count_of_notes.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['count_of_notes'] = message.text
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Ready, take a look:\n<b>"
               f"City: {data['city']}\n"
               f"Number of posts: {data['count_of_notes']}\n</b>")
    bot.send_message(message.chat.id, msg, parse_mode="html")
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=CustomStates.count_of_notes, is_digit=False)
def age_incorrect(message):
    """
    Wrong response for LowStates.count_of_notes
    """
    bot.send_message(message.chat.id, 'Похоже, Вы ввели не число. Повторите, пожалуйста, ввод!')
