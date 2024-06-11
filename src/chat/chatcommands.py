# pylint:disable=E1121
# pylint:disable=W0221
from typing import Type


# ----- PARENTS ----- #

# This part of the code represents the base objects (you will inherit from them to create commands and
# subcommands (== command groups))

class ChatBase:
    def __init__(self):
        self.command_set = None

    @staticmethod
    def create_commands(command_set) -> set:
        raise NotImplementedError(
            "This is the parent class, you should create a child and redefine this method"
        )

    @staticmethod
    def add_commands(commands: set):
        for command in commands:
            command.add()

    @classmethod
    def create_chat(cls, chat=None):
        # This is a factory method, it will create an object for you
        # (it's a mix between __new__, __init__ and a simple method)
        if not chat:
            chat = cls()

        command_set = CommandSetBase(chat)
        chat.add_command_set(command_set)

        commands = cls.create_commands(command_set)
        cls.add_commands(commands)

        command_set.load_commands()

        return chat

    @property
    def tree(self):
        return self.command_set.tree

    def add_command_set(self, command_set):
        self.command_set = command_set

    def is_command(self, message: str) -> bool:
        return self.command_set and self.command_set.is_command(message)

    def call_if_command(self, message: str) -> bool:
        if self.is_command(message):
            self.command_set.dispatch_command(message)
            return True
        return False

    def receive_message(self, message: str):  # Should be called on message sent by user
        was_called: bool = self.call_if_command(message)
        if was_called:
            return

        self.send_message(message)

    def send_message(self, message: str):  # Should be called on messages from commands / plugins
        pass


class CommandSetBase:  # Intermediate between the chat and the commands (set prefix to None to create subcommands'
    prefix: str | None = "/"

    def __init__(self, chat: Type[ChatBase]):
        self.commands = {}
        self.chat = chat

    @classmethod
    def is_command(cls, message: str):
        return cls.prefix is None or message.startswith(cls.prefix)

    @property
    def tree(self):
        return {name: command.tree for name, command in self.commands.items()}

    def dispatch_command(self, message: str):
        if message.count(" ") == 0:
            raw_command_name = (self.prefix if self.prefix else "") + message
            argument = ""
        else:
            raw_command_name, argument = message.split(" ", 1)
        command_name = raw_command_name[
                       0 if self.prefix is None else len(self.prefix):
                       ]

        self.call_command(command_name, argument)

    def add_command(self, command):
        command_name = command.name
        if command_name in self.commands:
            raise KeyError(f"This command alreay exists : {command_name}")
        self.commands[command_name] = command

    def load_commands(self):
        for command in self.commands.values():
            command.load()

    def call_command(self, command_name: str, argument: str):
        if not command_name in self.commands:
            raise KeyError(f"This command does not exist : {command_name}")
        self.commands[command_name](argument)


class SubCommandSetBase(CommandSetBase):
    prefix = None


class CommandBase:
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
    """
    # Base class of commands, you can create custom commands by overriding load and __call__
    name: str
    help_message: str | None = None

    def __init__(self, command_set: Type[CommandSetBase]):
        self.command_set = command_set
        self.chat = command_set.chat

        if not hasattr(self, "name"):
            raise NotImplementedError("This command has no name or is the parent class")

    def __call__(self, argument: str):
        if argument.strip(" ") == "help":
            self.chat.send_message(self.help)
        raise NotImplementedError(
            "This command is not callable (this is the parent class)"
        )

    @property
    def tree(self):
        return set()

    @property
    def help(self):
        return self.help_message or "No help available for this command."

    @property
    def full_name(self):
        # TODO: Get the full name of the command (e.g: /chat echo)
        raise NotImplementedError("This feature is not implemented yet.")

    def add(self):
        self.command_set.add_command(self)

    def load(self):
        load_message = f"Loading {self.name}..."
        self.chat.send_message(load_message)  # Do some stuff... (sends a message on loading)


class CommandGroupBase(CommandBase):
    # A builtin command to handle subcommands (inherit and override the create_commands method' to create command
    # groups)
    name: str

    def __init__(self, command_set: Type[CommandSetBase]):
        super().__init__(command_set)
        self.sub_command_set = SubCommandSetBase(self.chat)

    @staticmethod
    def create_commands(command_set: Type[CommandSetBase]) -> set:
        raise NotImplementedError(
            "This is the base command group, you should create a child and override this method"
        )

    @staticmethod
    def add_commands(commands: set):
        for command in commands:
            command.add()

    @property
    def tree(self):
        return self.sub_command_set.tree

    def load(self):
        commands = self.create_commands(self.sub_command_set)
        self.add_commands(commands)
        self.sub_command_set.load_commands()

    def __call__(self, argument: str):
        if argument.strip(" "):
            self.sub_command_set.dispatch_command(argument)
            return
        self.chat.send_message(self.help)


if __name__ == "__main__":
    pass
