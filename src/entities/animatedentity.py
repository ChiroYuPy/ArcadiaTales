import pygame
from pygame import Vector2

from src.entities.entity import Entity
from src.utils.utils import import_folder


class AnimatedEntity(Entity):
    def __init__(self, group, pos, animations, image_offset=(0, 0)):
        super().__init__(group=group, pos=pos)
        self.animations = animations
        self.current_animation = "down_idle"
        self.current_frame = 0
        self.current_time = 0
        self.animation_speed = 1
        self.image_offset = Vector2(image_offset)
        self.name = "animated_entity"

    def import_assets(self, scale=1):
        for animation in self.animations.keys():
            full_path = f'assets/images/entities/{self.name}/' + animation
            animation_images = import_folder(full_path)
            for index, image in enumerate(animation_images):
                scaled_width = int(image.get_width() * scale)
                scaled_height = int(image.get_height() * scale)
                animation_images[index] = pygame.transform.scale(image, (scaled_width, scaled_height))
            self.animations[animation] = animation_images
        self.image = self.animations[self.current_animation][int(self.current_frame)]

    def animate(self, dt):
        self.current_frame += self.animation_speed * dt
        if self.current_frame >= len(self.animations[self.current_animation]):
            self.current_frame = 0
        self.image = self.animations[self.current_animation][int(self.current_frame)]

    def update(self, dt):
        super().update(dt)
        self.animate(dt)
