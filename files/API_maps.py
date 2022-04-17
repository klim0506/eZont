# В этом файле собраны функции и классы для работы с Яндекс Картами
import sqlite3
import requests
import numpy


# Определение ближайшего аппарата
def near_app(path_to_db, latitude, longitude):
    # Получаем список координат всех аппаратов из БД
    connect = sqlite3.connect(path_to_db)
    cursor = connect.cursor()

    coordinates = list(map(lambda x: tuple(float(i) for i in x[0].split(', ')),
                           cursor.execute("SELECT coordinate FROM points").fetchall()))

    # Находим ближайшую координату к местоположению пользователя
    coordinates = numpy.array(coordinates)
    user_location = numpy.array((longitude, latitude))
    nearst_dev_coord = coordinates[numpy.argmin(numpy.linalg.norm(coordinates-user_location, axis=1))]

    # Возращаем данные об аппарате из БД
    info = cursor.execute(f"SELECT place, free_cell, fill_cell FROM points WHERE coordinate='{nearst_dev_coord[0]}, {nearst_dev_coord[1]}'").fetchall()[0]

    data = {'place': info[0],
            'latitude': nearst_dev_coord[0],
            'longitude': nearst_dev_coord[1],
            'free_cell': info[1],
            'fill_cell': info[2]}

    return data


# Карта-схема до ближайшего аппарата
def near_app_map(user_coord, device_coord):
    response = requests.get(f"https://static-maps.yandex.ru/1.x/?pt={user_coord[1]},{user_coord[0]},"
                            f"org~{device_coord[1]},{device_coord[0]},round&l=map")

    with open('images/near_app_map.jpg', 'wb') as file:
        file.write(response.content)


# Карта всех аппаратов из БД
def all_app_map(path_to_db):
    url = 'https://static-maps.yandex.ru/1.x/?l=map&pt='

    connect = sqlite3.connect(path_to_db)
    cursor = connect.cursor()
    all_coordinates = list(map(lambda x: tuple(float(i) for i in x[0].split(', ')),
                               cursor.execute("SELECT coordinate FROM points").fetchall()))

    for point in all_coordinates:
        url = url + str(point[1]) + ',' + str(point[0]) + ',round' + '~'

    response = requests.get(url[:-1])

    with open('images/all_app_map.jpg', 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    longitude = 55.662627
    latitude = 37.476347

    my_dev = near_app('../db/data.db', longitude=longitude, latitude=latitude)
    near_app_map((longitude, latitude), (my_dev['latitude'], my_dev['longitude']))
    all_app_map('../db/data.db')
