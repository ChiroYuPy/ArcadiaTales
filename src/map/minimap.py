import pygame

from src.utils.colors import Color


class MiniMap:
    def __init__(self, tiles_map, mini_map_size, display_surface, visible_area_size):
        self.tiles_map = tiles_map
        self.mini_map_size = mini_map_size
        self.display_surface = display_surface
        self.visible_area_size = visible_area_size
        self.colors = {
            0: Color.WHITE,
            1: Color.DARK_RED,
            2: Color.DARK_BLUE
        }

    def draw(self, player_position):
        mini_map_surface = pygame.Surface(self.mini_map_size)
        for (x, y), tile in self.tiles_map.items():
            rect = pygame.Rect(x * self.mini_map_size[0] / len(self.tiles_map),
                               y * self.mini_map_size[1] / len(self.tiles_map),
                               self.mini_map_size[0] / len(self.tiles_map),
                               self.mini_map_size[1] / len(self.tiles_map))
            pygame.draw.rect(mini_map_surface, self.colors[tile.tile_id], rect)

        visible_area_rect = pygame.Rect(player_position.x * self.mini_map_size[0] / len(self.tiles_map),
                                        player_position.y * self.mini_map_size[1] / len(self.tiles_map),
                                        self.visible_area_size[0] * self.mini_map_size[0] / len(self.tiles_map),
                                        self.visible_area_size[1] * self.mini_map_size[1] / len(self.tiles_map))
        pygame.draw.rect(mini_map_surface, (255, 0, 0), visible_area_rect, 2)

        self.display_surface.blit(mini_map_surface, (0, 0))