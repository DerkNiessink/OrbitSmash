import numpy as np
from scipy.spatial.transform import Rotation
import pandas as pd
from collections import defaultdict
from itertools import combinations
from tqdm import tqdm
import pickle
import random
from numba import njit


""" ['EPOCH', 'INCLINATION', 'RA_OF_ASC_NODE', 'ARG_OF_PERICENTER',
       'MEAN_ANOMALY', 'NORAD_CAT_ID', 'SEMIMAJOR_AXIS', 'OBJECT_TYPE',
       'RCS_SIZE', 'LAUNCH_DATE', 'positions', 'subclass'] """

class Model:

    # standard gravitational parameter = G * M
    JD = 86400  # s
    mu = 6.6743 * 10**-11 * 5.972 * 10**24  # m**3 * s**-2
    max_norad_cat_id = 270288

    def __init__(self, objects): # wordt een numpy 
        self.objects = objects
        self.positions = tuple()
    

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

    def new_position(self, time: float, object) -> np.ndarray:
        """
        Calculate the position of an object at specific point in time

        time: time in seconds after object's epoch at which the position will
        computed.

        Returns the 3D position vector (in the Earth frame) of the object at
        the given time.
        """
        true_anomaly = self._calc_new_anomaly(
            time, object[0], object[4], object[6]
        )
        pos_orbit_frame = (
            np.array(
                [np.cos(np.deg2rad(true_anomaly)), np.sin(np.deg2rad(true_anomaly)), 0]
            )
            * object[6]
        )
        pos = self._rotate_to_earth_frame(
            pos_orbit_frame,
            object[3],
            object[2],
            object[1],
        )
        return pos

    def collision(self, collision_list):
        """ """

        # Create new debris

        if self._check_collosion == True:

            for collision in collision_list:

                for object in collision:

                    # object is nu debris
                    object[7] = "DEBRIS"

                    # aanpassen size
                    if object[8] == "MEDIUM":
                        object[8] = "SMALL"
                    elif object[8] == "LARGE":
                        object[8] == "MEDIUM"

                    # new id per new object
                    self.max_norad_cat_id += 1

                    # calculate new inclination
                    new_inclination = object[1] + random.sample(
                        [-3, -2, -1, 1, 2, 3]
                    )
                    if new_inclination > 180:
                        new_inclination -= 180
                    if new_inclination < 0:
                        new_inclination += 180

                    self.objects.append(
                            object[0],
                            new_inclination,
                            object[2],
                            object[3],
                            object[4],
                            self.max_norad_cat_id,
                            object[6],
                            object[7],
                            object[8],
                            object[9],
                            object[10])

        return

    def _check_collisions(self): # nog aanpassen 
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
            print(object1[10])
            if (bool(set(object1.octree) & set(object2.octree))) == True and str(
                np.isclose(
                    object1[10], object2[10], rtol=1e-09, atol=2.0
                )
            ) == "[True,  True,  True]":
                collision_list.append(combo)
                collisions = True

        self.collision(collision_list)
        return collisions

    def add_satellites(self, current_year, new_satellites=50):
        self.max_norad_cat_id += 1

        new_mean_anomaly = object[4] + 180
        if new_mean_anomaly > 360:
            new_mean_anomaly -= 360

        launch_date = current_year

        number_of_new_satellites = np.random.normal(
            loc=new_satellites, scale=new_satellites * 0.2
        )

        for _ in range(0, number_of_new_satellites):
            object = np.random.choice(self.objects)

            self.max_norad_cat_id += 1

            new_mean_anomaly = object[4] + 180
            if new_mean_anomaly > 360:
                new_mean_anomaly -= 360

            self.objects.append(
                            object[0],
                            object[1],
                            object[2],
                            object[3],
                            new_mean_anomaly,
                            self.max_norad_cat_id,
                            object[6],
                            object[7],
                            object[8],
                            launch_date, 
                            object[10])
               

    def remove_objects(self, time_removing, frequency=10, average_lifespan=20):

        deleted_objects = 0
        # nu moet de fequentie uit objectenlijst worden gehaald.
        for object in self.objects:
            try:
                if (
                    object[8] == "LARGE"
                    and (time_removing - object[9]) > average_lifespan
                    and deleted_objects < frequency
                ):
                    # delete this object x times
                    self.objects.remove(object)
                    deleted_objects += 1
            except:
                pass

        return

    def calc_all_positions(
        self, endtime, timestep, begin_year=2030, epoch=1635771601.0
    ):
        """
        Calculate the new positions of all objects by first initializing all
        positions and save the positions in a csv as "output.csv".

        objects: list of objects to be evaluated.
        endtime: how long you want the trial to be.
        timestep: the size of the steps in time.

        epoch: Monday 1 November 2021 13:00:01
        """

        time_removing = 2021
        for time in tqdm(np.arange(epoch, epoch + endtime, timestep), ncols=100):

            for object in self.objects:  # tqdm for progress bar.
                new_position = self.new_position(time, object)
                object[10] = tuple(new_position)

                # self._check_collisions()

                """ HIER KOMT REMOVE SATELLITE + NEW SATELLITE """
                # wordt elk jaar aangeroepen
                if time % 31556926 == 0:
                    if time_removing == begin_year:
                        self.remove_objects(time_removing)
                        self.add_satellites(time_removing)
                    time_removing += 1
                

        self.save_objects()

    def save_objects(self):
        """
        Save the objects as "output.dat" using pickles.
        """

        print("Saving output...")
        with open("output.dat", "wb") as f:
            for object in self.objects:
                pickle.dump(object, f)
