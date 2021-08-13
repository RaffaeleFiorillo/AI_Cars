import pygame
import random as r
import math

pygame.init()


def sin(angle):
    return round(math.sin(math.radians(angle)))


def cos(angle):
    return round(math.cos(math.radians(angle)))


def normalize(number):
    return number/150000


def normal_minus1_1(number, min_value=-1, max_value=1):
    return 2*(number-min_value)/(max_value-min_value) -1


def module(number):
    return number*-1 if number < 0 else number


def vectorized(n1, n2):
    return math.sqrt(math.pow(n1, 2)+math.pow(n2, 2))


def random():
    return r.random()


def random_choice(given_list):
    return r.choice(given_list)


# sorts minds based on fitness level in ascending order
def sort_minds(minds):
    minds.sort(key=lambda mind: mind.fitness)
    return minds


def vector_distance(x_origin, y_origin, x_end, y_end):
    x = math.pow(x_end - x_origin, 2)
    y = math.pow(y_end - y_origin, 2)
    return math.sqrt(x + y)


def get_square_image():
    return pygame.image.load("car_image - normal.png").convert_alpha()


def get_rhombus_image():
    return pygame.image.load("car_image - rotated.png").convert_alpha()


rectangles_1 = [(75, 30, 900, 10), (75, 670, 900, 10), (75, 40, 10, 630), (965, 40, 10, 630),
                ]

rectangles_2 = [(75, 30, 900, 10), (75, 670, 900, 10), (75, 40, 10, 630), (965, 40, 10, 630),
                (200, 140, 640, 10), (210, 560, 630, 10), (200, 140, 10, 430), (840, 140, 10, 430)
                ]
rectangles_3 = []
rectangles_4 = []

ROAD_RECTANGLES = [rectangles_1, rectangles_2, rectangles_3, rectangles_4]  # rectangles-like collision boxes

YELLOW = (255, 255, 0)
ROAD_COLOR = (0, 0, 255)
MAX_CAR_NUMBER = 20
WINDOW_LENGTH = 1080
WINDOW_HEIGHT = 720
FRAME_RATE = 10

INITIAL_X_COORDINATE = 140
INITIAL_Y_COORDINATE = 170
CAR_COLOR = (0, 255, 255)
CAR_SIZE = 20
CAR_SPEED_MODULE = 15
DRAWING_CENTER_SQUARE = (-CAR_SIZE//2, -CAR_SIZE//2)
adjust = round(-CAR_SIZE * (1 - 1 / math.sqrt(CAR_SIZE)))
DRAWING_CENTER_RHOMBUS = (adjust, adjust)
del adjust

MUTATION_POSSIBILITY = 0.4
FILE_NAME = "best_minds.txt"

# CAR_IMAGES = {True: SQUARE, False: RHOMBUS}
