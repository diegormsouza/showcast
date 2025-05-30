#######################################################################################################
# LICENSE
# Copyright (C) 2019 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU 
# General Public License as published by the Free Software Foundation, either version 3 of the License, 
# or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without 
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General 
# Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. 
# If not, see http://www.gnu.org/licenses/.
#######################################################################################################
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Required modules
from netCDF4 import Dataset                                  # Read / Write NetCDF4 files
from mpl_toolkits.axes_grid1.inset_locator import inset_axes # Add a child inset axes to this existing axes.
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
from cpt_convert import loadCPT                              # Import the CPT convert function
from matplotlib.colors import LinearSegmentedColormap        # Linear interpolation for color maps
import matplotlib.pyplot as plt                              # Plotting library
import matplotlib.colors                                     # Matplotlib colors
import numpy as np                                           # Scientific computing with Python
import cartopy, cartopy.crs as ccrs                          # Plot maps
import cartopy.io.shapereader as shpreader                   # Import shapefiles
import time as t                                             # Time access and conversion
from osgeo import gdal, osr, ogr                             # Import GDAL
import os                                                    # Miscellaneous operating system interfaces
import sys                                                   # Import the "system specific parameters and functions" module
from html_update import update                               # Update the HTML animation 
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()
 
# Read the image
file = (sys.argv[1])
#file = "..//Samples//G16_ARMS07_201910211730.tif"
#file = "..//Samples//G16_CLPS07_201910211730.tif"
#file = "..//Samples//G16_CONS07_201910211730.tif"
#file = "..//Samples//G16_DCPS07_201910211730.tif"
#file = "..//Samples//G16_DLCS07_201910211730.tif"
#file = "..//Samples//G16_DMPS07_201910211730.tif"
#file = "..//Samples//G16_DSTS07_201910211730.tif"
#file = "..//Samples//G16_NMPS07_201910211730.tif"
#file = "..//Samples//G16_NTCS07_201910211730.tif"

# For the log
path = file

# File name
file_name = os.path.splitext(os.path.basename(file))[0]

# Read the satellite 
satellite = "G16"

# Get times and dates
product = file_name[4:7] + "RGB"

# Create the satellite output directory if it doesn't exist
out_dir = '..//Output//' + satellite
if not os.path.exists(out_dir):
   os.mkdir(out_dir)

# Create the product output directory if it doesn't exist
out_dir = '..//Output//' + satellite + '//' + product + '//'
if not os.path.exists(out_dir):
   os.mkdir(out_dir)
 
# Desired Extent
extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]
# South America
#extent = [-90.0, -60.0, -30.0, 15.0]
# INPE RGB extent
#extent = [-145.0, -65.0, -5.0, 65.0]
 
# Desired resolution
band_resolution_km = int(sys.argv[6])
resolution = int(sys.argv[6])
    
# Define KM_PER_DEGREE
KM_PER_DEGREE = 111.32

print (resolution)
# Compute grid dimension
sizex = int(((extent[2] - extent[0]) * KM_PER_DEGREE) / band_resolution_km) 
sizey = int(((extent[3] - extent[1]) * KM_PER_DEGREE) / band_resolution_km) 

print(sizex)
print(sizey)

# Path to the GOES-16 RGB file (Sector 07 is the last sector received)
path_S07 = file
path_FDK = file.replace("S07", "FDK")
path_S01 = file.replace("S07", "S01")
path_S02 = file.replace("S07", "S02")
path_S03 = file.replace("S07", "S03")
path_S04 = file.replace("S07", "S04")
path_S05 = file.replace("S07", "S05")
path_S06 = file.replace("S07", "S06")

# File output name
path_out = file.replace("S07", "RGB")

import ntpath
file_only = ntpath.basename(path_out)
path_out = out_dir + file_only

print(path_out)
print(path_FDK)
print(path_S01)
print(path_S02)
print(path_S03)
print(path_S04)
print(path_S05)
print(path_S06)
print(path_S07)


# Create the mosaic and cut
grid = gdal.Warp(path_out,[path_FDK, path_S01, path_S02, path_S03, path_S04, path_S05, path_S06, path_S07],options=gdal.WarpOptions(outputBounds = [extent[0], extent[1], extent[2], extent[3]], width = sizex, height = sizey))
grid = None
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Open the file:
raster = gdal.Open(path_out)

# File name
file_name = os.path.splitext(os.path.basename(path_out))[0]

# Get times and dates
product = file_name[4:7] 
year = file_name[11:15]
month = file_name[15:17]
day = file_name[17:19]
hour = file_name[19:21]
minutes = file_name[21:23]

# Read the product name
title = "GOES-16 " + product + " " + "RGB" + " " + year + "-" + month + "-" + day + " " + hour + ":" + minutes + " " + "UTC"

# Product Name
product = product + "RGB"

# Read the raster band as separate variable
Rb = raster.GetRasterBand(1)
R = Rb.ReadAsArray()

# Read the raster band as separate variable
Gb = raster.GetRasterBand(2)
G = Gb.ReadAsArray()

# Read the raster band as separate variable
Bb = raster.GetRasterBand(3)
B = Bb.ReadAsArray()

# Delete the ancillary GeoTIFF
raster = None
Rb = None
Gb = None
Bb = None
gdal.Unlink(path_out)

# Create the RGB
data = np.stack([R, G, B], axis=2)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Plot configuration
plot_config = {
"resolution": band_resolution_km, 
"dpi": 150, 
"states_color": 'white', "states_width": data.shape[0] * 0.00006, 
"countries_color": 'white', "countries_width": data.shape[0] * 0.00012,
"continents_color": 'white', "continents_width": data.shape[0] * 0.00025,
"grid_color": 'white', "grid_width": data.shape[0] * 0.00025, "grid_interval": 10.0,
"title_text": title, "title_size": int(data.shape[1] * 0.005), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[0] - int(data.shape[0] * 0.016), 
"file_name_id_1": "G16",  "file_name_id_2": "RGB" 
}
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Desired plot resolution
resolution = plot_config["resolution"]

# Division factor to reduce image size
res_f = resolution / band_resolution_km

# Choose the plot size (width x height, in inches)
# Diego: Put zero on both width and height because after reprojection both are equal
fig = plt.figure(figsize=(data.shape[1]/float(plot_config["dpi"]), data.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])

# Define the projection
# Diego: For some reason it only worked with the central longitude as "0.0" instead of "-75.0"
proj = ccrs.PlateCarree(central_longitude = 0.0)
ax = plt.axes([0, 0, 1, 1], projection = proj)
ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree(central_longitude = 0.0))
img_extent = (extent[0], extent[2], extent[1], extent[3])

# Plot the image
img = ax.imshow(data, extent=img_extent, origin='upper', zorder=1)

# Add states and provinces
shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=2)

# Add countries
shapefile = list(shpreader.Reader('..//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=3)

# Add continents
shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_coastline.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=4)
  
# Add coastlines, borders and gridlines
ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=False, zorder=5)

# Remove the outline border
ax.outline_patch.set_visible(False)

# Add a title
plt.annotate(plot_config["title_text"], xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=6)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Create the satellite output directory if it doesn't exist
out_dir = '..//Output//' + satellite
if not os.path.exists(out_dir):
   os.mkdir(out_dir)

# Create the product output directory if it doesn't exist
out_dir = '..//Output//' + satellite + '//' + product + '//'
if not os.path.exists(out_dir):
   os.mkdir(out_dir)
   
# Save the image
plt.savefig(out_dir + file_name + '.png', bbox_inches='tight', pad_inches=0)

# Update the animation
update(satellite, product)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Put the processed file on the log
import datetime # Basic Date and Time types
with open('..//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
 log.write(str(datetime.datetime.now()))
 log.write('\n')
 log.write(path + '\n')
 log.write('\n')
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

print('Total processing time:', round((t.time() - start),2), 'seconds.') 

