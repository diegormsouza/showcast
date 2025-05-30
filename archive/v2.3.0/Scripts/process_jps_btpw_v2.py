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
from netCDF4 import Dataset                                  # Read / Write NetCDF4 files
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
# Ignore possible warnings
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start_time = t.time()  

# SHOWCast directory:
main_dir = dirname(dirname(abspath(__file__)))

# Reading the file:
path = sys.argv[1]

# Detecting if is BTPW or PCT:
product = (path[path.find("BHP-")+4:path.find("_v")])

# Detecting time and date:
date = (path[path.find("_c")+2:path.find(".nc")])
date_file = date
date_formated = date[0:4] + "-" + date[4:6] + "-" + date[6:8] + " " + date [8:10] + ":" + date [10:12] + " UTC"

# Define the extent
extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]
min_lon = extent[0]; max_lon = extent[2]; min_lat = extent[1]; max_lat = extent[3]

# Define KM_PER_DEGREE
KM_PER_DEGREE = 111.32

# Calculate the total number of degrees in lat and lon
deg_lon = extent[2] - extent[0]
deg_lat = extent[3] - extent[1]

# Calculate the number of pixels
resolution = int(sys.argv[6])
sizex = (KM_PER_DEGREE * deg_lon) /  resolution
sizey = (KM_PER_DEGREE * deg_lat) /  resolution

# Open the file using the NetCDF4 library
nc = Dataset(path)

# Reading lats and lons 
lats = nc.variables['lat'][:]
lons = nc.variables['lon'][:]

# latitude lower and upper index
latli = np.argmin( np.abs( lats - extent[1] ) )
latui = np.argmin( np.abs( lats - extent[3] ) )
 
# longitude lower and upper index
lonli = np.argmin( np.abs( lons - extent[0] ) )
lonui = np.argmin( np.abs( lons - extent[2] ) )

# Extract the Sea Surface Temperature
data = nc.variables[product][latli:latui , lonli:(lonui)]

# Return a reshaped matrix
data = data.squeeze()
#print(data)
#print(data.shape)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

if (product == "TPW"):
    product = "BTPW"
    nomenclature = "MUL_BLETPW"
    satellite = "MUL"
    product = "BLETPW"
    colors = ["#bc8462", "#ae656f", "#a44a79", "#962e97", "#6158c5", "#2b8ffb", "#5fcdff", "#94fff0", "#a5ff94", "#fff88c", "#ffbf52", "#ec7b27", "#b84827", "#a1333d", "#bd5478", "#cc6a99", "#d982b8"]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    vmin = 0
    vmax = 80
    thick_interval = 5
    prod_title = "Blended Precipitable Water"
elif (product == "PCT"):
    product = "BPCT"
    nomenclature = "MUL_BLEPCT"
    satellite = "MUL"
    product = "BLEPCT"
    colors = ["#351a00", "#8b5226", "#ce9f80", "#dcb69f", "#ecd1c2", "#7af2ff", "#3ae4ff", "#03aced", "#007a99", "#b2b200", "#cccc00", "#eaea00", "#ffff00"]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    vmin = 1
    vmax = 300
    thick_interval = 20
    prod_title = "Precipitable Water Anomaly"
elif (product == "RR"):
    product = "BRRT"
    nomenclature = "MUL_BLERRT"
    satellite = "MUL"
    product = "BLERRT"
    #colors = ["#351a00", "#8b5226", "#ce9f80", "#dcb69f", "#ecd1c2", "#7af2ff", "#3ae4ff", "#03aced", "#007a99", "#b2b200", "#cccc00", "#eaea00", "#ffff00"]
    #cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    cmap = 'jet'
    vmin = 0
    vmax = 10
    thick_interval = 0.5
    prod_title = "Blended Rain Rate"
    data[data == 0] = np.nan
	
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Plot configuration
plot_config = {
"resolution": resolution, 
"dpi": 150, 
"states_color": 'white', "states_width": data.shape[0] * 0.00024, 
"countries_color": 'black', "countries_width": data.shape[0] * 0.00036,
"continents_color": 'black', "continents_width": data.shape[0] * 0.00050,
"grid_color": 'white', "grid_width": data.shape[0] * 0.00025, "grid_interval": 10.0,
"vmin": vmin, "vmax": vmax, "cmap": cmap,
"title_text": "Multimission " + prod_title + " ", "title_size": int(data.shape[1] * 0.0025), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[0] - int(data.shape[0] * 0.032), 
"thick_interval": thick_interval, "cbar_labelsize": int(data.shape[0] * 0.005), "cbar_labelpad": -int(data.shape[0] * 0.0),
"file_name_id_1": "MUL",  "file_name_id_2": product + "_SEC"
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
#fname = os.path.join(main_dir + '//Maps//', 'land_ocean_ice_8192.jpg')
fname = os.path.join(main_dir + '//Maps//', 'natural-earth-1_large2048px.jpg')
ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)
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
'''
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
'''
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
cb = fig.colorbar(img, cax=axins1, orientation="horizontal", ticks=ticks)
cb.outline.set_visible(False)
cb.ax.tick_params(width = 0)
cb.ax.xaxis.set_tick_params(pad=plot_config["cbar_labelpad"])
cb.ax.xaxis.set_ticks_position('top')
cb.ax.tick_params(axis='x', colors='black', labelsize=plot_config["cbar_labelsize"])

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------   
       
product = product + "_SEC"
          
# Create the satellite output directory if it doesn't exist
out_dir = main_dir + '//Output//' + satellite
if not os.path.exists(out_dir):
  os.mkdir(out_dir)

# Create the product output directory if it doesn't exist
out_dir = main_dir + '//Output//' + satellite + '//' + product + '//'
if not os.path.exists(out_dir):
  os.mkdir(out_dir)
                     
# Save the image
plt.savefig(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.png', facecolor='black')#, bbox_inches='tight', pad_inches=0, facecolor='black')

# Update the animation
nfiles = 20
update(satellite, product, nfiles)

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

print('Total processing time:', round((t.time() - start_time),2), 'seconds.') 