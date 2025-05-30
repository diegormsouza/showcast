#######################################################################################################
# LICENSE
# Copyright (C) 2019 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU 
# General Public License as published by the Free Software Foundation, either version 3 of the License, 
# or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without 
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General 
# Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. 
# If not, see http://www.gnu.org/licenses/.
#######################################################################################################
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Required modules
from netCDF4 import Dataset, num2date                        # Read / Write NetCDF4 files
from mpl_toolkits.axes_grid1.inset_locator import inset_axes # Add a child inset axes to this existing axes.
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
from cpt_convert import loadCPT                              # Import the CPT convert function
from matplotlib.colors import LinearSegmentedColormap        # Linear interpolation for color maps
import matplotlib.pyplot as plt                              # Plotting library
import numpy as np                                           # Scientific computing with Python
import cartopy, cartopy.crs as ccrs                          # Plot maps
import cartopy.io.shapereader as shpreader                   # Import shapefiles
import time as t                                             # Time access and conversion
import scipy as sp                                           # Scipy
from scipy.ndimage import gaussian_filter                    # Scipy Gaussian Filter
from matplotlib.image import imread                          # Read an image from a file into an array
import os                                                    # Miscellaneous operating system interfaces
from cartopy.feature.nightshade import Nightshade            # Draws a polygon where there is no sunlight for the given datetime.
import re                                                    # re
import glob                                                  # Unix style pathname pattern expansion
import sys                                                   # Import the "system specific parameters and functions" module
import math                                                  # Import math
import os 												     # Miscellaneous operating system interfaces
import platform                                              # To check which OS is being used
from html_update import update                               # Update the HTML animation 
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()  

# Read the image
path_dmw = (sys.argv[1])
#path_dmw = ("..//Samples//OR_ABI-L2-DMWF-M6C14_G16_s20192970600363_e20192970610071_c20192970623560.nc")

# For the log
path = path_dmw

#print(path)
	
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Remove the identification
path_dmw = path_dmw[:-4]

#print(path_dmw)
#print(start)

# Get the Band 13, same file
#path_ch13 = re.sub('OR_ABI-L2-DMWF*(.*)', '', path_dmw)

# Get the Band 13, same file
osystem = platform.system()
if osystem == "Windows":
    path_ch13 = re.sub('DMWF-C14\\\\OR_ABI-L2-DMWF*(.*)', '', path_dmw)
    path_ch13 = re.sub('GOES-R-Level-2-Products', '', path_ch13)
else:
    path_ch13 = re.sub('DMWF-C14/OR_ABI-L2-DMWF*(.*)', '', path_dmw)
    path_ch13 = re.sub('GOES-R-Level-2-Products', '', path_ch13)

print(path_dmw)
print(path_ch13)

# Get the start of scan from the file name
scan_start = (path_dmw[path_dmw.find("_s")+2:path_dmw.find("_e")])

file = []
for filename in sorted(glob.glob(path_ch13+'GOES-R-CMI-Imagery//Band13//OR_ABI-L2-CMIPF-M*C13_G16*.nc')):
    file.append(filename)

#print(file)
    
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
    path_ch13 = file[index]

print(path_dmw)
print(path_ch13)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Read the image
#file = Dataset("..//Samples//OR_ABI-L2-DMWF-M6C02_G16_s20192941000351_e20192941010059_c20192941022585.nc")
#file = Dataset("..//Samples//OR_ABI-L2-DMWF-M6C07_G16_s20192941000351_e20192941010071_c20192941023027.nc")
#file = Dataset("..//Samples//OR_ABI-L2-DMWF-M6C08_G16_s20192941000351_e20192941010059_c20192941023042.nc")
#file = Dataset("..//Samples//OR_ABI-L2-DMWF-M6C09_G16_s20192941000351_e20192941010065_c20192941043082.nc")
#file = Dataset("..//Samples//OR_ABI-L2-DMWF-M6C10_G16_s20192941000351_e20192941010071_c20192941043077.nc")
#file = Dataset("..//Samples//OR_ABI-L2-DMWF-M6C14_G16_s20192941000351_e20192941010059_c20192941024086.nc")
file_dmw = Dataset(path_dmw)

# Read the satellite 
satellite = getattr(file_dmw, 'platform_ID')

# Visualization Region
# GOES-R Full Disk
extent = [-156.29, -81.32, 6.29, 81.32]
#extent = [-125.0, -60.0, -15.0, 60.0]

# Define KM_PER_DEGREE
KM_PER_DEGREE = 111.32

# Get the resolution
band_resolution_km = getattr(file_dmw, 'spatial_resolution')
band_resolution_km = float(band_resolution_km[:band_resolution_km.find("km")])

# Get the central longitude
longitude = file_dmw.variables['geospatial_lat_lon_extent'].geospatial_lon_center

# Compute grid dimension
sizex = int(((extent[2] - extent[0]) * KM_PER_DEGREE) / band_resolution_km) * 1
sizey = int(((extent[3] - extent[1]) * KM_PER_DEGREE) / band_resolution_km) * 1

# Getting the band
band = str(file_dmw.variables['band_id'][0]).zfill(2)
	
# Getting the file time and date
add_seconds = int(file_dmw.variables['time_bounds'][0])
date = datetime(2000,1,1,12) + timedelta(seconds=add_seconds)
date_formated = date.strftime('%Y-%m-%d %H:%M UTC')
date_file = date.strftime('%Y%m%d%H%M')
year = date.strftime('%Y')
month = date.strftime('%m')
day = date.strftime('%d')
hour = date.strftime('%H')
minutes = date.strftime('%M')

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Band 13 file
file_ch13 = Dataset(path_ch13)

# Read the satellite 
satellite = getattr(file_ch13, 'platform_ID')

# Read the band number
band = str(file_ch13.variables['band_id'][0]).zfill(2)

# Desired resolution
resolution = int(sys.argv[6])

# Read the resolution
band_resolution_km = getattr(file_ch13, 'spatial_resolution')
band_resolution_km = float(band_resolution_km[:band_resolution_km.find("km")])

# Division factor to reduce image size
f = math.ceil(float(resolution / band_resolution_km))

# Read the central longitude
longitude = file_ch13.variables['goes_imager_projection'].longitude_of_projection_origin

# Calculate the image extent 
H = file_ch13.variables['goes_imager_projection'].perspective_point_height
x1 = file_ch13.variables['x_image_bounds'][0] * H 
x2 = file_ch13.variables['x_image_bounds'][1] * H 
y1 = file_ch13.variables['y_image_bounds'][1] * H 
y2 = file_ch13.variables['y_image_bounds'][0] * H 

# Getting the file time and date
add_seconds = int(file_ch13.variables['time_bounds'][0])
date = datetime(2000,1,1,12) + timedelta(seconds=add_seconds)
#date_formated = date.strftime('%Y-%m-%d %H:%M UTC')
#date_file = date.strftime('%Y%m%d%H%M')
year = date.strftime('%Y')
month = date.strftime('%m')
day = date.strftime('%d')
hour = date.strftime('%H')
minutes = date.strftime('%M')

# Get the pixel values
data = file_ch13.variables['CMI'][:,:][::f ,::f ]

# Product Name
product = "DMWF" + band
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Plot configuration
plot_config = {
"resolution": band_resolution_km, 
"dpi": 150, 
"states_color": 'white', "states_width": data.shape[0] * 0.00006, 
"countries_color": 'gold', "countries_width": data.shape[0] * 0.00012,
"continents_color": 'gold', "continents_width": data.shape[0] * 0.00025,
"grid_color": 'white', "grid_width": data.shape[0] * 0.00025, "grid_interval": 10.0,
"title_text": "GOES-16 DWM + BAND-14", "title_size": int(data.shape[1] * 0.005), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[1] - int(data.shape[1] * 0.016), 
"file_name_id_1": satellite,  "file_name_id_2": product
}
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
fig = plt.figure(figsize=(data.shape[1]/float(plot_config["dpi"]), data.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])
  
# Define the projection
proj = ccrs.Geostationary(central_longitude=longitude, satellite_height=H)
img_extent = (x1,x2,y1,y2)

# Use the Geostationary projection in cartopy
ax = plt.axes([0, 0, 1, 1], projection=proj)

# Add a background image
#ax.stock_img()
fname = os.path.join('..//Maps//', 'land_ocean_ice_8192.jpg')
ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)
date = datetime(int(year), int(month), int(day), int(hour))
#ax.add_feature(Nightshade(date, alpha=0.7), zorder=2)

#print("First layer...")
# Apply range limits for clean IR channel
data1 = data
data1 = np.maximum(data1, 90)
data1 = np.minimum(data1, 313)
# Normalize the channel between a range
data1 = (data1-90)/(313-90)
# Invert colors
data1 = 1 - data1
img = ax.imshow(data1, cmap='gray', vmin=0.1, vmax=0.25, alpha = 0.6, origin='upper', extent=img_extent, zorder=2)

#print("Second layer...")
# SECOND LAYER
data2 = data1
data2[data2 < 0.25] = np.nan
img2 = ax.imshow(data2, cmap='gray', vmin=0.05, vmax=0.50, alpha = 0.7, origin='upper', extent=img_extent, zorder=3)

#print("Third layer...")
# Third LAYER
data2 = data1
data2[data2 < 0.30] = np.nan
img3 = ax.imshow(data2, cmap='gray', vmin=0.05, vmax=0.50, alpha = 1.0, origin='upper', extent=img_extent, zorder=4)

# Add states and provinces
shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=5)

# Add countries
shapefile = list(shpreader.Reader('..//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=6)

# Add continents
shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_coastline.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=7)
  
# Add coastlines, borders and gridlines
ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=False, zorder=8)

# Remove the outline border
ax.outline_patch.set_visible(False)
  
# Add a title
plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=9)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Read the required variables: ================================================ 
pressure = file_dmw.variables['pressure'][:]
temperature = file_dmw.variables['temperature'][:]
wind_direction = file_dmw.variables['wind_direction'][:]
wind_speed = file_dmw.variables['wind_speed'][:]
lats = file_dmw.variables['lat'][:]
lons = file_dmw.variables['lon'][:]
 
# Selecting data only from the region of interest: ============================
# Detect Latitude lower and upper index, according to the selected extent: 
try:
    latli = np.argmin( np.abs( lats - extent[1] ) ) # Lower index
except: 
    # Sometimes the dataset is empty. Put the processed file on the log to avoid processing this data again
    with open('..//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
        log.write(path + '\n')
        sys.exit(1)

latui = np.argmin( np.abs( lats - extent[3] ) ) # Upper index
 
# Detect the Longitude index:
# Store the indexes where the lons are between the selected extent:
lon_ind = np.where(( lons >= extent[0]) & (lons <= extent[2] ))[0]
# Eliminate the lon indexes where we don't have the lat indexes:
lon_ind = lon_ind[(lon_ind >= latui) & (lon_ind <= latli)]
 
# Create the variables lists ==================================================
pressure_a = []
temperature_a = []
wind_direction_a = []
wind_speed_a = []
lats_a = []
lons_a = []

# For each item, append the values to the respective variables ================
for item in lon_ind:
    lons_a.append(lons[item])
    lats_a.append(lats[item])
    pressure_a.append(pressure[item])
    temperature_a.append(temperature[item])
    wind_direction_a.append(wind_direction[item])
    wind_speed_a.append(wind_speed[item])
 
# Read the variables as numpy arrays
temperature = np.asarray(temperature_a)
wind_direction = np.asarray(wind_direction_a)
wind_speed = np.asarray(wind_speed_a)
lons = np.asarray(lons_a)
lats = np.asarray(lats_a)

for x in range(1, 7):
           
    # Read the pressures as python arrays
    pressure = np.asarray(pressure_a)
     
    # Plot the wind vectors divided in 6 pressure ranges, separated by color
    if (x == 1): 
        #print ("Plotting Pressure Range 1: (249-100 hPa)")
        pressure_index = np.where(( pressure >= 100 ) & ( pressure <= 249 ))[0]
        color = '#0000FF' # Blue 
        #color = '#100000' # Blue 
    elif (x == 2):
        #print ("Plotting Range 2: (399-250 hPa)")
        pressure_index = np.where(( pressure >= 250 ) & ( pressure <= 399 ))[0]
        color = '#309AFF' # Light Blue
        #color = '#200000' # Light Blue
    elif (x == 3):
        #print ("Plotting Range 3: (400-549 hPa)")
        pressure_index = np.where(( pressure >= 400 ) & ( pressure <= 549 ))[0]
        color = '#00FF00' # Green
        #color = '#300000' # Green
    elif (x == 4):
        #print ("Plotting Range 4: (699-550 hPa)")
        pressure_index = np.where(( pressure >= 550 ) & ( pressure <= 699 ))[0]
        color = '#FFFF00' # Yellow
        #color = '#400000' # Yellow
    elif (x == 5):
        #print ("Plotting Range 5: (849-700 hPa)")
        pressure_index = np.where(( pressure >= 700 ) & ( pressure <= 849 ))[0]
        color = '#FF0000' # Red
        #color = '#500000' # Red
    elif (x == 6):
        #print ("Plotting Range 6: (1000-850 hPa)")
        pressure_index = np.where(( pressure >= 850 ) & ( pressure <= 1000 ))[0]
        color = '#FF2FCD' # Violet  
        #color = '#600000' # Violet   
     
    # Create the variables lists (considerign only the given pressure range)
    pressure_b = []
    temperature_b = []
    wind_direction_b = []
    wind_speed_b = []
    lats_b = []
    lons_b = []
 
    # For each item, append the values to the respective variables 
    for item in pressure_index:
        lons_b.append(lons_a[item])
        lats_b.append(lats_a[item])
        pressure_b.append(pressure_a[item])
        temperature_b.append(temperature_a[item])
        wind_direction_b.append(wind_direction_a[item])
        wind_speed_b.append(wind_speed_a[item])
         
    # Final variables for the given pressure range
    # Read the variables as numpy arrays
    pressure = np.asarray(pressure_b)
    temperature = np.asarray(temperature_b)
    wind_direction = np.asarray(wind_direction_b)
    wind_speed = np.asarray(wind_speed_b)
    lons = np.asarray(lons_b)
    lats = np.asarray(lats_b)
           
    # Calculating the u and v components using the wind_speed and wind direction
    # in order to plot the barbs. Reference:
    # https://earthscience.stackexchange.com/questions/11982/plotting-wind-barbs-in-python-no-u-v-component
    u = []
    v = []
    for item in range(lons.shape[0]):
        u.append(-(wind_speed[item]) * math.sin((math.pi / 180) * wind_direction[item]))
        v.append(-(wind_speed[item]) * math.cos((math.pi / 180) * wind_direction[item]))
     
    # Read the u and v components as numpy arrays
    u_comp = np.asarray(u) 
    v_comp = np.asarray(v)
     
    # Make the barb plot  
    ax.barbs(lons, lats, u_comp, v_comp, length = 5.0, sizes = dict(emptybarb=0.25, spacing=0.2, height=0.5), linewidth=0.8, pivot='middle', barbcolor=color, transform=ccrs.PlateCarree(), zorder=3)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Create the satellite output directory if it doesn't exist
out_dir = '..//Output//' + satellite
if not os.path.exists(out_dir):
   os.mkdir(out_dir)

# Create the product output directory if it doesn't exist
out_dir = '..//Output//' + satellite + '//' + product + '//'
if not os.path.exists(out_dir):
   os.mkdir(out_dir)
   
# Save the image
plt.savefig(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.png', bbox_inches='tight', pad_inches=0, facecolor='black')

# Update the animation
update(satellite, product)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Put the processed file on the log
import datetime # Basic Date and Time types
with open('..//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
 log.write(str(datetime.datetime.now()))
 log.write('\n')
 log.write(path + '\n')
 log.write('\n')
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

print('Total processing time:', round((t.time() - start),2), 'seconds.') 
