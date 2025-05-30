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
__credits__ = ["Diego Souza", "Rogerio Batista"]
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
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
from netCDF4 import Dataset                                  # Read / Write NetCDF4 files
from osgeo import gdal, osr, ogr                             # Import GDAL
from shutil import move                                      # High-level file operations
from matplotlib.image import imread                          # Read an image from a file into an array
from cartopy.feature.nightshade import Nightshade            # Draws a polygon where there is no sunlight for the given datetime.
from html_update import update                               # Update the HTML animation 
from mpl_toolkits.axes_grid1.inset_locator import inset_axes # Add a child inset axes to this existing axes.
import pyresample as pr                                      # Import the pyresample package
from pyresample import geometry                              # Import the pyresample geometry module 
from pyresample.kd_tree import resample_nearest              # Import the pyresample neares neighbor   
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

def getGeoTransform(extent, nlines, ncols):
    resx = (extent[2] - extent[0]) / ncols
    resy = (extent[3] - extent[1]) / nlines
    return [extent[0], resx, 0, extent[3] , 0, -resy]

# File to be processed
path = sys.argv[1]

# Convert user lat lons to bounding box with pyproj        
import pyproj
prj = pyproj.Proj('+proj=eqc')

# Choose the interpolation interval
interp_step = 1

# The extent below only works with the Equidistant Cylindrical Projection
extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]
original_extent = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]

if "VIIRS_NCC_EDR" in path:      # If it is the Day Night Band
    lons_interp = np.empty((771,4121))
    lats_interp = np.empty((771,4121))
    L0 = np.empty((1,4121))
    L1 = np.empty((1,4121))
    L2 = np.empty((1,4121))
    path2 = re.sub('VIIRS_NCC_EDR(.*)', '', path)	
elif "VIIRS_I5_IMG_EDR" in path: # If it is the I5 Band
    lons_interp = np.zeros((1541,8241))
    lats_interp = np.zeros((1541,8241))
    L0 = np.empty((1,8241))
    L1 = np.empty((1,8241))
    L2 = np.empty((1,8241))
    path2 = re.sub('VIIRS_I5_IMG_EDR(.*)', '', path)
	    
# Get the start of scan from the file name
Start = (path[path.find("_s")+2:path.find("_e")])

# Get all geolocation files in the directory    
geo = []
for filename in sorted(glob.glob(path2+'VIIRS_*_EDR_GEO*.nc')):
    geo.append(filename)
    #print(filename)
    
# Seek for a GEO file in the directory
matching = [s for s in geo if Start in s]     
#print(matching)

# If the GEO file is not found, exit the loop
if not matching:
    #print(geo)
    print("GEO File Not Found! Exiting Script.")
    sys.exit()
    #print("NO FILES!)
else: # If the GEO file is found, continue
    print("GEO File OK!")
    matching = matching[0]
    #print(matching)
    index = geo.index(matching)
    #print(index)
    path2 = geo[index]
    #print(path2)          
# Open the file using the NetCDF4 library
#print(path)
#print(path2)

nc = Dataset(path)
nc2 = Dataset(path2)

# Get the lats and lons from the GEO file
if "VIIRS_NCC_EDR" in path:      # If it is the Day Night Band
    lats = nc2.variables['Latitude@VIIRS-NCC-EDR-GEO'][:]
    lons = nc2.variables['Longitude@VIIRS-NCC-EDR-GEO'][:]
elif "VIIRS_I5_IMG_EDR" in path: # If it is the I5 Band
    lats = nc2.variables['Latitude@VIIRS-IMG-GTM-EDR-GEO'][:]
    lons = nc2.variables['Longitude@VIIRS-IMG-GTM-EDR-GEO'][:]
    
# Verifying if the granule is inside the region of interest
inside = True
if (min(lons[:,0] < extent[0])) and (min(lons[:,1] < extent[0])) and (min(lons[:,2] < extent[0])):
    inside = False
        
if (max(lons[:,0] > extent[2])) and (max(lons[:,1] > extent[2])) and (max(lons[:,2] > extent[2])):
    inside = False
        
if (min(lats[:,0] < extent[1])) and (min(lats[:,1] < extent[1])) and (min(lats[:,2] < extent[1])):
    inside = False
        
if (max(lats[:,0] > extent[3])) and (max(lats[:,1] > extent[3])) and (max(lats[:,2] > extent[3])):
    inside = False 
   
# If the granule is inside the region of interest
if (inside == True):
    #start = t.time()	
    #print(x)   
        
    # Disable the auto scale (for some reason the automatic scale is giving errors)
    nc.set_auto_maskandscale(False)
        
    if "VIIRS_NCC_EDR" in path:         # If it is the Day Night Band
        data = nc.variables['Albedo@VIIRS-NCC-EDR'][:]
        scale = nc.variables['Albedo@VIIRS-NCC-EDR'].scale_factor
        offset = nc.variables['Albedo@VIIRS-NCC-EDR'].add_offset
        L0 = np.arange(4121)
        L1 = np.arange(4121)
        L2 = np.arange(4121)
        band = 'DNBAND'
        satellite = 'JPS'
        product = band + '_STR' # to store data before mosaicing
        #=====================================================================
        # Calculate the number of pixels
        resolution = int(sys.argv[6])
        #resolution = 0.750
        no_data = -10
        data_type = gdal.GDT_Float32
        
        # Create the satellite output directory if it doesn't exist
        out_dir = main_dir + '//Output//' + satellite
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        # Create the product output directory if it doesn't exist
            out_dir = main_dir + '//Output//' + satellite + '//' + product + '//'
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
            
    elif "VIIRS_I5_IMG_EDR" in path:    # If it is the I5 Band
        data = nc.variables['BrightnessTemperature@VIIRS-I5-IMG-EDR'][:]
        scale = nc.variables['BrightnessTemperature@VIIRS-I5-IMG-EDR'].scale_factor
        offset = nc.variables['BrightnessTemperature@VIIRS-I5-IMG-EDR'].add_offset     
        L0 = np.arange(8241)
        L1 = np.arange(8241)
        L2 = np.arange(8241)		
        band = 'I5BAND'
        satellite = 'JPS'
        product = band + '_STR' # to store data before mosaicing
        prod_title = 'I5 Band'
        # Calculate the number of pixels
        resolution = int(sys.argv[6])
        #resolution = 0.350			
        no_data = -10
        data_type = gdal.GDT_Int16

        # Create the satellite output directory if it doesn't exist
        out_dir = main_dir + '//Output//' + satellite
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        # Create the product output directory if it doesn't exist
            out_dir = main_dir + '//Output//' + satellite + '//' + product + '//'
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
			
	# Close the NetCDF file after getting the data
    nc.close()
    nc2.close()
		
	# Apply the scale and offset
    data = (data * scale) + offset   
        
	# Get rid of the bad values
    #data[data >= 380] = np.nan
     
    # We have a condensed GEO file (only 3 columns). We need to interpolate.
    #    print ("%i, %i, %i", lons[x,0], lons[x,1], lons[x,2])
    #  1         | 2060      | 4121
    #  lons[x,0] | lons[x,1] | lons[x,2]
    #L0 = (x-x1)(x-x2)/(x0-x1)(x0-x2)
    #L1 = (x-x0)(x-x2)/(x1-x0)(x1-x2)
    #L2 = (x-x0)(x-x1)/(x2-x0)(x2-x1)
   
    fcol = 1.                       # First column 
    mcol = int(data.shape[1] / 2)   # Middle column 
    lcol = data.shape[1]            # Last column
    nlines = data.shape[0]

    #print(data.shape[0])
    #print(lats.shape[0])
    #print(lons.shape[0])
    #print (mcol)
    #print (lcol)
	        
    #print("Interpolation Started")
           
    L0 = ( (L0[:] * L0[:]  - lcol * L0[:]  - mcol * L0[:] + mcol * lcol) / ((fcol - mcol) * (fcol - lcol)) )
    L1 = ( (L1[:] * L1[:] - lcol * L1[:] - fcol * L1[:] + fcol * lcol) / ((mcol - fcol) * (mcol - lcol)) )
    L2 = ( (L2[:] * L2[:] - mcol * L2[:] - fcol * L2[:] + fcol * mcol) / ((lcol - fcol) * (lcol - mcol)) )
        
    #print(L0.shape)
    #print(L1.shape)
    #print(L2.shape)
    #print(lons.shape)
    #print(lats.shape)
    #print(lons_interp.shape)
    #print(lats_interp.shape)
    #print(nlines)
    #print(lcol)		
		
    for x in range (0,nlines,interp_step):
        lons_interp[x,:] = (lons[x,0])*(L0[:])+(lons[x,1])*(L1[:])+(lons[x,2])*(L2[:])
        lats_interp[x,:] = (lats[x,0])*(L0[:])+(lats[x,1])*(L1[:])+(lats[x,2])*(L2[:])        	
		
    lons_interp[lons_interp < -180] = np.nan
    lats_interp[lats_interp < -90] = np.nan
        
    #print("Interpolation ended")
    #print(np.nanmin(lons_interp))
    min_lon = np.nanmin(lons_interp)
    #print(np.nanmin(lats_interp))
    min_lat = np.nanmin(lats_interp)
    #print(np.nanmax(lons_interp))
    max_lon = np.nanmax(lons_interp)		
    #print(np.nanmax(lats_interp))
    max_lat = np.nanmax(lats_interp)
    #print(lons_interp)
    #=========================================================================================		
    #print(extent)
    if (min_lon < extent[0]):
        min_lon = extent[0]
    #print(min_lon)
    if (min_lat < extent[1]):
        min_lat = extent[1]
    #print(min_lat)
    if (max_lon > extent[2]):
        max_lon = extent[2]
    #print(max_lon)
    if (max_lat > extent[3]):
        max_lat = extent[3]
    #print(max_lat)

    extent = [min_lon, min_lat, max_lon, max_lat]
    #print(extent)
    lon_bbox = (extent[0], extent[2])
    lat_bbox = (extent[1], extent[3])
    x, y = prj(lon_bbox, lat_bbox)
    # Choose the resolution. Lower the number, higher the resolution and slower the processing 
    KM_PER_DEGREE = 111.32
    # Final image size in pixels
    x_size = int(((extent[2] - extent[0]) * KM_PER_DEGREE) / resolution)
    y_size = int(((extent[3] - extent[1]) * KM_PER_DEGREE) / resolution)
    # Define the area of the plot
    area_def = geometry.AreaDefinition('Equidistant Cylindrical ', 'Plate Carree world map', 'Equidistant Cylindrical ', {'proj': 'eqc'}, x_size, y_size, [x[0], y[0], x[1], y[1]])
    # Define the swath
    swath_def = pr.geometry.SwathDefinition(lons_interp, lats_interp)
	# Get a result with the pyresample magic
    result = resample_nearest(swath_def, data, area_def, radius_of_influence=2000, fill_value=None)
    result[result >= 380] = no_data
    data = result
    #print(data)
    #print(isinstance(np.max(data),float))
    if (isinstance(np.max(data),float) == False):
        print("Invalid Data. Program finished.")
        # Put the processed file on the log
        import datetime     # Basic Date and Time types
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
        
    # Export the result to GeoTIFF ================================================
    # Get GDAL driver GeoTiff
    driver = gdal.GetDriverByName('GTiff')
    # Get dimensions
    nlines = y_size
    ncols = x_size
    nbands = len(data.shape)
    data_type = data_type
    # Create grid
    #options = ['COMPRESS=JPEG', 'JPEG_QUALITY=80', 'TILED=YES']
    date = Start[0:12]
    grid = driver.Create(main_dir + '//Output//' + satellite + '//' + product + '//' + 'JPS_' + band + '_' + date, ncols, nlines, 1, data_type)#, options)
    # Write data for each bands
    grid.GetRasterBand(1).WriteArray(data)
    # Lat/Lon WSG84 Spatial Reference System
    srs = osr.SpatialReference()
    srs.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    # Setup projection and geo-transform
    grid.SetProjection(srs.ExportToWkt())
    grid.SetGeoTransform(getGeoTransform(extent, nlines, ncols))
    #print(band + '_' + date + '.tif')
    dst_ds = driver.CreateCopy(main_dir + '//Output//' + satellite + '//' + product + '//' + 'JPS_' + band + '_' + date + '.tif', grid, 0) 
    print('Generated GeoTIFF: ', 'JPS_' + band + '_' + date + '.tif')	
    # Close the file
    srs = None
    dst_ds = None
    driver = None
    grid = None
    # Delete the grid
    os.remove(main_dir + '//Output//' + satellite + '//' + product + '//' + 'JPS_' + band  + '_' + date)     
    #print("Processing finished.")

    date_day = date[0:8] # this option takes lots of disk space! But it is possible
	
    # Create the mosaic ===========================================================
    gdal.BuildVRT(main_dir + '//Output//' + satellite + '//' + product + '//' + 'JPS_' + band + 'HA_' + date + '.vrt', sorted(glob.glob(main_dir + '//Output//' + satellite + '//' + product + '//' + 'JPS_' + band + '_' + date_day +'*.tif'), key=os.path.getmtime), srcNodata = -10)
    gdal.Translate(main_dir + '//Output//' + satellite + '//' + product + '//' + 'JPS_' + band[0:4] + 'HA_' + date + '.tif', main_dir + '//Output//' + satellite + '//' + product + '//' + 'JPS_' + band + 'HA_' + date + '.vrt')
    print('Generated GeoTIFF: ', 'JPS_' + band[0:4] + 'HA_' + date + '.tif')
    os.remove(main_dir + '//Output//' + satellite + '//' + product + '//' + 'JPS_' + band + 'HA_' + date + '.vrt')
    # Export the result to GeoTIFF ================================================
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    
    # Check if there is valid pixels in the region of interest
    mosaic = gdal.Open(main_dir + '//Output//' + satellite + '//' + product + '//' + 'JPS_' + band[0:4] + 'HA_' + date + '.tif')
    file_band = mosaic.GetRasterBand(1)
    data = file_band.ReadAsArray()
    data[data == min(data[0])] = np.nan
    
    ulx, xres, xskew, uly, yskew, yres  = mosaic.GetGeoTransform()
    lrx = ulx + (mosaic.RasterXSize * xres)
    lry = uly + (mosaic.RasterYSize * yres)
    
    #print(ulx) # min_lon
    #print(uly) # max_lat
    #print(lrx) # max_lon 
    #print(lry) # min_lat
    
    extent = [ulx, lry, lrx, uly]

    mosaic = None  

    product = band[0:4] + 'HA'
    date_file = date
    date_formated = date[0:4] + "-" + date[4:6] + "-" + date[6:8] + " " + date [8:10] + ":" + date [10:12] + " UTC"

    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    
    # Choose the resolution. Lower the number, higher the resolution and slower the processing 
    KM_PER_DEGREE = 111.32
    # Final image size in pixels
    sizex = int(((original_extent[2] - original_extent[0]) * KM_PER_DEGREE) / resolution)
    sizey = int(((original_extent[3] - original_extent[1]) * KM_PER_DEGREE) / resolution)
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    # NIGHT LIGHTS COLOR SCHEME
    
    #=====================================================================
    colors = ["#01021e", "#76614c", "#c29e6c", "#fae397", "#ffffeb"]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    cmap = cmap
    vmin = 0
    vmax = 8
    product = product.replace("B", "L")
    thick_interval = 0.5
    prod_title = 'Day Night Band (Night Lights)'
    #=====================================================================
    
    # Plot configuration
    plot_config = {
    "resolution": resolution, 
    "dpi": 150, 
    "states_color": 'white', "states_width": sizey * 0.00006, 
    "countries_color": 'gold', "countries_width": sizey * 0.00012,
    "continents_color": 'gold', "continents_width": sizey * 0.00025,
    "grid_color": 'white', "grid_width": sizey * 0.00025, "grid_interval": 10.0,
    "vmin": vmin, "vmax": vmax, "cmap": cmap,
    "title_text": "JPSS " + prod_title + " ", "title_size": int(sizex * 0.005), "title_x_offset": int(sizex * 0.01), "title_y_offset": sizey - int(sizey * 0.016),
    "thick_interval": thick_interval, "cbar_labelsize": int(sizey * 0.005), "cbar_labelpad": -int(sizey * 0.0),
    "file_name_id_1": "JPS",  "file_name_id_2": product + "_SEC"
    }

    # Choose the plot size (width x height, in inches)
    fig = plt.figure(figsize=(sizex/float(plot_config["dpi"]), sizey/float(plot_config["dpi"])), dpi=plot_config["dpi"])
    # Define the projection
    proj = ccrs.PlateCarree()
    # Use the PlateCarree projection in cartopy
    ax = plt.axes([0, 0, 1, 1], projection=proj)
    ax.set_extent([original_extent[0], original_extent[2], original_extent[1], original_extent[3]], ccrs.PlateCarree())
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
    plt.savefig(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.png', bbox_inches='tight', pad_inches=0, facecolor='black')

    # Update the animation
    nfiles = 20
    update(satellite, product, nfiles)
    #---------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------- 
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    # NIGHT CLOUDS COLOR SCHEME
    
    #=====================================================================
    cmap = 'gray'
    vmin = 0.0
    vmax = 1.0
    thick_interval = 0.1
    product = product.replace("L", "C")
    prod_title = 'Day Night Band (Clouds)'
    #=====================================================================
    
    # Plot configuration
    plot_config = {
    "resolution": resolution, 
    "dpi": 150, 
    "states_color": 'white', "states_width": sizey * 0.00006, 
    "countries_color": 'gold', "countries_width": sizey * 0.00012,
    "continents_color": 'gold', "continents_width": sizey * 0.00025,
    "grid_color": 'white', "grid_width": sizey * 0.00025, "grid_interval": 10.0,
    "vmin": vmin, "vmax": vmax, "cmap": cmap,
    "title_text": "JPSS " + prod_title + " ", "title_size": int(sizex * 0.005), "title_x_offset": int(sizex * 0.01), "title_y_offset": sizey - int(sizey * 0.016),
    "thick_interval": thick_interval, "cbar_labelsize": int(sizey * 0.005), "cbar_labelpad": -int(sizey * 0.0),
    "file_name_id_1": "JPS",  "file_name_id_2": product + "_SEC"
    }

    # Choose the plot size (width x height, in inches)
    fig = plt.figure(figsize=(sizex/float(plot_config["dpi"]), sizey/float(plot_config["dpi"])), dpi=plot_config["dpi"])
    # Define the projection
    proj = ccrs.PlateCarree()
    # Use the PlateCarree projection in cartopy
    ax = plt.axes([0, 0, 1, 1], projection=proj)
    ax.set_extent([original_extent[0], original_extent[2], original_extent[1], original_extent[3]], ccrs.PlateCarree())
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
    plt.savefig(out_dir + plot_config["file_name_id_1"] + "_" + plot_config["file_name_id_2"] + "_" + date_file + '.png', facecolor='black')#, bbox_inches='tight', pad_inches=0, facecolor='black')

    # Update the animation
    nfiles = 20
    update(satellite, product, nfiles)
    #---------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------- 
	
else:
    print("The image is not on the desired region.")

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

print('Total processing time:', round((t.time() - start_time),2), 'seconds.') 