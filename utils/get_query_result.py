from telebot import types

from database.common import add_query
from site_API.rapidapi import get_cheapest_hotels, get_luxury_hotels, get_custom_hotels


def get_result(data):
    quantity_search = min(10, data['count_of_notes'])
    if data['command'] == '/low':
        hotels = get_cheapest_hotels(city=data['city'], quantity_search=quantity_search,
                                     day_in=data['day_in'],
                                     day_out=data['day_out'])
    elif data['command'] == '/high':
        hotels = get_luxury_hotels(city=data['city'], quantity_search=quantity_search,
                                   day_in=data['day_in'],
                                   day_out=data['day_out'])
    elif data['command'] == '/custom':
        hotels = get_custom_hotels(city=data['city'], quantity_search=quantity_search,
                                   day_in=data['day_in'],
                                   day_out=data['day_out'],
                                   min_price=data['min_price'], max_price=data['max_price'])
    else:
        return None
    if hotels is None:
        return None
    add_query(data)
    result = []
    for hotel in hotels:
        caption = f'{hotel.get("name")}\n' \
                  f'Адрес: {hotel.get("address", "Не указан")}\n' \
                  f'Рейтинг: {hotel.get("rate", "Не указан")}\n' \
                  f'Цена за ночь: {hotel.get("price")}'
        images = [types.InputMediaPhoto(img_url) for img_url in hotel.get('images')]
        images[0].caption = caption
        result.append(images)
    return result
