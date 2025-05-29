#######################################################################################################
# LICENSE
# Copyright (C) 2020 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL
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
__copyright__ = "Copyright (C) 2020 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL"
__credits__ = ["Diego Souza"]
__license__ = "GPL"
__version__ = "2.2.0"
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
from remap import remap                                      # Import the Remap function
import re                                                    # Regular expression operations 
from osgeo import gdal, osr, ogr                             # Import GDAL
import glob                                                  # Unix style pathname pattern expansion
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

# Get the file name from path
file_name = os.path.splitext(os.path.basename(path))[0] 

# Get the file dir only
dir = path.replace(file_name + ".tif",'')

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Get the product type from the file name
if ("ABI" in file_name): 
	prod_name = "GOES-16 ABI Hourly Composite"
	product = "ABIHLY"
	product = product + "_SEC"
	hour = ''.join(filter(str.isdigit, file_name))[8:14] 
	#print(hour)
	band_resolution_km = 1
if ("global" in file_name): 
	prod_name = "Suomi-NPP and NOAA-20 VIIRS 5-day Composite (daily)"
	product = "VRS5DA"
	product = product + "_SEC"
	hour = "080000"
	band_resolution_km = 0.375
if ("joint" in file_name): 
	prod_name = "Joint VIIRS / ABI flood product (daily)"
	product = "JOINVA"
	product = product + "_SEC"
	hour = "080000"
	band_resolution_km = 0.375
print ("Product:", prod_name)

# Get the AOI/Full Disk part, from the file name
part = ''.join(filter(str.isdigit, file_name))[-3:] 
#print("Part:", part)

# Get the time and date from the file name
date = ''.join(filter(str.isdigit, file_name))[0:8] 
#print("Date:", date)

year = date[0:4]
month = date[4:6]
day = date[6:8]
hour = hour[0:2]
minutes = "00"

#print(year)
#print(month)
#print(day)
#print(hour)
#print(minutes)

date_formated = year + "-" + month + "-" + day + " " + hour + ":" + minutes + " " + "UTC"
date_file = year + month + day + hour + minutes

#print(date_formated)
#print(date_file)

# Main folder name
satellite = "FLD"

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Choose the visualization extent (min lon, min lat, max lon, max lat)
extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]

# Desired resolution
band_resolution_km = float(sys.argv[6])
resolution = float(sys.argv[6])
    
# Define KM_PER_DEGREE
KM_PER_DEGREE = 111.32

#print (resolution)
# Compute grid dimension
sizex = int(((extent[2] - extent[0]) * KM_PER_DEGREE) / band_resolution_km) * 4
sizey = int(((extent[3] - extent[1]) * KM_PER_DEGREE) / band_resolution_km) * 4

# Mosaicking the available AOI's:
path_mosaic = re.sub(r'part*.*', 'part*.tif', path)
gdal.BuildVRT(dir + date_file + '_mosaic.vrt', sorted(glob.glob(path_mosaic), key=os.path.getmtime))
translate_options = gdal.TranslateOptions(projWin = [extent[0], extent[3], extent[2], extent[1]],  width = sizex, height = sizey)
gdal.Translate(dir + date_file + '_mosaic.tif', dir + date_file +'_mosaic.vrt', options=translate_options)
mosaic = dir + date_file + '_mosaic.tif'

#print(mosaic)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Read the GeoTIFF as array
file = gdal.Open(mosaic)
data = file.GetRasterBand(1).ReadAsArray()
#print("Size:", data.shape)

# Getting the GeoTIFF extent
geoTransform = file.GetGeoTransform()
min_lon = geoTransform[0]
max_lon = min_lon + geoTransform[1] * file.RasterXSize
max_lat = geoTransform[3]
min_lat = max_lat + geoTransform[5] * file.RasterYSize
# The full GeoTIFF extent
extent = [min_lon, min_lat, max_lon, max_lat]
#print("Min Lon:", min_lon, "Min Lat:", min_lat, "Max Lon:", max_lon, "Max Lat:", max_lat)

# The extent I would like to plot
plot_area = extent

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# COLOR SETUP EXAMPLE 1
# Define plot colors [VIIRS | Hourly ABI] 
c_nodata = '#000000' # 14       (No Data)
c_land   = '#c4a272' # 17 | 42  (Land)
c_clouds = '#c8c8c8' # 30 | 98  (Clouds)
c_supra  = '#b400e6' # 56       (Supra Snow/Ice Water)
c_snow   = '#ffffff' # 70       (Snow)
c_ice    = '#00ffff' # 84       (Ice)
c_water  = '#0000ff' # 99 | 126 (Normal Open Water)
#Floodwater          # 100~200 | 140~254
c_floodwater = ["#3dfaab", "#2df863", "#00f700", "#c6f800", "#faf690", "#f7f701", "#f5c400", "#f79029", "#f75e00", "#ff0000"]
cmap_flood = matplotlib.colors.ListedColormap(c_floodwater)

'''

# COLOR SETUP EXAMPLE 2
# Define plot colors [VIIRS | Hourly ABI] 
c_nodata = '#000000' # 14       (No Data)
c_land   = '#282828' # 17 | 43  (Land)
c_clouds = '#383838' # 30 | 99  (Clouds)
c_supra  = '#b400e6' # 56       (Supra Snow/Ice Water)
c_snow   = '#ffffff' # 70       (Snow)
c_ice    = '#00ffff' # 84       (Ice)
c_water  = '#0000ff' # 99 | 126 (Normal Oper Water)
#Floodwater          # 100~200 | 140~254
c_floodwater = ["#3dfaab", "#2df863", "#00f700", "#c6f800", "#faf690", "#f7f701", "#f5c400", "#f79029", "#f75e00", "#ff0000"]
cmap_flood = matplotlib.colors.ListedColormap(c_floodwater)


# COLOR SETUP EXAMPLE 3
# Define plot colors [VIIRS | Hourly ABI] 
c_nodata = '#000000' # 14       (No Data)
c_land   = '#013220' # 17 | 43  (Land)
c_clouds = '#383838' # 30 | 99  (Clouds)
c_supra  = '#b400e6' # 56       (Supra Snow/Ice Water)
c_snow   = '#ffffff' # 70       (Snow)
c_ice    = '#00ffff' # 84       (Ice)
c_water  = '#000033' # 99 | 126 (Normal Oper Water)
#Floodwater          # 100~200 | 140~254
c_floodwater = ["#3dfaab", "#2df863", "#00f700", "#c6f800", "#faf690", "#f7f701", "#f5c400", "#f79029", "#f75e00", "#ff0000"]
cmap_flood = 'Blues'

'''

#print("Plotting the Map Elements...")

# Plot the map elements (land, clouds, snow, ice, etc)
if (prod_name == "GOES-16 ABI Hourly Composite"):
	cmap = matplotlib.colors.ListedColormap([c_nodata, c_land, c_supra, c_snow, c_ice, c_clouds, c_water])
	boundaries = [0, 15, 44, 57, 71, 85, 100, 127]
	# Get only the flood from the full data	
	data_flood = data.astype(np.float64)
	data_flood[data_flood < 140] = np.nan
	data_flood = data_flood - 140
	vmin = 0
	vmax = 114
	thick_interval = 10
else:
	cmap = matplotlib.colors.ListedColormap([c_nodata, c_land, c_clouds, c_supra, c_snow, c_ice, c_water])
	boundaries = [0, 15, 18, 31, 57, 71, 85, 100]
	# Get only the flood from the full data	
	data_flood = data.astype(np.float64)
	data_flood[data_flood < 100] = np.nan
	data_flood = data_flood - 100
	vmin = 0
	vmax = 100
	thick_interval = 10
	
norm = matplotlib.colors.BoundaryNorm(boundaries, cmap.N, clip=True)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Plot configuration
plot_config = {
"resolution": 1, 
"dpi": 150, 
"states_color": 'white', "states_width": data.shape[0] * 0.00036, 
"countries_color": 'white', "countries_width": data.shape[0] * 0.00024,
"continents_color": 'white', "continents_width": data.shape[0] * 0.00050,
"grid_color": 'white', "grid_width": data.shape[0] * 0.00040, "grid_interval": 1.0,
"vmin": vmin, "vmax": vmax, "cmap": cmap,
"title_text": prod_name, "title_size": int(data.shape[1] * 0.005), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[0] - int(data.shape[0] * 0.016), 
"thick_interval": thick_interval, "cbar_labelsize": int(data.shape[0] * 0.005), "cbar_labelpad": -int(data.shape[0] * 0.0),
"file_name_id_1": "FLD",  "file_name_id_2": product 
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
ax.stock_img()
fname = os.path.join(main_dir + '//Maps//', 'land_ocean_ice_8192.jpg')
ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)
#date = datetime(int(year), int(month), int(day), int(hour))
#ax.add_feature(Nightshade(date, alpha=0.7), zorder=2)

# Plot the background
img1 = ax.imshow(data, origin='upper', extent=img_extent, cmap=cmap, norm=norm, zorder=2)

#print("Plotting the Floodwater fraction...")

# Plot the floodwater fraction (%)
img2 = ax.imshow(data_flood, vmin=vmin, vmax=vmax, origin='upper', extent=img_extent, cmap=cmap_flood, zorder=3)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

#print("Plotting other elements...")

# To put colorbar inside picture
axins1 = inset_axes(ax, width="100%", height="1%", loc='lower center', borderpad=0.0)
  
# Add states and provinces
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=4)

# Add countries
#shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
#ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=5)

# Add continents
#shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_coastline.shp').geometries())
#ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=6)
  
# Add coastlines, borders and gridlines
ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=False, zorder=7)

# Remove the outline border
ax.outline_patch.set_visible(False)
  
# Add a title
plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=8)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Add logos / images to the plot
my_logo = plt.imread(main_dir + '//Logos//my_logo.png')
newax = fig.add_axes([0.01, 0.03, 0.10, 0.10], anchor='SW', zorder=12) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
newax.imshow(my_logo)
newax.axis('off')

my_logo = plt.imread(main_dir + '//Logos//noaa_logo.png')
newax = fig.add_axes([0.12, 0.03, 0.08, 0.08], anchor='SW', zorder=12) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
newax.imshow(my_logo)
newax.axis('off')

#my_logo = plt.imread(main_dir + '//Logos//gmu_logo.png')
#newax = fig.add_axes([0.22, 0.03, 0.15, 0.15], anchor='SW', zorder=12) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
#newax.imshow(my_logo)
#newax.axis('off')

# Add a legend to the plot
my_legend = plt.imread(main_dir + '//Legends//FLOOD_legend.png')
newax = fig.add_axes([0.77, 0.77, 0.22, 0.22], anchor='NE', zorder=13) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
newax.imshow(my_legend)
newax.axis('off')
	
# Add a colorbar
ticks = np.arange(plot_config["vmin"], plot_config["vmax"], plot_config["thick_interval"]).tolist()     
ticks = plot_config["thick_interval"] * np.round(np.true_divide(ticks,plot_config["thick_interval"]))
ticks = ticks[1:]
cb = fig.colorbar(img2, cax=axins1, orientation="horizontal", ticks=ticks)
cb.outline.set_visible(False)
cb.ax.tick_params(width = 0)
cb.ax.xaxis.set_tick_params(pad=plot_config["cbar_labelpad"])
cb.ax.xaxis.set_ticks_position('top')
cb.ax.tick_params(axis='x', colors='black', labelsize=plot_config["cbar_labelsize"])

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Create the satellite output directory if it doesn't exist
out_dir = main_dir + '//Output//' + satellite
if not os.path.exists(out_dir):
   os.mkdir(out_dir)

# Create the product output directory if it doesn't exist
out_dir = main_dir + '//Output//' + satellite + '//' + product + '//'
if not os.path.exists(out_dir):
   os.mkdir(out_dir)

# Save the image
fig.savefig(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.png', facecolor='black')#, bbox_inches='tight', pad_inches=0, facecolor='black')

# Update the animation
nfiles = 20
update(satellite, product, nfiles)

# Remove ancillary files
file = None
os.remove(dir + date_file +'_mosaic.vrt')
os.remove(dir + date_file +'_mosaic.tif')

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
