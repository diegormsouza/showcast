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
__version__ = "2.5.0"
__maintainer__ = "Diego Souza"
__email__ = "diego.souza@inpe.br"
__status__ = "Production"
__last_modified__ = "Jun 2023"
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Required modules
#--------------------------------
#to run in a pure text terminal:
import matplotlib
from pyproj import transform
matplotlib.use('Agg')
#--------------------------------
from netCDF4 import Dataset                                  # Read / Write NetCDF4 files
from mpl_toolkits.axes_grid1.inset_locator import inset_axes # Add a child inset axes to this existing axes.
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
from cpt_convert import loadCPT                              # Import the CPT convert function
from matplotlib.colors import LinearSegmentedColormap        # Linear interpolation for color maps
import matplotlib.pyplot as plt                              # Plotting library
import matplotlib.colors                                     # Matplotlib colors
import numpy as np                                           # Scientific computing with Python
import cartopy, cartopy.crs as ccrs                          # Plot maps
import cartopy.io.shapereader as shpreader                   # Import shapefiles
import time as t                                             # Time access and conversion
import math                                                  # Import math
import re                                                    # re
import glob                                                  # Unix style pathname pattern expansion
import sys                                                   # Import the "system specific parameters and functions" module
import os 												     # Miscellaneous operating system interfaces
from os.path import dirname, abspath                         # Return a normalized absolutized version of the pathname path 
import platform                                              # To check which OS is being used
from html_update import update                               # Update the HTML animation 
from remap import remap                                      # Import the Remap function
import matplotlib.patheffects as PathEffects
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()  

# SHOWCast directory:
main_dir = dirname(dirname(abspath(__file__)))

# Band 01 file
path_ch01 = (sys.argv[1])

# For the log
path = path_ch01

# Read the sector
sector = (sys.argv[9])
sector = sector[:-3]
#---------------------------------------------------------------------------------------------
# Read the interval and check if this file should be processed based on the config file
# import re                        # Regular expression operations
# intervals = (sys.argv[9])        # Read the string from the parameters
# intervals = intervals.split(",") # Split the string in a list
# for interval in intervals:       # For each interval in the list, check the file
    #print(interval)
#    regex = re.compile(r'(?:s.........' + str(interval) + ')..._')
#    finder = re.findall(regex, path)
    # If "matches" is "0", it is not from a desired interval. If it is "1", process the file	
#    matches = len(finder)
    # If it is from a desired minute, exit verification loop
#    if (matches == 1): break
#if (matches == 0): # After the loop, if "matches" is "0", the file is not from a desired interval
#    print("This file is not from an interval that should be processed. Exiting script.")
    # Put the processed file on the log
#    import datetime # Basic Date and Time types
#    with open(main_dir + '//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
#        log.write(str(datetime.datetime.now()))
#        log.write('\n')
#        log.write(path + '\n')
#        log.write('\n')
#    quit()
#---------------------------------------------------------------------------------------------  

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Remove the identification
path_ch01 = path_ch01[:-7]

# Get the Band 02, same file
osystem = platform.system()
if osystem == "Windows":
    path_ch02 = re.sub('Band01\\\\OR_ABI-L2-CMIPF*(.*)', '', path_ch01)
else:
    path_ch02 = re.sub('Band01/OR_ABI-L2-CMIPF*(.*)', '', path_ch01)

# Get the start of scan from the file name
scan_start = (path_ch01[path_ch01.find("_s")+2:path_ch01.find("_e")])

#------------------------------------------------------------------------------------------------------

file = []
for filename in sorted(glob.glob(path_ch02+'Band02//OR_ABI-L2-CMIPF-M*C02_G1*.nc')):
    file.append(filename)
    
# Seek for a GOES-16 file (same time) in the directory
matching = [s for s in file if scan_start in s]     

# If the file is not found, exit the loop
if not matching:
    print("File Not Found! Exiting Script.")
    sys.exit()
else: # If the file is found, continue
    print("File OK!")
    matching = matching[0]
    index = file.index(matching)
    path_ch02 = file[index]

#------------------------------------------------------------------------------------------------------

# Get the Band 03, same file
osystem = platform.system()
if osystem == "Windows":
    path_ch03 = re.sub('Band01\\\\OR_ABI-L2-CMIPF*(.*)', '', path_ch01)
else:
    path_ch03 = re.sub('Band01/OR_ABI-L2-CMIPF*(.*)', '', path_ch01)

# Get the start of scan from the file name
scan_start = (path_ch01[path_ch01.find("_s")+2:path_ch01.find("_e")])

#------------------------------------------------------------------------------------------------------

file = []
for filename in sorted(glob.glob(path_ch03+'Band03//OR_ABI-L2-CMIPF-M*C03_G1*.nc')):
    file.append(filename)
    
# Seek for a GOES-16 file (same time) in the directory
matching = [s for s in file if scan_start in s]     

# If the file is not found, exit the loop
if not matching:
    print("File Not Found! Exiting Script.")
    sys.exit()
else: # If the file is found, continue
    print("File OK!")
    matching = matching[0]
    index = file.index(matching)
    path_ch03 = file[index]

#------------------------------------------------------------------------------------------------------

#print(path_ch01)
#print(path_ch02)
#print(path_ch03)
#quit()

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Read the image
file_ch01 = Dataset(path_ch01)

# Read the satellite 
satellite = getattr(file_ch01, 'platform_ID')

# Read the band number
band = str(file_ch01.variables['band_id'][0]).zfill(2)

# Desired resolution
resolution = int(sys.argv[6])

# Read the resolution
band_resolution_km = getattr(file_ch01, 'spatial_resolution')
band_resolution_km = float(band_resolution_km[:band_resolution_km.find("km")])

# Division factor to reduce image size
f = math.ceil(float(resolution / band_resolution_km))

# Read the central longitude
longitude = file_ch01.variables['goes_imager_projection'].longitude_of_projection_origin

# Read the semi major axis
a = file_ch01.variables['goes_imager_projection'].semi_major_axis

# Read the semi minor axis
b = file_ch01.variables['goes_imager_projection'].semi_minor_axis

# Calculate the image extent 
h = file_ch01.variables['goes_imager_projection'].perspective_point_height
x1 = file_ch01.variables['x_image_bounds'][0] * h 
x2 = file_ch01.variables['x_image_bounds'][1] * h 
y1 = file_ch01.variables['y_image_bounds'][1] * h 
y2 = file_ch01.variables['y_image_bounds'][0] * h 

# Getting the file time and date
add_seconds = int(file_ch01.variables['time_bounds'][0])
date = datetime(2000,1,1,12) + timedelta(seconds=add_seconds)
date_formated = date.strftime('%Y-%m-%d %H:%M UTC')
date_file = date.strftime('%Y%m%d%H%M')
year = date.strftime('%Y')
month = date.strftime('%m')
day = date.strftime('%d')
hour = date.strftime('%H')
minutes = date.strftime('%M')

# Choose the visualization extent (min lon, min lat, max lon, max lat)
extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]

# Variable to remap
variable = "CMI"

# Call the reprojection funcion
grid = remap(path_ch01, variable, extent, resolution, h, a, b, longitude, x1, y1, x2, y2)
     
# Read the data returned by the function 
data_ch01 = grid.ReadAsArray()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Read the image
file_ch02 = Dataset(path_ch02)

# Variable to remap
variable = "CMI"

# Call the reprojection funcion
grid = remap(path_ch02, variable, extent, resolution, h, a, b, longitude, x1, y1, x2, y2)
     
# Read the data returned by the function 
data_ch02 = grid.ReadAsArray()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Read the image
file_ch03 = Dataset(path_ch03)

# Variable to remap
variable = "CMI"

# Call the reprojection funcion
grid = remap(path_ch03, variable, extent, resolution, h, a, b, longitude, x1, y1, x2, y2)
     
# Read the data returned by the function 
data_ch03 = grid.ReadAsArray()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Calculates the solar zenith angle 
from pyorbital import astronomy
from datetime import datetime

print("Calculating the lons and lats...")
# Create the lats and lons based on the extent
lat = np.linspace(extent[3], extent[1], data_ch01.shape[0])
lon = np.linspace(extent[0], extent[2], data_ch01.shape[1])
xx,yy = np.meshgrid(lon,lat)
lons = xx.reshape(data_ch01.shape[0], data_ch01.shape[1])
lats = yy.reshape(data_ch01.shape[0], data_ch01.shape[1])

# Get the year month day hour and minute to apply the zenith correction
utc_time = datetime(int(year), int(month), int(day), int(hour), int(minutes))
sun_zenith = np.zeros((data_ch01.shape[0], data_ch01.shape[1]))
sun_zenith = astronomy.sun_zenith_angle(utc_time, lons, lats)

# Apply the sun zenith correction
data_ch01 = (data_ch01)/(np.cos(np.deg2rad(sun_zenith)))
data_ch02 = (data_ch02)/(np.cos(np.deg2rad(sun_zenith)))
data_ch03 = (data_ch03)/(np.cos(np.deg2rad(sun_zenith)))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
print("Applying the Rayleigh correction...")

# Applying the Rayleigh correction
from pyspectral.rayleigh import Rayleigh     # Atmospherioc correction in the visible spectrum 
from pyorbital.astronomy import get_alt_az
from pyorbital.orbital import get_observer_look

# Satellite height
sat_h = file_ch01.variables['goes_imager_projection'].perspective_point_height

sunalt, suna = get_alt_az(utc_time, lons, lats)
suna = np.rad2deg(suna)
#sata, satel = get_observer_look(sat_lon, sat_lat, sat_alt, vis.attrs['start_time'], lons, lats, 0)
sata, satel = get_observer_look(longitude, 0.0, sat_h, utc_time, lons, lats, 0)
satz = 90 - satel

# Reyleigh Correction
atmosphere = 'us-standard'
aerosol_type = 'rayleigh_only'
rayleigh_key = ('GOES-16','abi', atmosphere, aerosol_type)
corrector = Rayleigh('GOES-16', 'abi', atmosphere=atmosphere, aerosol_type=aerosol_type)

sata = sata % 360.
suna = suna % 360.
ssadiff = np.absolute(suna - sata)
ssadiff = np.minimum(ssadiff, 360 - ssadiff)

red = data_ch02 * 100

refl_cor_band_c01 = corrector.get_reflectance(sun_zenith, satz, ssadiff, 'C01', redband=red)
data_ch01 = data_ch01 - (refl_cor_band_c01 / 100)

refl_cor_band_c02 = corrector.get_reflectance(sun_zenith, satz, ssadiff, 'C02', redband=red)
data_ch02 = data_ch02 - (refl_cor_band_c02 / 100)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# RGB Components
R = data_ch02
G = (data_ch01 + data_ch02) / 2 * 0.93 + 0.07 * data_ch03 
B = data_ch01

# Apply the CIRA Strech
band_data = R 
log_root = np.log10(0.0223)
denom = (1.0 - log_root) * 0.75
band_data *= 0.01
band_data = band_data.clip(np.finfo(float).eps)
band_data = np.log10(band_data)
band_data -= log_root
band_data /= denom
R  = 1 + band_data
#print (R.shape)

band_data = G
log_root = np.log10(0.0223)
denom = (1.0 - log_root) * 0.75
band_data *= 0.01
band_data = band_data.clip(np.finfo(float).eps)
band_data = np.log10(band_data)
band_data -= log_root
band_data /= denom
G = 1 + band_data
#print (G.shape)

band_data = B
log_root = np.log10(0.0223)
denom = (1.0 - log_root) * 0.75
band_data *= 0.01
band_data = band_data.clip(np.finfo(float).eps)
band_data = np.log10(band_data)
band_data -= log_root
band_data /= denom
B = 1 + band_data
#print (B.shape)

# Create the RGB
RGB = np.stack([R, G, B], axis=2)		
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Product Name
product = "TRURGB" + sector
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
# Plot configuration
plot_config = {
"resolution": band_resolution_km, 
"dpi": 150, 
"states_color": 'gold', "states_width": 0.5, 
"countries_color": 'gold', "countries_width": 0.5,
"continents_color": 'gold', "continents_width": 0.5,
"grid_color": 'white', "grid_width": 0.3, "grid_interval": 5.0,
"vmin": 0, "vmax": 1, "cmap": 'jet',
"title_text": "GOES-" + satellite[1:3] + " True Color RGB + NHC (Color verdadero + NHC)", "title_size": 8, "title_x_offset": int(data_ch01.shape[1] * 0.01), "title_y_offset": data_ch01.shape[0] - int(data_ch01.shape[0] * 0.016), 
"thick_interval": 0, "cbar_labelsize": 8, "cbar_labelpad": -int(data_ch01.shape[0] * 0.0),
"file_name_id_1": satellite,  "file_name_id_2": product
}
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
fig = plt.figure(figsize=(1920/float(plot_config["dpi"]), 1080/float(plot_config["dpi"])), dpi=plot_config["dpi"])
  
# Define the projection
proj = ccrs.PlateCarree()

# Use the PlateCarree projection in cartopy
ax = plt.axes([0, 0, 1, 1], projection=proj)
ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

# Define the image extent
img_extent = [extent[0], extent[2], extent[1], extent[3]]

# Plot the image
img = ax.imshow(RGB, origin='upper', extent=img_extent, zorder=1)

# Add states and provinces
# shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//El_Salvador_departamentos.shp').geometries())
# ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=2)

# Add countries
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//Centro_America.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=2)

# Add continents
shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//GSHHS_h_L1_clipped.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=3)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Hurricane tracks 
#---------------------------------------------------------------------------------------------
# Required libs
import urllib.request
import zipfile
from tropycal import realtime
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Invest: plot monitoring areas
#---------------------------------------------------------------------------------------------
# Cleaning NHC working dir
for files in glob.glob(main_dir + "//Shapefiles//nhc//*"):
    os.remove(files)
# Downloading latest GIS data for selected monitoring areas:
nhc_gis_files = "https://www.nhc.noaa.gov/xgtwo/gtwo_shapefiles.zip"
urllib.request.urlretrieve(nhc_gis_files, main_dir + "//Shapefiles//nhc//gtwo_shapefiles.zip")
with zipfile.ZipFile(main_dir + "//Shapefiles//nhc//gtwo_shapefiles.zip", 'r') as zip_ref:
    zip_ref.extractall(main_dir + "//Shapefiles//nhc//")
# Reading NHC shapefiles
shp_files = []
for filename in glob.glob(main_dir + '//Shapefiles//nhc//gtwo_areas_*.shp'):
    shp_files.append(os.path.normpath(filename))
for filename in glob.glob(main_dir + '//Shapefiles//nhc//gtwo_points_*.shp'):
    shp_files.append(os.path.normpath(filename))
for filename in glob.glob(main_dir + '//Shapefiles//nhc//gtwo_lines_*.shp'):
    shp_files.append(os.path.normpath(filename))
# Add probabilities areas
shapefile = list(shpreader.Reader(shp_files[0]).records())
areas_low = [x.geometry for x in shapefile if float(x.attributes['PROB2DAY'].replace("%", "")) < 40]
areas_medium = [x.geometry for x in shapefile if float(x.attributes['PROB2DAY'].replace("%", "")) >= 40 and float(x.attributes['PROB2DAY'].replace("%", "")) <= 60]
areas_high = [x.geometry for x in shapefile if float(x.attributes['PROB2DAY'].replace("%", "")) > 60]
# Plotting probabilities ares
ax.add_geometries(areas_low, ccrs.PlateCarree(), edgecolor='gold',facecolor='yellow',alpha=0.4, linewidth=plot_config["states_width"]*6, zorder=4)
ax.add_geometries(areas_medium, ccrs.PlateCarree(), edgecolor='darkorange',facecolor='orange',alpha=0.4, linewidth=plot_config["states_width"]*6, zorder=4)
ax.add_geometries(areas_high, ccrs.PlateCarree(), edgecolor='darkred',facecolor='red',alpha=0.4, linewidth=plot_config["states_width"]*6, zorder=4)
# Add trajectories areas
shapefile = list(shpreader.Reader(shp_files[2]).records())
trajectories_low = [x.geometry for x in shapefile if float(x.attributes['PROB2DAY'].replace("%", "")) < 40]
trajectories_medium = [x.geometry for x in shapefile if float(x.attributes['PROB2DAY'].replace("%", "")) >= 40 and float(x.attributes['PROB2DAY'].replace("%", "")) <= 60]
trajectories_high = [x.geometry for x in shapefile if float(x.attributes['PROB2DAY'].replace("%", "")) > 60]
# Plotting trajectories
ax.add_geometries(trajectories_low, ccrs.PlateCarree(), edgecolor='gold',facecolor='none', alpha=0.4, linewidth=plot_config["states_width"]*6, zorder=4)
ax.add_geometries(trajectories_medium, ccrs.PlateCarree(), edgecolor='darkorange',facecolor='none', alpha=0.4, linewidth=plot_config["states_width"]*6, zorder=4)
ax.add_geometries(trajectories_high, ccrs.PlateCarree(), edgecolor='darkred',facecolor='none', alpha=0.4, linewidth=plot_config["states_width"]*6, zorder=4)
# Add positions
shapefile = list(shpreader.Reader(shp_files[1]).records())
points_low = [x for x in shapefile if float(x.attributes['PROB2DAY'].replace("%", "")) < 40]
points_medium = [x for x in shapefile if float(x.attributes['PROB2DAY'].replace("%", "")) >= 40 and float(x.attributes['PROB2DAY'].replace("%", "")) <= 60]
points_high = [x for x in shapefile if float(x.attributes['PROB2DAY'].replace("%", "")) > 60]
# Plotting positions and labels
for pl in points_low:
    ax.scatter(pl.geometry.x,pl.geometry.y, marker='X', s=150, edgecolor='black', facecolor='gold', transform=ccrs.PlateCarree(), zorder=9)
    if float(pl.attributes['PROB2DAY'].replace("%", "")) < 40:
        text = ax.text(pl.geometry.x+0.5,pl.geometry.y+0.5,'2d: '+pl.attributes['PROB2DAY'],color='gold', fontsize='large', fontweight='bold',zorder=9)
        text.set_path_effects([PathEffects.withStroke(linewidth=1.5, foreground='k')])
    elif float(pl.attributes['PROB2DAY'].replace("%", "")) >= 40 and float(pl.attributes['PROB2DAY'].replace("%", "")) <= 60:
        text = ax.text(pl.geometry.x+0.5,pl.geometry.y+0.5,'2d: '+pl.attributes['PROB2DAY'],color='orange', fontsize='large', fontweight='bold',zorder=9)
        text.set_path_effects([PathEffects.withStroke(linewidth=1.5, foreground='k')])
    else:
        text = ax.text(pl.geometry.x+0.5,pl.geometry.y+0.5,'2d: '+pl.attributes['PROB2DAY'],color='red', fontsize='large', fontweight='bold',zorder=9)
        text.set_path_effects([PathEffects.withStroke(linewidth=1.5, foreground='k')])
    text = ax.text(pl.geometry.x+0.5,pl.geometry.y-0.5,'7d: '+pl.attributes['PROB7DAY'],color='gold', fontsize='large', fontweight='bold',zorder=9)
    text.set_path_effects([PathEffects.withStroke(linewidth=1.5, foreground='k')])
for pm in points_medium:
    ax.scatter(pm.geometry.x,pm.geometry.y, marker='X', s=150, edgecolor='black', facecolor='orange', transform=ccrs.PlateCarree(), zorder=9)
    if float(pm.attributes['PROB2DAY'].replace("%", "")) < 40:
        text = ax.text(pm.geometry.x+0.5,pm.geometry.y+0.5,'2d: '+pm.attributes['PROB2DAY'],color='gold', fontsize='large', fontweight='bold',zorder=9)
        text.set_path_effects([PathEffects.withStroke(linewidth=1.5, foreground='k')])
    elif float(pm.attributes['PROB2DAY'].replace("%", "")) >= 40 and float(pm.attributes['PROB2DAY'].replace("%", "")) <= 60:
        text = ax.text(pm.geometry.x+0.5,pm.geometry.y+0.5,'2d: '+pm.attributes['PROB2DAY'],color='orange', fontsize='large', fontweight='bold',zorder=9)
        text.set_path_effects([PathEffects.withStroke(linewidth=1.5, foreground='k')])
    else:
        text = ax.text(pm.geometry.x+0.5,pm.geometry.y+0.5,'2d: '+pm.attributes['PROB2DAY'],color='red', fontsize='large', fontweight='bold',zorder=9)
        text.set_path_effects([PathEffects.withStroke(linewidth=1.5, foreground='k')])
    text = ax.text(pm.geometry.x+0.5,pm.geometry.y-0.5,'7d: '+pm.attributes['PROB7DAY'],color='orange', fontsize='large', fontweight='bold',zorder=9)
    text.set_path_effects([PathEffects.withStroke(linewidth=1.5, foreground='k')])
for ph in points_high:
    ax.scatter(ph.geometry.x,ph.geometry.y, marker='X', s=150, edgecolor='black', facecolor='red', transform=ccrs.PlateCarree(), zorder=9)
    if float(ph.attributes['PROB2DAY'].replace("%", "")) < 40:
        text = ax.text(ph.geometry.x+0.5,ph.geometry.y+0.5,'2d: '+ph.attributes['PROB2DAY'],color='gold', fontsize='large', fontweight='bold',zorder=9)
        text.set_path_effects([PathEffects.withStroke(linewidth=1.5, foreground='k')])
    elif float(ph.attributes['PROB2DAY'].replace("%", "")) >= 40 and float(ph.attributes['PROB2DAY'].replace("%", "")) <= 60:
        text = ax.text(ph.geometry.x+0.5,ph.geometry.y+0.5,'2d: '+ph.attributes['PROB2DAY'],color='orange', fontsize='large', fontweight='bold',zorder=9)
        text.set_path_effects([PathEffects.withStroke(linewidth=1.5, foreground='k')])
    else:
        text = ax.text(ph.geometry.x+0.5,ph.geometry.y+0.5,'2d: '+ph.attributes['PROB2DAY'],color='red', fontsize='large', fontweight='bold',zorder=9)
        text.set_path_effects([PathEffects.withStroke(linewidth=1.5, foreground='k')])
    text = ax.text(ph.geometry.x+0.5,ph.geometry.y-0.5,'7d: '+ph.attributes['PROB7DAY'],color='red', fontsize='large', fontweight='bold',zorder=9)
    text.set_path_effects([PathEffects.withStroke(linewidth=1.5, foreground='k')])
# Reading realtime active NHC data:
realtime_obj = realtime.Realtime()
# Extracting list of active system names
tsystems = realtime_obj.list_active_storms(basin='all')
# Checking if a system name is an Invest or not
for name in tsystems:
    storm = realtime_obj.get_storm(name)
    if storm.invest == True:
        print(name + " is an invest!")
    else:
        print(name + " is not an invest!")
        #---------------------------------------------------------------------------------------------
        # Invest: plot monitoring areas
        #---------------------------------------------------------------------------------------------
        # Cleaning NHC working dir
        for files in glob.glob(main_dir + "//Shapefiles//nhc//*"):
            os.remove(files)
        # Downloading latest GIS data for selected storm:
        nhc_gis_files = "https://www.nhc.noaa.gov/gis/forecast/archive/"+name.lower()+"_5day_latest.zip"
        urllib.request.urlretrieve(nhc_gis_files, main_dir + "//Shapefiles//nhc//"+name.lower()+"_5day_latest.zip")
        with zipfile.ZipFile(main_dir + "//Shapefiles//nhc//"+name.lower()+"_5day_latest.zip", 'r') as zip_ref:
             zip_ref.extractall(main_dir + "//Shapefiles//nhc//")
        # Reading NHC shapefiles
        shp_files = []
        for filename in glob.glob(main_dir + '//Shapefiles//nhc//'+name.lower()+'*_5day_lin.shp'):
            shp_files.append(os.path.normpath(filename))
        for filename in glob.glob(main_dir + '//Shapefiles//nhc//'+name.lower()+'*_5day_pgn.shp'):
            shp_files.append(os.path.normpath(filename))
        for filename in glob.glob(main_dir + '//Shapefiles//nhc//'+name.lower()+'*_5day_pts.shp'):
            shp_files.append(os.path.normpath(filename))
        # Add line trajectory
        shapefile = list(shpreader.Reader(shp_files[0]).geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='white',facecolor='none', linewidth=plot_config["states_width"]*4, zorder=4)
        # Add probabilities cone
        shapefile = list(shpreader.Reader(shp_files[1]).geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black',facecolor='white', alpha=0.4,linewidth=plot_config["states_width"]*4, zorder=4)
        # Add positions
        shapefile = list(shpreader.Reader(shp_files[2]).geometries())
        # Plotting positions and labels
        ax.scatter([shapefile.x for shapefile in shapefile],[shapefile.y for shapefile in shapefile], edgecolor='black', facecolor='red', transform=ccrs.PlateCarree(), zorder=5)
        shapefile = list(shpreader.Reader(shp_files[2]).records())
        for field in shapefile:
            text = ax.text((field.attributes['LON']+0.5),(field.attributes['LAT']+0.5),field.attributes['DVLBL'],color='blue', fontsize='large', fontweight='bold',zorder=5)
            text.set_path_effects([PathEffects.withStroke(linewidth=1.5, foreground='w')])

#---------------------------------------------------------------------------------------------
# Add coastlines, borders and gridlines
gl = ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=True, zorder=5)
gl.bottom_labels = False
gl.right_labels = False
gl.xpadding = -2
gl.ypadding = -2
gl.xlabel_style = {'size': 6, 'weight': 'bold', 'color': 'white'}
gl.ylabel_style = {'size': 6, 'weight': 'bold', 'color': 'white'}

# Remove the outline border
ax.outline_patch.set_visible(False)
  
# Add a title
plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(0.015,0.965), xycoords='figure fraction', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=10)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Add labels to specific coordinates

import configparser
conf = configparser.ConfigParser()
if (satellite == 'G16'):
    conf.read(main_dir + '//Utils//Labels//labels_g16_cam.ini')
elif (satellite == 'G17'):
    conf.read(main_dir + '//Utils//Labels//labels_g17.ini')

labels, city_lons, city_lats, x_offsets, y_offsets, sizes, colors, marker_types, marker_colors, marker_sizes = [],[],[],[],[],[],[],[],[],[]

for each_section in conf.sections():
    for (each_key, each_val) in conf.items(each_section):
        if (each_key == 'label'): labels.append(each_val)
        if (each_key == 'lon'): city_lons.append(float(each_val))
        if (each_key == 'lat'): city_lats.append(float(each_val))
        if (each_key == 'x_offset'): x_offsets.append(float(each_val))
        if (each_key == 'y_offset'): y_offsets.append(float(each_val))
        if (each_key == 'size'): sizes.append(int(each_val))
        if (each_key == 'color'): colors.append(each_val)
        if (each_key == 'marker_type'): marker_types.append(each_val)
        if (each_key == 'marker_color'): marker_colors.append(each_val)
        if (each_key == 'marker_size'): marker_sizes.append(each_val)
 
import matplotlib.patheffects as PathEffects
for label, xpt, ypt, x_offset, y_offset, size, col, mtype, mcolor, msize in zip(labels, city_lons, city_lats, x_offsets, y_offsets, sizes, colors, marker_types, marker_colors, marker_sizes):
    ax.plot(xpt, ypt, str(mtype), color=str(mcolor), markersize=int(msize), transform=ccrs.Geodetic(), markeredgewidth=1.0, markeredgecolor=(0, 0, 0, 1), zorder=11)
    txt = ax.text(xpt+x_offset , ypt+y_offset, label, fontsize=int(size), fontweight='bold', color=str(col), transform=ccrs.Geodetic(), zorder=12)
    txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='black')])
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Add logos / images to the plot
my_logo = plt.imread(main_dir + '//Logos//my_logo.webp')
newax = fig.add_axes([0.84, 0.015, 0.15, 0.15], anchor='SW', zorder=13) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
newax.imshow(my_logo)
newax.axis('off')

# Add a legend to the plot
# my_legend = plt.imread(main_dir + '//Legends//TRUECOLOR_legend.webp')
# newax = fig.add_axes([0.55, 0.55, 0.44, 0.44], anchor='NE', zorder=13) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
# newax.imshow(my_legend)
# newax.axis('off')
    
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Create the satellite output directory if it doesn't exist
out_dir = (sys.argv[7]) + satellite
if not os.path.exists(out_dir):
   os.mkdir(out_dir)

# Create the product output directory if it doesn't exist
out_dir = (sys.argv[7]) + satellite + '//' + product + '//'
if not os.path.exists(out_dir):
   os.mkdir(out_dir)
   
# Save the image
plt.savefig(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.png', facecolor='black')

# Convert to webp
from PIL.WebPImagePlugin import Image          
im = Image.open(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.png')
im.save(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.webp', format = "WebP", lossless = True)
im.close()

# Update the animation
nfiles = 25
update(satellite, product, nfiles, sys.argv[7], sys.argv[8],sector)

# Delete aux files
os.remove(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.png')  

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

print('Total processing time:', round((t.time() - start),2), 'seconds.') 
