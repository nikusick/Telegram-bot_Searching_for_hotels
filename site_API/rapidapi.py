import datetime
import json
import re
from typing import Dict

import requests
from telebot.types import Message
from loader import bot


def make_request(method: str, url: str, params: Dict,
                 timeout=10, success=requests.codes.ok):
    url = 'https://hotels4.p.rapidapi.com' + url
    headers = {
        "X-RapidAPI-Key": "4f2d02f44dmshc4aa5ffc1ea662fp11ea85jsnfad2e7e02480",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    try:
        if method == 'get':
            request = requests.request(method=method, url=url, params=params, headers=headers, timeout=timeout)
        else:
            request = requests.request(method=method, url=url, json=params, headers=headers, timeout=timeout)
        if request.status_code == success:
            return request
    except Exception:
        return None
    return None


def get_city_destination(city: str):
    url = '/locations/v3/search'
    params = {"q": city}
    response = make_request('get', url, params)
    if response:
        return (response.json().get('sr')[0].get('gaiaId'),
                response.json().get('sr')[0].get('coordinates').get('lat'),
                response.json().get('sr')[0].get('coordinates').get('long'))
    else:
        return None


def get_detail_info(id):
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": f"{id}"
    }
    url_post = "/properties/v2/detail"
    return make_request(method='post', url=url_post, params=payload, timeout=30)


def get_properties(city: str, day_in: datetime.date, day_out: datetime.date, price=None):
    gaiaId, lat, long = get_city_destination(city=city)
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {
            "coordinates": {
                "latitude": float(lat),
                "longitude": float(long)
            },
            "regionId": gaiaId
        },
        "checkInDate": {
            "day": day_in.day,
            "month": day_in.month,
            "year": day_in.year
        },
        "checkOutDate": {
            "day": day_out.day,
            "month": day_out.month,
            "year": day_out.year
        },
        "rooms": [
            {
                "adults": 2,
                "children": []
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": 'PRICE_LOW_TO_HIGH',
        "filters": {
        }
    }
    if price is not None:
        payload['filters'] = price
    url_post = "/properties/v2/list"

    response = make_request(method='post', url=url_post, params=payload, timeout=30)
    if response is not None:
        try:
            response = response.json()
            properties = response.get('data').get('propertySearch').get('properties')
            return properties
        except Exception:
            return None
    return None


def get_cheapest_hotels(city, quantity_search, day_in, day_out):
    try:
        properties = get_properties(city=city, day_in=day_in, day_out=day_out)
        result = []
        for index in range(len(properties[:quantity_search])):
            price = (properties[index].get("price").get("options")[0].get("formattedDisplayPrice"))
            details = get_detail_info(properties[index].get('id'))
            if details:
                result.append(price)
        return result
    except Exception:
        return None


def get_luxury_hotels(city, quantity_search, day_in, day_out):
    try:
        properties = get_properties(city=city, day_in=day_in, day_out=day_out)
        result = []
        for index in range(len(properties) - 1, len(properties) - 1 - quantity_search, -1):
            price = (properties[index].get("price").get("options")[0].get("formattedDisplayPrice"))
            details = get_detail_info(properties[index].get('id'))
            if details:
                result.append(price)
        return result
    except Exception:
        return None


print(get_cheapest_hotels('Paris', 5, datetime.date(2023, 1, 1), datetime.date(2023, 3, 3)))
print(get_luxury_hotels('Paris', 5, datetime.date(2023, 1, 1), datetime.date(2023, 3, 3)))
