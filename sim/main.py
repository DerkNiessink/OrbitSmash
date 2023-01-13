import sys
import csv
import ast
import pandas as pd
import numpy as np

from model import Object, Model
from graphics import View


def run_sim(objects: list[Object]):

    model = Model()
    model.calc_all_positions(objects, 100000, 100)


def view_sim(objects: list[Object]):

    df = pd.read_csv("output.csv")

    for i, object in enumerate(objects):

        # Convert string of list to list.
        positions = ast.literal_eval(df.iloc[:, i].values[0])
        object.positions = positions

    view = View(objects)
    view.draw(fps=40)


if __name__ == "__main__":

    with open("../data/satelite2.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        objects = [
            Object(
                float(row[0]),
                float(row[1]),
                float(row[2]),
                float(row[3]),
                float(row[4]),
                float(row[5]),
                float(row[6]),
                row[7],
                float(row[8]) * 1000,  # convert to meters
                float(row[9]),
                float(row[10]),
                float(row[11]),
                row[12],
                row[13],
                row[14],
                row[15],
            )
            for row in reader
        ]

    objects = objects[0:1000]

    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run_sim(objects)
    elif len(sys.argv) > 1 and sys.argv[1] == "view":
        view_sim(objects)
    else:
        print(
            "\ninput 'python main.py run' for running the simulation and "
            "'python main.py view' for visualizing the simulation.\n"
        )
