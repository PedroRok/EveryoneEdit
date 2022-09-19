import pygame

import player
from tiles import Tile, TileType
from settings import *
from player import *
from build import Builder


class Level:
    def __init__(self, level_data, surface):
        self.solid_tiles = None
        self.bg_tiles = None
        self.display_surface = surface
        self.setup_level(level_data, True)
        self.builder = Builder(self, level_data)
        self.world_shift_x = 0
        self.world_shift_y = 0

    def setup_level(self, layout, player_update=True):
        self.solid_tiles = pygame.sprite.Group()
        self.bg_tiles = pygame.sprite.Group()
        if player_update: self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == 'X':
                    tile = Tile((x, y), tile_size, TileType.PANEL)
                    self.solid_tiles.add(tile)
                if cell == ' ':
                    tile = Tile((x, y), tile_size, TileType.BACKGROUND)
                    self.bg_tiles.add(tile)
                if cell == 'P' and player_update:
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

    def set_block_at(self, pos, tile_type):
        sd_tile = Tile((pos[0] * tile_size, pos[1] * tile_size), tile_size, TileType.PANEL)
        bg_tile = Tile((pos[0] * tile_size, pos[1] * tile_size), tile_size, TileType.BACKGROUND)
        if tile_type == TileType.PANEL:
            self.solid_tiles.add(sd_tile)
        if tile_type == TileType.BACKGROUND:
            for sprite in self.solid_tiles.sprites():
                if (sprite.rect.x == sd_tile.rect.x) and (sprite.rect.y == sd_tile.rect.y):
                    self.solid_tiles.remove(sprite)
            self.bg_tiles.add(bg_tile)


    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 8 and direction_x < 0:
            self.world_shift_x = max_speed_x
            player.speed = 0
        elif player_x > screen_width - (screen_width / 8) and direction_x > 0:
            self.world_shift_x = -max_speed_x
            player.speed = 0
        else:
            self.world_shift_x = 0
            player.speed = 3

    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y

        if player_y < screen_height / 8 and direction_y < 0:
            self.world_shift_y = max_speed_y * 2
        elif player_y > screen_height - (screen_height / 8) and direction_y > 0:
            self.world_shift_y = -max_speed_y * 2

        else:
            self.world_shift_y = 0

    def h_move_colision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.solid_tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x > 0:
                    player.direction.x = 0
                    player.rect.right = sprite.rect.left
                elif player.direction.x < 0:
                    player.direction.x = 0
                    player.rect.left = sprite.rect.right

    def v_move_colision(self):
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.solid_tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.on_ground = True
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.on_ground = False
                    player.direction.y = 0

    def run(self, events):
        self.bg_tiles.update(self.world_shift_x, self.world_shift_y)
        self.bg_tiles.draw(self.display_surface)
        self.solid_tiles.update(self.world_shift_x, self.world_shift_y)
        self.solid_tiles.draw(self.display_surface)
        # self.scroll_x()
        # self.scroll_y()

        self.builder.check_clicked_pos(events)
        self.player.update()
        self.h_move_colision()
        self.v_move_colision()
        self.player.draw(self.display_surface)
