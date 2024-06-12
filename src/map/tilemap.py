from perlin_noise import PerlinNoise
from pygame import Vector2, Rect

from src.config.gamedata import GameData

config = GameData()


class Tile:
    def __init__(self, tile_id, x, y, variant=1):
        self.tile_id = tile_id
        self.variant = variant
        self.pos = Vector2(x, y)


class NoiseTileMapGenerator:
    def __init__(self):
        self.generated_tiles = {}
        self.tiles_map = {}

        self.seed = 0
        self.octaves = 4
        self.scale = 50

        self.noise = PerlinNoise(octaves=4, seed=-1)

    def generate_tile(self, x, y):
        if (x, y) in self.generated_tiles:
            return self.generated_tiles[(x, y)]

        noise_value = self.noise([x / self.scale, y / self.scale])
        if noise_value > 0:
            tile = Tile(1, x, y)
        else:
            tile = Tile(2, x, y)

        self.generated_tiles[(x, y)] = tile
        return tile

    def generate_tiles_map(self, origin_x, origin_y, w, h):
        self.tiles_map = {}

        if not self.tiles_map:
            for y in range(int(origin_y - h), int(origin_y + h)):
                for x in range(int(origin_x - w), int(origin_x + w)):
                    tile = self.generate_tile(x, y)
                    self.tiles_map[(x, y)] = tile

        return self.tiles_map
