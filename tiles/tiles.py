import pygame
from enum import Enum

from settings import tile_size
import textures


def get_tile_by_id(id):
    for tile in TileType:
        if tile.value == id:
            return tile
    return TileType.BACKGROUND


class TileType(bytes, Enum):
    def __new__(cls, value, label, file, solid):
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.label = label
        obj.file = file
        obj.solid = solid
        return obj

    REMOVER = (0, 'Remover', textures.get().get_texture_by_label('remove'), False)
    BACKGROUND = (1, 'Default_BG', textures.get().get_texture_by_label('bg'), False)
    PANEL = (2, 'Default_Plane', textures.get().get_texture_by_label('panel'), True)
    GEM = (3, 'Default_Gem', textures.get().get_texture_by_label('gem1'), True)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, tile_type):
        super().__init__()
        self.image = tile_type.file
        self.rect = self.image.get_rect(topleft=pos)
        self.shadow = Shadow((self.rect.x + 1 + tile_size / 8, self.rect.y + 1 + tile_size / 8))

    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift


class Shadow(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill((0, 0, 0))
        self.image.set_alpha(60)
        self.rect = self.image.get_rect(topleft=pos)
