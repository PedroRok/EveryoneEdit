import pygame
from enum import Enum


class TileType(bytes, Enum):
    def __new__(cls, value, label, file):
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.label = label
        obj.file = file
        return obj

    BACKGROUND = (0, ' ', 'bg')
    PANEL = (1, 'X', 'panel')


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, tile_type):
        super().__init__()
        self.image = pygame.image.load(f'resources/{tile_type.file}.png')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift
