import pygame
from pyqtree import Index
from src.config.gamedata import GameData
from src.entities.enemies.slime import Slime
from src.entities.player import Player
from src.map.camera import Camera
from src.map.tilemap import NoiseTileMapGenerator
from src.utils.utils import Direction


class Level:
    def __init__(self, game, clock) -> None:
        self.game = game
        self.clock = clock
        self.config = GameData()
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = Camera()
        self.player = Player(group=self.all_sprites, pos=(0, 0))
        self.enemies = [Slime(group=self.all_sprites, pos=(x * 2, 0)) for x in range(10)]
        for slime in self.enemies:
            slime.target = self.player

        bbox = (0, 0, self.config.window_width, self.config.window_height)
        self.quadtree = Index(bbox=bbox)
        self.quadtree_items = set()

        self.player.rect = pygame.Rect(0, 0, 32, 32)
        self.quadtree.insert(item=self.player, bbox=self.player.rect)

        for enemy in self.enemies:
            self.quadtree.insert(item=enemy, bbox=(-2, -2, 2, 2))

        self.tile_map_generator = NoiseTileMapGenerator()
        self.load_tile_images()

    def load_tile_images(self) -> None:
        self.tile_images = {
            1: pygame.image.load("assets/images/tiles/floor_center_2.png").convert_alpha(),
            2: pygame.image.load("assets/images/tiles/ground.png").convert_alpha(),
            3: pygame.image.load("assets/images/tiles/wall_up_0.png").convert_alpha(),
            4: pygame.image.load("assets/images/tiles/wall_down_0.png").convert_alpha()
        }
        for key, image in self.tile_images.items():
            self.tile_images[key] = pygame.transform.scale(image, (
                image.get_width() * self.config.tile_scale, image.get_height() * self.config.tile_scale))

    def summon_entity(self, entity: str, pos: tuple[int, int]) -> bool:
        if entity == "slime":
            slime = Slime(group=self.all_sprites, pos=pos)
            slime.target = self.player
            self.enemies.append(slime)
            self.quadtree.insert(item=slime, bbox=slime.collide_rect)
            return True
        return False

    def teleport_player(self, pos) -> None:
        x, y = pos
        pixel_x, pixel_y = x * self.config.tile_size, y * self.config.tile_size
        self.player.pos = pygame.Vector2(pixel_x, pixel_y)

    def draw_map(self) -> None:
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
                if self.config.debug_level == 3 or self.config.debug_level == 4:
                    pygame.draw.rect(self.display_surface, (255, 0, 0),
                                     (tile_x,
                                      tile_y,
                                      self.config.tile_size,
                                      self.config.tile_size), 1)
            else:
                pygame.draw.rect(self.display_surface, (255, 127, 160),
                                 (x * self.config.tile_size, y * self.config.tile_size, self.config.tile_size,
                                  self.config.tile_size))

    def draw(self) -> None:
        self.draw_map()
        self.all_sprites.shifted_draw(self.player)

    def update(self, dt) -> None:
        self.player.update(dt)
        self.check_tile_collision(self.player)
        for enemy in self.enemies:
            enemy.update(dt)

        self.check_collision(self.player)
        for enemy in self.enemies:
            self.check_collision(enemy)

    def check_tile_collision(self, entity):
        entity_rect = entity.collide_rect
        for (x, y), tile in self.tile_map_generator.tiles_map.items():
            if tile.tile_id == 2:
                tile_rect = pygame.Rect(x * self.config.tile_size + 16,
                                        y * self.config.tile_size + 16,
                                        self.config.tile_size,
                                        self.config.tile_size)
                if entity_rect.colliderect(tile_rect):
                    direction = self.get_collision_direction(entity_rect, tile_rect)
                    entity.collide_with(tile_rect, direction)

    def get_collision_direction(self, entity_rect, tile_rect):
        dx_center = entity_rect.centerx - tile_rect.centerx
        dy_center = entity_rect.centery - tile_rect.centery
        if abs(dx_center) > abs(dy_center):
            return Direction.RIGHT if dx_center > 0 else Direction.LEFT
        return Direction.DOWN if dy_center > 0 else Direction.UP

    def check_collision(self, entity) -> None:
        entity_collisions = self.quadtree.intersect(entity.collide_rect)
        for other_entity in entity_collisions:
            if other_entity != entity and entity.collide_rect.colliderect(other_entity.collide_rect):
                self.handle_collision(entity, other_entity)

    def handle_collision(self, entity1, entity2) -> None:
        if isinstance(entity1, Player) and isinstance(entity2, Slime):
            self.remove_entity(entity2)
        elif isinstance(entity2, Player) and isinstance(entity1, Slime):
            self.remove_entity(entity1)
        elif isinstance(entity1, Slime) and isinstance(entity2, Slime):
            # Calculate distance between centers
            dx = entity1.pos.x - entity2.pos.x
            dy = entity1.pos.y - entity2.pos.y
            distance_squared = dx * dx + dy * dy
            min_distance_squared = (entity1.width / 2 + entity2.width / 2) ** 2

            if distance_squared < min_distance_squared:
                distance = distance_squared ** 0.5
                overlap = (entity1.width / 2 + entity2.width / 2) - distance
                if overlap > 0:
                    overlap_dx = (dx / distance) * overlap
                    overlap_dy = (dy / distance) * overlap
                    entity1.pos.x += overlap_dx
                    entity1.pos.y += overlap_dy
                    entity2.pos.x -= overlap_dx
                    entity2.pos.y -= overlap_dy

    def add_entity(self, entity) -> None:
        self.quadtree.insert(item=entity, bbox=entity.collide_rect)
        self.quadtree_items.add(entity)

    def remove_entity(self, entity) -> None:
        if entity in self.enemies:
            self.enemies.remove(entity)
        if entity in self.quadtree_items:
            self.quadtree.remove(item=entity, bbox=entity.collide_rect)
            self.quadtree_items.remove(entity)
        if entity in self.all_sprites:
            self.all_sprites.remove(entity)
