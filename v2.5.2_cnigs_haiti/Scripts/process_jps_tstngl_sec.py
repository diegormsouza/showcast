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
import pygrib                                                # Provides a high-level interface to the ECWMF ECCODES C library for reading GRIB files
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
from matplotlib.colors import LinearSegmentedColormap        # Linear interpolation for color maps
from mpl_toolkits.axes_grid1.inset_locator import inset_axes # Add a child inset axes to this existing axes.
import matplotlib.colors                                     # Matplotlib colors
import matplotlib.pyplot as plt                              # Plotting library
import numpy as np                                           # Scientific computing with Python
import cartopy, cartopy.crs as ccrs                          # Plot maps
import cartopy.io.shapereader as shpreader                   # Import shapefiles
import time as t                                             # Time access and conversion
import sys                                                   # Import the "system specific parameters and functions" module
import math                                                  # Import math
from matplotlib.image import imread                          # Read an image from a file into an array
import os                                                    # Miscellaneous operating system interfaces
from os.path import dirname, abspath                         # Return a normalized absolutized version of the pathname path 
from html_update import update                               # Update the HTML animation 
import warnings                                              # Warning control
warnings.filterwarnings("ignore")
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()  

# SHOWCast directory:
main_dir = dirname(dirname(abspath(__file__)))

# Choose the visualization extent (min lon, min lat, max lon, max lat)
extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]

# Desired resolution
resolution = int(sys.argv[6])

# Define KM_PER_DEGREE
KM_PER_DEGREE = 111.32

# Compute grid dimension
sizex = int(((extent[2] - extent[0]) * KM_PER_DEGREE) / resolution) 
sizey = int(((extent[3] - extent[1]) * KM_PER_DEGREE) / resolution) 

# Image path
path = (sys.argv[1])

# Open the GRIB file
grib = pygrib.open(path)

# To print all the variables to a txt file
#f = open("toast_variables.txt", "w")
#for variables in grib:
#    print(variables, file=f)
#f.close()

# Read the TOAST
toast = grib.select(name='Total column ozone')[0]
toast, lats, lons = toast.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# To smooth the data
import scipy.ndimage
toast = scipy.ndimage.zoom(toast, 3)
lats = scipy.ndimage.zoom(lats, 3)
lons = scipy.ndimage.zoom(lons, 3)

# Get the data from the file name
date = path[path.find("OMPS_")+5:path.find(".grb")]
year = date[0:4]
month = date[4:6]
day = date[6:8]
date_formated = year + '-' + month + '-' + day

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Create the color scale 
#colors = ["#d3d2d2", "#bcbcbc", "#969696", "#1464d2", "#1e6eeb", "#2882f0", "#3c96f5", "#50a5f5", "#78b9fa", "#96d2fa", "#b4f0fa", "#1eb41e", "#37d23c", "#50f050", "#78f573", "#96f58c", "#b4faaa", "#c8ffbe", "#ffe878", "#ffc03c", "#ffa000", "#ff6000", "#ff3200", "#e11400", "#c00000", "#a50000", "#785046", "#8c6359", "#b48b82", "#e1beb4"]
#cmap = matplotlib.colors.ListedColormap(colors)
#cmap.set_over('#fadad5')
#cmap.set_under('#e5e5e5')
cmap = "nipy_spectral"

vmin = 100
vmax = 500
thick_interval = 50

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------    

# Product name
satellite = "JPS"
product   = "TSTNGL_SEC"

# Plot configuration
plot_config = {
"resolution": resolution, 
"dpi": 150, 
"states_color": 'white', "states_width": sizey * 0.00006, 
"countries_color": 'white', "countries_width": sizey * 0.00012,
"continents_color": 'white', "continents_width": sizey * 0.00025,
"grid_color": 'white', "grid_width": sizey * 0.00025, "grid_interval": 10.0,
"vmin": vmin, "vmax": vmax, "cmap": cmap,
"title_text": "Blended TOAST - SNPP OMPS & NOAA-20 CrIS Daily Total Ozone", "title_size": int(sizex * 0.004), "title_x_offset": int(sizex * 0.01), "title_y_offset": sizey - int(sizey * 0.032), 
"thick_interval": thick_interval, "cbar_labelsize": int(sizey * 0.005), "cbar_labelpad": -int(sizey * 0.00),
"file_name_id_1": satellite,  "file_name_id_2": product
}
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Choose the plot size (width x height, in inches)
fig = plt.figure(figsize=(sizex/float(plot_config["dpi"]), sizey/float(plot_config["dpi"])), dpi=plot_config["dpi"])
  
# Define the projection
proj = ccrs.PlateCarree()

# Use the PlateCarree projection in cartopy
ax = plt.axes([0, 0, 1, 1], projection=proj)
ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

# Define the image extent
img_extent = [extent[0], extent[2], extent[1], extent[3]]

# Add a background image
ax.stock_img()
#fname = os.path.join(main_dir + '//Maps//', 'land_ocean_ice_8192.jpg')
#ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)
#date = datetime(int(year), int(month), int(day), int(hour))
#ax.add_feature(Nightshade(date, alpha=0.7), zorder=2)

# Plot the image
img = ax.imshow(toast, vmin=plot_config["vmin"], vmax=plot_config["vmax"], origin='upper', extent=img_extent, cmap=plot_config["cmap"], alpha = 0.6, zorder=2)

# Add states and provinces
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=5)

# Add countries
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=6)

# Add continents
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_coastline.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=7)
  
# Add gridlines
gl = gl = ax.gridlines(color=plot_config["grid_color"], alpha=1.0, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=True, zorder=8)
gl.left_labels = True; gl.right_labels = False; gl.top_labels = True; gl.bottom_labels = False
gl.xpadding = -plot_config["cbar_labelsize"]; gl.ypadding = -plot_config["cbar_labelsize"]
gl.ylabel_style = {'color': 'white', 'size': plot_config["cbar_labelsize"], 'weight': 'bold'}
gl.xlabel_style = {'color': 'white', 'size': plot_config["cbar_labelsize"], 'weight': 'bold'}

# Remove the outline border
ax.outline_patch.set_visible(False)
  
# Add a title
plt.annotate(plot_config["title_text"] + " " + date_formated, xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=9)

# To put colorbar inside picture
axins1 = inset_axes(ax, width="1%", height="100%", loc='right', borderpad=0.0)

# Add a colorbar
ticks = np.arange(plot_config["vmin"], plot_config["vmax"], plot_config["thick_interval"]).tolist()     
ticks = plot_config["thick_interval"] * np.round(np.true_divide(ticks,plot_config["thick_interval"]))
ticks = ticks[1:]
cb = fig.colorbar(img, cax=axins1, orientation="vertical", ticks=ticks)
cb.set_label(label='Total ozone (Dobson)', size=plot_config["cbar_labelsize"], weight='bold')
cb.outline.set_visible(False)
cb.ax.tick_params(width = 0)
cb.ax.xaxis.set_tick_params(pad=plot_config["cbar_labelpad"])
cb.ax.yaxis.set_ticks_position('left')
cb.ax.yaxis.set_label_position('left')
cb.ax.tick_params(axis='y', colors='black', labelsize=plot_config["cbar_labelsize"])

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
newax = fig.add_axes([0.01, 0.01, 0.10, 0.10], anchor='SW', zorder=14) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
newax.imshow(my_logo)
newax.axis('off')

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Create the satellite output directory if it doesn't exist
out_dir = (sys.argv[7]) + satellite
if not os.path.exists(out_dir):
   os.mkdir(out_dir)

# Create the product output directory if it doesn't exist
out_dir = (sys.argv[7]) + satellite + '//' + product + '//'
if not os.path.exists(out_dir):
   os.mkdir(out_dir)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Save the image
plt.savefig(out_dir + satellite + '_' + product + '_' + date + '.png')

# Convert to webp
from PIL.WebPImagePlugin import Image          
im = Image.open(out_dir + satellite + '_' + product + '_' + date + '.png')
im.save(out_dir + satellite + '_' + product + '_' + date + '.webp', format = "WebP", lossless = True)
im.close()

# Update the animation
nfiles = 20
update(satellite, product, nfiles, sys.argv[7], sys.argv[8])

# Delete aux files
os.remove(out_dir + satellite + '_' + product + '_' + date + '.png')  

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

# Total processing time
print('Total processing time:', round((t.time() - start),2), 'seconds.') 
