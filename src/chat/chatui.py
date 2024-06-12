import pygame
import pygame.freetype

from src.config.gamedata import GameData
from src.utils.utils import format_text, draw_formatted_message


class ChatUI:
    def __init__(self, chat):
        self.screen = pygame.display.get_surface()
        self.chat = chat
        self.config = GameData()
        self.chat_font = pygame.freetype.Font("assets/fonts/LycheeSoda.ttf", self.config.Chat.font_size)
        self.input_text = ""
        self.cursor_pos = 0
        self.chat_surfaces = []
        self.input_surface = None
        self.completer_surface = None
        self.update_surfaces()
        self.message_history = []
        self.history_index = -1

    def handle_event(self, event):
        allowed_characters = ("abcdefghijklmnopqrstuvwxyz"
                              "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                              "éèçàêâîôûäëïöüÿâêîôû"
                              "1234567890"
                              "#@&%$=+-/,.!?;:()[]{}<> '")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_text.strip():
                    self.chat.add_message(self.input_text)
                    self.message_history.insert(0, self.input_text)
                    self.history_index = -1
                    self.input_text = ""
                    self.cursor_pos = 0
                    self.config.Chat.chat_open = False
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.input_text = self.input_text[:self.cursor_pos - 1] + self.input_text[self.cursor_pos:]
                    self.cursor_pos -= 1
            elif event.key == pygame.K_LEFT:
                if self.cursor_pos > 0:
                    self.cursor_pos -= 1
            elif event.key == pygame.K_RIGHT:
                if self.cursor_pos < len(self.input_text):
                    self.cursor_pos += 1
            elif event.key == pygame.K_UP:
                self.navigate_message_history(-1)
            elif event.key == pygame.K_DOWN:
                self.navigate_message_history(1)
            elif event.key == pygame.K_DELETE:
                if self.cursor_pos < len(self.input_text):
                    self.input_text = self.input_text[:self.cursor_pos] + self.input_text[self.cursor_pos + 1:]
            elif event.unicode in allowed_characters:
                if len(self.input_text) < self.config.Chat.max_input_characters:
                    self.input_text = self.input_text[:self.cursor_pos] + event.unicode + self.input_text[
                                                                                          self.cursor_pos:]
                    self.cursor_pos += 1

            self.update_surfaces()  # Ensure surfaces are updated on each input change

    def navigate_message_history(self, direction):
        if direction == -1:
            if self.history_index < len(self.message_history) - 1:
                self.history_index += 1
        elif direction == 1:
            if self.history_index == 0:
                self.history_index = -1
            elif self.history_index > 0:
                self.history_index -= 1

        if 0 <= self.history_index < len(self.message_history):
            self.input_text = self.message_history[self.history_index]
            self.cursor_pos = len(self.input_text)
        else:
            self.input_text = ""

    def update_surfaces(self):
        # TODO: You should split this function into smaller pieces
        completer_texts = self.update_completer()

        # Update chat surface
        self.chat_surfaces.clear()
        recent_messages = self.chat.get_messages()[-self.config.Chat.max_shown_messages:]

        for message in reversed(recent_messages):
            message_surface = pygame.Surface((self.config.Chat.width, self.config.Chat.font_size*0.6), pygame.SRCALPHA)
            message_surface.fill((30, 30, 30, 127))
            draw_formatted_message(self.chat_font, message_surface, format_text(message), (0, 0))
            self.chat_surfaces.append(message_surface)

        # Update input surface width based on input text width
        input_text_width = self.chat_font.get_rect(self.input_text).width
        input_surface_width = input_text_width + 10
        input_surface = pygame.Surface((input_surface_width, self.config.Chat.font_size), pygame.SRCALPHA)
        input_surface.fill((30, 30, 30, 127))
        self.chat_font.render_to(input_surface, (5, 5), self.input_text, (255, 255, 255))

        # Draw the cursor
        cursor_x_pos = self.chat_font.get_rect(self.input_text[:self.cursor_pos]).width + 5
        pygame.draw.rect(input_surface, (0, 255, 0), (cursor_x_pos - 1, 0, 2, self.config.Chat.font_size))

        self.input_surface = input_surface

        # Update completer surface
        completer_surface_height = self.config.Chat.font_size * len(completer_texts)
        completer_surface = pygame.Surface((80, completer_surface_height), pygame.SRCALPHA)
        completer_surface.fill((32, 32, 32, 127))
        y_offset = completer_surface_height - self.config.Chat.font_size  # Commencer depuis le bas
        for text in completer_texts:
            self.chat_font.render_to(completer_surface, (5, y_offset + 5), text, (255, 255, 255))
            y_offset -= self.config.Chat.font_size  # Déplacer vers le haut pour le texte suivant
        self.completer_surface = completer_surface

    def draw(self):
        y_offset = self.config.window_height - 80
        for surface in self.chat_surfaces:
            self.screen.blit(surface, (0, y_offset))
            y_offset -= surface.get_height()

        x, y = (0, self.config.window_height - self.input_surface.get_height() - 2)
        if self.input_surface and self.config.Chat.chat_open:
            self.screen.blit(self.input_surface, (x, y))

        if self.completer_surface and self.config.Chat.chat_open:
            x += self.input_surface.get_width() - 6
            self.screen.blit(self.completer_surface, (x, y - self.completer_surface.get_height()))

    def update_completer(self):
        text = self.input_text
        tree = self.chat.chat.tree

        if not text.startswith("/"):
            return ()

        word = current_text = text[1:]
        leaf = tree.copy()
        argument = None

        while " " in current_text:
            word, argument = current_text.split(" ", 1)
            current_text = argument
            if word not in leaf:
                break
            leaf = leaf[word]

        return tuple(filter(lambda x: x.startswith(current_text), leaf))
