from vpython import *
from model import Model, Object
import numpy as np

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