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
import re                                                    # Regular expression operations
import numpy as np                                           # Scientific computing with Python
import os                                                    # Miscellaneous operating system interfaces
from os.path import dirname, abspath                         # Return a normalized absolutized version of the pathname path 
import glob                                                  # Unix style pathname pattern expansion
import matplotlib.colors                                     # Matplotlib colors
import cartopy, cartopy.crs as ccrs                          # Plot maps
import cartopy.io.shapereader as shpreader                   # Import shapefiles
import matplotlib.pyplot as plt                              # Plotting library
import sys                                                   # Import the "system specific parameters and functions" module
import time as t                                             # Time access and conversion
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
from netCDF4 import Dataset                                  # Read / Write NetCDF4 files
from osgeo import gdal, osr, ogr                             # Import GDAL
from shutil import move                                      # High-level file operations
from matplotlib.image import imread                          # Read an image from a file into an array
from cartopy.feature.nightshade import Nightshade            # Draws a polygon where there is no sunlight for the given datetime.
from html_update import update                               # Update the HTML animation 
from mpl_toolkits.axes_grid1.inset_locator import inset_axes # Add a child inset axes to this existing axes.
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
 
def getGeoTransform(extent, nlines, ncols):
    resx = (extent[2] - extent[0]) / ncols
    resy = (extent[3] - extent[1]) / nlines
    return [extent[0], resx, 0, extent[3] , 0, -resy] 
 
###############################################################################
# Reading the Data
###############################################################################
  
# Path to the GOES-R simulated image file
path = sys.argv[1]
 
# Open the file using the NetCDF4 library
nc = Dataset(path)
 
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

satellite = 'MTP'
product = 'SSTSKN'
storage =  product + '_STR' # to store data before mosaicing

# Create the satellite output directory if it doesn't exist
out_dir = main_dir + '//Output//' + satellite
if not os.path.exists(out_dir):
   os.mkdir(out_dir)

# Create the product output directory if it doesn't exist
out_dir = main_dir + '//Output//' + satellite + '//' + storage + '//'
if not os.path.exists(out_dir):
   os.mkdir(out_dir)
        
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
data = nc.variables['sea_surface_temperature'][ : , latli:latui , lonli:lonui ]
# Return a reshaped matrix
data = data.squeeze()
# Flip the y axis
data = np.flipud(data)
# Convert to Celsius
data = data - 273.15
  
# Search for the date in the file name
date = (path[path.find("FIELD-")+6:path.find("Z.nc")])
date_file = date
date_formated = date[0:4] + "-" + date[4:6] + "-" + date[6:8] + " " + date [8:10] + ":" + date [10:12] + " UTC"
 
# Export the result to GeoTIFF ================================================
# Get GDAL driver GeoTiff
driver = gdal.GetDriverByName('GTiff')
# Get dimensions
nlines = data.shape[0]
ncols = data.shape[1]
nbands = len(data.shape)
data_type = gdal.GDT_Float32 # gdal.GDT_Float32
# Create grid
#options = ['COMPRESS=JPEG', 'JPEG_QUALITY=80', 'TILED=YES']
grid = driver.Create('grid', ncols, nlines, 1, data_type)#, options)
# Write data for each bands
grid.GetRasterBand(1).WriteArray(data)
# Lat/Lon WSG84 Spatial Reference System
srs = osr.SpatialReference()
srs.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
# Setup projection and geo-transform
grid.SetProjection(srs.ExportToWkt())
grid.SetGeoTransform(getGeoTransform(extent, nlines, ncols))

driver.CreateCopy(out_dir + satellite + "_" + storage + "_" + date + '.tif', grid, 0)
print('Generated GeoTIFF: ',satellite + "_" + storage + "_" + date + '.tif')

# Close the file
driver = None
grid = None
# Delete the grid
import os
os.remove('grid')
#==============================================================================

date_month = date[0:6] # this option takes lots of disk space! But it is possible
	
# Create the mosaic ===========================================================
gdal.BuildVRT(out_dir + 'MTP_SSTMAC_STR_' + date + '.vrt', sorted(glob.glob(out_dir + satellite + "_" + storage + "_" + date_month +'*.tif'), key=os.path.getmtime), srcNodata = -32768)
gdal.Translate(out_dir + 'MTP_SSTMAC_STR_' + date + '.tif', out_dir + 'MTP_SSTMAC_STR_' + date + '.vrt')
print('Generated GeoTIFF: ', 'MTP_SSTMAC_STR_' + date + '.tif')
os.remove(out_dir + 'MTP_SSTMAC_STR_' + date + '.vrt')
# Export the result to GeoTIFF ================================================

# Read the mosaic
mosaic = gdal.Open(out_dir + 'MTP_SSTMAC_STR_' + date + '.tif')
file_band = mosaic.GetRasterBand(1)
data = file_band.ReadAsArray()
data[data == min(data[0])] = np.nan

# Colormap 
cmap = 'jet'
vmin = -5.0
vmax = 35.0
thick_interval = 1
prod_title = 'Global Sea Surface Temperature (0.05°)'
product = 'SSTMAC'

# Plot configuration
plot_config = {
"resolution": resolution, 
"dpi": 150, 
"states_color": 'white', "states_width": sizey * 0.00006, 
"countries_color": 'gold', "countries_width": sizey * 0.00012,
"continents_color": 'gold', "continents_width": sizey * 0.00025,
"grid_color": 'white', "grid_width": sizey * 0.00025, "grid_interval": 10.0,
"vmin": vmin, "vmax": vmax, "cmap": cmap,
"title_text": "METOP " + prod_title + " ", "title_size": int(sizex * 0.0025), "title_x_offset": int(sizex * 0.01), "title_y_offset": sizey - int(sizey * 0.016),
"thick_interval": thick_interval, "cbar_labelsize": int(sizey * 0.005), "cbar_labelpad": -int(sizey * 0.0),
"file_name_id_1": "MTP",  "file_name_id_2": product + "_SEC"
}

# Choose the plot size (width x height, in inches)
fig = plt.figure(figsize=(sizex/float(plot_config["dpi"]), sizey/float(plot_config["dpi"])), dpi=plot_config["dpi"])
# Define the projection
proj = ccrs.PlateCarree()
# Use the PlateCarree projection in cartopy
ax = plt.axes([0, 0, 1, 1], projection=proj)
img_extent = [extent[0], extent[2], extent[1], extent[3]]
# Add a background image
#ax.stock_img()
fname = os.path.join(main_dir + '//Maps//', 'land_ocean_ice_8192.jpg')
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