from src.config.gamedata import GameData
from src.entities.enemies.enemy import Enemy


class Slime(Enemy):
    def __init__(self, group, pos):
        self.config = GameData()

        super().__init__(group=group,
                         pos=pos,
                         animations={'up_walk': [], 'down_walk': [], 'left_walk': [], 'right_walk': [],
                                     'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                                     'right_atk': [], 'left_atk': [], 'up_atk': [], 'down_atk': []},
                         image_offset=(0, 0))

        self.name = "slime"
        self.animation_state = "idle"
        self.animation_direction = "down"
        self.speed = self.config.slime_speed
        self.import_assets(scale=self.config.tile_scale)

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
            self.animation_speed = 8
        self.current_animation = self.animation_direction + "_" + self.animation_state

    def update(self, dt):
        self.update_animation_state()
        self.animate(dt)
        super().update(dt)
