from states.custom_states import HighStates

from loader import bot


@bot.message_handler(state='*', commands=['high'])
def ask_city(message):
    """
    State 1. Will process when user's state is LowStates.city.
    """
    bot.set_state(message.from_user.id, HighStates.city, message.chat.id)
    bot.send_message(message.chat.id, 'Какой город Вас интересует?')


@bot.message_handler(state=HighStates.city)
def get_city(message):
    """
    State 2. Will process when user's state is LowStates.city.
    """
    bot.set_state(message.from_user.id, HighStates.count_of_notes, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
    bot.send_message(message.chat.id, 'Сколько номеров показать?')


@bot.message_handler(state=HighStates.count_of_notes, is_digit=True)
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


@bot.message_handler(state=HighStates.count_of_notes, is_digit=False)
def age_incorrect(message):
    """
    Wrong response for LowStates.count_of_notes
    """
    bot.send_message(message.chat.id, 'Похоже, Вы ввели не число. Повторите, пожалуйста, ввод!')
