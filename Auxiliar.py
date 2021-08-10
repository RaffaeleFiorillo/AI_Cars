import pygame
import random
import math


def road_1(screen, color):
    road_components = [(75, 30, 900, 10), (75, 670, 900, 10), (75, 40, 10, 630), (965, 40, 10, 630),
                       (200, 140, 640, 10), (210, 560, 630, 10), (200, 140, 10, 430), (840, 140, 10, 430)
                       ]
    for component in road_components:
        pygame.draw.rect(screen, color, component)


def road_2(screen):
    pass


def road_3(screen):
    pass


def road_4(screen):
    pass


def sin(angle):
    return round(math.sin(math.radians(angle)))


def cos(angle):
    return round(math.cos(math.radians(angle)))


def vector_distance(x_origin, y_origin, x_end, y_end):
    x = math.pow(x_end-x_origin, 2)
    y = math.pow(y_end-y_origin, 2)
    return math.sqrt(x + y)


ROADS = [road_1, road_2, road_3, road_4]  # list of roads
YELLOW = (255, 255, 0)
ROAD_COLOR = (0, 0, 255)
CAR_COLOR = (0, 255, 255)
WINDOW_LENGTH = 1080
WINDOW_HEIGHT = 720
FRAME_RATE = 1
