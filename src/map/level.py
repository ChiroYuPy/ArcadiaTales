import math

import pygame
from pygame import Vector2
from pyqtree import Index
from src.config.game_data import GameData
from src.entities.enemies.slime import Slime
from src.entities.player import Player
from src.guis.graphical_user_interface import InventoryUI
from src.map.camera import Camera
from src.map.mini_map import MiniMap
from src.map.tile_map import NoiseTileMapGenerator
from src.utils.colors import Color
from src.utils.utils import Direction


class Level:
    def __init__(self, game, clock) -> None:
        self.tile_images = []
        self.game = game
        self.clock = clock
        self.config = GameData()
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = Camera()
        self.player = Player(group=self.all_sprites, pos=(-6, -16))
        self.inventory_ui = InventoryUI(self.player.inventory)
        self.uis = [self.inventory_ui]
        self.enemies = []
        names = ("Gertrude", "Gerald", "Geraldine", "Geraldina", "Geraldino", "Geraldinio")
        color = "&c"
        for i in range(12):
            angle = 2 * math.pi * i / 12
            x = -6 + 4 * math.cos(angle)
            y = -16 + 4 * math.sin(angle)
            slime = Slime(group=self.all_sprites, pos=(x, y))
            slime.target = self.player
            slime.name = color + names[i % len(names)]
            self.enemies.append(slime)

        bbox = (0, 0, self.config.window_width, self.config.window_height)
        self.quadtree = Index(bbox=bbox)
        self.quadtree_items = set()

        self.quadtree.insert(item=self.player, bbox=self.player.collide_rect)

        for enemy in self.enemies:
            self.quadtree.insert(item=enemy, bbox=enemy.collide_rect)

        self.tile_map_generator = NoiseTileMapGenerator(self)
        self.tiles_map = self.tile_map_generator.generate_tiles_map(
            0,
            0,
            self.config.map_size,
            self.config.map_size)
        self.load_tile_images()

        self.mini_map = MiniMap(tiles_map=self.tiles_map,
                                mini_map_size=20,
                                display_surface=self.display_surface,
                                visible_area_size=20)

    def load_tile_images(self) -> None:
        self.tile_images = {
            0: pygame.image.load("assets/images/tiles/wall_up_0.png").convert_alpha(),
            1: pygame.image.load("assets/images/tiles/floor_center_2.png").convert_alpha(),
            2: pygame.image.load("assets/images/tiles/ground.png").convert_alpha(),
        }
        for key, image in self.tile_images.items():
            self.tile_images[key] = pygame.transform.scale(image, (
                image.get_width() * self.config.tile_scale, image.get_height() * self.config.tile_scale))

    def spawn_entity(self, entity: str, pos: tuple[int, int]) -> bool:
        if entity == "slime":
            entity = Slime(group=self.all_sprites, pos=pos)
            entity.target = self.player
            self.enemies.append(entity)
            self.quadtree.insert(item=entity, bbox=entity.collide_rect)
            return True
        return False

    def teleport_player(self, pos) -> None:
        x, y = pos
        pixel_x, pixel_y = x * self.config.tile_size, y * self.config.tile_size
        self.player.pos = pygame.Vector2(pixel_x, pixel_y)

    def draw_map(self) -> None:
        visible_tiles = self.tile_map_generator.get_visible_tiles()
        for tile in visible_tiles:
            tile_id = tile.tile_id
            if tile_id in self.tile_images:
                tile_image = self.tile_images[tile_id]
                tile_x = ((tile.pos.x * self.config.tile_size + self.config.tile_size / 2)
                          - self.player.pos.x + self.config.window_width // 2)
                tile_y = ((tile.pos.y * self.config.tile_size + self.config.tile_size / 2)
                          - self.player.pos.y + self.config.window_height // 2)
                self.display_surface.blit(tile_image, (tile_x, tile_y))
                if self.config.debug_level == 3 or self.config.debug_level == 4:
                    pygame.draw.rect(self.display_surface, Color.DARK_BLUE,
                                     (tile_x,
                                      tile_y,
                                      self.config.tile_size,
                                      self.config.tile_size), 1)
            else:
                pygame.draw.rect(self.display_surface, Color.WHITE,
                                 (tile.pos.x * self.config.tile_size, tile.pos.y * self.config.tile_size,
                                  self.config.tile_size,
                                  self.config.tile_size))

    def draw(self) -> None:
        self.draw_map()
        self.all_sprites.shifted_draw(self.player)
        if self.config.show_player_inventory:
            for ui in self.uis:
                ui.draw()
        # self.mini_map.draw()

    def update(self, dt) -> None:
        self.player.update(dt)
        self.check_tile_collision(self.player)
        self.check_collision(self.player)
        for enemy in self.enemies:
            enemy.update(dt)
            self.check_tile_collision(enemy)
            self.check_collision(enemy)

    def handle_events(self, event) -> None:
        if self.config.show_player_inventory:
            for ui in self.uis:
                ui.handle_events(event)

    def get_tile_position(self, pixel_position):
        tile_x = pixel_position[0] // self.config.tile_size
        tile_y = pixel_position[1] // self.config.tile_size
        return Vector2(tile_x, tile_y)

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
            # self.remove_entity(entity2)
            pass
        elif isinstance(entity2, Player) and isinstance(entity1, Slime):
            # self.remove_entity(entity1)
            pass
        elif isinstance(entity1, Slime) and isinstance(entity2, Slime):
            # Calculate distance between centers
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
