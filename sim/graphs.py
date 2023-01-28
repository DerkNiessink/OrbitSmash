import sys
import numpy as np
from tqdm import tqdm
import csv
from data_cleaning import all_groups
import matplotlib.pyplot as plt
from collections import defaultdict


""" The code to make the first collision graph """
endtime = 31556926 *0.01
timestep = 100
epoch = 1675209600

collisions_dict = defaultdict(list)
#for group in all_groups:
for group in range(1,13):
    with open(f"sim/data_storage/group_{group}/collisions.csv", 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            collisions_dict[group].append(round((int(row[2]) - epoch) / (60 * 60 * 24), 5))

#for group in all_groups:
for group in range(1,13):
    time = collisions_dict[group]
    number_of_collisions = [i for i in range(len(collisions_dict[group]))]
  
    # plot line
    plt.plot(time,number_of_collisions, color = '#838B8B')

plt.title('Insert title')
plt.xlabel('Time')
plt.ylabel('Number of collisions')
plt.show()

""" Code to make thew second graph """
    