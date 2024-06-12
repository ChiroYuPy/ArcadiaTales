class GameData:
    """Singleton class for game data."""

    _instance = None  # Singleton instance

    window_width: int = 1280  # Width of the game window
    window_height: int = 720  # Height of the game window
    window_frame: bool = True  # Whether to display window frame
    window_resizable: bool = True  # Whether the window is resizable
    window_caption: str = "ChatSystem"  # Caption for the game window
    game_version: str = "0.1.0"  # Version of the game
    max_fps: int = 165  # Maximum frames per second
    debug: bool = False  # Whether to display debug information

    tile_scale: int = 2  # Scale of the tiles
    tile_image_size = 16  # Size of the tile images
    tile_size = tile_image_size * tile_scale  # Size of the tiles

    player_speed = 200  # Speed of the player
    slime_speed = 50  # Speed of the slime enemy

    class Chat:
        """Nested class for chat configuration."""

        chat_open = False  # Whether the chat is open
        command_prefix = "/"  # Prefix for commands
        max_lines_characters = 80  # Maximum number of characters per line
        max_input_characters = 100  # Maximum number of characters in the input field
        width: int = 600  # Width of the chat window
        font_size: int = 20  # Font size for chat messages
        max_messages: int = 100  # Maximum number of messages to store
        max_shown_messages: int = 20  # Maximum number of messages to display at once

    def __new__(cls, *args, **kwargs):
        """Override __new__ to implement Singleton pattern."""

        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
