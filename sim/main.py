import sys
import numpy as np
from tqdm import tqdm
import csv
import os
from collections import defaultdict

from model import *
from graphics import View
from data_cleaning import  data_array_group, data_array_debris_group # data_array,


def fast_arr(objects: np.ndarray):
    """
    Prepare fast array for usage with Numba.

    Returns array of the form:
      -> ['EPOCH', 'MEAN_ANOMALY', 'SEMIMAJOR_AXIS', 'pos_x', pos_y', 'pos_z']
    """
    return np.array(
        [[object[0], object[4], object[6], 0, 0, 0, object[1]] for object in objects]
    )


def run_sim(
    objects: np.ndarray,
    debris: np.ndarray,
    endtime: float,
    timestep: float,
    epoch=1635771601.0,
    draw=False,
    probability = 0.8,
    percentage = 10,  
):
    """
    Run the simulation by calculating the position of the objects, checking
    for collisions and handling the collisions.
    """

    if draw:
        view = View(objects)

    initialize_positions(objects, epoch)
    
    

    objects_fast = fast_arr(objects)
    debris_fast = fast_arr(debris)
    matrices = np.array([object[11] for object in objects])

    collisions =  []
    added_debris = []

    for time in tqdm(np.arange(epoch, epoch + endtime, timestep), ncols=100):
        calc_all_positions(objects_fast, matrices, time)

        check_collisions(objects_fast, debris_fast)

        if check_collisions(objects_fast, debris_fast) != None:
            print('True')
        
        
        debris = random_debris(objects, debris, probability, percentage)

        #collisions.append([object1, object2, time])
        added_debris.append([debris, time])

        """Functies die na een bepaalde delta t worden aangeroepen"""
        """ Een dag """
        if time % 86400 == 0:
            # roep hier dan een functie aan 
            # random_debris(...)
            pass

        """ Een jaar """
        if time % 31556926 == 0:
            # roep hier dan een functie aan 
            #random_debris(...)
            pass

        
        if draw:
            view.draw(objects_fast)

    """ DATA """
    parameters = {'group': objects[0][12], 'epoch': epoch, 'endtime' : endtime, 'timestep':timestep, 
                    'probabilty': probability , 'precentage' : percentage}


    return parameters, collisions, added_debris




if __name__ == "__main__":
    objects = data_array_group
    debris = data_array_debris_group

    view = False

    if len(sys.argv) > 1 and sys.argv[1] == "view":
        view = True

    epoch = int()
    endtime = int() 
    timestep = int(), 
    probabilty = float() 
    precentage = int()
    
    parameters, collisions, added_debris = run_sim(objects, debris, endtime=31556926, timestep=100, draw=view)

    with open(f'all_data/{object[0][12]}/parameters.csv', 'w') as f:
      
        csv_writer = csv.writer(f)
        csv_writer.writerow(parameters.keys())
        csv_writer.writerows(parameters)

    with open(f'all_data/{object[0][12]}/collisions.csv', 'w') as f:
      
        csv_writer = csv.writer(f)
        csv_writer.writerow(['Object1', 'Object 2', 'Time'])
        csv_writer.writerows(collisions)

    with open(f'all_data/{object[0][12]}/new_debris.csv', 'w') as f:
      
        csv_writer = csv.writer(f)
        csv_writer.writerow(['Number of new debris', 'Time'])
        csv_writer.writerows(collisions)
    
    
    

