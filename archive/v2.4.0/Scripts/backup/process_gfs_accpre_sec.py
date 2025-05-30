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

# Desired extent 
extent = [-64.0, -36.0, -40.0, -15.0] # [min_lon, min_lat, max_lon, max_lat]

# Image path
path = (sys.argv[1])

# Open the GRIB file
grib = pygrib.open(path)

# To print all the variables to a txt file
#f = open("gfs_variables_024.txt", "w")
#for variables in grib:
#    print(variables, file=f)
#f.close()

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------   
# Read the surface pressure
tmtmp = grib.select(name='Total Precipitation', typeOfLevel = 'surface')[1]

#################################################################################
# For some reason the "Total Precipitation" variable doesnt' have the right keys!
title = grib.select(name='2 metre temperature')[0] 

# For later use
init  = title.analDate     # Analysis date / time
hour  = title.hour         # Run
ftime = title.forecastTime # Forecast hour
valid = title.validDate    # Valid date / time 

#print("============================")
#print("Type of Level: ", title.typeOfLevel)
#print("Level: ", title.level)
#print("Name: ", title.name)
#print("Unit: ", title.units)
#print("Analysis Date: ", title.analDate)
#print("Forecast Hour: ", title.forecastTime)
#print("Valid Date: ", title.validDate)
#print("============================")

#print(str(title.hour).zfill(2))
#################################################################################

# Read the data for a specific region
tmtmp, lats, lons = tmtmp.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# Converting the longitudes to -180 ~ 180
lons = lons - 360 

#import scipy.ndimage
# Resample your data grid by a factor of 3 using cubic spline interpolation.
#tmtmp = scipy.ndimage.gaussian_filter(tmtmp, sigma=0.5, order=0)
#lats = scipy.ndimage.gaussian_filter(lats, sigma=0.5, order=0)
#lons = scipy.ndimage.gaussian_filter(lons, sigma=0.5, order=0)


#import scipy.ndimage
#tmtmp = scipy.ndimage.zoom(tmtmp, 3)
#lats = scipy.ndimage.zoom(lats, 3)
#lons = scipy.ndimage.zoom(lons, 3)

tmtmp[tmtmp == 0] = np.nan

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Create the color scale 
colors = ["#b4f0f0", "#96d2fa", "#78b9fa", "#3c95f5", "#1e6deb", "#1463d2", "#0fa00f", "#28be28", "#50f050", "#72f06e", "#b3faaa", "#fff9aa", "#ffe978", "#ffc13c", "#ffa200", "#ff6200", "#ff3300", "#ff1500", "#c00100", "#a50200", "#870000", "#653b32"]
cmap = matplotlib.colors.ListedColormap(colors)
cmap.set_over('#000000')
cmap.set_under('#828282')
vmin = 1
vmax = 90
thick_interval = 5

# Create the color scale for low values
colors2 = ["#bebebe", "#a5a5a5", "#969696", "#828282"]
cmap2 = matplotlib.colors.ListedColormap(colors2)
cmap2.set_over('#828282')
cmap2.set_under('#000000')
vmin2 = 0.0
vmax2 = 1.0
thick_interval = 0.1

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
#fname = os.path.join(main_dir + '//Maps//', 'natural-earth-1_large2048px.jpg')
#ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)
import cartopy.feature as cfeature
land = ax.add_feature(cfeature.LAND, facecolor='whitesmoke', zorder=1)
ocean = ax.add_feature(cfeature.OCEAN, facecolor='white', zorder=1)

# Plot the image (high values)
# Define de contour interval
data_min = 1
data_max = 90 
interval = 5
levels = np.arange(data_min,data_max,interval)
img1 = ax.contourf(lons, lats, tmtmp, transform=ccrs.PlateCarree(), cmap=cmap, levels=levels, extend='both', zorder=2)
img2 = ax.contour(lons, lats, tmtmp, transform=ccrs.PlateCarree(), colors='black', linewidths=0.1, levels=levels, zorder=3)
ax.clabel(img2, inline=1, inline_spacing=0, fontsize=10,fmt = '%1.0f', colors= 'black')

# Plot the image (low values)
data_min2 = 0.0
data_max2 = 1.0
interval2 = 0.2
levels2 = np.arange(data_min2,data_max2,interval2)
tmtmp[tmtmp > 1] = np.nan
img3 = ax.contourf(lons, lats, tmtmp, transform=ccrs.PlateCarree(), cmap=cmap2, levels=levels2, zorder=4)

# Add states and provinces
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black',facecolor='none', linewidth=0.25, zorder=5)

# Add countries
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black',facecolor='none', linewidth=0.50, zorder=6)

# Add continents
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_coastline.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black',facecolor='none', linewidth=0.75, zorder=7)
  
# Add coastlines, borders and gridlines
gl = ax.gridlines(color='gray', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-180, 180, 5), draw_labels=  True, zorder=8)
gl.xlabels_top=False
gl.ylabels_right=False

# Remove the outline border
ax.outline_patch.set_visible(False)
  
# Add a title
plt.title("GFS (0.5°): Accum. Precip. (mm) - 24 h", fontweight='bold', fontsize=10, loc='left')
plt.title("Init: " + str(init)[:-6] + "Z | Forecast Hour: [" + str(ftime).zfill(3) + "]" + " | Valid: " + str(valid)[:-6] + "Z ", fontsize=10, loc='right')

# To put colorbar inside picture
axins1 = inset_axes(ax, width="2%", height="100%", loc='right', borderpad=0.0)

# Add a colorbar
ticks = np.arange(data_min, data_max, interval).tolist()     
ticks = interval * np.round(np.true_divide(ticks,interval))
ticks = ticks[1:]
cb = fig.colorbar(img1, label="24 h Accum. Precip. (mm) - 24 h", cax=axins1, orientation="vertical", ticks=ticks)
cb.outline.set_visible(False)
cb.ax.tick_params(width = 0)
cb.ax.xaxis.set_tick_params(pad=0.00)
cb.ax.xaxis.set_ticks_position('top')
cb.ax.tick_params(axis='x', colors='black', labelsize=10)

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
plt.savefig('GFS' + '_PRE24H_' + str(init)[:-9].replace('-', '') + str(hour).zfill(2) + 'Z_' + str(ftime).zfill(3) + '.png', bbox_inches='tight', pad_inches=0)

# Show the image
#plt.show()

# Total processing time
print('Total processing time:', round((t.time() - start),2), 'seconds.') 
