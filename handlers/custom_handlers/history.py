from loader import bot

from database.common import get_history


@bot.message_handler(commands=['history'])
def history_command(message):
    queries = get_history(message.from_user.id, 10)
    if len(queries) == 0:
        bot.send_message(message.chat.id, "Ваша история поиска чиста!")
    else:
        for query in queries:
            bot.send_message(message.chat.id, query)
