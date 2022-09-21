import pygame
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
        self.gravity = (0, 0.5)
        self.jump_speed = 8
        self.can_jump = False
        self.on_ground = False
        self.cd_to_align = 60

    def get_input(self):

        if not self.can_move:
            return

        keys = pygame.key.get_pressed()

        speedy = 0

        # Jump
        if self.gravity[1] != 0:
            if self.gravity[1] > 0:
                jumpKey = keys[ord('w')]
                jumpArrow = keys[pygame.K_UP]
            else:
                jumpKey = keys[ord('s')]
                jumpArrow = keys[pygame.K_DOWN]
        else:
            if self.gravity[1] > 0:
                jumpKey = keys[ord('D')]
                jumpArrow = keys[pygame.K_RIGHT]
            else:
                jumpKey = keys[ord('A')]
                jumpArrow = keys[pygame.K_LEFT]

        if (keys[pygame.K_SPACE] or jumpKey or jumpArrow) and self.can_jump:
            self.jump()
            speedy = +0.2

        # Move
        if self.gravity[1] != 0:
            if keys[pygame.K_RIGHT] or keys[ord('d')]:
                self.direction.x += 0.2 + speedy
            elif keys[pygame.K_LEFT] or keys[ord('a')]:
                self.direction.x -= 0.2 + speedy
            else:
                if self.direction.x > 0:
                    self.direction.x -= 0.2 + speedy
                elif self.direction.x < 0:
                    self.direction.x += 0.2 + speedy

        if self.gravity[0] != 0:
            if keys[pygame.K_DOWN] or keys[ord('w')]:
                self.direction.y += 0.2 + speedy
            elif keys[pygame.K_UP] or keys[ord('s')]:
                self.direction.y -= 0.2 + speedy
            else:
                if self.direction.y > 0:
                    self.direction.y -= 0.2 + speedy
                elif self.direction.y < 0:
                    self.direction.y += 0.2 + speedy

    def manage_velocity(self):
        if self.direction.x > max_speed_x:
            self.direction.x = max_speed_x
        elif self.direction.x < -max_speed_x:
            self.direction.x = -max_speed_x + 1
        elif 0.2 > self.direction.x > -0.2:
            self.direction.x = 0

        if self.on_ground:
            if (self.direction.y < 0 or self.direction.y > 1) and self.gravity[1] != 0:
                self.can_jump = False
                self.on_ground = False
            elif self.gravity[1] != 0:
                self.can_jump = True

            print(self.direction.x)
            if (self.direction.x < 0 or self.direction.x > 1) and (self.gravity[0] != 0):
                self.can_jump = False
                self.on_ground = False
            elif self.gravity[0] != 0:
                self.can_jump = True

        else:
            self.can_jump = False

        # Align cd
        if self.direction.x == 0 and self.cd_to_align > 0:
            self.cd_to_align -= 1
        else:
            self.cd_to_align = 20
        if self.cd_to_align == 0:
            self.align()

    def align(self):
        value = self.rect.x / 16
        rnd = round(value) - value
        if 0.4 > rnd > -0.4:
            # self.rect.x = round(value) * 16
            self.direction.x += (round(value) - value)
            # Todo: Finalizar isso
            # self.cd_to_align = 0

    def apply_gravity(self):
        if self.direction.y < max_speed_y and self.gravity[1] != 0:
            self.direction.y += self.gravity[1]

        if self.direction.x < max_speed_y and self.gravity[0] != 0:
            self.direction.x += self.gravity[0]
        elif self.gravity[0] != 0:
            self.rect.x += self.direction.x

        self.rect.y += self.direction.y

    def jump(self):
        print("jumping")
        self.can_jump = False
        if self.gravity[1] > 0:
            self.direction.y = -self.jump_speed
        elif self.gravity[1] < 0:
            self.direction.y = +self.jump_speed
        elif self.gravity[0] > 0:
            self.direction.x = -self.jump_speed
        elif self.gravity[0] < 0:
            self.direction.x = +self.jump_speed

    def update(self):
        self.get_input()
        self.manage_velocity()
