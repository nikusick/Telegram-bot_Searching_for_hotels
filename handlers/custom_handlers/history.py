from loader import bot

from database.common import get_history


@bot.message_handler(commands=['history'])
def get_history(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_id'] = message.from_user.id
    queries = get_history(message.from_user.id)
    if len(queries) == 0:
        bot.send_message(message.chat.id, "Ваша история поиска чиста!")
    else:
        for query in queries:
            bot.send_message(message.chat.id, query)
