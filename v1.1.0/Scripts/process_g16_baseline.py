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
from matplotlib.image import imread                          # Read an image from a file into an array
import os                                                    # Miscellaneous operating system interfaces
import sys                                                   # Import the "system specific parameters and functions" module
from cartopy.feature.nightshade import Nightshade            # Draws a polygon where there is no sunlight for the given datetime.
from html_update import update                               # Update the HTML animation 
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()  

# Image path
path = (sys.argv[1])
#path = ("..//Samples//OR_ABI-L2-ACHAF-M6_G16_s20192671310233_e20192671319541_c20192671321150.nc")
#file = Dataset("..//Samples//OR_ABI-L2-ACHAF-M6_G16_s20192671310233_e20192671319541_c20192671321150.nc")
#file = Dataset("..//Samples//OR_ABI-L2-ACHTF-M6_G16_s20192671310233_e20192671319541_c20192671321151.nc")
#file = Dataset("..//Samples//OR_ABI-L2-ACMF-M6_G16_s20192671310233_e20192671319541_c20192671320284.nc")
#file = Dataset("..//Samples//OR_ABI-L2-ACTPF-M6_G16_s20192671310233_e20192671319541_c20192671320382.nc")
#file = Dataset("..//Samples//OR_ABI-L2-AODF-M6_G16_s20192671310233_e20192671319541_c20192671323574.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CODF-M6_G16_s20192671310233_e20192671319541_c20192671321177.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CPSF-M6_G16_s20192671310233_e20192671319541_c20192671321177.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CTPF-M6_G16_s20192671310233_e20192671319541_c20192671321150.nc")
#file = Dataset("..//Samples//OR_ABI-L2-LSTF-M6_G16_s20192671300233_e20192671309541_c20192671310334.nc")
#file = Dataset("..//Samples//OR_ABI-L2-RRQPEF-M6_G16_s20192671330233_e20192671339541_c20192671340038.nc")
#file = Dataset("..//Samples//OR_ABI-L2-SSTF-M6_G16_s20192671400233_e20192671459541_c20192671505580.nc")
#file = Dataset("..//Samples//OR_ABI-L2-TPWF-M6_G16_s20192671130232_e20192671139540_c20192671141117.nc")

#print(path)

# Read the image
file = Dataset(path)

# Read the satellite 
satellite = getattr(file, 'platform_ID')

# Read the main variable
variable = list(file.variables.keys())[0]

# Read the product name
prod_name = getattr(file, 'title')

# Desired resolution
resolution = int(sys.argv[6])

# Read the resolution
band_resolution_km = getattr(file, 'spatial_resolution')
band_resolution_km = float(band_resolution_km[:band_resolution_km.find("km")])

# Division factor to reduce image size
f = math.ceil(float(resolution / band_resolution_km))

#print(resolution)
#print(band_resolution_km)
#print(f)

# Read the central longitude
longitude = file.variables['goes_imager_projection'].longitude_of_projection_origin

# Calculate the image extent 
h = file.variables['goes_imager_projection'].perspective_point_height
x = file.variables['x_image_bounds'] * h 
y = file.variables['y_image_bounds'] * h 

# Reading the file time and date
add_seconds = int(file.variables['time_bounds'][0])
date = datetime(2000,1,1,12) + timedelta(seconds=add_seconds)
date_formated = date.strftime('%Y-%m-%d %H:%M UTC')
date_file = date.strftime('%Y%m%d%H%M')
year = date.strftime('%Y')
month = date.strftime('%m')
day = date.strftime('%d')
hour = date.strftime('%H')
minutes = date.strftime('%M')

# Read the data
data = file.variables[variable][:,:][::f ,::f]

# Convert from int16 to uint16
data = data.astype(np.float64)

#print(data.shape)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
if (variable == 'HT'):  
    # ACHAF
    colors = ["#000000", "#804000", "#ff00ff", "#0000ff", "#00ffff", "#00ff00", "#ffff00", "#ff0000", "#c0c0c0", "#ffffff"]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    vmin = 0
    vmax = 15000
    thick_interval = 1000
    product = "CLDHGT"
elif (variable == 'TEMP'):  
    # ACHTF
    cmap = 'jet'
    vmin = 180
    vmax = 300
    thick_interval = 10
    data[data == 0] = np.nan
    product = "CLDTMP"
elif (variable == 'BCM'): 
    # ACMF
    colors = ["#ffffff"]
    cmap = matplotlib.colors.ListedColormap(colors)
    vmin = 0
    vmax = 2
    thick_interval = 1
    data[data == 0] = np.nan
    product = "CLDMSK"
elif (variable == 'Phase'): 
    # ACTPF
    colors = ["#00ffff", "#00ff00", "#30782a", "#ff0000"]#, "#000000"]
    cmap = matplotlib.colors.ListedColormap(colors)
    vmin = 1
    vmax = 4
    thick_interval = 1
    data[data == 0] = np.nan
    data[data == 5] = np.nan    
    product = "CLDPHA"
elif (variable == 'AOD'): 
    # AODF
    cmap = 'jet'
    vmin = 0
    vmax = 1
    thick_interval = 0.1
    product = "AEROPT"
elif (variable == 'COD'): 
    # CODF
    cmap = 'jet'
    vmin = 0
    vmax = 100
    thick_interval = 10
    product = "CLDOPT"
elif (variable == 'PSD'): 
    # CPSF
    cmap = 'jet'
    vmin = 0
    vmax = 100
    thick_interval = 10
    product = "CLDPAS"
elif (variable == 'PRES'): 
    # CTPF
    cmap = 'jet'
    vmin = 0
    vmax = 1050
    thick_interval = 100
    product = "CLDPRE"
elif (variable == 'FSC'): 
    # FSCF
    cmap = 'gist_stern'
    vmin = 0
    vmax = 1
    thick_interval = 0.1
    product = "SNOWCO"
elif (variable == 'LST'):
    # LSTF
    cmap = 'jet'
    vmin = 230
    vmax = 320
    thick_interval = 10
    product = "LSTSKN"
elif (variable == 'RRQPE'):
    # RRQPE
    cmap = 'jet'
    vmin = 0
    vmax = 60
    thick_interval = 5
    data[data == 0] = np.nan
    product = "RRQPEF"
elif (variable == 'SST'):
    # SSTF
    cmap = 'jet'
    vmin = 268
    vmax = 308
    thick_interval = 5
    # Read the DQF data
    data_DQF = file.variables['DQF'][::f ,::f]
    data[data_DQF != 0] = np.nan
    product = "SSTSKN"
elif (variable == 'TPW'):
    # TPW
    colors = ["#bc8462", "#ae656f", "#a44a79", "#962e97", "#6158c5", "#2b8ffb", "#5fcdff", "#94fff0", "#a5ff94", "#fff88c", "#ffbf52", "#ec7b27", "#b84827", "#a1333d", "#bd5478", "#cc6a99", "#d982b8"]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    vmin = 0
    vmax = 80
    thick_interval = 5
    product = "TOTPWA"
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
"vmin": vmin, "vmax": vmax, "cmap": cmap,
"title_text": "GOES-16 " + prod_name, "title_size": int(data.shape[1] * 0.005), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[0] - int(data.shape[0] * 0.016), 
"thick_interval": thick_interval, "cbar_labelsize": int(data.shape[0] * 0.005), "cbar_labelpad": -int(data.shape[0] * 0.0085),
"file_name_id_1": "G16",  "file_name_id_2": product 
}
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
fig = plt.figure(figsize=(data.shape[1]/float(plot_config["dpi"]), data.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])
 
# Define the projection
proj = ccrs.Geostationary(central_longitude=longitude, satellite_height=h)
#img_extent = (x1,x2,y1,y2)
img_extent = (x.min(), x.max(), y.min(), y.max())

# Use the Geostationary projection in cartopy
ax = plt.axes([0, 0, 1, 1], projection=proj)

# Add a background image
#ax.stock_img()
fname = os.path.join('..//Maps//', 'land_ocean_ice_8192.jpg')
ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)
date = datetime(int(year), int(month), int(day), int(hour))
#ax.add_feature(Nightshade(date, alpha=0.7), zorder=2)

# Plot the image
img = ax.imshow(data, vmin=plot_config["vmin"], vmax=plot_config["vmax"], origin='upper', extent=img_extent, cmap=plot_config["cmap"], zorder=3)

# To put colorbar inside picture
axins1 = inset_axes(ax, width="100%", height="1%", loc='lower center', borderpad=0.0)
  
# Add states and provinces
shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=4)

# Add countries
shapefile = list(shpreader.Reader('..//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=5)

# Add continents
shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_coastline.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=6)
  
# Add coastlines, borders and gridlines
ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=False, zorder=7)

# Remove the outline border
ax.outline_patch.set_visible(False)
  
# Add a title
plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=8)

# Add a colorbar
ticks = np.arange(plot_config["vmin"], plot_config["vmax"], plot_config["thick_interval"]).tolist()     
ticks = plot_config["thick_interval"] * np.round(np.true_divide(ticks,plot_config["thick_interval"]))
ticks = ticks[1:]
cb = fig.colorbar(img, cax=axins1, orientation="horizontal", ticks=ticks)
cb.outline.set_visible(False)
cb.ax.tick_params(width = 0)
cb.ax.xaxis.set_tick_params(pad=plot_config["cbar_labelpad"])
cb.ax.tick_params(axis='x', colors='black', labelsize=plot_config["cbar_labelsize"])

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
