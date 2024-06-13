import pygame
from pygame import Vector2, Surface, SRCALPHA
from src.config.game_data import GameData
from src.utils.colors import Color


class InventoryUI:
    def __init__(self, inventory):
        self.inventory = inventory
        self.config = GameData()
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface(
            (self.inventory.width * self.config.player_inventory_slot_size,
             self.inventory.height * self.config.player_inventory_slot_size))
        self.inventory_slot_image = pygame.image.load("assets/images/gui/slot.png")
        self.inventory_slot_image = pygame.transform.scale(self.inventory_slot_image, (
            self.config.player_inventory_slot_size, self.config.player_inventory_slot_size))

        self.inventory_pos = Vector2((self.config.window_width - self.surface.get_width()) // 2,
                                     (self.config.window_height - self.surface.get_height()) // 2)

        self.inventory_rect = self.inventory_slot_image.get_rect(center=self.inventory_pos)

    def get_slot_coordinates_from_pos(self, pos):
        x, y = pos
        relative_x = x - self.inventory_pos.x
        relative_y = y - self.inventory_pos.y
        row = int(relative_y // self.config.player_inventory_slot_size)
        col = int(relative_x // self.config.player_inventory_slot_size)
        return row, col

    def get_hand_surface(self):
        if self.inventory.hand_inventory:
            hand_surface = Surface((self.config.player_inventory_slot_size, self.config.player_inventory_slot_size), SRCALPHA)
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
                            self.inventory.remove_item(row * self.inventory.width + col)  # Remove item from inventory
                        else:
                            temp = self.inventory.slots[row][col]
                            self.inventory.slots[row][col] = self.inventory.hand_inventory
                            self.inventory.hand_inventory = temp
                    else:
                        if self.inventory.hand_inventory:
                            self.inventory.slots[row][col] = self.inventory.hand_inventory
                            self.inventory.hand_inventory = None

    def draw(self):
        self.inventory_pos = Vector2(self.config.window_width * 0.766 - self.surface.get_width() // 2,
                                     self.config.window_height // 2 - self.surface.get_height() // 2)
        # Create a new surface for the inventory image
        inventory_image = pygame.Surface(self.surface.get_size())

        # Draw the inventory surface onto inventory_image
        for row, slot_row in enumerate(self.inventory.slots):
            for col, tile in enumerate(slot_row):
                x = col * self.config.player_inventory_slot_size
                y = row * self.config.player_inventory_slot_size
                inventory_image.blit(self.inventory_slot_image, (x, y))
                if tile.image:
                    inventory_image.blit(tile.image.value, (x, y))

        # Blit the inventory_image onto self.surface
        self.surface.blit(inventory_image, (0, 0))

        # Blit self.surface onto display_surface
        self.display_surface.blit(self.surface, self.inventory_pos)

        # Draw the hand surface
        hand_surface = self.get_hand_surface()
        if hand_surface:
            mouse_pos = pygame.mouse.get_pos()
            image_rect = hand_surface.get_rect(center=mouse_pos)
            self.display_surface.blit(hand_surface, image_rect)
