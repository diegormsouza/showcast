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
from matplotlib.image import imread                          # Read an image from a file into an array
import os                                                    # Miscellaneous operating system interfaces
from os.path import dirname, abspath                         # Return a normalized absolutized version of the pathname path 
import sys                                                   # Import the "system specific parameters and functions" module
from cartopy.feature.nightshade import Nightshade            # Draws a polygon where there is no sunlight for the given datetime.
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

# Image path
path = (sys.argv[1])

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

# Read the image
file = Dataset(path)

# Read the satellite 
satellite = getattr(file, 'platform_ID')

# Read the product name
prod_name = getattr(file, 'title')

# Desired resolution
resolution = int(sys.argv[6])

# Read the resolution
band_resolution_km = getattr(file, 'spatial_resolution')
band_resolution_km = float(band_resolution_km[:band_resolution_km.find("km")])

# Division factor to reduce image size
f = math.ceil(float(resolution / band_resolution_km))

# Read the central longitude
longitude = file.variables['goes_imager_projection'].longitude_of_projection_origin

# Calculate the image extent 
h = file.variables['goes_imager_projection'].perspective_point_height
x = file.variables['x_image_bounds'] * h 
y = file.variables['y_image_bounds'] * h 

# Reading the file time and date
add_seconds = int(file.variables['time_bounds'][0])
date = datetime(2000,1,1,12) + timedelta(seconds=add_seconds)
date_formated = date.strftime('%Y-%m-%d %H:%M UTC')
date_file = date.strftime('%Y%m%d%H%M')
year = date.strftime('%Y')
month = date.strftime('%m')
day = date.strftime('%d')
hour = date.strftime('%H')
minutes = date.strftime('%M')

# Read the smoke data
data_smk = file.variables['Smoke'][:,:][::f ,::f]
# Convert from int16 to uint16
data_smk = data_smk.astype(np.float64)

# Read the dust data
data_dst = file.variables['Dust'][:,:][::f ,::f]
# Convert from int16 to uint16
data_dst = data_dst.astype(np.float64)

# Join both 
#data_smk_dst = np.where(np.isnan(data_smk), data_dst, data_smk) 

# Read the DQF
data_DQF = file.variables['DQF'][:,:][::f ,::f]
# Convert from int16 to uint16
data_DQF = data_DQF.astype(np.float64)

#data_DQF[data_smk_dst != 1] = np.nan

#data_smk = data_DQF   
#data_smk[data_smk == 1] = np.nan             # Invalid Smoke Detection
#data_smk[data_smk == 2] = np.nan             # Invalid Dust Detection
#data_smk[data_smk == 64] = np.nan            # Sunglint
#data_smk[data_smk == 65] = np.nan            # Sunglint 
#data_smk[data_smk == 128] = np.nan           # Outside Valid Area
#data_smk[data_smk == 129] = np.nan           # Outside Valid Area
#data_smk[data_smk == 130] = np.nan           # Outside Valid Area
#data_smk[data_smk == 0] = 3


# Remove some pixels
#data_DQF[data_dst != 1 and data_smk != 1] = np.nan

# Convert from int16 to uint16
#data_DQF = data_DQF.astype(np.float64)
#data_DQF[data_smk != 1] = np.nan
#data_dst = data_DQF   
#data_dst[data_dst == 1] = np.nan             # Invalid Smoke Detection
#data_dst[data_dst == 2] = np.nan             # Invalid Dust Detection
#data_dst[data_dst == 64] = np.nan            # Sunglint
#data_dst[data_dst == 65] = np.nan            # Sunglint 
#data_dst[data_dst == 128] = np.nan           # Outside Valid Area
#data_dst[data_dst == 129] = np.nan           # Outside Valid Area
#data_dst[data_dst == 130] = np.nan           # Outside Valid Area
#data_dst[data_dst == 0] = 15 

# Removing values that doesn't represent smoke and dust
data_DQF[data_DQF == 0] = np.nan
data_DQF[data_DQF == 1] = np.nan
data_DQF[data_DQF == 3] = np.nan
data_DQF[data_DQF == 64] = np.nan
data_DQF[data_DQF == 65] = np.nan
data_DQF[data_DQF == 66] = np.nan
data_DQF[data_DQF == 67] = np.nan
data_DQF[data_DQF == 128] = np.nan
data_DQF[data_DQF == 129] = np.nan
data_DQF[data_DQF == 130] = np.nan
data_DQF[data_DQF == 131] = np.nan
data_DQF[data_DQF > 131] = np.nan

# Join both smoke and dust datasets, not considering the nans
data = data_DQF
# Join both smoke and dust datasets, not considering the nans
#data = np.where(1, data_dst, data_smk) 
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# ADPF
#product = 'Smoke'
cmap = 'jet'
vmin = 0
vmax = 50
thick_interval = 10
product = "AERDET_FDK"
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Plot configuration
plot_config = {
"resolution": band_resolution_km, 
"dpi": 150, 
"states_color": 'white', "states_width": data.shape[0] * 0.00006, 
"countries_color": 'gold', "countries_width": data.shape[0] * 0.00012,
"continents_color": 'gold', "continents_width": data.shape[0] * 0.00025,
"grid_color": 'white', "grid_width": data.shape[0] * 0.00025, "grid_interval": 10.0,
"vmin": vmin, "vmax": vmax, "cmap": cmap,
"title_text": "GOES-19 " + prod_name, "title_size": int(data.shape[1] * 0.005), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[0] - int(data.shape[0] * 0.016), 
"thick_interval": thick_interval, "cbar_labelsize": int(data.shape[0] * 0.005), "cbar_labelpad": -int(data.shape[0] * 0.0),
"file_name_id_1": "G19",  "file_name_id_2": product 
}

# Choose the plot size (width x height, in inches)
fig = plt.figure(figsize=(data.shape[1]/float(plot_config["dpi"]), data.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])
  
# Define the projection
proj = ccrs.Geostationary(central_longitude=longitude, satellite_height=h)
#img_extent = (x1,x2,y1,y2)
img_extent = (x.min(), x.max(), y.min(), y.max())

# Use the Geostationary projection in cartopy
ax = plt.axes([0, 0, 1, 1], projection=proj)

ax.background_patch.set_fill(False)
# Add a background image
#ax.stock_img()
#fname = os.path.join(main_dir + '//Maps//', 'land_ocean_ice_8192.jpg')
#ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)
#date = datetime(int(year), int(month), int(day), int(hour))
#ax.add_feature(Nightshade(date, alpha=0.7), zorder=2)

# Plot the image
img = ax.imshow(data, vmin=plot_config["vmin"], vmax=plot_config["vmax"], origin='upper', extent=img_extent, cmap=plot_config["cmap"], zorder=3)

# To put colorbar inside picture
axins1 = inset_axes(ax, width="100%", height="1%", loc='lower center', borderpad=0.0)
  
# Add states and provinces
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=4)

# Add countries
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=5)

# Add continents
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_coastline.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=6)
  
# Add coastlines, borders and gridlines
ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=False, zorder=7)

# Remove the outline border
ax.outline_patch.set_visible(False)
  
# Add a title
plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=8)

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

# Add a legend to the plot
my_legend = plt.imread(main_dir + '//Legends//AEROSSOL_legend.png')
newax = fig.add_axes([0.87, 0.87, 0.12, 0.12], anchor='NE', zorder=13) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
newax.imshow(my_legend)
newax.axis('off')

# Add a colorbar
ticks = np.arange(plot_config["vmin"], plot_config["vmax"], plot_config["thick_interval"]).tolist()     
ticks = plot_config["thick_interval"] * np.round(np.true_divide(ticks,plot_config["thick_interval"]))
ticks = ticks[1:]
cb = fig.colorbar(img, cax=axins1, orientation="horizontal", ticks=ticks)
cb.outline.set_visible(False)
cb.ax.tick_params(width = 0)
cb.ax.xaxis.set_tick_params(pad=plot_config["cbar_labelpad"])
cb.ax.xaxis.set_ticks_position('top')
cb.ax.tick_params(axis='x', colors='lightgray', labelsize=plot_config["cbar_labelsize"])

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
