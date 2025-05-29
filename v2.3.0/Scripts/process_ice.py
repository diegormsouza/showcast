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
import re                                                    # Regular expression operations
import numpy as np                                           # Scientific computing with Python
import os                                                    # Miscellaneous operating system interfaces
from os.path import dirname, abspath                         # Return a normalized absolutized version of the pathname path 
import glob                                                  # Unix style pathname pattern expansion
import matplotlib.colors                                     # Matplotlib colors
import cartopy, cartopy.crs as ccrs                          # Plot maps
import cartopy.io.shapereader as shpreader                   # Import shapefiles
import matplotlib.pyplot as plt                              # Plotting library
import sys                                                   # Import the "system specific parameters and functions" module
import time as t                                             # Time access and conversion
import gzip, shutil                                          # Support for gzip files
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
from netCDF4 import Dataset                                  # Read / Write NetCDF4 files
from osgeo import gdal, osr, ogr                             # Import GDAL
from shutil import move                                      # High-level file operations
from matplotlib.image import imread                          # Read an image from a file into an array
from cartopy.feature.nightshade import Nightshade            # Draws a polygon where there is no sunlight for the given datetime.
from html_update import update                               # Update the HTML animation 
from mpl_toolkits.axes_grid1.inset_locator import inset_axes # Add a child inset axes to this existing axes.
# Ignore possible warnings
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

def procIce(product, time, lat_file, lon_file, var_file, nodata):
   # Create the storage variable 
   storage = product + "_STR"
   
   # Create the satellite output directory if it doesn't exist
   out_dir = main_dir + '//Output//' + satellite
   if not os.path.exists(out_dir):
       os.mkdir(out_dir)

   # Create the product output directory if it doesn't exist
   out_dir = main_dir + '//Output//' + satellite + '//' + storage + '//'
   if not os.path.exists(out_dir):
       os.mkdir(out_dir)
       
   # Read environment dataset
   connectionInfo = 'NETCDF:\"' + path + '\":' + variable_env
   print(connectionInfo)
   gdal.Translate(out_dir + product + '_' + time + '_image.vrt', connectionInfo, format='VRT')
   
   # Read latitude dataset
   connectionInfo = 'NETCDF:\"' + path + '\":' + variable_lat
   #print(connectionInfo)
   gdal.Translate(out_dir + product + '_' + time + '_lat.vrt', connectionInfo, format='VRT')

   # Read longitude dataset
   connectionInfo = 'NETCDF:\"' + path + '\":' + variable_lon
   #print(connectionInfo)
   gdal.Translate(out_dir + product + '_' + time + '_lon.vrt', connectionInfo, format='VRT')

   # Make the necessary change to the VRT file (the same for any GCOM product)
   readFile = open(out_dir + product + '_' + time + '_image.vrt')
   lines = readFile.readlines()
   readFile.close()
   w = open(out_dir + product + '_' + time + '_image.vrt','w')
   w.writelines([item for item in lines[:-1]])
   w.write("<Metadata domain=\"GEOLOCATION\">" + '\n')
   w.write("<MDI key=\"X_DATASET\">" + out_dir + product + '_' + time + '_lon.vrt' + "</MDI>" + '\n')
   w.write("<MDI key=\"X_BAND\">1</MDI>" + '\n')
   w.write("<MDI key=\"Y_DATASET\">" + out_dir + product + '_' + time + '_lat.vrt' + "</MDI>" + '\n')
   w.write("<MDI key=\"Y_BAND\">1</MDI>" + '\n')
   w.write("<MDI key=\"PIXEL_OFFSET\">0</MDI>" + '\n')
   w.write("<MDI key=\"LINE_OFFSET\">0</MDI>" + '\n')
   w.write("<MDI key=\"PIXEL_STEP\">1</MDI>" + '\n')
   w.write("<MDI key=\"LINE_STEP\">1</MDI>" + '\n')
   w.write("</Metadata>" + '\n')
   w.write("</VRTDataset>" + '\n')
   w.close()

   # Create the GeoTIFF
   grid = gdal.Warp(out_dir + product + '_' + time + '.tif', out_dir + product + '_' + time + '_image.vrt', format='GTiff', outputBounds=extent, geoloc=True, srcNodata=nodata)
   print('Generated GeoTIFF: ', product + '_' + time + '.tif')
   grid = None

   # Delete the unnecessary files
   os.remove(out_dir + product + '_' + time + '_image.vrt')
   os.remove(out_dir + product + '_' + time + '_lat.vrt')
   os.remove(out_dir + product + '_' + time + '_lon.vrt')
   
   # Check if there is valid pixels in the region of interest
   geotiff = gdal.Open(out_dir + product + '_' + time + '.tif')
   band = geotiff.GetRasterBand(1)
   data = band.ReadAsArray()
   data = data.astype(float)
   
   #print(data)
   
   if (product == "SSSICN") or (product == "SSSICS") or (product == "AMSICN") or (product == "AMSICS") or (product == "AMSIEN") or (product == "AMSIES"):
       data[data == min(data[0])] = np.nan
       data[data == -999] = np.nan
       data[data == 0] = np.nan
       data[data == 0] = np.nan
       data[data == -1.00e+10] = np.nan
   if (product == "SICETN") or (product == "SICETS") or (product == "SICEEN") or (product == "SICEES"):
       data[data == max(data[0])] = np.nan
       #data[data == 1] = np.nan
       
   geotiff = None
          
   if (hemisphere == "NH"):
      #------------------------------------------------------------------------------------------------------
      #------------------------------------------------------------------------------------------------------
      # Plot configuration
      plot_config = {
      "resolution": resolution, 
      "dpi": 150, 
      "states_color": 'lightgray', "states_width": 2712 * 0.00018, 
      "countries_color": 'black', "countries_width": 2712 * 0.00012,
      "continents_color": 'black', "continents_width": 2712 * 0.00025,
      "grid_color": 'white', "grid_width": 2712 * 0.00025, "grid_interval": 10.0,
      "vmin": vmin, "vmax": vmax, "cmap": cmap,
      "title_text": sat_title + " " + prod_title + " ", "title_size": int(2712 * 0.005), "title_x_offset": int(2712 * 0.01), "title_y_offset": 2712 - int(2712 * 0.016), 
      "thick_interval": thick_interval, "cbar_labelsize": int(2712 * 0.005), "cbar_labelpad": -int(2712 * 0.0),
      "file_name_id_1": satellite,  "file_name_id_2": product + "_SEC"
      }
      #------------------------------------------------------------------------------------------------------
      #------------------------------------------------------------------------------------------------------
      # Choose the plot size (width x height, in inches)
      fig = plt.figure(figsize=(2712/float(plot_config["dpi"]), 2712/float(plot_config["dpi"])), dpi=plot_config["dpi"])
      # Define the projection
      proj = ccrs.Orthographic(0, 90)
      # Use the PlateCarree projection in cartopy
      ax = plt.axes([0, 0, 1, 1], projection=proj)
      #ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())
      # Define the image extent
      img_extent = [extent[0], extent[2], extent[1], extent[3]]
      # Add a background image
      ax.stock_img()
      #fname = os.path.join(main_dir + '//Maps//', 'land_ocean_ice_8192.jpg')
      #ax.imshow(imread(fname), origin='upper', transform=proj, zorder=1)
      #date = datetime(int(year), int(month), int(day), int(hour))
      #ax.add_feature(Nightshade(date, alpha=0.7), zorder=2)
      img = ax.imshow(data, vmin=plot_config["vmin"], vmax=plot_config["vmax"], transform=ccrs.PlateCarree(), extent=img_extent, origin='upper', cmap=plot_config["cmap"], zorder=3)
   elif (hemisphere == "SH"):
      #------------------------------------------------------------------------------------------------------
      #------------------------------------------------------------------------------------------------------
      # Plot configuration
      plot_config = {
      "resolution": resolution, 
      "dpi": 150, 
      "states_color": 'lightgray', "states_width": 2712 * 0.00018, 
      "countries_color": 'black', "countries_width": 2712 * 0.00012,
      "continents_color": 'black', "continents_width": 2712 * 0.00025,
      "grid_color": 'white', "grid_width": 2712 * 0.00025, "grid_interval": 10.0,
      "vmin": vmin, "vmax": vmax, "cmap": cmap,
      "title_text": sat_title + " " + prod_title + " ", "title_size": int(2712 * 0.005), "title_x_offset": int(2712 * 0.01), "title_y_offset": 2712 - int(2712 * 0.016), 
      "thick_interval": thick_interval, "cbar_labelsize": int(2712 * 0.005), "cbar_labelpad": -int(2712 * 0.0),
      "file_name_id_1": satellite,  "file_name_id_2": product + "_SEC" 
      }
      #------------------------------------------------------------------------------------------------------
      #------------------------------------------------------------------------------------------------------
      # Choose the plot size (width x height, in inches)
      fig = plt.figure(figsize=(2712/float(plot_config["dpi"]), 2712/float(plot_config["dpi"])), dpi=plot_config["dpi"])
      # Define the projection
      proj = ccrs.Orthographic(180, -90)
      # Use the PlateCarree projection in cartopy
      ax = plt.axes([0, 0, 1, 1], projection=proj)
      #ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())
      # Define the image extent
      img_extent = [extent[0], extent[2], extent[1], extent[3]]       
      # Add a background image
      ax.stock_img()
      #fname = os.path.join(main_dir + '//Maps//', 'land_ocean_ice_8192.jpg')
      #ax.imshow(imread(fname), origin='upper', transform=proj, zorder=1)
      #date = datetime(int(year), int(month), int(day), int(hour))
      #ax.add_feature(Nightshade(date, alpha=0.7), zorder=2)
      img = ax.imshow(data, vmin=plot_config["vmin"], vmax=plot_config["vmax"], transform=ccrs.PlateCarree(), extent=img_extent, origin='upper', cmap=plot_config["cmap"], zorder=3)   

   # To put colorbar inside picture
   axins1 = inset_axes(ax, width="100%", height="1%", loc='lower center', borderpad=0.0)
  
   # Add states and provinces
   shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
   ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=4)

   # Add countries
   shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
   ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=5)

   # Add continents
   shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_coastline.shp').geometries())
   ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=6)
  
   # Add coastlines, borders and gridlines
   ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=False, zorder=7)

   # Remove the outline border
   ax.outline_patch.set_visible(False)
  
   # Add a title
   plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=8)

   # Add logos / images to the plot
   my_logo = plt.imread(main_dir + '//Logos//my_logo.png')
   newax = fig.add_axes([0.01, 0.03, 0.10, 0.10], anchor='SW', zorder=12) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
   newax.imshow(my_logo)
   newax.axis('off')

   # Add a colorbar
   ticks = np.arange(plot_config["vmin"], plot_config["vmax"], plot_config["thick_interval"]).tolist()     
   ticks = plot_config["thick_interval"] * np.round(np.true_divide(ticks,plot_config["thick_interval"]))
   ticks = ticks[1:]
   cb = fig.colorbar(img, cax=axins1, orientation="horizontal", ticks=ticks)
   cb.outline.set_visible(False)
   cb.ax.tick_params(width = 0)
   cb.ax.xaxis.set_tick_params(pad=plot_config["cbar_labelpad"])
   cb.ax.xaxis.set_ticks_position('top')
   cb.ax.tick_params(axis='x', colors='lightgray', labelsize=plot_config["cbar_labelsize"])

   #plt.show()
    
   #---------------------------------------------------------------------------------------------
   #---------------------------------------------------------------------------------------------   
       
   product = product + "_SEC"
          
   # Create the satellite output directory if it doesn't exist
   out_dir = main_dir + '//Output//' + satellite
   if not os.path.exists(out_dir):
      os.mkdir(out_dir)

   # Create the product output directory if it doesn't exist
   out_dir = main_dir + '//Output//' + satellite + '//' + product + '//'
   if not os.path.exists(out_dir):
      os.mkdir(out_dir)
        
   # Save the image
   plt.savefig(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.png', facecolor='black')#, bbox_inches='tight', pad_inches=0, facecolor='black')

   # Update the animation
   nfiles = 20
   update(satellite, product, nfiles)
       
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 

###############################################################################
# Reading the Data
###############################################################################

# Start the time counter
print('Script started.')
start_time = t.time()  

# SHOWCast directory:
main_dir = dirname(dirname(abspath(__file__)))
    
# Path to the ice file
path = sys.argv[1]
path_original = path

path2 = re.sub('S-OSI*(.*)', '', path)
#print(path2)
path3 = path.replace(path2,'')
path3 = path3.replace('.gz','')
#print(path3)

with gzip.open(path, 'r') as f_in, open(path2+path3, 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)
    path = path2+path3
		
'''
import gzip
# Unzipp the ice file
with gzip.open(path) as gz:
    with Dataset(path3, mode='r', memory=gz.read()) as nc:
        print(nc.variables)
'''

# Choose the visualization extent (min lon, min lat, max lon, max lat)
extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]

# Define KM_PER_DEGREE
KM_PER_DEGREE = 111.32

# Calculate the total number of degrees in lat and lon
deg_lon = extent[2] - extent[0]
deg_lat = extent[3] - extent[1]

# Calculate the number of pixels
resolution = int(sys.argv[6])
width = (KM_PER_DEGREE * deg_lon) /  resolution
height = (KM_PER_DEGREE * deg_lat) /  resolution

# Get the aquisition time
time = path[-16:]
time = time[:12]
#print(time)

date_formated = time[0:4] + "-" + time[4:6] + "-" + time[6:8] + " " + time[8:10] + ":" + time[10:12] + " UTC"
#print(date_formated)
date_file = time

# Get the product type:
# Have to unzip: "\\data\OSI\OSI_HL_data\output\ice\ssmi\product\"
if "S-OSI_-DMI_-MULT-GL_NH_CONCn" in path:
    variable_lat = 'lat'
    variable_lon = 'lon'
    variable_env = 'ice_conc'
    product = 'SSSICN'
    nodata = -999
    cmap = 'jet'
    vmin = 1
    vmax = 10000
    thick_interval = 1000
    satellite = "DMS"
    sat_title = "DMPS"
    hemisphere = "NH"
    prod_title = "Sea Ice Concentration (Northern Hemisphere)"
    procIce(product, time, variable_lat, variable_lon, variable_env, nodata)
    os.remove(path2+path3) 
# Have to unzip: "\\data\OSI\OSI_HL_data\output\ice\ssmi\product\"
elif "S-OSI_-DMI_-MULT-GL_SH_CONCn" in path:
    variable_lat = 'lat'
    variable_lon = 'lon'
    variable_env = 'ice_conc'
    product = 'SSSICS'
    nodata = -999
    cmap = 'jet'
    vmin = 1
    vmax = 10000
    thick_interval = 1000
    satellite = "DMS"
    sat_title = "DMPS"
    hemisphere = "SH"
    prod_title = "Sea Ice Concentration (Southern Hemisphere)"
    procIce(product, time, variable_lat, variable_lon, variable_env, nodata)
    os.remove(path2+path3)
# Have to unzip: "\\data\OSI\OSI_HL_data\output\ice\ssmi\product\"
if "S-OSI_-DMI_-AMSR-GL_NH_CONC" in path:
    variable_lat = 'lat'
    variable_lon = 'lon'
    variable_env = 'ice_conc'
    product = 'AMSICN'
    nodata = -999
    cmap = 'jet'
    vmin = 1
    vmax = 10000
    thick_interval = 1000
    satellite = "DMS"
    sat_title = "DMPS"
    hemisphere = "NH"
    prod_title = "Sea Ice Concentration (Northern Hemisphere)"
    procIce(product, time, variable_lat, variable_lon, variable_env, nodata)
    os.remove(path2+path3) 
# Have to unzip: "\\data\OSI\OSI_HL_data\output\ice\ssmi\product\"
elif "S-OSI_-DMI_-AMSR-GL_SH_CONC" in path:
    variable_lat = 'lat'
    variable_lon = 'lon'
    variable_env = 'ice_conc'
    product = 'AMSICS'
    nodata = -999
    cmap = 'jet'
    vmin = 1
    vmax = 10000
    thick_interval = 1000
    satellite = "DMS"
    sat_title = "DMPS"
    hemisphere = "SH"
    prod_title = "Sea Ice Concentration (Southern Hemisphere)"
    procIce(product, time, variable_lat, variable_lon, variable_env, nodata)
    os.remove(path2+path3)
# Simple Unzip
elif "S-OSI_-NOR_-MULT-GL_NH_TYPEn" in path:
    variable_lat = 'lat'
    variable_lon = 'lon'
    variable_env = 'ice_type'
    product = 'SICETN'
    nodata = 255
    colors = ["#383881", "#2b9565", "#9ccc66", "#ffffff", "#f91111", "#000000"]
    cmap = matplotlib.colors.ListedColormap(colors)
    vmin = 1
    vmax = 6
    thick_interval = 1
    satellite = "MUL"
    sat_title = "MULTIMISSION"
    hemisphere = "NH"
    prod_title = "Sea Ice Type (Northern Hemisphere)"
    procIce(product, time, variable_lat, variable_lon, variable_env, nodata)
    os.remove(path2+path3)
# Simple Unzip
elif "S-OSI_-NOR_-MULT-GL_SH_TYPEn" in path:
    variable_lat = 'lat'
    variable_lon = 'lon'
    variable_env = 'ice_type'
    product = 'SICETS'
    nodata = 255
    colors = ["#383881", "#2b9565", "#9ccc66", "#ffffff", "#f91111", "#000000"]
    cmap = matplotlib.colors.ListedColormap(colors)
    vmin = 1
    vmax = 6
    thick_interval = 1
    satellite = "MUL"
    sat_title = "MULTIMISSION"
    hemisphere = "SH"
    prod_title = "Sea Ice Type (Southern Hemisphere)"
    procIce(product, time, variable_lat, variable_lon, variable_env, nodata)
    os.remove(path2+path3)
# Simple Unzip
elif "S-OSI_-NOR_-MULT-GL_NH_EDGEn" in path:
    variable_lat = 'lat'
    variable_lon = 'lon'
    variable_env = 'ice_edge'
    product = 'SICEEN'
    nodata = 255
    colors = ["#383881", "#7dabcf", "#ffffff", "#ffffff", "#ffffff", "#000000"]
    cmap = matplotlib.colors.ListedColormap(colors)
    vmin = 1
    vmax = 6
    thick_interval = 1
    satellite = "MUL"
    sat_title = "MULTIMISSION"
    hemisphere = "NH"
    prod_title = "Sea Ice Edge (Northern Hemisphere)"
    procIce(product, time, variable_lat, variable_lon, variable_env, nodata)
    os.remove(path2+path3)
# Simple Unzip
elif "S-OSI_-NOR_-MULT-GL_SH_EDGEn" in path:
    variable_lat = 'lat'
    variable_lon = 'lon'
    variable_env = 'ice_edge'
    product = 'SICEES'
    nodata = 255
    colors = ["#383881", "#7dabcf", "#ffffff", "#ffffff", "#ffffff", "#000000"]
    cmap = matplotlib.colors.ListedColormap(colors)
    vmin = 1
    vmax = 6
    thick_interval = 1
    satellite = "MUL"
    sat_title = "MULTIMISSION"
    hemisphere = "SH"
    prod_title = "Sea Ice Edge (Southern Hemisphere)"
    procIce(product, time, variable_lat, variable_lon, variable_env, nodata)
    os.remove(path2+path3)
# Have to unzip: "\\data\OSI\OSI_HL_data\output\ice\emissivity\data\"
elif "S-OSI_-DMI_-DMSP-GL_NH_EMIS" in path: 
    variable_lat = 'lat'
    variable_lon = 'lon'
    variable_env = 'e'
    product = 'AMSIEN'
    nodata = -999
    cmap = 'jet'
    vmin = 0.5
    vmax = 0.9
    thick_interval = 0.05
    satellite = "DMS"
    sat_title = "DMSP"
    hemisphere = "NH"
    prod_title = "Sea Ice Emissivity (Northern Hemisphere)"
    procIce(product, time, variable_lat, variable_lon, variable_env, nodata)
    #variable_lat = 'lat'
    #variable_lon = 'lon'
    #variable_env = 'ev'
    #product = 'DMS_SSSIEN'
    #nodata = -999
    #procIce(product, time, variable_lat, variable_lon, variable_env, nodata)
    #os.remove(path2+path3)
# Have to unzip: "\\data\OSI\OSI_HL_data\output\ice\emissivity\data\"
elif "S-OSI_-DMI_-DMSP-GL_SH_EMIS" in path: 
    variable_lat = 'lat'
    variable_lon = 'lon'
    variable_env = 'e'
    product = 'AMSIES'
    nodata = -999
    cmap = 'jet'
    vmin = 0.5
    vmax = 0.9
    thick_interval = 0.05
    satellite = "DMS"
    sat_title = "DMSP"
    hemisphere = "SH"
    prod_title = "Sea Ice Emissivity (Southern Hemisphere)"
    procIce(product, time, variable_lat, variable_lon, variable_env, nodata) 
    #variable_lat = 'lat'
    #variable_lon = 'lon'
    #variable_env = 'ev'
    #product = 'DMS_SSSIES'
    #nodata = -999
    #procIce(product, time, variable_lat, variable_lon, variable_env, nodata) 
    #os.remove(path2+path3)
elif "S-OSI_-NOR_-MULT-NH_LRSIDRIFT" in path:
    print("Still have to add.")  
elif "S-OSI_-NOR_-MULT-SH_LRSIDRIFT" in path: 
    print("Still have to add.")
elif "S-OSI_-DMI_-MTOP-NH_MRSIDRIFT" in path: 
    print("Still have to add.")
elif "S-OSI_-DMI_-MTOP-SH_MRSIDRIFT" in path: 
    print("Still have to add.")  

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Put the processed file on the log
import datetime # Basic Date and Time types
with open(main_dir + '//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
 log.write(str(datetime.datetime.now()))
 log.write('\n')
 log.write(path_original + '\n')
 log.write('\n')
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

print('Total processing time:', round((t.time() - start_time),2), 'seconds.') 