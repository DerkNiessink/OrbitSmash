import numpy as np
import csv

from model import Object, Model

# import graphics

model = Model()

with open("../data/satelite2.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    objects = [
        Object(
            float(row[0]),
            float(row[1]),
            float(row[2]),
            float(row[3]) * (np.pi / 180),
            float(row[4]) * (np.pi / 180),
            float(row[5]) * (np.pi / 180),
            float(row[6]) * (np.pi / 180),
            row[7],
            float(row[8]),
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

model.initialize_positions(objects, 1635771601.0)
model.calc_all_positions(objects, 50, 10)

# graphics.plot(objects, all_positions)

print(len(objects))
