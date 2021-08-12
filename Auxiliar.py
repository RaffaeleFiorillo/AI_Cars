import pygame
import random
import math

pygame.init()


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
    x = math.pow(x_end - x_origin, 2)
    y = math.pow(y_end - y_origin, 2)
    return math.sqrt(x + y)


def get_square_image():
    return pygame.image.load("car_image - normal.png").convert_alpha()


def get_rhombus_image():
    return pygame.image.load("car_image - rotated.png").convert_alpha()


rectangles_1 = [(75, 30, 900, 10), (75, 670, 900, 10), (75, 40, 10, 630), (965, 40, 10, 630),
                (200, 140, 640, 10), (210, 560, 630, 10), (200, 140, 10, 430), (840, 140, 10, 430)
                ]
rectangles_2 = []
rectangles_3 = []
rectangles_4 = []

ROADS = [road_1, road_2, road_3, road_4]  # list of roads
ROAD_RECTANGLES = [rectangles_1, rectangles_2, rectangles_3, rectangles_4]  # rectangles-like collision boxes

YELLOW = (255, 255, 0)
ROAD_COLOR = (0, 0, 255)
CAR_COLOR = (0, 255, 255)
WINDOW_LENGTH = 1080
WINDOW_HEIGHT = 720
FRAME_RATE = 10

INITIAL_X_COORDINATE = 140
INITIAL_Y_COORDINATE = 170
CAR_SIZE = 20
CAR_SPEED_MODULE = 10
DRAWING_CENTER_SQUARE = (-CAR_SIZE // 2, -CAR_SIZE // 2)
adjust = round(-CAR_SIZE * (1 - 1 / math.sqrt(CAR_SIZE)))
DRAWING_CENTER_RHOMBUS = (adjust, adjust)
del adjust

# CAR_IMAGES = {True: SQUARE, False: RHOMBUS}
