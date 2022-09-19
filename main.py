import pygame, sys
from pygame.locals import *
from settings import *
from map import *
from level import Level
from build import Builder

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_map, screen)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    level.run(events)

    pygame.display.update()
    clock.tick(60)