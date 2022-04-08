from loader import bot
from rapidapi import take_destination_id, take_json_file
from users import users


def take_number_of_posts(city):
    dest_id = take_destination_id(city.text)
    if dest_id != -1:
        users[city.chat.id].city = city.text
        users[city.chat.id].destination_id = dest_id
        number = bot.send_message(city.chat.id,
                                  'How many posts do you wanna see? ')
        bot.register_next_step_handler(number, add_photos)
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
    users[min_price.chat.id].min_price = min_price.text
    max_price = bot.send_message(min_price.chat.id, 'Max price: ')
    bot.register_next_step_handler(max_price, take_distance)


def take_distance(max_price):
    users[max_price.chat.id].min_price = max_price.text
    distance = bot.send_message(max_price.chat.id,
                                'Max distance from landmark: ')
    bot.register_next_step_handler(distance, take_num_of_posts)


def take_num_of_posts(distance):
    users[distance.chat.id].distance = float(distance.text)
    number = bot.send_message(distance.chat.id,
                              'How many posts do you wanna see? ')
    bot.register_next_step_handler(number, add_photos)


def add_photos(number_of_posts):
    users[number_of_posts.chat.id].num_of_posts = number_of_posts.text
    photos = bot.send_message(number_of_posts.chat.id,
                              'Do you wanna any photos? ')
    bot.register_next_step_handler(photos, add_num_of_photos)


def add_num_of_photos(photos):
    users[photos.chat.id].photos = photos.text.lower()
    if photos.text.lower() == 'yes':
        num = bot.send_message(photos.chat.id,
                               'How many photos do you wanna see? ')
        bot.register_next_step_handler(num, result_w_photos)
    else:
        result(photos.chat.id)


def result_w_photos(number_of_photos):
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
                         f'\nPrice: {el["ratePlan"]["price"]["current"]}'
                         f'\nPhotos: {photos[el["name"]]}')


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
                         f'\nPrice: {el["ratePlan"]["price"]["current"]}')
