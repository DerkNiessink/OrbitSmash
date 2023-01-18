import numpy as np
import random
from numba import jit


"""

"objects" =
['EPOCH' (0), 'INCLINATION' (1), 'RA_OF_ASC_NODE' (2), 'ARG_OF_PERICENTER' (3),
       'MEAN_ANOMALY' (4), 'NORAD_CAT_ID' (5), 'SEMIMAJOR_AXIS' (6), 'OBJECT_TYPE' (7),
       'RCS_SIZE' (8), 'LAUNCH_DATE' (9), 'positions' (10), 'rotation_matrix' (11), 'groups' (12)]

"objects_fast" =
['EPOCH', 'MEAN_ANOMALY', 'SEMIMAJOR_AXIS', 'pos_x', pos_y', 'pos_z']

"""


JD = 86400  # s
# standard gravitational parameter = G * M
mu = 6.6743 * 10**-11 * 5.972 * 10**24  # m**3 * s**-2
max_norad_cat_id = 270288


def initialize_positions(objects: np.ndarray, epoch: float):
    """
    Initialize all objects in the given array to the same given epoch by
    adjusting object's true anomaly.

    objects: array of objects to be calibrated.
    epoch: desired Julian date in seconds (Monday 1 November 2021 13:00:01).
    """
    for object in objects:
        initialized_anomaly = calc_new_anomaly(epoch, object[0], object[4], object[6])
        object[4] = initialized_anomaly
        object[0] = epoch


@jit(nopython=True)
def calc_new_anomaly(
    time: float, epoch: float, mean_anomaly: float, semimajor_axis: float
) -> float:
    """
    Calculate the new anomaly of an object at a specific Julian date in
    seconds.

    time: Julian date in seconds of the desired anomaly.
    epoch: Julian date in seconds.
    mean_anomaly: anomaly corresponding to the object's epoch in rad.
    semimajor_axis: semimajor-axis of the object's orbit in meters.
    """
    time_delta = time - epoch  # s
    return mean_anomaly + time_delta * np.sqrt(mu / semimajor_axis**3)


@jit(nopython=True)
def new_position(
    time: float,
    epoch: float,
    mean_anomaly: float,
    semimajor_axis: float,
    rotation_matrix: np.ndarray,
) -> np.ndarray:
    """
    Calculate the position of an object at specific point in time

    time: time in seconds after object's epoch at which the position will
    computed.
    epoch: time corresponding to the mean anomaly of the object.
    mean_anomaly: anomaly in rad corresponding to the time.
    semimajor_axis: semimajor axis of the orbit.
    rotation_matrix: rotation matrix computed from the 3 orbital angles.

    Returns the 3D position vector (in the Earth frame) of the object at
    the given time.
    """
    time_delta = time - epoch  # s
    true_anomaly = mean_anomaly + time_delta * np.sqrt(mu / semimajor_axis**3)

    pos_orbit_frame = (
        np.array([np.cos(true_anomaly), np.sin(true_anomaly), 0]) * semimajor_axis
    )

    return rotation_matrix.dot(pos_orbit_frame)


@jit(nopython=True)
def calc_all_positions(
    objects: np.ndarray, matrices: np.ndarray, time: float
) -> np.ndarray:
    """
    Calculate the new positions of all objects.

    objects: array of objects to be evaluated, which has to be in following form
     -> ['EPOCH', 'MEAN_ANOMALY', 'SEMIMAJOR_AXIS', 'pos_x', pos_y', 'pos_z']
    marices: array of rotation matrices of the objects computed from the 3
    orbital angles.
    time: time at which the positions will be calculated.
    """
    for i in range(len(objects)):

        pos = new_position(
            time,
            epoch=objects[i][0],
            mean_anomaly=objects[i][1],
            semimajor_axis=objects[i][2],
            rotation_matrix=matrices[i],
        )
        objects[i][3], objects[i][4], objects[i][5] = (
            pos[0],
            pos[1],
            pos[2],
        )

        """
        HIER KOMT REMOVE SATELLITE + NEW SATELLITE
        # wordt elk jaar aangeroepen
        time_removing = 2021
        if time % 31556926 == 0:
            if time_removing == begin_year:
                self.remove_objects(time_removing)
                self.add_satellites(time_removing)
            time_removing += 1
        """


@jit(nopython=True)
def check_collisions(objects: np.ndarray, margin=100.0):
    """
    Checks for collisions by iterating over all possible combinations,
    by checking if the objects in the combination share a similar position.

    objects: array of objects to be evaluated, which has to be in following form
     -> ['EPOCH', 'MEAN_ANOMALY', 'SEMIMAJOR_AXIS', 'pos_x', pos_y', 'pos_z']
    margin: say that there could be a collision when difference off the x, y
    and z coordinates is smaller than this margin.

    returns a generator of tuples of the two candidate colliding objects.
    """

    for i in range(len(objects) - 1):
        for j in range(i + 1, len(objects)):

            pos1 = np.array([objects[i][3], objects[i][4], objects[i][5]])
            pos2 = np.array([objects[j][3], objects[j][4], objects[j][5]])

            if np.linalg.norm(pos1 - pos2) < margin:
                return (objects[i], objects[j])


def zoom_collision(objects: np.ndarray, epoch, margin=1000):
    pass


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
                new_inclination = object[1] + random.sample([-3, -2, -1, 1, 2, 3])
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
                    object[10],
                )


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
            object[10],
        )


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
