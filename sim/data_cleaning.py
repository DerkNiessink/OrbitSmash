import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np 

dataset = pd.read_csv('data/satellites.csv')

# removing irrelevant columns 
dataset = dataset.drop(columns=['CCSDS_OMM_VERS', 'COMMENT', 'CREATION_DATE', 'ORIGINATOR', 'OBJECT_NAME', 'OBJECT_ID', 'CENTER_NAME', 
                        'REF_FRAME', 'TIME_SYSTEM', 'MEAN_ELEMENT_THEORY', 'EPHEMERIS_TYPE', 'CLASSIFICATION_TYPE', 'ELEMENT_SET_NO', 
                        'REV_AT_EPOCH', 'BSTAR', 'MEAN_MOTION_DOT', 'MEAN_MOTION_DDOT', 'SITE', 'DECAY_DATE', 'FILE', 'GP_ID', 
                        'TLE_LINE0', 'TLE_LINE1', 'TLE_LINE2', 'ECCENTRICITY', 'MEAN_MOTION','PERIOD', 'APOAPSIS', 'PERIAPSIS',
                        'COUNTRY_CODE' ])

def epoch(df_column):
    date_list = list(df_column) 
    new_date_list = []

    for data in date_list:
        date, time = data.split('T')
        year, month, day = date.split('-')
        hour, minute, second = time.split(':')
        second = second[0:2]

        new_date_list.append(datetime.datetime(int(year), int(month), int(day), int(hour), 
        int(minute), int(second)).timestamp())

    return new_date_list

# only selecting data in LEO 
dataset = dataset[dataset['SEMIMAJOR_AXIS'] < 8371]
dataset['EPOCH'] = epoch(dataset['EPOCH'])
dataset['tuples'] = [(0,0,0) for i in range(len(dataset.index))]


# Dataset to numpy array
data_array = dataset.to_numpy()




