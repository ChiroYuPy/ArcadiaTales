from enum import Enum

import pygame


class ItemImage(Enum):
    AMETHYST_SHARD = pygame.image.load('assets/images/items/amethyst_shard.png')
    APPLE = pygame.image.load('assets/images/items/apple.png')
    ARMOR_STAND = pygame.image.load('assets/images/items/armor_stand.png')
    ARROW = pygame.image.load('assets/images/items/arrow.png')
    BAKED_POTATO = pygame.image.load('assets/images/items/baked_potato.png')
    BEEF = pygame.image.load('assets/images/items/beef.png')


ITEMS = {
    "amethyst_shard": {"display_name": "Amethyst Shard", "image": ItemImage.AMETHYST_SHARD},
    "apple": {"display_name": "Apple", "image": ItemImage.APPLE},
    "armor_stand": {"display_name": "Armor Stand", "image": ItemImage.ARMOR_STAND},
    "arrow": {"display_name": "Arrow", "image": ItemImage.ARROW},
    "baked_potato": {"display_name": "Baked Potato", "image": ItemImage.BAKED_POTATO},
    "beef": {"display_name": "Beef", "image": ItemImage.BEEF},
}


class TileItem:
    def __init__(self, slot, item_id=None):
        self.slot = slot
        self.item_id = item_id
        if item_id:
            self.name = ITEMS[item_id]["display_name"]
            self.image = ITEMS[item_id]["image"]
        else:
            self.name = None
            self.image = None


class Inventory:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.slots = [[TileItem(slot=x + y * self.width) for x in range(self.width)] for y in range(self.height)]
        self.hand_inventory = None

    def add_item(self, item_id):
        for row in self.slots:
            for tile in row:
                if not tile.item_id:
                    tile.item_id = item_id
                    tile.name = ITEMS[item_id]["display_name"]
                    tile.image = ITEMS[item_id]["image"]
                    return

    def set_item(self, item_id, slot):
        tile = self.slots[slot[1]][slot[0]]
        tile.item_id = item_id
        tile.name = ITEMS[item_id]["display_name"]
        tile.image = ITEMS[item_id]["image"]

    def remove_item(self, slot):
        tile = self.slots[slot[1]][slot[0]]
        tile.item_id = None
        tile.name = None
        tile.image = None

    def reset_inventory(self):
        for row in range(self.height):
            for col in range(self.width):
                self.slots[row][col] = TileItem(slot=row * self.width + col)
