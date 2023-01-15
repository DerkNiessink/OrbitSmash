import numpy as np
from scipy.spatial.transform import Rotation
import pandas as pd
from collections import defaultdict
from itertools import combinations
from tqdm import tqdm


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
        self.epoch = epoch  # time of mean_anomaly
        self.mean_motion = mean_motion
        self.eccentricity = eccentricity  # 1
        self.inclination = inclination  # rad
        self.ra_of_asc_node = ra_of_asc_node  # rad
        self.arg_of_pericenter = arg_of_pericenter  # rad
        self.mean_anomaly = mean_anomaly  # rad
        self.norad_cat_id = norad_cat_id
        self.semimajor_axis = (
            semimajor_axis  # meter, minimum = 654_285_0, maximum = 837_081_9
        )
        self.period = period
        self.apoapsis = apoapsis
        self.periapsis = periapsis
        self.object_type = object_type
        self.rcs_size = rcs_size
        self.country_code = country_code
        self.launch_date = launch_date
        self.octree = self.init_octree()

        self.positions = []

    def init_octree(
        self,
        subsections=[
            654_285_0,
            690_454_1,
            692_536_2,
            702_464_7,
            712_772_3,
            718_941_0,
            724_381_3,
            738_820_9,
            837_100_0,
        ],
        margin_perc=0.1,
    ) -> list:
        """
        Determine the orbit number of a specific object from a given list of
        subsections for the semi-major axis. If the semi-major axis of the
        object falls into the given margin of another section, say that the
        object falls into both sections.

        subsections: list of distances in meters that correspond to the
        boundaries of the subsectionsin meters.
        margin_perc: margin of specific subsection, the object falls also
        into the adjacent section.

        returns a list of the orbit number(s) which are numbers between 0 and
        len(subsections).
        """
        # a 10% margin of the subsections
        differences = np.diff(subsections)

        all_orbit_numbers = [i for i in range(len(subsections))]
        margin = differences * margin_perc

        orbit_n = []
        for i in range(len(differences)):

            if self.semimajor_axis > subsections[i] - margin[
                i
            ] and self.semimajor_axis < (subsections[i] + differences[i] + margin[i]):

                orbit_n.append(all_orbit_numbers[i])

        return orbit_n


class Model:

    # standard gravitational parameter = G * M
    JD = 86400  # s
    mu = 6.6743 * 10**-11 * 5.972 * 10**24  # m**3 * s**-2

    def __init__(self, objects: list[Object]):
        self.objects = objects

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
            "zxz", [-ra_of_asc_node, -inclination, -arg_of_pericenter], degrees=True
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
            np.array(
                [np.cos(np.deg2rad(true_anomaly)), np.sin(np.deg2rad(true_anomaly)), 0]
            )
            * object.semimajor_axis
        )
        pos = self._rotate_to_earth_frame(
            pos_orbit_frame,
            object.arg_of_pericenter,
            object.ra_of_asc_node,
            object.inclination,
        )
        return pos

    def initialize_positions(self, epoch):
        """
        Initialize all objects in the given list to the same given epoch by
        adjusting object's true anomaly.

        objects: list of objects to be calibrated.
        epoch: desired Julian date in seconds.
        """
        for object in self.objects:
            initialized_anomaly = self._calc_new_anomaly(
                epoch, object.epoch, object.mean_anomaly, object.semimajor_axis
            )
            object.mean_anomaly = initialized_anomaly
            object.epoch = epoch

    def collision(self, collision_list):
        # Create new debris

        pass

    def _check_collisions(self):
        """
        Checks for collisions by iterating over all possible combinations,
        checking if the objects in the combination share a similar orbit. If
        this is the case their closeness will be checked. In the case of a
        collision the involved bodies will be added to a list.

        objects: list of all objects to be evaluated for colliding.
        """
        collision_list, collisions = [], False
        for combo in combinations(self.objects, 2):
            object1, object2 = combo
            print(object1.positions)
            if (bool(set(object1.octree) & set(object2.octree))) == True and str(
                np.isclose(
                    object1.positions[-1], object2.positions[-1], rtol=1e-09, atol=2.0
                )
            ) == "[True,  True,  True]":
                collision_list.append(combo)
                collisions = True

        self.collision(collision_list)
        return collisions

    def calc_all_positions(self, endtime, timestep, epoch=1635771601.0):
        """
        Calculate the new positions of all objects by first initializing all
        positions and save the positions in a csv as "output.csv".

        objects: list of objects to be evaluated.
        endtime: how long you want the trial to be.
        timestep: the size of the steps in time.
        """
        self.initialize_positions(epoch)
        datadict = defaultdict(list)

        for object in tqdm(self.objects, ncols=100):
            # tqdm for progress bar.

            for time in np.arange(epoch, epoch + endtime, timestep):
                new_position = self.new_position(time, object)
                object.positions.append(tuple(new_position))

            # self._check_collisions()
            datadict[object.norad_cat_id].append(object.positions)

        print("Saving output...")
        df = pd.DataFrame(datadict)
        df.to_csv("output.csv", index=False)
