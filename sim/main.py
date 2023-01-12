import numpy as np
import csv

from model import Object, Model
from graphics import View

model = Model()

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
model.calc_all_positions(objects, 100000, 100)

view = View(objects)
view.draw()
