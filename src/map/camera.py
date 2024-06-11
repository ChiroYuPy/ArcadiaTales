import pygame
from pygame import Vector2
from pygame.sprite import Group

from gamedata import GameData


class Camera(Group):
    def __init__(self):
        super().__init__()
        self.config = GameData()
        self.display_surface = pygame.display.get_surface()
        self.offset = Vector2()

    def customize_draw(self, player):
        self.offset = player.pos - Vector2(self.config.window_width / 2, self.config.window_height / 2)
        sprites_sorted = sorted(self.sprites(), key=lambda sprite: sprite.pos.y)
        for sprite in sprites_sorted:
            offset_pos = sprite.pos.copy()
            offset_pos -= self.offset
            image_width = sprite.image.get_width()
            image_height = sprite.image.get_height()
            image_shape = image_width, image_height
            hitbox_shape = sprite.collide_rect.width, sprite.collide_rect.height
            centered_pos = Vector2(offset_pos.x - image_width / 2 + sprite.image_offset.x,
                                   offset_pos.y - image_height / 2 + sprite.image_offset.y)
            self.display_surface.blit(sprite.image, centered_pos)
            if self.config.debug:
                self.draw_debug_squares(sprite, offset_pos, image_shape, hitbox_shape)

    def draw_debug_squares(self, sprite, offset_pos, image_shape, hitbox_shape):
        image_width, image_height = image_shape
        hitbox_width, hitbox_height = hitbox_shape

        # Draw the image rectangle
        pygame.draw.rect(self.display_surface,
                         (0, 255, 0),
                         (offset_pos.x - image_width / 2 + sprite.image_offset.x,
                          offset_pos.y - image_height / 2 + sprite.image_offset.y,
                          image_width,
                          image_height),
                         width=1)

        # Draw the hitbox rectangle
        pygame.draw.rect(self.display_surface,
                         (255, 0, 0),
                         (offset_pos.x - hitbox_width / 2,
                          offset_pos.y - hitbox_height / 2,
                          hitbox_width,
                          hitbox_height),
                         width=1)
