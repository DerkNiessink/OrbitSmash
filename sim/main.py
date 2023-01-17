import sys
import csv
import ast
import pickle
import numpy as np

from model import Object, Model
from graphics import View
from data_cleaning import data_array


def run_sim(data_array):
    objects = data_array
    model = Model(objects)
    model.calc_all_positions(100000, 100)


def load_objects(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


def view_sim(objects: list[Object]):

    objects = load_objects("output.dat")  # Gives a generators
    objects_list = [object for object in objects]

    view = View(objects_list)
    view.draw(fps=40)


if __name__ == "__main__":
    objects = data_array
    objects = objects[0:100]

    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run_sim(objects)
    elif len(sys.argv) > 1 and sys.argv[1] == "view":
        view_sim(objects)
    else:
        print(
            "\ninput 'python main.py run' for running the simulation and "
            "'python main.py view' for visualizing the simulation.\n"
        )
