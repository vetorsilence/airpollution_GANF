# description ...

##

# Import Libraries and class

import pandas as pd
import numpy as np

from preprocessing.Station import Station
from preprocessing.Point import Point
from preprocessing.Coord import Coord
from preprocessing.Bounding_box import Bounding_box

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

# Reset index and nan = 0

meo_data_60.reset_index()
aq_data_60.reset_index()
aq_data_60.fillna(0.0)
meo_data_60.fillna(0.0)
##

# Times without meteorological data is ignore

count = 0
station_ignore = []
date_ignore = []
time_ignore = []
for i in range(0,len(meo_data_60)):
    if(meo_data_60.iloc[i,10] != count):
        station_ignore.append(meo_data_60.iloc[i,0])
        date_ignore.append(meo_data_60.iloc[i,9])
        time_ignore.append(count)
        print( meo_data_60.iloc[i,0],meo_data_60.iloc[i,9] , " ", count)
        count += 1
    count += 1
    if(count > 23):
        count = 0

##

# Times without pollutants

count = 0
for i in range(0,len(aq_data_60)):
    if(aq_data_60.iloc[i,8] != count):
        print( aq_data_60.iloc[i,0],aq_data_60.iloc[i,7] , " ", count)
        count += 1
    count += 1
    if(count > 23):
        count = 0


##

# values > 1000.0 = 0.0

# Air Quality data

for i in range(0,len(aq_data_60)):
    for j in range(1,len(aq_data_60.columns)-2):
        if(aq_data_60.iloc[i,j] >= 1000.0):
            aq_data_60.iloc[i,j] = 0.0

described_aq = aq_data_60.describe()

print(described_aq)

##

# Meteorological values > = 999000 = 0.0

# Meteorological data

for i in range(0,len(meo_data_60)):
    for j in range(1,len(meo_data_60.columns)-3):
        if(meo_data_60.iloc[i,j] >= 999000.0):
            meo_data_60.iloc[i,j] = 0.0

described_meo = meo_data_60.describe()

print(described_aq)

##

# Convert coordinates meteorological to points

meo_points = []
for i in range(0, len(coord_meo_stations)):
    coord = Coord(coord_meo_stations.iloc[i, 0], coord_meo_stations.iloc[i, 1])
    x, y  = coord.convertToPoint()
    meo_point = Point(x, y)
    meo_points.append(meo_point)
##

# Find bounding boxes where there is a meteorological data

meo_rect_meteorological = []
for j in range(0, len(bb_meo_stations)):
    meo_rect = Bounding_box(j,6,Point(bb_meo_stations.iloc[j, 0], bb_meo_stations.iloc[j, 1]),Point(bb_meo_stations.iloc[j, 2], bb_meo_stations.iloc[j, 3]))
    for meo_point in meo_points:
        print(meo_point.x, meo_point.y)
        if(meo_point.isWithinBB(meo_rect)):
            meo_rect_meteorological.append(meo_rect)

##

# there aren't stations - centroids

for i in range(0, len(bb_aq_stations)):
    rect = Bounding_box(i,2,Point(bb_aq_stations.loc[i, 0], bb_aq_stations.loc[i, 1]), Point(bb_aq_stations.loc[i, 2], bb_aq_stations.loc[i, 3]))
    x_c, y_c = rect.getCenter()
    center = Point(x_c, y_c)

    if center.isWithinBB():


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

##

