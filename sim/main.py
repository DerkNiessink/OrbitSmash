import sys
import numpy as np
from tqdm import tqdm
import csv

from model import *

from graphics import View
from data_cleaning import data_array, all_groups


def fast_arr(objects: np.ndarray):
    """
    Prepare fast array for usage with Numba.

    Returns array of the form:
      -> ['EPOCH', 'MEAN_ANOMALY', 'SEMIMAJOR_AXIS', 'SATELLITE/DEBRIS  'pos_x', pos_y', 'pos_z']
    """
    return np.array([[object[0], object[4], object[6], object[13], 0, 0, 0] for object in objects])


def run_sim(
    objects: np.ndarray,
    group: int,
    draw: bool,
    margin: int,
    endtime: float,
    timestep: float,
    epoch: float,
    probability: float,
    percentage: float,
    frequency_new_debris: int,
):
    """
    Run the simulation by calculating the position of the objects, checking
    for collisions and handling the collisions.
    """

    if draw:
        view = View(objects)

    initialize_positions(objects, epoch)

    objects_fast = fast_arr(objects)
    matrices = np.array([object[11] for object in objects])

    parameters = []
    collisions = []
    added_debris = []

    for time in tqdm(
        range(int(epoch), int(epoch + endtime), timestep),
        ncols=100,
        desc=f"group: {group}",
    ):
        calc_all_positions(objects_fast, matrices, time)

        collided_objects = check_collisions(objects_fast, margin)
        if collided_objects != None:
            print("Collision!")
            object1, object2 = collided_objects[0], collided_objects[1]

            # Compute new debris
            new_debris = collision(object1, object2)
            

            # Add new debris to the total objects an debris arrays
            objects_fast = np.concatenate((objects_fast, new_debris), axis=0)

            # Save the collision data
            collisions.append([object1, object2, time])

        if (
            frequency_new_debris != None
            and (time - epoch) % (frequency_new_debris * timestep) == 0
        ):
            objects_fast, matrices, new_debris = random_debris(
                objects_fast, matrices, time, percentage
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

    """GROUP SELECTION"""
    if len(sys.argv) > 1 and int(sys.argv[1]) in all_groups:
        group = int(sys.argv[1])

    else:
        print("Give a valid number of the orbit you want to evaluate")
        sys.exit()

    group_selection = data_array[:, 12] == group

    data_array_group = data_array[group_selection]

    objects = data_array_group

    """ VISUALISATION"""
    draw = False

    if len(sys.argv) > 2 and sys.argv[2] == "view":
        draw = True

    parameters, collisions, added_debris = run_sim(
        objects,
        group,
        draw,
        margin=100,
        endtime=315569260/10,
        timestep=100,
        epoch=1675209600.0,
        probability=1,
        percentage=0,
        frequency_new_debris=31556926,
    )

    """ DATA STORAGE """
    with open(
        f"sim/data_storage/group_{objects[0][12]}/parameters.csv", "w"
    ) as csvfile:
        write = csv.writer(csvfile)
        write.writerow(
            ["group", "epoch", "endtime", "timestep", "probabilty", "precentage"]
        )
        write.writerows(parameters)

    with open(
        f"sim/data_storage/group_{objects[0][12]}/collisions.csv", "w"
    ) as csvfile:
        write = csv.writer(csvfile)
        write.writerow(["object1", "object2", "time"])
        write.writerows(collisions)

    with open(f"sim/data_storage/group_{objects[0][12]}/debris.csv", "w") as csvfile:
        write = csv.writer(csvfile)
        write.writerow(["number_debris", "time"])

    print(f"\ngroup {group} done running")
