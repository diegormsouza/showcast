#######################################################################################################
# LICENSE
# Copyright (C) 2025 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL
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
__copyright__ = "Copyright (C) 2025 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL"
__credits__ = ["Diego Souza"]
__license__ = "GPL"
__version__ = "2.5.2"
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
from netCDF4 import Dataset, num2date                        # Read / Write NetCDF4 files
from mpl_toolkits.axes_grid1.inset_locator import inset_axes # Add a child inset axes to this existing axes.
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
import matplotlib.pyplot as plt                              # Plotting library
import numpy as np                                           # Scientific computing with Python
import cartopy, cartopy.crs as ccrs                          # Plot maps
import cartopy.io.shapereader as shpreader                   # Import shapefiles
import time as t                                             # Time access and conversion
import os                                                    # Miscellaneous operating system interfaces
import re                                                    # re
import glob                                                  # Unix style pathname pattern expansion
import sys                                                   # Import the "system specific parameters and functions" module
import os 												     # Miscellaneous operating system interfaces
from os.path import dirname, abspath                         # Return a normalized absolutized version of the pathname path 
import platform                                              # To check which OS is being used
import math                                                  # Import math
from html_update import update                               # Update the HTML animation 
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()  

# SHOWCast directory:
main_dir = dirname(dirname(abspath(__file__)))

# Path for logging purposes
path = (sys.argv[1])

# GLM file
path_glm = (sys.argv[1])[:-4]

# Read the GLM file
fileGLM = Dataset(path)

# Read the central longitude
longitude = fileGLM.variables['lon_field_of_view'][0]

# Read the satellite height
h = fileGLM.variables['nominal_satellite_height'][0] * 1000

# Reading the file time and date
add_seconds = int(fileGLM.variables['product_time'][0])
date = datetime(2000,1,1,12) + timedelta(seconds=add_seconds)
date_formated = date.strftime('%Y-%m-%d %H:%M:%S UTC')
date_file = date.strftime('%Y%m%d%H%M%S')

# Desired resolution
resolution = int(sys.argv[6])

# Create the empty Full Disk array
shape = (5424 / ((resolution)/2))
data = np.empty((int(shape),int(shape)))
data[:] = np.nan

# Read the satellite 
satellite = getattr(fileGLM, 'platform_ID')

# Product Name
product = "GLM20S_FDK" 
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Plot configuration
plot_config = {
"resolution": resolution, 
"dpi": 150, 
"states_color": 'white', "states_width": data.shape[0] * 0.00006, 
"countries_color": 'white', "countries_width": data.shape[0] * 0.00012,
"continents_color": 'white', "continents_width": data.shape[0] * 0.00025,
"grid_color": 'white', "grid_width": data.shape[0] * 0.00025, "grid_interval": 10.0,
"title_text": "GOES-19 GLM (20s)", "title_size": int(data.shape[1] * 0.005), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[1] - int(data.shape[1] * 0.016), 
"file_name_id_1": satellite,  "file_name_id_2": product
}
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
fig = plt.figure(figsize=(data.shape[1]/float(plot_config["dpi"]), data.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])
  
# Define the projection
proj = ccrs.Geostationary(central_longitude=longitude, satellite_height=h)
img_extent = (-5434894.67527,5434894.67527,-5434894.67527,5434894.67527)

# Use the Geostationary projection in cartopy
ax = plt.axes([0, 0, 1, 1], projection=proj)
#---------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------- 
# Background color
import cartopy.feature as cfeature
land = ax.add_feature(cfeature.LAND, facecolor='black', zorder=1)
ocean = ax.add_feature(cfeature.OCEAN, facecolor='black', zorder=2)

# Plotting the empty full disk
img1 = ax.imshow(data, vmin=0, vmax=1, extent=img_extent, zorder=3) 

# Get the events lats and lons
e_lats = fileGLM.variables['event_lat'][:]
e_lons = fileGLM.variables['event_lon'][:]
# Get the groups lats and lons
g_lats = fileGLM.variables['group_lat'][:]
g_lons = fileGLM.variables['group_lon'][:]
# Get the flashes lats and lons
f_lats = fileGLM.variables['flash_lat'][:]
f_lons = fileGLM.variables['flash_lon'][:]

# Plotting events, groups and flashes
img2 = ax.plot(e_lons,e_lats, 'o', markersize=1.0, color='#fffb8a', alpha = 0.01, transform=ccrs.PlateCarree(), zorder=4)
img3 = ax.plot(g_lons,g_lats, 'o', markersize=1.0, color='#fffdc7', alpha = 0.02, transform=ccrs.PlateCarree(), zorder=5)
img4 = ax.plot(f_lons,f_lats, 'o', markersize=1.0, color='#fff700', alpha = 0.20, transform=ccrs.PlateCarree(), zorder=6)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Add states and provinces
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=7)

# Add coastlines and borders
ax.coastlines(resolution='50m', color=plot_config["countries_color"], linewidth=plot_config["countries_width"], zorder=8)
ax.add_feature(cartopy.feature.BORDERS, edgecolor=plot_config["continents_color"], linewidth=plot_config["continents_width"], zorder=9)

# Add countries
#shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
#ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=8)

# Add continents
#shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_coastline.shp').geometries())
#ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=9)
  
# Add gridlines
ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=False, zorder=10)

# Remove the outline border
ax.outline_patch.set_visible(False)

# Add a title
plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=11)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Add labels to specific coordinates

import configparser
conf = configparser.ConfigParser()
conf.read(main_dir + '//Utils//Labels//labels_g19.ini')

labels, city_lons, city_lats, x_offsets, y_offsets, sizes, colors, marker_types, marker_colors, marker_sizes = [],[],[],[],[],[],[],[],[],[]

for each_section in conf.sections():
    for (each_key, each_val) in conf.items(each_section):
        if (each_key == 'label'): labels.append(each_val)
        if (each_key == 'lon'): city_lons.append(float(each_val))
        if (each_key == 'lat'): city_lats.append(float(each_val))
        if (each_key == 'x_offset'): x_offsets.append(float(each_val))
        if (each_key == 'y_offset'): y_offsets.append(float(each_val))
        if (each_key == 'size'): sizes.append(int(each_val))
        if (each_key == 'color'): colors.append(each_val)
        if (each_key == 'marker_type'): marker_types.append(each_val)
        if (each_key == 'marker_color'): marker_colors.append(each_val)
        if (each_key == 'marker_size'): marker_sizes.append(each_val)
 
import matplotlib.patheffects as PathEffects
for label, xpt, ypt, x_offset, y_offset, size, col, mtype, mcolor, msize in zip(labels, city_lons, city_lats, x_offsets, y_offsets, sizes, colors, marker_types, marker_colors, marker_sizes):
    ax.plot(xpt, ypt, str(mtype), color=str(mcolor), markersize=int(msize), transform=ccrs.Geodetic(), markeredgewidth=1.0, markeredgecolor=(0, 0, 0, 1), zorder=10)
    txt = ax.text(xpt+x_offset , ypt+y_offset, label, fontsize=int(size), fontweight='bold', color=str(col), transform=ccrs.Geodetic(), zorder=11)
    txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='black')])

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Add logos / images to the plot
my_logo = plt.imread(main_dir + '//Logos//my_logo.png')
newax = fig.add_axes([0.01, 0.03, 0.10, 0.10], anchor='SW', zorder=12) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
newax.imshow(my_logo)
newax.axis('off')

# Create the satellite output directory if it doesn't exist
out_dir = (sys.argv[7]) + satellite
if not os.path.exists(out_dir):
   os.mkdir(out_dir)

# Create the product output directory if it doesn't exist
out_dir = (sys.argv[7]) + satellite + '//' + product + '//'
if not os.path.exists(out_dir):
   os.mkdir(out_dir)
   
# Save the image
plt.savefig(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.png', facecolor='black')

# Convert to webp
from PIL.WebPImagePlugin import Image          
im = Image.open(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.png')
im.save(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.webp', format = "WebP", lossless = True)
im.close()

# Update the animation
nfiles = 60
update(satellite, product, nfiles, sys.argv[7], sys.argv[8])

# Delete aux files
os.remove(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.png') 

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Put the processed file on the log
import datetime # Basic Date and Time types
with open(main_dir + '//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
 log.write(str(datetime.datetime.now()))
 log.write('\n')
 log.write(path + '\n')
 log.write('\n')
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
print('Total processing time:', round((t.time() - start),2), 'seconds.') 
