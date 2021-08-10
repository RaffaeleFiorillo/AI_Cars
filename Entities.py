# This module contains all the classes that are used in the game classes in order to make the game work.
# Everything that needs to appear in the game is an instance of these classes.
# for those entities that need to appear multiple times, can be of different kinds or comes and goes from the screen,
# there is a class that represents a group of these instances, and can be differentiated from the normal classes by
# looking if his name is plural

# ---------------------------------------------------- IMPORTS ---------------------------------------------------------
import pygame
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
    def __init__(self):
        self.x_module_speed = 7
        self.y_module_speed = 7
        self.x_speed = 0
        self.y_speed = 0
        self.x_y_center = (140, 170)
        self.width = 20
        self.height = 20
        self.vision_step = 5
        self.angle = 0
        self.vertices_coo = self.update_vertices()
        self.vision_coo = None
        self.inversion = 1
        self.seen_values = []

    def update_vertices(self):
        up_left = (self.x_y_center[0]-self.width//2, self.x_y_center[1]-self.height//2)
        up_right = (self.x_y_center[0]+self.width//2, self.x_y_center[1]-self.height//2)
        down_left = (self.x_y_center[0]-self.width//2, self.x_y_center[1]+self.height//2)
        down_right = (self.x_y_center[0]+self.width//2, self.x_y_center[1]+self.height//2)
        return [up_left, up_right, down_left, down_right]

    def obstacle_collision(self):
        """for obst in l_obstacles:
            if self.hit_box.overlap(obst.hit_box, (self.x - obst.x + obst.adjust, self.y - obst.y + obst.adjust)):
                # f.play(hit_sound)
                return True"""
        return False

    def get_distance(self, screen: pygame.Surface, vision_type: str):
        angles = {"front": 90, "left": 0, "right": 180, "front-left": 45, "front-right": 135}
        additional_angle = angles[vision_type]
        distance = 0
        x_coo, y_coo = self.x_y_center
        while True:
            x_coo += self.vision_step * Aux.cos(self.angle+additional_angle)
            y_coo += self.vision_step * Aux.sin(self.angle+additional_angle)
            color = screen.get_at((x_coo, y_coo))
            if color == Aux.ROAD_COLOR:
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

    def draw(self, screen):
        # drawing squared car
        pygame.draw.line(screen, Aux.CAR_COLOR, self.vertices_coo[0], self.vertices_coo[1])  # upper line
        pygame.draw.line(screen, Aux.CAR_COLOR, self.vertices_coo[2], self.vertices_coo[3])  # bottom line
        pygame.draw.line(screen, Aux.CAR_COLOR, self.vertices_coo[0], self.vertices_coo[2])  # left line
        pygame.draw.line(screen, Aux.CAR_COLOR, self.vertices_coo[1], self.vertices_coo[3])  # right line

    def movement(self, screen):
        print(self.vision(screen))
        self.angle += 45  #*self.inversion
        # self.inversion = -1*self.inversion


# ---------------------------------------------------- ROAD ------------------------------------------------------------
class Road:
    def __init__(self, draw_func, color):
        self.draw_function = draw_func
        self.color = color

    def draw(self, screen):
        self.draw_function(screen, self.color)


# --------------------------------------------------- WORLD ------------------------------------------------------------
class World:
    def __init__(self, screen, road_color, road_type=0):
        self.screen = screen
        self.road = Road(Aux.ROADS[road_type], road_color)
        self.car = Car()
        self.run = True
        self.clock = pygame.time.Clock()

    def draw(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, Aux.WINDOW_LENGTH, Aux.WINDOW_HEIGHT))  # Background
        self.road.draw(self.screen)
        self.car.draw(self.screen)

    def refresh(self):
        self.draw()
        self.car.movement(self.screen)
        pygame.display.update()

    def loop(self):
        time_passed = 0
        while self.run:
            time_passed += self.clock.tick(Aux.FRAME_RATE) / (33 * 30)
            # terminate execution
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            self.refresh()
