from src.entities.entity import Entity


class GraphicEntity(Entity):
    def __init__(self, group, pos):
        super().__init__(group, pos)
        self.image = "None"