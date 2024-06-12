from enum import Enum

import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite

from src.config.gamedata import GameData
from src.utils.utils import Direction


class Entity(Sprite):
    def __init__(self, group, pos):
        self.config = GameData()
        super().__init__(group)
        self.pos = Vector2(pos) * self.config.tile_size
        self.height = self.config.tile_size
        self.width = self.config.tile_size
        self.collide_rect = self.get_collide_rect()
        self.direction = Vector2()
        self.speed = 100
        self.name = "entity"

    def collide_with(self, tile_rect, direction):
        if direction == Direction.RIGHT:
            self.pos.x = tile_rect.right + self.collide_rect.width / 2
        elif direction == Direction.LEFT:
            self.pos.x = tile_rect.left - self.collide_rect.width / 2
        elif direction == Direction.DOWN:
            self.pos.y = tile_rect.bottom + self.collide_rect.height / 2
        elif direction == Direction.UP:
            self.pos.y = tile_rect.top - self.collide_rect.height / 2

    def get_collide_rect(self):
        return pygame.rect.Rect(self.pos.x - self.width / 2,self.pos.y - self.height / 2,self.width,self.height)

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        self.pos += self.direction * self.speed * dt * self.config.tile_scale
        self.collide_rect = self.get_collide_rect()

    def update(self, dt):
        self.move(dt)
