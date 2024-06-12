from pygame import display, draw
from pygame import Vector2
from pygame.sprite import Group
from pygame.freetype import Font

from src.config.game_data import GameData
from src.utils.colors import Color
from src.utils.utils import draw_formatted_message, format_text


class Camera(Group):
    def __init__(self):
        super().__init__()
        self.config = GameData()
        self.display_surface = display.get_surface()
        self.offset = Vector2()
        self.font = Font("assets/fonts/LycheeSoda.ttf", self.config.Chat.font_size)

    def shifted_draw(self, player):
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

            if sprite.name:
                formatted_message = format_text(sprite.name)

                # Calculate total width and height of the formatted text
                total_text_width = sum(self.font.get_rect(text).width for text, _ in formatted_message)
                total_text_height = sum(self.font.get_rect(text).height for text, _ in formatted_message)

                # Center the text on both x and y axes
                text_pos = (offset_pos.x - total_text_width / 2 + sprite.name_offset.x,
                            offset_pos.y - total_text_height / 2 + sprite.name_offset.y)

                draw_formatted_message(font=self.font,
                                       surface=self.display_surface,
                                       formatted_message=formatted_message,
                                       pos=text_pos)

            if self.config.debug_level == 2 or self.config.debug_level == 4:
                self.draw_debug_squares(sprite, offset_pos, image_shape, hitbox_shape)

    def draw_debug_squares(self, sprite, offset_pos, image_shape, hitbox_shape):
        image_width, image_height = image_shape
        hitbox_width, hitbox_height = hitbox_shape

        # Draw the image rectangle
        draw.rect(self.display_surface,
                  Color.DARK_GREEN,
                  (offset_pos.x - image_width / 2 + sprite.image_offset.x,
                   offset_pos.y - image_height / 2 + sprite.image_offset.y,
                   image_width,
                   image_height),
                  width=1)

        # Draw the hitbox rectangle
        draw.rect(self.display_surface,
                  Color.DARK_RED,
                  (offset_pos.x - hitbox_width / 2,
                   offset_pos.y - hitbox_height / 2,
                   hitbox_width,
                   hitbox_height),
                  width=1)
