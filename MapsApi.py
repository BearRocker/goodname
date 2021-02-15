import pygame
import os

import requests

pygame.init()

longitude = '37.61779'
lattitude = '55.755241'
z = '12'


def draw_map():
    map_params = {
            "ll": ",".join([longitude, lattitude]),
            'z': z,
            "l": "map",
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
    map_file = draw_map()
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
