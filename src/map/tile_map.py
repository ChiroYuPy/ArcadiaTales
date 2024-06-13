import random

from perlin_noise import PerlinNoise
from pygame import Vector2

from src.config.game_data import GameData

config = GameData()


class Tile:
    def __init__(self, tile_id, x, y, variant=1):
        self.tile_id = tile_id
        self.variant = variant
        self.pos = Vector2(x, y)


class NoiseTileMapGenerator:
    def __init__(self, game):
        self.game = game
        self.config = GameData()
        self.tiles_map = {}

        self.seed = -1
        self.octaves = 4
        self.scale = 50

        random.seed(self.seed)
        self.noise = PerlinNoise(octaves=4, seed=-1)

    def generate_tile(self, x, y):
        noise_value = self.noise([x / self.scale, y / self.scale])
        if noise_value > 0:
            tile = Tile(1, x, y, int(random.randint(1, 3)))
        else:
            tile = Tile(2, x, y)
        return tile

    def generate_tiles_map(self, origin_x, origin_y, w, h):
        self.tiles_map = {}
        if not self.tiles_map:
            for y in range(int(origin_y - h / 2), int(origin_y + h / 2)):
                for x in range(int(origin_x - w / 2), int(origin_x + w / 2)):
                    if x == int(origin_x - w / 2) or x == int(origin_x + w / 2) - 1 or y == int(
                            origin_y - h / 2) or y == int(origin_y + h / 2) - 1:
                        tile = Tile(0, x, y)
                    else:
                        tile = self.generate_tile(x, y)
                    self.tiles_map[(x, y)] = tile

        return self.tiles_map

    def get_visible_tiles(self):
        player_tile_pos = self.get_tile_position(self.game.player.pos)
        visible_tiles_x = self.config.window_width // self.config.tile_size + 2
        visible_tiles_y = self.config.window_height // self.config.tile_size + 3
        start_x = int(player_tile_pos.x - visible_tiles_x / 2)
        start_y = int(player_tile_pos.y - visible_tiles_y / 2)
        visible_tiles = []
        for y in range(start_y, start_y + visible_tiles_y):
            for x in range(start_x, start_x + visible_tiles_x):
                if (x, y) in self.tiles_map:
                    visible_tiles.append(self.tiles_map[(x, y)])
        return visible_tiles

    def get_tile_position(self, pixel_position):
        tile_x = pixel_position[0] // self.config.tile_size
        tile_y = pixel_position[1] // self.config.tile_size
        return Vector2(tile_x, tile_y)
