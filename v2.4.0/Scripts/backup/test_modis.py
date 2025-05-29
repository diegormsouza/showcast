#######################################################################################################
# LICENSE
# Copyright (C) 2021 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU 
# General Public License as published by the Free Software Foundation, either version 3 of the License, 
# or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without 
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General 
# Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. 
# If not, see http://www.gnu.org/licenses/.
#######################################################################################################
__author__ = "Diego Souza"
__copyright__ = "Copyright (C) 2021 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL"
__credits__ = ["Diego Souza"]
__license__ = "GPL"
__version__ = "2.3.0"
__maintainer__ = "Diego Souza"
__email__ = "diego.souza@inpe.br"
__status__ = "Production"
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Required modules
#--------------------------------
#to run in a pure text terminal:
import matplotlib
matplotlib.use('Agg')
#--------------------------------
import numpy as np                                           # Import the Numpy package
import os 									                 # Miscellaneous operating system interfaces
from os.path import dirname, abspath                         # Return a normalized absolutized version of the pathname path 
import sys                                                   # Import the "system specific parameters and functions" module
import matplotlib.colors                                     # Matplotlib colors
import cartopy, cartopy.crs as ccrs                          # Plot maps
import cartopy.io.shapereader as shpreader                   # Import shapefiles
import matplotlib.pyplot as plt                              # Plotting library
import time as t                                             # Time access and conversion
from matplotlib.image import imread                          # Read an image from a file into an array
from cartopy.feature.nightshade import Nightshade            # Draws a polygon where there is no sunlight for the given datetime.
from html_update import update                               # Update the HTML animation 
from mpl_toolkits.axes_grid1.inset_locator import inset_axes # Add a child inset axes to this existing axes.
from osgeo import gdal, osr, ogr                             # Import GDAL
from pyhdf.SD import SD, SDC                                 # Import the HDF library
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
# Ignore possible warnings
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Reading the file:
path = "MOD14.A2021085.0315.006.2021085095713.hdf"
file = SD(path, SDC.READ)

# Printing all the datasets names
datasets_dic = file.datasets()
for idx,sds in enumerate(datasets_dic.keys()):
    print (idx,sds)
    
# Reading the dataset
sds_obj = file.select('fire mask') # select sds  
data = sds_obj.get()               # get sds data

# Check the dimensions
print(data.shape)






'''
sds_obj = file.select('Time_Mean')

time = sds_obj.get()
#print(time.shape)
#print(time [0][0])
add_seconds = time[0][0]
# Datetime of image scan
date_partial = datetime(1993, 1, 1, 00) + timedelta(seconds=add_seconds)
date_partial = (date_partial.strftime('%Y%m%d'))
#print(date_partial)
time = (path[path.find(".E")+2:path.find(".he4")])
time = time [5:9]
#print(time)
date = date_partial + time
date_formated = date[0:4] + "-" + date[4:6] + "-" + date[6:8] + " " + date [8:10] + ":" + date [10:12] + " UTC"
date_file = date
product = (path[path.find("COMP.")+5:path.find(".S")])

if (product == "TPW"):
    
elif (product == "PCT"):
'''