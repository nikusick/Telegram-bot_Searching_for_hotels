import telebot

bot = telebot.TeleBot('2144775858:AAH2coKvBIOUH2rQxDawqVTM3i3pVwH6fPE')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text:
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")

bot.polling(none_stop=True, interval=0)
