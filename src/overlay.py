import pygame

from gamedata import GameData


class Overlay:
    def __init__(self, game):
        self.display_surface = pygame.display.get_surface()
        self.config = GameData()
        self.game = game
        self.clock = self.game.clock

        self.f3_font = pygame.font.Font("assets/fonts/Bubble.ttf", 12)
        self.texts = []

    def update_texts(self):
        self.texts = [
            f'Player Position: ({int(self.game.level.player.pos.x)}, {int(self.game.level.player.pos.y)})',
            f'FPS: {int(self.clock.get_fps())}',
        ]

    def draw(self):
        if self.config.debug:
            self.update_texts()
            for i, text in enumerate(self.texts):
                text_surf = self.f3_font.render(text, True, (255, 255, 255))
                text_rect = text_surf.get_rect(topleft=(10, 10 + i * 12))
                self.display_surface.blit(text_surf, text_rect)
