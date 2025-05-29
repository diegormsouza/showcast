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
# Read the surface pressure
prmls = grib.select(name='Pressure reduced to MSL')[0]

# For later use
init  = prmls.analDate     # Analysis date / time
hour  = prmls.hour         # Run
ftime = prmls.forecastTime # Forecast hour
valid = prmls.validDate    # Valid date / time 

#print("GRIB Keys :", sfcps.keys())

print(str(prmls.hour).zfill(2))

# Read the data for a specific region
prmls, lats, lons = prmls.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# Converting the longitudes to -180 ~ 180
lons = lons - 360 

# Convert to hPa
prmls = prmls / 100

# To smooth the contours
import scipy.ndimage
prmls = scipy.ndimage.zoom(prmls, 3)
lats = scipy.ndimage.zoom(lats, 3)
lons = scipy.ndimage.zoom(lons, 3)
#print(prmls.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Read the temperature in 850 hPa
ucomp = grib.select(name='U component of wind', typeOfLevel = 'isobaricInhPa', level = 850)[0]

# Read the data for a specific region
ucomp = ucomp.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# To smooth the contours
ucomp = scipy.ndimage.zoom(ucomp, 3)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Read the temperature in 850 hPa
vcomp = grib.select(name='V component of wind', typeOfLevel = 'isobaricInhPa', level = 850)[0]

# Read the data for a specific region
vcomp = vcomp.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# To smooth the contours
vcomp = scipy.ndimage.zoom(vcomp, 3)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Create the color scale 
colors = ["#310d00", "#631b00", "#942800", "#c53500", "#fd6123", "#fb824e", "#faa679", "#f8c8a3", "#f6f6e1", "#f8f8e7", "#fafaee", "#fcfcf5", "#fefefc", "#e8eef5", "#d9e2ef", "#c9d7e9", "#bacce2", "#a9bbd9", "#95a1c9", "#8187b9", "#6d6da8", "#595398", "#463b87", "#382f6c", "#2a2351", "#1c1836", "#0e161b"]
cmap = matplotlib.colors.ListedColormap(colors)
cmap.set_over('#000000')
cmap.set_under('#000000')

#colors = ["#7dc3e3", "#a09fbf", "#dab8d9", "#e1e2f6", "#728292", "#97a9bf", "#e8ebf0", "#eeffff", "#f8fff7", "#f6faf9", "#d7d8da", "#a4eceb", "#57ebd0", "#8af4aa", "#d7fdf2", "#01e882", "#3db23f", "#dce5ae", "#e0bc8c", "#d4a01d", "#ad701a", "#e2190b", "#850000", "#834e26", "#b236b2", "#aa00aa"]
#cmap = matplotlib.colors.ListedColormap(colors)
#cmap.set_over('#9400d4')
#cmap.set_under('#6395ec')
vmin = 990
vmax = 1050
thick_interval = 6

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

# Define de contour interval
data_min = 990
data_max = 1050
interval = 2
levels = np.arange(data_min,data_max,interval)
 
# Plot the image
img1 = ax.contourf(lons, lats, prmls, transform=ccrs.PlateCarree(), cmap=cmap, levels=levels, extend='both')
img2 = ax.contour(lons, lats, prmls, transform=ccrs.PlateCarree(), colors='black', linewidths=0.1, levels=levels)
ax.clabel(img2, inline=1, inline_spacing=0, fontsize=10,fmt = '%1.0f', colors= 'black')
#img3 = ax.barbs(lons, lats, ucomp, vcomp, length = 1.0, sizes = dict(emptybarb=0.25, spacing=0.2, height=0.5), linewidth=0.8, pivot='middle', barbcolor='black', transform=ccrs.PlateCarree())
img3 = ax.barbs(lons[::9,::9], lats[::9,::9], ucomp[::9,::9], vcomp[::9,::9], length = 6.0, sizes = dict(emptybarb=0.25, spacing=0.2, height=0.5), linewidth=0.8, pivot='middle', barbcolor='gray', transform=ccrs.PlateCarree())

# Add states and provinces
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black',facecolor='none', linewidth=0.25, zorder=2)

# Add countries
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black',facecolor='none', linewidth=0.50, zorder=3)

# Add continents
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_coastline.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black',facecolor='none', linewidth=0.75, zorder=4)
  
# Add coastlines, borders and gridlines
gl = ax.gridlines(color='white', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-180, 180, 5), draw_labels=True, zorder=5)
gl.xlabels_top=False
gl.ylabels_right=False

# Remove the outline border
ax.outline_patch.set_visible(False)
  
# Add a title
plt.title("GFS (0.5°): PMSL + Winds (850 hPa)", fontweight='bold', fontsize=10, loc='left')
plt.title("Init: " + str(init)[:-6] + "Z | Forecast Hour: [" + str(ftime).zfill(3) + "]" + " | Valid: " + str(valid)[:-6] + "Z ", fontsize=10, loc='right')

# To put colorbar inside picture
axins1 = inset_axes(ax, width="2%", height="100%", loc='right', borderpad=0.0)

# Add a colorbar
ticks = np.arange(data_min, data_max, interval).tolist()     
ticks = interval * np.round(np.true_divide(ticks,interval))
ticks = ticks[1:]
cb = fig.colorbar(img1, label="PMSL (hPa)", cax=axins1, orientation="vertical", ticks=ticks)
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
plt.savefig('GFS' + '_PRTMSL_' + str(init)[:-9].replace('-', '') + str(hour).zfill(2) + 'Z_' + str(ftime).zfill(3) + '.png', bbox_inches='tight', pad_inches=0)

# Show the image
plt.show()

# Total processing time
print('Total processing time:', round((t.time() - start),2), 'seconds.') 
