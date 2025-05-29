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
import matplotlib.colors                                     # Matplotlib colors
import numpy as np                                           # Scientific computing with Python
import cartopy, cartopy.crs as ccrs                          # Plot maps
import cartopy.io.shapereader as shpreader                   # Import shapefiles
import time as t                                             # Time access and conversion
from osgeo import gdal, osr, ogr                             # Import GDAL
import os                                                    # Miscellaneous operating system interfaces
import sys                                                   # Import the "system specific parameters and functions" module
from html_update import update                               # Update the HTML animation 
from pyspectral.rayleigh import Rayleigh                     # Rayleigh correction
from pyproj import Proj                                      # Python interface to PROJ (cartographic projections and coordinate transformations library)
from matplotlib.image import imread                          # Read an image from a file into an array
gdal.PushErrorHandler('CPLQuietErrorHandler')
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()
 
# Read the image
file = (sys.argv[1])

# For the log
path = file

# Get the desired channel
channel = file[-3:]

# Remove the identification
file = file[:-4]

# Read the satellite 
satellite = "G16"

# Get times and dates
product = "DLCRGB_SEC"

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
#extent = [-156.29, -81.32, 6.29, 81.32]
 
# Desired resolution
band_resolution_km = int(sys.argv[6])
resolution = int(sys.argv[6])
#band_resolution_km = 8
#resolution = 8  
  
# Define KM_PER_DEGREE
KM_PER_DEGREE = 111.32

#print (resolution)
# Compute grid dimension
sizex = int(((extent[2] - extent[0]) * KM_PER_DEGREE) / band_resolution_km) 
sizey = int(((extent[3] - extent[1]) * KM_PER_DEGREE) / band_resolution_km) 
#print(sizex)
#print(sizey)

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

# Create the mosaic and cut
grid = gdal.Warp(path_out,[path_FDK, path_S01, path_S02, path_S03, path_S04, path_S05, path_S06, path_S07],options=gdal.WarpOptions(outputBounds = [extent[0], extent[1], extent[2], extent[3]], width = sizex, height = sizey))
grid = None
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Open the file:
raster = gdal.Open(path_out)

# File name
file_name = os.path.splitext(os.path.basename(path_out))[0] + "_SEC"

# Get times and dates
product = file_name[4:7] 
year = file_name[11:15]
month = file_name[15:17]
day = file_name[17:19]
hour = file_name[19:21]
minutes = file_name[21:23]

# Read the product name
title = "GOES-16 " + product + " " + "RGB" + " " + year + "-" + month + "-" + day + " " + hour + ":" + minutes + " " + "UTC"
date_formated = year + "-" + month + "-" + day + " " + hour + ":" + minutes + " " + "UTC"

# Product Name
product = "DLCRGB_SEC"

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Read the raster band as separate variable
Rb = raster.GetRasterBand(1)
R = Rb.ReadAsArray()

# Read the raster band as separate variable
Gb = raster.GetRasterBand(2)
G = Gb.ReadAsArray()

# Read the raster band as separate variable
Bb = raster.GetRasterBand(3)
B = Bb.ReadAsArray()

#print(R.shape)
#print(G.shape)
#print(B.shape)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

data1 = (R * (1.0 / 255.0)) 
data2 = (G * (1.0 / 255.0)) 
data3 = (B * (1.0 / 255.0)) 

# Delete the ancillary GeoTIFF
raster = None
Rb = None
Gb = None
Bb = None
gdal.Unlink(path_out)
gdal.Unlink(path_out + '_rep')

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

if (channel == "BS3"):
    data = data2
    band = "03"
    satellite = "G16"
    product = "BAND" + band
    product = product + "_SEC"
    # Converts a CPT file to be used in Python
    cpt = loadCPT('..//Colortables//Square Root Visible Enhancement.cpt')
    cmap = LinearSegmentedColormap('cpt', cpt)
    vmin = 0.0
    vmax = 1.0
    thick_interval = 0.1
if (channel == "BS5"):
    data = data1
    band = "05"
    satellite = "G16"
    product = "BAND" + band
    product = product + "_SEC"
    # Converts a CPT file to be used in Python
    cpt = loadCPT('..//Colortables//Square Root Visible Enhancement.cpt')
    cmap = LinearSegmentedColormap('cpt', cpt)
    vmin = 0.0
    vmax = 1.0
    thick_interval = 0.1
   
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------    
# Plot configuration
plot_config = {
"resolution": band_resolution_km, 
"dpi": 150, 
"states_color": 'white', "states_width": data.shape[0] * 0.00006, 
"countries_color": 'turquoise', "countries_width": data.shape[0] * 0.00012,
"continents_color": 'cyan', "continents_width": data.shape[0] * 0.00025,
"grid_color": 'white', "grid_width": data.shape[0] * 0.00025, "grid_interval": 10.0,
"vmin": vmin, "vmax": vmax, "cmap": cmap,
"title_text": "GOES-" + satellite[1:3] + " Band " + band, "title_size": int(data.shape[1] * 0.005), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[0] - int(data.shape[0] * 0.016), 
"thick_interval": thick_interval, "cbar_labelsize": int(data.shape[0] * 0.005), "cbar_labelpad": -int(data.shape[0] * 0.0),
"file_name_id_1": satellite,  "file_name_id_2": product
}
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Desired plot resolution
resolution = plot_config["resolution"]

# Choose the plot size (width x height, in inches)
# Diego: Put zero on both width and height because after reprojection both are equal
fig = plt.figure(figsize=(data.shape[1]/float(plot_config["dpi"]), data.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])

# Define the projection
# Diego: For some reason it only worked with the central longitude as "0.0" instead of "-75.0"
proj = ccrs.PlateCarree(central_longitude = 0.0)
ax = plt.axes([0, 0, 1, 1], projection = proj)
ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())
img_extent = (extent[0], extent[2], extent[1], extent[3])

# Add a background image
#ax.stock_img()
#fname = os.path.join('..//Maps//', 'land_ocean_ice_8192.jpg')
#ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)
#date = datetime(int(year), int(month), int(day), int(hour))
#ax.add_feature(Nightshade(date, alpha=0.7), zorder=2)

# Plot the image
img = ax.imshow(data, vmin=plot_config["vmin"], vmax=plot_config["vmax"], origin='upper', extent=img_extent, cmap=plot_config["cmap"], zorder=2)

# To put colorbar inside picture
axins1 = inset_axes(ax, width="100%", height="1%", loc='lower center', borderpad=0.0)

# Add states and provinces
shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=3)

# Add countries
shapefile = list(shpreader.Reader('..//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=4)

# Add continents
shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_coastline.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=5)
  
# Add coastlines, borders and gridlines
ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=False, zorder=6)

# Remove the outline border
ax.outline_patch.set_visible(False)

# Add a title
plt.annotate(plot_config["title_text"] + " " + date_formated, xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=7)

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
out_dir = '..//Output//' + satellite
if not os.path.exists(out_dir):
   os.mkdir(out_dir)

# Create the product output directory if it doesn't exist
out_dir = '..//Output//' + satellite + '//' + product + '//'
if not os.path.exists(out_dir):
   os.mkdir(out_dir)
 
file_name = satellite + "_" + product + "_" + year + month + day + hour + minutes
 
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
