from enum import Enum, auto

import pygame

from settings import *


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Gravity:
    def __init__(self, player):
        self.player = player
        self.gravity = 0.5
        self.direction = Direction.DOWN
        self.gravity_speed = 0

    def get_direction(self):
        return self.direction

    def apply_gravity(self):
        g_direct = self.direction
        # TODO: O PROBLEMA É AQUI

        if g_direct == Direction.DOWN:
            if self.player.direction.y < max_speed_x:
                self.player.direction.y += self.gravity
            else:
                self.player.direction.y = max_speed_x - self.gravity
        elif g_direct == Direction.UP:
            if self.player.direction.y > -max_speed_x:
                self.player.direction.y -= self.gravity
            else:
                self.player.direction.y = -max_speed_x + self.gravity
        elif g_direct == Direction.RIGHT:
            if self.player.direction.x < max_speed_x:
                self.player.direction.x += self.gravity
            else:
                self.player.direction.x = max_speed_x - self.gravity
        elif g_direct == Direction.LEFT:
            if self.player.direction.x > -max_speed_x:
                self.player.direction.x -= self.gravity
            else:
                self.player.direction.x = -max_speed_x + self.gravity
        # i think this is the problem
        self.player.rect.y += self.player.direction.y

    def get_jump_key(self, keys):
        g_direct = self.direction
        jumpKey = False
        jumpArrow = False
        if g_direct == Direction.DOWN:
            jumpKey = keys[ord('w')]
            jumpArrow = keys[pygame.K_UP]
        elif g_direct == Direction.UP:
            jumpKey = keys[ord('s')]
            jumpArrow = keys[pygame.K_DOWN]
        elif g_direct == Direction.LEFT:
            jumpKey = keys[ord('D')]
            jumpArrow = keys[pygame.K_RIGHT]
        elif g_direct == Direction.RIGHT:
            jumpKey = keys[ord('A')]
            jumpArrow = keys[pygame.K_LEFT]
        return jumpKey or jumpArrow

    def change_gravity(self):
        g_direct = self.direction
        if g_direct == Direction.DOWN:
            self.direction = Direction.LEFT
        elif g_direct == Direction.LEFT:
            self.direction = Direction.UP
        elif g_direct == Direction.UP:
            self.direction = Direction.RIGHT
        elif g_direct == Direction.RIGHT:
            self.direction = Direction.DOWN
