try:
    from src.chat.chatcommands import CommandBase, CommandGroupBase, ChatBase
except ImportError:
    from chatcommands import CommandBase, CommandGroupBase, ChatBase
import traceback


# Adapters

class GameChat(ChatBase):

    def __init__(self):
        super().__init__()
        self.core = None
        self.game = None

    @classmethod
    def create_chat(cls, core, game):
        chat = cls()
        chat.add_core(core)
        chat.add_game(game)

        return super().create_chat(chat=chat)

    def log_user_mistake(self, error):
        self.core.send_error_log(f"{error}.")
    
    def log_error(self, error):
        traceback.print_tb(error.__traceback__)
        self.core.send_error_log("An unexpected error occured.")

    def add_core(self, core):
        self.core = core
    
    def add_game(self, game):
        self.game = game

    def send_message(self, message):
        self.core.show_message(message)
    
    def clear(self):
        self.core.clear_all_messages()


# Commands

class Echo(CommandBase):
    name = "echo"

    def __call__(self, argument: str):  # When command is called by the user
        self.chat.send_message(argument)


class Clear(CommandBase):
    name = "clear"
    help_message = """Clears the chat (returns an error if there is nothing to clear)."""

    def __call__(self, argument: str):
        self.chat.clear()


class GodMode(CommandBase):
    name = "godmode"
    _god_mode_state: bool
    
    def load(self):
        self._god_mode_state = False

    def __call__(self, argument: str):
        state = self._god_mode_state
        
        message = "God mode deactivated" \
        if state else "God mode activated"
        
        self.chat.send_message(message)
        self._god_mode_state = not(state)
        


# Command Groups

class ChatCommands(CommandGroupBase):  # Creates a simple group of commands (subcommands)
    name = "chat"  # Name of the group

    @staticmethod
    def create_commands():
        # Initializes commands of the group (and returns them in a set)
        return {
            Echo,
            Clear,
        }


class GameCommands(CommandGroupBase):
    name = "game"

    @staticmethod
    def create_commands():
        return {
            GodMode,
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



