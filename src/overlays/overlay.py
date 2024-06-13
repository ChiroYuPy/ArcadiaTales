import pygame

from src.config.game_data import GameData
from src.utils.colors import Color


class Overlay:
    def __init__(self, game):
        self.display_surface = pygame.display.get_surface()
        self.config = GameData()
        self.game = game
        self.clock = self.game.clock

        self.f3_font = pygame.font.Font("assets/fonts/Bubble.ttf", 12)
        self.texts = []
        self.previous_texts = None
        self.text_surfaces = []
        self.text_rects = []

    def update_texts(self):
        player_pixel_pos = self.game.level.player.pos
        player_tile_pos = self.game.level.tile_map_generator.get_tile_position(self.game.level.player.pos)
        new_texts = [
            f'Player Pixel Position: ({int(player_pixel_pos.x)}, {int(player_pixel_pos.y)})',
            f'Player Tile Position: ({int(player_tile_pos.x)}, {int(player_tile_pos.y)})',
            f'FPS: {int(self.clock.get_fps())}',
            f'Player Speed: {self.config.player_speed}',
            f'Player Health: {self.config.player_health}',
            f'Entities number: {len(self.game.level.entity_manager.enemies)+1}',
        ]

        if new_texts != self.previous_texts:
            self.texts = new_texts
            self.previous_texts = new_texts
            self.text_surfaces = [self.f3_font.render(text, True, Color.WHITE) for text in self.texts]
            self.text_rects = [text_surf.get_rect(topleft=(10, 10 + i * 12)) for i, text_surf in enumerate(self.text_surfaces)]

    def draw(self):
        if self.config.debug_level == 1 or self.config.debug_level == 4:
            self.update_texts()
            for text_surf, text_rect in zip(self.text_surfaces, self.text_rects):
                self.display_surface.blit(text_surf, text_rect)