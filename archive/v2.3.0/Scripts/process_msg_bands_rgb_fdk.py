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
from netCDF4 import Dataset                                  # Read / Write NetCDF4 files
from mpl_toolkits.axes_grid1.inset_locator import inset_axes # Add a child inset axes to this existing axes.
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
from cpt_convert import loadCPT                              # Import the CPT convert function
from matplotlib.colors import LinearSegmentedColormap        # Linear interpolation for color maps
import matplotlib.pyplot as plt                              # Plotting library
import matplotlib.colors                                     # Matplotlib colors
from matplotlib.image import imread                          # Read an image from a file into an array
import numpy as np                                           # Scientific computing with Python
import cartopy, cartopy.crs as ccrs                          # Plot maps
import cartopy.io.shapereader as shpreader                   # Import shapefiles
import time as t                                             # Time access and conversion
from osgeo import gdal, osr, ogr                             # Import GDAL
import os                                                    # Miscellaneous operating system interfaces
from os.path import dirname, abspath                         # Return a normalized absolutized version of the pathname path 
import sys                                                   # Import the "system specific parameters and functions" module
from html_update import update                               # Update the HTML animation 
from glob import glob                                        # Unix style pathname pattern expansion
import pyproj                                                # Python interface to PROJ (cartographic projections and coordinate transformations library)
import math                                                  # Mathematical functions
import re                                                    # Regular expression operations 
import platform                                              # Access to underlying platform’s identifying data
from pathlib import Path                                     # Object-oriented filesystem paths
from tempfile import gettempdir                              # Generate temporary files and directories
from satpy.scene import Scene                                # Python package for earth-observing satellite data processing
from satpy import find_files_and_readers                     # Python package for earth-observing satellite data processing
from satpy.writers import get_enhanced_image                 # Python package for earth-observing satellite data processing
from satpy.writers import geotiff                            # Python package for earth-observing satellite data processing 
#from satpy.utils import debug_on                            # Python package for earth-observing satellite data processing
#debug_on()                                                  # Python package for earth-observing satellite data processing
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()

# SHOWCast directory:
main_dir = dirname(dirname(abspath(__file__)))

# set PPP_CONFIG_DIR for custom composites 
os.environ['PPP_CONFIG_DIR'] = main_dir + "Miniconda3//envs//showcast//Lib//site-packages//satpy"
os.environ['SATPY_ANCPATH'] = main_dir + "Miniconda3//envs//showcast//Lib//site-packages//satpy//backgrounds"

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------	
# Select the data you want to process
composites = []

VIS006 = True
VIS008 = True
IR_016 = True
IR_039 = True
WV_062 = True
WV_073 = True
IR_087 = True
IR_097 = True
IR_108 = True
IR_120 = True
IR_134 = True
HRV = True
airmass = True
ash = True
cloudtop = True
convection = True
day_microphysics = True
dust = True
fog = True
ir_overview = True
natural_with_night_fog = True
night_fog = True
overview = True
snow = True

if (VIS006 == True): composites.append('VIS006')
if (VIS008 == True): composites.append('VIS008')
if (IR_016 == True): composites.append('IR_016')
if (IR_039 == True): composites.append('IR_039')
if (WV_062 == True): composites.append('WV_062')
if (WV_073 == True): composites.append('WV_073')
if (IR_087 == True): composites.append('IR_087')
if (IR_097 == True): composites.append('IR_097')
if (IR_108 == True): composites.append('IR_108')
if (IR_120 == True): composites.append('IR_120')
if (IR_134 == True): composites.append('IR_134')
if (HRV == True): composites.append('HRV')
if (airmass == True): composites.append('airmass')
if (ash == True): composites.append('ash')
if (cloudtop == True): composites.append('cloudtop')
if (convection == True): composites.append('convection')
if (day_microphysics == True): composites.append('day_microphysics')
if (dust == True): composites.append('dust')
if (fog == True): composites.append('fog')
if (ir_overview == True): composites.append('ir_overview')
if (natural_with_night_fog == True): composites.append('natural_with_night_fog')
if (night_fog == True): composites.append('night_fog')
if (overview == True): composites.append('overview')
if (snow == True): composites.append('snow')
#print (composites)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------	

# Delete the decompressed files from the tmp dir
XRIT_DECOMPRESS_OUTDIR = gettempdir() + '//'

decompress_files = glob(XRIT_DECOMPRESS_OUTDIR + '*000*MSG*')

for f in decompress_files:
    os.remove(f)
    
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
    
def LatLon_To_XY(Lat,Lon):
    return P(Lat,Lon)   

def procMSG(data,product,type):
    
    print('Processing ' + product + '...')
    
    # Satellite name
    satellite = 'MSG'
  
    # Read the product name
    title = "METEOSAT" + " " + product + " " + year + "-" + month + "-" + day + " " + hour + ":" + minutes + " " + "UTC"
    #--------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------
    
    # Plot the image
    if (type == 'RGB'):
        #--------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------
        product = product + "_FDK"
        # Plot configuration
        plot_config = {
        "resolution": 8, 
        "dpi": 150, 
        "states_color": 'white', "states_width": data.shape[0] * 0.00006, 
        "countries_color": 'white', "countries_width": data.shape[0] * 0.00012,
        "continents_color": 'white', "continents_width": data.shape[0] * 0.00025,
        "grid_color": 'white', "grid_width": data.shape[0] * 0.00025, "grid_interval": 10.0,
        "title_text": title, "title_size": int(data.shape[0] * 0.005), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[0] - int(data.shape[0] * 0.016), 
        "file_name_id_1": "MSG",  "file_name_id_2": product 
        }
        #--------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------
        # Choose the plot size (width x height, in inches)
        fig = plt.figure(figsize=(data.shape[1]/float(plot_config["dpi"]), data.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])
  
        # Define the projection
        proj = ccrs.Geostationary(central_longitude=0.0, satellite_height=35786023)
        img_extent = (-5568748.27576, 5568748.27576, -5568748.27576, 5568748.27576)

        # Use the Geostationary projection in cartopy
        ax = plt.axes([0, 0, 1, 1], projection=proj)
        
        # Plot the image
        img = ax.imshow(data, origin='upper', extent=img_extent, zorder=3)
  
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
        plt.annotate(plot_config["title_text"], xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=8)
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Add labels to specific coordinates

        import configparser
        conf = configparser.ConfigParser()
        conf.read(main_dir + '//Utils//Labels//labels_msg.ini')

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

    else:
        # Converts a CPT file to be used in Python
        if (product == 'VIS006') or (product == 'VIS008') or (product == 'NIR016') or (product == 'HRVCHN'):
            cpt = loadCPT(main_dir + '//Colortables//Square Root Visible Enhancement.cpt')
            cmap = LinearSegmentedColormap('cpt', cpt)
            vmin = 0.0
            vmax = 1.0
            thick_interval = 0.1
        if (product == 'IRD039'):
            cpt = loadCPT(main_dir + '//Colortables//SVGAIR2_TEMP.cpt')
            cmap = LinearSegmentedColormap('cpt', cpt)
            data -= 273.15
            vmin = -112.15
            vmax = 56.85
            thick_interval = 10.0 
        if (product == 'WVP062') or (product == 'WVP073'):
            cpt = loadCPT(main_dir + '//Colortables//SVGAWVX_TEMP.cpt')
            cmap = LinearSegmentedColormap('cpt', cpt)
            data -= 273.15
            vmin = -112.15
            vmax = 56.85
            thick_interval = 10.0
        if (product == 'IRD087') or (product == 'IRD097') or (product == 'IRD108') or (product == 'IRD120') or (product == 'IRD134'):
            cpt = loadCPT(main_dir + '//Colortables//IR4AVHRR6.cpt')
            cmap = LinearSegmentedColormap('cpt', cpt)
            data -= 273.15    
            vmin = -103.0
            vmax = 84.0
            thick_interval = 10.0  
    
        #--------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------      
        product = product + "_FDK"
        # Plot configuration
        plot_config = {
        "resolution": 8, 
        "dpi": 150, 
        "states_color": 'white', "states_width": data.shape[0] * 0.00006, 
        "countries_color": 'cyan', "countries_width": data.shape[0] * 0.00012,
        "continents_color": 'cyan', "continents_width": data.shape[0] * 0.00025,
        "grid_color": 'white', "grid_width": data.shape[0] * 0.00025, "grid_interval": 10.0,
        "vmin": vmin, "vmax": vmax, "cmap": cmap,
        "title_text": title, "title_size": int(data.shape[0] * 0.005), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[0] - int(data.shape[0] * 0.016), 
        "thick_interval": thick_interval, "cbar_labelsize": int(data.shape[0] * 0.005), "cbar_labelpad": -int(data.shape[0] * 0.0),
        "file_name_id_1": "MSG",  "file_name_id_2": product 
        }
        #--------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------
        # Choose the plot size (width x height, in inches)
        fig = plt.figure(figsize=(data.shape[1]/float(plot_config["dpi"]), data.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])
  
        # Define the projection
        proj = ccrs.Geostationary(central_longitude=0.0, satellite_height=35786023)
        img_extent = (-5568748.27576, 5568748.27576, -5568748.27576, 5568748.27576)

        # Use the Geostationary projection in cartopy
        ax = plt.axes([0, 0, 1, 1], projection=proj)
    
        # Add background image if HRV
        if (product == 'HRVCHN_FDK'):
            #ax.stock_img()
            fname = os.path.join(main_dir + '//Maps//', 'land_ocean_ice_8192.jpg')
            ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)
            #date = datetime(int(year), int(month), int(day), int(hour))
            #ax.add_feature(Nightshade(date, alpha=0.7), zorder=2)
    
        # Plot the image
        img = ax.imshow(data, vmin=plot_config["vmin"], vmax=plot_config["vmax"], origin='upper', extent=img_extent, cmap=plot_config["cmap"], zorder=3)

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
        plt.annotate(plot_config["title_text"], xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=8)

        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Add labels to specific coordinates

        import configparser
        conf = configparser.ConfigParser()
        conf.read(main_dir + '//Utils//Labels//labels_msg.ini')

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

    # Create the satellite output directory if it doesn't exist
    out_dir = main_dir + '//Output//' + satellite
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    # Create the product output directory if it doesn't exist
    out_dir = main_dir + '//Output//' + satellite + '//' + product + '//'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
   
    # Save the image
    plt.savefig(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + time_date + '.png', facecolor='black')#, bbox_inches='tight', pad_inches=0, facecolor='black')

    # Update the animation
    nfiles = 20
    update(satellite, product, nfiles)
    
    #---------------------------------------------------------------------------------------------    
    #---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------	
# Get the script and SHOWCast directories  
script_path = Path(os.path.abspath(__file__))
showcast_path = (script_path.parent).parent
   
# Get the OS
osystem = platform.system()

# Get the XRIT_DECOMPRESS_PATH
if osystem == "Windows":
    XRIT_DECOMPRESS_PATH = str(showcast_path) + '//Utils//xRITDecompress_x64//xRITDecompress.exe'
else:
    XRIT_DECOMPRESS_PATH = str(showcast_path) + '//Utils//xRITDecompress_x64//xRITDecompress'

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------	

# Maximum extent for MSG-0degree	
extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]

# File to be processed
path = str(sys.argv[1])

# Desired resolution
resolution = int(sys.argv[6])

# Read the resolution
band_resolution_km = 3

# Division factor to reduce image size
f = math.ceil(float(resolution / band_resolution_km))

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
 
result = re.search('________-_________-EPI______-(.*)-__', path)
path2 = re.sub('H-000*(.*)', '', path)

# Read the time and date
time_date = str(result.group(1))
year = time_date[0:4]
month = time_date[4:6]
day = time_date[6:8]
hour = time_date[8:10]
minutes = time_date[10:12]

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------	

# Path to XRIT_DECOMPRESS library
os.environ['XRIT_DECOMPRESS_PATH'] = XRIT_DECOMPRESS_PATH

# Create the global scene
global_scene = Scene(reader='seviri_l1b_hrit',filenames=glob(path2 + '*' + time_date + '*'))

# Load the global scene
global_scene.load(composites)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------	

if (VIS006 == True):
    variable = 'VIS006'
    product = 'VIS006'
    type = 'BAND'
    data = global_scene[variable] / 100
    data = data[:,:][::f ,::f ]
    data = np.flipud(data)
    data = np.fliplr(data)
    # Call the plotting function
    procMSG(data, product, type)
    
if (VIS008 == True):
    variable = 'VIS008'
    product = 'VIS008'
    type = 'BAND'
    data = global_scene[variable] / 100
    data = data[:,:][::f ,::f ]
    data = np.flipud(data)
    data = np.fliplr(data)
    # Call the plotting function
    procMSG(data, product, type)
    
if (IR_016 == True):	
    variable = 'IR_016'
    product = 'NIR016'
    type = 'BAND'
    data = global_scene[variable] / 100
    data = data[:,:][::f ,::f ]
    data = np.flipud(data)
    data = np.fliplr(data)
    # Call the plotting function
    procMSG(data, product, type)

if (IR_039 == True):
    variable = 'IR_039' 
    product = 'IRD039' 
    type = 'BAND'
    data = global_scene[variable]
    data = data[:,:][::f ,::f ]
    data = np.flipud(data)
    data = np.fliplr(data)
    # Call the plotting function
    procMSG(data, product, type)
    
if (WV_062 == True):	
    variable = 'WV_062'
    product = 'WVP062'
    type = 'BAND'
    data = global_scene[variable]
    data = data[:,:][::f ,::f ]
    data = np.flipud(data)
    data = np.fliplr(data)
    # Call the plotting function
    procMSG(data, product, type)

if (WV_073 == True):	
    variable = 'WV_073'
    product = 'WVP073'
    type = 'BAND'
    data = global_scene[variable]
    data = data[:,:][::f ,::f ]
    data = np.flipud(data)
    data = np.fliplr(data)
    # Call the plotting function
    procMSG(data, product, type)

if (IR_087 == True):	
    variable = 'IR_087'
    product = 'IRD087'
    type = 'BAND'
    data = global_scene[variable]
    data = data[:,:][::f ,::f ]
    data = np.flipud(data)
    data = np.fliplr(data)
    # Call the plotting function
    procMSG(data, product, type)

if (IR_097 == True):	
    variable = 'IR_097'
    product = 'IRD097'
    type = 'BAND'
    data = global_scene[variable]
    data = data[:,:][::f ,::f ]
    data = np.flipud(data)
    data = np.fliplr(data)
    # Call the plotting function
    procMSG(data, product, type)

if (IR_108 == True):	
    variable = 'IR_108'
    product = 'IRD108'
    type = 'BAND'
    data = global_scene[variable]
    data = data[:,:][::f ,::f ]
    data = np.flipud(data)
    data = np.fliplr(data)
    # Call the plotting function
    procMSG(data, product, type)

if (IR_120 == True):	
    variable = 'IR_120'
    product = 'IRD120'
    type = 'BAND'
    data = global_scene[variable]
    data = data[:,:][::f ,::f ]
    data = np.flipud(data)
    data = np.fliplr(data)
    # Call the plotting function
    procMSG(data, product, type)

if (IR_134 == True):	
    variable = 'IR_134'
    product = 'IRD134'
    type = 'BAND'
    data = global_scene[variable]
    data = data[:,:][::f ,::f ]
    data = np.flipud(data)
    data = np.fliplr(data)
    # Call the plotting function
    procMSG(data, product, type)

if (HRV == True):	
    variable = 'HRV'
    product = 'HRVCHN'
    type = 'BAND'
    data = global_scene[variable] / 100
    data = data[:,:][::f ,::f ]
    data = np.flipud(data)
    data = np.fliplr(data)
    # Call the plotting function
    procMSG(data, product, type)
	
if (airmass == True):	
    variable = 'airmass'
    product = 'ARMRGB'
    type = 'RGB'
    data = get_enhanced_image(global_scene[variable])
    data = data.finalize(fill_value=None)[0]
    #print(data.shape)
    R = (data[0,:,:][::f ,::f])
    R = np.flipud(R)
    R = np.fliplr(R)  
    G = (data[1,:,:][::f ,::f])
    G = np.flipud(G)
    G = np.fliplr(G)    
    B = (data[2,:,:][::f ,::f])
    B = np.flipud(B)
    B = np.fliplr(B)            
    # Create the RGB
    data = np.stack([R, G, B], axis=2)
    # Call the plotting function
    procMSG(data, product, type)
    
if (ash == True):		
    variable ='ash'
    product = 'ASHRGB'
    type = 'RGB'
    data = get_enhanced_image(global_scene[variable])
    data = data.finalize(fill_value=None)[0]
    #print(data.shape)
    R = (data[0,:,:][::f ,::f])
    R = np.flipud(R)
    R = np.fliplr(R)  
    G = (data[1,:,:][::f ,::f])
    G = np.flipud(G)
    G = np.fliplr(G)    
    B = (data[2,:,:][::f ,::f])
    B = np.flipud(B)
    B = np.fliplr(B)            
    # Create the RGB
    data = np.stack([R, G, B], axis=2)
    # Call the plotting function
    procMSG(data, product, type)

if (cloudtop == True):	
    variable ='cloudtop'
    product = 'TOPRGB'
    type = 'RGB'
    data = get_enhanced_image(global_scene[variable])
    data = data.finalize(fill_value=None)[0]
    #print(data.shape)
    R = (data[0,:,:][::f ,::f])
    R = np.flipud(R)
    R = np.fliplr(R)  
    G = (data[1,:,:][::f ,::f])
    G = np.flipud(G)
    G = np.fliplr(G)    
    B = (data[2,:,:][::f ,::f])
    B = np.flipud(B)
    B = np.fliplr(B)            
    # Create the RGB
    data = np.stack([R, G, B], axis=2)
    # Call the plotting function
    procMSG(data, product, type)

if (convection == True):		
    variable = 'convection'
    product = 'CONRGB'
    type = 'RGB'
    data = get_enhanced_image(global_scene[variable]) 
    data = data.finalize(fill_value=None)[0]
    #print(data.shape)
    R = (data[0,:,:][::f ,::f])
    R = np.flipud(R)
    R = np.fliplr(R)  
    G = (data[1,:,:][::f ,::f])
    G = np.flipud(G)
    G = np.fliplr(G)    
    B = (data[2,:,:][::f ,::f])
    B = np.flipud(B)
    B = np.fliplr(B)            
    # Create the RGB
    data = np.stack([R, G, B], axis=2)
    # Call the plotting function
    procMSG(data, product, type)

if (natural_with_night_fog == True):
    variable = 'natural_with_night_fog'
    product = 'DLCRGB'	
    type = 'RGB'
    data = get_enhanced_image(global_scene[variable]) 
    data = data.finalize(fill_value=None)[0]
    #print(data.shape)
    R = (data[0,:,:][::f ,::f])
    R = np.flipud(R)
    R = np.fliplr(R)  
    G = (data[1,:,:][::f ,::f])
    G = np.flipud(G)
    G = np.fliplr(G)    
    B = (data[2,:,:][::f ,::f])
    B = np.flipud(B)
    B = np.fliplr(B)            
    # Create the RGB
    data = np.stack([R, G, B], axis=2)
    # Call the plotting function
    procMSG(data, product, type)
    
if (day_microphysics == True):	
    variable = 'day_microphysics'
    product = 'DMPRGB'
    type = 'RGB'
    data = get_enhanced_image(global_scene[variable]) 
    data = data.finalize(fill_value=None)[0]
    #print(data.shape)
    R = (data[0,:,:][::f ,::f])
    R = np.flipud(R)
    R = np.fliplr(R)  
    G = (data[1,:,:][::f ,::f])
    G = np.flipud(G)
    G = np.fliplr(G)    
    B = (data[2,:,:][::f ,::f])
    B = np.flipud(B)
    B = np.fliplr(B)            
    # Create the RGB
    data = np.stack([R, G, B], axis=2)
    # Call the plotting function
    procMSG(data, product, type)
	
if (dust == True):
    variable = 'dust'
    product = 'DSTRGB'
    type = 'RGB'
    data = get_enhanced_image(global_scene[variable]) 
    data = data.finalize(fill_value=None)[0]
    #print(data.shape)
    R = (data[0,:,:][::f ,::f])
    R = np.flipud(R)
    R = np.fliplr(R)  
    G = (data[1,:,:][::f ,::f])
    G = np.flipud(G)
    G = np.fliplr(G)    
    B = (data[2,:,:][::f ,::f])
    B = np.flipud(B)
    B = np.fliplr(B)            
    # Create the RGB
    data = np.stack([R, G, B], axis=2)
    # Call the plotting function
    procMSG(data, product, type)

if (fog == True):
    variable = 'fog'
    product = 'FOGRGB'	
    type = 'RGB'
    data = get_enhanced_image(global_scene[variable]) 
    data = data.finalize(fill_value=None)[0]
    #print(data.shape)
    R = (data[0,:,:][::f ,::f])
    R = np.flipud(R)
    R = np.fliplr(R)  
    G = (data[1,:,:][::f ,::f])
    G = np.flipud(G)
    G = np.fliplr(G)    
    B = (data[2,:,:][::f ,::f])
    B = np.flipud(B)
    B = np.fliplr(B)            
    # Create the RGB
    data = np.stack([R, G, B], axis=2)
    # Call the plotting function
    procMSG(data, product, type)

if (ir_overview == True):	
    variable = 'ir_overview'
    product = 'IRORGB'		
    type = 'RGB'
    data = get_enhanced_image(global_scene[variable]) 
    data = data.finalize(fill_value=None)[0]
    #print(data.shape)
    R = (data[0,:,:][::f ,::f])
    R = np.flipud(R)
    R = np.fliplr(R)  
    G = (data[1,:,:][::f ,::f])
    G = np.flipud(G)
    G = np.fliplr(G)    
    B = (data[2,:,:][::f ,::f])
    B = np.flipud(B)
    B = np.fliplr(B)            
    # Create the RGB
    data = np.stack([R, G, B], axis=2)
    # Call the plotting function
    procMSG(data, product, type)
	
if (night_fog == True):	
    variable = 'night_fog'
    product = 'NFORGB'	
    type = 'RGB'
    data = get_enhanced_image(global_scene[variable]) 
    data = data.finalize(fill_value=None)[0]
    #print(data.shape)
    R = (data[0,:,:][::f ,::f])
    R = np.flipud(R)
    R = np.fliplr(R)  
    G = (data[1,:,:][::f ,::f])
    G = np.flipud(G)
    G = np.fliplr(G)    
    B = (data[2,:,:][::f ,::f])
    B = np.flipud(B)
    B = np.fliplr(B)            
    # Create the RGB
    data = np.stack([R, G, B], axis=2)
    # Call the plotting function
    procMSG(data, product, type)

if (overview == True):
    variable = 'overview'
    product = 'OVWRGB'	
    type = 'RGB'
    data = get_enhanced_image(global_scene[variable]) 
    data = data.finalize(fill_value=None)[0]
    #print(data.shape)
    R = (data[0,:,:][::f ,::f])
    R = np.flipud(R)
    R = np.fliplr(R)  
    G = (data[1,:,:][::f ,::f])
    G = np.flipud(G)
    G = np.fliplr(G)    
    B = (data[2,:,:][::f ,::f])
    B = np.flipud(B)
    B = np.fliplr(B)            
    # Create the RGB
    data = np.stack([R, G, B], axis=2)
    # Call the plotting function
    procMSG(data, product, type)
	
if (snow == True):
    variable = 'snow'
    product = 'SNWRGB'			
    type = 'RGB'
    data = get_enhanced_image(global_scene[variable]) 
    data = data.finalize(fill_value=None)[0]
    #print(data.shape)
    R = (data[0,:,:][::f ,::f])
    R = np.flipud(R)
    R = np.fliplr(R)  
    G = (data[1,:,:][::f ,::f])
    G = np.flipud(G)
    G = np.fliplr(G)    
    B = (data[2,:,:][::f ,::f])
    B = np.flipud(B)
    B = np.fliplr(B)            
    # Create the RGB
    data = np.stack([R, G, B], axis=2)
    # Call the plotting function
    procMSG(data, product, type)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------	
print('Total processing time:', round((t.time() - start),2), 'seconds.') 
