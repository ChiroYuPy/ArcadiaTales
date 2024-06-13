from src.entities.entity import Entity
from src.guis.items import ITEMS


class DroppedItem(Entity):
    def __init__(self, item_id):
        super().__init__(group=None, pos=(0, 0))
        self.name = ITEMS[item_id]["display_name"]
        self.image = ITEMS[item_id]["image"]
        self.stack = 0
        self.stack_max = ITEMS[item_id]["stack"]