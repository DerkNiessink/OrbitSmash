import numpy as np
from scipy.spatial.transform import Rotation
import pandas as pd
from collections import defaultdict


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
        launch_date,
    ):
        """
        Class to model the objects.
        """

        # Keplerian orbital elements
        # time of mean_anomaly
        self.epoch = epoch
        self.mean_motion = mean_motion
        self.eccentricity = eccentricity  # 1
        self.inclination = inclination  # rad
        self.ra_of_asc_node = ra_of_asc_node  # rad
        self.arg_of_pericenter = arg_of_pericenter  # rad
        self.mean_anomaly = mean_anomaly  # rad
        self.norad_cat_id = norad_cat_id
        self.semimajor_axis = semimajor_axis  # m
        self.period = period
        self.apoapsis = apoapsis
        self.periapsis = periapsis
        self.object_type = object_type
        self.rcs_size = rcs_size
        self.country_code = country_code
        self.launch_date = launch_date

        self.positions = []


class Model:

    # standard gravitational parameter = G * M
    JD = 86400  # s
    mu = 6.6743 * 10**-11 * 5.972 * 10**24  # m**3 * s**-2

    def __init__(self):
        """
        Model parameters
        Initialize the model with the parameters.
        """

    def _calc_new_anomaly(self, time, epoch, mean_anomaly, semimajor_axis):
        """
        Calculate the new anomaly of an object at a specific Julian date in
        seconds

        time: Julian date in seconds of the desired anomaly.
        epoch: Julian date in seconds.
        mean_anomaly: anomaly corresponding to the object's epoch in rad.
        semimajor_axis: semimajor-axis of the object's orbit in meters.
        """

        time_delta = time - epoch  # s
        mean_anomaly = mean_anomaly + time_delta * np.sqrt(
            self.mu / semimajor_axis**3
        )

        # assumming eccentricity is 0:
        true_anomaly = mean_anomaly

        return true_anomaly

    def _rotate_to_earth_frame(
        self,
        pos_orbit_frame: np.ndarray,
        arg_of_pericenter: float,
        ra_of_asc_node: float,
        inclination: float,
    ) -> np.ndarray:
        """
        Rotate a vector in the orbit frame (z-axis perpendicular to
        orbital plane, x-asis pointing to periapses of orbit) to the earth
        frame

        pos_orbit_frame: position vector in meters in the orbital frame.
        arg_of_pericenter: argument of pericenter of the specific orbit in rad.
        ra_of_asc_nod: right ascension of the ascending node of the specific
        orbit in rad.
        inclination: inclination of the specific orbit in rad.

        Returns the rotated position vector, now in the Earth's frame.
        """
        R = Rotation.from_euler(
            "zxz", [-ra_of_asc_node, -inclination, -arg_of_pericenter]
        )
        return R.as_matrix().dot(pos_orbit_frame)

    def new_position(self, time: float, object: Object) -> np.ndarray:
        """
        Calculate the position of an object at specific point in time

        time: time in seconds after object's epoch at which the position will
        computed.

        Returns the 3D position vector (in the Earth frame) of the object at
        the given time.
        """

        true_anomaly = self._calc_new_anomaly(
            time, object.epoch, object.mean_anomaly, object.semimajor_axis
        )
        pos_orbit_frame = (
            np.array([np.cos(true_anomaly), np.sin(true_anomaly), 0])
            * object.semimajor_axis
        )
        pos = self._rotate_to_earth_frame(
            pos_orbit_frame,
            object.arg_of_pericenter,
            object.ra_of_asc_node,
            object.inclination,
        )
        return pos

    def initialize_positions(self, objects: list[Object], epoch):
        """
        Initialize all objects in the given list to the same given epoch by
        adjusting object's true anomaly.

        objects: list of objects to be calibrated.
        epoch: desired Julian date in seconds.
        """

        for object in objects:
            initialized_anomaly = self._calc_new_anomaly(
                epoch, object.epoch, object.mean_anomaly, object.semimajor_axis
            )
            object.mean_anomaly = initialized_anomaly
            object.epoch = epoch

    def calc_all_positions(
        self, objects: list[Object], endtime, timestep, epoch=1635771601.0
    ):
        """
        Calculate the new positions of all objects by first initializing all
        positions and save the positions in a csv as "output.csv".

        objects: list of objects to be evaluated.
        endtime: how long you want the trial to be.
        timestep: the size of the steps in time.
        """
        self.initialize_positions(objects, epoch)
        datadict = defaultdict(list)
        self.initialize_positions(objects, 1635771601.0)

        for object in objects:
            for time in range(int(object.epoch), int(object.epoch + endtime), timestep):
                new_position = self.new_position(time, object)
                object.positions.append(new_position)

            datadict[object.norad_cat_id].append(object.positions)

        df = pd.DataFrame(datadict)
        df.to_csv("output.csv", index=False)

    def collision():
        pass
