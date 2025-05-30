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
sfcps = grib.select(name='Surface pressure')[0]

# For later use
init  = sfcps.analDate     # Analysis date / time
hour  = sfcps.hour         # Run
ftime = sfcps.forecastTime # Forecast hour
valid = sfcps.validDate    # Valid date / time 

#print("GRIB Keys :", sfcps.keys())
print(str(sfcps.hour).zfill(2))

# Read the data for a specific region
sfcps, lats, lons = sfcps.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# Converting the longitudes to -180 ~ 180
lons = lons - 360 

# Convert the surface pressure to hectopascal
sfcps = sfcps / 100
#print(sfcps.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the temperature in 950 hPa
temp950 = grib.select(name='Temperature', typeOfLevel = 'isobaricInhPa', level = 950)[0]

# Read the data for a specific region
temp950 = temp950.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Calculate the theta
T950 = ((temp950)*(pow((1000/950),(2/7))))
#print(T950.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the specific humidity in 950 hPa
spfh950 = grib.select(name='Specific humidity', typeOfLevel = 'isobaricInhPa', level = 950)[0]

# Read the data for a specific region
R950 = spfh950.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]
#print(R950.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the temperature in 850 hPa
temp850 = grib.select(name='Temperature', typeOfLevel = 'isobaricInhPa', level = 850)[0]

# Read the data for a specific region
temp850 = temp850.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Calculate the theta
T850 = ((temp850)*(pow((1000/850),(2/7))))
#print(T850.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the specific humidity in 850 hPa
spfh850 = grib.select(name='Specific humidity', typeOfLevel = 'isobaricInhPa', level = 850)[0]

# Read the data for a specific region
R850 = spfh850.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]
#print(R850.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the temperature in 700 hPa
temp700 = grib.select(name='Temperature', typeOfLevel = 'isobaricInhPa', level = 700)[0]

# Read the data for a specific region
temp700 = temp700.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Calculate the theta
T700 = ((temp700)*(pow((1000/700),(2/7))))
#print(T700.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the specific humidity in 700 hPa
spfh700 = grib.select(name='Specific humidity', typeOfLevel = 'isobaricInhPa', level = 700)[0]

# Read the data for a specific region
R700 = spfh700.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]
#print(R700.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the temperature in 500 hPa
temp500 = grib.select(name='Temperature', typeOfLevel = 'isobaricInhPa', level = 500)[0]

# Read the data for a specific region
temp500 = temp500.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

# Calculate the theta
T500 = ((temp500)*(pow((1000/500),(2/7))))
#print(T500.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the specific humidity in 500 hPa
spfh500 = grib.select(name='Specific humidity', typeOfLevel = 'isobaricInhPa', level = 500)[0]

# Read the data for a specific region
R500 = spfh500.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]
#print(R500.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Layer-averaged thetas and mixing ratios
THETAA = T950
A1 = T850 + T700
THETAB = 0.5 * A1
THETAC = T500
RA = R950
C2 = R850 + R700
RB = 0.5 * C2
RC = R500

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Calculate the Theta-E (EPT) Proxys 
L0 = 2690000
alpha = -10
cpd = 1005.7
p1 = L0 * RA
p2 = L0 * RB
p3 = L0 * RC
p4 = cpd * T850
x1 = p1 / p4
x2 = p2 / p4
x3 = p3 / p4 
y1 = np.exp(x1)
y2 = np.exp(x2)
y3 = np.exp(x3)
EPTPA = THETAA * y1
EPTPB = THETAB * y2 + alpha
EPTPC = THETAC * y3 + alpha

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Calculate the EPT Core Index (ECI)
beta = 303
ME = EPTPC - beta
LE = EPTPA - beta
gamma= 0.065

# Decide the value of the ECI
ECI = np.where(LE <= 0, 0, gamma * LE * ME)

#print("ECI Max.: ", ECI.max())
#print("ECI Min.: ", ECI.min())
#print(ECI)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Calculate the Mid Warming Index (MWI)
tau = 263.15
mu = -7
calc1 = temp500 - tau

# Decide the value of the MWI
MWI = np.where(calc1 <= 0, 0, calc1 * mu)

#print("MWI Max.: ", MWI.max())
#print("MWI Min.: ", MWI.min()) 
#print(MWI) 

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Calculate the Inversion Index (II)
sigma = 1.5
op1 = temp950 - temp700
S = sigma * op1
op2 = EPTPB - EPTPA
D = sigma * op2
calc2 = D + S

# Decide the value of the II
II = np.where(calc2 <= 0, D + S, 0)

#print("II Max.: ", II.max())
#print("II Min.: ", II.min()) 
#print(II) 
 
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Orography correction just to aid visualization for forecaster. Co is added to the GDI
pp1 = 500
pp2 = 9000
pp3 = 18
divisor = sfcps - pp1
division = pp2 / divisor
C0 = pp3 - division

#print("C0 Max.: ", C0.max())
#print("C0 Min.: ", C0.min()) 
#print(C0) 

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Galvez Davison Index - Indices with and without correction
GDI = ECI + MWI + II
GDIc = ECI + MWI + II + C0

# To smooth the contours
import scipy.ndimage
GDIc = scipy.ndimage.zoom(GDIc, 3)
lats = scipy.ndimage.zoom(lats, 3)
lons = scipy.ndimage.zoom(lons, 3)

#print(GDI.shape)
#print(GDIc.shape)

#print(GDIc.max())
#print(GDIc.min())

#print("GDIc Max.: ", GDIc.max())
#print("GDIc Min.: ", GDIc.min()) 
#print(GDIc) 
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Create the color scale 
colors = ["#323232", "#646464", "#737373", "#7e7e7e", "#909090", "#a3a3a3", "#b1b1b1", "#bcbcbc", "#bbc7cb", "#b2d2dd", "#90d5bb", "#55d065", "#5acf28", "#bad411", "#ffcc00", "#ffa900", "#fc8106", "#eb4722", "#d8133a", "#ac0a1d"]
cmap = matplotlib.colors.ListedColormap(colors)
cmap.set_over('#800000')
cmap.set_under('#000000')
vmin = -30
vmax = 70
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
data_min = -30 
data_max = 70 
interval = 5
levels = np.arange(data_min,data_max,interval)
 
# Plot the image
img1 = ax.contourf(lons, lats, GDIc, transform=ccrs.PlateCarree(), cmap=cmap, levels=levels, extend='both')
img2 = ax.contour(lons, lats, GDIc, transform=ccrs.PlateCarree(), colors='black', linewidths=0.1, levels=levels)
ax.clabel(img2, inline=1, inline_spacing=0, fontsize=10,fmt = '%1.0f', colors= 'black')


# Add states and provinces
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='white',facecolor='none', linewidth=0.25, zorder=2)

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
plt.title("GFS (0.5°): Galvez Davison Index (GDI)", fontweight='bold', fontsize=10, loc='left')
plt.title("Init: " + str(init)[:-6] + "Z | Forecast Hour: [" + str(ftime).zfill(3) + "]" + " | Valid: " + str(valid)[:-6] + "Z ", fontsize=10, loc='right')

# To put colorbar inside picture
axins1 = inset_axes(ax, width="2%", height="100%", loc='right', borderpad=0.0)

# Add a colorbar
ticks = np.arange(data_min, data_max, interval).tolist()     
ticks = interval * np.round(np.true_divide(ticks,interval))
ticks = ticks[1:]
cb = fig.colorbar(img1, label="Galvez Davison Index (GDI)", cax=axins1, orientation="vertical", ticks=ticks)
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
plt.savefig('GFS' + '_GDINDX_' + str(init)[:-9].replace('-', '') + str(hour).zfill(2) + 'Z_' + str(ftime).zfill(3) + '.png', bbox_inches='tight', pad_inches=0)

# Show the image
plt.show()

# Total processing time
print('Total processing time:', round((t.time() - start),2), 'seconds.') 
