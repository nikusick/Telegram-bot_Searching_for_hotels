from loader import bot


@bot.message_handler(commands=['cancel'])
def any_state(message):
    """
    Отменяет последний запрос
    """
    bot.send_message(message.chat.id, "Поиск отменен")
    bot.delete_state(message.from_user.id, message.chat.id)
