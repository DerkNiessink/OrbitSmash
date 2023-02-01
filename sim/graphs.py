import numpy as np
import csv
from data_cleaning import mean_semi_group
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib
from matplotlib.lines import Line2D


""" The code to make the first collision graph """
endtime = 31556926 * 0.01
timestep = 100
epoch = 1675209600

groups_100 = [3, 7, 8, 9, 14, 25, 26, 29, 34, 35, 37, 38, 39, 60, 63]

# build collisions_dict
collisions_dict = defaultdict(list)
for group in groups_100:
    with open(f"sim/data_storage/group_{group}/collisions.csv", "r") as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            collisions_dict[group].append(
                round((int(row[2]) - epoch) / (60 * 60 * 24 * 365.25), 5)
            )


# create color list
cmap = matplotlib.cm.get_cmap('gist_ncar')
x_list=np.linspace(0.1,0.9,4)
color_list=[]
for i in x_list:
    color_list.append(cmap(i))

# create color coded plot for each group
plt.clf()
custom_legend = []
for group in groups_100:
    if len(collisions_dict[group]) > 0:
        time = collisions_dict[group]
        number_of_collisions = [i for i in range(1, len(collisions_dict[group])+1)]

        # plot line
        plt.plot(time, number_of_collisions, '-o', color=color_list[0])

        custom_legend.append(Line2D([0], [0], marker='o', color='w', label=int(mean_semi_group['SEMIMAJOR_AXIS'][group]),
                          markerfacecolor=color_list[0], markersize=8))
                        
        color_list.remove(color_list[0])


# add legend outside of plot
plt.legend(handles=custom_legend, loc='upper left', fontsize=9, title="\u03B1 in meters")
plt.tight_layout()

plt.xlim(0,10)
plt.xticks(np.linspace(0,10,11))
plt.ylim(0,60)
plt.title("Amount of collisions with a margin of 100m")
plt.xlabel("Time in years")
plt.ylabel("Number of collisions")
plt.show()

""" Code to make thew second graph """
groups_700 = [1, 2, 4, 5, 6, 10, 11, 12, 13, 16, 17, 18, 20, 21, 22, 23, 24, 27, 28, 30, 31, 32, 33, 35, 37, 38, 39, 40, 41, 42, 46, 48, 52, 53, 57, 58]

# build the collisions_dict
collisions_dict = defaultdict(list)
for group in groups_700:
    with open(f"sim/data_storage/group_{group}/collisions.csv", "r") as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            collisions_dict[group].append(
                round((int(row[2]) - epoch) / (60 * 60 * 24 * 365.25), 5)
            )


# create color list
x_list=np.linspace(0.1,0.9,len(groups_700))
for i in x_list:
    color_list.append(cmap(i))

# create color coded plot for each group
plt.clf()
custom_legend=[]
for group in groups_700:
    if len(collisions_dict[group]) > 0:
        
        time = collisions_dict[group]
        number_of_collisions = [i for i in range(1, len(collisions_dict[group])+1)]

        # plot line
        plt.plot(time, number_of_collisions, '.', color=color_list[0])

        # create lines for legend
        custom_legend.append(Line2D([0], [0], marker='o', color='w', label=int(mean_semi_group['SEMIMAJOR_AXIS'][group]),
                          markerfacecolor=color_list[0], markersize=8))

    color_list.remove(color_list[0])

# add legend outside of plot
plt.legend(handles=custom_legend, bbox_to_anchor=(1.05, 1.0), loc='upper left', title="r in kilometer", fontsize=9)
plt.tight_layout()

plt.xlim(0,10)
plt.ylim(0,130)
plt.xticks(np.linspace(0,10,11))
plt.subplots_adjust(top=0.90, bottom=0.3)
plt.title("Amount of collisions with a margin of 700m", fontsize=20)
plt.xlabel("Time in years", fontsize=18)
plt.ylabel("Number of collisions", fontsize=18)
plt.show()