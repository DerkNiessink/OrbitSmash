import numpy as np
from collections import defaultdict

def octree(objects = [6904, 7120, 8000] , subsections = [6542.85, 6904.541, 6925.362, 7024.647, 7127.723, 7189.41, 7243.813, 7388.209], marge = 0.1):
    
    subsections.append(8371)
    # a 10% margin of the subsections 
    differance = np.diff(subsections) 

    subclass = [i for i in range(8)]
    margin = differance * marge
   
    classes = []
    for object in objects: 
        for i in range(len(differance)):
            if object > subsections[i] - margin[i] and object < (subsections[i] + differance[i] + margin[i]):
                classes.append(subclass[i])
        object.semimajor_axis = classes
    return 

x = np.arange(35).reshape(5, 7)
print(x)
b = x[:,6] == 20
print(x[b])
