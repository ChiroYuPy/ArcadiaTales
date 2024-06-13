import random
import pygame
from pyqtree import Index
from src.entities.enemies.slime import Slime
from src.entities.player import Player
from src.utils.utils import Direction

class EntityManager:
    def __init__(self, config, player, all_sprites, tile_map_generator) -> None:
        self.config = config
        self.player = player
        self.all_sprites = all_sprites
        self.tile_map_generator = tile_map_generator
        self.enemies = []

        bbox = (0, 0, self.config.window_width, self.config.window_height)
        self.quadtree = Index(bbox=bbox)
        self.quadtree_items = set()

        self.generate_random_slimes()

        # Insert player into QuadTree
        self.quadtree.insert(item=self.player, bbox=self.player.collide_rect)

        # Insert enemies into QuadTree
        for enemy in self.enemies:
            self.quadtree.insert(item=enemy, bbox=enemy.collide_rect)

    def generate_random_slimes(self) -> None:
        path_tiles = [pos for pos, tile in self.tile_map_generator.tiles_map.items() if tile.tile_id == 1]
        slime_count = 50
        slime_names = ["Slime", "Slimey", "Gooey", "Squishy", "Blobby", "Jelly", "Squidgy", "Sloppy", "Sloshy"]
        color = "&c"

        for i in range(slime_count):
            pos = random.choice(path_tiles)
            slime = Slime(group=self.all_sprites, pos=pos)
            slime.target = self.player
            slime.name = color + slime_names[i % len(slime_names)]
            self.enemies.append(slime)

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

    def check_tile_collision(self, entity):
        entity_tile_pos = self.get_tile_position(entity.pos)
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                x, y = entity_tile_pos.x + dx, entity_tile_pos.y + dy
                if (x, y) in self.tile_map_generator.tiles_map:
                    tile = self.tile_map_generator.tiles_map[(x, y)]
                    if tile.tile_id == 2 or tile.tile_id == 0:
                        tile_rect = pygame.Rect(x * self.config.tile_size + self.config.tile_size / 2,
                                                y * self.config.tile_size + self.config.tile_size / 2,
                                                self.config.tile_size,
                                                self.config.tile_size)
                        if entity.collide_rect.colliderect(tile_rect):
                            direction = self.get_collision_direction(entity.collide_rect, tile_rect)
                            entity.collide_with(tile_rect, direction)

    @staticmethod
    def get_collision_direction(entity_rect, tile_rect):
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
            # Handle collision between player and slime
            pass
        elif isinstance(entity2, Player) and isinstance(entity1, Slime):
            # Handle collision between player and slime
            pass
        elif isinstance(entity1, Slime) and isinstance(entity2, Slime):
            dx = entity1.pos.x - entity2.pos.x
            dy = entity1.pos.y - entity2.pos.y
            distance_squared = dx * dx + dy * dy
            min_distance_squared = (entity1.width / 2 + entity2.width / 2) ** 2

            if distance_squared < min_distance_squared:
                distance = distance_squared ** 0.5
                if distance != 0:
                    overlap = (entity1.width / 2 + entity2.width / 2) - distance
                    if overlap > 0:
                        overlap_dx = (dx / distance) * overlap
                        overlap_dy = (dy / distance) * overlap
                        entity1.pos.x += overlap_dx
                        entity1.pos.y += overlap_dy
                        entity2.pos.x -= overlap_dx
                        entity2.pos.y -= overlap_dy

    def spawn_entity(self, entity: str, pos: tuple[int, int]) -> bool:
        if entity == "slime":
            entity = Slime(group=self.all_sprites, pos=pos)
            entity.target = self.player
            self.enemies.append(entity)
            self.quadtree.insert(item=entity, bbox=entity.collide_rect)
            return True
        return False

    def get_tile_position(self, pixel_position):
        tile_x = pixel_position[0] // self.config.tile_size
        tile_y = pixel_position[1] // self.config.tile_size
        return pygame.Vector2(tile_x, tile_y)

    def update(self, dt) -> None:
        self.player.update(dt)
        self.check_tile_collision(self.player)
        self.check_collision(self.player)
        for enemy in self.enemies:
            enemy.update(dt)
            self.check_tile_collision(enemy)
            self.check_collision(enemy)
