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
print(glm_dir)

# Read the GLM file
fileGLM = Dataset(path_glm)

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

print(year)
print(month)
print(day)
print(hour)
print(minutes)
print(seconds)

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

        #quit()

        # OR_GLM-L2-LCFA_G16_s2021067120000
        # OR_GLM-L2-LCFA_G16_s2021067120020
        # OR_GLM-L2-LCFA_G16_s2021067120040
        # OR_GLM-L2-LCFA_G16_s2021067120100
        # OR_GLM-L2-LCFA_G16_s2021067120120
        # OR_GLM-L2-LCFA_G16_s2021067120140
        # OR_GLM-L2-LCFA_G16_s2021067120200
        # OR_GLM-L2-LCFA_G16_s2021067120220
        # OR_GLM-L2-LCFA_G16_s2021067120240
        # OR_GLM-L2-LCFA_G16_s2021067120300
        # OR_GLM-L2-LCFA_G16_s2021067120320
        # OR_GLM-L2-LCFA_G16_s2021067120340
        # OR_GLM-L2-LCFA_G16_s2021067120400
        # OR_GLM-L2-LCFA_G16_s2021067120420
        # OR_GLM-L2-LCFA_G16_s2021067120440
        # OR_GLM-L2-LCFA_G16_s2021067120500
        # OR_GLM-L2-LCFA_G16_s2021067120520
        # OR_GLM-L2-LCFA_G16_s2021067120540
        # OR_GLM-L2-LCFA_G16_s2021067120600
        # OR_GLM-L2-LCFA_G16_s2021067120620
        # OR_GLM-L2-LCFA_G16_s2021067120640
        # OR_GLM-L2-LCFA_G16_s2021067120700
        # OR_GLM-L2-LCFA_G16_s2021067120720
        # OR_GLM-L2-LCFA_G16_s2021067120740
        # OR_GLM-L2-LCFA_G16_s2021067120800
        # OR_GLM-L2-LCFA_G16_s2021067120820
        # OR_GLM-L2-LCFA_G16_s2021067120840
        # OR_GLM-L2-LCFA_G16_s2021067120900
        # OR_GLM-L2-LCFA_G16_s2021067120920
        # OR_GLM-L2-LCFA_G16_s2021067120940
        # OR_GLM-L2-LCFA_G16_s2021067121000
        # OR_GLM-L2-LCFA_G16_s2021067121020
        # OR_GLM-L2-LCFA_G16_s2021067121040
        # OR_GLM-L2-LCFA_G16_s2021067121100

        # 1-) When "seconds" is "00" I have a full minute
        # 2-) How many past minutes I want to append? 
        # e.g.: 1 mimnute: Every file inside the same "minutes"
        # e.g.: 2 minutes: When "minutes" is 02, or 04, or 06, or 08, or 10
        # e.g.: 5 minutes: When "minutes" is 05 or 10 or 15...
        # e.g.: 10 minutes: When "miutes" is 10 or 20 or 30...

        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        '''
        # Stack and transpose the lat lons
        values = np.vstack((lats, lons)).T

        # Get the counts
        points, counts = np.unique(values, axis=0, return_counts=True)

        # Get the counts indices
        idx = counts.argsort()
        '''
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        '''
        from matplotlib.colors import Normalize 
        from scipy.interpolate import interpn
        
        data , x_e, y_e = np.histogram2d( lons, lats, bins = 20, density = True )
        
        z = interpn( ( 0.5*(x_e[1:] + x_e[:-1]) , 0.5*(y_e[1:]+y_e[:-1]) ) , data , np.vstack([lons,lats]).T , method = "splinef2d", bounds_error = False)
        
        #To be sure to plot all data
        z[np.where(np.isnan(z))] = 0.0
        
        # Sort the points by density, so that the densest points are plotted last        
        idx = z.argsort()
        x, y, z = lons[idx], lats[idx], z[idx]         
        '''
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        
        from scipy.ndimage.filters import gaussian_filter
        
        heatmap, xedges, yedges = np.histogram2d(g_lons, g_lats, bins=2000)
        heatmap = gaussian_filter(heatmap, sigma=2)

        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        heatmap = heatmap.T
        
        #from scipy import ndimage, misc
        #heatmap = ndimage.zoom(heatmap, 2)
        
        heatmap_a = heatmap
        #heatmap_b = heatmap
        #heatmap_a[heatmap < 0.500] = np.nan
        #heatmap_b[heatmap < 0.0001] = np.nan
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        
        from matplotlib.colors import LinearSegmentedColormap
        
        '''
        # get colormap
        ncolors = 256
        color_array = plt.get_cmap('gist_rainbow_r')(range(ncolors))

        #print(color_array.shape)
        # change alpha values
        #color_array[:,-1] = np.linspace(0.0,1.0,ncolors) # Original code
        color_array[0:40,-1] = 0.0
        my_cmap = LinearSegmentedColormap.from_list(name='my_cmap', colors=color_array)
        '''
        
        
        '''
        colors = ["#f9dfff00", "#dcadff", "#a64aff", "#962fff", "#5d00ff", "#2500ff", "#0018ff", "#0f40ff", \
        "#486fff", "#86a3ff", "#c4d7ff", "#ffffff", "#ffffff", "#ffffff", "#ffffff", "#ffffff", "#ffffff"]
        # create a colormap object
        my_cmap = LinearSegmentedColormap.from_list(name='my_cmap', colors=colors)

        colors = ["#f9dfff00", "#dcadff00", "#a64aff00", "#962fff", "#5d00ff", "#2500ff", "#0018ff", "#0f40ff", \
        "#486fff", "#86a3ff", "#c4d7ff", "#ffffff", "#ffffff", "#ffffff", "#ffffff", "#ffffff", "#ffffff"]
        # create a colormap object
        my_cmap2 = LinearSegmentedColormap.from_list(name='my_cmap', colors=colors)
        
        colors = ["#f9dfff00", "#dcadff00", "#a64aff00", "#962fff00", "#5d00ff00", "#2500ff00", "#0018ff00", "#0f40ff", \
        "#486fff", "#86a3ff", "#c4d7ff", "#ffffff", "#ffffff", "#ffffff", "#ffffff", "#ffffff", "#ffffff"]
        # create a colormap object
        my_cmap3 = LinearSegmentedColormap.from_list(name='my_cmap', colors=colors)
        '''
        
        from matplotlib import cm            # Colormap handling utilities
        colors = ["#fbdfff", "#ac53ff", "#6001fd", "#0e00ff", "#0f40fd", "#6a87ff", "#c2d7fd", "#fefefe", \
        "#ffffff"]
        my_colors = cm.colors.LinearSegmentedColormap.from_list("",colors) # Create a custom colormap
        my_colors = my_colors(np.linspace(0, 1, 256))                      # Create the array
        my_colors[0:128,-1] = np.linspace(0.0,1.0, 128)#**2
        my_cmap = LinearSegmentedColormap.from_list(name='my_cmap', colors=my_colors)
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        
        # Read the satellite 
        satellite = getattr(fileGLM, 'platform_ID')

        # Product Name
        product = "GLD20S_FDK" 

        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        '''
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
        #print(path_ch13)

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
        #quit()
        '''
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        '''
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

        # Desired resolution
        resolution = int(sys.argv[6])

        # Read the resolution
        band_resolution_km = getattr(file_ch13, 'spatial_resolution')
        band_resolution_km = float(band_resolution_km[:band_resolution_km.find("km")])

        # Division factor to reduce image size
        f = math.ceil(float(resolution / band_resolution_km))

        # Get the pixel values
        data = file_ch13.variables['CMI'][:,:][::f ,::f] - 273.15
        '''
        # Desired resolution
        resolution = int(sys.argv[6])

        # Create the empty Full Disk array
        shape = (5424 / ((resolution)/2))
        data = np.empty((int(shape),int(shape)))
        data[:] = np.nan

        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Plot configuration
        plot_config = {
        "resolution": resolution, 
        "dpi": 150, 
        "states_color": 'white', "states_width": data.shape[0] * 0.00006, 
        "countries_color": 'white', "countries_width": data.shape[0] * 0.00012,
        "continents_color": 'white', "continents_width": data.shape[0] * 0.00025,
        "grid_color": 'white', "grid_width": data.shape[0] * 0.00025, "grid_interval": 10.0,
        "title_text": "GOES-16 GLM (20s) + BAND-13", "title_size": int(data.shape[1] * 0.005), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[0] - int(data.shape[0] * 0.016), 
        "file_name_id_1": satellite,  "file_name_id_2": product
        }
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Choose the plot size (width x height, in inches)
        fig = plt.figure(figsize=(data.shape[1]/float(plot_config["dpi"]), data.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])
          
        # Define the projection
        proj = ccrs.Geostationary(central_longitude=longitude, satellite_height=h)
        
        img_extent = (-5434894.67527,5434894.67527,-5434894.67527,5434894.67527)

        # Use the Geostationary projection in cartopy
        ax = plt.axes([0, 0, 1, 1], projection=proj)
        #ax.set_extent([-5434894.67527,5434894.67527,-5434894.67527,5434894.67527], proj)
        #---------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------- 
        # Background color
        import cartopy.feature as cfeature
        land = ax.add_feature(cfeature.LAND, facecolor='black', zorder=1)
        ocean = ax.add_feature(cfeature.OCEAN, facecolor='black', zorder=2)

        # Plotting the empty full disk
        img1 = ax.imshow(data, vmin=-80, vmax=40, cmap='Greys', alpha = 0.50, extent=img_extent, zorder=3) 

        # Get the events lats and lons
        #e_lats = fileGLM.variables['event_lat'][:]
        #e_lons = fileGLM.variables['event_lon'][:]
        # Get the groups lats and lons
        #g_lats = fileGLM.variables['group_lat'][:]
        #g_lons = fileGLM.variables['group_lon'][:]
        # Get the flashes lats and lons
        #f_lats = fileGLM.variables['flash_lat'][:]
        #f_lons = fileGLM.variables['flash_lon'][:]

        # Plotting events, groups and flashes
        #img2 = ax.plot(e_lons,e_lats, 'o', markersize=2.5, color='#fffb8a', alpha = 0.01, transform=ccrs.PlateCarree(), zorder=4)
        #img3 = ax.plot(g_lons,g_lats, 'o', markersize=2.5, color='#fffdc7', alpha = 0.02, transform=ccrs.PlateCarree(), zorder=5)
        #img4 = ax.plot(f_lons,f_lats, 'o', markersize=2.5, color='#fff700', alpha = 0.20, transform=ccrs.PlateCarree(), zorder=6)
        # Plot the GLM Data
        #glm = plt.scatter(points[idx,1], points[idx,0], vmin=0, vmax=250, s=counts[idx]*0.1, c=counts[idx], cmap="jet",  transform=ccrs.PlateCarree(), zorder=4)
        #glm = plt.scatter(x, y, c=z, cmap="jet",  transform=ccrs.PlateCarree(), zorder=4)
        
        #glm = ax.imshow(heatmap_b, vmin=0, vmax=3, interpolation='bilinear', extent=extent, origin='lower', cmap="jet", transform=ccrs.PlateCarree(), alpha = 0.50, zorder=4)
        
        #glm = ax.imshow(heatmap_a, vmin=0, vmax=5, interpolation='bilinear', extent=extent, origin='lower', cmap=my_cmap, transform=ccrs.PlateCarree(), alpha = 0.10, zorder=5)
        #glm = ax.imshow(heatmap_a, vmin=0, vmax=5, interpolation='bilinear', extent=extent, origin='lower', cmap=my_cmap2, transform=ccrs.PlateCarree(), alpha = 0.30, zorder=6)
        #glm = ax.imshow(heatmap_a, vmin=0, vmax=5, interpolation='bilinear', extent=extent, origin='lower', cmap=my_cmap3, transform=ccrs.PlateCarree(), alpha = 1.00, zorder=7)

        glm = ax.imshow(heatmap_a, vmin=0, vmax=20, interpolation='bilinear', extent=extent, origin='lower', cmap=my_cmap, transform=ccrs.PlateCarree(), alpha = 1.00, zorder=5)
        # events: max: 6 # group: max: 3
        img2 = ax.plot(g_lons,g_lats, 'o', markersize=1.0, color='#ffffff', alpha = 0.05, transform=ccrs.PlateCarree(), zorder=8)
        
        #img3 = ax.plot(g_lons,g_lats, 'o', markersize=1.0, color='#ffffff', alpha = 0.02, transform=ccrs.PlateCarree(), zorder=8)
        #img4 = ax.plot(f_lons,f_lats, 'o', markersize=1.0, color='#ffffff', alpha = 0.20, transform=ccrs.PlateCarree(), zorder=9)

        #---------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------
        # Add states and provinces
        shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=10)

        # Add coastlines and borders
        ax.coastlines(resolution='50m', color=plot_config["countries_color"], linewidth=plot_config["countries_width"], zorder=11)
        ax.add_feature(cartopy.feature.BORDERS, edgecolor=plot_config["continents_color"], linewidth=plot_config["continents_width"], zorder=12)

        # Add countries
        #shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
        #ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=8)

        # Add continents
        #shapefile = list(shpreader.Reader(main_dir + '//Shapefiles//ne_10m_coastline.shp').geometries())
        #ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=9)
          
        # Add gridlines
        ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=False, zorder=13)

        # Remove the outline border
        ax.outline_patch.set_visible(False)

        # Add a title
        plt.annotate(plot_config["title_text"] + " " + date_formated , xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=14)

        plt.show()
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Add labels to specific coordinates
        '''
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
            ax.plot(xpt, ypt, str(mtype), color=str(mcolor), markersize=int(msize), transform=ccrs.Geodetic(), markeredgewidth=1.0, markeredgecolor=(0, 0, 0, 1), zorder=10)
            txt = ax.text(xpt+x_offset , ypt+y_offset, label, fontsize=int(size), fontweight='bold', color=str(col), transform=ccrs.Geodetic(), zorder=11)
            txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='black')])
        '''
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------

        # Add logos / images to the plot
        my_logo = plt.imread(main_dir + '//Logos//my_logo.png')
        newax = fig.add_axes([0.01, 0.03, 0.10, 0.10], anchor='SW', zorder=15) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
        newax.imshow(my_logo)
        newax.axis('off')

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

        #---------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------
        # Put the processed file on the log
        '''
        import datetime # Basic Date and Time types
        with open(main_dir + '//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
         log.write(str(datetime.datetime.now()))
         log.write('\n')
         log.write(path + '\n')
         log.write('\n')
        '''
        #---------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------
        print('Total processing time:', round((t.time() - start),2), 'seconds.') 
