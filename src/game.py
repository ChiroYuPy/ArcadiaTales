import pygame
from pygame.time import Clock

from src.config.gamedata import GameData
from src.chat.chatcore import ChatCore
from src.chat.chatui import ChatUI
from src.map.level import Level
from src.overlay import Overlay


class Game:
    def __init__(self):
        self.running = True
        self.config = GameData()

        self.display_surface = pygame.display.set_mode(
            (self.config.window_width, self.config.window_height),
            pygame.NOFRAME if not self.config.window_frame else False | pygame.RESIZABLE if self.config.window_resizable else False)
        pygame.display.set_caption(self.config.window_caption + " v" + self.config.game_version)
        self.clock = Clock()
        self.level = Level(self, self.clock)
        self.overlay = Overlay(self)
        self.chat = ChatCore(self)
        self.chat_ui = ChatUI(self.chat)
        self.startup()

    def startup(self):
        self.chat.show_message("&bWelcome &7to the chat system!")
        self.chat.show_message("&7Use &bt &7to open the Chat")
        self.chat_ui.update_surfaces()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            # TODO: Do you know match / case ? You should split thins function into smaller pieces
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.VIDEORESIZE:
                self.config.window_width, self.config.window_height = event.size
                self.display_surface = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                if self.config.Chat.chat_open:
                    self.chat_ui.handle_event(event)
                if event.key == pygame.K_t and not self.config.Chat.chat_open:
                    self.config.Chat.chat_open = True
                if event.key == pygame.K_ESCAPE:
                    if self.config.Chat.chat_open:
                        self.config.Chat.chat_open = False
                    else:
                        self.quit_game()
                if event.key == pygame.K_F3:
                    self.config.debug_level += 1
                    if self.config.debug_level > 4:
                        self.config.debug_level = 0

    def quit_game(self):

        self.running = False

    def update(self):
        dt = self.clock.tick(self.config.max_fps) / 1000
        self.level.update(dt)
        self.overlay.update_texts()

    def render(self):
        self.display_surface.fill((32, 0, 0))
        self.draw()
        pygame.display.flip()

    def draw(self):
        self.level.draw()
        self.chat_ui.draw()
        self.overlay.draw()
