from tiles.hotbar import HotBar
from tiles.tiles import Tile, TileType
from player.player import *
from tiles.build import Builder
from player.gravity import Direction
import pygame
from settings import *


def get_tile_on_group(tile_group, pos):
    for sprite in tile_group.sprites():
        if (sprite.rect.x == pos[0]) and (sprite.rect.y == pos[1]):
            return sprite


class Level:
    def __init__(self, level_data, surface):
        self.solid_tiles = None
        self.bg_tiles = None
        self.display_surface = surface
        self.setup_level(level_data)
        self.hotbar = HotBar()
        self.builder = Builder(self, level_data, self.hotbar)
        self.world_shift_x = 0
        self.world_shift_y = 0

    def setup_level(self, layout):
        self.solid_tiles = pygame.sprite.Group()
        self.bg_tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                for tile_type in TileType:
                    if cell == tile_type.value:
                        if tile_type.solid:
                            self.solid_tiles.add(Tile((x, y), tile_type))
                        else:
                            self.bg_tiles.add(Tile((x, y), tile_type))
                    continue
                if cell == -1:
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                    self.bg_tiles.add(Tile((x, y), TileType.BACKGROUND))

    def set_block_at(self, pos, tile_type):
        pos = (pos[0] * tile_size, pos[1] * tile_size)
        self.bg_tiles.remove(get_tile_on_group(self.solid_tiles, pos))
        self.solid_tiles.remove(get_tile_on_group(self.solid_tiles, pos))
        if tile_type.solid:
            sd_tile = Tile(pos, tile_type)
            self.solid_tiles.add(sd_tile)
        else:
            bg_tile = Tile(pos, tile_type)
            self.bg_tiles.add(bg_tile)

    #def scroll_x(self):
    #    player = self.player.sprite
    #    player_x = player.rect.centerx
    #    direction_x = player.direction.x
    #
    #    if player_x < screen_width / 8 and direction_x < 0:
    #        self.world_shift_x = max_speed_x
    #        player.speed = 0
    #    elif player_x > screen_width - (screen_width / 8) and direction_x > 0:
    #        self.world_shift_x = -max_speed_x
    #        player.speed = 0
    #    else:
    #        self.world_shift_x = 0
    #        player.speed = 3

    #def scroll_y(self):
    #    player = self.player.sprite
    #    player_y = player.rect.centery
    #    direction_y = player.direction.y
    #
    #    if player_y < screen_height / 8 and direction_y < 0:
    #        self.world_shift_y = max_speed_y * 2
    #    elif player_y > screen_height - (screen_height / 8) and direction_y > 0:
    #        self.world_shift_y = -max_speed_y * 2
    #
    #    else:
    #        self.world_shift_y = 0

    def h_move_colision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x
        for sprite in self.solid_tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                colision_result = abs(sprite.rect.x - player.rect.x)
                g_direct = player.gravity.get_direction()
                if player.direction.x > 0:
                    if g_direct == Direction.RIGHT:
                        player.on_ground = True
                    elif g_direct != Direction.DOWN and g_direct != Direction.UP:
                        player.on_ground = False

                    if colision_result > tile_size / 4:
                        player.rect.right = sprite.rect.left
                        player.can_move = True
                    else:
                        player.can_move = False
                    player.direction.x = 0
                elif player.direction.x < 0:

                    if g_direct == Direction.LEFT:
                        player.on_ground = True
                    elif g_direct != Direction.DOWN and g_direct != Direction.UP:
                        player.on_ground = False

                    if colision_result > tile_size / 4:
                        player.rect.left = sprite.rect.right
                        player.can_move = True
                    else:
                        player.can_move = False
                    player.direction.x = 0

    def v_move_colision(self):
        player = self.player.sprite
        player.apply_gravity()
        player.rect.y += player.direction.y

        for sprite in self.solid_tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                colision_result = abs(sprite.rect.y - player.rect.y)
                g_direct = player.gravity.get_direction()
                if player.direction.y > 0:
                    if g_direct == Direction.DOWN:
                        player.on_ground = True
                    elif g_direct != Direction.RIGHT and g_direct != Direction.LEFT:
                        player.on_ground = False

                    if colision_result > tile_size / 4:
                        player.rect.bottom = sprite.rect.top
                        player.can_move = True
                    elif g_direct != Direction.RIGHT and g_direct != Direction.LEFT:
                        player.can_move = False
                    player.direction.y = 0
                elif player.direction.y < 0:

                    if g_direct == Direction.UP:
                        player.on_ground = True
                    else:
                        player.on_ground = False

                    if colision_result > tile_size / 4:
                        player.rect.top = sprite.rect.bottom
                        player.can_move = True
                    else:
                        player.can_move = False
                    player.direction.y = 0

    def run(self, events):
        self.bg_tiles.update(self.world_shift_x, self.world_shift_y)
        self.bg_tiles.draw(self.display_surface)

        self.solid_tiles.update(self.world_shift_x, self.world_shift_y)
        self.solid_tiles.draw(self.display_surface)

        # Run clock every second
        self.hotbar.drawn(self.display_surface)

        # self.scroll_x()
        # self.scroll_y()

        self.builder.pre_rend.draw(self.display_surface)

        self.builder.check_clicked_pos(events)
        self.hotbar.check_clicked_pos(events)
        self.player.update()
        self.v_move_colision()
        self.h_move_colision()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[ord('g')]:
                    self.player.sprite.gravity.change_gravity()

        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render('\n Gravity: '+ str(self.player.sprite.gravity.get_direction()) + ' | Player Velocity: ' + str(self.player.sprite.direction), True, (255, 0, 0))
        #print('[PLAYER] Velocity: ' + str(self.player.sprite.direction))
        text.get_rect().center = (screen_width / 2, screen_height / 2)
        self.display_surface.blit(text, text.get_rect())

        self.player.draw(self.display_surface)
