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
matplotlib.use('Agg')
#--------------------------------
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
# Start the time counter
print('Script started.')
start_time = t.time()  

# SHOWCast directory:
main_dir = dirname(dirname(abspath(__file__)))

def procGcom(product, start, lat_file, lon_file, var_file, width, height):

   # Create the satellite output directory if it doesn't exist
   out_dir = main_dir + '//Output//' + satellite
   if not os.path.exists(out_dir):
       os.mkdir(out_dir)

   # Create the product output directory if it doesn't exist
   out_dir = main_dir + '//Output//' + satellite + '//' + storage + '//'
   if not os.path.exists(out_dir):
       os.mkdir(out_dir)
          
   # Read environment dataset
   connectionInfo = 'HDF5:\"' + path + '\"://' + variable_env
   print(connectionInfo)
   gdal.Translate(main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '_image.vrt', connectionInfo, format='VRT')
 
   # Read latitude dataset
   connectionInfo = 'HDF5:\"' + path + '\"://' + variable_lat
   #print(connectionInfo)
   gdal.Translate(main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '_lat.vrt', connectionInfo, format='VRT')

   # Read longitude dataset
   connectionInfo = 'HDF5:\"' + path + '\"://' + variable_lon
   #print(connectionInfo)
   gdal.Translate(main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '_lon.vrt', connectionInfo, format='VRT')

   # Make the necessary change to the VRT file (the same for any GCOM product)
   readFile = open( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '_image.vrt')
   lines = readFile.readlines()
   readFile.close()
   w = open( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '_image.vrt','w')
   w.writelines([item for item in lines[:-1]])
   w.write("<Metadata domain=\"GEOLOCATION\">" + '\n')
   w.write("<MDI key=\"X_DATASET\">" +  main_dir + '//Output//' + satellite + '//' + storage  + '//' + 'GCM_' + product + '_' + start + '_lon.vrt' + "</MDI>" + '\n')
   w.write("<MDI key=\"X_BAND\">1</MDI>" + '\n')
   w.write("<MDI key=\"Y_DATASET\">" +  main_dir + '//Output//' + satellite + '//' + storage  + '//' + 'GCM_' + product + '_' + start + '_lat.vrt' + "</MDI>" + '\n')
   w.write("<MDI key=\"Y_BAND\">1</MDI>" + '\n')
   w.write("<MDI key=\"PIXEL_OFFSET\">0</MDI>" + '\n')
   w.write("<MDI key=\"LINE_OFFSET\">0</MDI>" + '\n')
   w.write("<MDI key=\"PIXEL_STEP\">1</MDI>" + '\n')
   w.write("<MDI key=\"LINE_STEP\">1</MDI>" + '\n')
   w.write("</Metadata>" + '\n')
   w.write("</VRTDataset>" + '\n')
   w.close()

   # Create the GeoTIFF
   grid = gdal.Warp( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.tif',  main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '_image.vrt', format = 'GTiff', outputType = gdal.GDT_Float32, outputBounds = extent, geoloc = True, srcNodata=-9999, width = width, height = height)
   print('Generated GeoTIFF: ','GCM_' + product + '_' + start + '.tif')
   #grid = gdal.Warp('GCM_' + product + '_' + start + '.tif', 'GCM_' + product + '_' + start + '_image.vrt', format='GTiff', outputBounds=extent, geoloc=True, srcNodata=-9999, xRes = 0.0, yRes = 0.0)
   #grid = gdal.Warp('GCM_' + product + '_' + start + '.tif', 'GCM_' + product + '_' + start + '_image.vrt', format='GTiff', srcSRS='EPSG:4326', dstSRS='EPSG:4326', geoloc=True, srcNodata=-999)
   grid = None

   # Delete the unnecessary files
   os.remove( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '_image.vrt')
   os.remove( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '_lat.vrt')
   os.remove( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '_lon.vrt')
   
   #print("Opening GeoTIFF:")
   # Read the created GeoTIFF to check if it has valid pixels
   geotiff = gdal.Open( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.tif')
   #number_of_bands = geotiff.RasterCount
   #print(number_of_bands)
   # Read the band as a Python array
   band = geotiff.GetRasterBand(1)  
   
   data = band.ReadAsArray()
   geotiff = None 
   
   if (product != "SEAICN" and product != "SEAICS"): 
       global orbit
       #print (orbit)
       if (orbit == "A"):
            orbit_title = "(Ascending Pass)"
       elif (orbit == "D"):
            orbit_title = "(Descending Pass)"
       elif (orbit == "E"):
            orbit_title = "(Unknown Pass)"
            
       if orbit == "None":
           try:
               #print("FIRST TRY. CHECK IF VALID DATA ON MIDDLE LINE") 
               a = int(int(data.shape[0])/2)
               factor = int(int(data.shape[0])/5)       
               x1 = np.argwhere(data[a,:] != -9999)[0]
               x2 = np.argwhere(data[a+factor,:] != -9999)[0]
	           #print(x1)
               #print(x2)
               result = x1 - x2
               #print(result)
   
               if result > 0:
                   #print("DESCENDING PASS")
                   orbit_title = "(Descending Pass)"
                   orbit = "D"	
                   move( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.tif',  main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + 'D_' + start + '.tif')
                   orbit = "D"                   
                   product = product + orbit   
               elif result < 0:
                   #print("ASCENDING PASS")
                   orbit_title = "(Ascending Pass)"
                   orbit = "A"		   
                   move( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.tif',  main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + 'A_' + start + '.tif')
                   orbit = "A"
                   product = product + orbit
               elif result == 0: # Pass under a cut (equal for both lines)
                   #print("PASS UNDER CUT. CHANGING THE REFERENCE")
                   a = int(int(data.shape[0])/2)
                   factor = int(int(data.shape[0])/5)       
                   x1 = np.argwhere(data[a,:] != -9999)[-1]
                   x2 = np.argwhere(data[a+factor,:] != -9999)[-1]
                   #print(x1)
                   #print(x2)
                   result = x1 - x2
                   #print(result)
   
                   if result > 0:
                       #print("DESCENDING PASS") 
                       orbit_title = "(Descending Pass)"
                       orbit = "D"			   
                       move( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.tif',  main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + 'D_' + start + '.tif')
                       orbit = "D"                       
                       product = product + orbit
                   elif result < 0:
                       #print("ASCENDING PASS") 
                       orbit_title = "(Ascending Pass)"
                       orbit = "A"
                       move( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.tif',  main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + 'A_' + start + '.tif')
                       orbit = "A"                       
                       product = product + orbit
                   elif result == 0:
                       #print("GIVE UP!") 
                       orbit_title = "(Unknown)"
                       move( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.tif',  main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + 'E_' + start + '.tif')
                       orbit = "E"                       
                       product = product + orbit
           except: # No valid data on the middle line. Let's get the 1/4 line (the first line produces error dor the Ocean Products!
               #print ("ERRO!")
               #print("NO VALID DATA ON THE MIDDLE LINE. TRYING 1/4")
               a = int(int(data.shape[0])/4)
               factor = int(int(data.shape[0])/5)       
               x1 = np.argwhere(data[a,:] != -9999)[0]
               x2 = np.argwhere(data[a+factor,:] != -9999)[0]
	           #print(x1)
               #print(x2)
               result = x1 - x2
               #print(result)
   
               if result > 0:
                   #print("DESCENDING PASS")
                   orbit_title = "(Descending Pass)"
                   orbit = "D"		   
                   move( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.tif',  main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + 'D_' + start + '.tif')
                   orbit = "D"                   
                   product = product + orbit
               elif result < 0:
                   #print("ASCENDING PASS")
                   orbit_title = "(Ascending Pass)"
                   orbit = "A"		   
                   move( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.tif',  main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + 'A_' + start + '.tif')
                   orbit = "A"                   
                   product = product + "A"
               elif result == 0: # Pass under a cut (equal for both lines)
                   #print("PASS UNDER CUT. CHANGING THE REFERENCE")
                   a = int(int(data.shape[0])/2)
                   factor = int(int(data.shape[0])/5)       
                   x1 = np.argwhere(data[a,:] != -9999)[-1]
                   x2 = np.argwhere(data[a+factor,:] != -9999)[-1]
                   #print(x1)
                   #print(x2)
                   result = x1 - x2
                   #print(result)
   
                   if result > 0:
                       #print("DESCENDING PASS")
                       orbit_title = "(Descending Pass)"
                       orbit = "D" 			   
                       move( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.tif',  main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + 'D_' + start + '.tif')
                       orbit = "D"                       
                       product = product + orbit
                   elif result < 0:
                       #print("ASCENDING PASS")
                       orbit_title = "(Ascending Pass)"
                       orbit = "A"			   
                       move( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.tif',  main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + 'A_' + start + '.tif')
                       orbit = "A"                       
                       product = product + orbit
                   elif result == 0:
                       #print("GIVE UP!")			   
                       orbit_title = "(Unknown)"
                       move( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.tif',  main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + 'E_' + start + '.tif')
                       orbit = "E"                       
                       product = product + orbit			   
       else:
            move( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.tif',  main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + orbit + '_' + start + '.tif')
            product = product + orbit
		
   print('Generated GeoTIFF: ','GCM_' + product + '_' + start + '.tif')
   #print(data[a,227])
   #print(data[a,228])
   #print(data[a,229])
   #print(data[a,:] - data[a+1,:])
   # Use GDAL exceptions
   #gdal.UseExceptions() 
   try:
       # Check if there is valid pixels in the region of interest
       geotiff = gdal.Open( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.tif')
       band = geotiff.GetRasterBand(1)
       stats = band.GetStatistics(True, True)
       geotiff = None 
       os.remove( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.tif.aux.xml')
       if (product != "SEAICN" and product != "SEAICS"):
	      # Generates the daily mosaic
          start_day = start[0:8]
          gdal.BuildVRT( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.vrt', sorted(glob.glob( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start_day + '*.tif'), key=os.path.getmtime), srcNodata = -9999)
          gdal.Translate( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product[2:6] + 'DA_' + start + '.tif',  main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.vrt', outputType = gdal.GDT_Float32, width = width, height = height)        
          print('Generated GeoTIFF: ','GCM_' + product[2:6] + 'DA_' + start + '.tif')  
          os.remove( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product + '_' + start + '.vrt')
          
          # Check if there is valid pixels in the region of interest
          mosaic = gdal.Open( main_dir + '//Output//' + satellite + '//' + storage + '//' + 'GCM_' + product[2:6] + 'DA_' + start + '.tif')
          band = mosaic.GetRasterBand(1)
          data = band.ReadAsArray()
          data[data == min(data[0])] = np.nan
          mosaic = None  
       else:
          orbit_title = ""
       
       if (product != "SEAICN" and product != "SEAICS"):
          #------------------------------------------------------------------------------------------------------
          #------------------------------------------------------------------------------------------------------
          # Plot configuration
          plot_config = {
          "resolution": resolution, 
          "dpi": 150, 
          "states_color": 'white', "states_width": data.shape[0] * 0.00018, 
          "countries_color": 'gold', "countries_width": data.shape[0] * 0.00012,
          "continents_color": 'gold', "continents_width": data.shape[0] * 0.00025,
          "grid_color": 'white', "grid_width": data.shape[0] * 0.00025, "grid_interval": 10.0,
          "vmin": vmin, "vmax": vmax, "cmap": cmap,
          "title_text": "GCOM-W1 " + prod_title + " " + orbit_title + " ", "title_size": int(data.shape[1] * 0.005), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[0] - int(data.shape[0] * 0.016), 
          "thick_interval": thick_interval, "cbar_labelsize": int(data.shape[0] * 0.005), "cbar_labelpad": -int(data.shape[0] * 0.0),
          "file_name_id_1": "GCM",  "file_name_id_2": product + "_SEC"
          }
          #------------------------------------------------------------------------------------------------------
          #------------------------------------------------------------------------------------------------------
          # Choose the plot size (width x height, in inches)
          fig = plt.figure(figsize=(data.shape[1]/float(plot_config["dpi"]), data.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])
          # Define the projection
          proj = ccrs.PlateCarree()
          # Use the PlateCarree projection in cartopy
          ax = plt.axes([0, 0, 1, 1], projection=proj)
          ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())
          # Define the image extent
          img_extent = [extent[0], extent[2], extent[1], extent[3]]
          # Add a background image
          #ax.stock_img()
          fname = os.path.join(main_dir + '//Maps//', 'land_ocean_ice_8192.jpg')
          ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)
          #date = datetime(int(year), int(month), int(day), int(hour))
          #ax.add_feature(Nightshade(date, alpha=0.7), zorder=2)
          # Plot the image
          img = ax.imshow(data, vmin=plot_config["vmin"], vmax=plot_config["vmax"], origin='upper', extent=img_extent, cmap=plot_config["cmap"], zorder=3)
       elif (product == "SEAICN"):
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
          "title_text": "GCOM-W1 " + prod_title + " ", "title_size": int(2712 * 0.005), "title_x_offset": int(2712 * 0.01), "title_y_offset": 2712 - int(2712 * 0.016), 
          "thick_interval": thick_interval, "cbar_labelsize": int(2712 * 0.005), "cbar_labelpad": -int(2712 * 0.0),
          "file_name_id_1": "GCM",  "file_name_id_2": product + "_SEC"
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
       elif (product == "SEAICS"):
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
          "title_text": "GCOM-W1 " + prod_title + " ", "title_size": int(2712 * 0.005), "title_x_offset": int(2712 * 0.01), "title_y_offset": 2712 - int(2712 * 0.016), 
          "thick_interval": thick_interval, "cbar_labelsize": int(2712 * 0.005), "cbar_labelpad": -int(2712 * 0.0),
          "file_name_id_1": "GCM",  "file_name_id_2": product + "_SEC" 
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

       #------------------------------------------------------------------------------------------------------
       #------------------------------------------------------------------------------------------------------
       if (product != "SEAICN" and product != "SEAICS"):
          # Add labels to specific coordinates

          import configparser
          conf = configparser.ConfigParser()
          conf.read(main_dir + '//Utils//Labels//labels_gcm.ini')

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
              ax.plot(xpt, ypt, str(mtype), color=str(mcolor), markersize=int(msize), transform=ccrs.Geodetic(), markeredgewidth=1.0, markeredgecolor=(0, 0, 0, 1), zorder=10)
              txt = ax.text(xpt+x_offset , ypt+y_offset, label, fontsize=int(size), fontweight='bold', color=str(col), transform=ccrs.Geodetic(), zorder=11)
              txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='black')])
       #------------------------------------------------------------------------------------------------------
       #------------------------------------------------------------------------------------------------------

       # Add logos / images to the plot
       my_logo = plt.imread(main_dir + '//Logos//my_logo.png')
       newax = fig.add_axes([0.01, 0.03, 0.10, 0.10], anchor='SW', zorder=12) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
       newax.imshow(my_logo)
       newax.axis('off')
       
       # Add a legend to the plot
       if (product == "SOLCTA") or (product == "SOLCTD"):
           my_legend = plt.imread(main_dir + '//Legends//LANDCOVERTYPE_legend.png')
           newax = fig.add_axes([0.70, 0.70, 0.29, 0.29], anchor='NE', zorder=13) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
           newax.imshow(my_legend)
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
       
   except RuntimeError: # If there is no valid pixels in the region of interest, delete the GeoTIFF
       print("No valid data in the extent. Deleting created GeoTIFF")
       geotiff = None 
       os.remove('GCM_' + product + '_' + start + '.tif') 
           
###############################################################################
# Reading the Data
###############################################################################
  
# Path to the GCOM file
path = sys.argv[1]

# Variable that will store if it is ascending or descending
orbit = "None"

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

# Get the aquisition start date
start = (path[path.find("_e")+2:path.find("_c")])
start = start[0:14]
#print(start)
date_formated = start[0:4] + "-" + start[4:6] + "-" + start[6:8] + " " + start [8:10] + ":" + start [10:12] + " UTC"
#print(date_formated)
date_file = start

# Initialize the orbit_title variable
orbit_title = "None"

# Satellite name (for folder and file name creation)
satellite = "GCM"
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Get the product type:
product = (path[path.find("AMSR2-")+6:path.find("_v")])

# Possibilities:
# MBT
# OCEAN
# PRECIP
# SEAICE-NH
# SEAICE-SH
# SNOW
# SOIL
#print(product)

if (product == "MBT"):
    #print("MBT")
    '''
    product = 'IM69H'
    variable_lat = 'Latitude_for_6'
    variable_lon = 'Longitude_for_6'
    variable_env = 'Brightness_Temperature_6_GHzH'
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    product = 'IM69V'
    variable_lat = 'Latitude_for_6'
    variable_lon = 'Longitude_for_6'
    variable_env = 'Brightness_Temperature_6_GHzV'
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    product = 'IM73H'
    variable_lat = 'Latitude_for_7'
    variable_lon = 'Longitude_for_7'
    variable_env = 'Brightness_Temperature_7_GHzH'
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    product = 'IM73V'
    variable_lat = 'Latitude_for_7'
    variable_lon = 'Longitude_for_7'
    variable_env = 'Brightness_Temperature_7_GHzV'
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    product = 'IM10H'
    variable_lat = 'Latitude_for_10'
    variable_lon = 'Longitude_for_10'
    variable_env = 'Brightness_Temperature_10_GHzH'
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    product = 'IM10V'
    variable_lat = 'Latitude_for_10'
    variable_lon = 'Longitude_for_10'
    variable_env = 'Brightness_Temperature_10_GHzV'
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    product = 'IM18H'
    variable_lat = 'Latitude_for_18'
    variable_lon = 'Longitude_for_18'
    variable_env = 'Brightness_Temperature_18_GHzH'
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    product = 'IM18V'
    variable_lat = 'Latitude_for_18'
    variable_lon = 'Longitude_for_18'
    variable_env = 'Brightness_Temperature_18_GHzV'
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    product = 'IM23H'
    variable_lat = 'Latitude_for_23'
    variable_lon = 'Longitude_for_23'
    variable_env = 'Brightness_Temperature_23_GHzH'
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    product = 'IM23V'
    variable_lat = 'Latitude_for_23'
    variable_lon = 'Longitude_for_23'
    variable_env = 'Brightness_Temperature_23_GHzV'
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    '''
    #=================================================================================
    product = 'IM36H'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_36'
    variable_lon = 'Longitude_for_36'
    variable_env = 'Brightness_Temperature_36_GHzH'
    cmap = 'jet'
    vmin = 135
    vmax = 285
    thick_interval = 5.0
    prod_title = "36.5 GHz Band Horizontal Polarization"
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
    product = 'IM36V'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_36'
    variable_lon = 'Longitude_for_36'
    variable_env = 'Brightness_Temperature_36_GHzV'
    cmap = 'jet'
    vmin = 180
    vmax = 295
    thick_interval = 5.0
    prod_title = "36.5 GHz Band Vertical Polarization"
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
    product = 'IM8HA'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_89A'
    variable_lon = 'Longitude_for_89A'
    variable_env = 'Brightness_Temperature_89_GHz_AH'
    cmap = 'jet'
    vmin = 165
    vmax = 290
    thick_interval = 5.0
    prod_title = "89.0 GHz Band Horizontal Polarization"
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
    product = 'IM8VA'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_89A'
    variable_lon = 'Longitude_for_89A'
    variable_env = 'Brightness_Temperature_89_GHz_AV'
    cmap = 'jet'
    vmin = 180
    vmax = 295
    thick_interval = 5.0
    prod_title = "89.0 GHz Band Vertical Polarization"
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
    '''
    product = 'IM8HB'
    variable_lat = 'Latitude_for_89B'
    variable_lon = 'Longitude_for_89B'
    variable_env = 'Brightness_Temperature_89_GHz_BH'
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    product = 'IM8VB'
    variable_lat = 'Latitude_for_89B'
    variable_lon = 'Longitude_for_89B'
    variable_env = 'Brightness_Temperature_89_GHz_BV'
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    '''
elif (product == "OCEAN"):
    #print("OCEAN")
    #=================================================================================
    product = 'OCRRT'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_Low_Resolution'
    variable_lon = 'Longitude_for_Low_Resolution'
    variable_env = 'Rain_Rate'
    my_cmap = matplotlib.cm.get_cmap('jet')
    my_cmap.set_under((1.0, 1.0, 1.0, 0.5))
    cmap = my_cmap
    vmin = 1.0
    vmax = 60
    thick_interval = 5.0
    prod_title = "Rain Rate"   
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
    product = 'OCCLW'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_Low_Resolution'
    variable_lon = 'Longitude_for_Low_Resolution'
    variable_env = 'CLW'
    cmap = 'jet'
    vmin = 0.0
    vmax = 0.5
    thick_interval = 0.025
    prod_title = "Cloud Liquid Water"
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
    product = 'OCSST'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_Low_Resolution'
    variable_lon = 'Longitude_for_Low_Resolution'
    variable_env = 'SST'
    cmap = 'jet'
    vmin = 268
    vmax = 308
    thick_interval = 5.0
    prod_title = "Sea Surface Temperature"
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
    product = 'OCTPW'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_Low_Resolution'
    variable_lon = 'Longitude_for_Low_Resolution'
    variable_env = 'TPW'
    colors = ["#bc8462", "#ae656f", "#a44a79", "#962e97", "#6158c5", "#2b8ffb", "#5fcdff", "#94fff0", "#a5ff94", "#fff88c", "#ffbf52", "#ec7b27", "#b84827", "#a1333d", "#bd5478", "#cc6a99", "#d982b8"]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    cmap = cmap
    vmin = 0
    vmax = 80
    thick_interval = 5.0
    prod_title = "Total Precipitable Water"
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
    product = 'OCWSP'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_Low_Resolution'
    variable_lon = 'Longitude_for_Low_Resolution'
    variable_env = 'WSPD'	
    colors = ["#7d7d7d", "#2c2c2c", "#00ffff", "#0000ff", "#00ff00", "#007300", "#ffff28", "#ffbe00", "#ff8c0a", "#e92104", "#ff2a45", "#ff0000", "#ca7c4c", "#470c0c", "#ff00ff", "#62009a", "#320064"]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    cmap = cmap
    vmin = 0
    vmax = 25
    thick_interval = 1.0
    prod_title = "Sea Surface Wind Speed"
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
elif (product == "PRECIP"):
    #print("PRECIP")
    #=================================================================================    
    product = 'PRRRT'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_High_Resolution'
    variable_lon = 'Longitude_for_High_Resolution'
    variable_env = 'Rain_Rate'	
    my_cmap = matplotlib.cm.get_cmap('jet')
    my_cmap.set_under((1.0, 1.0, 1.0, 0.5))
    cmap = my_cmap
    vmin = 1.0
    vmax = 60
    thick_interval = 5.0
    prod_title = "Rain Rate"    
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
    product = 'PRCVP'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_High_Resolution'
    variable_lon = 'Longitude_for_High_Resolution'
    variable_env = 'convectPrecipitation'	
    my_cmap = matplotlib.cm.get_cmap('jet')
    my_cmap.set_under((1.0, 1.0, 1.0, 0.5))
    cmap = my_cmap
    vmin = 1.0
    vmax = 60
    thick_interval = 5.0
    prod_title = "Convective Precipitation"    
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
    product = 'PRPPR'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_High_Resolution'
    variable_lon = 'Longitude_for_High_Resolution'
    variable_env = 'ProbabilityOfPrecip'	
    cmap = 'jet'
    vmin = 0
    vmax = 100
    thick_interval = 10.0
    prod_title = "Propability of Precipitation" 
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
elif (product == "SEAICE-NH"):
    #print("SEAICE-NH")
    #=================================================================================
    product = 'SEAICN'
    storage = product + "P_STR"
    variable_lat = 'Latitude'
    variable_lon = 'Longitude'
    variable_env = 'NASA_Team_2_Ice_Concentration'	
    my_cmap = matplotlib.cm.get_cmap('jet')
    my_cmap.set_under((0.0, 0.0, 0.0, 0.0))
    cmap = my_cmap
    vmin = 1
    vmax = 100
    thick_interval = 5.0
    prod_title = "Sea Ice Concentration - Northern Hemisphere"
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
elif (product == "SEAICE-SH"):
    #print("SEAICE-SH")	
    #=================================================================================
    product = 'SEAICS'
    storage = product + "P_STR"
    variable_lat = 'Latitude'
    variable_lon = 'Longitude'
    variable_env = 'NASA_Team_2_Ice_Concentration'	
    my_cmap = matplotlib.cm.get_cmap('jet')
    my_cmap.set_under((0.0, 0.0, 0.0, 0.0))
    cmap = my_cmap
    vmin = 1
    vmax = 100
    thick_interval = 5.0
    prod_title = "Sea Ice Concentration - Southern Hemisphere"
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
elif (product == "SNOW"):
    #print("SNOW")
    #=================================================================================
    product = 'SNSNC'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_Low_Resolution'
    variable_lon = 'Longitude_for_Low_Resolution'
    variable_env = 'Snow_Cover'
    colors = ["#383881", "#25593d", "#757575", "#ffffff"]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    cmap = cmap
    vmin = 1
    vmax = 4
    thick_interval = 0.1
    prod_title = "Snow Cover"
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
    product = 'SNSND'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_Low_Resolution'
    variable_lon = 'Longitude_for_Low_Resolution'
    variable_env = 'Snow_Depth'
    colors = ["#d3d3d3", "#b0c4de", "#add8e6", "#afeeee", "#48d1cc", "#00bfff", "#4169e1", "#000080", "#990082", "#8b008b", "#9400d3", "#ff32cc", "#c71585", "#a0522d", "#8b4513"]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    cmap = cmap
    vmin = 0
    vmax = 150
    thick_interval = 10.0
    prod_title = "Snow Depth"
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
    product = 'SNSWE'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_Low_Resolution'
    variable_lon = 'Longitude_for_Low_Resolution'
    variable_env = 'SWE'
    colors = ["#c0c0c0", "#33ffff", "#0080ff", "#00cc00", "#ffff00", "#007e00", "#663300", "#ff0000"]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    cmap = cmap
    vmin = 0
    vmax = 160
    thick_interval = 10.0
    prod_title = "Snow Water Equivalent"
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================
elif (product == "SOIL"):
    #print("SOIL")
    #=================================================================================
    product = 'SOLCT'
    storage = product + "P_STR"
    variable_lat = 'Latitude_for_Low_Resolution'
    variable_lon = 'Longitude_for_Low_Resolution'
    variable_env = 'Land_Cover_Type'
    #colors = ["#383881", "#2b9749", "#20dd54", "#23793b", "#1cb144", "#6ad36c", "#9eff34", "#b7d61d", "#204b30", "#145b2e", "#1aeaa0", "#7ee9cf", "#aa8855", "#66aab8", "#000000", "#000000"]
    colors = ["#0066cc", "#006600", "#009900", "#00cc00", "#00ff00", "#66cc00", "#00cc66", "#b3ff66", "#cccc00", "#ffe9b4", "#99ff99", "#ffff00", "#e9ce90", "#00ff80", "#c0c0c0"]
    cmap = matplotlib.colors.ListedColormap(colors)
    cmap = cmap
    vmin = 0
    vmax = 15
    thick_interval = 1.0
    prod_title = "Land Cover Type"
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)    
    #=================================================================================
    product = 'SOSMT'
    storage = product +  "P_STR"
    variable_lat = 'Latitude_for_Low_Resolution'
    variable_lon = 'Longitude_for_Low_Resolution'
    variable_env = 'Soil_Moisture'
    colors = ["#ff7f00", "#ffff00", "#00ff00", "#00967f", "#0000ff"]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    cmap = cmap
    vmin = 0.0
    vmax = 0.4
    thick_interval = 0.025
    prod_title = "Soil Moisture"
    procGcom(product, start, variable_lat, variable_lon, variable_env, width, height)
    #=================================================================================

print('Total processing time:', round((t.time() - start_time),2), 'seconds.') 
