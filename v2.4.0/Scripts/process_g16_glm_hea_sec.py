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
__version__ = "2.4.0"
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
from netCDF4 import Dataset, num2date                        # Read / Write NetCDF4 files
from mpl_toolkits.axes_grid1.inset_locator import inset_axes # Add a child inset axes to this existing axes.
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
import matplotlib.pyplot as plt                              # Plotting library
import numpy as np                                           # Scientific computing with Python
import cartopy, cartopy.crs as ccrs                          # Plot maps
import cartopy.io.shapereader as shpreader                   # Import shapefiles
import time as t                                             # Time access and conversion
import os                                                    # Miscellaneous operating system interfaces
import re                                                    # re
import glob                                                  # Unix style pathname pattern expansion
import sys                                                   # Import the "system specific parameters and functions" module
import os 												     # Miscellaneous operating system interfaces
from os.path import dirname, abspath                         # Return a normalized absolutized version of the pathname path 
import platform                                              # To check which OS is being used
import math                                                  # Import math
from html_update import update                               # Update the HTML animation 
from remap import remap                                      # Import the Remap function
import warnings
warnings.filterwarnings("ignore")
#-----------------------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()  

# SHOWCast directory:
main_dir = dirname(dirname(abspath(__file__)))

# Path for logging purposes
path = (sys.argv[1])

# GLM file
path_glm = (sys.argv[1])[:-4]

# Get the GLM file parent directory
from pathlib import Path
glm_dir = Path(path_glm).parent

# Read the GLM file
fileGLM = Dataset(path_glm)

# Choose the visualization extent (min lon, min lat, max lon, max lat)
extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]

# Desired resolution
resolution = int(sys.argv[6])

# Define KM_PER_DEGREE
KM_PER_DEGREE = 111.32

# Compute grid dimension
sizex = int(((extent[2] - extent[0]) * KM_PER_DEGREE) / resolution) 
sizey = int(((extent[3] - extent[1]) * KM_PER_DEGREE) / resolution) 

# Read the central longitude
longitude = fileGLM.variables['lon_field_of_view'][0]

# Read the satellite height
h = fileGLM.variables['nominal_satellite_height'][0] * 1000

# Reading the file time and date
add_seconds = int(fileGLM.variables['product_time'][0])
date = datetime(2000,1,1,12) + timedelta(seconds=add_seconds)
date_formated = date.strftime('%Y-%m-%d %H:%M:%S UTC')
date_file = date.strftime('%Y%m%d%H%M%S')

# Separate the date parameters
year = date.strftime('%Y')
month = date.strftime('%m')
day = date.strftime('%d')
jday = date.strftime('%j')
hour = date.strftime('%H')
minutes = date.strftime('%M')
seconds = date.strftime('%S')
print(date_formated)

# Minutes you want to accumulate
acum_minutes = 10

# Initialize arrays for latitude, longitude, and event energy
e_lats = np.array([])
e_lons = np.array([])
g_lats = np.array([])
g_lons = np.array([])
f_lats = np.array([])
f_lons = np.array([])

if (seconds == '00'):
    
    print("This is a full minute file.")
    
    if (int(minutes) % acum_minutes == 0):
        
        print("This is a divisible minute number. Will start the accumulation using this file as a reference.")        
        date_ini = (datetime(int(year),int(month),int(day),int(hour),int(minutes),int(seconds)) - timedelta(minutes=acum_minutes))
        date_end = (datetime(int(year),int(month),int(day),int(hour),int(minutes),int(seconds)))
        
        print("Entering the accumulation loop")
        # GLM accumulation loop
        while (date_ini < date_end):
        
            # GOES-16 GLM file name convention (start of the scan)    
            file_name = '_s' + str(date_ini.strftime('%Y%j%H%M%S'))
            
            # Check if the file is in the ingestion folder:   
            for fname in os.listdir(glm_dir):
                if file_name in fname:
                    print(fname, " will be processed!")
                    
                    # Read the file
                    glm = Dataset(f'{glm_dir}/{fname}')
                    # Append lats / longs / event energies
                    e_lats = np.append(e_lats, glm.variables['event_lat'][:])
                    e_lons = np.append(e_lons, glm.variables['event_lon'][:])
                    g_lats = np.append(g_lats, glm.variables['group_lat'][:])
                    g_lons = np.append(g_lons, glm.variables['group_lon'][:])
                    f_lats = np.append(f_lats, glm.variables['flash_lat'][:])
                    f_lons = np.append(f_lons, glm.variables['flash_lon'][:])
            
            # Increment the date_ini in 20 seconds
            date_ini = (datetime.strptime(str(date_ini), '%Y-%m-%d %H:%M:%S') + timedelta(seconds=20))

        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        from scipy.ndimage.filters import gaussian_filter
        
        heatmap, xedges, yedges = np.histogram2d(g_lons, g_lats, bins=1000)
        heatmap = gaussian_filter(heatmap, sigma=2)
        heatmap = heatmap.T
        
        extent_glm = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------ 
        from matplotlib.colors import LinearSegmentedColormap
           
        from matplotlib import cm                                          # Colormap handling utilities
        colors = plt.get_cmap('gist_rainbow_r')(range(256))
        #colors = ["#fbdfff", "#ac53ff", "#6001fd", "#0e00ff", "#0f40fd", "#6a87ff", "#c2d7fd", "#fefefe", \
        #"#ffffff"]
        my_colors = cm.colors.LinearSegmentedColormap.from_list("",colors) # Create a custom colormap
        my_colors = my_colors(np.linspace(0, 1, 256))                      # Create the array
        my_colors[0:100,-1] = np.linspace(0.0,1.0, 100)#**2
        my_cmap = LinearSegmentedColormap.from_list(name='my_cmap', colors=my_colors)
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Read the satellite 
        satellite = getattr(fileGLM, 'platform_ID')

        # Product Name
        product = "GLMHEA_SEC" 
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------       
        # Seek for an ABI Band 13 file for the same time and date
        # Round the GLM time and date for the previous 10 minute mark
        date_round = date - timedelta(minutes=date.minute % 10, seconds=date.second, microseconds=date.microsecond)

        # Create the ABI Band 13 identifier
        abi_file_date = '_s' + date_round.strftime('%Y%j%H%M')
        #print(abi_file_date)

        # Get the Band 13, same file
        osystem = platform.system()
        if osystem == "Windows":
            path_ch13 = re.sub('GOES-R-GLM-Products\\\\OR_GLM*(.*)', '', path_glm)
        else:
            path_ch13 = re.sub('GOES-R-GLM-Products/OR_GLM*(.*)', '', path_glm)
        print(path_ch13)

        file = []
        for filename in sorted(glob.glob(path_ch13+'GOES-R-CMI-Imagery//Band13//OR_ABI-L2-CMIPF-M*C13_G16*.nc')):
            file.append(filename)
            
        # Seek for a GOES-16 file (same time) in the directory
        matching = [s for s in file if abi_file_date in s]     

        # If the file is not found, exit the loop
        if not matching:
            print("File Not Found! Exiting Script.")
            sys.exit()
        else: # If the file is found, continue
            print("File OK!")
            matching = matching[0]
            index = file.index(matching)
            path_ch13 = file[index]

        print(path_glm)
        print(path_ch13)        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------        
        # Open the GOES-R image
        file_ch13 = Dataset(path_ch13)

        # Read the central longitude
        longitude = file_ch13.variables['goes_imager_projection'].longitude_of_projection_origin

        # Read the semi major axis
        a = file_ch13.variables['goes_imager_projection'].semi_major_axis

        # Read the semi minor axis
        b = file_ch13.variables['goes_imager_projection'].semi_minor_axis

        # Calculate the image extent 
        h = file_ch13.variables['goes_imager_projection'].perspective_point_height
        x1 = file_ch13.variables['x_image_bounds'][0] * h 
        x2 = file_ch13.variables['x_image_bounds'][1] * h 
        y1 = file_ch13.variables['y_image_bounds'][1] * h 
        y2 = file_ch13.variables['y_image_bounds'][0] * h 

        # Choose the visualization extent (min lon, min lat, max lon, max lat)
        extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]

        # Variable to remap
        variable = "CMI"

        # Call the reprojection funcion
        grid = remap(path_ch13, variable, extent, resolution, h, a, b, longitude, x1, y1, x2, y2)
             
        # Read the data returned by the function 
        data = grid.ReadAsArray() - 273.15
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Plot configuration
        plot_config = {
        "resolution": resolution, 
        "dpi": 150, 
        "states_color": 'white', "states_width": sizey * 0.00006, 
        "countries_color": 'white', "countries_width": sizey * 0.00012,
        "continents_color": 'white', "continents_width": sizey * 0.00025,
        "grid_color": 'white', "grid_width": sizey * 0.00025, "grid_interval": 5.0,
        "title_text": "GOES-16 GLM (Heatmap)", "title_size": int(sizex * 0.005), "title_x_offset": int(sizex * 0.01), "title_y_offset": sizey - int(sizey * 0.016), 
        "file_name_id_1": satellite,  "file_name_id_2": product
        }
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Choose the plot size (width x height, in inches)
        fig = plt.figure(figsize=(sizex/float(plot_config["dpi"]), sizey/float(plot_config["dpi"])), dpi=plot_config["dpi"])

        # Define the projection
        proj = ccrs.PlateCarree()
          
        # Use the PlateCarree projection in cartopy
        ax = plt.axes([0, 0, 1, 1], projection=proj)
        ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

        # Define the image extent
        img_extent = [extent[0], extent[2], extent[1], extent[3]]
        #---------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------- 
        # Background color
        import cartopy.feature as cfeature
        land = ax.add_feature(cfeature.LAND, facecolor='black', zorder=1)
        ocean = ax.add_feature(cfeature.OCEAN, facecolor='black', zorder=2)
        
        # Plotting the empty full disk
        img1 = ax.imshow(data, vmin=-80, vmax=40, cmap='Greys', alpha = 0.50, extent=img_extent, zorder=3) 

        # Plot the GLM heatmap
        glm = ax.imshow(heatmap, vmin=0, vmax=40, interpolation='bilinear', extent=extent_glm, origin='lower', cmap=my_cmap, transform=ccrs.PlateCarree(), alpha = 1.00, zorder=4)

        # Plot the accumulated flashes, groups and events
        #img2 = ax.plot(e_lons,e_lats, 'o', markersize=1.0, color='#fffb8a', alpha = 0.01, transform=ccrs.PlateCarree(), zorder=5)
        #img3 = ax.plot(g_lons,g_lats, 'o', markersize=1.0, color='#fffdc7', alpha = 0.02, transform=ccrs.PlateCarree(), zorder=6)
        #img4 = ax.plot(f_lons,f_lats, 'o', markersize=1.0, color='#fff700', alpha = 0.20, transform=ccrs.PlateCarree(), zorder=7)
        #img2 = ax.plot(e_lons,e_lats, 'o', markersize=1.0, color='#dedede', alpha = 0.01, transform=ccrs.PlateCarree(), zorder=5)
        #img3 = ax.plot(g_lons,g_lats, 'o', markersize=1.0, color='#ededed', alpha = 0.02, transform=ccrs.PlateCarree(), zorder=6)
        #img4 = ax.plot(f_lons,f_lats, 'o', markersize=1.0, color='#ffffff', alpha = 0.20, transform=ccrs.PlateCarree(), zorder=7)
        #---------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------
        # Add states and provinces
        shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=8)

        # Add coastlines and borders
        #ax.coastlines(resolution='50m', color=plot_config["countries_color"], linewidth=plot_config["countries_width"], zorder=11)
        #ax.add_feature(cartopy.feature.BORDERS, edgecolor=plot_config["continents_color"], linewidth=plot_config["continents_width"], zorder=12)

        # Add countries
        shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=9)

        # Add continents
        shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_coastline.shp').geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=10)
          
        # Add gridlines
        ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=False, zorder=11)

        # Remove the outline border
        ax.outline_patch.set_visible(False)

        # Add a title
        plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=12)

        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Add labels to specific coordinates
        
        import configparser
        conf = configparser.ConfigParser()
        conf.read(main_dir + '//Utils//Labels//labels_g16.ini')

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
            ax.plot(xpt, ypt, str(mtype), color=str(mcolor), markersize=int(msize), transform=ccrs.Geodetic(), markeredgewidth=1.0, markeredgecolor=(0, 0, 0, 1), zorder=13)
            txt = ax.text(xpt+x_offset , ypt+y_offset, label, fontsize=int(size), fontweight='bold', color=str(col), transform=ccrs.Geodetic(), zorder=14)
            txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='black')])
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------

        # Add logos / images to the plot
        my_logo = plt.imread(main_dir + '//Logos//my_logo.png')
        newax = fig.add_axes([0.01, 0.03, 0.10, 0.10], anchor='SW', zorder=15) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
        newax.imshow(my_logo)
        newax.axis('off')

        # Create the satellite output directory if it doesn't exist
        out_dir = (sys.argv[7]) + satellite
        if not os.path.exists(out_dir):
           os.mkdir(out_dir)

        # Create the product output directory if it doesn't exist
        out_dir = (sys.argv[7]) + satellite + '//' + product + '//'
        if not os.path.exists(out_dir):
           os.mkdir(out_dir)
           
        # Save the image
        plt.savefig(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.png', facecolor='black')#, bbox_inches='tight', pad_inches=0, facecolor='black')
        #plt.show()

        # Update the animation
        nfiles = 20
        update(satellite, product, nfiles, sys.argv[7], sys.argv[8])

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
    else:
        print("This is not a divisible minute. Exiting script.")    
        # Put the processed file on the log
        import datetime # Basic Date and Time types
        with open(main_dir + '//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
         log.write(str(datetime.datetime.now()))
         log.write('\n')
         log.write(path + '\n')
         log.write('\n')        
        quit()
else:
    print("This is not a full minute file. Exiting script.")
    # Put the processed file on the log
    import datetime # Basic Date and Time types
    with open(main_dir + '//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
     log.write(str(datetime.datetime.now()))
     log.write('\n')
     log.write(path + '\n')
     log.write('\n') 
    quit()