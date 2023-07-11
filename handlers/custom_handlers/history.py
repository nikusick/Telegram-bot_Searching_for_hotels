from telegram.constants import ParseMode

from loader import bot

from database.common import get_history


@bot.message_handler(commands=['history'])
def history_command(message):
    queries = get_history(message.from_user.id, 10)
    if len(queries) == 0:
        bot.send_message(message.chat.id, "Ваша история поиска чиста!")
    else:
        for query in queries:
            query_text = f'Команда: {query.get("command")}\n' \
             f'Город: {query.get("city")}\n' \
             f'Дата заезда: {query.get("day_in")}\n' \
             f'Дата выезда: {query.get("day_out")}\n'
            if query.get('command') == '/custom':
                query_text += f'Минимальная цена: {query.get("min_price")}\n' \
                              f'Максимальная цена: {query.get("max_price")}\n'
            query_text += 'Результаты: \n'
            for result in query.get('results'):
                query_text += f'-----------------------------------\n' \
                              f'<b>{result.get("hotel_name")}</b>\n' \
                  f'Адрес: {result.get("address")}\n' \
                  f'Рейтинг: {result.get("rate")}\n' \
                  f'Цена за ночь: {result.get("price")}\n'
            bot.send_message(message.chat.id, query_text, parse_mode=ParseMode.HTML)
