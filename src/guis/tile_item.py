from src.config.items_config import ITEMS


class TileItem:
    def __init__(self, slot, item_id=None):
        self.slot = slot
        self.item_id = item_id
        if item_id:
            self.name = ITEMS[item_id]["display_name"]
            self.image = ITEMS[item_id]["image"]
            self.stack = 0
            self.stack_max = ITEMS[item_id]["stack"]
        else:
            self.name = None
            self.image = None
