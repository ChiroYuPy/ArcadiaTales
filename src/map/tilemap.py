from perlin_noise import PerlinNoise


class Tile:
    def __init__(self, tile_id, variant):
        self.tile_id = tile_id
        self.variant = variant


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
            tile = Tile(1, 1)
        else:
            tile = Tile(2, 1)

        self.generated_tiles[(x, y)] = tile
        return tile

    def generate_tiles_map(self, origin_x, origin_y, w, h):
        self.tiles_map = {}

        for y in range(int(origin_y - h), int(origin_y + h)):
            for x in range(int(origin_x - w), int(origin_x + w)):
                tile = self.generate_tile(x, y)
                self.tiles_map[(x, y)] = tile

        return self.tiles_map
