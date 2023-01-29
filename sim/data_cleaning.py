import pandas as pd
import numpy as np
import datetime
from scipy.spatial.transform import Rotation
import os


dataset = pd.read_csv("../data/satellites.csv")

# removing irrelevant columns
dataset = dataset.drop(
    columns=[
        "CCSDS_OMM_VERS",
        "COMMENT",
        "CREATION_DATE",
        "ORIGINATOR",
        "OBJECT_NAME",
        "OBJECT_ID",
        "CENTER_NAME",
        "REF_FRAME",
        "TIME_SYSTEM",
        "MEAN_ELEMENT_THEORY",
        "EPHEMERIS_TYPE",
        "CLASSIFICATION_TYPE",
        "ELEMENT_SET_NO",
        "REV_AT_EPOCH",
        "BSTAR",
        "MEAN_MOTION_DOT",
        "MEAN_MOTION_DDOT",
        "SITE",
        "DECAY_DATE",
        "FILE",
        "GP_ID",
        "TLE_LINE0",
        "TLE_LINE1",
        "TLE_LINE2",
        "ECCENTRICITY",
        "MEAN_MOTION",
        "PERIOD",
        "APOAPSIS",
        "PERIAPSIS",
        "COUNTRY_CODE",
    ]
)


def epoch(df_column):
    date_list = list(df_column)
    new_date_list = []

    for data in date_list:
        date, time = data.split("T")
        year, month, day = date.split("-")
        hour, minute, second = time.split(":")
        second = second[0:2]

        new_date_list.append(
            datetime.datetime(
                int(year), int(month), int(day), int(hour), int(minute), int(second)
            ).timestamp()
        )

    return new_date_list


# only selecting data in LEO
dataset = dataset.sort_values("SEMIMAJOR_AXIS")
dataset = dataset[dataset["SEMIMAJOR_AXIS"] < 8371]
dataset["MEAN_ANOMALY"] = dataset["MEAN_ANOMALY"] * np.pi / 180
dataset["EPOCH"] = epoch(dataset["EPOCH"])
dataset["tuples"] = [(0, 0, 0) for i in range(len(dataset.index))]
dataset["SEMIMAJOR_AXIS"] = dataset["SEMIMAJOR_AXIS"].apply(
    lambda x: x * 1000
)  # Convert to meters

matrices = []
for index, row in dataset.iterrows():
    R = Rotation.from_euler(
        "zxz",
        [-row["RA_OF_ASC_NODE"], -row["INCLINATION"], -row["ARG_OF_PERICENTER"]],
        degrees=True,
    )
    matrices.append(R.as_matrix())

dataset["rotation_matrix"] = matrices


""" MAKING GROUPS """
linspace = np.linspace(
    min(dataset["SEMIMAJOR_AXIS"]), max(dataset["SEMIMAJOR_AXIS"]), num=100
)
bins = np.digitize(np.array(dataset["SEMIMAJOR_AXIS"]), linspace, right=False)
dataset["groups"] = bins


subgroups = dataset.loc[dataset["groups"].isin([i for i in range(17, 42)])]
linspace_sub = np.linspace(
    min(subgroups["SEMIMAJOR_AXIS"]), max(subgroups["SEMIMAJOR_AXIS"]), num=100
)
bins_sub = np.digitize(np.array(subgroups["SEMIMAJOR_AXIS"]), linspace_sub, right=False)
subgroups_ = subgroups.copy()
subgroups_["groups"] = bins_sub


dataset = subgroups_.loc[subgroups_["groups"] != 19]
# linspace_21 = np.linspace(
#     min(group_21["SEMIMAJOR_AXIS"]), max(group_21["SEMIMAJOR_AXIS"]), num=20
# )
# bins21 = (np.digitize(np.array(group_21["SEMIMAJOR_AXIS"]), linspace_21, right=False) * 0.05) + 21
# group_21['groups'] = bins21
# print(group_21.groupby("groups")["groups"].count())
# dataset = dataset.loc[dataset['groups'] != 21]
# dataset = dataset.append(group_21, ignore_index=True)


small_group = dataset.groupby("groups")["groups"].count() != 1
delete = list(small_group.loc[small_group == False].index)

# the groups that have no debris
grouped = dataset.groupby("groups")
debris_groups = grouped.filter(
    lambda x: all(x["OBJECT_TYPE"].isin(["TBA", "ROCKET BODY", "PAYLOAD"]))
)


no_debris = []
for i in set(debris_groups["groups"]):
    no_debris.append(i)

delete.extend(no_debris)


dataset = dataset[~dataset["groups"].isin(delete)]
group_amount = dataset.groupby("groups")["groups"].count()


data_debris = dataset.loc[dataset["OBJECT_TYPE"] == "DEBRIS"]

all_groups = []
for i in group_amount.index:
    all_groups.append(i)
    if not os.path.exists(f"data_storage/group_{i}"):
        os.makedirs(f"data_storage/group_{i}", exist_ok=True)

# Dataset to numpy array
data_array = dataset.to_numpy()
data_array_debris = data_debris.to_numpy()

group_selection = data_array[:, 12] == 8
group_selection_debris = data_array_debris[:, 12] == 8

data_array_group = data_array[group_selection]
data_array_debris_group = data_array_debris[group_selection_debris]
