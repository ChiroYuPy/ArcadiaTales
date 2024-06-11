import pygame
from pygame import Vector2
from pygame.key import get_pressed

from gamedata import GameData
from src.entities.animatedentity import AnimatedEntity


class Enemy(AnimatedEntity):
    def __init__(self, group, pos, animations, image_offset):
        self.config = GameData()

        super().__init__(group=group,
                         pos=pos,
                         animations=animations,
                         image_offset=image_offset)
        self.import_assets(scale=self.config.tile_scale)

    def update(self, dt):
        self.animate(dt)
        super().update(dt)
