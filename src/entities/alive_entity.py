from src.entities.animated_entity import AnimatedEntity
from src.overlays.health_bar import HealthBar


class AliveEntity(AnimatedEntity):
    def __init__(self, group, pos, animations, image_offset=(0, 0), name_offset=(0, 0)):
        super().__init__(group, pos, animations, image_offset, name_offset)
        self.health = 9
        self.max_health = 10
        self.attack = 10
        self.defense = 10
        self.is_alive = True

        self.health_bar = HealthBar(self, 60, 8)

    def take_damage(self, damage):
        self.health -= damage*(1 - self.defense/100)
        if self.health <= 0:
            self.is_alive = False

    def attack_target(self, target):
        target.take_damage(self.attack)

    def update(self, dt):
        super().update(dt)
