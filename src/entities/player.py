import pygame
from pygame import Vector2
from pygame.key import get_pressed

from src.config.game_data import GameData
from src.entities.alive_entity import AliveEntity
from src.guis.inventory import Inventory


class Player(AliveEntity):
    def __init__(self, group, pos):
        self.config = GameData()
        super().__init__(group=group,
                         pos=pos,
                         animations={'up_walk': [], 'down_walk': [], 'left_walk': [], 'right_walk': [],
                                     'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                                     'right_atk': [], 'left_atk': [], 'up_atk': [], 'down_atk': [],
                                     'fall': []},
                         image_offset=(0, - 10),
                         name_offset=(0, - 16))
        self.health_bar.offset.y = 12
        self.health_bar.width = 80
        self.health_bar.height = 10

        self.name = self.config.player_name
        self.assets_name = "player"
        self.current_skin = 1
        self.assets_folder = "player" + "/" + str(self.current_skin)
        self.animation_state = "idle"
        self.animation_direction = "down"
        self.speed = self.config.player_speed
        self.import_assets(scale=self.config.tile_scale)

        self.inventory = Inventory(self.config.player_inventory_slot_width,
                                   self.config.player_inventory_slot_height)
        self.inventory.add_item("amethyst_shard")
        self.inventory.add_item("apple")
        self.inventory.add_item("baked_potato")
        self.inventory.add_item("beef")
        self.inventory.add_item("beetroot")
        self.inventory.add_item("blaze_powder")
        self.inventory.add_item("bone_meal")
        self.inventory.add_item("bowl")
        self.inventory.add_item("bread")
        self.inventory.add_item("carrot")

    def input(self):
        keys = get_pressed()
        up = pygame.K_z
        down = pygame.K_s
        left = pygame.K_q
        right = pygame.K_d

        if not self.config.Chat.chat_open:
            self.direction = Vector2(keys[right] - keys[left], keys[down] - keys[up])
        else:
            self.direction = Vector2()

    def collide_with(self, tile_rect, direction):
        super().collide_with(tile_rect, direction)

    def update_animation_state(self):
        self.animation_direction = "right" if self.direction.x > 0 else \
            "left" if self.direction.x < 0 else \
                "down" if self.direction.y > 0 else \
                    "up" if self.direction.y < 0 else (
                        self.animation_direction)
        if self.direction.magnitude() == 0:
            self.animation_state = "idle"
            self.animation_speed = 4
        else:
            self.animation_state = "walk"
            self.animation_speed = 6
        self.current_animation = self.animation_direction + "_" + self.animation_state

    def fall(self):
        self.current_animation = "fall"
        self.animation_speed = -20
        self.current_frame = 0

    def update(self, dt):
        if self.current_animation == "fall":
            if self.current_frame >= len(self.animations["fall"]) - 1:
                self.current_animation = "down_idle"
        else:
            self.input()
            self.update_animation_state()
        self.animate(dt)
        super().update(dt)
