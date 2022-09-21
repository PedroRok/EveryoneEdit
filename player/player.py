import pygame

from player.gravity import *
from settings import *
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("resources/player.png")
        self.rect = self.image.get_rect(topleft=pos)

        # Player Movement
        self.can_move = True
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 1.5
        self.gravity = Gravity(self)
        self.jump_speed = 8
        self.can_jump = False
        self.on_ground = False
        self.cd_to_align = 60

    def get_input(self):

        if pygame.mouse.get_pressed()[2]:
            self.rect.center = pygame.mouse.get_pos()

        if not self.can_move:
            return

        keys = pygame.key.get_pressed()
        speedy = 0
        g_direct = self.gravity.get_direction()

        # Jump
        if (keys[pygame.K_SPACE] or self.gravity.get_jump_key(keys)) and self.can_jump:
            self.jump()

        # Move
        if g_direct == g_direct.DOWN or g_direct == g_direct.UP:
            if keys[pygame.K_RIGHT] or keys[ord('d')]:
                self.direction.x += 0.2
            elif keys[pygame.K_LEFT] or keys[ord('a')]:
                self.direction.x -= 0.2
            else:
                if self.direction.x > 0:
                    self.direction.x -= 0.2
                elif self.direction.x < 0:
                    self.direction.x += 0.2

                if abs(self.direction.x) < 0.2:
                    self.direction.x = 0

        if g_direct == g_direct.LEFT or g_direct == g_direct.RIGHT:
            if keys[pygame.K_DOWN] or keys[ord('w')]:
                self.direction.y += 0.2
            elif keys[pygame.K_UP] or keys[ord('s')]:
                self.direction.y -= 0.2
            else:
                if self.direction.y > 0:
                    self.direction.y -= 0.2
                elif self.direction.y < 0:
                    self.direction.y += 0.2

                if abs(self.direction.y) < 0.2:
                    self.direction.y = 0

    def manage_velocity(self):
        g_direct = self.gravity.get_direction()
        if g_direct == Direction.RIGHT or g_direct == Direction.LEFT:
            if self.direction.y > max_speed_x:
                self.direction.y = max_speed_x
            elif self.direction.y < -max_speed_x:
                self.direction.y = -max_speed_x + 1
            elif 0.2 > self.direction.y > -0.2:
                self.direction.y = 0
        else:
            if self.direction.x > max_speed_x:
                self.direction.x = max_speed_x
            elif self.direction.x < -max_speed_x:
                self.direction.x = -max_speed_x + 1
            elif 0.2 > self.direction.x > -0.2:
                self.direction.x = 0

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

        # Align cd
        if self.direction.x == 0 and self.cd_to_align > 0:
            self.cd_to_align -= 1
        else:
            self.cd_to_align = 30
        if self.cd_to_align == 0:
            pass
            # self.align()

    # def align(self):
    #    value = self.rect.x / 16
    #    rnd = round(value) - value
    #    if 0.4 > rnd > -0.4:
    #        # self.rect.x = round(value) * 16
    #        self.direction.x += (round(value) - value)
    #        # Todo: Finalizar isso
    #        # self.cd_to_align = 0

    def apply_gravity(self):
        self.gravity.apply_gravity()

    def jump(self):
        direct = self.gravity.get_direction()
        print("[PLAYER] Jump (", direct.name, ")")
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
