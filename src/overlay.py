import pygame

from src.config.gamedata import GameData
from src.utils.colors import Color


class Overlay:
    def __init__(self, game):
        self.display_surface = pygame.display.get_surface()
        self.config = GameData()
        self.game = game
        self.clock = self.game.clock

        self.f3_font = pygame.font.Font("assets/fonts/Bubble.ttf", 12)
        self.texts = []

    def update_texts(self):
        player_pixel_pos = self.game.level.player.pos
        player_tile_pos = self.game.level.get_tile_position(self.game.level.player.pos)
        self.texts = [
            f'Player Pixel Position: ({int(player_pixel_pos.x)}, {int(player_pixel_pos.y)})',
            f'Player Tile Position: ({int(player_tile_pos.x)}, {int(player_tile_pos.y)})',
            f'FPS: {int(self.clock.get_fps())}',
            f'Config Debug Level: {self.config.debug_level}',
            f'Config Player Speed: {self.config.player_speed}',
        ]

    def draw(self):
        if self.config.debug_level == 1 or self.config.debug_level == 4:
            self.update_texts()
            for i, text in enumerate(self.texts):
                text_surf = self.f3_font.render(text, True, Color.WHITE)
                text_rect = text_surf.get_rect(topleft=(10, 10 + i * 12))
                self.display_surface.blit(text_surf, text_rect)
