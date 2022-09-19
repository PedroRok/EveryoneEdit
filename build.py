import threading

import pygame
from map import level_map
from settings import tile_size
from tiles import TileType


class Builder():
    def __init__(self, level, level_data):
        self.level = level
        self.level_data = level_data
        self.clicked_pos = [(int, int)]

    def check_clicked_pos(self, event):
        for ev in event:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pass
            if ev.type == pygame.MOUSEBUTTONUP:
                self.clicked_pos = [(int, int)]

        x, y = pygame.mouse.get_pos()
        x = int(x / tile_size)
        y = int(y / tile_size)
        if pygame.mouse.get_pressed()[0] and not self.clicked_pos.__contains__((x, y)):
            self.clicked_pos.append((x, y))
            for char_index, char in enumerate(level_map[y]):
                if char_index == x:
                    if char == 'X':
                        self.level.set_block_at((x, y), TileType.BACKGROUND)
                        level_map[y] = level_map[y][:char_index] + ' ' + level_map[y][char_index + 1:]
                    else:
                        self.level.set_block_at((x, y), TileType.PANEL)
                        level_map[y] = level_map[y][:char_index] + 'X' + level_map[y][char_index + 1:]