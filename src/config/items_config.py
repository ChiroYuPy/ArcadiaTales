from enum import Enum

from src.config.game_data import GameData
from src.utils.utils import load_and_scale_image

config = GameData()
tile_size = config.player_inventory_slot_size


class ItemImage(Enum):
    AMETHYST_SHARD = load_and_scale_image('assets/images/items/amethyst_shard.png', (tile_size, tile_size))
    APPLE = load_and_scale_image('assets/images/items/apple.png', (tile_size, tile_size))
    ARMOR_STAND = load_and_scale_image('assets/images/items/armor_stand.png', (tile_size, tile_size))
    ARROW = load_and_scale_image('assets/images/items/arrow.png', (tile_size, tile_size))
    BAKED_POTATO = load_and_scale_image('assets/images/items/baked_potato.png', (tile_size, tile_size))
    BEEF = load_and_scale_image('assets/images/items/beef.png', (tile_size, tile_size))
    BEETROOT = load_and_scale_image('assets/images/items/beetroot.png', (tile_size, tile_size))
    BLAZE_POWDER = load_and_scale_image('assets/images/items/blaze_powder.png', (tile_size, tile_size))
    BONE = load_and_scale_image('assets/images/items/bone.png', (tile_size, tile_size))
    BONE_MEAL = load_and_scale_image('assets/images/items/bone_meal.png', (tile_size, tile_size))
    BOOK = load_and_scale_image('assets/images/items/book.png', (tile_size, tile_size))
    BOW = load_and_scale_image('assets/images/items/bow.png', (tile_size, tile_size))
    BOWL = load_and_scale_image('assets/images/items/bowl.png', (tile_size, tile_size))
    BREAD = load_and_scale_image('assets/images/items/bread.png', (tile_size, tile_size))
    BRICK = load_and_scale_image('assets/images/items/brick.png', (tile_size, tile_size))
    BROKEN_ELYTRA = load_and_scale_image('assets/images/items/broken_elytra.png', (tile_size, tile_size))
    BUCKET = load_and_scale_image('assets/images/items/bucket.png', (tile_size, tile_size))
    CAKE = load_and_scale_image('assets/images/items/cake.png', (tile_size, tile_size))
    CANDLE = load_and_scale_image('assets/images/items/candle.png', (tile_size, tile_size))
    CARROT = load_and_scale_image('assets/images/items/carrot.png', (tile_size, tile_size))
    CHAINMAIL_BOOTS = load_and_scale_image('assets/images/items/chainmail_boots.png', (tile_size, tile_size))



ITEMS = {
    "amethyst_shard": {"display_name": "Amethyst Shard", "image": ItemImage.AMETHYST_SHARD, "stack": 4},
    "apple": {"display_name": "Apple", "image": ItemImage.APPLE, "stack": 4},
    "armor_stand": {"display_name": "Armor Stand", "image": ItemImage.ARMOR_STAND, "stack": 4},
    "arrow": {"display_name": "Arrow", "image": ItemImage.ARROW, "stack": 4},
    "baked_potato": {"display_name": "Baked Potato", "image": ItemImage.BAKED_POTATO, "stack": 4},
    "beef": {"display_name": "Beef", "image": ItemImage.BEEF, "stack": 4},
    "beetroot": {"display_name": "Beetroot", "image": ItemImage.BEETROOT, "stack": 4},
    "blaze_powder": {"display_name": "Blaze Powder", "image": ItemImage.BLAZE_POWDER, "stack": 4},
    "bone": {"display_name": "Bone", "image": ItemImage.BONE, "stack": 4},
    "bone_meal": {"display_name": "Bone Meal", "image": ItemImage.BONE_MEAL, "stack": 4},
    "book": {"display_name": "Book", "image": ItemImage.BOOK, "stack": 4},
    "bow": {"display_name": "Bow", "image": ItemImage.BOW, "stack": 4},
    "bowl": {"display_name": "Bowl", "image": ItemImage.BOWL, "stack": 4},
    "bread": {"display_name": "Bread", "image": ItemImage.BREAD, "stack": 4},
    "brick": {"display_name": "Brick", "image": ItemImage.BRICK, "stack": 4},
    "broken_elytra": {"display_name": "Broken Elytra", "image": ItemImage.BROKEN_ELYTRA, "stack": 4},
    "bucket": {"display_name": "Bucket", "image": ItemImage.BUCKET, "stack": 4},
    "cake": {"display_name": "Cake", "image": ItemImage.CAKE, "stack": 4},
    "candle": {"display_name": "Candle", "image": ItemImage.CANDLE, "stack": 4},
    "carrot": {"display_name": "Carrot", "image": ItemImage.CARROT, "stack": 4},
    "chainmail_boots": {"display_name": "Chainmail Boots", "image": ItemImage.CHAINMAIL_BOOTS, "stack": 4},
}
