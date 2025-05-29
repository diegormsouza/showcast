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
from matplotlib.image import imread                          # Read an image from a file into an array
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
hour_end = 25  # End time
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
        # Read the total precipitation
        try:
            totpr = grib.select(name='Total Precipitation', typeOfLevel = 'surface')[1]
        except:
            print("Field not available on the GRIB file. Skipping the current iteration.")
            continue  

        #################################################################################
        # For some reason the "Total Precipitation" variable doesnt' have the right keys!
        title = grib.select(name='2 metre temperature')[0] 

        # For later use
        init  = title.analDate     # Analysis date / time
        hour  = title.hour         # Run
        ftime = title.forecastTime # Forecast hour
        valid = title.validDate    # Valid date / time 

        #print("GRIB Keys :", sfcps.keys())

        # Read the run time
        run = str(title.hour).zfill(2) + 'Z'
        #################################################################################

        # Read the data for a specific region
        totpr, lats, lons = totpr.data(lat1=extent[1],lat2=extent[3],lon1=extent[0]+360,lon2=extent[2]+360)

        # Converting the longitudes to -180 ~ 180
        lons = lons - 360 

        #totpr2 = totpr
        #lons2 = lons
        #lats2 = lats
        #totpr2[totpr2 == 0] = np.nan

        import scipy.ndimage
        totpr = scipy.ndimage.zoom(totpr, 3)
        lats = scipy.ndimage.zoom(lats, 3)
        lons = scipy.ndimage.zoom(lons, 3)
                
        #---------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------
        # NOTE: FOR SOME REASON THE ZOOM WITH NAN CREATES WRONG VALUES, SO I HAD TO DO THE WORKAROUND BELOW (INVISIBLE COLORBAR AT THE BEGGINING)
        
        from matplotlib import cm                                          # Colormap handling utilities
        # Create the color scale 
        colors = ["#b4f0f0", "#96d2fa", "#78b9fa", "#3c95f5", "#1e6deb", "#1463d2", "#0fa00f", "#28be28", "#50f050", "#72f06e", "#b3faaa", "#fff9aa", "#ffe978", "#ffc13c", "#ffa200", "#ff6200", "#ff3300", "#ff1500", "#c00100", "#a50200", "#870000", "#653b32"]
        #cmap = matplotlib.colors.ListedColormap(colors)
       
        my_colors = cm.colors.LinearSegmentedColormap.from_list("",colors) # Create a custom colormap
        my_colors = my_colors(np.linspace(0, 1, 256))                      # Create the array
        my_colors[0:2,-1] = 0.0 #np.linspace(0.0,1.0, 1)#**2
        cmap = LinearSegmentedColormap.from_list(name='my_cmap', colors=my_colors)

        cmap.set_over('#000000')
        cmap.set_under('#828282')
        
        vmin = 1
        vmax = 90
        thick_interval = 5

        # Create the color scale for low values
        colors2 = ["#bebebe", "#a5a5a5", "#969696", "#828282"]
        
        my_colors = cm.colors.LinearSegmentedColormap.from_list("",colors2) # Create a custom colormap
        my_colors = my_colors(np.linspace(0, 1, 256))                      # Create the array
        my_colors[0:80,-1] = 0.0#np.linspace(0.0,1.0, 128)#**2
        cmap2 = LinearSegmentedColormap.from_list(name='my_cmap', colors=my_colors)
        cmap2.set_over('#828282')
        
        vmin2 = 0.0
        vmax2 = 1.0
        thick_interval2 = 0.1

        #---------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------
                        
        # Product name
        satellite = "GFS"
        product   = "ACCPRE_" + run
        
        # Plot configuration
        plot_config = {
        "resolution": resolution, 
        "dpi": 150, 
        "states_color": 'black', "states_width": sizey * 0.00006, 
        "countries_color": 'black', "countries_width": sizey * 0.00012,
        "continents_color": 'black', "continents_width": sizey * 0.00025,
        "grid_color": 'white', "grid_width": sizey * 0.00025, "grid_interval": 5.0,
        "vmin": vmin, "vmax": vmax, "cmap": cmap,
        "title_text": "GFS (0.5°): Total Precipitation" + "    -    " + "Init: " + str(init)[:-6] + "Z | Forecast Hour: [" + str(ftime).zfill(3) + "]" + " | Valid: " + str(valid)[:-6] + "Z ", "title_size": int(sizex * 0.005), "title_x_offset": int(sizex * 0.01), "title_y_offset": sizey - int(sizey * 0.016), 
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

        # Add a background image
        import cartopy.feature as cfeature
        land = ax.add_feature(cfeature.LAND, facecolor='whitesmoke', zorder=1)
        ocean = ax.add_feature(cfeature.OCEAN, facecolor='white', zorder=1)

        # Plot the image (low values)
        data_min2 = 0.0
        data_max2 = 2.0
        interval2 = 0.2
        levels2 = np.arange(data_min2,data_max2,interval2)
        #totpr2[totpr2 > 1] = np.nan
        img3 = ax.contourf(lons, lats, totpr, transform=ccrs.PlateCarree(), cmap=cmap2, levels=levels2, zorder=2)
        
        # Plot the image (high values)
        # Define de contour interval
        data_min = 1
        data_max = 90 
        interval = 5
        levels = np.arange(data_min,data_max,interval)
        img1 = ax.contourf(lons, lats, totpr, transform=ccrs.PlateCarree(), cmap=cmap, levels=levels, extend='max', zorder=3)
        img2 = ax.contour(lons, lats, totpr, transform=ccrs.PlateCarree(), colors='black', linewidths=0.1, levels=levels, zorder=4)
        ax.clabel(img2, inline=1, inline_spacing=0, fontsize=plot_config["cbar_labelsize"],fmt = '%1.0f', colors= 'black', zorder=5)

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
        #plt.title("GFS (0.5°): Total Precipitation", fontweight='bold', fontsize=7, loc='left')
        #plt.title("Init: " + str(init)[:-6] + "Z | Forecast Hour: [" + str(ftime).zfill(3) + "]" + " | Valid: " + str(valid)[:-6] + "Z ", fontsize=6, loc='right')
        
        # Add a title
        plt.annotate(plot_config["title_text"], xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=10)
       
        # To put colorbar inside picture
        axins1 = inset_axes(ax, width="2%", height="100%", loc='right', borderpad=0.0)
        
        # Add a colorbar
        ticks = np.arange(plot_config["vmin"], plot_config["vmax"], plot_config["thick_interval"]).tolist()     
        ticks = plot_config["thick_interval"] * np.round(np.true_divide(ticks,plot_config["thick_interval"]))
        ticks = ticks[1:]
        cb = fig.colorbar(img1, cax=axins1, orientation="vertical", ticks=ticks)
        cb.set_label(label='Total Precipitation (mm)', size='10', weight='bold') 
        cb.outline.set_visible(False)
        cb.ax.tick_params(width = 0)
        cb.ax.xaxis.set_tick_params(pad=plot_config["cbar_labelpad"])
        cb.ax.yaxis.set_ticks_position('left')
        cb.ax.yaxis.set_label_position('left')
        cb.ax.tick_params(axis='y', colors='black', labelsize=plot_config["cbar_labelsize"])

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
