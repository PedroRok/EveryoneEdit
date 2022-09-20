import pygame
from map import level_map
from settings import tile_size

select_image = pygame.image.load('resources/selected_item.png')


class PreRendererSprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = select_image
        self.image.set_alpha(80)
        self.rect = self.image.get_rect(topleft=pos)


class Builder:
    pre_rend = pygame.sprite.GroupSingle()

    def __init__(self, level, level_data, hotbar):
        self.level = level
        self.level_data = level_data
        self.hotbar = hotbar
        self.clicked_pos = []

    def check_clicked_pos(self, event):

        # get mouse position on grid
        x, y = pygame.mouse.get_pos()
        x = int(x / tile_size)
        y = int(y / tile_size)

        if y < len(level_map) and x < len(level_map[y]):
            self.pre_render((x * tile_size, y * tile_size))


        for ev in event:
            if ev.type == pygame.MOUSEBUTTONUP:
                self.clicked_pos = []

        # is right mouse button being pressed?
        if not pygame.mouse.get_pressed()[0]:
            return

        if len(level_map) < y + 1:
            return
        # check if clicked position is already in list
        if self.clicked_pos.__contains__((x, y)):
            return

        # add clicked position to list
        self.clicked_pos.append((x, y))

        # set block at clicked position
        for tile_index, char in enumerate(level_map[y]):
            if tile_index == x:
                tile = self.hotbar.get_item_in_hand()
                # verify if is border
                if (y < len(level_map) - 1 and x < len(level_map[y]) - 1) and (y > 0 and x > 0):
                    self.set_block_at((x, y), tile)
                elif tile.solid:
                    self.set_block_at((x, y), tile)

    def set_block_at(self, pos, tile):
        self.level.set_block_at((pos[0], pos[1]), tile)
        level_map[pos[1]][pos[0]] = tile.value

    def pre_render(self, pos):
        self.pre_rend.add(PreRendererSprite((pos[0] - 4, pos[1] - 4)))
