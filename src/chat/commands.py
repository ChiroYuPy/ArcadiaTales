from src.chat.chatcommands import CommandBase, CommandGroupBase, ChatBase


class Echo(CommandBase):
    name = "echo"

    @property
    def tree(self):
        return set()

    @property
    def help(self):
        return """Example command, repeats the argument."""

    def __call__(self, argument: str):  # When command is called by the user
        self.chat.send_message(argument)


class Clear(CommandBase):
    name = "clear"
    help_message = """Clears the chat (returns an error if there is nothing to clear)."""

    def __call__(self, argument: str):  # When command is called by the user
        self.chat.game.clear_all_messages()


class ChatCommands(CommandGroupBase):  # Creates a simple group of commands (subcommands)
    name = "chat"  # Name of the group

    @staticmethod
    def create_commands(command_set):
        # Initializes commands of the group (and returns them in a set)
        return {
            Echo(command_set),
            Clear(command_set)
        }


class GodMode(CommandBase):
    name = "godmode"

    def load(self):  # Do some stuff... (sends a message on loading)
        load_message = f"Loading {self.name}..."
        self.chat.send_message(load_message)

    def __call__(self, argument: str):  # When command is called by the user
        self.chat.send_message(f"God mode activated")


class GameCommands(CommandGroupBase):  # Creates a simple group of commands (subcommands)
    name = "game"  # Name of the group

    @staticmethod
    def create_commands(command_set):
        # Initializes commands of the group (and returns them in a set)
        return {
            GodMode(command_set),
        }


class MyChat(ChatBase):

    def __init__(self):
        super().__init__()
        self.game = None

    @staticmethod
    def create_commands(command_set):
        return {
            ChatCommands(command_set),
            GameCommands(command_set)
        }

    @classmethod
    def create_chat(cls, game):
        chat = cls()
        chat.add_game(game)

        return super().create_chat(chat=chat)

    def call_if_command(self, message) -> bool:
        try:
            return super().call_if_command(message)
        except KeyError as e:
            self.send_message(f"Unknown command: {e}")
            return True

    def add_game(self, game):
        self.game = game

    def send_message(self, message):
        self.game.show_message(message)
