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

# Description data

# Air Quality data
aq_data.describe()

# Meteorological data
meo_data.describe()

##

# Preprocessing

# Clean redundant data (same datetime)


