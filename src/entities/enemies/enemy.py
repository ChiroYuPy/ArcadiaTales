from pygame import Vector2

from src.config.gamedata import GameData
from src.entities.animatedentity import AnimatedEntity


class Enemy(AnimatedEntity):
    def __init__(self, group, pos, animations, image_offset=(0, 0), name_offset=(0, 0)):
        self.config = GameData()
        super().__init__(group=group,
                         pos=pos,
                         animations=animations,
                         image_offset=image_offset,
                         name_offset=name_offset)
        self.target = None

    def set_target(self, target):
        self.target = target

    def move_towards_target(self):
        target_pos = self.target.pos
        dist_x = target_pos.x - self.pos.x
        dist_y = target_pos.y - self.pos.y

        distance = Vector2(dist_x, dist_y)
        if distance.length() > 10 * self.config.tile_size:
            self.direction = Vector2()
        elif distance.length() > 2 * self.config.tile_size:
            self.direction = distance.normalize()
        else:
            self.direction = Vector2()

    def update(self, dt):
        if self.target is not None:
            self.move_towards_target()
        super().update(dt)