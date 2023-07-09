from states.custom_states import CustomStates
from loader import bot
from utils.get_query_result import get_result


@bot.message_handler(state=CustomStates.min_price)
def get_low_price_ask_high_price(message):
    bot.set_state(message.from_user.id, CustomStates.max_price, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['min_price'] = int(message.text)
    bot.send_message(message.chat.id, 'Максимальная цена')


@bot.message_handler(state=CustomStates.max_price)
def get_high_price(message):
    bot.set_state(message.from_user.id, CustomStates.count_of_notes, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['max_price'] = int(message.text)
        result = get_result(data)
        if result is None:
            bot.send_message(message.chat.id, 'По Вашему запросу ничего не найдено(')
        else:
            for images in result:
                bot.send_media_group(message.chat.id, images)
    bot.delete_state(message.from_user.id, message.chat.id)


