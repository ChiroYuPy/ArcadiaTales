import pygame

from gamedata import GameData
from src.entities.player import Player
from src.map.camera import Camera
from src.map.tilemap import NoiseTileMapGenerator


class Level:
    def __init__(self, game, clock):
        self.game = game
        self.clock = clock
        self.config = GameData()
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = Camera()

        self.player = Player(group=self.all_sprites, pos=(1, 0))

        self.tile_map_generator = NoiseTileMapGenerator()

        self.tile_images = {
            1: pygame.image.load("assets/images/tiles/floor_center_2.png").convert_alpha(),
            2: pygame.image.load("assets/images/tiles/ground.png").convert_alpha(),
            3: pygame.image.load("assets/images/tiles/wall_up_0.png").convert_alpha(),
            4: pygame.image.load("assets/images/tiles/wall_down_0.png").convert_alpha()
        }
        for key, image in self.tile_images.items():
            self.tile_images[key] = pygame.transform.scale(image, (
                image.get_width() * self.config.tile_scale, image.get_height() * self.config.tile_scale))

    def draw_map(self):
        tile_map = self.tile_map_generator.generate_tiles_map(
            self.player.pos.x // self.config.tile_size,
            self.player.pos.y // self.config.tile_size,
            int(self.config.window_width / self.config.tile_size) // 2 + 2,
            int(self.config.window_height / self.config.tile_size) // 2 + 2)

        for (x, y), tile in tile_map.items():
            tile_id = tile.tile_id

            if tile_id in self.tile_images:
                tile_image = self.tile_images[tile_id]
                tile_x = (x * self.config.tile_size + self.config.tile_size / 2) - self.player.pos.x + self.config.window_width // 2
                tile_y = (y * self.config.tile_size + self.config.tile_size / 2) - self.player.pos.y + self.config.window_height // 2
                self.display_surface.blit(tile_image, (tile_x, tile_y))
            else:
                pygame.draw.rect(self.display_surface, (255, 127, 160),
                                 (x * self.config.tile_size, y * self.config.tile_size, self.config.tile_size,
                                  self.config.tile_size))

    def draw(self):
        self.draw_map()
        self.all_sprites.customize_draw(self.player)

    def update(self, dt):
        self.player.update(dt)
