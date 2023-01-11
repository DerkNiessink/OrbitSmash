# import different libaries
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation
import csv


class Object:
    def __init__(
        self,
        epoch,
        mean_motion, 
        eccentricity,
        inclination,
        ra_of_asc_node, 
        arg_of_pericenter, 
        mean_anomaly,
        norad_cat_id, 
        semimajor_axis,
        period, 
        apoapsis, 
        periapsis, 
        object_type, 
        rcs_size, 
        country_code, 
        launch_date
    ):
        """
        Class to model the objects.
        """

        # Keplerian orbital elements
        # time of mean_anomaly
        self.epoch = epoch
        self.mean_motion = mean_motion
        self.eccentricity = eccentricity # 1 
        self.inclination = inclination # rad 
        self.ra_of_asc_node = ra_of_asc_node # rad
        self.arg_of_pericenter = arg_of_pericenter # rad 
        self.mean_anomaly = mean_anomaly # rad 
        self.norad_cat_id = norad_cat_id
        self.semimajor_axis = semimajor_axis # m
        self.period = period
        self.apoapsis = apoapsis
        self.periapsis = periapsis
        self.object_type = object_type
        self.rcs_size = rcs_size
        self.country_code = country_code
        self.launch_date = launch_date


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

    def _calc_new_anomaly(self, time, epoch, mean_anomaly, semimajor_axis):
        """Calculate the new anomaly of an object at a specific time point in days"""

        time_delta = self.JD * (time - epoch)  # s
        mean_anomaly = mean_anomaly + time_delta * np.sqrt(self.mu / semimajor_axis**3)

        # assumming eccentricity is 0:
        true_anomaly = mean_anomaly

        return true_anomaly

    def _rotate_to_earth_frame(self, pos_orbit_frame, arg_of_pericenter, ra_of_asc_node, inclination):
        """Rotate a vector in the orbit frame (z-axis perpendicular to
        orbital plane, x-asis pointing to periapses of orbit) to the earth
        frame"""
        R = Rotation.from_euler("zxz", [-ra_of_asc_node, -inclination, -arg_of_pericenter])
        return R.as_matrix().dot(pos_orbit_frame) # welke variabele is dit? 

    def new_position(self, time, object: Object):
        """Calculate the position of an object at specific point in time"""

        true_anomaly = self._calc_new_anomaly(
            time, object.epoch, object.mean_anomaly, object.semimajor_axis
        )
        pos_orbit_frame = (
            np.array([np.cos(true_anomaly), np.sin(true_anomaly), 0])
            * object.semimajor_axis
        )
        pos = self._rotate_to_earth_frame(
            pos_orbit_frame, object.arg_of_pericenter, object.ra_of_asc_node, object.inclination
        )
        return pos

    def calc_all_positions():
        """Calculate the new positions of all objects"""
        pass


if __name__ == "__main__":
    model = Model(1, 0)

    # inladen csv 
    Objects_list = []

    with open('file.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            Objects_list.append(Object(row[0], row[1], row[2],row[3] * (np.pi / 180), row[4] * (np.pi / 180),
             row[5] * (np.pi / 180) ,row[6] * (np.pi / 180), row[7], row[8], row[9], 
            row[10], row[11], row[12], row[13], row[14], row[15]))

























    # satellite = Object(
    #     'DEBRIS', 
    #     17352.664,
    #     6738000,
    #     0,
    #     256.7529 * (np.pi / 180),
    #     198.7788 * (np.pi / 180),
    #     51.6357 * (np.pi / 180),
    #     103.3278 * (np.pi / 1),
    #     1,
    #     1,
    # )

    # positions = [
    #     model.new_position(t + 17352.664, Objects_list[0]) / 1000
    #     for t in np.arange(0, 1 / 24, 0.001)
    # ]

    # fig = plt.figure()
    # ax = plt.axes(projection="3d")
    # for position in positions:
    #     ax.scatter3D(position[0], position[1], position[2], c="red")

    # ax.scatter3D(0, 0, 0)
    # ax.set_xlabel("x")
    # ax.set_ylabel("y")
    # ax.set_zlabel("z")
    # fig.savefig("test.png")
