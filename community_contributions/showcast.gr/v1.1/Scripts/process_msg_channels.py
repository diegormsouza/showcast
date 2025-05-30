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
# If not, see http://www.gnu.org/licenses/.# Modified for the needs of HNMS by RMC/LARISSA
# Using MET Satellites
# Last Update: Sep 2020
#######################################################################################################
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Required modules
#--------------------------------
#to run in a pure text terminal:
import matplotlib
matplotlib.use('Agg')
#--------------------------------
from PIL import Image
import threading
from mpl_toolkits.axes_grid1.inset_locator import inset_axes # Add a child inset axes to this existing axes.
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
import datetime                                              # Basic Date and Time types
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
import sys                                                   # Import the "system specific parameters and functions" module
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

# Get Satellite name from config
satellite = str(sys.argv[7])

# Get sectors list  from config
sectors = str(sys.argv[8]).strip(",").split(",")
print("sectors to produce: ",sectors)

# Start the time counter
print(satellite +  ' Script started.\n')
start = t.time()
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Select the data you want to process
composites = []
bands_list = []
rgbs_list  = []

# individual channels
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
# RGB channels
airmass = True
ash = True
cloudtop = True
convection = True
day_microphysics = True
dust = True
fog = True
ir_overview = False
ir_cloud_day = False
ir_sandwich = False
ir108_3d = False
natural_color = False
night_fog =True
overview = False
snow = True
natural_with_night_fog = True
hrv_fog = True
hrv_clouds = True
natural_enh_sun = False
realistic_colors = False
hrv_severe_storms_masked = False
hrv_severe_storms = False
vis_sharpened_ir = False

# if true add individual channel to bands_list array
if (VIS006 == True): bands_list.append('VIS006')
if (VIS008 == True): bands_list.append('VIS008')
if (IR_016 == True): bands_list.append('IR_016')
if (IR_039 == True): bands_list.append('IR_039')
if (WV_062 == True): bands_list.append('WV_062')
if (WV_073 == True): bands_list.append('WV_073')
if (IR_087 == True): bands_list.append('IR_087')
if (IR_097 == True): bands_list.append('IR_097')
if (IR_108 == True): bands_list.append('IR_108')
if (IR_120 == True): bands_list.append('IR_120')
if (IR_134 == True): bands_list.append('IR_134')
if (HRV == True)   : bands_list.append('HRV')

# if true add RGB  channel to rgbs_list array
if (airmass == True)                 : rgbs_list.append('airmass')
if (ash == True)                     : rgbs_list.append('ash')
if (cloudtop == True)                : rgbs_list.append('cloudtop')
if (convection == True)              : rgbs_list.append('convection')
if (day_microphysics == True)        : rgbs_list.append('day_microphysics')
if (dust == True)                    : rgbs_list.append('dust')
if (fog == True)                     : rgbs_list.append('fog')
if (ir_overview == True)             : rgbs_list.append('ir_overview')
if (ir_cloud_day == True)            : rgbs_list.append('ir_cloud_day')
if (ir_sandwich == True)             : rgbs_list.append('ir_sandwich')
if (ir108_3d == True)                : rgbs_list.append('ir108_3d')
if (natural_color == True)           : rgbs_list.append('natural_color')
if (night_fog == True)               : rgbs_list.append('night_fog')
if (overview == True)                : rgbs_list.append('overview')
if (snow == True)                    : rgbs_list.append('snow')
if (natural_with_night_fog == True)  : rgbs_list.append('natural_with_night_fog')
if (hrv_fog == True)                 : rgbs_list.append('hrv_fog')
if (hrv_clouds == True)              : rgbs_list.append('hrv_clouds')
if (natural_enh_sun == True)         : rgbs_list.append('natural_enh_sun')
if (realistic_colors == True)        : rgbs_list.append('realistic_colors')
if (hrv_severe_storms_masked == True): rgbs_list.append('hrv_severe_storms_masked')
if (vis_sharpened_ir == True)        : rgbs_list.append('vis_sharpened_ir')

# composite is the array with the summary of products. Individual plus RGB
composites = bands_list + rgbs_list
#print (composites)

# HRV RGB composites need resampling for FDK
hrv_rgb_list=['hrv_fog','hrv_clouds','hrv_severe_storms_masked','vis_sharpened_ir','hrv_severe_storms']
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Delete previous decompressed files from current working satellite. If not may cause conflict to data arrays
# "satellite" : "file identifier"
sats_dict={"MSG":"*-MSG?___*","MSG_IODC":"*_IODC_*","MSG_RSS":"*_RSS_*"}

# xritDecompress uses by default the system tmp directory. gettempdir() returns tmp directory
XRIT_DECOMPRESS_OUTDIR = gettempdir() + '//'
decompress_files = glob(XRIT_DECOMPRESS_OUTDIR + sats_dict[satellite])
for f in decompress_files:
    os.remove(f)
print(XRIT_DECOMPRESS_OUTDIR + " got cleared for " + satellite + " satellite")

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

def LatLon_To_XY(Lat,Lon):
    return P(Lat,Lon)

def procMSG(data,product,comp,type,sector_name,extent,time_date=""):

    print('Processing image ' + satellite +(9-len(satellite)) * " " +   product + sector_name + " " + time_date)
#    print("os environ outdir:",os.environ['XRIT_DECOMPRESS_OUTDIR'])
    # Read the product name
    title = satellite + " " + product + " " + year + "-" + month + "-" + day + " " + hour + ":" + minutes + " " + "UTC"
    #--------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------

    # Plot the image
    if (type == 'RGB'):
        #--------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------
        # Plot configuration
        plot_config = {
        "resolution": 8,
        "dpi": 150,
        "states_color": 'white', "states_width": data.shape[0] * 0.00000,
        "countries_color": 'white', "countries_width": data.shape[0] * 0.00012,
        "continents_color": 'white', "continents_width": data.shape[0] * 0.00011,
        "fir_color": 'orange', "fir_width": data.shape[0] * 0.00011,
        "grid_color": 'white', "grid_width": data.shape[0] * 0.00025, "grid_interval": 10.0,
        "title_text": title, "title_size": int(data.shape[0] * 0.008), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[0] - int(data.shape[0] * 0.025),
        "file_name_id_1": satellite,  "file_name_id_2": product + sector_name
        }
        #--------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------
        # Choose the plot size (width x height, in inches)
        fig = plt.figure(figsize=(data.shape[1]/float(plot_config["dpi"]), data.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])

        if sector_name == "_FDK":
             # Define the projection
            if satellite=="MSG_IODC":
                proj = ccrs.Geostationary(central_longitude=41.5, satellite_height=35786023)
            elif satellite=="MSG_RSS":
                proj = ccrs.Geostationary(central_longitude=9.5, satellite_height=35786023)
            else:
                proj = ccrs.Geostationary(central_longitude=0.0, satellite_height=35786023)
            img_extent = (-5568748.27576, 5568748.27576, -5568748.27576, 5568748.27576)

            # Use the Geostationary projection in cartopy
            ax = plt.axes([0, 0, 1, 1], projection=proj)

            # Add background map image if HRV
            if comp in hrv_rgb_list:
                fname = os.path.join('..//Maps//', 'land_ocean_ice_8192.jpg')
                ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)
                 # Plot the image . using alpha for showing background map
                img = ax.imshow(data, origin='upper', alpha=0.7, extent=img_extent, zorder=3)
            else:
                 # Plot the image
                img = ax.imshow(data, origin='upper', extent=img_extent, zorder=3)

        else:
            # Define the projection
            proj = ccrs.PlateCarree()

            # Use the PlateCarree projection in cartopy
            ax = plt.axes([0, 0, 1, 1], projection=proj)
            ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

            # Define the image extent
            img_extent = [extent[0], extent[2], extent[1], extent[3]]

            # Plot the image
            img = ax.imshow(data, origin='upper', extent=img_extent, zorder=3)

        # Add states and provinces
        shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=4)

        # Add countries
        shapefile = list(shpreader.Reader('..//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=5)

        # Add continents
#        shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_coastline.shp').geometries())
#        shapefile = list(shpreader.Reader('../Shapefiles/GRC_admin/GRC_adm2.shp').geometries())
        shapefile = list(shpreader.Reader('../Shapefiles/gis_osm_places_a_free_1.shp').geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=6)

        # Add Athens FIR
        shapefile = list(shpreader.Reader('../Shapefiles/FIR_ATH/FIR_Athens.shp').geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["fir_color"],facecolor='none', linewidth=plot_config["fir_width"], zorder=7)

        # Add coastlines, borders and gridlines
#        ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=False, zorder=8)

        # Remove the outline border
        ax.outline_patch.set_visible(False)

        # Add a title
        plt.annotate(plot_config["title_text"], xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=9)

        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Add labels to specific coordinates

        #import configparser
        #conf = configparser.ConfigParser()
        #conf.read('..//Utils//Labels//labels_msg.ini')

        #labels, city_lons, city_lats, x_offsets, y_offsets, sizes, colors, marker_types, marker_colors, marker_sizes = [],[],[],[],[],[],[],[],[],[]

        #for each_section in conf.sections():
        #    for (each_key, each_val) in conf.items(each_section):
        #        if (each_key == 'label'): labels.append(each_val)
        #        if (each_key == 'lon'): city_lons.append(float(each_val))
        #        if (each_key == 'lat'): city_lats.append(float(each_val))
        #        if (each_key == 'x_offset'): x_offsets.append(float(each_val))
        #        if (each_key == 'y_offset'): y_offsets.append(float(each_val))
        #        if (each_key == 'size'): sizes.append(int(each_val))
        #        if (each_key == 'color'): colors.append(each_val)
        #        if (each_key == 'marker_type'): marker_types.append(each_val)
        #        if (each_key == 'marker_color'): marker_colors.append(each_val)
        #        if (each_key == 'marker_size'): marker_sizes.append(each_val)

        #import matplotlib.patheffects as PathEffects
        #for label, xpt, ypt, x_offset, y_offset, size, col, mtype, mcolor, msize in zip(labels, city_lons, city_lats, x_offsets, y_offsets, sizes, colors, marker_types, marker_colors, marker_sizes):
        #    ax.plot(xpt, ypt, str(mtype), color=str(mcolor), markersize=int(msize), transform=ccrs.Geodetic(), markeredgewidth=1.0, markeredgecolor=(0, 0, 0, 1), zorder=10)
        #    txt = ax.text(xpt+x_offset , ypt+y_offset, label, fontsize=int(size), fontweight='bold', color=str(col), transform=ccrs.Geodetic(), zorder=11)
        #    txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='black')])

        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------

      # Add RGB Legend
        rgb_legend_flag = False
        rgb_legend_lang = "ENG"
		# rgb_legend_lang = "GR"
        if (product == "ARMRGB"):
            if sector_name == "_FDK":
                rgb_legend = plt.imread('..//Legends//AIRMASS_legend_cyan_' + rgb_legend_lang + '.png')
            else:
                rgb_legend = plt.imread('..//Legends//AIRMASS_legend_white_' + rgb_legend_lang + '.png')
            rgb_legend_flag = True

        if (product == "ASHRGB"):
            if sector_name == "_FDK":
                rgb_legend = plt.imread('..//Legends//ASH_legend_cyan_' + rgb_legend_lang + '.png')
            else:
                rgb_legend = plt.imread('..//Legends//ASH_legend_black_' + rgb_legend_lang + '.png')
            rgb_legend_flag = True

		#
		
        if (product == "CONRGB"):
            if sector_name == "_FDK":
                rgb_legend = plt.imread('..//Legends//SEVERESTORMS_legend_cyan_' + rgb_legend_lang + '.png')
            else:
                rgb_legend = plt.imread('..//Legends//SEVERESTORMS_legend_black_' + rgb_legend_lang + '.png')
            rgb_legend_flag = True

        if (product == "NAFRGB"):
            if sector_name == "_FDK":
                rgb_legend = plt.imread('..//Legends//NATURALCOLOR_legend_cyan_' + rgb_legend_lang + '.png')
            else:
                rgb_legend = plt.imread('..//Legends//NATURALCOLOR_legend_black_' + rgb_legend_lang + '.png')
            rgb_legend_flag = True

        if (product == "DMPRGB"):
            if sector_name == "_FDK":
                rgb_legend = plt.imread('..//Legends//DAYMICROPHYSICS_legend_cyan_' + rgb_legend_lang + '.png')
            else:
                rgb_legend = plt.imread('..//Legends//DAYMICROPHYSICS_legend_black_' + rgb_legend_lang + '.png')
            rgb_legend_flag = True

		#2nd row			
        if (product == "DSTRGB"):
            if sector_name == "_FDK":
                rgb_legend = plt.imread('..//Legends//DUST_legend_cyan_' + rgb_legend_lang + '.png')
            else:
                rgb_legend = plt.imread('..//Legends//DUST_legend_black_' + rgb_legend_lang + '.png')
            rgb_legend_flag = True

        if (product == "FOGRGB"):
            if sector_name == "_FDK":
                rgb_legend = plt.imread('..//Legends//24MICROPHYSICS_legend_cyan_' + rgb_legend_lang + '.png')
            else:
                rgb_legend = plt.imread('..//Legends//24MICROPHYSICS_legend_black_' + rgb_legend_lang + '.png')
            rgb_legend_flag = True

        if (product == "HCDRGB"):
            if sector_name == "_FDK":
                rgb_legend = plt.imread('..//Legends//HRVCLOUDS_legend_cyan_' + rgb_legend_lang + '.png')
            else:
                rgb_legend = plt.imread('..//Legends//HRVCLOUDS_legend_cyan_' + rgb_legend_lang + '.png')
            rgb_legend_flag = True
			
        if (product == "NFORGB"):
            if sector_name == "_FDK":
                rgb_legend = plt.imread('..//Legends//NIGHTMICROPHYSICS_legend_cyan_' + rgb_legend_lang + '.png')
            else:
                rgb_legend = plt.imread('..//Legends//NIGHTMICROPHYSICS_legend_black_' + rgb_legend_lang + '.png')
            rgb_legend_flag = True

        if (product == "HFGRGB"):
            if sector_name == "_FDK":
                rgb_legend = plt.imread('..//Legends//HRVFOG_legend_cyan_' + rgb_legend_lang + '.png')
            else:
                rgb_legend = plt.imread('..//Legends//HRVFOG_legend_white_' + rgb_legend_lang + '.png')
            rgb_legend_flag = True
			
        if (product == "SNWRGB"):
            if sector_name == "_FDK":
                rgb_legend = plt.imread('..//Legends//SNOW_legend_cyan_' + rgb_legend_lang + '.png')
            else:
                rgb_legend = plt.imread('..//Legends//SNOW_legend_black_' + rgb_legend_lang + '.png')
            rgb_legend_flag = True

        if rgb_legend_flag :
            # To put colorbar inside picture
            legendax  = fig.add_axes([0.06, 0,  0.94 , 0.9], anchor='SE', zorder=12)
            legendax.imshow(rgb_legend)
            legendax.axis('off')

    else:
        # Converts a CPT file to be used in Python
        if (product == 'VIS006') or (product == 'VIS008') or (product == 'NIR016') or (product == 'HRVCHN'):
            cpt = loadCPT('..//Colortables//Square Root Visible Enhancement.cpt')
            cmap = LinearSegmentedColormap('cpt', cpt)
            vmin = 0.0
            vmax = 1.0
            thick_interval = 0.1
        if (product == 'IRD039'):
            if sector_name == "_FDK":
                cpt = loadCPT('..//Colortables//SVGAIR2_TEMP.cpt')
            else:
                cpt = loadCPT('..//Colortables//MSGIR.cpt')
            cmap = LinearSegmentedColormap('cpt', cpt)
            data -= 273.15
            vmin = -112.15
            vmax = 56.85
            thick_interval = 10.0
        if (product == 'WV_062') or (product == 'WV_073'):
            if sector_name == "_FDK":
                cpt = loadCPT('..//Colortables//SVGAWVX_TEMP.cpt')
            else:
                cpt = loadCPT('..//Colortables//MSGWV.cpt')
            cmap = LinearSegmentedColormap('cpt', cpt)
            data -= 273.15
            vmin = -112.15
            vmax = 56.85
            thick_interval = 10.0
        if (product == 'IRD087')  or (product == 'IRD108') or (product == 'IRD120'):
            cpt = loadCPT('..//Colortables//IR4AVHRR6.cpt')
            cmap = LinearSegmentedColormap('cpt', cpt)
            data -= 273.15
            vmin = -103.0
            vmax = 84.0
            thick_interval = 10.0
        if (product == 'IRD097') or (product == 'IRD134'):
            if sector_name == "_FDK":
                cpt = loadCPT('..//Colortables//IR4AVHRR6.cpt')
            else:
                cpt = loadCPT('..//Colortables//MSGIR.cpt')
            cmap = LinearSegmentedColormap('cpt', cpt)
            data -= 273.15
            vmin = -88.0
            vmax = 84.0
            thick_interval = 10.0

        #--------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------

        # Plot configuration
        plot_config = {
        "resolution": 8,
        "dpi": 150,
        "states_color": 'white', "states_width": data.shape[0] * 0.000,
        "countries_color": 'cyan', "countries_width": data.shape[0] * 0.00012,
        "continents_color": 'cyan', "continents_width": data.shape[0] * 0.00011,
        "fir_color": 'orange', "fir_width": data.shape[0] * 0.00011,
        "grid_color": 'white', "grid_width": data.shape[0] * 0.00025, "grid_interval": 10.0,
        "vmin": vmin, "vmax": vmax, "cmap": cmap,
        "title_text": title, "title_size": int(data.shape[0] * 0.008), "title_x_offset": int(data.shape[1] * 0.01), "title_y_offset": data.shape[0] - int(data.shape[0] * 0.025),
        "thick_interval": thick_interval, "cbar_labelsize": int(data.shape[0] * 0.008), "cbar_labelpad": -int(data.shape[0] * 0.0),
        "file_name_id_1": satellite,  "file_name_id_2": product + sector_name
        }
        #--------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------
        # Choose the plot size (width x height, in inches)
        fig = plt.figure(figsize=(data.shape[1]/float(plot_config["dpi"]), data.shape[0]/float(plot_config["dpi"])), dpi=plot_config["dpi"])

        if sector_name == "_FDK":
             # Define the projection
            if satellite=="MSG_IODC":
                proj = ccrs.Geostationary(central_longitude=41.5, satellite_height=35786023)
            elif satellite=="MSG_RSS":
                proj = ccrs.Geostationary(central_longitude=9.5, satellite_height=35786023)
            else:
                proj = ccrs.Geostationary(central_longitude=0.0, satellite_height=35786023)
            img_extent = (-5568748.27576, 5568748.27576, -5568748.27576, 5568748.27576)

            # Use the Geostationary projection in cartopy
            ax = plt.axes([0, 0, 1, 1], projection=proj)

        else:
            # Define the projection
            proj = ccrs.PlateCarree()

            # Use the PlateCarree projection in cartopy
            ax = plt.axes([0, 0, 1, 1], projection=proj)
            ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

            # Define the image extent
            img_extent = [extent[0], extent[2], extent[1], extent[3]]


        # Add background image if HRV
        #if (product == 'HRVCHN_FDK'):
        if (product == 'HRVCHN'):
            #ax.stock_img()
            fname = os.path.join('..//Maps//', 'land_ocean_ice_8192.jpg')
            ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)
            #date = datetime(int(year), int(month), int(day), int(hour))
            #ax.add_feature(Nightshade(date, alpha=0.7), zorder=2)


        # Add background image if HRV
        # if (product == 'HRVCHN_EU') or (product == 'HRVCHN_GR'):
        #     #ax.stock_img()
        #     fname = os.path.join('..//Maps//', 'land_ocean_ice_8192.jpg')
        #     ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=1)
        #     #date = datetime(int(year), int(month), int(day), int(hour))
        #     #ax.add_feature(Nightshade(date, alpha=0.7), zorder=2)

        # Plot the image
        img = ax.imshow(data, interpolation='antialiased', vmin=plot_config["vmin"], vmax=plot_config["vmax"], origin='upper', extent=img_extent, cmap=plot_config["cmap"], zorder=3)

        # To put colorbar inside picture
        axins1 = inset_axes(ax, width="100%", height="1%", loc='lower center', borderpad=0.0)

        # Add states and provinces
        shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_admin_1_states_provinces.shp').geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["states_color"],facecolor='none', linewidth=plot_config["states_width"], zorder=4)

        # Add countries
        shapefile = list(shpreader.Reader('..//Shapefiles//ne_50m_admin_0_countries.shp').geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["countries_color"],facecolor='none', linewidth=plot_config["countries_width"], zorder=5)

        # Add continents
#        shapefile = list(shpreader.Reader('..//Shapefiles//ne_10m_coastline.shp').geometries())
#        shapefile = list(shpreader.Reader('../Shapefiles/GRC_admin/GRC_adm2.shp').geometries())
        shapefile = list(shpreader.Reader('../Shapefiles/gis_osm_places_a_free_1.shp').geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["continents_color"],facecolor='none', linewidth=plot_config["continents_width"], zorder=6)

        # Add Athens FIR
        shapefile = list(shpreader.Reader('../Shapefiles/FIR_ATH/FIR_Athens.shp').geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor=plot_config["fir_color"],facecolor='none', linewidth=plot_config["fir_width"], zorder=6)


        # Add coastlines, borders and gridlines
#        ax.gridlines(color=plot_config["grid_color"], alpha=0.5, linestyle='--', linewidth=plot_config["grid_width"], xlocs=np.arange(-180, 180, plot_config["grid_interval"]), ylocs=np.arange(-180, 180, plot_config["grid_interval"]), draw_labels=False, zorder=7)

        # Remove the outline border
        ax.outline_patch.set_visible(False)

        # Add a title
        plt.annotate(plot_config["title_text"], xy=(plot_config["title_x_offset"], plot_config["title_y_offset"]), xycoords='figure pixels', fontsize=plot_config["title_size"], fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0), ec=(1., 1., 1.)), zorder=8)

        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Add labels to specific coordinates

        #import configparser
        #conf = configparser.ConfigParser()
        #conf.read('..//Utils//Labels//labels_msg.ini')

        #labels, city_lons, city_lats, x_offsets, y_offsets, sizes, colors, marker_types, marker_colors, marker_sizes = [],[],[],[],[],[],[],[],[],[]

        #for each_section in conf.sections():
        #    for (each_key, each_val) in conf.items(each_section):
        #        if (each_key == 'label'): labels.append(each_val)
        #        if (each_key == 'lon'): city_lons.append(float(each_val))
        #        if (each_key == 'lat'): city_lats.append(float(each_val))
        #        if (each_key == 'x_offset'): x_offsets.append(float(each_val))
        #        if (each_key == 'y_offset'): y_offsets.append(float(each_val))
        #        if (each_key == 'size'): sizes.append(int(each_val))
        #        if (each_key == 'color'): colors.append(each_val)
        #        if (each_key == 'marker_type'): marker_types.append(each_val)
        #        if (each_key == 'marker_color'): marker_colors.append(each_val)
        #        if (each_key == 'marker_size'): marker_sizes.append(each_val)

        #import matplotlib.patheffects as PathEffects
        #for label, xpt, ypt, x_offset, y_offset, size, col, mtype, mcolor, msize in zip(labels, city_lons, city_lats, x_offsets, y_offsets, sizes, colors, marker_types, marker_colors, marker_sizes):
        #    ax.plot(xpt, ypt, str(mtype), color=str(mcolor), markersize=int(msize), transform=ccrs.Geodetic(), markeredgewidth=1.0, markeredgecolor=(0, 0, 0, 1), zorder=10)
        #    txt = ax.text(xpt+x_offset , ypt+y_offset, label, fontsize=int(size), fontweight='bold', color=str(col), transform=ccrs.Geodetic(), zorder=11)
        #    txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='black')])
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------

        # Add a colorbar
        ticks = np.arange(plot_config["vmin"], plot_config["vmax"], plot_config["thick_interval"]).tolist()
        ticks = plot_config["thick_interval"] * np.round(np.true_divide(ticks,plot_config["thick_interval"]))
        ticks = ticks[1:]
        cb = fig.colorbar(img, cax=axins1, orientation="horizontal", ticks=ticks)
        cb.outline.set_visible(False)
        cb.ax.tick_params(width = 0)
        cb.ax.xaxis.set_tick_params(pad=plot_config["cbar_labelpad"])
        cb.ax.xaxis.set_ticks_position('top')
        cb.ax.tick_params(axis='x', colors='cyan', labelsize=plot_config["cbar_labelsize"])

    # Add logos / images to the plot
    my_logo = plt.imread('..//Logos//my_logo.png')
    newax = fig.add_axes([0.01, 0.03, 0.05, 0.05], anchor='SW', zorder=12) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
    newax.imshow(my_logo)
    newax.axis('off')
    #---------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------

    # Create the satellite output directory if it doesn't exist
    # Caution! The output directory is outside the SHOWCast folder
    out_dir = '..//..//Output/' + satellite
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
        os.chmod(out_dir, 0o777)

    # Create the product output directory if it doesn't exist
    out_dir = '..//..//Output/' + satellite + '//' + product + sector_name + '//'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
        os.chmod(out_dir, 0o777)

    # Save the image
    plt.savefig(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + time_date + '.png', bbox_inches='tight', pad_inches=0, facecolor='black')

    # Create the thumbnails output sub-directory if it doesn't exist
    thumb_dir = '..//..//Output//Thumbnails/'
    if not os.path.exists(thumb_dir):
        os.mkdir(thumb_dir)
        os.chmod(thumb_dir, 0o777)
    
    #create the thumbnail
    thumb_dir = '..//..//Output//Thumbnails/' + satellite + "_" + product + sector_name + '_' + 'thumbnail.png'
    im = Image.open(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + time_date + '.png')
    #size = (1024,1024)
    size = (512,512)
    im.thumbnail(size)
    im.save(thumb_dir)

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
#print("601 MSG path to file=",path)

# Desired resolution
resolution = int(sys.argv[6])

# Read the resolution
band_resolution_km = 3

# Division factor to reduce image size
f = math.ceil(float(resolution / band_resolution_km))

P = pyproj.Proj(proj='eqc', ellps='WGS84', preserve_units=True)
G = pyproj.Geod(ellps='WGS84')
# Image extent
# extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Put the processed file on the log
with open('..//Logs//shc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
    log.write(str(datetime.datetime.now()))
    log.write('\n')
    log.write(path + '\n')
    log.write('\n')
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------


result = re.search('-_________-EPI______-(.*)-__', path)
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

# Creating an Area Definition on the fly
from pyresample import geometry

def extents(extent,resolution,sector_name):
    # Division factor to reduce image size
    f = math.ceil(float(resolution / band_resolution_km))
    x1,y1 = LatLon_To_XY(extent[1],extent[0])
    x2,y2 = LatLon_To_XY(extent[3],extent[2])

    # Define KM_PER_DEGREE
    KM_PER_DEGREE = 111.32
    # Calculate the total number of degrees in lat and lon
    deg_lon = extent[2] - extent[0]
    deg_lat = extent[3] - extent[1]
    # Calculate the number of pixels
    width = (KM_PER_DEGREE * deg_lon) /  resolution
    height = (KM_PER_DEGREE * deg_lat) /  resolution
    # =============================================================================
    # area_id = 'seviri_0deg'
    # description = 'Seviri 0 Degree'
    # proj_id = 'seviri_0deg'
    # =============================================================================
    area_id = 'Greece'
    description = 'seviri_l1b_hrit'
    proj_id = 'seviri_l1b_hrit'
    x_size = int(width)
    y_size = int(height)
    area_extent = (y1,x1,y2,x2)
    proj_dict = {'a': 6378169.0, 'b': 6378169.0,'units': 'm', 'lon_0': 0.0,'proj': 'eqc', 'lat_0': 0.0}
    return area_id, description, proj_id, proj_dict, x_size, y_size, area_extent ,f

    #-----------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#extents(extent,resolution)

# Path to XRIT_DECOMPRESS library
os.environ['XRIT_DECOMPRESS_PATH'] = XRIT_DECOMPRESS_PATH

# Create the global scene
global_scene = Scene(reader='seviri_l1b_hrit',filenames=glob(path2 + '*' + time_date + '*'))

# Load the global scene
global_scene.load(composites)
print("available names: \n",global_scene.available_composite_names())
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

#  Set folder names for products
products_dict = {'VIS006':'VIS006', 'VIS008':'VIS008', 'IR_016':'NIR016', 'IR_039':'IRD039', 'WV_062':'WV_062', 'WV_073':'WV_073', 'IR_087':'IRD087', 'IR_097':'IRD097',
                 'IR_108':'IRD108', 'IR_120':'IRD120', 'IR_134':'IRD134', 'HRV':'HRVCHN', 'airmass':'ARMRGB', 'ash':'ASHRGB', 'cloudtop':'TOPRGB', 'convection':'CONRGB',
                 'natural_enh_sun':'NLCRGB', 'day_microphysics':'DMPRGB', 'dust':'DSTRGB', 'fog':'FOGRGB', 'ir_overview':'IRORGB', 'night_fog':'NFORGB',
                 'overview_sun':'OVWRGB', 'snow':'SNWRGB', 'natural_enh':'NAENRGB', 'colorized_ir_clouds':'CIRCRGB', 'realistic_colors':'REARGB',
                 'natural_with_night_fog':'NAFRGB', 'overview':'OVWRGB', 'hrv_clouds': 'HCDRGB', 'hrv_fog':'HFGRGB', 'natural_color':'DLCRGB', 'ir_sandwich':'IRSRGB', 'ir108_3d':'I3DRGB', 'hrv_severe_storms_masked':'HSTRGB', 'hrv_severe_storms':'HSVRGB', 'vis_sharpened_ir':'VSHRGB'}

# List of products that we need to devide data/100
d100_list = ['VIS006','VIS008','IR_016','HRV']

# 3 sector for producing 3 images - Full disk - European region -  Greek region
# sectors = ["_FDK","_EU","_GR"] got from config

# Extent init [-x,-y,x,y] extents for the 3 sectors (lats and lons)
extent_global    = [0.0, 0.0, 0.0, 0.0]
extent_europe    = [-16.0, 25.0, 52.0, 70.0]
extent_greece    = [15.0, 31.0, 35.0, 44.0]

area_extents     = {"_EU":extent_europe,"_GR":extent_greece,"_FDK":extent_global}
area_resolutions = {"_EU":3,"_GR":1,"_FDK":5}

# Producing all sector images using one decompress
for sector_name in sectors:
    extent=area_extents[sector_name]
    if sector_name =="_EU":
        area_id, description, proj_id, proj_dict, x_size, y_size, area_extent ,f = extents(area_extents[sector_name],area_resolutions[sector_name],sector_name)
        area_def = geometry.AreaDefinition(area_id, description, proj_id, proj_dict, x_size, y_size, area_extent )
        europe_scn = global_scene.resample(area_def)
    if sector_name =="_GR":
        area_id, description, proj_id, proj_dict, x_size, y_size, area_extent ,f = extents(area_extents[sector_name],area_resolutions[sector_name],sector_name)
        area_def = geometry.AreaDefinition(area_id, description, proj_id, proj_dict, x_size, y_size, area_extent )
        greek_scn = global_scene.resample(area_def)

    # produce images for band products included in bands_list
    for band in bands_list:
        try:
            product = products_dict[band]
            type = 'BAND'
            diairetis =1
            if band in d100_list:
                diairetis=100
            # if producing full disk image
            if sector_name=="_FDK":
                data = global_scene[band] / diairetis
                data = data[:,:][::f ,::f ]
                data = np.flipud(data)
                data = np.fliplr(data)
            # if producing sector image
            elif sector_name=="_EU":
                data = europe_scn[band] / diairetis
                data = data[:,:][::f ,::f ]
            elif sector_name=="_GR":
                data = greek_scn[band] / diairetis
                data = data[:,:][::f ,::f ]
                # data = np.flipud(data)
                # data = np.fliplr(data)
            # Call the plotting function
#            print(product," data: \n",data)
            procMSG(data, product, band, type, sector_name,extent,time_date)
        except Exception as ex:
            print(ex)

    # produce images for RGB products included in rgbs_list
    for rgb in rgbs_list:
        try:
            product = products_dict[rgb]
            type = 'RGB'
            # if producing full disk image
            if sector_name=="_FDK":
                if rgb in hrv_rgb_list:
                    hrv_glob = global_scene.resample(global_scene.min_area(), resampler='native')
                    data=get_enhanced_image(hrv_glob[rgb])
                else:
                    data = get_enhanced_image(global_scene[rgb])
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
            # if producing sector image
            elif sector_name=="_EU":
                data = get_enhanced_image(europe_scn[rgb])
                data = data.finalize(fill_value=None)[0]
                #print(data.shape)
                R = (data[0,:,:][::f ,::f])
                G = (data[1,:,:][::f ,::f])
                B = (data[2,:,:][::f ,::f])
            elif sector_name=="_GR":
                data = get_enhanced_image(greek_scn[rgb])
                data = data.finalize(fill_value=None)[0]
                #print(data.shape)
                R = (data[0,:,:][::f ,::f])
                G = (data[1,:,:][::f ,::f])
                B = (data[2,:,:][::f ,::f])
            # Create the RGB
            data = np.stack([R, G, B], axis=2)
#            print(product," rgb data: \n",data)
            # Call the plotting function
            procMSG(data, product, rgb, type, sector_name,extent,time_date)
        except Exception as ex:
            print(ex)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
print('Total processing time:', round((t.time() - start),2), 'seconds.')
