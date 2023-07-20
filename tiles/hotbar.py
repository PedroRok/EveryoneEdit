import pygame

import tiles.tiles
import textures
from settings import screen_width, screen_height


class HotBarSlot(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.scale(textures.get().get_texture_by_label('hotbar_slot'), (48, 48))
        self.rect = self.image.get_rect(center=pos)


class Select(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.scale(textures.get().get_texture_by_label('selected_item'), (48, 48))
        self.rect = self.image.get_rect(center=pos)


class Item(pygame.sprite.Sprite):
    def __init__(self, pos, item_type):
        super().__init__()
        self.image = pygame.transform.scale(item_type.file.copy(), (32, 32))
        self.rect = self.image.get_rect(center=pos)


class HotBar:
    def __init__(self):
        super().__init__()

        # Index, TileType
        self.item_in_hand = (0, tiles.tiles.TileType.REMOVER)

        self.hb = pygame.sprite.Group()
        self.hb_size = (216*2, 24*2)
        self.select = pygame.sprite.GroupSingle()

        self.items = pygame.sprite.Group()
        self.items_order = []

        self.screen_width = (screen_width / 2) - (self.hb_size[0] / 2) + (self.hb_size[1] / 2)
        self.screen_height = screen_height - (self.hb_size[1] / 2)
        for i in range(9):
            self.hb.add(HotBarSlot((self.screen_width + i * self.hb_size[1], self.screen_height)))
        self.select.add(Select((self.screen_width, screen_height - 24)))
        self.add_items_to_hotbar()

    def get_item_in_hand(self) -> tiles.tiles.TileType:
        return self.item_in_hand[1]

    def set_select_pos(self, pos):
        self.select.sprite.rect.center = (self.screen_width + pos * self.hb_size[1], self.screen_height)

    def add_items_to_hotbar(self):
        for tile_index, tiletype in enumerate(tiles.tiles.TileType):
            if tile_index > 9:
                break
            self.items.add(
                Item((self.screen_width + tile_index * self.hb_size[1], self.screen_height), tiletype))
            self.items_order.append(tiletype)

    def drawn(self, screen):
        self.hb.draw(screen)
        self.select.draw(screen)
        self.items.draw(screen)

    def check_clicked_pos(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for slot_index, slot in enumerate(self.items):
                        if slot.rect.collidepoint(event.pos):
                            self.set_item_in_hand(slot_index)
                self.check_mouse_scroll(event)

            for i in range(len(self.items_order)):
                if event.type == pygame.KEYDOWN:
                    if event.key == getattr(pygame, f'K_{i + 1}'):
                        self.set_item_in_hand(i)

    def check_mouse_scroll(self, event):
        if event.button == 4:
            if self.item_in_hand[0] == 0:
                self.set_item_in_hand(len(self.items_order) - 1)
            else:
                self.set_item_in_hand(self.item_in_hand[0] - 1)
        if event.button == 5:
            if self.item_in_hand[0] == len(self.items_order) - 1:
                self.set_item_in_hand(0)
            else:
                self.set_item_in_hand(self.item_in_hand[0] + 1)

    def set_item_in_hand(self, index):
        self.item_in_hand = (index, self.items_order[index])
        self.set_select_pos(index)

    def get_item_pos_in_hand(self, id):
        for index, item in enumerate(self.items_order):
            if item.value == id:
                return index
        return 0
