import pygame
from pygame import Vector2, Surface, SRCALPHA
from src.config.game_data import GameData
from src.utils.colors import Color

scale = 2
slot_size = 16 * scale


class InventoryUI:
    def __init__(self, inventory):
        self.inventory = inventory
        self.config = GameData()
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface(
            (self.inventory.width * slot_size,
             self.inventory.height * slot_size), pygame.SRCALPHA)
        self.inventory_slot_image = pygame.image.load("assets/images/gui/slot.png")
        self.inventory_slot_image = pygame.transform.scale(self.inventory_slot_image, (slot_size, slot_size))
        self.inventory_pos = Vector2((self.config.window_width - self.surface.get_width()) // 2,
                                     (self.config.window_height - self.surface.get_width()) // 2)
        self.inventory_rect = self.inventory_slot_image.get_rect(center=self.inventory_pos)

    @staticmethod
    def get_slot_coordinates_from_pos(pos):
        x = pos[0] // slot_size
        y = pos[1] // slot_size
        return x, y

    def get_hand_surface(self):
        if self.inventory.hand_inventory:
            hand_surface = Surface((slot_size, slot_size), SRCALPHA)
            hand_surface.fill(Color.TRANSPARENT)
            hand_surface.blit(self.inventory.hand_inventory.image.value, (0, 0))
            return hand_surface
        return None

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                row, col = self.get_slot_coordinates_from_pos(mouse_pos)
                if 0 <= row < self.inventory.height and 0 <= col < self.inventory.width:
                    if self.inventory.slots[row][col].item_id is not None:
                        if self.inventory.hand_inventory is None:
                            self.inventory.hand_inventory = self.inventory.slots[row][col]
                            self.inventory.remove_item((col, row))
                        else:
                            temp = self.inventory.slots[row][col]
                            self.inventory.slots[row][col] = self.inventory.hand_inventory
                            self.inventory.hand_inventory = temp
                    else:
                        if self.inventory.hand_inventory:
                            self.inventory.slots[row][col] = self.inventory.hand_inventory
                            self.inventory.hand_inventory = None

    def draw(self):
        self.surface.fill(Color.DARK_RED)
        for row, slot_row in enumerate(self.inventory.slots):
            for col, tile in enumerate(slot_row):
                x = col * slot_size
                y = row * slot_size
                if tile.image:
                    self.surface.blit(tile.image.value, (x, y))
                self.surface.blit(self.inventory_slot_image, (x, y))
        self.display_surface.blit(self.surface, self.inventory_pos)
