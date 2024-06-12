import yaml


class GameData:
    """Singleton class for game data."""

    _instance = None  # Singleton instance

    window_width: int = 1280  # Width of the game window
    window_height: int = 720  # Height of the game window
    window_frame: bool = True  # Whether to display window frame
    window_resizable: bool = True  # Whether the window is resizable
    window_caption: str = "ArcadiaTales"  # Caption for the game window
    game_version: str = "0.1.1"  # Version of the game
    max_fps: int = 165  # Maximum frames per second
    debug_level: int = 0  # Debug level
    # ( 0 = False, 1 = infos, 2 = sprite_collide_rects, 3 = tile_collide_rects, 4 = all)

    tile_scale: int = 2  # Scale of the tiles
    tile_image_size: int = 16  # Size of the tile images
    tile_size: int = tile_image_size * tile_scale  # Size of the tiles

    player_speed: int = 100  # Speed of the player
    slime_speed: int = 50  # Speed of the slime enemy

    class Chat:
        """Nested class for chat configuration."""

        chat_open: bool = False  # Whether the chat is open
        command_prefix: str = "/"  # Prefix for commands
        max_lines_characters: int = 80  # Maximum number of characters per line
        max_input_characters: int = 100  # Maximum number of characters in the input field
        width: int = 600  # Width of the chat window
        font_size: int = 16  # Font size for chat messages
        max_messages: int = 100  # Maximum number of messages to store
        max_shown_messages: int = 20  # Maximum number of messages to display at once

    def __new__(cls, *args, **kwargs):
        """Override __new__ to implement Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def to_dict(self):
        """Convert the configuration to a dictionary."""
        return {
            'window_width': self.window_width,
            'window_height': self.window_height,
            'window_frame': self.window_frame,
            'window_resizable': self.window_resizable,
            'window_caption': self.window_caption,
            'game_version': self.game_version,
            'max_fps': self.max_fps,
            'debug_level': self.debug_level,
            'tile_scale': self.tile_scale,
            'tile_image_size': self.tile_image_size,
            'tile_size': self.tile_size,
            'player_speed': self.player_speed,
            'slime_speed': self.slime_speed,
            'chat': {
                'chat_open': self.Chat.chat_open,
                'command_prefix': self.Chat.command_prefix,
                'max_lines_characters': self.Chat.max_lines_characters,
                'max_input_characters': self.Chat.max_input_characters,
                'width': self.Chat.width,
                'font_size': self.Chat.font_size,
                'max_messages': self.Chat.max_messages,
                'max_shown_messages': self.Chat.max_shown_messages,
            }
        }

    def from_dict(self, config_dict):
        """Load the configuration from a dictionary."""
        self.window_width = config_dict.get('window_width', self.window_width)
        self.window_height = config_dict.get('window_height', self.window_height)
        self.window_frame = config_dict.get('window_frame', self.window_frame)
        self.window_resizable = config_dict.get('window_resizable', self.window_resizable)
        self.window_caption = config_dict.get('window_caption', self.window_caption)
        self.game_version = config_dict.get('game_version', self.game_version)
        self.max_fps = config_dict.get('max_fps', self.max_fps)
        self.debug_level = config_dict.get('debug_level', self.debug_level)
        self.tile_scale = config_dict.get('tile_scale', self.tile_scale)
        self.tile_image_size = config_dict.get('tile_image_size', self.tile_image_size)
        self.tile_size = config_dict.get('tile_size', self.tile_size)
        self.player_speed = config_dict.get('player_speed', self.player_speed)
        self.slime_speed = config_dict.get('slime_speed', self.slime_speed)
        chat_config = config_dict.get('chat', {})
        self.Chat.chat_open = chat_config.get('chat_open', self.Chat.chat_open)
        self.Chat.command_prefix = chat_config.get('command_prefix', self.Chat.command_prefix)
        self.Chat.max_lines_characters = chat_config.get('max_lines_characters', self.Chat.max_lines_characters)
        self.Chat.max_input_characters = chat_config.get('max_input_characters', self.Chat.max_input_characters)
        self.Chat.width = chat_config.get('width', self.Chat.width)
        self.Chat.font_size = chat_config.get('font_size', self.Chat.font_size)
        self.Chat.max_messages = chat_config.get('max_messages', self.Chat.max_messages)
        self.Chat.max_shown_messages = chat_config.get('max_shown_messages', self.Chat.max_shown_messages)

    def save_config(self, filename='config.yml'):
        """Save the configuration to the config YAML file."""
        with open(filename, 'w') as f:
            yaml.dump(self.to_dict(), f)

    def load_config(self, filename='config.yml'):
        """Load the configuration from the config YAML file."""
        try:
            with open(filename, 'r') as f:
                config_dict = yaml.safe_load(f)
                self.from_dict(config_dict)
        except FileNotFoundError:
            print(f"No config file found. Using default settings.")
