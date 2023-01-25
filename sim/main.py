import sys
import numpy as np
from tqdm import tqdm
import csv

from model import *
from graphics import View
from data_cleaning import data_array, data_array_debris, all_groups


def fast_arr(objects: np.ndarray):
    """
    Prepare fast array for usage with Numba.

    Returns array of the form:
      -> ['EPOCH', 'MEAN_ANOMALY', 'SEMIMAJOR_AXIS', 'pos_x', pos_y', 'pos_z']
    """
    return np.array([[object[0], object[4], object[6], 0, 0, 0] for object in objects])


def run_sim(
    objects: np.ndarray,
    debris: np.ndarray,
    margin: int,
    endtime: float,
    timestep: float,
    epoch=1635771601.0,
    draw=False,
    probability=0.5,
    percentage=10,
    frequency_new_debris=200000,
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

    parameters = []
    collisions = []
    added_debris = []

    for time in tqdm(np.arange(epoch, epoch + endtime, timestep), ncols=100):

        calc_all_positions(objects_fast, matrices, time)
        
        
        if check_collisions(objects_fast, debris_fast, margin) != None:
            object1, object2 = check_collisions(objects_fast, debris_fast, margin)
            collisions.append([object1, object2, time])
            

        if (
            frequency_new_debris != None
            and (time - epoch) % (frequency_new_debris * timestep) == 0
        ):
            objects_fast, debris_fast, matrices, new_debris = random_debris(
                objects_fast, debris_fast, matrices, time, percentage
            )

            added_debris.append([new_debris, time])
    

            if draw:
                view.make_new_drawables(objects_fast)

        if draw:
            view.draw(objects_fast, time - epoch)

    """ DATA """
    parameters.append(
        [objects[0][12], epoch, endtime, timestep, probability, percentage]
    )

    return parameters, collisions, added_debris


if __name__ == "__main__":

    """ GROUP SELECTION """
    group = 78
    # roep de variabele 'all_groups' aan als je een lijst wil met alle groepen. 

    group_selection = data_array[:, 12] == group
    group_selection_debris = data_array_debris[:, 12] == group

    data_array_group = data_array[group_selection]
    data_array_debris_group = data_array_debris[group_selection_debris]

    objects = data_array_group
    debris = data_array_debris_group

    """ VISUALISATION"""
    view = False

    if len(sys.argv) > 1 and sys.argv[1] == "view":
        view = False

    parameters, collisions, debris = run_sim(
        objects, debris, margin=100, endtime=31556926, timestep=100, draw=view
    )
    

    """ DATA STORAGE """
    with open(f"data_storage/group_{objects[0][12]}/parameters.csv", "w") as csvfile:
        write = csv.writer(csvfile)
        write.writerow(
            ["group", "epoch", "endtime", "timestep", "probabilty", "precentage"]
        )
        write.writerows(parameters)

    with open(f"data_storage/group_{objects[0][12]}/collisions.csv", "w") as csvfile:
        write = csv.writer(csvfile)
        write.writerow(["object1", "object2", "time"])
        write.writerows(collisions)

    with open(f"data_storage/group_{objects[0][12]}/debris.csv", "w") as csvfile:
        write = csv.writer(csvfile)
        write.writerow(["number_debris", "time"])
        write.writerows(debris)
