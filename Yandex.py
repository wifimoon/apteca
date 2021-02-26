import sys
from io import BytesIO
import requests
from PIL import Image
from cords import get_cords
import math


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)

    return distance


address = " ".join(sys.argv[1:])
address_ll = get_cords(address)
search_api_server = "https://search-maps.yandex.ru/v1/"

search_params = {
    "apikey": 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)

if not response:
    print('Ошибка в запросе')

json_response = response.json()
apteca_coodrinates = list(map(str, json_response["features"][0]['geometry']['coordinates']))
apteca = json_response['features'][0]['properties']['CompanyMetaData']
print(apteca['address'])
print(apteca['name'])
print(apteca['Hours']['text'])
print(int(lonlat_distance(list(map(float, get_cords(apteca['address']).split(','))),
                          list(map(float, address_ll.split(','))))), 'метров')

map_params = {
    "l": "map",
    "pt": '~'.join([",".join(apteca_coodrinates), address_ll])
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()