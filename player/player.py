import pygame

import textures
from player.gravity import *
from settings import *
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = textures.get().get_texture_by_label("player")
        self.rect = self.image.get_rect(topleft=pos)

        # Player Movement
        self.can_move = True
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 1.5
        self.gravity = Gravity(self)
        self.jump_speed = 9
        self.can_jump = False
        self.is_moving = False
        self.on_ground = False
        self.cd_to_align = 30

    def get_input(self):

        if pygame.mouse.get_pressed()[2]:
            self.rect.center = pygame.mouse.get_pos()

        if not self.can_move:
            return

        keys = pygame.key.get_pressed()
        speedy = 0
        g_direct = self.gravity.get_direction()

        # Jump
        if (self.gravity.get_jump_key(keys)) and self.can_jump:
            self.is_moving = True
            self.jump()

        # Move
        if g_direct == g_direct.DOWN or g_direct == g_direct.UP or g_direct == g_direct.NONE:
            if keys[pygame.K_RIGHT] or keys[ord('d')]:
                self.is_moving = True
                self.direction.x += 0.2
            elif keys[pygame.K_LEFT] or keys[ord('a')]:
                self.is_moving = True
                self.direction.x -= 0.2
            else:
                if self.direction.x > 0:
                    self.direction.x -= 0.2
                elif self.direction.x < 0:
                    self.direction.x += 0.2

                if abs(self.direction.x) < 0.2:
                    self.direction.x = 0
                    if g_direct != g_direct.NONE:
                        self.is_moving = False

        if g_direct == g_direct.LEFT or g_direct == g_direct.RIGHT or g_direct == g_direct.NONE:
            if keys[pygame.K_DOWN] or keys[ord('s')]:
                self.is_moving = True
                self.direction.y += 0.2
            elif keys[pygame.K_UP] or keys[ord('w')]:
                self.is_moving = True
                self.direction.y -= 0.2
            else:
                if self.direction.y > 0:
                    self.direction.y -= 0.2
                elif self.direction.y < 0:
                    self.direction.y += 0.2

                if abs(self.direction.y) < 0.2:
                    self.direction.y = 0
                    if g_direct != g_direct.NONE:
                        self.is_moving = False
        if g_direct == g_direct.NONE:
            if self.direction.x == 0 and self.direction.y == 0:
                self.is_moving = False

    def limit_speed(self, velocity):
        if velocity > max_speed_x:
            velocity = max_speed_x
        elif velocity < -max_speed_x:
            velocity = -max_speed_x + 1
        elif 0.2 > velocity > -0.2:
            velocity = 0
        return velocity

    def manage_velocity(self):
        g_direct = self.gravity.get_direction()

        # LIMIT VELOCITY
        if g_direct == Direction.RIGHT or g_direct == Direction.LEFT:
            self.direction.y = self.limit_speed(self.direction.y)
        elif g_direct != Direction.NONE:
            self.direction.x = self.limit_speed(self.direction.x)
        else:
            self.direction.x = self.limit_speed(self.direction.x)
            self.direction.y = self.limit_speed(self.direction.y)
        # End of LIMIT VELOCITY

        if self.on_ground:
            g_direct = self.gravity.get_direction()
            if g_direct == Direction.DOWN or g_direct == Direction.UP:
                if self.direction.y < 0 or self.direction.y > 1:
                    self.can_jump = False
                    self.on_ground = False
                else:
                    self.can_jump = True

            if g_direct == Direction.LEFT or g_direct == Direction.RIGHT:
                if self.direction.x < 0 or self.direction.x > 1:
                    self.can_jump = False
                    self.on_ground = False
                else:
                    self.can_jump = True

        else:
            self.can_jump = False

        self.align_new()

    def align(self):
        g_direct = self.gravity.get_direction()
        if g_direct == Direction.DOWN or g_direct == Direction.UP:
            align_value = (self.rect.x + 8) / 16
        else:
            align_value = (self.rect.y + 8) / 16

        align_value = (round(align_value) - align_value)

        if not self.is_moving:
            self.cd_to_align -= 1
        else:
            self.cd_to_align = 30
        if self.cd_to_align <= 0 and abs(align_value) != 0.5:
            if g_direct == Direction.DOWN or g_direct == Direction.UP:
                if align_value > 0.1:
                    self.rect.x -= tile_size / 16
                elif align_value < -0.1:
                    self.rect.x += tile_size / 16
            else:
                if align_value > 0.1:
                    self.rect.y -= tile_size / 16
                elif align_value < -0.1:
                    self.rect.y += tile_size / 16
            self.cd_to_align = 0

    def align_new(self):
        g_direct = self.gravity.get_direction()
        if g_direct == Direction.DOWN or g_direct == Direction.UP:
            self.rect.x += self.limit_align((self.rect.x + 8) / 16)
        elif g_direct != Direction.NONE:
            self.rect.y += self.limit_align((self.rect.y + 8) / 16)
        else:
            self.rect.x += self.limit_align((self.rect.x + 8) / 16)
            self.rect.y += self.limit_align((self.rect.y + 8) / 16)

        if not self.is_moving:
            if self.cd_to_align > 0:
                self.cd_to_align -= 1
            else:
                self.cd_to_align = 0
        else:
            self.cd_to_align = 40

    def limit_align(self, align_value):
        align_value = (round(align_value) - align_value)
        if self.cd_to_align <= 0 and abs(align_value) != 0.5:
            if align_value > 0.1:
                return -(tile_size / 16)
            elif align_value < -0.1:
                return tile_size / 16
        return 0

    def apply_gravity(self):
        if self.gravity.get_direction() != Direction.NONE:
            self.gravity.apply_gravity()

    def jump(self):
        direct = self.gravity.get_direction()
        self.can_jump = False
        if direct == Direction.DOWN:
            self.direction.y += -self.jump_speed
        elif direct == Direction.UP:
            self.direction.y += +self.jump_speed
        elif direct == Direction.LEFT:
            self.direction.x += +self.jump_speed
        elif direct == Direction.RIGHT:
            self.direction.x += -self.jump_speed
        self.apply_gravity()

    def update(self):
        self.get_input()
        self.manage_velocity()
