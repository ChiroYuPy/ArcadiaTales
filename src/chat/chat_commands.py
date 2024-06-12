# pylint:disable=E1121
# pylint:disable=W0221


# ----- PARENTS ----- #

# This part of the code represents the base objects (you will inherit from them to create commands and
# subcommands (== command groups))

class UserMistake(Exception):
    """Exception thrown when a user makes a mistake."""


class CommandManager:
    @staticmethod
    def create_commands() -> set:
        raise NotImplementedError("You should override this method")

    @staticmethod
    def add_commands(commands):
        for command in commands:
            command.add()

    @staticmethod
    def init_commands(commands, command_set):
        for command in commands:
            yield command(command_set)

    @classmethod
    def install_commands(cls, command_set):
        commands = cls.create_commands()
        initialized_commands = cls.init_commands(commands, command_set)
        cls.add_commands(initialized_commands)
        command_set.load_commands()


class ErrorManager:
    def __init__(self, chat):
        self.chat = chat

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            return True

        error = exc_type(exc_value)
        error.with_traceback(exc_tb)

        if issubclass(exc_type, UserMistake):
            self.chat.log_user_mistake(error)
            return True

        self.chat.log_error(error)
        return True


class Chat(CommandManager):
    def __init__(self):
        self.command_set = None
        self.prefix: str | None = None

    @classmethod
    def create_chat(cls, *args, **kwargs):
        # This is a factory method, it will create an object for you
        # (it's a mix between __new__, __init__ and a simple method)
        _ = args, kwargs  # To avoid unused arguments warnings

        chat = kwargs.get("chat")

        if not chat:
            chat = cls()

        command_set = CommandSetBase(chat, chat)
        chat.add_command_set(command_set)

        cls.install_commands(command_set)

        return chat

    @property
    def prefix_length(self) -> int:
        if self.command_set is None:
            return 0
        return len(self.command_set.prefix or "")

    @property
    def tree(self) -> dict:
        if self.command_set is None:
            return {}
        return self.command_set.tree

    def remove_prefix(self, text: str):
        return text[self.prefix_length:]

    def add_command_set(self, command_set):
        self.command_set = command_set
        self.prefix = command_set.prefix

    def is_command(self, message: str) -> bool:
        if self.command_set is None:
            return False
        return self.command_set.is_command(message)

    def call_if_command(self, message: str) -> bool:
        if self.is_command(message) and self.command_set is not None:
            self.command_set.dispatch_command(message)
            return True
        return False

    def complete(self, text):
        if not self.is_command(text):
            return ()

        current_text = self.remove_prefix(text)
        leaf = self.tree.copy()

        while " " in current_text:
            word, current_text = current_text.split(" ", 1)
            if word not in leaf:
                break

            leaf = leaf[word]

        return filter(lambda x: x.startswith(current_text), leaf)

    def error_manager(self):
        return ErrorManager(self)

    def receive_message(self, message: str):  # Should be called on message sent by user
        was_called = True
        _ = was_called  # To avoid linter's warning

        with self.error_manager():
            was_called = self.call_if_command(message)

        if was_called:
            return

        self.send_message(message)

    def send_message(self, message: str):  # Should be called on messages from commands / plugins
        raise NotImplementedError("You should override this method")

    def log_user_mistake(self, error):
        raise NotImplementedError("You should override this method")

    def log_error(self, error):
        raise NotImplementedError("You should override this method")

    def clear(self):
        raise NotImplementedError("You should override this method")


class CommandSetBase:
    """
    Parameters
    ----------
    chat
    parent

    Attributes
    ----------
    chat
    parent

    Methods
    -------
    is_command(message: str)
    """
    # Intermediate between the chat and the commands (set prefix to None to create subcommands)
    prefix: str | None = "/"

    def __init__(self, chat, parent):
        self.commands = {}
        self.chat = chat
        self.parent = parent

    @classmethod
    def is_command(cls, message: str) -> bool:
        return cls.prefix is None or message.startswith(cls.prefix)

    @property
    def tree(self) -> set | dict:
        return {name: command.tree for name, command in self.commands.items()}

    def dispatch_command(self, message: str):
        if " " not in message:
            raw_command_name, argument = message, ""
        else:
            raw_command_name, argument = message.split(" ", 1)
        command_name = raw_command_name[
                       0 if self.prefix is None else len(self.prefix):
                       ]

        self.call_command(command_name, argument)

    def add_command(self, command):
        command_name = command.name
        if command_name in self.commands:
            raise KeyError(f"This command already exists : {command_name}")
        self.commands[command_name] = command

    def load_commands(self):
        for command in self.commands.values():
            command.load()

    def call_command(self, command_name: str, argument: str):
        if not (not command_name or command_name in self.commands):
            raise UserMistake(f"This command does not exist : {command_name}")
        self.commands[command_name].trigger(argument)


class SubCommandSetBase(CommandSetBase):
    prefix = None


class Command:
    """
    Parent class of every command.
    When inheriting from this class, the child class must override:
        Methods:
            - __call__(self, argument: str)
        Properties:
            - name: str
    And should have:
        Methods:
            None
        Properties:
            - help (as a property / getter)
            - help_message (if you don't want to set the help property)
            - tree (as a property / getter)

    Parameters
    ----------
    command_set
        The parent of this node. Should be a ``CommandSetBase``

    Attributes
    ----------
    name : str
    help_message : str
    command_set
        Should be a ``CommandSetBase`` subclass.

    Methods
    -------
    __call__(argument: str)
        The function called when a user triggers the command.
    generate_help()
    add()
    load()
        Function triggered when the command is loaded (should be when creating a chat).

    """
    # Base class of commands, you can create custom commands by overriding load and __call__
    name: str
    help_message: str = "No help available for this command."

    def __init__(self, command_set):
        self.command_set = command_set
        self.chat = command_set.chat

        if not hasattr(self, "name"):
            raise NotImplementedError("This command has no name or is the parent class")

    def __call__(self, argument: str):
        raise NotImplementedError(
            "You should override this method"
        )

    @property
    def tree(self) -> set | dict:
        """set: List of subcommands."""
        return set()

    @property
    def help(self):
        """str: Will generate the documentation."""
        return self.generate_help()

    @property
    def full_name(self) -> str:
        """str: Full name of the command (e.g : ``/chat echo``)."""
        path = []
        node = self

        while node is not self.chat:
            path.append(node.name)
            node = node.command_set.parent

        return self.chat.prefix + " ".join(path[::-1])

    def generate_help(self):
        message = f"{self.full_name}: {self.help_message}"
        tree = self.tree.copy()

        if not tree:
            return message

        message += "\n\nAvailable subcommands :"
        for key in tree:
            message += f"\n- {key}"

        return message

    def add(self):
        self.command_set.add_command(self)

    def load(self):
        load_message = f"Loading {self.name}..."
        self.chat.send_message(load_message)  # Do some stuff... (sends a message on loading)

    def trigger(self, argument: str):
        if not "help" in self.tree and argument.strip(" ") == "help":
            self.chat.send_message(self.help)
            return
        return self(argument)


class CommandGroup(Command, CommandManager):
    """
    A builtin command to handle subcommands (inherit and override the create_commands method to create command
    groups).
    """
    name: str

    def __init__(self, command_set):
        super().__init__(command_set)
        self.sub_command_set = SubCommandSetBase(self.chat, self)

    @property
    def tree(self) -> set | dict:
        return self.sub_command_set.tree

    def load(self):
        self.install_commands(self.sub_command_set)

    def __call__(self, argument: str):
        if argument.strip(" "):
            self.sub_command_set.dispatch_command(argument)
            return
        self.chat.send_message(self.help)


def test():
    # TODO: Use unit tests instead
    import json

    class SetEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, set):
                return list(o)
            return json.JSONEncoder.default(self, o)

    print("================= TEST MODE =================\n")

    # Adapters

    class TextChat(Chat):
        @staticmethod
        def create_commands():
            return set()

        def send_message(self, message: str):
            print(message)

        def clear(self):
            print("\033c\033[3J", end='')

        def log_user_mistake(self, error):
            self.send_message(f"\033[91m{error}\033[0m")

        def log_error(self, error):
            # Some logging stuff...
            self.send_message("\033[91mAn unexpected error has occurred\033[0m")

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
            super().load()
            self._god_mode_state = False

        def __call__(self, argument: str):
            state = self._god_mode_state

            self.chat.send_message(
                "God mode deactivated"
                if state else "God mode activated"
            )

            self._god_mode_state = not state

    class MockError(Command):
        name = "error"

        def __call__(self, argument: str):
            self.chat.send_message(1 / 0)

    class MockFullName(Command):
        name = "full_name"

        def __call__(self, argument: str):
            self.chat.send_message(self.full_name)

    class MockFullTree(Command):
        name = "full_tree"

        def __call__(self, argument: str):
            self.chat.send_message(json.dumps(self.chat.tree, indent=4, cls=SetEncoder))

    class Exit(Command):
        name = "exit"

        def __call__(self, argument: str):
            _ = argument  # To avoid linter's warning
            exit()

    # Command Groups

    class ChatCommands(CommandGroup):

        # Creates a simple group of commands (subcommands)
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
            }

    class MockCommands(CommandGroup):
        name = "mock"

        @staticmethod
        def create_commands():
            return {
                MockError,
                MockFullName,
                MockFullTree,
            }

    # Chats

    class MyChat(TextChat):
        @staticmethod
        def create_commands():
            return {
                ChatCommands,
                GameCommands,
                MockCommands,
                Exit,
            }

    # Main

    mychat = MyChat.create_chat()

    mock_messages = (
        "basic test message",
        "/chat echo this is a test for echo",
        "/chat",
        "/chat help",
        "/chat clear help",
        "/I_Dont_Exist",
        "/mock error",
        "/mock full_name",
        "/mock full_tree",
    )

    print("\n\n----- Starting Tests ----\n")

    for mock_message in mock_messages:
        print("$", mock_message)
        mychat.receive_message(mock_message)

    print("\n----- Ending Tests -----\n\n")

    import os
    while True:
        os.system(input("$ "))

    while True:
        mychat.receive_message(input('$ '))


if __name__ == "__main__":
    test()
