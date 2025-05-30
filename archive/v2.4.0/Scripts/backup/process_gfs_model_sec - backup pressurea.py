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
#import matplotlib
#matplotlib.use('Agg')
#--------------------------------
from netCDF4 import Dataset                                  # Read / Write NetCDF4 files
from mpl_toolkits.axes_grid1.inset_locator import inset_axes # Add a child inset axes to this existing axes.
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
from cpt_convert import loadCPT                              # Import the CPT convert function
from matplotlib.colors import LinearSegmentedColormap        # Linear interpolation for color maps
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
from remap import remap                                      # Import the Remap function  
import warnings
import pygrib
warnings.filterwarnings("ignore")
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()  

# SHOWCast directory:
main_dir = dirname(dirname(abspath(__file__)))

# Image path
path = (sys.argv[1])

# Read the GRIB file
grib = pygrib.open(path)

# To print all the variables to a txt file
#f = open("gfs_variables.txt", "w")
#for variables in grib:
#    print(variables, file=f)
#f.close()
    
# Read the model field
grb = grib.select(name='Surface pressure')[0]

print("============================")
print("Type of Level: ", grb.typeOfLevel)
print("Level: ", grb.level)
print("Name: ", grb.name)
print("Unit: ", grb.units)
print("Valid Date: ", grb.validDate)
print("Analysis Date: ", grb.analDate)
print("Forecast Time: ", grb.forecastTime)
print("============================")

# Print the available keys
#print("GRIB Keys :", grb.keys())

##############################
# Read the full dataset values
##############################

'''
data = grb.values
# Read the full lat / lon values
lats,lons = grb.latlons()
'''

##############################
# Read a subset of the dataset
##############################

# Select the desired extent 
# Max. extent for the S.A. sector [-88.0, -60.0, -30.0, 8.00]
extent = [-64.0, -36.0, -40.0, -20.0]

# Read the data for a specific region
data, lats, lons = grb.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

##############################
# Check the data parameters
##############################

# Convert the data to numpy arrays
data = np.array(data)
lats = np.array(lats) 
lons = np.array(lons) - 360 # Converting to -180 ~ 180

print("Data Shape: ", data.shape)
print("Lats Shape: ", lats.shape)
print("Lons Shape: ", lons.shape)
print("============================")
print("Min. Latitude: ", lats.min())
print("Max. Latitude: ", lats.max())
print("Min. Longitude: ", lons.min())
print("Max. Longitude: ", lons.max())
print("============================")

# Data extent
extent = [lons.min(), lats.min(), lons.max(), lats.max()]
print("Extent: ", extent)

'''
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------    
# Plot configuration
plot_config = {
"resolution": 0.5, 
"dpi": 150, 
"states_color": 'white', "states_width": data.shape[0] * 0.00018, 
"countries_color": 'turquoise', "countries_width": data.shape[0] * 0.00012,
"continents_color": 'cyan', "continents_width": data.shape[0] * 0.00025,
"grid_color": 'white', "grid_width": data.shape[0] * 0.00025, "grid_interval": 10.0,
"vmin": vmin, "vmax": vmax, "cmap": cmap,
"title_text": "GOES-" + satellite[1:3] + " Band " + band, "title_size": int(data.shape[1] * 0.005), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[0] - int(data.shape[0] * 0.016), 
"thick_interval": thick_interval, "cbar_labelsize": int(data.shape[0] * 0.005), "cbar_labelpad": -int(data.shape[0] * 0),
"file_name_id_1": satellite,  "file_name_id_2": product 
}
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
'''

# Choose the plot size (width x height, in inches)
fig = plt.figure(figsize=(8, 8))
  
# Define the projection
proj = ccrs.PlateCarree()

# Use the PlateCarree projection in cartopy
ax = plt.axes([0, 0, 1, 1], projection=proj)
ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

# Define the image extent
img_extent = [extent[0], extent[2], extent[1], extent[3]]

# Scale the data if needed
data = data / 100 # Pa to hPa

# Define de contour interval
data_min = 850 #np.min(data) - 1000
data_max = 1050 #np.max(data) + 1000
interval = 10
levels = np.arange(data_min,data_max,interval)
 
# Plot the image
#img = ax.imshow(data, extent=img_extent, origin='lower', cmap='GnBu', zorder=1)
img1 = ax.contourf(lons, lats, data, transform=ccrs.PlateCarree(), cmap='GnBu', levels=levels)
img2 = ax.contour(lons, lats, data, transform=ccrs.PlateCarree(), colors='black', linewidths=0.1, levels=levels)
ax.clabel(img2, inline=0, inline_spacing=0, fontsize=5,fmt = '%1.0f', colors= 'white')

# Add coastlines, borders and gridlines
#ax.coastlines(resolution='10m', color='white', linewidth=0.8, zorder=2)
#ax.add_feature(cartopy.feature.BORDERS, edgecolor='white', linewidth=0.5, zorder=3)
#ax.gridlines(color='white', alpha=0.5, linestyle='--', linewidth=0.5, zorder=4)

# To put colorbar inside picture
#axins1 = inset_axes(ax, width="100%", height="1%", loc='lower center', borderpad=0.0)
  
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
ax.gridlines(color='white', alpha=0.5, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 10), ylocs=np.arange(-180, 180, 10), draw_labels=False, zorder=5)

# Remove the outline border
ax.outline_patch.set_visible(False)
  
# Add a title
#plt.title("GFS 0.5° - " + grb.name + " (" + grb.units + ")", fontweight='bold', fontsize=10, loc='left')
plt.title("GFS 0.5° - " + grb.name + " (hPa)", fontweight='bold', fontsize=10, loc='left')

plt.title(str(grb.analDate) + " UTC", fontsize=10, loc='right')

#plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=6)

# Add a colorbar
plt.colorbar(img1, label=grb.name + " (hPa)", extend='both', orientation='horizontal', pad=0.03, fraction=0.15)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Save the image
plt.savefig('Image_Test.png', bbox_inches='tight', pad_inches=0)

#Show the image
plt.show()

print('Total processing time:', round((t.time() - start),2), 'seconds.') 
