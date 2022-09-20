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
        self.gravity = 0.5
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
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE] or keys[ord('w')]) and self.can_jump:
            self.jump()
            speedy = +0.2

        if keys[pygame.K_RIGHT] or keys[ord('d')]:
            self.direction.x += 0.2 + speedy
        elif keys[pygame.K_LEFT] or keys[ord('a')]:
            self.direction.x -= 0.2 + speedy
        else:
            if self.direction.x > 0:
                self.direction.x -= 0.2 + speedy
            elif self.direction.x < 0:
                self.direction.x += 0.2 + speedy

    def manage_velocity(self):
        if self.direction.x > max_speed_x:
            self.direction.x = max_speed_x
        elif self.direction.x < -max_speed_x:
            self.direction.x = -max_speed_x + 1
        elif 0.2 > self.direction.x > -0.2:
            self.direction.x = 0

        if self.on_ground == True:
            if self.direction.y < 0 or self.direction.y > 1:
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
            self.cd_to_align = 20
        if self.cd_to_align == 0:
            self.align()

    def align(self):
        value = self.rect.x / 16
        rnd = round(value) - value
        if 0.4 > rnd > -0.4:
            #self.rect.x = round(value) * 16
            self.direction.x += (round(value) - value)
            #print(rnd)
            #self.cd_to_align = 0

    def apply_gravity(self):
        if self.direction.y < max_speed_y:
            self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.can_jump = False
        self.direction.y = -self.jump_speed

    def update(self):
        self.get_input()
        self.manage_velocity()
