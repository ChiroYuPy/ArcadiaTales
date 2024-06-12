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

        self.animation_state = "idle"
        self.animation_direction = "down"

    def input(self):
        keys = get_pressed()
        up = pygame.K_z
        down = pygame.K_s
        left = pygame.K_q
        right = pygame.K_d

        if not self.config.Chat.chat_open:
            self.direction = Vector2(keys[right] - keys[left], keys[down] - keys[up])
        else:
            self.direction = Vector2()
        self.animation_direction = "right" if self.direction.x > 0 else \
            "left" if self.direction.x < 0 else \
                "down" if self.direction.y > 0 else \
                    "up" if self.direction.y < 0 else (
                        self.animation_direction)
        if self.direction.magnitude() == 0:
            self.animation_state = "idle"
            self.animation_speed = 4
        else:
            self.animation_state = "walk"
            self.animation_speed = 8
        self.current_animation = self.animation_direction + "_" + self.animation_state

    def update(self, dt):
        self.input()
        self.animate(dt)
        super().update(dt)
