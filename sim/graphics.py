from vpython import *

from model import Object


class View:
    RE = 6371 * 10**3

    def __init__(self, objects: list[Object]):
        self.objects = objects
        self.Earth = sphere(pos=vector(0, 0, 0), radius=self.RE, texture=textures.earth)
        self.drawables = self._make_drawables()
        self.n_positions = len(objects[0].positions)

    def _make_drawables(self):
        drawables = [
            sphere(
                pos=vector(
                    object.positions[0][0],
                    object.positions[0][1],
                    object.positions[0][2],
                ),
                radius=0.01 * self.RE,
                make_trail=False,
            )
            for object in self.objects
        ]
        return drawables

    def draw(self):
        for i in range(self.n_positions):
            rate(40)
            for object, drawable in zip(self.objects, self.drawables):
                drawable.pos = vector(
                    object.positions[i][0],
                    object.positions[i][1],
                    object.positions[i][2],
                )
