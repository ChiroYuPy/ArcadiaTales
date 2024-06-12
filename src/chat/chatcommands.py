# pylint:disable=E1121
# pylint:disable=W0221
from typing import Type, Iterable


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


class ChatBase(CommandManager):
    def __init__(self):
        self.command_set = None
        self.prefix = None
    
    @classmethod
    def create_chat(cls, *args, chat=None, **kwargs):
        # This is a factory method, it will create an object for you
        # (it's a mix between __new__, __init__ and a simple method)
        _ = args, kwargs  # To avoid unused arguments warnings
        
        if not chat:
            chat = cls()

        command_set = CommandSetBase(chat, chat)
        chat.add_command_set(command_set)

        cls.install_commands(command_set)

        return chat
    
    @property
    def prefix_length(self) -> int:
        return len(self.command_set.prefix or "")

    @property
    def tree(self) -> dict:
        return self.command_set.tree
    
    def remove_prefix(self, text: str):
        return text[self.prefix_length:]

    def add_command_set(self, command_set) -> Iterable:
        self.command_set = command_set
        self.prefix = command_set.prefix

    def is_command(self, message: str) -> bool:
        return self.command_set and self.command_set.is_command(message)

    def call_if_command(self, message: str) -> bool:
        if self.is_command(message):
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
        
    def on_message(self, message: str) -> str:
        # Adapter method --> should format the message
        return message

    def receive_message(self, message: str):  # Should be called on message sent by user
        message = self.on_message(message)
        was_called: bool = True

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


class CommandSetBase:  # Intermediate between the chat and the commands (set prefix to None to create subcommands'
    prefix: str | None = "/"

    def __init__(self, chat: Type[ChatBase], parent):
        self.commands = {}
        self.chat = chat
        self.parent = parent

    @classmethod
    def is_command(cls, message: str):
        return cls.prefix is None or message.startswith(cls.prefix)

    @property
    def tree(self):
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
        if command_name and not command_name in self.commands:
            raise UserMistake(f"This command does not exist : {command_name}")
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
    help_message: str = "No help available for this command."

    def __init__(self, command_set: Type[CommandSetBase]):
        self.command_set = command_set
        self.chat = command_set.chat

        if not hasattr(self, "name"):
            raise NotImplementedError("This command has no name or is the parent class")

    def __call__(self, argument: str):
        if argument.strip(" ") == "help":
            self.chat.send_message(self.help)
            return
        raise NotImplementedError(
            "You should override this method"
        )

    @property
    def tree(self):
        return set()

    @property
    def help(self):
        return self.generate_help()

    @property
    def full_name(self) -> str:
        path = []
        node = self
        
        while node is not self.chat:
           path.append(node.name)
           node = node.command_set.parent
           
        return self.chat.prefix+" ".join(path[::-1])
    
    def generate_help(self):
        message = f"{self.full_name}: {self.help_message}"
        tree = self.tree.copy()
        
        if not tree:
            return message
        
        message += "\n\nAvailable subcommands :\n- " + "\n- ".join(tree) + "\n"
        
        return message
    
    def add(self):
        self.command_set.add_command(self)

    def load(self):
        load_message = f"Loading {self.name}..."
        self.chat.send_message(load_message)  # Do some stuff... (sends a message on loading)


class CommandGroupBase(CommandBase, CommandManager):
    # A builtin command to handle subcommands (inherit and override the create_commands method' to create command
    # groups)
    name: str

    def __init__(self, command_set: Type[CommandSetBase]):
        super().__init__(command_set)
        self.sub_command_set = SubCommandSetBase(self.chat, self)
        
    @staticmethod
    def create_commands():
        return super().create_commands()

    @property
    def tree(self):
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
    
    print("================= TEST MODE =================\n")
    
    class TextChat(ChatBase):
        @staticmethod
        def create_commands():
            return set()
        
        def send_message(self, message):
            print(message)
        
        def clear(self):
            print("\033c\033[3J", end='')
        
        def log_user_mistake(self, error):
            self.send_message(f"\033[91m{error}\033[0m")
         
        def log_error(self, error):
            # Some logging stuff...
            self.send_message("\033[91mAn unexpected error has occured\033[0m")
    
    
    # Commands
    
    class Echo(CommandBase):
        name = "echo"
    
        def __call__(self, argument: str):  # When command is called by the user
            self.chat.send_message(argument)
    
    
    class Clear(CommandBase):
        name = "clear"
        help_message = """Clears the chat (returns an error if there is nothing to clear)."""
    
        def __call__(self, argument: str):  # When command is called by the user
            self.chat.clear()
    
    
    class GodMode(CommandBase):
        name = "godmode"
    
        def __call__(self, argument: str):  # When command is called by the user
            self.chat.send_message("God mode activated")
    
    class MockError(CommandBase):
        name = "error"
        
        def __call__(self, argument: str):
            self.chat.send_message(1/0)
    
    class MockFullName(CommandBase):
        name = "fullname"
        
        def __call__(self, argument: str):
            self.chat.send_message(self.full_name)
    
    
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
    
    class MockCommands(CommandGroupBase): 
        name = "mock"
    
        @staticmethod
        def create_commands():
            return {
                MockError,
                MockFullName,
            }
    
    
    # Chats
    
    class MyChat(TextChat):
        @staticmethod
        def create_commands():
            return {
                ChatCommands,
                GameCommands,
                MockCommands,
            }
    
    
    # main
    
    mychat = MyChat.create_chat()
    
    mock_messages = (
        "basic test message",
        "/chat echo this is a test for echo",
        "/chat",
        "/I_Dont_Exist",
        "/mock error",
        "/mock fullname"
    )
    
    print("\n\n----- Starting Tests ----\n")
    for message in mock_messages:
        print("$", message)
        mychat.receive_message(message)
    print("\n----- Ending Tests -----\n\n")
    
    while True:
        mychat.receive_message(input('$ '))


if __name__ == "__main__":
        test()
