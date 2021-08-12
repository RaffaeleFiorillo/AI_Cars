import Entities as Ent
import Auxiliar as Aux
import AI
import pygame

"""LENGTH = Aux.WINDOW_LENGTH
HEIGHT = Aux.WINDOW_HEIGHT
LABEL = "AI CARS"

ROAD = 0  # integer from 0 to 4 representing the type of road. each road has a different shape
ROAD_COLOR = Aux.ROAD_COLOR

screen = pygame.display.set_mode((LENGTH, HEIGHT))
pygame.display.set_caption(LABEL)

WORLD = Ent.World(screen, ROAD_COLOR, ROAD)
WORLD.loop()"""


first_mind = AI.mind(0)
first_mind.create_mind()
