from handlers import take_number_of_posts, take_min_price
from users import users, User
from loader import bot


@bot.message_handler(commands=['highprice'])
def highprice(message):
    if users.get(message.chat.id) is None:
        users[message.chat.id] = User()
    users[message.chat.id].command = 'highprice'
    city = bot.send_message(message.chat.id, 'City: ')
    bot.register_next_step_handler(city, take_number_of_posts)


@bot.message_handler(commands=['lowprice'])
def lowprice(message):
    if users.get(message.chat.id) is None:
        users[message.chat.id] = User()
    users[message.chat.id].command = 'lowprice'
    city = bot.send_message(message.chat.id, 'City: ')
    bot.register_next_step_handler(city, take_number_of_posts)


@bot.message_handler(commands=['bestdeal'])
def bestdeal(message):
    if users.get(message.chat.id) is None:
        users[message.chat.id] = User()
    users[message.chat.id].command = 'bestdeal'
    city = bot.send_message(message.chat.id, 'City: ')
    bot.register_next_step_handler(city, take_min_price)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text in ["Привет", '/hello-world']:
        bot.send_message(message.from_user.id,
                         "Привет, чем я могу тебе помочь?")


bot.polling(none_stop=True, interval=0)
