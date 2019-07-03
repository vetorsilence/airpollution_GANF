# description ...

##

# Import Libraries and class

import pandas as pd
import numpy as np
import preprocessing.importClass
from preprocessing.importClass import Point, Coord, Bounding_box, station
##

# Read Data

bb_aq_stations = pd.read_csv('data/aq_grids_csv.csv')
bb_meo_stations = pd.read_csv('data/meo_grids_csv.csv')
coord_aq_stations = pd.read_csv('data/aq_stations_csv.csv')
coord_meo_stations = pd.read_csv('data/meo_stations_csv.csv')
point_centroids = pd.read_csv('data/centroids_aq_csv.csv')
aq_data = pd.read_csv('data/beijing_17_18_aq.csv')
meo_data = pd.read_csv('data/beijing_17_18_meo.csv')

##

# separate date and time

aq_data['utc_time'] = pd.to_datetime(aq_data['utc_time'], utc=True)

aq_data['date'] = [d.date() for d in aq_data['utc_time']]
aq_data['time'] = [t.time() for t in aq_data['utc_time']]

del aq_data['utc_time']

aq_data['date'] = pd.to_datetime(aq_data['date'],utc=True)
aq_data['date'] = aq_data['date'].dt.date
aq_data['date'] = aq_data['date'].astype('datetime64[D]')

aq_data['time'] = pd.to_datetime(aq_data['time'],format= '%H:%M:%S' ).dt.hour
aq_data['time'] = aq_data['time'].astype(int)

##

meo_data['utc_time'] = pd.to_datetime(meo_data['utc_time'], utc=True)

meo_data['date'] = [d.date() for d in meo_data['utc_time']]
meo_data['time'] = [t.time() for t in meo_data['utc_time']]

del meo_data['utc_time']

meo_data['date'] = pd.to_datetime(meo_data['date'],utc=True)
meo_data['date'] = meo_data['date'].dt.date
meo_data['date'] = meo_data['date'].astype('datetime64[D]')

meo_data['time'] = pd.to_datetime(meo_data['time'],format= '%H:%M:%S' ).dt.hour
meo_data['time'] = meo_data['time'].astype(int)

##

# Considering only 60 days

# Air quality data

aq_data['stationId'], b = pd.factorize(aq_data['stationId'])

start_date = pd.to_datetime('2017-02-28',utc=True).date()
end_date = pd.to_datetime('2017-04-30',utc=True).date()
mask = (aq_data['date'] > start_date) & (aq_data['date'] <= end_date)
aq_data_60 = aq_data.loc[mask]

# Meteorological data

meo_data['station_id'], b = pd.factorize(meo_data['station_id'])

mask = (meo_data['date'] > start_date) & (meo_data['date'] <= end_date)
meo_data_60 = meo_data.loc[mask]

##
meo_data_60.reset_index()

##

# Days without meteorological data ignore

count = 0
station_ignore = []
date_ignore = []
time_ignore = []
for i in range(0,len(meo_data_60)):
    if(meo_data_60.iloc[i,10] != count):
        station_ignore.append(meo_data_60.iloc[i,0])
        date_ignore.append(meo_data_60.iloc[i,9])
        time_ignore.append(meo_data_60.iloc[i,10])
        print( meo_data_60.iloc[i,0],meo_data_60.iloc[i,9] , " ", meo_data_60.iloc[i,10])
        count += 1
    count += 1
    if(count > 23):
        count = 0

##

# Description data

# Air Quality data
aq_data.describe()

# Meteorological data
meo_data.describe()


##

# Preprocessing

# Air Quality data

# Clean redundant data (same datetime)


used_times = []
count = 0
for i in range(0, len(aq_data)):
    count+=1
    current_time = aq_data.loc[i]['utc_time']
    if current_time not in used_times:
        used_times.append(current_time)
    else:
        aq_data.drop(index=i,columns='utc_time')
    print(count)

# NAN and 9991 to 0
aq_data.replace()
aq_data.fillna(0.0)

##
aq_data.describe()
#
##

# Meteorological data
meo_data['utc_time'] = pd.to_datetime(meo_data['utc_time'], utc=True)

used_times = []
count = 0
for i in range(0, len(meo_data)):
    count+=1
    current_time = meo_data.loc[i]['utc_time']
    if current_time not in used_times:
        used_times.append(current_time)
    else:
        meo_data.drop(index=i,columns='utc_time')
    print(count)
