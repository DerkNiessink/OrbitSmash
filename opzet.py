# import different libaries 
import numpy as np 
import matplotlib.pyplot as plt

class Model:
    def __init__(self, number_of_satelites, number_of_debris, collition_probability, new_satelite):
        """
        Model parameters
        Initialize the model with the parameters.
        """

        def set_number_of_satelites():
            """ Creates initial satelites, with a state, radius and speed."""
            pass

        def set_number_of_debris():
            """ Creates initial debris, with a state, radius and speed."""
            pass


        
class Satelite:
    def __init__(self, state,  radius, position, path, size, mass, speed):
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

if __name__ == '__main__':
    pass 