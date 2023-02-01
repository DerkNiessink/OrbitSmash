import sys
import numpy as np
from tqdm import tqdm
import csv
from data_cleaning import all_groups, mean_semi_group
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib


""" The code to make the first collision graph """
endtime = 31556926 * 0.01
timestep = 100
epoch = 1675209600

groups_100 = [3, 7, 8, 9, 14, 25, 26, 29, 34, 35, 37, 38, 39]

collisions_dict = defaultdict(list)
# for group in all_groups:
for group in groups_100:
    with open(f"sim/data_storage/group_{group}/collisions.csv", "r") as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            collisions_dict[group].append(
                round((int(row[2]) - epoch) / (60 * 60 * 24 * 365.25), 5)
            )

plt.clf()
color_list=['#FF006E', '#3A86FF', '#FFBE0B']
# for group in all_groups:
for group in groups_100:
    if len(collisions_dict[group]) > 0:
        time = collisions_dict[group]
        number_of_collisions = [i for i in range(1, len(collisions_dict[group])+1)]

        # plot line
        plt.plot(time, number_of_collisions, '-o', color=color_list[0])
        color_list.remove(color_list[0])



plt.title("Insert title")
plt.xlabel("Time")
plt.ylabel("Number of collisions")
plt.show()

""" Code to make thew second graph """
groups_700 = [1, 2, 4, 5, 6, 10, 11, 12, 13, 16, 17, 18, 20, 21, 22, 23, 24, 27, 28, 30, 31, 32, 33, 35, 37, 38, 39, 40, 41, 42, 46, 48, 52, 53, 57, 58]


collisions_dict = defaultdict(list)
# for group in all_groups:
for group in groups_700:
    with open(f"sim/data_storage/group_{group}/collisions.csv", "r") as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            collisions_dict[group].append(
                round((int(row[2]) - epoch) / (60 * 60 * 24 * 365.25), 5)
            )

plt.clf()
print(collisions_dict)

cmap = matplotlib.cm.get_cmap('gist_ncar')

x_list=np.linspace(0,1,len(groups_700))

for i in x_list:
    color_list.append(cmap(i))

# for group in all_groups:
for group in groups_700:
    if len(collisions_dict[group]) > 0:
        time = collisions_dict[group]
        number_of_collisions = [i for i in range(1, len(collisions_dict[group])+1)]

        # plot line
        plt.plot(time, number_of_collisions, c=color_list[0])
        ax = plt.subplot()
        im = ax.imshow(mean_semi_group.values())
    
    color_list.remove(color_list[0])


plt.colorbar(im, label="Semi-major axis", orientation="horizontal")





plt.title("Insert title")
plt.xlabel("Time")
plt.ylabel("Number of collisions")
plt.show()