import numpy as np 

x = np.array([[1,2,3], [4,5,6]])
print(x[0][2])

""" Data opslaan """

parameters = {'group': int(), 'epoch': int(), 'endtime': int(), 'timestep':int(), 
            'probabilty': float(), 'precentage': int()}
parameters = {'group': objects[0][12], 'epoch': epoch, 'endtime' : endtime, 'timestep':timestep, 
'probabilty': probability , 'precentage' : percentage}
with open('parameters.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(data)