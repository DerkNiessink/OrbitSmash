from vpython import *
import vpython
import numpy as np


class View:
    RE = 6371 * 10**3

    def __init__(self, objects: np.ndarray):
        self.objects = objects
        self.Earth = sphere(pos=vector(0, 0, 0), radius=self.RE, texture=textures.earth)
        # self.Earth.rotate(angle=0.5 * pi, axis=vector(1, 0, 0))
        scene.width, scene.height = 1900, 980
        self.drawables = self._make_drawables()

    def make_new_drawables(self, objects):
        for drawable in self.drawables:
            drawable.visible = False

        self.objects = objects
        self.drawables = self._make_drawables()

    def _make_drawables(self) -> list[sphere]:
        """
        Create spheres from the objects that can be drawn on the screen

        Returns the drawable spheres with an initial positions.
        """
        drawables = [
            sphere(
                pos=vector(0, 0, 0),
                radius=0.005 * self.RE,
                make_trail=False,
                color=self._get_color_(object),
            )
            for object in self.objects
        ]
        return drawables

    def _get_color_(self, object: np.ndarray) -> vector:
        """Returns the color vector of the given object"""

        if len(object) < 7 or object[7] == "DEBRIS":
            return vector(1, 0, 0)
        else:
            return vector(1, 1, 1)

    def draw(self, objects: np.ndarray, time, fps=40):
        """
        Draw the objects on the screen in the browser.

        fps: frame per seconds.
        """
        rate(fps)
        scene.title = f"t = {time} \nN objects = {len(objects)}"
        for object, drawable in zip(objects, self.drawables):
            drawable.pos = vector(object[3], object[4], object[5])
