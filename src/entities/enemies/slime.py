import pygame
from pygame import Vector2
from pygame.key import get_pressed

from gamedata import GameData
from src.entities.enemies.enemy import Enemy


class Slime(Enemy):
    def __init__(self, group, pos):
        self.config = GameData()

        super().__init__(group=group,
                         pos=pos,
                         animations={'up_walk': [], 'down_walk': [], 'left_walk': [], 'right_walk': [],
                                     'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                                     'right_atk': [], 'left_atk': [], 'up_atk': [], 'down_atk': []},
                         image_offset=(0, -4))
        self.import_assets(scale=self.config.tile_scale)

        self.animation_state = "idle"
        self.animation_direction = "down"
        self.speed = self.config.slime_speed

    def update(self, dt):
        self.input()
        self.animate(dt)
        super().update(dt)
