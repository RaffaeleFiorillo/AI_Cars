# This module contains all the classes that are used in the game classes in order to make the game work.
# Everything that needs to appear in the game is an instance of these classes.
# for those entities that need to appear multiple times, can be of different kinds or comes and goes from the screen,
# there is a class that represents a group of these instances, and can be differentiated from the normal classes by
# looking if his name is plural

# ---------------------------------------------------- IMPORTS ---------------------------------------------------------
import pygame
import AI
import Auxiliar as Aux

# ---------------------------------------------------- SOUNDS ----------------------------------------------------------
"""fire_sound = f.load_sound("game/level failed.WAV")
part_sound = f.load_sound("game/part_collection.WAV")
hit_sound = f.load_sound("game/impact.WAV")"""

# ----------------------------------------------- GLOBAL VARIABLES -----------------------------------------------------
obstacles_distance = 290
parts_distance = 5
space_between_obstacles = [o for o in range(300, 1290, obstacles_distance)]


# ----------------------------------------------------- CAR ------------------------------------------------------------
class Car:
    def __init__(self, name):
        self.speed_module= Aux.CAR_SPEED_MODULE
        self.mind = AI.mind(name)
        self.x_y_center = (Aux.INITIAL_X_COORDINATE, Aux.INITIAL_Y_COORDINATE)
        self.width = self.height = Aux.CAR_SIZE
        self.vision_step = 2
        self.images = {True: Aux.get_square_image(), False: Aux.get_rhombus_image()}
        self.x_y_adjusts = {True: Aux.DRAWING_CENTER_SQUARE, False: Aux.DRAWING_CENTER_RHOMBUS}
        self.image_is_square = True
        self.y_x_adjust = self.x_y_adjusts[self.image_is_square]
        self.image = self.images[self.image_is_square]
        self.hit_box = self.image.get_rect()
        self.angle = 0
        self.alive = True

    def get_distance(self, screen: pygame.Surface, vision_type: str):
        angles = {"front": 90, "left": 0, "right": 180, "front-left": 45, "front-right": 135}
        min_distance_for_death = {"front": 20, "left": 7, "right": 7, "front-left": 29, "front-right": 29}
        additional_angle = angles[vision_type]
        distance = 0
        x_coo, y_coo = self.x_y_center
        while True:
            x_coo += self.vision_step * Aux.cos(self.angle+additional_angle)
            y_coo += self.vision_step * Aux.sin(self.angle+additional_angle)
            try:
                color = screen.get_at((x_coo, y_coo))
            except IndexError:
                color = Aux.ROAD_COLOR
                distance = 0
            if color == Aux.ROAD_COLOR:
                if (distance := round(distance)) <= min_distance_for_death[vision_type]:
                    print("car crashed")
                    self.alive = False

                return distance
            distance += Aux.vector_distance(self.x_y_center[0], self.x_y_center[1], x_coo, y_coo)
            pygame.draw.circle(screen, Aux.YELLOW, (x_coo, y_coo), 1, 1)

    def vision(self, screen):
        frontal_distance = self.get_distance(screen, "front")
        left_distance = self.get_distance(screen, "left")
        right_distance = self.get_distance(screen, "right")
        diagonal_left_distance = self.get_distance(screen, "front-left")
        diagonal_right_distance = self.get_distance(screen, "front-right")
        return frontal_distance, left_distance, right_distance, diagonal_left_distance, diagonal_right_distance

    def get_drawing_coordinates(self):
        return self.x_y_center[0]+self.y_x_adjust[0], self.x_y_center[1]+self.y_x_adjust[1]

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.get_drawing_coordinates())

    def rotate_car_image(self):
        self.image_is_square = not self.image_is_square
        self.y_x_adjust = self.x_y_adjusts[self.image_is_square]
        self.image = self.images[self.image_is_square]

    def turn_left(self):
        self.angle = (self.angle-45) % 360
        self.rotate_car_image()

    def turn_right(self):
        self.angle = (self.angle+45) % 360
        self.rotate_car_image()

    def move_ahead(self):
        updated_x_coo = self.x_y_center[0] + self.speed_module * Aux.sin(-self.angle)
        updated_y_coo = self.x_y_center[1] + self.speed_module * Aux.cos(self.angle)
        self.x_y_center = updated_x_coo, updated_y_coo

    def movement(self, screen):
        print(f"vision: {self.vision(screen)} | angle: {self.angle}")

# ---------------------------------------------------- ROAD ------------------------------------------------------------
class Road:
    def __init__(self, road_rectangles, color):
        self.road_components = self.get_rectangles(road_rectangles)
        self.color = color

    @staticmethod
    def get_rectangles(road_rectangles):
        return [pygame.Rect(x, y, w, h) for x, y, w, h in road_rectangles]

    def draw(self, screen):
        for component in self.road_components:
            pygame.draw.rect(screen, self.color, component)


# --------------------------------------------------- WORLD ------------------------------------------------------------
class World:
    def __init__(self, screen, road_color, road_type=0):
        self.screen = screen
        self.screen_width = self.screen.get_size()[0]
        self.screen_height = self.screen.get_size()[1]
        self.road = Road(Aux.ROAD_RECTANGLES[road_type], road_color)
        self.car = Car(0)
        self.run = True
        self.clock = pygame.time.Clock()

    def car_is_alive(self):
        return self.car.alive

    def refresh(self):
        self.screen.fill((0, 0, 0))  # Background
        self.road.draw(self.screen)
        self.car.movement(self.screen)
        self.car.draw(self.screen)
        self.run = self.car_is_alive()

        pygame.display.update()

    def loop(self):
        time_passed = 0
        while self.run:
            time_passed += self.clock.tick(Aux.FRAME_RATE) / (33 * 30)
            # terminate execution
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.car.turn_left()
                    elif event.key == pygame.K_RIGHT:
                        self.car.turn_right()
                    elif event.key == pygame.K_UP:
                        self.car.move_ahead()
            self.refresh()
