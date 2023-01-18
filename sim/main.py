import sys
import numpy as np
from tqdm import tqdm

from model import *
from graphics import View
from data_cleaning import data_array


def run_sim(
    objects: np.ndarray,
    endtime: float,
    timestep: float,
    begin_year=2030,
    epoch=1635771601.0,
    draw=False,
):

    if draw:
        view = View(objects)

    initialize_positions(objects, epoch)

    objects_fast = np.array(
        [
            [
                object[0],
                object[4],
                object[6],
                0,
                0,
                0,
            ]
            for object in objects
        ]
    )
    matrices = np.array([object[11] for object in objects])

    for time in tqdm(np.arange(epoch, epoch + endtime, timestep), ncols=100):
        calc_all_positions(objects_fast, matrices, time)
        # check_collisions(objects_fast)

        if draw:
            view.draw(objects_fast)


if __name__ == "__main__":
    objects = data_array
    view = False

    if len(sys.argv) > 1 and sys.argv[1] == "view":
        view = True

    run_sim(objects, endtime=100000, timestep=100, draw=view)
