from enum import Enum

from src.config.game_data import GameData
from src.chat.commands import Commands


class ErrorLevel(Enum):
    INFO = "&7"      # Informative message
    WARNING = "&e"   # Warning message
    ERROR = "&c"     # Error message
    CRITICAL = "&4"  # Critical message


class Command:
    def __init__(self, arg_desc):
        self.arg_desc = arg_desc


class ChatCore:
    def __init__(self, game):
        self.messages = []
        self.game = game
        self.data = GameData()
        self.commands = Commands.create_chat(self, game)

    def show_message(self, message):
        """Shows a message in the chat."""
        self.messages.append(message)
        self.trim_messages()

    def add_message(self, message):
        """Adds a message received by the user to the chat."""
        self.commands.receive_message(message)

    def send_error_log(self, message, level=ErrorLevel.ERROR):
        """Sends an error message in the chat."""
        self.messages.append(f"{level.value} Error: {message}")
        self.trim_messages()

    def trim_messages(self):
        """Removes messages out of the limit specified by the configuration."""
        while len(self.messages) > self.data.Chat.max_messages:
            self.messages.pop(0)

    def get_messages(self):
        """Reverses the list of actual messages in the chat."""
        return self.messages

    def clear_last_message(self, args=None):
        """Removes last message of the chat."""
        if self.messages:
            self.messages.pop()
        else:
            self.send_error_log("Aucun message à supprimer.", ErrorLevel.WARNING)

    def clear_all_messages(self, args=None):
        """Clears every message in the chat."""
        if self.messages:
            self.messages.clear()
        else:
            self.send_error_log("Aucun message à supprimer.", ErrorLevel.WARNING)
