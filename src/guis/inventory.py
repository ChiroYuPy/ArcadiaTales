from src.guis.items import TileItem, ITEMS


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
        row = slot // self.width
        col = slot % self.width
        if 0 <= row < self.height and 0 <= col < self.width:
            self.slots[row][col] = TileItem(slot=slot, item_id=item_id)

    def remove_item(self, slot):
        row = slot // self.width
        col = slot % self.width
        if 0 <= row < self.height and 0 <= col < self.width:
            self.slots[row][col] = TileItem(slot=slot)

    def reset_inventory(self):
        for row in range(self.height):
            for col in range(self.width):
                self.slots[row][col] = TileItem(slot=row * self.width + col)
