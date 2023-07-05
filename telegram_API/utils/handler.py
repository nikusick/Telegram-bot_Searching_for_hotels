from ..core import bot


@bot.message_handler(commands=['low'])
def low_price(message):
    city = bot.send_message(message.chat.id, 'City: ')
    bot.register_next_step_handler(city, take_number_of_posts)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text in ["Привет", '/hello-world']:
        bot.send_message(message.from_user.id,
                         f"Привет, {message.from_user.first_name}, чем я могу тебе помочь?")


def take_number_of_posts(city):
    number = bot.send_message(city.chat.id, 'How many posts do you wanna see? ')
    bot.register_next_step_handler(number, get_low_price, city.text)


def get_low_price(num, city):
    print(num.text, city)
