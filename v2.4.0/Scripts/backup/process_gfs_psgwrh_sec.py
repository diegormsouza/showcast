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
# Read the pressure reduced to MSL
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
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the geopotential height at 850 hPa
gh850 = grib.select(name='Geopotential Height', typeOfLevel = 'isobaricInhPa', level = 850)[0]

# Read the data for a specific region
gh850 = gh850.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# To smooth the contours
gh850 = scipy.ndimage.zoom(gh850, 3)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the geopotential height at 1000 hPa
gh1000 = grib.select(name='Geopotential Height', typeOfLevel = 'isobaricInhPa', level = 1000)[0]

# Read the data for a specific region
gh1000 = gh1000.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# To smooth the contours
gh1000 = scipy.ndimage.zoom(gh1000, 3)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Calculate the geopotential difference
ghdif = gh850 - gh1000
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the U component of wind in 935 hPa
ucomp = grib.select(name='U component of wind', typeOfLevel = 'isobaricInhPa', level = 925)[0]

# Read the data for a specific region
ucomp = ucomp.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# To smooth the contours
ucomp = scipy.ndimage.zoom(ucomp, 3)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the V component of wind in 935 hPa
vcomp = grib.select(name='V component of wind', typeOfLevel = 'isobaricInhPa', level = 925)[0]

# Read the data for a specific region
vcomp = vcomp.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# To smooth the contours
vcomp = scipy.ndimage.zoom(vcomp, 3)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the relative humidity in 400 hPa
rh400 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 400)[0]
# Read the data for a specific region
rh400 = rh400.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Read the relative humidity in 450 hPa
rh450 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 450)[0]
# Read the data for a specific region
rh450 = rh450.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Read the relative humidity in 500 hPa
rh500 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 500)[0]
# Read the data for a specific region
rh500 = rh500.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Read the relative humidity in 550 hPa
rh550 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 550)[0]
# Read the data for a specific region
rh550 = rh550.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Read the relative humidity in 600 hPa
rh600 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 600)[0]
# Read the data for a specific region
rh600 = rh600.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Read the relative humidity in 650 hPa
rh650 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 650)[0]
# Read the data for a specific region
rh650 = rh650.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Read the relative humidity in 700 hPa
rh700 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 700)[0]
# Read the data for a specific region
rh700 = rh700.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Read the relative humidity in 750 hPa
rh750 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 750)[0]
# Read the data for a specific region
rh750 = rh750.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Read the relative humidity in 800 hPa
rh800 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 800)[0]
# Read the data for a specific region
rh800 = rh800.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Read the relative humidity in 850 hPa
rh850 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 850)[0]
# Read the data for a specific region
rh850 = rh850.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Read the relative humidity in 900 hPa
rh900 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 900)[0]
# Read the data for a specific region
rh900 = rh900.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Read the relative humidity in 925 hPa
rh925 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 925)[0]
# Read the data for a specific region
rh925 = rh925.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Read the relative humidity in 950 hPa
rh950 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 950)[0]
# Read the data for a specific region
rh950 = rh950.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Read the relative humidity in 975 hPa
rh975 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 975)[0]
# Read the data for a specific region
rh975 = rh975.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Read the relative humidity in 1000 hPa
rh1000 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 1000)[0]
# Read the data for a specific region
rh1000 = rh1000.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Calculate the Mean RH
mrhum = (rh400 + rh450 + rh500 + rh550 + rh600 + rh650 + rh700 + rh750 + rh800 + rh850 + rh900 + rh925 + rh950 + rh975 + rh1000) / 15
# To smooth the contours
mrhum = scipy.ndimage.zoom(mrhum, 3)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Create the color scale 
colors = ["#322800", "#463c00", "#5a4600", "#503c3c", "#505050", "#006400", "#008c00", "#008c8c", "#0064c8"]
cmap = matplotlib.colors.ListedColormap(colors)
cmap.set_over('#0064c8')
cmap.set_under('#322800')

vmin = 30
vmax = 80
thick_interval = 5
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
data_min_rh = 30
data_max_rh = 100
interval_rh = 5
levels_rh = np.arange(data_min_rh,data_max_rh,interval_rh)
 
# Plot the image
img1 = ax.contourf(lons, lats, mrhum, transform=ccrs.PlateCarree(), cmap=cmap, levels=levels_rh, extend='both')
img2 = ax.contour(lons, lats, mrhum, transform=ccrs.PlateCarree(), colors='black', linewidths=0.1, levels=levels_rh)
ax.clabel(img2, inline=1, inline_spacing=0, fontsize=10,fmt = '%1.0f', colors= 'black')

# Plot the image
img3 = ax.barbs(lons[::5,::5], lats[::5,::5], ucomp[::5,::5], vcomp[::5,::5], length = 6.0, sizes = dict(emptybarb=0.0, spacing=0.2, height=0.5), linewidth=0.5, pivot='middle', barbcolor='black', transform=ccrs.PlateCarree())

# Define de contour interval
data_min = 1200
data_max = 1500
interval = 5
levels = np.arange(data_min,data_max,interval)
# Plot the image
img4 = ax.contour(lons, lats, ghdif, transform=ccrs.PlateCarree(), colors='gold', linewidths=1.0, linestyles = 'dashed', levels=levels)
ax.clabel(img4, inline=1, inline_spacing=0, fontsize=10,fmt = '%1.0f', colors= 'gold')

# Define de contour interval
data_min = 990
data_max = 1050
interval = 4
levels = np.arange(data_min,data_max,interval)
# Plot the image
img5 = ax.contour(lons, lats, prmls, transform=ccrs.PlateCarree(), colors='black', linewidths=2.0, levels=levels)
ax.clabel(img5, inline=1, inline_spacing=0, fontsize=10,fmt = '%1.0f', colors= 'black')

# Add states and provinces
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='white',facecolor='none', linewidth=0.25, zorder=2)

# Add countries
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='white',facecolor='none', linewidth=0.50, zorder=3)

# Add continents
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_coastline.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='white',facecolor='none', linewidth=0.75, zorder=4)
  
# Add coastlines, borders and gridlines
gl = ax.gridlines(color='gray', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-180, 180, 5), draw_labels=True, zorder=5)
gl.xlabels_top=False
gl.ylabels_right=False

# Remove the outline border
ax.outline_patch.set_visible(False)
  
# Add a title
plt.title("GFS (0.5°): PSML + Geop. Dif. (1000-850 hPa) + Winds (925 hPa) + Mean RH (1000~400 hPa)", fontweight='bold', fontsize=7, loc='left')
plt.title("Init: " + str(init)[:-6] + "Z | Forecast Hour: [" + str(ftime).zfill(3) + "]" + " | Valid: " + str(valid)[:-6] + "Z ", fontsize=6, loc='right')

# To put colorbar inside picture
axins1 = inset_axes(ax, width="2%", height="100%", loc='right', borderpad=0.0)

# Add a colorbar
ticks = np.arange(data_min_rh, data_max_rh, interval_rh).tolist()     
ticks = interval_rh * np.round(np.true_divide(ticks,interval_rh))
ticks = ticks[1:]
cb = fig.colorbar(img1, label="Mean Relative Humidity (1000 ~ 400 hPa)", cax=axins1, orientation="vertical", ticks=ticks)
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
plt.savefig('GFS' + '_PSGWRH_' + str(init)[:-9].replace('-', '') + str(hour).zfill(2) + 'Z_' + str(ftime).zfill(3) + '.png', bbox_inches='tight', pad_inches=0)

# Show the image
#plt.show()

# Total processing time
print('Total processing time:', round((t.time() - start),2), 'seconds.') 
