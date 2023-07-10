from typing import Dict, Tuple, List

from requests import Response

from config_data.config import RAPID_API_KEY

import datetime
import requests


def make_request(method: str, url: str, params: Dict,
                 timeout: int = 10, success: int = requests.codes.ok) -> Response | None:
    url = 'https://hotels4.p.rapidapi.com' + url
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
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


def get_city_destination(city: str) -> Tuple[str, str, str] | None:
    url = '/locations/v3/search'
    params = {"q": city}
    response = make_request('get', url, params)
    if response:
        return (response.json().get('sr')[0].get('gaiaId'),
                response.json().get('sr')[0].get('coordinates').get('lat'),
                response.json().get('sr')[0].get('coordinates').get('long'))
    else:
        return None


def get_detail_info(id: int) -> Dict | None:
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": f"{id}"
    }
    url_post = "/properties/v2/detail"
    response = make_request(method='post', url=url_post, params=payload, timeout=30).json()
    try:
        result = {'name': response.get('data').get('propertyInfo').get('summary').get('name'),
                  'address': response.get('data').get('propertyInfo')
                  .get('summary').get('location').get('address').get('addressLine'),
                  'rate': response.get('data').get('propertyInfo').get('reviewInfo')
                  .get('summary').get('overallScoreWithDescriptionA11y').get('value'),
                  'images': [img.get('image').get('url') for img in response.get('data')
                                                                    .get('propertyInfo').get('propertyGallery').get(
                      'images')[:3]]
                  }
        return result
    except Exception:
        return None


def get_properties(city: str, day_in: datetime.date, day_out: datetime.date, price: Dict = None) -> List | None:
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


def get_cheapest_hotels(city: str, quantity_search: int,
                        day_in: datetime.date, day_out: datetime.date) -> List[Dict] | None:
    try:
        properties = get_properties(city=city, day_in=day_in, day_out=day_out)
        result = []
        for property in properties[:quantity_search]:
            price = (property.get("price").get("options")[0].get("formattedDisplayPrice"))
            details = get_detail_info(property.get('id'))
            if details:
                details.update({'price': price})
                result.append(details)
        return result
    except Exception:
        return None


def get_luxury_hotels(city: str, quantity_search: int,
                      day_in: datetime.date, day_out: datetime.date) -> List[Dict] | None:
    try:
        properties = get_properties(city=city, day_in=day_in, day_out=day_out)
        result = []
        for property in properties[:-quantity_search - 1:-1]:
            price = (property.get("price").get("options")[0].get("formattedDisplayPrice"))
            details = get_detail_info(property.get('id'))
            if details:
                details.update({'price': price})
                result.append(details)
        return result
    except Exception:
        return None


def get_custom_hotels(city: str, quantity_search: int,
                      day_in: datetime.date, day_out: datetime.date,
                      min_price: float, max_price: float) -> List[Dict] | None:
    try:
        properties = get_properties(city=city, day_in=day_in, day_out=day_out, price={"price":
                                                                                          {"max": max_price,
                                                                                           "min": min_price}})
        result = []
        for property in properties[:quantity_search]:
            price = (property.get("price").get("options")[0].get("formattedDisplayPrice"))
            details = get_detail_info(property.get('id'))
            if details:
                details.update({'price': price})
                result.append(details)
        return result
    except Exception:
        return None
