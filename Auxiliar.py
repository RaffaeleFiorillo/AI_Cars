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
FRAME_RATE = 100

INITIAL_X_COORDINATE = 140
INITIAL_Y_COORDINATE = 170
CAR_COLOR = (0, 255, 255)
CAR_SIZE = 20
CAR_SPEED_MODULE = 15
DRAWING_CENTER_SQUARE = (-CAR_SIZE//2, -CAR_SIZE//2)
adjust = round(-CAR_SIZE * (1 - 1 / math.sqrt(CAR_SIZE)))
DRAWING_CENTER_RHOMBUS = (adjust, adjust)
del adjust

MUTATION_POSSIBILITY = 0.6
FILE_NAME = "best_minds.txt"

WEIGHTS = [
    [(0.8682282315001495, 0.5214865014166954), (0.40835527353772894, 0.9482474000315406), (0.8617493195441277, 0.47192730890897794, -0.7495283561542576, 0.7943682149269868, 0.006728252147426117), (-0.3989611432122605, 0.059033280995067175), (-0.002075778937549899, 0.276583168207298)],
    [-0.8400917902671333, (-0.9664399074670939, 0.6677622604457064), -0.9664399074670939, 0.47382596869218063, (0.47382596869218063, 0.25266911664255187), 0.15619669166428507],
    [0.8207635079233428, (0.9407684095118458, -0.9120968073178516), (0.9939584006932731, -0.7675458170634546), 0.7002156848661526],
    [0.7621993301950512, 0.671649845214933, 0.13647643042239088]]

BIAS =[[(0.5175198551834236, 0.5246746828314977), (0.13010850108113092, 0.3213715547871653), (0.8934086842589766, 0.24742009240828416, 0.1253293965123826, 0.3890897408165538, 0.18235998669463288), (0.5062055984863532, 0.17235748674915563), (0.45573918295730453, 0.32567771817858526)],
       [-0.7009981390630262, (0.2565845225987002, -0.5031218674759798), 0.2565845225987002, -0.238071520822012, (-0.238071520822012, 0.8751316044024925), 0.3018275058186668],
       [0.27407046684365877, (0.9509214903210592, -0.1904382908428719), (-0.4548372052961492, -0.08388869680600279), 0.7291774896852719],
       [0.19914982050510488, 0.9109410849749023, -0.2631689007505914]]

# CAR_IMAGES = {True: SQUARE, False: RHOMBUS}
