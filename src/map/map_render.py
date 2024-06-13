import pygame

from src.config.game_data import GameData
from src.utils.colors import Color


class MapRender:
    def __init__(self, level):
        self.tile_images = None
        self.config = GameData()
        self.level = level
    
    def load_tile_images(self) -> None:
        self.tile_images = {
            0: pygame.image.load("assets/images/tiles/wall_up_0.png").convert_alpha(),
            1: pygame.image.load("assets/images/tiles/floor_center_2.png").convert_alpha(),
            2: pygame.image.load("assets/images/tiles/ground.png").convert_alpha(),
        }
        for key, image in self.tile_images.items():
            self.tile_images[key] = pygame.transform.scale(image, (
                image.get_width() * self.config.tile_scale, image.get_height() * self.config.tile_scale))

    def draw_map(self) -> None:
        visible_tiles = self.level.tile_map_generator.get_visible_tiles()
        for tile in visible_tiles:
            tile_id = tile.tile_id
            if tile_id in self.tile_images:
                tile_image = self.tile_images[tile_id]
                tile_x = ((tile.pos.x * self.config.tile_size + self.config.tile_size / 2)
                          - self.level.player.pos.x + self.config.window_width // 2)
                tile_y = ((tile.pos.y * self.config.tile_size + self.config.tile_size / 2)
                          - self.level.player.pos.y + self.config.window_height // 2)
                self.level.display_surface.blit(tile_image, (tile_x, tile_y))
                if self.config.debug_level == 3 or self.config.debug_level == 4:
                    pygame.draw.rect(self.level.display_surface, Color.DARK_BLUE,
                                     (tile_x,
                                      tile_y,
                                      self.config.tile_size,
                                      self.config.tile_size), 1)
            else:
                pygame.draw.rect(self.level.display_surface, Color.WHITE,
                                 (tile.pos.x * self.config.tile_size, tile.pos.y * self.config.tile_size,
                                  self.config.tile_size,
                                  self.config.tile_size))
                