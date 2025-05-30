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
gh500 = grib.select(name='Geopotential Height', typeOfLevel = 'isobaricInhPa', level = 500)[0]

# For later use
init  = gh500.analDate     # Analysis date / time
hour  = gh500.hour         # Run
ftime = gh500.forecastTime # Forecast hour
valid = gh500.validDate    # Valid date / time 

#print("GRIB Keys :", sfcps.keys())

print(str(gh500.hour).zfill(2))

# Read the data for a specific region
gh500, lats, lons = gh500.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# Converting the longitudes to -180 ~ 180
lats = np.array(lats) 
lons = np.array(lons) - 360 # Converting to -180 ~ 180
#lons = lons - 360 
#print(2mtmp.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the temperature in 950 hPa
vcomp = grib.select(name='V component of wind', typeOfLevel = 'isobaricInhPa', level = 500)[0]

# Read the data for a specific region
vcomp = vcomp.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the temperature in 950 hPa
ucomp = grib.select(name='U component of wind', typeOfLevel = 'isobaricInhPa', level = 500)[0]

# Read the data for a specific region
ucomp = ucomp.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Calculate dx and dy for calculations
# Ref: https://unidata.github.io/python-training/workshop/MetPy_Case_Study/metpy-case-study/

dx, dy = mpcalc.lat_lon_grid_deltas(lons, lats)

from metpy.units import units
from xarray import DataArray
u = units('m/s') * DataArray(ucomp)
v = units('m/s') * DataArray(vcomp)

# Relative Vorticity
#rv500 = mpcalc.vorticity(ucomp, vcomp, dx, dy, dim_order='yx')

rv500 = mpcalc.vorticity(u, v, dx, dy)#, dim_order='yx')

# Another option:
# ref: https://github.com/keltonhalbert/wrftools/blob/master/wrftools/variables/winds.py

#dx_r = dx.reshape(ucomp.shape[0], ucomp.shape[1])
#dy_r = dy.reshape(ucomp.shape[0], ucomp.shape[1])
#a = np.ones((lons.shape[0],1))
#dx_r = np.hstack((dx,a))
#b = np.ones((1, lons.shape[1]))
#dy_r = np.hstack((dy,b))

#print(ucomp.shape)
#print(vcomp.shape)
#print(dx.shape)
#print(dy.shape)
#print(dx_r.shape)
#print(dy_r.shape)

#dy = dx
#du = np.gradient(ucomp)
#dv = np.gradient(vcomp)
#rv500 = dv[-1]/dx - du[-2]/dy

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Create the color scale 
#colors = ["#e7f2f4", "#ceeaee", "#b6e2e8", "#abdcff", "#a4d685", "#9cd04e", "#abcf2a", "#c9d21b", "#e8d50c", "#ffd100", "#ffba00", "#ffa200"]
#cmap = matplotlib.colors.ListedColormap(colors)
#cmap.set_over('#ff8c00')
#cmap.set_under('#fffafa')

cmap = 'bwr'
vmin = -12.0
vmax = 12.0
thick_interval = 1

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
data_min = -12.0
data_max = 12.0
interval = 1
levels = np.arange(data_min,data_max,interval)
 
# Plot the image
img1 = ax.contourf(lons, lats, rv500, transform=ccrs.PlateCarree(), cmap=cmap, levels=levels, extend='both')
img2 = ax.contour(lons, lats, rv500, transform=ccrs.PlateCarree(), colors='black', linewidths=0.1, levels=levels)
ax.clabel(img2, inline=1, inline_spacing=0, fontsize=10,fmt = '%1.0f', colors= 'black')

# Plot the streamlines
#qv = plt.quiver(lons, lats, ucomp, vcomp, scale=1300, color='gray', alpha=1.0)
#img3 = ax.streamplot(lons, lats, ucomp, vcomp, density=[1.5, 1.5], linewidth=1, color='gray')

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
plt.title("GFS (0.5°): Relative Vorticity (1 e-5 / s)", fontweight='bold', fontsize=10, loc='left')
plt.title("Init: " + str(init)[:-6] + "Z | Forecast Hour: [" + str(ftime).zfill(3) + "]" + " | Valid: " + str(valid)[:-6] + "Z ", fontsize=10, loc='right')

# To put colorbar inside picture
axins1 = inset_axes(ax, width="2%", height="100%", loc='right', borderpad=0.0)

# Add a colorbar
ticks = np.arange(data_min, data_max, interval).tolist()     
ticks = interval * np.round(np.true_divide(ticks,interval))
ticks = ticks[1:]
cb = fig.colorbar(img1, label="Relative Vorticity (1 e-5 / s)", cax=axins1, orientation="vertical", ticks=ticks)
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
plt.savefig('GFS' + '_GHV500_' + str(init)[:-9].replace('-', '') + str(hour).zfill(2) + 'Z_' + str(ftime).zfill(3) + '.png', bbox_inches='tight', pad_inches=0)

# Show the image
plt.show()

# Total processing time
print('Total processing time:', round((t.time() - start),2), 'seconds.') 
