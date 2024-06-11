import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite

from gamedata import GameData


class Entity(Sprite):
    def __init__(self, group, pos):
        self.config = GameData()
        super().__init__(group)
        self.pos = Vector2(pos) * self.config.tile_size
        self.height = 32
        self.width = 32
        self.collide_rect = self.get_collide_rect()
        self.direction = Vector2()
        self.speed = 100

    def get_collide_rect(self):
        return pygame.rect.Rect(self.pos.x - self.width / 2, self.pos.y - self.height / 2, self.width, self.height)

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        self.pos += self.direction * self.speed * dt * self.config.tile_scale
        self.collide_rect = self.get_collide_rect()

    def update(self, dt):
        self.move(dt)
