import numpy as np
from numba import jit, njit

from scipy.spatial.transform import Rotation


"""

"objects" =
['EPOCH' (0), 'INCLINATION' (1), 'RA_OF_ASC_NODE' (2), 'ARG_OF_PERICENTER' (3),
       'MEAN_ANOMALY' (4), 'NORAD_CAT_ID' (5), 'SEMIMAJOR_AXIS' (6), 'OBJECT_TYPE' (7),
       'RCS_SIZE' (8), 'LAUNCH_DATE' (9), 'positions' (10), 'rotation_matrix' (11), 'groups' (12)]

"objects_fast" =
['EPOCH' (0), 'MEAN_ANOMALY' (1), 'SEMIMAJOR_AXIS' (2), 'SATTELITE/DEBRIS'(3), 'pos_x' (4), pos_y' (5), 'pos_z' (6)]

"""

""" PARAMETERS 
    Hier kunnen we een lijstje parameters maken die we willen opslaan tijdens het runnen.
    Bijv:

    collisions = {'objects': [object1, object2], 'timestep': float}
    new_debris = {'timestep': float, 'number of new debris': 'int'}
    parameters = ['group', 'epoch', 'endtime', 'timestep', 'probabilty', 'percentage']
    etc. 
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


def random_debris(
    objects: np.ndarray,
    matrices: np.ndarray,
    time: float,
    percentage: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:

    """
    Add a certain amount, given by the percentage of the existing debris, of
    debris with random orbits and positions. The new debris is added to the
    objects and debris arrays and its random rotation matrix to matrices.

    objects: np.array of all objects (including debris).
    debris: np.array of all debris.
    matrices: np.array of all rotation matrices of the objects.
    time: current simulation times.
    percentage: desired percentage of the number of existing objects to add.

    Returns a tuple of the new objects, debris and matrices arrays.
    """

    n_new_debris = np.ceil(len(objects) * (percentage / 100))

    for _ in range(int(n_new_debris)):
        mean_anomaly, semimajor_axis, matrix = random_params(objects)
        matrices = np.append(matrices, matrix, axis=0)
        pos = new_position(time, time + 1, mean_anomaly, semimajor_axis, matrices[-1])
        new_debris = np.array(
            [[time, mean_anomaly, semimajor_axis, 1, pos[0], pos[1], pos[2]]]
        )
        
        objects = np.append(objects, new_debris, axis=0)
    return objects, matrices, int(n_new_debris)


def random_params(objects) -> tuple:
    """Returns random object parameters"""
    R = Rotation.from_euler(
        "zxz",
        [
            -np.random.uniform(0, 360),
            -np.random.normal(0, 360),
            -np.random.uniform(0, 360),
        ],
        degrees=True,
    )
    mean_anomaly = np.random.uniform(0, 360)
    semimajor_axis = objects[np.random.randint(len(objects))][2]
    return mean_anomaly, semimajor_axis, np.array([R.as_matrix()])


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

    objects: array of objects to be evaluated. An objects has to be in the
    following form:
     -> ['EPOCH', 'MEAN_ANOMALY', 'SEMIMAJOR_AXIS', 'object_bool', 'pos_x', pos_y', 'pos_z']
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
        objects[i][4], objects[i][5], objects[i][6] = (
            pos[0],
            pos[1],
            pos[2],
        )


@jit(nopython=True)
def check_collisions(objects: np.ndarray, margin: float):
    """
    Checks for collisions by iterating over all possible combinations,
    by checking if the objects in the combination share a similar position.

    objects: array of objects to be evaluated. An object has to be in the
    following form:
     -> ['EPOCH', 'MEAN_ANOMALY', 'SEMIMAJOR_AXIS', 'pos_x', pos_y', 'pos_z']
    margin: say that there could be a collision when difference of the x, y
    and z coordinates is smaller than this margin.

    returns a generator of tuples of the two candidate colliding objects.
    """
    for i in range(len(objects) - 1):
        for j in range(i+1, len(objects) - 1):
            if objects[i][3]!=0 and objects[j][3]!=0:
                pos1 = np.array([objects[i][4], objects[i][5], objects[i][6]])
                pos2 = np.array([objects[j][4], objects[j][5], objects[j][6]])
                if np.linalg.norm(pos1 - pos2) < margin:
                    #print("boom")
                    return objects[i], objects[j]


@jit(nopython=True)
def collision(object1: np.ndarray, object2: np.ndarray):
    """
    Add two new objects at the positions of the two objects involved in a
    collision with a slightly adjusted inclination.

    object_involved: np.array of the object to be evaluated and has to be in the
    following form:
     -> ['EPOCH' (0), 'MEAN_ANOMALY' (1), 'SEMIMAJOR_AXIS' (2), 'SATTELITE/DEBRIS'(3), 'pos_x' (4), pos_y' (5), 'pos_z' (6)]

    Returns a copy of the objects with the 2 new objects appended.
    """
    new_debris = list()
    # Create new debris

    # calculate new inclination
    g = np.random.rand()
    new_semi_major_axis = object1[2] + ((g * 200) - 100)

    new_mean_anomaly = object1[1]+180
    if new_mean_anomaly > 360:
        new_mean_anomaly -= 360

    new_debris.append(
        [(object1[0]+object2[0])/2, new_mean_anomaly, new_semi_major_axis, 1, -object1[4], -object1[5], -object1[6]]
    )

    return new_debris
