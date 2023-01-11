from vpython import *

G=6.67e-11
RE=6.378e6
ME=5.972e24

Earth=sphere(pos=vector(0,0,0),radius=RE, texture=textures.earth)
Earth.m=ME
Earth.p=Earth.m*vector(0,0,0)

# sat=sphere(pos=vector(2*RE,0,0),radius=.03*RE, make_trail=True)
# sat.m=100
# sat.p=sat.m*vector(0,5000,0)

# t=0
# dt=1

# while t<10000:
#   rate(400)
#   r=sat.pos-Earth.pos
#   F=-G*Earth.m*sat.m*norm(r)/mag(r)**2
#   sat.p=sat.p+F*dt
#   sat.pos=sat.pos+sat.p*dt/sat.m
#   t=t+dt