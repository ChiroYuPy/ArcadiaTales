from src.chat.chat_commands import Command, CommandGroup, Chat
import traceback


# Adapters


class GameChat(Chat):

    def __init__(self):
        super().__init__()
        self.core = None
        self.game = None

    @classmethod
    def create_chat(cls, core, game, chat=None):
        if not chat:
            chat = cls()
        chat.add_core(core)
        chat.add_game(game)

        return super().create_chat(chat=chat)

    def log_user_mistake(self, error):
        self.core.send_error_log(f"{error}.")

    def log_error(self, error):
        traceback.print_tb(error.__traceback__)
        self.core.send_error_log("An unexpected error occurred.")

    def add_core(self, core):
        self.core = core

    def add_game(self, game):
        self.game = game

    def send_message(self, message):
        self.core.show_message(message)

    def clear(self):
        self.core.clear_all_messages()


# Commands

class Echo(Command):
    name = "echo"

    def __call__(self, argument: str):  # When command is called by the user
        self.chat.send_message(argument)


class Clear(Command):
    name = "clear"
    help_message = """Clears the chat (returns an error if there is nothing to clear)."""

    def __call__(self, argument: str):
        self.chat.clear()


class GodMode(Command):
    name = "god_mode"
    _god_mode_state: bool

    def load(self):
        self._god_mode_state = False

    def __call__(self, argument: str):
        state = self._god_mode_state

        message = "God mode deactivated" \
            if state else "God mode activated"

        self.chat.send_message(message)
        self._god_mode_state = not state


class Teleport(Command):
    name = "tp"

    @staticmethod
    def _is_int(n: str):
        if n.startswith("-"):
            n = n[1:]
        return n.isdigit()

    def __call__(self, argument: str):
        argument = argument.strip().split()

        if len(argument) != 2:
            self.chat.send_message("Please provide both x and y coordinates.")
            return

        if not all(self._is_int(n) for n in argument):
            self.chat.send_message("Invalid coordinates.")
            return

        x, y = map(int, argument)

        self.chat.game.level.player.fall((x * self.chat.game.config.tile_size, y * self.chat.game.config.tile_size))

        self.chat.send_message(f"Teleported to ({x}, {y}).")


class Summon(Command):
    name = "summon"

    @staticmethod
    def _is_int(n: str):
        if n.startswith("-"):
            n = n[1:]
        return n.isdigit()

    def __call__(self, argument: str):
        argument = argument.strip().split()

        if len(argument) != 3:
            self.chat.send_message("Please provide both entity name, x and y coordinates.")
            return

        if not all(self._is_int(n) for n in argument[1:]):
            self.chat.send_message("Invalid coordinates.")
            return

        entity_name, x, y = argument[0], int(argument[1]), int(argument[2])

        self.chat.game.level.entity_manager.spawn_entity(entity_name, (x, y))

        self.chat.send_message(f"Summoned {entity_name} at ({x}, {y}).")


# Command Groups

class ChatCommands(CommandGroup):  # Creates a simple group of commands (subcommands)
    name = "chat"  # Name of the group

    @staticmethod
    def create_commands():
        # Initializes commands of the group (and returns them in a set)
        return {
            Echo,
            Clear,
        }


class GameCommands(CommandGroup):
    name = "game"

    @staticmethod
    def create_commands():
        return {
            GodMode,
            Teleport,
            Summon,
        }


# Chats

class Commands(GameChat):
    @staticmethod
    def create_commands():
        return {
            ChatCommands,
            GameCommands,
        }


if __name__ == "__main__":
    # TODO: Test chat
    pass
