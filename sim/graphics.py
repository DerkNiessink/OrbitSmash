import sys
from vpython import *

from model import Object


class View:
    RE = 6371 * 10**3

    def __init__(self, objects: list[Object]):
        self.objects = objects
        self.Earth = sphere(pos=vector(0, 0, 0), radius=self.RE, texture=textures.earth)
        scene.width, scene.height = 1900, 980
        self.drawables = self._make_drawables()
        self.n_positions = len(objects[0].positions)

    def _make_drawables(self) -> list[sphere]:
        """
        Create spheres from the objects that can be drawn on the screen

        Returns the drawable spheres with an initial positions.
        """
        drawables = [
            sphere(
                pos=vector(
                    object.positions[0][0],
                    object.positions[0][1],
                    object.positions[0][2],
                ),
                radius=0.005 * self.RE,
                make_trail=False,
                color=self._get_color_(object),
            )
            for object in self.objects
        ]
        return drawables

    def _get_color_(self, object: Object) -> vector:
        """Returns the color vector of the given object"""

        if object.object_type == "DEBRIS":
            return vector(1, 0, 0)
        else:
            return vector(1, 1, 1)

    def draw(self, fps=40):
        """
        Draw the objects on the screen in the browser.

        fps: frame per seconds.
        """
        for i in range(self.n_positions):
            rate(fps)
            for object, drawable in zip(self.objects, self.drawables):
                drawable.pos = vector(
                    object.positions[i][0],
                    object.positions[i][1],
                    object.positions[i][2],
                )
        sys.exit()
