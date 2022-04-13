import datetime
import time

from telebot import types

from loader import bot
from rapidapi import take_destination_id, take_json_file, check
from users import users

main_keyboard = types.ReplyKeyboardMarkup()
main_keyboard.add(types.KeyboardButton(text="/lowprice"))
main_keyboard.add(types.KeyboardButton(text="/highprice"))
main_keyboard.add(types.KeyboardButton(text="/bestdeal"))


def take_number_of_posts(city):
    dest_id = take_destination_id(city.text)
    if dest_id != -1:
        users[city.chat.id].city = city.text
        users[city.chat.id].destination_id = dest_id
        number = bot.send_message(city.chat.id,
                                  'How many posts do you wanna see? ')
        bot.register_next_step_handler(number, take_checkIn)
    else:
        bot.send_message(city.chat.id,
                         'I can not find this city!')


def take_min_price(city):
    dest_id = take_destination_id(city.text)
    if dest_id != -1:
        users[city.chat.id].city = city.text
        users[city.chat.id].destination_id = dest_id
        min_price = bot.send_message(city.chat.id, 'Min price: ')
        bot.register_next_step_handler(min_price, take_max_price)
    else:
        bot.send_message(city.chat.id,
                         'I can not find this city!')


def take_max_price(min_price):
    if check(min_price.text):
        users[min_price.chat.id].min_price = min_price.text
        max_price = bot.send_message(min_price.chat.id, 'Max price: ')
        bot.register_next_step_handler(max_price, take_distance)
    else:
        bot.send_message(min_price.chat.id, 'Incorrect answer')


def take_distance(max_price):
    if check(max_price.text) and float(users[max_price.chat.id].min_price) <= float(max_price.text):
        users[max_price.chat.id].max_price = max_price.text
        distance = bot.send_message(max_price.chat.id,
                                    'Max distance from landmark: ')
        bot.register_next_step_handler(distance, take_num_of_posts)
    else:
        bot.send_message(max_price.chat.id, 'Incorrect answer')


def take_num_of_posts(distance):
    if check(distance):
        users[distance.chat.id].distance = float(distance.text)
        number = bot.send_message(distance.chat.id,
                                  'How many posts do you wanna see? ')
        bot.register_next_step_handler(number, take_checkIn)
    else:
        bot.send_message(distance.chat.id, 'Incorrect answer')


def take_checkIn(number_of_posts):
    if check(number_of_posts.text) and number_of_posts.text.isdigit():
        users[number_of_posts.chat.id].num_of_posts = number_of_posts.text
        checkIn = bot.send_message(number_of_posts.chat.id, "Date of check in(format yyyy-mm-dd:")
        bot.register_next_step_handler(checkIn, take_checkOut)
    else:
        bot.send_message(number_of_posts.chat.id, 'Incorrect answer')


def take_checkOut(check_in):
    try:
        valid_date = time.strptime(check_in.text, '%Y-%m-%d')
    except ValueError:
        bot.send_message(check_in.chat.id, 'Invalid date!')
    users[check_in.chat.id].checkIn = check_in.text
    checkOut = bot.send_message(check_in.chat.id, "Date of check out(format yyyy-mm-dd:")
    bot.register_next_step_handler(checkOut, add_photos)


def add_photos(checkOut):
    try:
        valid_date = time.strptime(checkOut.text, '%Y-%m-%d')
        users[checkOut.chat.id].checkOut = checkOut.text
        keyboard = types.ReplyKeyboardMarkup()
        keyboard.add(types.KeyboardButton(text="Yes"))
        keyboard.add(types.KeyboardButton(text="No"))
        photos = bot.send_message(checkOut.chat.id,
                                  'Do you wanna any photos? ', reply_markup=keyboard)
        bot.register_next_step_handler(photos, add_num_of_photos)
    except ValueError:
        bot.send_message(checkOut.chat.id, 'Invalid date!')


def add_num_of_photos(photos):
    users[photos.chat.id].photos = photos.text.lower()
    if photos.text == 'Yes':
        num = bot.send_message(photos.chat.id,
                               'How many photos do you wanna see? ', reply_markup=main_keyboard)
        bot.register_next_step_handler(num, result_w_photos)
    else:
        result(photos.chat.id)


def result_w_photos(number_of_photos):
    if check(number_of_photos.text) and number_of_photos.text.isdigit():
        user = users[number_of_photos.chat.id]
        user.num_of_photos = number_of_photos.text
        file, photos = take_json_file(user)
        for el in file:
            if user.distance is not None and \
                    float(el["landmarks"][0]["distance"][:-6]) >= user.distance:
                break
            bot.send_message(number_of_photos.chat.id,
                             f'Name: {el["name"]} '
                             f'\nStreet address: {el["address"]["streetAddress"]} '
                             f'\nDestination to centre: '
                             f'{el["landmarks"][0]["distance"]} '
                             f'\nPrice per night: {el["ratePlan"]["price"]["current"]}'
                             f'\nAverage price: ${int(el["ratePlan"]["price"]["current"][1:]) * int((datetime.datetime.strptime(user.checkOut, "%Y-%m-%d") - datetime.datetime.strptime(user.checkIn, "%Y-%m-%d")).days)}'
                             f'\nPhotos: {photos[el["name"]]}')
    else:
        bot.send_message(number_of_photos.chat.id, 'Incorrect answer', reply_markup=main_keyboard)


def result(user_id):
    user = users[user_id]
    file, photos = take_json_file(user)
    for el in file:
        if user.distance is not None and \
                float(el["landmarks"][0]["distance"][:-6]) >= user.distance:
            break
        bot.send_message(user_id,
                         f'Name: {el["name"]} '
                         f'\nStreet address: {el["address"]["streetAddress"]} '
                         f'\nDestination to centre: '
                         f'{el["landmarks"][0]["distance"]} '
                         f'\nPrice: {el["ratePlan"]["price"]["current"]}'
                         f'\nAverage price: ${int(el["ratePlan"]["price"]["current"][1:]) * int((datetime.datetime.strptime(user.checkOut, "%Y-%m-%d") - datetime.datetime.strptime(user.checkIn, "%Y-%m-%d")).days)}', reply_markup=main_keyboard)
