from pygame import Vector2

from src.config.gamedata import GameData
from src.entities.animatedentity import AnimatedEntity


class Enemy(AnimatedEntity):
    def __init__(self, group, pos, animations, image_offset):
        self.config = GameData()
        self.target = None

        super().__init__(group=group,
                         pos=pos,
                         animations=animations,
                         image_offset=image_offset)

    def set_target(self, target):
        self.target = target

    def move_towards_target(self):
        target_pos = self.target.pos
        dist_x = target_pos.x - self.pos.x
        dist_y = target_pos.y - self.pos.y

        distance = Vector2(dist_x, dist_y)
        if distance.length() > 0:
            self.direction = distance.normalize()
        else:
            self.direction = Vector2()

    def update(self, dt):
        if self.target is not None:
            self.move_towards_target()
        super().update(dt)