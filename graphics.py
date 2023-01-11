from vpython import *
from main import Model, Object
import numpy as np
import csv

# Objects_list = []

# with open('data/satelite2.csv', 'r') as f:
#         reader = csv.reader(f)
#         next(reader)
#         for row in reader:
#             Objects_list.append(Object(float(row[0]), float(row[1]), float(row[2]),float(row[3]) * (np.pi / 180), float(row[4]) * (np.pi / 180),
#              float(row[5]) * (np.pi / 180) ,float(row[6]) * (np.pi / 180), row[7], float(row[8]), float(row[9]), 
#             float(row[10]), float(row[11]), row[12], row[13], row[14], row[15]))

model = Model(1, 0)

satellite = Object(
    17352.664,
    6738000,
    0,
    256.7529 * (np.pi / 180),
    198.7788 * (np.pi / 180),
    51.6357 * (np.pi / 180),
    103.3278 * (np.pi / 1),
    1,
    1,
)

positions = [model.new_position(t + 17352.664, satellite) for t in np.arange(0, 1, 0.00001)]

RE=6.378*(10**6)

Earth=sphere(pos=vector(0,0,0),radius=RE, texture=textures.earth)


sat=sphere(pos=vector(positions[0][0], positions[0][1], positions[0][2]),radius=.03*RE, make_trail=False)


t=0
dt=1

while t<1000000:
  rate(400)
#   r=sat.pos-Earth.pos

  sat.pos=vector(positions[t][0], positions[t][1], positions[t][2])
  t=t+dt