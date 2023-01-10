# import different libaries
import numpy as np
import matplotlib.pyplot as plt


class Model:
    def __init__(self, number_of_satelites, number_of_debris, new_satelite):
        """
        Model parameters
        Initialize the model with the parameters.
        """

        def set_satelites():
            """Creates initial satelites, with a state, radius and speed."""
            pass

        def set_debris():
            """Creates initial debris, with a state, radius and speed."""
            pass

        def update():
            """Update the simulation"""
            pass

        def calc_new_position():
            """Calculate the new position of a specific object"""
            pass

        def calc_all_positions():
            """Calculate the new positions of all objects"""
            pass


class Satelite:
    def __init__(self, state, radius, position, path, size, mass, speed):
        """
        Class to model the satelites.
        """
        self.state = state  # is the satelite active or inactive?
        self.radius = radius
        self.position = position
        self.path = path
        self.size = size
        self.mass = mass
        self.speed = speed


class Debris:
    def __init__(self, state, radius, position, path, size, mass, speed):
        """
        Class to model the debris.
        """
        self.state = state  # is the debris lethal or non-lethal?
        self.radius = radius
        self.position = position
        self.path = path
        self.size = size
        self.mass = mass
        self.speed = speed


if __name__ == "__main__":
    pass
