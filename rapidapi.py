from requests import get, codes


def take_destination_id(city):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city}

    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "4f2d02f44dmshc4aa5ffc1ea662fp11ea85jsnfad2e7e02480"
    }

    response = request_to_api(url, headers, querystring)

    for el in response.json()['suggestions'][0]['entities']:
        if el['type'] == 'CITY' and city.lower() == el['name'].lower():
            return el['destinationId']
    else:
        return -1


def take_json_file(user):
    if user.command == 'highprice':
        sortOrder = 'PRICE_HIGHEST_FIRST'
    else:
        sortOrder = 'PRICE'

    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": user.destination_id,
                   "pageNumber": "1",
                   "pageSize": user.num_of_posts,
                   "checkIn": user.checkIn,
                   "checkOut": user.checkOut,
                   "adults1": "1",
                   "priceMin": user.min_price,
                   "priceMax": user.max_price,
                   "sortOrder": sortOrder, "locale": "en_US",
                   "currency": "USD"}

    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "4f2d02f44dmshc4aa5ffc1ea662fp11ea85jsnfad2e7e02480"
    }
    response = request_to_api(url, headers, querystring)
    if user.photos == 'no':
        return response.json()['data']['body']['searchResults']['results'], \
               ''
    photos = {}
    for el in response.json()['data']['body']['searchResults']['results']:
        photo = ''
        photo_response = take_photos(el)
        for index in range(int(user.num_of_photos)):
            photo += str(photo_response[index]['baseUrl'][:-11]) \
                     + '.jpg' + '\n '
        photos.update({el['name']: photo})
    return response.json()['data']['body']['searchResults']['results'], photos


def take_photos(el):
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": el['id']}

    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key":
            "4f2d02f44dmshc4aa5ffc1ea662fp11ea85jsnfad2e7e02480"
    }

    photo_response = request_to_api(url, headers, querystring)
    return photo_response.json()['hotelImages']


def request_to_api(url, headers, querystring):
    try:
        response = get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == codes.ok:
            return response
    except:
        return None


def check(text):
    try:
        a = float(text)
        if a < 0:
            return False
        return True
    except:
        return False

