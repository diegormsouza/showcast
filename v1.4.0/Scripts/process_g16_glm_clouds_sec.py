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
from netCDF4 import Dataset, num2date                        # Read / Write NetCDF4 files
from mpl_toolkits.axes_grid1.inset_locator import inset_axes # Add a child inset axes to this existing axes.
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
from cpt_convert import loadCPT                              # Import the CPT convert function
from matplotlib.colors import LinearSegmentedColormap        # Linear interpolation for color maps
import matplotlib.pyplot as plt                              # Plotting library
import numpy as np                                           # Scientific computing with Python
import cartopy, cartopy.crs as ccrs                          # Plot maps
import cartopy.io.shapereader as shpreader                   # Import shapefiles
import time as t                                             # Time access and conversion
import scipy as sp                                           # Scipy
from scipy.ndimage import gaussian_filter                    # Scipy Gaussian Filter
from matplotlib.image import imread                          # Read an image from a file into an array
import os                                                    # Miscellaneous operating system interfaces
from cartopy.feature.nightshade import Nightshade            # Draws a polygon where there is no sunlight for the given datetime.
import re                                                    # re
import glob                                                  # Unix style pathname pattern expansion
import sys                                                   # Import the "system specific parameters and functions" module
import os 												     # Miscellaneous operating system interfaces
import platform                                              # To check which OS is being used
import math                                                  # Import math
from html_update import update                               # Update the HTML animation 
from remap import remap                                      # Import the Remap function
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()  

# GLM file
path_glm = (sys.argv[1])
#path_glm = ("..//Samples//GLM_DENS_20191024173000.nc")

# For the log
path = path_glm

# Remove the identification
path_glm = path_glm[:-4]

# Read the satellite 
satellite = "G16"

# Read the image
file_glm = Dataset(path_glm)

# Choose the visualization extent (min lon, min lat, max lon, max lat)
extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]
 
# Desired resolution
resolution = int(sys.argv[6])
band_resolution_km = int(sys.argv[6])
    
# Define KM_PER_DEGREE
KM_PER_DEGREE = 111.32

# Compute grid dimension
sizex = int(((extent[2] - extent[0]) * KM_PER_DEGREE) / band_resolution_km) 
sizey = int(((extent[3] - extent[1]) * KM_PER_DEGREE) / band_resolution_km) 

# Getting the GLM file date
time = file_glm.variables['time']
date = num2date(time[:], time.units, time.calendar) + timedelta(minutes=5)
#print(date)
date_formated = date[0].strftime('%Y-%m-%d %H:%M UTC')
date_file = date[0].strftime('%Y%m%d%H%M')
year = date[0].strftime('%Y')
month = date[0].strftime('%m')
day = date[0].strftime('%d')
hour = date[0].strftime('%H')
minutes = date[0].strftime('%M')

# Getting the julian day
date_form = year+month+day
dt = date[0].strptime(date_form, '%Y%m%d')
tt = dt.timetuple()
jday = str(tt.tm_yday).zfill(3)

#print(year)
#print(month)
#print(day)
#print(jday)

# Get the start date for GOES files
goes_start = "_s" + year + jday + hour #+ minutes[0]
print(goes_start)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Remove the identification
#path = path[:-4]

# Get the Band 13, same file
osystem = platform.system()
if osystem == "Windows":
    path_ch13 = re.sub('GOES-R-GLM-Products\\\\GLM_DENS_*(.*)', '', path_glm)
else:
    path_ch13 = re.sub('GOES-R-GLM-Products/GLM_DENS_*(.*)', '', path_glm)

#print(path_ch13)

file = []
for filename in sorted(glob.glob(path_ch13+'GOES-R-CMI-Imagery//Band13//OR_ABI-L2-CMIPF-M*C13_G16*.nc')):
    file.append(filename)
    
# Seek for a GOES-16 file (same time) in the directory
matching = [s for s in file if goes_start in s]     

# If the file is not found, exit the loop
if not matching:
    print("File Not Found! Exiting Script.")
    sys.exit()
else: # If the file is found, continue
    print("File OK!")
    matching = matching[0]
    index = file.index(matching)
    path_ch13 = file[index]

#print(path_glm)
#print(path_ch13)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Band 13 file
file_ch13 = Dataset(path_ch13)

# Read the satellite 
satellite = getattr(file_ch13, 'platform_ID')

# Read the band number
band = str(file_ch13.variables['band_id'][0]).zfill(2)

# Desired resolution
resolution = int(sys.argv[6])

# Read the resolution
band_resolution_km = getattr(file_ch13, 'spatial_resolution')
band_resolution_km = float(band_resolution_km[:band_resolution_km.find("km")])

# Division factor to reduce image size
f = math.ceil(float(resolution / band_resolution_km))

# Read the central longitude
longitude = file_ch13.variables['goes_imager_projection'].longitude_of_projection_origin

# Read the semi major axis
a = file_ch13.variables['goes_imager_projection'].semi_major_axis

# Read the semi minor axis
b = file_ch13.variables['goes_imager_projection'].semi_minor_axis

# Calculate the image extent 
h = file_ch13.variables['goes_imager_projection'].perspective_point_height
x1 = file_ch13.variables['x_image_bounds'][0] * h 
x2 = file_ch13.variables['x_image_bounds'][1] * h 
y1 = file_ch13.variables['y_image_bounds'][1] * h 
y2 = file_ch13.variables['y_image_bounds'][0] * h 

# Getting the file time and date
add_seconds = int(file_ch13.variables['time_bounds'][0])
date = datetime(2000,1,1,12) + timedelta(seconds=add_seconds)
#date_formated = date.strftime('%Y-%m-%d %H:%M UTC')
#date_file = date.strftime('%Y%m%d%H%M')
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
grid = remap(path_ch13, variable, extent, resolution, h, a, b, longitude, x1, y1, x2, y2)
     
# Read the data returned by the function 
data = grid.ReadAsArray()

# Product Name
product = "GLMIRC_SEC" 
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Plot configuration
plot_config = {
"resolution": band_resolution_km, 
"dpi": 150, 
"states_color": 'white', "states_width": data.shape[0] * 0.00018, 
"countries_color": 'gold', "countries_width": data.shape[0] * 0.00012,
"continents_color": 'gold', "continents_width": data.shape[0] * 0.00025,
"grid_color": 'white', "grid_width": data.shape[0] * 0.00025, "grid_interval": 10.0,
"title_text": "GOES-16 GLM + BAND-13", "title_size": int(data.shape[1] * 0.005), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[0] - int(data.shape[0] * 0.016), 
"file_name_id_1": satellite,  "file_name_id_2": product
}
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
fig = plt.figure(figsize=(data.shape[1]/float(plot_config["dpi"]), data.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])
  
# Define the projection
proj = ccrs.PlateCarree()

# Use the PlateCarree projection in cartopy
ax = plt.axes([0, 0, 1, 1], projection=proj)
ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

# Define the image extent
img_extent = [extent[0], extent[2], extent[1], extent[3]]

# Add a background image
#ax.stock_img()
fname = os.path.join('..//Maps//', 'land_ocean_ice_8192.jpg')
ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)
date = datetime(int(year), int(month), int(day), int(hour))
#ax.add_feature(Nightshade(date, alpha=0.7), zorder=2)

#print("First layer...")
# Apply range limits for clean IR channel
data1 = data
data1 = np.maximum(data1, 90)
data1 = np.minimum(data1, 313)
# Normalize the channel between a range
data1 = (data1-90)/(313-90)
# Invert colors
data1 = 1 - data1
img = ax.imshow(data1, cmap='gray', vmin=0.1, vmax=0.25, alpha = 0.6, origin='upper', extent=img_extent, zorder=3)

#print("Second layer...")
# SECOND LAYER
data2 = data1
data2[data2 < 0.25] = np.nan
img2 = ax.imshow(data2, cmap='gray', vmin=0.05, vmax=0.50, alpha = 0.7, origin='upper', extent=img_extent, zorder=4)

#print("Third layer...")
# Third LAYER
data2 = data1
data2[data2 < 0.30] = np.nan
img3 = ax.imshow(data2, cmap='gray', vmin=0.05, vmax=0.50, alpha = 1.0, origin='upper', extent=img_extent, zorder=5)

# Add states and provinces
shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=6)

# Add countries
shapefile = list(shpreader.Reader('..//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=7)

# Add continents
shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_coastline.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=8)
  
# Add coastlines, borders and gridlines
ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=False, zorder=9)

# Remove the outline border
ax.outline_patch.set_visible(False)
  
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Get the lats, lons and groups
lats_file=file_glm.variables['lat'][:]
lons_file=file_glm.variables['lon'][:]
dens_file=file_glm.variables['group'][:]
groups = dens_file[0,:,:]

# Getting smooth clusters for GLM
mout1 = gaussian_filter(groups, sigma=1.25, mode='constant', cval=0)
mout1[mout1 < 0.01] = np.nan
# Getting smooth clusters for GLM
mout2 = gaussian_filter(groups, sigma=1.00, mode='constant', cval=0)
mout2[mout2 < 0.01] = np.nan
# Getting smooth clusters for GLM
mout3 = gaussian_filter(groups, sigma=0.75, mode='constant', cval=0)
mout3[mout3 < 0.01] = np.nan

img1 = ax.pcolormesh(lons_file, lats_file, mout1, shading='None', vmin=0, vmax=4, alpha=0.4, cmap='BuPu_r', transform=ccrs.PlateCarree(), zorder=10)
img2 = ax.pcolormesh(lons_file, lats_file, mout2, shading='None', vmin=0, vmax=4, alpha=0.6, cmap='BuPu_r', transform=ccrs.PlateCarree(), zorder=11)
img3 = ax.pcolormesh(lons_file, lats_file, mout3, shading='None', vmin=0, vmax=50, alpha=0.8, cmap='Blues_r', transform=ccrs.PlateCarree(), zorder=12)
img4 = ax.pcolormesh(lons_file, lats_file, groups, shading='None',vmin=0, vmax=5000, alpha=0.4, cmap='binary', transform=ccrs.PlateCarree(), zorder=13)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Add a title
plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=14)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Add labels to specific coordinates

import configparser
conf = configparser.ConfigParser()
conf.read('..//Utils//Labels//labels_g16.ini')

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
my_logo = plt.imread('..//Logos//my_logo.png')
newax = fig.add_axes([0.01, 0.03, 0.10, 0.10], anchor='SW', zorder=12) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
newax.imshow(my_logo)
newax.axis('off')

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
