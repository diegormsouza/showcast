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
import numpy as np                                           # Scientific computing with Python
import cartopy, cartopy.crs as ccrs                          # Plot maps
import cartopy.io.shapereader as shpreader                   # Import shapefiles
import time as t                                             # Time access and conversion
import math                                                  # Import math
import re                                                    # re
import glob                                                  # Unix style pathname pattern expansion
import sys                                                   # Import the "system specific parameters and functions" module
import os 												     # Miscellaneous operating system interfaces
import platform                                              # To check which OS is being used
from html_update import update                               # Update the HTML animation 
import warnings
warnings.filterwarnings("ignore")
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()  

# Band 02 path
path_ch02 = (sys.argv[1])
#path_ch02 = ("..//Samples//OR_ABI-L2-CMIPF-M6C02_G16_s20192931650344_e20192931700052_c20192931700142-132002_0.nc")

# For the log
path = path_ch02

#print(path)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
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
    
# Seek for a GOES-16 file (same time) in the directory
matching = [s for s in file if scan_start in s]     

# If the file is not found, exit the loop
if not matching:
    print("File Not Found! Exiting Script.")
    sys.exit()
else: # If the file is found, continue
    print("File OK!")
    matching = matching[0]
    index = file.index(matching)
    path_ch13 = file[index]

#print(path_ch02)
print(path_ch13)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
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

# Calculate the image extent 
H = file_ch02.variables['goes_imager_projection'].perspective_point_height
x1 = file_ch02.variables['x_image_bounds'][0] * H 
x2 = file_ch02.variables['x_image_bounds'][1] * H 
y1 = file_ch02.variables['y_image_bounds'][1] * H 
y2 = file_ch02.variables['y_image_bounds'][0] * H 

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

# Get the pixel values
data_ch02 = file_ch02.variables['CMI'][:,:][::f ,::f ]

# Load the Channel 02 contrast curve
contrast_curve = [0.00000, 0.02576, 0.05148, 0.07712, 0.10264, 0.12799, 0.15313, 0.17803, 0.20264, 0.22692, 0.25083, 0.27432, 0.29737, 0.31991, 0.34193, 0.36336,
0.38418, 0.40433, 0.42379, 0.44250, 0.46043, 0.47754, 0.49378, 0.50911, 0.52350, 0.53690, 0.54926, 0.56055, 0.57073, 0.57976, 0.58984, 0.59659,
0.60321, 0.60969, 0.61604, 0.62226, 0.62835, 0.63432, 0.64016, 0.64588, 0.65147, 0.65694, 0.66230, 0.66754, 0.67267, 0.67768, 0.68258, 0.68738,
0.69206, 0.69664, 0.70112, 0.70549, 0.70976, 0.71394, 0.71802, 0.72200, 0.72589, 0.72968, 0.73339, 0.73701, 0.74055, 0.74399, 0.74736, 0.75065,
0.75385, 0.75698, 0.76003, 0.76301, 0.76592, 0.76875, 0.77152, 0.77422, 0.77686, 0.77943, 0.78194, 0.78439, 0.78679, 0.78912, 0.79140, 0.79363,
0.79581, 0.79794, 0.80002, 0.80206, 0.80405, 0.80600, 0.80791, 0.80978, 0.81162, 0.81342, 0.81518, 0.81692, 0.81862, 0.82030, 0.82195, 0.82358,
0.82518, 0.82676, 0.82833, 0.82987, 0.83140, 0.83292, 0.83442, 0.83592, 0.83740, 0.83888, 0.84036, 0.84183, 0.84329, 0.84476, 0.84623, 0.84771,
0.84919, 0.85068, 0.85217, 0.85368, 0.85520, 0.85674, 0.85829, 0.85986, 0.86145, 0.86306, 0.86469, 0.86635, 0.86803, 0.86974, 0.87149, 0.87326,
0.87500, 0.87681, 0.87861, 0.88038, 0.88214, 0.88388, 0.88560, 0.88730, 0.88898, 0.89064, 0.89228, 0.89391, 0.89552, 0.89711, 0.89868, 0.90023,
0.90177, 0.90329, 0.90479, 0.90627, 0.90774, 0.90919, 0.91063, 0.91205, 0.91345, 0.91483, 0.91620, 0.91756, 0.91890, 0.92022, 0.92153, 0.92282,
0.92410, 0.92536, 0.92661, 0.92784, 0.92906, 0.93027, 0.93146, 0.93263, 0.93380, 0.93495, 0.93608, 0.93720, 0.93831, 0.93941, 0.94050, 0.94157,
0.94263, 0.94367, 0.94471, 0.94573, 0.94674, 0.94774, 0.94872, 0.94970, 0.95066, 0.95162, 0.95256, 0.95349, 0.95441, 0.95532, 0.95622, 0.95711,
0.95799, 0.95886, 0.95973, 0.96058, 0.96142, 0.96225, 0.96307, 0.96389, 0.96469, 0.96549, 0.96628, 0.96706, 0.96783, 0.96860, 0.96936, 0.97010,
0.97085, 0.97158, 0.97231, 0.97303, 0.97374, 0.97445, 0.97515, 0.97584, 0.97653, 0.97721, 0.97789, 0.97856, 0.97922, 0.97988, 0.98053, 0.98118,
0.98182, 0.98246, 0.98309, 0.98372, 0.98435, 0.98497, 0.98559, 0.98620, 0.98681, 0.98741, 0.98802, 0.98862, 0.98921, 0.98980, 0.99039, 0.99098,
0.99157, 0.99215, 0.99273, 0.99331, 0.99389, 0.99446, 0.99503, 0.99561, 0.99618, 0.99675, 0.99732, 0.99788, 0.99845, 0.99902, 0.99959, 1.000000]
 
# Convert the contrast curve to a numpy array
curve = np.array(contrast_curve)

# Minimum and maximum reflectances
VISmin = 0.0
VISmax = 1.0
# Anything that is below the min or greater than max, keep min and max
data_ch02[data_ch02 > VISmax] = VISmax
# Convert to 0 - 255
data_ch02 = ((data_ch02 - VISmin) / (VISmax - VISmin)) * 255
# Convert to int
data_ch02 = data_ch02.astype(int)
# Apply the contrast curve
data_ch02 = curve[data_ch02] * 255
# Convert to int
data_ch02 = data_ch02.astype(int)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Read the image
file_ch13 = Dataset(path_ch13)

# Read the resolution
band_resolution_km = getattr(file_ch13, 'spatial_resolution')
band_resolution_km = float(band_resolution_km[:band_resolution_km.find("km")])

# Division factor to reduce image size
f = math.ceil(float(resolution / band_resolution_km))

# Get the pixel values
data_ch13 = file_ch13.variables['CMI'][:,:][::f ,::f ]

# Minimum and maximum reflectances
IRmin = 89.62
IRmax = 341.27
# Anything that is below the min or greater than max, keep min and max
data_ch13[data_ch13 > IRmax] = IRmax
# Convert to 0 - 255
data_ch13 = ((data_ch13 - IRmin) / (IRmax - IRmin)) * 255
# Convert to int
data_ch13 = data_ch13.astype(int)

#print("Reading the False Color Look Up Table...")
 
import matplotlib.image as mpimg
# Open the False Color Look Up Table
img = mpimg.imread('..//Colortables//wx-star.com_GOES-R_ABI_False-Color-LUT_sat20.png')
# Flip the array (for some reason, is necessary to flip the LUT horizontally)
img = np.fliplr(img)
# Apply the look up table based on the Band 02 reflectances and Band 13 Brightness Temperatures
data = img[data_ch02,data_ch13,0:3]

# Eliminate values outside the globe
mask = (data == [data[0,0]])
data[mask] = np.nan

# Product Name
product = "FCOLOR_FDK"
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
  
# Plot configuration
plot_config = {
"resolution": band_resolution_km, 
"dpi": 150, 
"states_color": 'white', "states_width": data_ch02.shape[0] * 0.00006, 
"countries_color": 'gold', "countries_width": data_ch02.shape[0] * 0.00012,
"continents_color": 'gold', "continents_width": data_ch02.shape[0] * 0.00025,
"grid_color": 'white', "grid_width": data_ch02.shape[0] * 0.00025, "grid_interval": 10.0,
"title_text": "GOES-" + satellite[1:3] + " FALSE COLOR ", "title_size": int(data_ch02.shape[1] * 0.005), "title_x_offset": int(data_ch02.shape[1] * 0.01), "title_y_offset": data_ch02.shape[0] - int(data_ch02.shape[0] * 0.016), 
"file_name_id_1": satellite,  "file_name_id_2": product
}

# Choose the plot size (width x height, in inches)
fig = plt.figure(figsize=(data_ch02.shape[1]/float(plot_config["dpi"]), data_ch02.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])
  
# Define the projection
proj = ccrs.Geostationary(central_longitude=longitude, satellite_height=H)
img_extent = (x1,x2,y1,y2)

# Use the Geostationary projection in cartopy
ax = plt.axes([0, 0, 1, 1], projection=proj)

# Plot the image
img = ax.imshow(data, origin='upper', extent=img_extent, zorder=1)

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
plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=6)

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
plt.savefig(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.png', bbox_inches='tight', pad_inches=0, facecolor='black')

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