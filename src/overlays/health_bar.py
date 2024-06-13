import pygame
from pygame import Vector2, SRCALPHA, Surface

from src.utils.colors import Color


class HealthBar:
    def __init__(self, alive_entity, width, height, offset=(0, 0)):
        self.display_surface = pygame.display.get_surface()
        self.entity = alive_entity
        self.offset = Vector2(offset)
        self.width = width
        self.height = height

    def get_surface(self):
        surface = Surface((self.width, self.height), SRCALPHA)

        if self.entity.max_health > 0:
            health_percentage = self.entity.health / self.entity.max_health
        else:
            health_percentage = 0

        pygame.draw.rect(surface, Color.LIGHT_GRAY, (0, 0, self.width, self.height), border_radius=int(self.height/2))
        pygame.draw.rect(surface, Color.DARK_GREEN, (0, 0, self.width * health_percentage, self.height), border_radius=int(self.height/2))

        return surface
