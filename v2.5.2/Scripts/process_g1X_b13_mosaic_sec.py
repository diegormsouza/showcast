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
from matplotlib.image import imread                          # Read an image from a file into an array
from cartopy.feature.nightshade import Nightshade            # Draws a polygon where there is no sunlight for the given datetime.
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

# Band 13 file
path_ch13_18 = (sys.argv[1])
#path_ch13 = ("..//Samples//OR_ABI-L2-CMIPF-M6C13_G16_s20192931650344_e20192931700064_c20192931700142.nc")
#path_ch13 = ("..//Samples//OR_ABI-L2-CMIPF-M6C13_G17_s20192931650341_e20192931659418_c20192931659465-132020_0.nc")

# For the log
path = path_ch13_18

#print(path)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Remove the identification
path_ch13_18 = path_ch13_18[:-4]

# Get the Band 15, same file
osystem = platform.system()
if osystem == "Windows":
    path_ch13_19 = re.sub('Band13\\\\OR_ABI-L2-CMIPF*(.*)', '', path_ch13_18)
    path_ch13_19 = re.sub('GOES-T-CMI-Imagery\\\\', '', path_ch13_19)
else:
    path_ch13_19 = re.sub('Band13/OR_ABI-L2-CMIPF*(.*)', '', path_ch13_18)
    path_ch13_19 = re.sub('GOES-T-CMI-Imagery//', '', path_ch13_19)
    print(path_ch13_16)

# Get the start of scan from the file name
scan_start = (path_ch13_18[path_ch13_18.find("_s")+2:path_ch13_18.find("_e")])
scan_start = scan_start[0:11]

print(path_ch13_19+'GOES-R-CMI-Imagery//Band13//OR_ABI-L2-CMIPF-M*C13_G1*.nc')
print(scan_start)

file = []
for filename in sorted(glob.glob(path_ch13_19+'GOES-R-CMI-Imagery//Band13//OR_ABI-L2-CMIPF-M*C13_G1*.nc')):
    file.append(filename)
    
#print(file)
    
# Seek for a GOES-16 file (same time) in the directory
matching = [s for s in file if scan_start in s]     

# If the file is not found, exit the loop
if not matching:
    print("One of the files necessary to create the composite is not available yet. Exiting Script.")
    sys.exit()
else: # If the file is found, continue
    print("File OK!")
    matching = matching[0]
    index = file.index(matching)
    path_ch13_19 = file[index]

print(path_ch13_18)
print(path_ch13_19)

# GOES-R: [-156.29, -81.32, 6.29, 81.32]
# GOES-R: [-106.29, -81.32, 6.29, 81.32]
# GOES-S: [-216.29, -81.32, -54.29, 81.32]
# GOES-S: [-216.29, -81.32, -106.29, 81.32]
# TOTAL_SAT: [-216.29, -81.32, 6.29, 81.32]
# TOTAL_VIS: [-222.0, -90.00, 10.0, 90.00]

satel_extent = [-216.29, -81.32, 6.29, 81.32]
total_extent = [-222.0, -83.00, 10.0, 83.00]
extent_19 = [-106.29, -81.32, 6.29, 81.32]
extent_18 = [-216.29, -81.32, -106.29, 81.32]
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Read the image
file = Dataset(path_ch13_18)

# Read the satellite 
satellite = getattr(file, 'platform_ID')

# Read the band number
band = str(file.variables['band_id'][0]).zfill(2)

# Product naming
product = "BAND" + band

# Add "SEC" to the product name to identify that is a sector product
product = product + "_SEC"

# Desired resolution
resolution = int(sys.argv[6])

# Read the resolution
band_resolution_km = getattr(file, 'spatial_resolution')
band_resolution_km = float(band_resolution_km[:band_resolution_km.find("km")])

# Division factor to reduce image size
f = math.ceil(float(resolution / band_resolution_km))

# Read the central longitude
longitude = file.variables['goes_imager_projection'].longitude_of_projection_origin

# Read the semi major axis
a = file.variables['goes_imager_projection'].semi_major_axis

# Read the semi minor axis
b = file.variables['goes_imager_projection'].semi_minor_axis

# Calculate the image extent 
h = file.variables['goes_imager_projection'].perspective_point_height
x1 = file.variables['x_image_bounds'][0] * h 
x2 = file.variables['x_image_bounds'][1] * h 
y1 = file.variables['y_image_bounds'][1] * h 
y2 = file.variables['y_image_bounds'][0] * h 

# Getting the file time and date
add_seconds = int(file.variables['time_bounds'][0])
date = datetime(2000,1,1,12) + timedelta(seconds=add_seconds)
date_formated = date.strftime('%Y-%m-%d %H:%M UTC')
date_file = date.strftime('%Y%m%d%H%M')
year = date.strftime('%Y')
month = date.strftime('%m')
day = date.strftime('%d')
hour = date.strftime('%H')
minutes = date.strftime('%M')

# GOES-R: [-156.29, -81.32, 6.29, 81.32]
# GOES-R: [-106.29, -81.32, 6.29, 81.32]
# GOES-S: [-216.29, -81.32, -54.29, 81.32]
# GOES-S: [-216.29, -81.32, -106.29, 81.32]
# TOTAL_SAT: [-216.29, -81.32, 6.29, 81.32]
# TOTAL_VIS: [-222.0, -90.00, 10.0, 90.00]

# Choose the visualization extent (min lon, min lat, max lon, max lat)
#extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]
extent = [-216.29, -81.32, -106.29, 81.32]

# Variable to remap
variable = "CMI"

# Call the reprojection funcion
grid = remap(path_ch13_18, variable, extent, resolution, h, a, b, longitude, x1, y1, x2, y2)
     
# Read the data returned by the function 
data_18 = grid.ReadAsArray()
data_18[data_18 == min(data_18[0])] = np.nan
#data_17[data_17 == max(data_17[0])] = np.nan
print(data_18.shape)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Read the image
file = Dataset(path_ch13_19)

# Read the satellite 
satellite = getattr(file, 'platform_ID')

# Read the band number
band = str(file.variables['band_id'][0]).zfill(2)

# Product naming
product = "BAND" + band

# Add "SEC" to the product name to identify that is a sector product
product = product + "_SEC"

# Desired resolution
resolution = int(sys.argv[6])

# Read the resolution
band_resolution_km = getattr(file, 'spatial_resolution')
band_resolution_km = float(band_resolution_km[:band_resolution_km.find("km")])

# Division factor to reduce image size
f = math.ceil(float(resolution / band_resolution_km))

# Read the central longitude
longitude = file.variables['goes_imager_projection'].longitude_of_projection_origin

# Read the semi major axis
a = file.variables['goes_imager_projection'].semi_major_axis

# Read the semi minor axis
b = file.variables['goes_imager_projection'].semi_minor_axis

# Calculate the image extent 
h = file.variables['goes_imager_projection'].perspective_point_height
x1 = file.variables['x_image_bounds'][0] * h 
x2 = file.variables['x_image_bounds'][1] * h 
y1 = file.variables['y_image_bounds'][1] * h 
y2 = file.variables['y_image_bounds'][0] * h 

# Getting the file time and date
add_seconds = int(file.variables['time_bounds'][0])
date = datetime(2000,1,1,12) + timedelta(seconds=add_seconds)
date_formated = date.strftime('%Y-%m-%d %H:%M UTC')
date_file = date.strftime('%Y%m%d%H%M')
year = date.strftime('%Y')
month = date.strftime('%m')
day = date.strftime('%d')
hour = date.strftime('%H')
minutes = date.strftime('%M')

# GOES-R: [-156.29, -81.32, 6.29, 81.32]
# GOES-R: [-106.29, -81.32, 6.29, 81.32]
# GOES-S: [-216.29, -81.32, -54.29, 81.32]
# GOES-S: [-216.29, -81.32, -106.29, 81.32]
# TOTAL_SAT: [-216.29, -81.32, 6.29, 81.32]
# TOTAL_VIS: [-222.0, -90.00, 10.0, 90.00]

# Choose the visualization extent (min lon, min lat, max lon, max lat)
#extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]
extent = [-106.29, -81.32, 6.29, 81.32]

# Variable to remap
variable = "CMI"

# Call the reprojection funcion
grid = remap(path_ch13_19, variable, extent, resolution, h, a, b, longitude, x1, y1, x2, y2)
     
# Read the data returned by the function 
data_19 = grid.ReadAsArray()
data_19[data_19 == min(data_19[0])] = np.nan
#data_16[data_16 == max(data_16[0])] = np.nan
print(data_19.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

#data = np.concatenate((data_17, data_16), axis=1)
#print(data.shape)

if int(band) <= 6:
    # Converts a CPT file to be used in Python
    cpt = loadCPT(main_dir + '//Colortables//Square Root Visible Enhancement.cpt')
    cmap = LinearSegmentedColormap('cpt', cpt)
    vmin = 0.0
    vmax = 1.0
    thick_interval = 0.1
elif int(band) == 7:
    # Converts a CPT file to be used in Python
    cpt = loadCPT(main_dir + '//Colortables//SVGAIR2_TEMP.cpt')
    cmap = LinearSegmentedColormap('cpt', cpt) 
    #data_16 -= 273.15
    #data_17 -= 273.15
    vmin = -112.15
    vmax = 56.85
    thick_interval = 10.0
elif int(band) > 7 and int(band) < 11:
    # Converts a CPT file to be used in Python
    cpt = loadCPT(main_dir + '//Colortables//SVGAWVX_TEMP.cpt')
    cmap = LinearSegmentedColormap('cpt', cpt) 
    #data_16 -= 273.15
    #data_17 -= 273.15
    vmin = -112.15
    vmax = 56.85
    thick_interval = 10.0
elif int(band) > 10 and int(band) < 14:
    # Converts a CPT file to be used in Python
    cpt = loadCPT(main_dir + '//Colortables//IR4AVHRR6.cpt')   
    cmap = LinearSegmentedColormap('cpt', cpt) 
    #data_16 -= 273.15
    #data_17 -= 273.15    
    vmin = -103.0
    vmax = 84.0
    thick_interval = 10.0
elif int(band) == 14:
    # Converts a CPT file to be used in Python
    cpt = loadCPT(main_dir + '//Colortables//SVGAIR_TEMP.cpt')   
    cmap = LinearSegmentedColormap('cpt', cpt) 
    #data_16 -= 273.15
    #data_17 -= 273.15   
    vmin = -112.15
    vmax = 56.85
    thick_interval = 10.0
elif int(band) == 15:
    # Converts a CPT file to be used in Python
    cpt = loadCPT(main_dir + '//Colortables//SVGAIR_TEMP.cpt')   
    cmap = LinearSegmentedColormap('cpt', cpt) 
    #data_16 -= 273.15
    #data_17 -= 273.15   
    vmin = -112.15
    vmax = 56.85
    thick_interval = 10.0

    
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------   
# Plot configuration
plot_config = {
"resolution": band_resolution_km, 
"dpi": 150, 
"states_color": 'white', "states_width": (data_18.shape[0]) * 0.00018, 
"countries_color": 'gold', "countries_width": (data_18.shape[0]) * 0.00012,
"continents_color": 'gold', "continents_width": (data_18.shape[0]) * 0.00025,
"grid_color": 'white', "grid_width": (data_18.shape[0]) * 0.00025, "grid_interval": 10.0,
"vmin": vmin, "vmax": vmax, "cmap": cmap,
"title_text": "GOES-18 and GOES-19" + " Band " + band + " Mosaic", "title_size": int((data_18.shape[1]+data_19.shape[1]) * 0.003), "title_x_offset": int((data_18.shape[1]+data_19.shape[1]) * 0.01), "title_y_offset": (data_18.shape[0]) - int((data_19.shape[0]) * 0.038), 
"thick_interval": thick_interval, "cbar_labelsize": int((data_18.shape[0]) * 0.005), "cbar_labelpad": -int((data_18.shape[0]) * 0),
"file_name_id_1": "G1X",  "file_name_id_2": "B13MOS_SEC" 
}
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
fig = plt.figure(figsize=((data_18.shape[1]+data_19.shape[1])/float(plot_config["dpi"]), (data_18.shape[0])/float(plot_config["dpi"])), dpi=plot_config["dpi"])
#print(data_17.shape[1])
#print(data_17.shape[0])
#print(data_16.shape[1])
#print(data_16.shape[0])

# Define the projection
cent_lon = 115.0
proj = ccrs.PlateCarree(central_longitude=-cent_lon)
img_proj = ccrs.PlateCarree(central_longitude=0.0)

# Use the PlateCarree projection in cartopy
ax = plt.axes([0, 0, 1, 1], projection=proj)
ax.set_extent([total_extent[0], total_extent[2], total_extent[1], total_extent[3]], crs=img_proj)

# Define the image extent
img_extent_18 = [extent_18[0]+cent_lon, extent_18[2]+cent_lon, extent_18[1], extent_18[3]]
img_extent_19 = [extent_19[0]+cent_lon, extent_19[2]+cent_lon, extent_19[1], extent_19[3]]

# Add a background image
#ax.stock_img()
fname = os.path.join(main_dir + '//Maps//', 'land_ocean_ice_8192.jpg')
ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)
#date = datetime(int(year), int(month), int(day), int(hour))
#ax.add_feature(Nightshade(date, alpha=0.7), zorder=2)
 
# Plot the image
# FOR CONVENTIONAL PLOT =========================================
#img1 = ax.imshow(data_17, vmin=plot_config["vmin"], vmax=plot_config["vmax"], origin='upper', extent=img_extent_17, cmap=plot_config["cmap"], zorder=2)
#img2 = ax.imshow(data_16, vmin=plot_config["vmin"], vmax=plot_config["vmax"], origin='upper', extent=img_extent_16, cmap=plot_config["cmap"], zorder=2)

# FOR HIGH CLOUDS (ENHANCED) ONLY ===============================
#print("First layer...")
# Apply range limits for clean IR channel
data_181 = data_18
data_181 = np.maximum(data_181, 90)
data_181 = np.minimum(data_181, 313)
# Normalize the channel between a range
data_181 = (data_181-90)/(313-90)
# Invert colors
data_181 = 1 - data_181
img1 = ax.imshow(data_181, cmap='gray', vmin=0.1, vmax=0.25, alpha = 0.6, origin='upper', extent=img_extent_18, zorder=3)

#print("Second layer...")
# SECOND LAYER
data_182 = data_181
data_182[data_182 < 0.20] = np.nan
img2 = ax.imshow(data_182, cmap='gray', vmin=0.15, vmax=0.30, alpha = 1.0, origin='upper', extent=img_extent_18, zorder=4)

#print("Third layer...")
# THIRD LAYER
data_183 = data_18
data_183 = data_18 - 273.15
data_183[np.logical_or(data_183 < -80, data_183 > -28)] = np.nan
img3 = ax.imshow(data_183, cmap=cmap, vmin=-103, vmax=84, alpha=1.0, origin='upper', extent=img_extent_18, zorder=5)

#print("First layer...")
# Apply range limits for clean IR channel
data_191 = data_19
data_191 = np.maximum(data_191, 90)
data_191 = np.minimum(data_191, 313)
# Normalize the channel between a range
data_191 = (data_191-90)/(313-90)
# Invert colors
data_191 = 1 - data_191
img1 = ax.imshow(data_191, cmap='gray', vmin=0.1, vmax=0.25, alpha = 0.6, origin='upper', extent=img_extent_19, zorder=3)

#print("Second layer...")
# SECOND LAYER
data_192 = data_191
data_192[data_192 < 0.20] = np.nan
img2 = ax.imshow(data_192, cmap='gray', vmin=0.15, vmax=0.30, alpha = 1.0, origin='upper', extent=img_extent_19, zorder=4)

#print("Third layer...")
# THIRD LAYER
data_193 = data_19
data_193 = data_19 - 273.15
data_193[np.logical_or(data_193 < -80, data_193 > -28)] = np.nan
img3 = ax.imshow(data_193, cmap=cmap, vmin=-103, vmax=84, alpha=1.0, origin='upper', extent=img_extent_19, zorder=5)

# To put colorbar inside picture
axins1 = inset_axes(ax, width="100%", height="1%", loc='lower center', borderpad=0.0)
  
# Add states and provinces
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=3)

# Add countries
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=4)

# Add continents
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_coastline.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=5)
  
# Add coastlines, borders and gridlines
gl = ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=True, zorder=6)
gl.left_labels = True; gl.right_labels = False; gl.top_labels = True; gl.bottom_labels = False
gl.xpadding = -plot_config["cbar_labelsize"]; gl.ypadding = -plot_config["cbar_labelsize"]
gl.ylabel_style = {'color': 'white', 'size': plot_config["cbar_labelsize"], 'weight': 'bold'}
gl.xlabel_style = {'color': 'white', 'size': plot_config["cbar_labelsize"], 'weight': 'bold'}

# Remove the outline border
ax.outline_patch.set_visible(False)

# Add a title
plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=7)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Add labels to specific coordinates

import configparser
conf = configparser.ConfigParser()
conf.read(main_dir + '//Utils//Labels//labels_g16.ini')

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

# Add a colorbar
ticks = np.arange(plot_config["vmin"], plot_config["vmax"], plot_config["thick_interval"]).tolist()     
ticks = plot_config["thick_interval"] * np.round(np.true_divide(ticks,plot_config["thick_interval"]))
ticks = ticks[1:]
cb = fig.colorbar(img3, cax=axins1, orientation="horizontal", ticks=ticks)
cb.outline.set_visible(False)
cb.ax.tick_params(width = 0)
cb.ax.xaxis.set_tick_params(pad=plot_config["cbar_labelpad"])
cb.ax.xaxis.set_ticks_position('top')
cb.ax.tick_params(axis='x', colors='black', labelsize=plot_config["cbar_labelsize"])

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

satellite = "G1X"
product = "B13MOS_SEC"

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
os.remove(path_ch13_19 +'.aux.xml')
os.remove(path_ch13_18 +'.aux.xml')

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Put the processed file on the log
import datetime # Basic Date and Time types
with open(main_dir + '//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
 log.write(str(datetime.datetime.now()))
 log.write('\n')
 log.write(path + '\n')
 log.write(path + '\n')
 log.write('\n')
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

print('Total processing time:', round((t.time() - start),2), 'seconds.') 
 