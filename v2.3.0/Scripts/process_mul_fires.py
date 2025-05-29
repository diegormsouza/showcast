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
import sys                                                   # Import the "system specific parameters and functions" module
import time as t                                             # Time access and conversion
import gzip, shutil                                          # Support for gzip files
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
from shutil import move                                      # High-level file operations
from html_update import update                               # Update the HTML animation 
import folium
from folium import plugins
from folium.plugins import Draw
from folium.plugins import MeasureControl
from folium.plugins import MousePosition
from folium.plugins import FloatImage
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Ignore possible warnings
import warnings
warnings.filterwarnings("ignore")
       
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

path2 = re.sub('INPE_MVF_*(.*)', '', path)
#print(path2)
path3 = path.replace(path2,'')
path3 = path3.replace('.gz','')
#print(path3)

# Unzipping the gz file
with gzip.open(path, 'r') as f_in, open(path2+path3, 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)
    path = path2+path3

# Unzipping the tar file, which was inside the gz. Extract it on the same directory
import tarfile
tf = tarfile.open(path)
tf.extractall(path2)
	
print("Arquivo: ", path)		

print(path)
print(path2)
print(path3)

path_shape = path2 + path3[:len(path3)-8] + "0000.shp"
print(path_shape)

###############################################################################
# Creating the HTML
###############################################################################

#================================================================================

# Create the map

m = folium.Map(
    location=[-15, -58],
    zoom_start=5,
    tiles='cartodbdark_matter',
	crs='EPSG3857',
    control_scale=True,
	prefer_canvas=True
)

# Add the full screen button

plugins.Fullscreen(
    position='topright',
    title='Expand me',
    title_cancel='Exit me',
    force_separate_button=True
).add_to(m)


# Add the mouse position coordinates

formatter = "function(num) {return L.Util.formatNum(num, 3) + ' ยบ ';};"
MousePosition(
    position='bottomleft',
    separator=' | ',
    empty_string='NaN',
    lng_first=True,
    num_digits=20,
    prefix='Coordinates:',
    lat_formatter=formatter,
    lng_formatter=formatter,
).add_to(m)


# Add a mini map
minimap = plugins.MiniMap()
m.add_child(minimap)

# Add drawinf controls
draw = Draw()
draw.add_to(m)
m.add_child(MeasureControl())

# Add the lat lon pop up when clicking
m.add_child(folium.LatLngPopup())

#================================================================================

# Add custom logos and legends

image = (main_dir + '//HTML//showcast_fire.png')
FloatImage(image, bottom=7, left=1).add_to(m)

image = (main_dir + '//Legends//showcast_fire_legend.png')
FloatImage(image, bottom=18, left=1).add_to(m)

#================================================================================

# Add shapefiles

shape = (main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp')
countries = gpd.read_file(shape)

shape = (main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp')
states = gpd.read_file(shape)

shape = (main_dir + '//Shapefiles//ne_10m_coastline.shp')
coastlines = gpd.read_file(shape)

geoPath_countries = countries.geometry.to_json()
geoPath_states = states.geometry.to_json()
geoPath_coastlines = coastlines.geometry.to_json()

folium.GeoJson(
    geoPath_states,
	name='States',
	show=False,
    style_function=lambda feature: {
        'fillColor': '#00000000',
        'color': 'gold',
        'weight': 1.0,
    }
).add_to(m)

folium.GeoJson(
    geoPath_countries,
	name='Countries',
	show=False,
    style_function=lambda feature: {
        'fillColor': '#00000000',
        'color': 'black',
        'weight': 1.0,
    }
).add_to(m)

folium.GeoJson(
    geoPath_coastlines,
	name='Coastlnes',
	show=False,
    style_function=lambda feature: {
        'fillColor': '#00000000',
        'color': 'red',
        'weight': 1.0,
    }
).add_to(m)

#================================================================================

# Read the Fire / Hot Spot Shapefile and plot it as points over the map

inpe_mvf = gpd.read_file(path_shape)
geometry = [Point(xy) for xy in zip(inpe_mvf['longitude'], inpe_mvf['latitude'])]
df = gpd.GeoDataFrame(inpe_mvf, geometry = geometry)
fires = folium.map.FeatureGroup()

latitudes = list(df.latitude)
longitudes = list(df.longitude)
labels = list(df.cod_sat)

times_dates = list(df.jld)

countries = list(df.name_0)
states = list(df.name_1)
cities = list(df.name_2)

for lat, lng, label, time_date, country, state, city in zip(latitudes, longitudes, labels, times_dates, countries, states, cities):
	if lng < -30:
		if label == 'GOES-16':
			popup_text = "<b>Satellite:</b> " + label + '<br>' + '<b>Time and Date:</b> ' + time_date + ' UTC' + '<br>' + '<b>Country:</b> ' + country + '<br>' + '<b>State / Province:</b> ' + state + '<br>' + '<b>City:</b> ' + city
			folium.Circle(
			   [lat, lng],
			   radius=50,
			   fill=True,
			   #line_color='white',
			   color='white',
			   fill_color='yellow',
			   weight = 0.2,
			   fill_opacity=1,
			   ).add_child(folium.Popup(popup_text, max_width=250,min_width=250)).add_to(m)

		elif label == 'METOP-B':
			popup_text = "<b>Satellite:</b> " + label + '<br>' + '<b>Time and Date:</b> ' + time_date + ' UTC' + '<br>' + '<b>Country:</b> ' + country + '<br>' + '<b>State / Province:</b> ' + state + '<br>' + '<b>City:</b> ' + city
			folium.Circle(
			   [lat, lng],
			   radius=50,
			   fill=True,
			   #line_color='white',
			   color='white',
			   fill_color='navajowhite',
			   weight = 0.2,
			   fill_opacity=1,
			   ).add_child(folium.Popup(popup_text, max_width=250,min_width=250)).add_to(m)

		elif label == 'METOP-C':
			popup_text = "<b>Satellite:</b> " + label + '<br>' + '<b>Time and Date:</b> ' + time_date + ' UTC' + '<br>' + '<b>Country:</b> ' + country + '<br>' + '<b>State / Province:</b> ' + state + '<br>' + '<b>City:</b> ' + city
			folium.Circle(
			   [lat, lng],
			   radius=50,
			   fill=True,
			   #line_color='white',
			   color='white',
			   fill_color='blue',
			   weight = 0.2,
			   fill_opacity=1,
			   ).add_child(folium.Popup(popup_text, max_width=250,min_width=250)).add_to(m)
			   
		elif label == 'NOAA-18':
			popup_text = "<b>Satellite:</b> " + label + '<br>' + '<b>Time and Date:</b> ' + time_date + ' UTC' + '<br>' + '<b>Country:</b> ' + country + '<br>' + '<b>State / Province:</b> ' + state + '<br>' + '<b>City:</b> ' + city
			folium.Circle(
			   [lat, lng],
			   radius=50,
			   fill=True,
			   #line_color='white',
			   color='white',
			   fill_color='red',
			   weight = 0.2,
			   fill_opacity=1,
			   ).add_child(folium.Popup(popup_text, max_width=250,min_width=250)).add_to(m)

		elif label == 'NOAA-19':
			popup_text = "<b>Satellite:</b> " + label + '<br>' + '<b>Time and Date:</b> ' + time_date + ' UTC' + '<br>' + '<b>Country:</b> ' + country + '<br>' + '<b>State / Province:</b> ' + state + '<br>' + '<b>City:</b> ' + city
			folium.Circle(
			   [lat, lng],
			   radius=50,
			   fill=True,
			   #line_color='white',
			   color='white',
			   fill_color='purple',
			   weight = 0.2,
			   fill_opacity=1,
			   ).add_child(folium.Popup(popup_text, max_width=250,min_width=250)).add_to(m)

		elif label == 'NOAA-20':
			popup_text = "<b>Satellite:</b> " + label + '<br>' + '<b>Time and Date:</b> ' + time_date + ' UTC' + '<br>' + '<b>Country:</b> ' + country + '<br>' + '<b>State / Province:</b> ' + state + '<br>' + '<b>City:</b> ' + city
			folium.Circle(
			   [lat, lng],
			   radius=50,
			   fill=True,
			   #line_color='white',
			   color='white',
			   fill_color='cyan',
			   weight = 0.2,
			   fill_opacity=1,
			   ).add_child(folium.Popup(popup_text, max_width=200,min_width=200)).add_to(m)
		   
		elif label == 'NPP-375':
			popup_text = "<b>Satellite:</b> " + label + '<br>' + '<b>Time and Date:</b> ' + time_date + ' UTC' + '<br>' + '<b>Country:</b> ' + country + '<br>' + '<b>State / Province:</b> ' + state + '<br>' + '<b>City:</b> ' + city
			folium.Circle(
			   [lat, lng],
			   radius=50,
			   fill=True,
			   #line_color='white',
			   color='white',
			   fill_color='green',
			   weight = 0.2,
			   fill_opacity=1,
			   ).add_child(folium.Popup(popup_text, max_width=250,min_width=250)).add_to(m)

		elif label == 'TERRA_M-M' or label == 'TERRA_M-T':
			popup_text = "<b>Satellite:</b> " + label + '<br>' + '<b>Time and Date:</b> ' + time_date + ' UTC' + '<br>' + '<b>Country:</b> ' + country + '<br>' + '<b>State / Province:</b> ' + state + '<br>' + '<b>City:</b> ' + city
			folium.Circle(
			   [lat, lng],
			   radius=50,
			   fill=True,
			   #line_color='white',
			   color='white',
			   fill_color='orange',
			   weight = 0.2,
			   fill_opacity=1,
			   ).add_child(folium.Popup(popup_text, max_width=250,min_width=250)).add_to(m)

		elif label == 'AQUA_M-M' or label == 'AQUA_M-T':
			popup_text = "<b>Satellite:</b> " + label + '<br>' + '<b>Time and Date:</b> ' + time_date + ' UTC' + '<br>' + '<b>Country:</b> ' + country + '<br>' + '<b>State / Province:</b> ' + state + '<br>' + '<b>City:</b> ' + city
			folium.Circle(
			   [lat, lng],
			   radius=50,
			   fill=True,
			   #line_color='white',
			   color='white',
			   fill_color='white',
			   weight = 0.2,
			   fill_opacity=1,
			   ).add_child(folium.Popup(popup_text, max_width=250,min_width=250)).add_to(m)
  
#================================================================================

# Add the background tile options

folium.TileLayer(
    name="Esri World Imagery",
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
).add_to(m)

folium.TileLayer('openstreetmap').add_to(m)
folium.TileLayer('Stamen Terrain').add_to(m)
folium.TileLayer('Stamen Toner').add_to(m)
folium.TileLayer('Stamen Water Color').add_to(m)
folium.TileLayer('cartodbpositron').add_to(m)
folium.TileLayer('cartodbdark_matter').add_to(m)
folium.LayerControl().add_to(m)

# Save the map as an HTML file
m.save(main_dir + '//HTML//SHOWCast_Fire.html')

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