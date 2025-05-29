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
#matplotlib.use('Agg')
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
import os                                                    # Miscellaneous operating system interfaces
from matplotlib.image import imread                          # Read an image from a file into an array
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

# Desired extent 
extent = [-64.0, -36.0, -40.0, -15.0] # [min_lon, min_lat, max_lon, max_lat]

# Image path
path = (sys.argv[1])

# Open the GRIB file
grib = pygrib.open(path)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------   
# Read the relative humidity in 300 hPa
sh300 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 300)[0]

# For later use
init  = sh300.analDate     # Analysis date / time
hour  = sh300.hour         # Run
ftime = sh300.forecastTime # Forecast hour
valid = sh300.validDate    # Valid date / time 

#print("GRIB Keys :", sfcps.keys())

print(str(sh300.hour).zfill(2))

# Read the data for a specific region
sh300, lats, lons = sh300.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# To smooth the contours
import scipy.ndimage
sh300 = scipy.ndimage.zoom(sh300, 3)
lats = scipy.ndimage.zoom(lats, 3)
lons = scipy.ndimage.zoom(lons, 3)

# Removing the values < 70%
sh300[sh300 < 70] = np.nan

# Converting the longitudes to -180 ~ 180
lons = lons - 360 
#print(sh300.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the relative humidity in 500 hPa
sh500 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 500)[0]

# Read the data for a specific region
sh500 = sh500.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# To smooth the contours
sh500 = scipy.ndimage.zoom(sh500, 3)

# Removing the values < 70%
sh500[sh500 < 70] = np.nan

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the relative humidity in 500 hPa
sh800 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 800)[0]

# Read the data for a specific region
sh800 = sh800.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# To smooth the contours
sh800 = scipy.ndimage.zoom(sh800, 3)

# Removing the values < 70%
sh800[sh800 < 70] = np.nan

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the precipitation rate
preci = grib.select(name='Precipitation rate')[0]

# Read the data for a specific region
preci = preci.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# To smooth the contours
preci = scipy.ndimage.zoom(preci, 3)

# Removing the values < 70%
preci[preci < 0] = np.nan

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
'''
# Create the color scale 
colors = ["#acefb2", "#f6bcbb", "#f3c4c4", "#f6cfd0", "#fde8e7"]
cmap = matplotlib.colors.ListedColormap(colors)
cmap.set_over('#fde8e7')
cmap.set_under('#f6b5b5')

# Create the color scale 
colors = ["#f6b5b5", "#bbf2c1", "#cbf5cd", "#d0f6cf", "#e6fbe6"]
cmap2 = matplotlib.colors.ListedColormap(colors)
cmap2.set_over('#e6fbe6')
cmap2.set_under('#f6b5b5')

# Create the color scale 
colors = ["#b2b8f6", "#bfbef8", "#cbcaf3", "#d2d2f8", "#e7e8fc"]
cmap3 = matplotlib.colors.ListedColormap(colors)
cmap3.set_over('#e7e8fc')
cmap3.set_under('#b2b8f6')
'''

cmap = 'gray'
cmap2 = 'gray'
cmap3 = 'gray'

vmin = 70.0
vmax = 100.0
thick_interval = 5.0

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Choose the plot size (width x height, in inches)
fig = plt.figure(figsize=(8, 8))
  
# Define the projection
proj = ccrs.PlateCarree()

# Use the PlateCarree projection in cartopy
ax = plt.axes([0, 0, 1, 1], projection=proj)
ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

# Define the image extent
img_extent = [extent[0], extent[2], extent[1], extent[3]]

# Add a background image
#ax.stock_img()
fname = os.path.join(main_dir + '//Maps//', 'land_ocean_ice_8192.jpg')
ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)

import cartopy.feature as cfeature
'''
land = ax.add_feature(cfeature.LAND, facecolor='whitesmoke', zorder=1)
ocean = ax.add_feature(cfeature.OCEAN, facecolor='lightcyan', zorder=1)
'''
'''
land = ax.add_feature(cfeature.LAND, facecolor='black', zorder=1)
ocean = ax.add_feature(cfeature.OCEAN, facecolor='black', zorder=1)
'''

# Define de contour interval
data_min = 70.0
data_max = 100.0
interval = 1.0
levels = np.arange(data_min,data_max,interval)
 
# Plot the image
img1 = ax.contourf(lons, lats, sh800, transform=ccrs.PlateCarree(), cmap=cmap3, levels=levels, extend='both', alpha = 0.5, zorder=2)
#img2 = ax.contour(lons, lats, sh300, transform=ccrs.PlateCarree(), colors='black', linewidths=0.1, levels=levels, zorder=3)
#ax.clabel(img2, inline=1, inline_spacing=0, fontsize=10,fmt = '%1.0f', colors= 'black')
img3 = ax.contourf(lons, lats, sh500, transform=ccrs.PlateCarree(), cmap=cmap2, levels=levels, extend='both', alpha = 0.8, zorder=4)
#img4 = ax.contour(lons, lats, sh500, transform=ccrs.PlateCarree(), colors='black', linewidths=0.1, levels=levels, zorder=5)
img5 = ax.contourf(lons, lats, sh300, transform=ccrs.PlateCarree(), cmap=cmap, levels=levels, extend='both', alpha = 1.0, zorder=5)


# Create the color scale 
colors = ["#b4f0f0", "#96d2fa", "#78b9fa", "#3c95f5", "#1e6deb", "#1463d2", "#0fa00f", "#28be28", "#50f050", "#72f06e", "#b3faaa", "#fff9aa", "#ffe978", "#ffc13c", "#ffa200", "#ff6200", "#ff3300", "#ff1500", "#c00100", "#a50200", "#870000", "#653b32"]
cmap4 = matplotlib.colors.ListedColormap(colors)
cmap4.set_over('#000000')
cmap4.set_under('#828282')

data_min = 1
data_max = 90 
interval = 5
levels = np.arange(data_min,data_max,interval)
img6 = ax.contourf(lons, lats, preci, transform=ccrs.PlateCarree(), cmap=cmap4, levels=levels, extend='both', zorder=6)
img7 = ax.contour(lons, lats, preci, transform=ccrs.PlateCarree(), colors='black', linewidths=0.1, levels=levels, zorder=7)
ax.clabel(img7, inline=1, inline_spacing=0, fontsize=10,fmt = '%1.0f', colors= 'black')


# This is the fix for the white lines between contour levels
for c in img1.collections:
    c.set_edgecolor("face")
for c in img3.collections:
    c.set_edgecolor("face")
for c in img5.collections:
    c.set_edgecolor("face")
 
# Add states and provinces
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='white',facecolor='none', linewidth=0.25, zorder=8)

# Add countries
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='white',facecolor='none', linewidth=0.50, zorder=9)

# Add continents
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_coastline.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='white',facecolor='none', linewidth=0.75, zorder=10)
  
# Add coastlines, borders and gridlines
gl = ax.gridlines(color='white', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-180, 180, 5), draw_labels=True, zorder=11)
gl.xlabels_top=False
gl.ylabels_right=False

# Remove the outline border
ax.outline_patch.set_visible(False)
  
# Add a title
plt.title("GFS (0.5°): Low, Middle, & High Clouds", fontweight='bold', fontsize=10, loc='left')
plt.title("Init: " + str(init)[:-6] + "Z | Forecast Hour: [" + str(ftime).zfill(3) + "]" + " | Valid: " + str(valid)[:-6] + "Z ", fontsize=10, loc='right')

# To put colorbar inside picture
#axins1 = inset_axes(ax, width="2%", height="100%", loc='right', borderpad=0.0)

# Add a colorbar
#ticks = np.arange(data_min, data_max, interval).tolist()     
#ticks = interval * np.round(np.true_divide(ticks,interval))
#ticks = ticks[1:]
#cb = fig.colorbar(img1, label="Low, Middle, & High Clouds", cax=axins1, orientation="vertical", ticks=ticks)
#cb.outline.set_visible(False)
#cb.ax.tick_params(width = 0)
#cb.ax.xaxis.set_tick_params(pad=0.00)
#cb.ax.xaxis.set_ticks_position('top')
#cb.ax.tick_params(axis='x', colors='black', labelsize=10)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Add logos / images to the plot
my_logo = plt.imread(main_dir + '//Logos//my_logo.png')
newax = fig.add_axes([0.01, 0.08, 0.10, 0.10], anchor='SW', zorder=12) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
newax.imshow(my_logo)
newax.axis('off')

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Save the image
plt.savefig('GFS' + '_SPHCLD_' + str(init)[:-9].replace('-', '') + str(hour).zfill(2) + 'Z_' + str(ftime).zfill(3) + '.png', bbox_inches='tight', pad_inches=0)

# Show the image
plt.show()

# Total processing time
print('Total processing time:', round((t.time() - start),2), 'seconds.') 
