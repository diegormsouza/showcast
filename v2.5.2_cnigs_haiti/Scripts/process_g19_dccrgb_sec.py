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
import math                                                  # Import math
import re                                                    # re
import glob                                                  # Unix style pathname pattern expansion
import sys                                                   # Import the "system specific parameters and functions" module
import os 												     # Miscellaneous operating system interfaces
from os.path import dirname, abspath                         # Return a normalized absolutized version of the pathname path 
import platform                                              # To check which OS is being used
from html_update import update                               # Update the HTML animation 
from remap import remap                                      # Import the Remap function
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()  

# SHOWCast directory:
main_dir = dirname(dirname(abspath(__file__)))

# Band 02 file
path_ch02 = (sys.argv[1])

# For the log
path = path_ch02

#---------------------------------------------------------------------------------------------
# Read the interval and check if this file should be processed based on the config file
import re                        # Regular expression operations
intervals = (sys.argv[9])        # Read the string from the parameters
intervals = intervals.split(",") # Split the string in a list
for interval in intervals:       # For each interval in the list, check the file
    #print(interval)
    regex = re.compile(r'(?:s.........' + str(interval) + ')..._')
    finder = re.findall(regex, path)
    # If "matches" is "0", it is not from a desired interval. If it is "1", process the file	
    matches = len(finder)
    # If it is from a desired minute, exit verification loop
    if (matches == 1): break
if (matches == 0): # After the loop, if "matches" is "0", the file is not from a desired interval
    print("This file is not from an interval that should be processed. Exiting script.")
    # Put the processed file on the log
    import datetime # Basic Date and Time types
    with open(main_dir + '//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
        log.write(str(datetime.datetime.now()))
        log.write('\n')
        log.write(path + '\n')
        log.write('\n')
    quit()
#---------------------------------------------------------------------------------------------   

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Remove the identification
path_ch02 = path_ch02[:-4]

# Get the Band 13, same file
osystem = platform.system()
if osystem == "Windows":
    path_ch13 = re.sub('Band02\\\\OR_ABI-L2-CMIPF*(.*)', '', path_ch02)
else:
    path_ch13 = re.sub('Band02/OR_ABI-L2-CMIPF*(.*)', '', path_ch02)

# Get the start of scan from the file name
scan_start = (path_ch02[path_ch02.find("_s")+2:path_ch02.find("_e")])

file = []
for filename in sorted(glob.glob(path_ch13+'Band13//OR_ABI-L2-CMIPF-M*C13_G1*.nc')):
    file.append(filename)
    
# Seek for a GOES-19 file (same time) in the directory
matching = [s for s in file if scan_start in s]     

# If the file is not found, exit the loop
if not matching:
    print("One of the files necessary to create the composite is not available yet. Exiting Script.")
    sys.exit()
else: # If the file is found, continue
    print("File OK!")
    matching = matching[0]
    index = file.index(matching)
    path_ch13 = file[index]

#print(path_ch02)
#print(path_ch13)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Read the image
file_ch02 = Dataset(path_ch02)

# Read the satellite 
satellite = getattr(file_ch02, 'platform_ID')

# Read the band number
band = str(file_ch02.variables['band_id'][0]).zfill(2)

# Desired resolution
resolution = int(sys.argv[6])

# Read the resolution
band_resolution_km = getattr(file_ch02, 'spatial_resolution')
band_resolution_km = float(band_resolution_km[:band_resolution_km.find("km")])

# Division factor to reduce image size
f = math.ceil(float(resolution / band_resolution_km))

# Read the central longitude
longitude = file_ch02.variables['goes_imager_projection'].longitude_of_projection_origin

# Read the semi major axis
a = file_ch02.variables['goes_imager_projection'].semi_major_axis

# Read the semi minor axis
b = file_ch02.variables['goes_imager_projection'].semi_minor_axis

# Calculate the image extent 
h = file_ch02.variables['goes_imager_projection'].perspective_point_height
x1 = file_ch02.variables['x_image_bounds'][0] * h 
x2 = file_ch02.variables['x_image_bounds'][1] * h 
y1 = file_ch02.variables['y_image_bounds'][1] * h 
y2 = file_ch02.variables['y_image_bounds'][0] * h 

# Getting the file time and date
add_seconds = int(file_ch02.variables['time_bounds'][0])
date = datetime(2000,1,1,12) + timedelta(seconds=add_seconds)
date_formated = date.strftime('%Y-%m-%d %H:%M UTC')
date_file = date.strftime('%Y%m%d%H%M')
year = date.strftime('%Y')
month = date.strftime('%m')
day = date.strftime('%d')
hour = date.strftime('%H')
minutes = date.strftime('%M')

# Choose the visualization extent (min lon, min lat, max lon, max lat)
extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]

# Variable to remap
variable = "CMI"

# Call the reprojection funcion
grid = remap(path_ch02, variable, extent, resolution, h, a, b, longitude, x1, y1, x2, y2)
     
# Read the data returned by the function 
data_ch02 = grid.ReadAsArray() 
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Read the image
file_ch13 = Dataset(path_ch13)

# Variable to remap
variable = "CMI"

# Call the reprojection funcion
grid = remap(path_ch13, variable, extent, resolution, h, a, b, longitude, x1, y1, x2, y2)
     
# Read the data returned by the function 
data_ch13 = grid.ReadAsArray() - 273.15
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# RGB Components
R = data_ch02 
G = data_ch02 
B = data_ch13

# Minimuns and Maximuns
Rmin = 0.0
Rmax = 1.0

Gmin = 0.0
Gmax = 1.0

Bmin = 49.85
Bmax = -70.15

R[R<Rmin] = Rmin
R[R>Rmax] = Rmax

G[G<Gmin] = Gmin
G[G>Gmax] = Gmax

B[B>Bmin] = Bmin
B[B<Bmax] = Bmax

# Choose the gamma
gamma_R = 1.7
gamma_G = 1.7
gamma_B = 1

# Normalize the data
R = ((R - Rmin) / (Rmax - Rmin)) ** (1/gamma_R)
G = ((G - Gmin) / (Gmax - Gmin)) ** (1/gamma_G)
B = ((B - Bmin) / (Bmax - Bmin)) ** (1/gamma_B) 

# Create the RGB
RGB = np.stack([R, G, B], axis=2)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Product Name
product = "DCCRGB_SEC" 

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
# Plot configuration
plot_config = {
"resolution": band_resolution_km, 
"dpi": 150, 
"states_color": 'white', "states_width": data_ch13.shape[0] * 0.00018, 
"countries_color": 'white', "countries_width": data_ch13.shape[0] * 0.00012,
"continents_color": 'white', "continents_width": data_ch13.shape[0] * 0.00025,
"grid_color": 'white', "grid_width": data_ch13.shape[0] * 0.00025, "grid_interval": 10.0,
"vmin": 0, "vmax": 1, "cmap": 'jet',
"title_text": "GOES-" + satellite[1:3] + " DCC RGB ", "title_size": int(data_ch13.shape[1] * 0.005), "title_x_offset": int(data_ch13.shape[1] * 0.01), "title_y_offset": data_ch13.shape[0] - int(data_ch13.shape[0] * 0.016), 
"thick_interval": 0, "cbar_labelsize": int(data_ch13.shape[0] * 0.005), "cbar_labelpad": -int(data_ch13.shape[0] * 0.0),
"file_name_id_1": satellite,  "file_name_id_2": product
}
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
fig = plt.figure(figsize=(data_ch13.shape[1]/float(plot_config["dpi"]), data_ch13.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])
  
# Define the projection
proj = ccrs.PlateCarree()

# Use the PlateCarree projection in cartopy
ax = plt.axes([0, 0, 1, 1], projection=proj)
ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

# Define the image extent
img_extent = [extent[0], extent[2], extent[1], extent[3]]

# Plot the image
img = ax.imshow(RGB, origin='upper', extent=img_extent, zorder=1)

# Add states and provinces
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=2)

# Add countries
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=3)

# Add continents
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_coastline.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=4)
  
# Add coastlines, borders and gridlines
gl = ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=True, zorder=5)
gl.left_labels = True; gl.right_labels = False; gl.top_labels = True; gl.bottom_labels = False
gl.xpadding = -plot_config["cbar_labelsize"]; gl.ypadding = -plot_config["cbar_labelsize"]
gl.ylabel_style = {'color': 'white', 'size': plot_config["cbar_labelsize"], 'weight': 'bold'}
gl.xlabel_style = {'color': 'white', 'size': plot_config["cbar_labelsize"], 'weight': 'bold'}

# Remove the outline border
ax.outline_patch.set_visible(False)
  
# Add a title
plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=6)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Add labels to specific coordinates

import configparser
conf = configparser.ConfigParser()
if (satellite == 'G16'):
    conf.read(main_dir + '//Utils//Labels//labels_g16.ini')
elif (satellite == 'G17'):
    conf.read(main_dir + '//Utils//Labels//labels_g17.ini')
elif (satellite == 'G18'):
    conf.read(main_dir + '//Utils//Labels//labels_g18.ini')
elif (satellite == 'G19'):
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

my_legend = plt.imread(main_dir + '//Legends//DAYCLOUDCONVECTION_legend.png')
newax = fig.add_axes([0.60, 0.60, 0.39, 0.39], anchor='NE', zorder=13) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
newax.imshow(my_legend)
newax.axis('off')
    
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

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
nfiles = 20
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