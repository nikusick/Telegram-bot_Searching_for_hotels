import requests

import telebot

bot = telebot.TeleBot('2144775858:AAH2coKvBIOUH2rQxDawqVTM3i3pVwH6fPE')


@bot.message_handler(commands=['highprice'])
def highprice(message):
    city = bot.send_message(message.chat.id, 'City: ')
    bot.register_next_step_handler(city, take_number_of_posts, 'highprice')


@bot.message_handler(commands=['lowprice'])
def lowprice(message):
    city = bot.send_message(message.chat.id, 'City: ')
    bot.register_next_step_handler(city, take_number_of_posts, 'lowprice')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text in ["Привет", '/hello-world']:
        bot.send_message(message.from_user.id,
                         "Привет, чем я могу тебе помочь?")


def take_number_of_posts(city, command):
    number = bot.send_message(city.chat.id,
                              'How many posts do you wanna see? ')
    bot.register_next_step_handler(number,
                                   take_destination_id, city.text, command)


def take_destination_id(number_of_posts, city, command):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city}

    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "4f2d02f44dmshc4aa5ffc1ea662fp11ea85jsnfad2e7e02480"
    }

    response = requests.request("GET", url,
                                headers=headers,
                                params=querystring)

    for el in response.json()['suggestions'][0]['entities']:
        if el['type'] == 'CITY' and city.lower() == el['name'].lower():
            destination_id = el['destinationId']
            photos = bot.send_message(number_of_posts.chat.id,
                                      'Do you wanna photos? ')
            bot.register_next_step_handler(photos, add_photos,
                                           destination_id,
                                           number_of_posts.text,
                                           command)
            break
    else:
        bot.send_message(city.chat.id, 'I cant find this city!')


def add_photos(photos, destination_id, number_of_posts, command):
    if photos.text.lower() == 'yes':
        num = bot.send_message(photos.chat.id, 'How many? ')
        bot.register_next_step_handler(num, result_w_photos,
                                       destination_id,
                                       number_of_posts,
                                       command)

    else:
        result(photos, destination_id, number_of_posts, command)


def result_w_photos(num, destination_id, number_of_posts, command):
    if command == 'highprice':
        sortOrder = 'PRICE_HIGHEST_FIRST'
    else:
        sortOrder = 'PRICE'
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": destination_id,
                   "pageNumber": "1",
                   "pageSize": number_of_posts,
                   "checkIn": "2020-01-08",
                   "checkOut": "2020-01-15",
                   "adults1": "1",
                   "sortOrder": sortOrder, "locale": "en_US",
                   "currency": "USD"}

    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "4f2d02f44dmshc4aa5ffc1ea662fp11ea85jsnfad2e7e02480"
    }
    response = requests.request("GET", url,
                                headers=headers,
                                params=querystring)

    for el in response.json()['data']['body']['searchResults']['results']:
        url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

        querystring = {"id": el['id']}

        headers = {
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
            "X-RapidAPI-Key":
                "4f2d02f44dmshc4aa5ffc1ea662fp11ea85jsnfad2e7e02480"
        }

        photo_response = requests.request("GET", url,
                                          headers=headers, params=querystring)
        photos = str()
        for index in range(int(num.text)):
            photos += \
                str(photo_response.json()['hotelImages']
                    [index]['baseUrl'][:-11]) + '.jpg' + ' '

        bot.send_message(num.chat.id,
                         f'Name: {el["name"]} '
                         f'\nStreet address: {el["address"]["streetAddress"]} '
                         f'\nDestination to centre: '
                         f'{el["landmarks"][0]["distance"]} '
                         f'\nPrice: {el["ratePlan"]["price"]["current"]}'
                         f'\nPhotos: {photos}')


def result(photos, destination_id, number_of_posts, command):
    if command == 'highprice':
        sortOrder = 'PRICE_HIGHEST_FIRST'
    else:
        sortOrder = 'PRICE'

    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": destination_id,
                   "pageNumber": "1",
                   "pageSize": number_of_posts,
                   "checkIn": "2020-01-08",
                   "checkOut": "2020-01-15",
                   "adults1": "1",
                   "sortOrder": sortOrder,
                   "locale": "en_US",
                   "currency": "USD"}

    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "4f2d02f44dmshc4aa5ffc1ea662fp11ea85jsnfad2e7e02480"
    }
    response = requests.request("GET", url,
                                headers=headers,
                                params=querystring)

    for el in response.json()['data']['body']['searchResults']['results']:
        bot.send_message(photos.chat.id,
                         f'Name: {el["name"]} '
                         f'\nStreet address: {el["address"]["streetAddress"]} '
                         f'\nDestination to centre: '
                         f'{el["landmarks"][0]["distance"]} '
                         f'\nPrice: {el["ratePlan"]["price"]["current"]}')


bot.polling(none_stop=True, interval=0)
