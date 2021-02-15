import requests
import sys

def return_params(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print('Error')
        print(geocoder_api_server)
        for key, val in geocoder_params.items():
            print(key, val, sep='=')
        sys.exit()

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ang_1 = toponym['boundedBy']['Envelope']['lowerCorner']
    ang_2 = toponym['boundedBy']['Envelope']['upperCorner']

    ang_1 = [float(i) for i in ang_1.split()]
    ang_2 = [float(i) for i in ang_2.split()]

    a = ang_2[0] - ang_1[0]
    b = ang_2[1] - ang_1[1]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    #Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")



    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([str(a), str(b)]),
        "l": "map",
        'pt': f'{toponym_longitude},{toponym_lattitude},pmwtm1'
    }
    return map_params