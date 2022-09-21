import pygame, sys
from pygame.locals import *
from settings import *
from map import *
from level import Level

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('EveryoneEdits')
pygame.display.set_icon(pygame.image.load('resources/player.png'))
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