import pygame

from src.config.game_data import GameData
from src.entities.entity_manager import EntityManager
from src.entities.player import Player
from src.guis.gui import InventoryUI
from src.map.camera import Camera
from src.map.map_render import MapRender
from src.map.mini_map import MiniMap
from src.map.tile_map import NoiseTileMapGenerator


class Level:
    def __init__(self, game, clock) -> None:
        self.tile_images = []
        self.game = game
        self.clock = clock
        self.config = GameData()
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = Camera()

        self.tile_map_generator = NoiseTileMapGenerator(self)
        self.tiles_map = self.tile_map_generator.generate_tiles_map(
            0,
            0,
            self.config.map_size,
            self.config.map_size)
        self.map_render = MapRender(self)
        self.map_render.load_tile_images()

        # Player creation
        self.player = Player(group=self.all_sprites, pos=(-6, -16))
        self.inventory_ui = InventoryUI(self.player.inventory)

        # EntityManager initialization
        self.entity_manager = EntityManager(self.config, self.player, self.all_sprites, self.tile_map_generator)

        self.mini_map = MiniMap(tiles_map=self.tiles_map,
                                mini_map_size=20,
                                display_surface=self.display_surface,
                                visible_area_size=20)
        self.uis = [self.inventory_ui]

    def draw(self) -> None:
        self.map_render.draw_map()
        self.all_sprites.shifted_draw(self.player)
        if self.config.show_player_inventory:
            for ui in self.uis:
                ui.draw()

    def update(self, dt) -> None:
        self.entity_manager.update(dt)

    def handle_events(self, event) -> None:
        if self.config.show_player_inventory:
            for ui in self.uis:
                ui.handle_events(event)

    def teleport_player(self, pos) -> None:
        x, y = pos
        pixel_x, pixel_y = x * self.config.tile_size, y * self.config.tile_size
        self.player.pos = pygame.Vector2(pixel_x, pixel_y)
