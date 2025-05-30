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
pwatr = grib.select(name='Precipitable water')[0]

# For later use
init  = pwatr.analDate     # Analysis date / time
hour  = pwatr.hour         # Run
ftime = pwatr.forecastTime # Forecast hour
valid = pwatr.validDate    # Valid date / time 

#print("GRIB Keys :", sfcps.keys())

print(str(pwatr.hour).zfill(2))

# Read the data for a specific region
pwatr, lats, lons = pwatr.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# To smooth the contours
import scipy.ndimage
pwatr = scipy.ndimage.zoom(pwatr, 3)
lats = scipy.ndimage.zoom(lats, 3)
lons = scipy.ndimage.zoom(lons, 3)

# Converting the longitudes to -180 ~ 180
lons = lons - 360 
#print(pwatr.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the CAPE
cape0 = grib.select(name='Convective available potential energy')[2]

# Read the data for a specific region
cape0 = cape0.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# To smooth the contours
cape0 = scipy.ndimage.zoom(cape0, 3)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

colors = ["#6b6763", "#7e7972", "#989083", "#b2a592", "#cab9a0", "#aebce3", "#9eabd6", "#9292ef", "#7777cd", "#6666b5", "#505096", "#146f5a", "#287a4f", "#3b8645", "#5b9834", "#73a528", "#a4c932", "#bbd725", "#d5e617", "#ecf40a", "#ffff00"]
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
cmap.set_over('#ffff00')
cmap.set_under('#6b6763')
vmin = 0
vmax = 80
thick_interval = 5

#colors = ["#bc8462", "#ae656f", "#a44a79", "#962e97", "#6158c5", "#2b8ffb", "#5fcdff", "#94fff0", "#a5ff94", "#fff88c", "#ffbf52", "#ec7b27", "#b84827", "#a1333d", "#bd5478", "#cc6a99", "#d982b8"]
#cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
#cmap.set_over('#d982b8')
#cmap.set_under('#bc8462')
#vmin = 0
#vmax = 80
#thick_interval = 5

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

#import cartopy.feature as cfeature
#land = ax.add_feature(cfeature.LAND, facecolor='whitesmoke', zorder=1)
#ocean = ax.add_feature(cfeature.OCEAN, facecolor='lightcyan', zorder=1)

# Define de contour interval
data_min = 0
data_max = 80
interval = 5
levels = np.arange(data_min,data_max,interval)
 
# Plot the image
img1 = ax.contourf(lons, lats, pwatr, transform=ccrs.PlateCarree(), cmap=cmap, levels=levels, extend='both', alpha = 0.8, zorder=2)
#img2 = ax.contour(lons, lats, pwatr, transform=ccrs.PlateCarree(), colors='black', linewidths=0.1, levels=levels, zorder=3)
#ax.clabel(img2, inline=1, inline_spacing=0, fontsize=10,fmt = '%1.0f', colors= 'black')

# This is the fix for the lines between contour levels
#for c in img1.collections:
#    c.set_edgecolor('none')
#    c.set_linewidths(0.000000000001)

# Define de contour interval
data_min = 100
data_max = 3000
interval = 100
levels = np.arange(data_min,data_max,interval)
levels = [200, 500, 1000, 1500, 3000]

# Plot the image
#img3 = ax.contour(lons, lats, cape0, transform=ccrs.PlateCarree(), colors='black', linewidths=2.0, levels=levels, zorder=4)
img3 = ax.contour(lons, lats, cape0, transform=ccrs.PlateCarree(), cmap='OrRd', linewidths=2.0, levels=levels, zorder=4)
ax.clabel(img3, inline=1, inline_spacing=0, fontsize=10, fmt = '%1.0f')

# Add states and provinces
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='gray',facecolor='none', linewidth=0.25, zorder=6)

# Add countries
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black',facecolor='none', linewidth=0.50, zorder=7)

# Add continents
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_coastline.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black',facecolor='none', linewidth=0.75, zorder=8)
  
# Add coastlines, borders and gridlines
gl = ax.gridlines(color='white', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-180, 180, 5), draw_labels=True, zorder=9)
gl.xlabels_top=False
gl.ylabels_right=False

# Remove the outline border
ax.outline_patch.set_visible(False)
  
# Add a title
plt.title("GFS (0.5°): Prec. Water (mm) + CAPE", fontweight='bold', fontsize=10, loc='left')
plt.title("Init: " + str(init)[:-6] + "Z | Forecast Hour: [" + str(ftime).zfill(3) + "]" + " | Valid: " + str(valid)[:-6] + "Z ", fontsize=10, loc='right')

# To put colorbar inside picture
axins1 = inset_axes(ax, width="2%", height="100%", loc='right', borderpad=0.0)

# Add a colorbar
ticks = np.arange(vmin, vmax, thick_interval).tolist()     
ticks = thick_interval * np.round(np.true_divide(ticks,thick_interval))
ticks = ticks[1:]
cb = fig.colorbar(img1, label="Precipitable Water (mm)", cax=axins1, orientation="vertical", ticks=ticks)
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
plt.savefig('GFS' + '_PWCAPE_' + str(init)[:-9].replace('-', '') + str(hour).zfill(2) + 'Z_' + str(ftime).zfill(3) + '.png', bbox_inches='tight', pad_inches=0)

# Show the image
plt.show()

# Total processing time
print('Total processing time:', round((t.time() - start),2), 'seconds.') 
