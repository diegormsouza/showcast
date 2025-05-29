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
from mpl_toolkits.axes_grid1.inset_locator import inset_axes # Add a child inset axes to this existing axes.
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
from matplotlib.colors import LinearSegmentedColormap        # Linear interpolation for color maps
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

# Select the desired extent 
extent = [-64.0, -36.0, -40.0, -15.0]

# Read the GRIB file
grib = pygrib.open(path)

# To print all the variables to a txt file
#f = open("gfs_variables.txt", "w")
#for variables in grib:
#    print(variables, file=f)
#f.close()

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------   
  
# Read the surface pressure
ps = grib.select(name='Surface pressure')[0]

# Read the data for a specific region
ps_data, lats, lons = ps.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# Convert the data to numpy arrays
#ps_data = np.array(ps_data)
#lats = np.array(lats) 
#lons = np.array(lons) - 360 # Converting to -180 ~ 180

lons = lons - 360 # Converting to -180 ~ 180

# Convert to hectopascal
ps_data = ps_data / 100

#print(ps_data.shape)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Read the temperature in 950 hPa
temp950 = grib.select(name='Temperature', typeOfLevel = 'isobaricInhPa', level = 950)[0]
#print(temp950)

# Read the data for a specific region
temp950_data, lats, lons = temp950.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# Convert the data to numpy arrays
#temp950_data = np.array(temp950_data)

#print(temp950_data.shape)

T950 = ((temp950_data)*(pow((1000/950),(2/7))))

#print(T950.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Read the specific humidity in 950 hPa
spfh950 = grib.select(name='Specific humidity', typeOfLevel = 'isobaricInhPa', level = 950)[0]
#print(temp950)

# Read the data for a specific region
spfh950_data, lats, lons = spfh950.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# Convert the data to numpy arrays
#spfh950_data = np.array(spfh950_data)

#print(spfh950_data.shape)

R950=spfh950_data

#print(R950.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the temperature in 850 hPa
temp850 = grib.select(name='Temperature', typeOfLevel = 'isobaricInhPa', level = 850)[0]
#print(temp850)

# Read the data for a specific region
temp850_data, lats, lons = temp850.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# Convert the data to numpy arrays
#temp850_data = np.array(temp850_data)

#print(temp850_data.shape)

T850 = ((temp850_data)*(pow((1000/850),(2/7))))

#print(T850.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Read the specific humidity in 850 hPa
spfh850 = grib.select(name='Specific humidity', typeOfLevel = 'isobaricInhPa', level = 850)[0]
#print(temp950)

# Read the data for a specific region
spfh850_data, lats, lons = spfh850.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# Convert the data to numpy arrays
#spfh850_data = np.array(spfh850_data)

#print(spfh850_data.shape)

R850=spfh850_data

#print(R850.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the temperature in 700 hPa
temp700 = grib.select(name='Temperature', typeOfLevel = 'isobaricInhPa', level = 700)[0]
#print(temp850)

# Read the data for a specific region
temp700_data, lats, lons = temp700.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# Convert the data to numpy arrays
#temp700_data = np.array(temp700_data)

#print(temp700_data.shape)

T700 = ((temp700_data)*(pow((1000/700),(2/7))))

#print(T700.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Read the specific humidity in 700 hPa
spfh700 = grib.select(name='Specific humidity', typeOfLevel = 'isobaricInhPa', level = 700)[0]
#print(temp950)

# Read the data for a specific region
spfh700_data, lats, lons = spfh700.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# Convert the data to numpy arrays
#spfh700_data = np.array(spfh700_data)

#print(spfh700_data.shape)

R700=spfh700_data

#print(R700.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Read the temperature in 500 hPa
temp500 = grib.select(name='Temperature', typeOfLevel = 'isobaricInhPa', level = 500)[0]
#print(temp850)

# Read the data for a specific region
temp500_data, lats, lons = temp500.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# Convert the data to numpy arrays
#temp500_data = np.array(temp500_data)

#print(temp500_data.shape)

T500 = ((temp500_data)*(pow((1000/500),(2/7))))

#print(T500.shape)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Read the specific humidity in 500 hPa
spfh500 = grib.select(name='Specific humidity', typeOfLevel = 'isobaricInhPa', level = 500)[0]
#print(temp950)

# Read the data for a specific region
spfh500_data, lats, lons = spfh500.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

# Convert the data to numpy arrays
#spfh500_data = np.array(spfh500_data)

#print(spfh500_data.shape)

R500=spfh500_data

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

#Decide a cuanto equivale el ECI

#print("LE shape: ", LE.shape)

#if (LE <= 0).any():
#    ECI = 0
#else:
#    ECI = gamma * LE * ME

ECI = np.where(LE <= 0, 0, gamma * LE * ME)

print("ECI Max.: ", ECI.max())
print("ECI Min.: ", ECI.min())
print(ECI)
#ECI = gamma * LE * ME
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Calculate the Mid Warming Index (MWI)

tau = 263.15
mu = -7

prueba1 = temp500_data - tau

MWI = np.where(prueba1 <= 0, 0, prueba1 * mu)

print("MWI Max.: ", MWI.max())
print("MWI Min.: ", MWI.min()) 
print(MWI) 
#MWI = (prueba1 * mu)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Calculate the Inversion Index (II)
   
sigma = 1.5
op1 = temp950_data - temp700_data
S = sigma * op1
op2 = EPTPB - EPTPA
D = sigma * op2
prueba2 = D + S

II = np.where(prueba2 <= 0, D + S, 0)

print("II Max.: ", II.max())
print("II Min.: ", II.min()) 
print(II) 
#II = D + S  
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Orography correction just to aid visualization for forecaster. Co is added to the GDI

pp1 = 500
pp2 = 9000
pp3 = 18
divisor = ps_data - pp1
division = pp2 / divisor
C0 = pp3 - division

print("C0 Max.: ", C0.max())
print("C0 Min.: ", C0.min()) 
print(C0) 
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Galvez Davison Index - Indices with and without correction

GDI = ECI + MWI + II

GDIc = ECI + MWI + II + C0

print(GDI.shape)
print(GDIc.shape)

print(GDIc.max())
print(GDIc.min())


print("GDIc Max.: ", GDIc.max())
print("GDIc Min.: ", GDIc.min()) 
print(GDIc) 
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

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
data_min = -30 #np.min(data) 
data_max = 70 #np.max(data) 
interval = 5
levels = np.arange(data_min,data_max,interval)
 
# Plot the image
#img = ax.imshow(data, extent=img_extent, origin='lower', cmap='GnBu', zorder=1)
img1 = ax.contourf(lons, lats, GDIc, transform=ccrs.PlateCarree(), cmap=cmap, levels=levels, extend='both')
img2 = ax.contour(lons, lats, GDIc, transform=ccrs.PlateCarree(), colors='black', linewidths=0.1, levels=levels)
ax.clabel(img2, inline=1, inline_spacing=0, fontsize=10,fmt = '%1.0f', colors= 'black')

# Add coastlines, borders and gridlines
#ax.coastlines(resolution='10m', color='white', linewidth=0.8, zorder=2)
#ax.add_feature(cartopy.feature.BORDERS, edgecolor='white', linewidth=0.5, zorder=3)
#ax.gridlines(color='white', alpha=0.5, linestyle='--', linewidth=0.5, zorder=4)

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
#plt.title("GFS 0.5° - " + grb.name + " (" + grb.units + ")", fontweight='bold', fontsize=10, loc='left')
#plt.title("GFS (0.5°) - " + grb.name + " (°C)", fontweight='bold', fontsize=10, loc='left')
plt.title("GFS (0.5°): Galvez Davison Index (GDI)", fontweight='bold', fontsize=10, loc='left')
plt.title("Init: " + str(ps.analDate)[:-6] + "Z | Forecast Hour: [" + str(ps.forecastTime).zfill(3) + "]" + " | Valid: " + str(ps.validDate)[:-6] + "Z ", fontsize=10, loc='right')

#plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=6)

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
plt.savefig('Image_Test_GDI.png', bbox_inches='tight', pad_inches=0)

#Show the image
plt.show()

print('Total processing time:', round((t.time() - start),2), 'seconds.') 
