# import different libaries
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation


class Object:
    def __init__(
        self,
        epoch,
        semi_major_axis,
        eccentricity,
        argument_of_periapsis,
        longitude_of_ascending_node,
        inclination,
        mean_anomaly,
        mass,
        radius,
    ):
        """
        Class to model the objects.
        """

        # Keplerian orbital elements
        self.semi_major_a = semi_major_axis  # m
        self.ecc = eccentricity  # 1
        self.arg_of_peri = argument_of_periapsis  # rad
        self.LAN = longitude_of_ascending_node  # rad
        self.incl = inclination  # rad
        self.mean_anomaly = mean_anomaly  # rad

        # time of mean_anomaly
        self.epoch = epoch  # JD

        self.mass = mass
        self.radius = radius


class Satellite:
    def __init__(self):
        pass


class Debris:
    def __init__(self):
        pass


class Model:

    # standard gravitational parameter = G * M
    JD = 86400  # s
    mu = 6.6743 * 10**-11 * 5.972 * 10**24  # m**3 * s**-2

    def __init__(self, number_of_satelites, number_of_debris):
        """
        Model parameters
        Initialize the model with the parameters.
        """

    def set_satelites():
        """Creates initial satelites, with a state, radius and speed."""
        pass

    def set_debris():
        """Creates initial debris, with a state, radius and speed."""
        pass

    def update():
        """Update the simulation"""
        pass

    def _calc_new_anomaly(self, time, epoch, mean_anomaly, semi_major_a):
        """Calculate the new anomaly of an object at a specific time point in days"""

        time_delta = self.JD * (time - epoch)  # s
        mean_anomaly = mean_anomaly + time_delta * np.sqrt(self.mu / semi_major_a**3)

        # assumming eccentricity is 0:
        true_anomaly = mean_anomaly

        return true_anomaly

    def _rotate_to_earth_frame(self, pos_orbit_frame, arg_of_peri, LAN, incl):
        """Rotate a vector in the orbit frame (z-axis perpendicular to
        orbital plane, x-asis pointing to periapses of orbit) to the earth
        frame"""
        R = Rotation.from_euler("zxz", [-LAN, -incl, -arg_of_peri])
        return R.as_matrix().dot(pos_orbit_frame)

    def new_position(self, time, object: Object):
        """Calculate the position of an object at specific point in time"""

        true_anomaly = self._calc_new_anomaly(
            time, object.epoch, object.mean_anomaly, object.semi_major_a
        )
        pos_orbit_frame = (
            np.array([np.cos(true_anomaly), np.sin(true_anomaly), 0])
            * object.semi_major_a
        )
        pos = self._rotate_to_earth_frame(
            pos_orbit_frame, object.arg_of_peri, object.LAN, object.incl
        )
        return pos

    def calc_all_positions():
        """Calculate the new positions of all objects"""
        pass


if __name__ == "__main__":
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

    positions = [
        model.new_position(t + 17352.664, satellite) / 1000
        for t in np.arange(0, 1 / 24, 0.001)
    ]

    fig = plt.figure()
    ax = plt.axes(projection="3d")
    for position in positions:
        ax.scatter3D(position[0], position[1], position[2], c="red")

    ax.scatter3D(0, 0, 0)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    fig.savefig("test.png")
