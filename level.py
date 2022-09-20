from tiles.hotbar import HotBar
from tiles.tiles import Tile, TileType
from player import *
from tiles.build import Builder


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
                colision_result = abs(sprite.rect.x - player.rect.x)
                if player.direction.x > 0:
                    player.direction.x = 0
                    if colision_result > tile_size / 4:
                        player.rect.right = sprite.rect.left
                    else:
                        player.can_move = False
                elif player.direction.x < 0:
                    player.direction.x = 0
                    if colision_result > tile_size / 4:
                        player.rect.left = sprite.rect.right
                    else:
                        player.can_move = False
            else:
                player.can_move = True

    def v_move_colision(self):
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.solid_tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                colision_result = abs(sprite.rect.y - player.rect.y)
                if player.direction.y > 0:
                    player.on_ground = True
                    if colision_result > tile_size / 4:
                        player.rect.bottom = sprite.rect.top
                    else:
                        player.can_move = False
                    player.direction.y = 0
                elif player.direction.y < 0:
                    if colision_result > tile_size / 4:
                        player.rect.top = sprite.rect.bottom
                    else:
                        player.can_move = False
                    player.on_ground = False
                    player.direction.y = 0
            else:
                player.can_move = True

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
        self.h_move_colision()
        self.v_move_colision()
        self.player.update()
        self.player.draw(self.display_surface)
