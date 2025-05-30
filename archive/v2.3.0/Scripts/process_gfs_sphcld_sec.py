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
__credits__ = ["Diego Souza", "Regina Ito"]
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

# Choose the visualization extent (min lon, min lat, max lon, max lat)
extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]

# Desired resolution
resolution = int(sys.argv[6])

# Define KM_PER_DEGREE
KM_PER_DEGREE = 111.32

# Compute grid dimension
sizex = int(((extent[2] - extent[0]) * KM_PER_DEGREE) / resolution) 
sizey = int(((extent[3] - extent[1]) * KM_PER_DEGREE) / resolution) 

# For logging purposes
path = (sys.argv[1])[:-16]

# Image path
path_gfs = path[:-7]
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Data you want to process
# (to process only the analisys, end and inc should be equal).
hour_ini = 0   # Init time  
hour_end = 24  # End time
hour_inc = 24  # Increment

for hour in range(hour_ini, hour_end, hour_inc):

    path_loop = path_gfs + str(hour).zfill(3)
    print(path_loop)
    
    if (os.path.exists(path_loop)):
    
        print("Processing file: ", path_loop)
        
        # Open the GRIB file
        grib = pygrib.open(path_loop)

        #---------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------   
        # Read the relative humidity in 300 hPa
        try:
            sh300 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 300)[0]
        except:
            print("Field not available on the GRIB file. Skipping the current iteration.")
            continue  
            
        # For later use
        init  = sh300.analDate     # Analysis date / time
        hour  = sh300.hour         # Run
        ftime = sh300.forecastTime # Forecast hour
        valid = sh300.validDate    # Valid date / time 

        #print("GRIB Keys :", sfcps.keys())

        # Read the run time
        run = str(sh300.hour).zfill(2) + 'Z'

        # Read the data for a specific region
        sh300, lats, lons = sh300.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

        # To smooth the contours
        import scipy.ndimage
        sh300 = scipy.ndimage.zoom(sh300, 3)
        lats = scipy.ndimage.zoom(lats, 3)
        lons = scipy.ndimage.zoom(lons, 3)

        # Removing the values < 70%
        sh300[sh300 < 70] = np.nan

        # Converting the longitudes to -180 ~ 180
        lons = lons - 360 
        #print(sh300.shape)
        #---------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------
        # Read the relative humidity in 500 hPa 
        try:
            sh500 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 500)[0]
        except:
            print("Field not available on the GRIB file. Skipping the current iteration.")
            continue 
            
        # Read the data for a specific region
        sh500 = sh500.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

        # To smooth the contours
        sh500 = scipy.ndimage.zoom(sh500, 3)

        # Removing the values < 70%
        sh500[sh500 < 70] = np.nan

        #---------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------
        # Read the relative humidity in 500 hPa   
        try:
            sh800 = grib.select(name='Relative humidity', typeOfLevel = 'isobaricInhPa', level = 800)[0]
        except:
            print("Field not available on the GRIB file. Skipping the current iteration.")
            continue 
            
        # Read the data for a specific region
        sh800 = sh800.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)[0]

        # To smooth the contours
        sh800 = scipy.ndimage.zoom(sh800, 3)

        # Removing the values < 70%
        sh800[sh800 < 70] = np.nan

        #---------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------
        # Create the color scale 
        colors = ["#acefb2", "#f6bcbb", "#f3c4c4", "#f6cfd0", "#fde8e7"]
        cmap = matplotlib.colors.ListedColormap(colors)
        cmap.set_over('#fde8e7')
        cmap.set_under('#f6b5b5')

        # Create the color scale 
        colors = ["#f6b5b5", "#bbf2c1", "#cbf5cd", "#d0f6cf", "#e6fbe6"]
        cmap2 = matplotlib.colors.ListedColormap(colors)
        cmap2.set_over('#e6fbe6')
        cmap2.set_under('#f6b5b5')

        # Create the color scale 
        colors = ["#b2b8f6", "#bfbef8", "#cbcaf3", "#d2d2f8", "#e7e8fc"]
        cmap3 = matplotlib.colors.ListedColormap(colors)
        cmap3.set_over('#e7e8fc')
        cmap3.set_under('#b2b8f6')

        vmin = 70.0
        vmax = 100.0
        thick_interval = 5.0

        #---------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------
                
        # Product name
        satellite = "GFS"
        product   = "SPHCLD_" + run
        
        # Plot configuration
        plot_config = {
        "resolution": resolution, 
        "dpi": 150, 
        "states_color": 'black', "states_width": sizey * 0.00006, 
        "countries_color": 'black', "countries_width": sizey * 0.00012,
        "continents_color": 'black', "continents_width": sizey * 0.00025,
        "grid_color": 'white', "grid_width": sizey * 0.00025, "grid_interval": 5.0,
        "vmin": vmin, "vmax": vmax, "cmap": cmap,
        "title_text": "GFS (0.5°): Relative Humidity at 800, 500, & 300 mb or Low, Middle, & High Clouds" + "    -    " + "Init: " + str(init)[:-6] + "Z | Forecast Hour: [" + str(ftime).zfill(3) + "]" + " | Valid: " + str(valid)[:-6] + "Z ", "title_size": int(sizex * 0.005), "title_x_offset": int(sizex * 0.01), "title_y_offset": sizey - int(sizey * 0.016),  
        "thick_interval": thick_interval, "cbar_labelsize": int(sizey * 0.005), "cbar_labelpad": -int(sizey * 0.00),
        "file_name_id_1": satellite,  "file_name_id_2": product
        }
        #---------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------

        # Choose the plot size (width x height, in inches)
        fig = plt.figure(figsize=(sizex/float(plot_config["dpi"]), sizey/float(plot_config["dpi"])), dpi=plot_config["dpi"])
          
        # Define the projection
        proj = ccrs.PlateCarree()

        # Use the PlateCarree projection in cartopy
        ax = plt.axes([0, 0, 1, 1], projection=proj)
        #ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

        # Define the image extent
        img_extent = [extent[0], extent[2], extent[1], extent[3]]

        import cartopy.feature as cfeature
        land = ax.add_feature(cfeature.LAND, facecolor='whitesmoke', zorder=1)
        ocean = ax.add_feature(cfeature.OCEAN, facecolor='lightcyan', zorder=1)

        # Define de contour interval
        data_min = 70.0
        data_max = 100.0
        interval = 5.0
        levels = np.arange(data_min,data_max,interval)
         
        # Plot the image
        img1 = ax.contourf(lons, lats, sh800, transform=ccrs.PlateCarree(), cmap=cmap3, levels=levels, extend='both', alpha = 0.8, zorder=2)
        img3 = ax.contourf(lons, lats, sh500, transform=ccrs.PlateCarree(), cmap=cmap2, levels=levels, extend='both', alpha = 0.8, zorder=4)
        img5 = ax.contourf(lons, lats, sh300, transform=ccrs.PlateCarree(), cmap=cmap, levels=levels, extend='both', alpha = 0.8, zorder=5)

        # Add states and provinces
        shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=6)

        # Add countries
        shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=7)

        # Add continents
        shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_coastline.shp').geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=8)
          
        # Add gridlines
        gl = ax.gridlines(color=plot_config["grid_color"], alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-180, 180, 5), draw_labels=False, zorder=9)
        gl.xlabels_top=False
        gl.ylabels_right=False

        # Remove the outline border
        ax.outline_patch.set_visible(False)
          
        # Add a title
        #plt.title("GFS (0.5°): Relative Humidity at 800, 500, & 300mb or Low, Middle, & High Clouds", fontweight='bold', fontsize=7, loc='left')
        #plt.title("Init: " + str(init)[:-6] + "Z | Forecast Hour: [" + str(ftime).zfill(3) + "]" + " | Valid: " + str(valid)[:-6] + "Z ", fontsize=6, loc='right')

        # Add a title
        plt.annotate(plot_config["title_text"], xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=9)
       
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        
        # Add labels to specific coordinates

        import configparser
        conf = configparser.ConfigParser()
        if ('.sam.' in path):
            conf.read(main_dir + '//Utils//Labels//labels_gfs_sam.ini')
        else:
            conf.read(main_dir + '//Utils//Labels//labels_gfs_crb.ini')
            
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
        newax = fig.add_axes([0.01, 0.01, 0.10, 0.10], anchor='SW', zorder=12) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
        newax.imshow(my_logo)
        newax.axis('off')

        # Add a legend to the plot
        my_legend = plt.imread(main_dir + '//Legends//GFS_CLOUDS_legend.png')
        newax = fig.add_axes([0.55, 0.03, 0.44, 0.44], anchor='SE', zorder=13) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
        newax.imshow(my_legend)
        newax.axis('off')

        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        
        # Create the satellite output directory if it doesn't exist
        out_dir = main_dir + '//Output//' + satellite
        if not os.path.exists(out_dir):
           os.mkdir(out_dir)

        # Create the product output directory if it doesn't exist
        out_dir = main_dir + '//Output//' + satellite + '//' + product + '//'
        if not os.path.exists(out_dir):
           os.mkdir(out_dir)
   
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------

        # Save the image
        plt.savefig(out_dir + satellite + '_' + product + '_' + str(init)[:-9].replace('-', '') + str(hour).zfill(2) + 'Z_' + str(ftime).zfill(3) + '.png', bbox_inches='tight', pad_inches=0)

        # Show the image
        #plt.show()
        
        # Update the animation
        nfiles = 30
        update(satellite, product, nfiles)
    
    else:
        
        print("File not available.")

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Put the processed file on the log
import datetime # Basic Date and Time types
import pathlib  # Object-oriented filesystem paths
# Get the file modification time
mtime = datetime.datetime.fromtimestamp(pathlib.Path(path[:-4]).stat().st_mtime).strftime('%Y%m%d%H%M%S')
# Write to the log
with open(main_dir + '//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
    log.write(str(datetime.datetime.now()))
    log.write('\n')
    log.write(path + '_c' + mtime + '\n')
    log.write('\n')
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Total processing time
print('Total processing time:', round((t.time() - start),2), 'seconds.') 
