import pygame
from enum import Enum


class TileType(bytes, Enum):
    def __new__(cls, value, label, file, solid):
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.label = label
        obj.file = file
        obj.solid = solid
        return obj

    BACKGROUND = (0, 'Default_BG', pygame.image.load('resources/bg.png'), False)
    PANEL = (1, 'Default_Plane', pygame.image.load('resources/panel.png'), True)
    GEM = (2, 'Default_Gem', pygame.image.load('resources/gem1.png'), True)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, tile_type):
        super().__init__()
        self.image = tile_type.file
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift
