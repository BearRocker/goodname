import pygame
import os
import find_obj

import requests

pygame.init()

toponym = input()

z = '8'
map = 'map'

map_params = find_obj.return_params(toponym)
longitude, lattitude = map_params['ll'].split(',')


def draw_map():
    global map
    map_params = {
            "ll": ",".join([longitude, lattitude]),
            'z': z,
            "l": map,
        }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


screen = pygame.display.set_mode((600, 450))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if int(z) + 1 <= 17:
                    z = str(int(z) + 1)
            if event.key == pygame.K_PAGEDOWN:
                if int(z) - 1 >= 0:
                    z = str(int(z) - 1)
            if event.key == pygame.K_SPACE:
                if map == 'map':
                    map = 'sat'
                elif map == 'sat':
                    map = 'sat,skl'
                else:
                    map = 'map'
            if int(z) > 9:
                if int(z) == 10:
                    s = 0.1
                s = 0.01
            else:
                s = 0.5
            if event.key == pygame.K_UP:
                if float(lattitude) + s >= 0:
                    lattitude = str(float(lattitude) + s)
            if event.key == pygame.K_DOWN:
                if float(lattitude) - s <= 85:
                    lattitude = str(float(lattitude) - s)
            if event.key == pygame.K_LEFT:
                if float(lattitude) - s >= 0:
                    longitude = str(float(longitude) - s)
            if event.key == pygame.K_RIGHT:
                if float(lattitude) + s <= 180:
                    longitude = str(float(longitude) + s)
    map_file = draw_map()
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
