# Python Script Example: New Script Pack
#---------------------------------------------------------------------------------------------
# Required modules
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
from html_update import update                               # Update the HTML animation 
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()  

# Image path
path = (sys.argv[1])
#path = ("..//Samples//OR_ABI-L2-CMIPF-M6C13_G16_s20192931650344_e20192931700064_c20192931700142.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CMIPF-M6C02_G16_s20192931650344_e20192931700052_c20192931700142-132002_0.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CMIPF-M6C07_G16_s20192931650344_e20192931700063_c20192931700143.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CMIPF-M6C08_G16_s20192931650344_e20192931700052_c20192931700144.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CMIPF-M6C09_G16_s20192931650344_e20192931700058_c20192931700143.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CMIPF-M6C13_G16_s20192931650344_e20192931700064_c20192931700142.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CMIPF-M6C14_G16_s20192931650344_e20192931700052_c20192931700153.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CMIPF-M6C15_G16_s20192931650344_e20192931700058_c20192931700156.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CMIPF-M6C02_G17_s20192931650341_e20192931659407_c20192931659460-132004_0.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CMIPF-M6C07_G17_s20192931650341_e20192931659419_c20192931659467-132008_0.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CMIPF-M6C08_G17_s20192931650341_e20192931659407_c20192931659473-132012_0.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CMIPF-M6C09_G17_s20192931650341_e20192931659413_c20192931659477-132016_0.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CMIPF-M6C13_G17_s20192931650341_e20192931659418_c20192931659465-132020_0.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CMIPF-M6C14_G17_s20192931650341_e20192931659407_c20192931659469-132024_0.nc")
#file = Dataset("..//Samples//OR_ABI-L2-CMIPF-M6C15_G17_s20192931650341_e20192931659413_c20192931659466-132028_0.nc")

# Read the image
file = Dataset(path)

# Read the satellite 
satellite = getattr(file, 'platform_ID')

# Read the band number
band = str(file.variables['band_id'][0]).zfill(2)

# Product naming
product = "BAND" + band

# Desired resolution
resolution = int(sys.argv[6])

# Read the resolution
band_resolution_km = getattr(file, 'spatial_resolution')
band_resolution_km = float(band_resolution_km[:band_resolution_km.find("km")])

# Division factor to reduce image size
f = math.ceil(float(resolution / band_resolution_km))

# Read the central longitude
longitude = file.variables['goes_imager_projection'].longitude_of_projection_origin

# Calculate the image extent 
H = file.variables['goes_imager_projection'].perspective_point_height
x1 = file.variables['x_image_bounds'][0] * H 
x2 = file.variables['x_image_bounds'][1] * H 
y1 = file.variables['y_image_bounds'][1] * H 
y2 = file.variables['y_image_bounds'][0] * H 

# Getting the file time and date
add_seconds = int(file.variables['time_bounds'][0])
date = datetime(2000,1,1,12) + timedelta(seconds=add_seconds)
date_formated = date.strftime('%Y-%m-%d %H:%M UTC')
date_file = date.strftime('%Y%m%d%H%M')
year = date.strftime('%Y')
month = date.strftime('%m')
day = date.strftime('%d')
hour = date.strftime('%H')
minutes = date.strftime('%M')

# Get the pixel values
data = file.variables['CMI'][:,:][::f ,::f ]
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

if int(band) <= 6:
    # Converts a CPT file to be used in Python
    cpt = loadCPT('..//Colortables//Square Root Visible Enhancement.cpt')
    cmap = LinearSegmentedColormap('cpt', cpt)
    vmin = 0.0
    vmax = 1.0
    thick_interval = 0.1
elif int(band) == 7:
    # Converts a CPT file to be used in Python
    cpt = loadCPT('..//Colortables//SVGAIR2_TEMP.cpt')
    cmap = LinearSegmentedColormap('cpt', cpt) 
    data -= 273.15
    vmin = -112.15
    vmax = 56.85
    thick_interval = 10.0
elif int(band) > 7 and int(band) < 11:
    # Converts a CPT file to be used in Python
    cpt = loadCPT('..//Colortables//SVGAWVX_TEMP.cpt')
    cmap = LinearSegmentedColormap('cpt', cpt) 
    data -= 273.15
    vmin = -112.15
    vmax = 56.85
    thick_interval = 10.0
elif int(band) > 10 and int(band) < 14:
    # Converts a CPT file to be used in Python
    cpt = loadCPT('..//Colortables//IR4AVHRR6.cpt')   
    cmap = LinearSegmentedColormap('cpt', cpt) 
    data -= 273.15    
    vmin = -103.0
    vmax = 84.0
    thick_interval = 10.0
elif int(band) > 13:
    # Converts a CPT file to be used in Python
    cmap = 'Greys'
    data -= 273.15    
    vmin = -80.0
    vmax = 40.0
    thick_interval = 10.0

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------    
# Plot configuration
plot_config = {
"resolution": band_resolution_km, 
"dpi": 150, 
"states_color": 'white', "states_width": data.shape[0] * 0.00006, 
"countries_color": 'turquoise', "countries_width": data.shape[0] * 0.00012,
"continents_color": 'cyan', "continents_width": data.shape[0] * 0.00025,
"grid_color": 'white', "grid_width": data.shape[0] * 0.00025, "grid_interval": 10.0,
"vmin": vmin, "vmax": vmax, "cmap": cmap,
"title_text": "GOES-" + satellite[1:3] + " Band " + band, "title_size": int(data.shape[1] * 0.005), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[1] - int(data.shape[1] * 0.016), 
"thick_interval": thick_interval, "cbar_labelsize": int(data.shape[0] * 0.005), "cbar_labelpad": -int(data.shape[0] * 0.0085),
"file_name_id_1": satellite,  "file_name_id_2": product
}
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
fig = plt.figure(figsize=(data.shape[1]/float(plot_config["dpi"]), data.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])
  
# Define the projection
proj = ccrs.Geostationary(central_longitude=longitude, satellite_height=H)
img_extent = (x1,x2,y1,y2)

# Use the Geostationary projection in cartopy
ax = plt.axes([0, 0, 1, 1], projection=proj)

# Plot the image
img = ax.imshow(data, vmin=plot_config["vmin"], vmax=plot_config["vmax"], origin='upper', extent=img_extent, cmap=plot_config["cmap"], zorder=1)

# To put colorbar inside picture
axins1 = inset_axes(ax, width="100%", height="1%", loc='lower center', borderpad=0.0)
  
# Add states and provinces
shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=2)

# Add countries
shapefile = list(shpreader.Reader('..//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=3)

# Add continents
shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_coastline.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=4)
  
# Add coastlines, borders and gridlines
ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=False, zorder=5)

# Remove the outline border
ax.outline_patch.set_visible(False)
  
# Add a title
plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=6)

# Add a colorbar
ticks = np.arange(plot_config["vmin"], plot_config["vmax"], plot_config["thick_interval"]).tolist()     
ticks = plot_config["thick_interval"] * np.round(np.true_divide(ticks,plot_config["thick_interval"]))
ticks = ticks[1:-1]
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