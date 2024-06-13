class GameData:
    """Singleton class for game data."""

    _instance = None  # Singleton instance

    window_width: int = 1280  # Width of the game window
    window_height: int = 720  # Height of the game window
    window_frame: bool = True  # Whether to display window frame
    window_resizable: bool = True  # Whether the window is resizable
    window_caption: str = "ArcadiaTales"  # Caption for the game window
    game_version: str = "0.1.2"  # Version of the game
    max_fps: int = 600  # Maximum frames per second
    debug_level: int = 0  # Debug level
    # ( 0 = False, 1 = infos, 2 = sprite_collide_rects, 3 = tile_collide_rects, 4 = all)

    tile_scale: int = 4  # Scale of the tiles
    tile_image_size: int = 16  # Size of the tile images
    tile_size: int = tile_image_size * tile_scale  # Size of the tiles

    map_size = 50

    show_player_inventory: bool = False  # Whether to show the player's inventory
    player_speed: int = 100  # Speed of the player
    player_name: str = "&eChiroYuki"  # Name of the player
    player_health: int = 100  # Health of the player
    player_max_health: int = 100  # Maximum health of the player
    player_attack_damage: int = 10  # Attack damage of the player
    player_inventory_slot_width: int = 8  # Width of the player's inventory
    player_inventory_slot_height: int = 10  # Height of the player's inventory
    player_inventory_slot_size: int = 32  # Size of the player's inventory slots
    player_inventory_slot_spacing: int = 2  # Spacing between player's inventory slots
    player_inventory_slot_image: str = "assets/images/gui/slot.png"  # Image for player's inventory slots
    player_inventory_slot_scale: float = 2  # Scale of the player's inventory slots

    slime_speed: int = 60  # Speed of the slime enemy
    slime_health: int = 20  # Health of the slime enemy
    slime_max_health: int = 20  # Maximum health of the slime enemy
    slime_attack_damage: int = 5  # Attack damage of the slime enemy
    slime_spawn_rate: int = 5  # Rate at which slimes spawn
    slime_spawn_max: int = 10  # Maximum number of slimes to spawn

    class Chat:
        """Nested class for chat configuration."""

        chat_open: bool = False  # Whether the chat is open
        command_prefix: str = "/"  # Prefix for commands
        max_lines_characters: int = 80  # Maximum number of characters per line
        max_input_characters: int = 100  # Maximum number of characters in the input field
        width: int = 600  # Width of the chat window
        font_size: int = 24  # Font size for chat messages
        max_messages: int = 100  # Maximum number of messages to store
        max_shown_messages: int = 20  # Maximum number of messages to display at once

    def __new__(cls, *args, **kwargs):
        """Override __new__ to implement Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
