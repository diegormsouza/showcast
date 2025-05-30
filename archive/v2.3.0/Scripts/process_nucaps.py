# -*- coding: utf-8 -*-
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
__author__ = 'Diego Enore'
__email__  = 'diego.enore@inpe.br'

from netCDF4 import Dataset, num2date

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader

from osgeo import ogr, gdal_array, gdal, osr
from affine import Affine
from rasterstats import zonal_stats
from pyresample import get_area_def

from sounding.indices import wh2o, MixR2VaporPress, DewPoint,\
    TTK, es, theta
from sounding.Showalter_index import showalter_index_bolton1
from sounding.cape import get_parcel, get_cape
from sounding.constants import Tb, Lb, gravity, Rstar_a, M
from sounding.skewt import plot_skewt
from scipy.interpolate import griddata

# Diego Souza Edits ------------------------------------------------------------
import os  
from os.path import dirname, abspath        
import time as t                                                                         
from matplotlib.image import imread  
from scipy.interpolate import interp2d  
import matplotlib.patches as mpatches
import sys                                                
import warnings
from html_update import update                               
warnings.filterwarnings("ignore")     
             
# SHOWCast directory:
main_dir = dirname(dirname(abspath(__file__)))

# Define Lat/Lon WSG84 Spatial Reference System (EPSG:4326)
LAT_LON_WGS84 = osr.SpatialReference()
LAT_LON_WGS84.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
map_provinces = main_dir + '//Shapefiles//ne_10m_admin_1_states_provinces.shp'
map_coastline = main_dir + '//Shapefiles//ne_10m_coastline.shp'
map_countries = main_dir + '//Shapefiles//ne_50m_admin_0_countries.shp'
# -------------------------------------------------------------------------------

def buildLatLonGrid(extent, sizex, sizey):
    # Build geographic area
    areaId = 'custom-area'
    areaName = 'Lat/Lon Area'
    SRID = 'EPSG:4326'
    proj4Str = '+proj=longlat +ellps=WGS84 +datum=WGS84'
    areaDefinition = get_area_def(areaId, areaName, SRID, proj4Str, sizex, sizey, extent)
    # Get grid latitudes + longitudes
    return areaDefinition.get_lonlats()

def getExtent(gt, shape):
    '''
    This function returns the extent based on the given GDAL
    geo-transform parameters and dimensions.
    '''
    llx = gt[0]
    lly = gt[3] + ((shape[0]) * gt[5])
    urx = gt[0] + ((shape[1])  * gt[1])
    ury = gt[3]
    return (llx, lly, urx, ury)

def getGeoT(extent, nlines, ncols):
    '''
    This function computes the resolution based on data dimensions.
    '''
    resx = (extent[2] - extent[0]) / ncols
    resy = (extent[3] - extent[1]) / nlines
    return [extent[0], resx, 0, extent[3] , 0, -resy]

def array2raster(array, extent, srs=LAT_LON_WGS84, nodata=None, output='', driver='MEM'):
    # Get array dimension and data type
    nlines = array.shape[0]
    ncols = array.shape[1]
    type = gdal_array.NumericTypeCodeToGDALTypeCode(array.dtype)

    # Adjust nodata values
    if nodata is not None and isinstance(array, np.ma.MaskedArray):
        array = np.ma.filled(array, nodata)
    
    # Create GDAL raster
    driver = gdal.GetDriverByName(driver)
    raster = driver.Create(output, ncols, nlines, 1, type)
    raster.SetGeoTransform(getGeoT(extent, nlines, ncols))

    # Adjust band and write
    band = raster.GetRasterBand(1)
    if nodata is not None:
        band.SetNoDataValue(nodata)
    band.WriteArray(array)

    # Adjust SRS
    if srs is not None:
        raster.SetProjection(srs.ExportToWkt())
        
    band.FlushCache()

    return raster

def cut_image(array, systems, extent):         
    # Get raster
    raster = array2raster(array, extent, nodata=-9999)
    
    # Get Affine object in order to run zonal_stats
    aff = Affine.from_gdal(*raster.GetGeoTransform())
    
    # Extract values
    values = raster.ReadAsArray()
    
    # Get no-data value
    nodata = raster.GetRasterBand(1).GetNoDataValue()

    # Compute stats for each polygon
    stats = zonal_stats(systems.ExportToWkt(), values, stats=['min', 'mean', 'std', 'count'],
                        affine=aff, nodata=nodata,
                        raster_out=True, prefix='')
    
    geoT = stats[0]['mini_raster_affine'].to_gdal()
    ny, nx = stats[0]['mini_raster_array'].shape
    ext  = getExtent(geoT, [ny, nx])
    lon, lat = buildLatLonGrid(ext, nx, ny)
    return stats[0]['mini_raster_array'], lon, lat

def extractCoordinates2NumpyArray(polygon):
    '''
    This method extract the coordinates of polygon to NumpyArray (N x 2).
    '''
    points = polygon.GetGeometryRef(0).GetPoints()
    coords = np.zeros((len(points), 2), dtype=np.float32)    
    i = 0
    for p in points:
        coords[i,0] = p[0]
        coords[i,1] = p[1]
        i += 1
    return coords

def geometry(string):
    # Get lon, lat of polygon
    split = str.split(string, ',')
    split[0]  = split[0][9:]
    split[-1] = split[-1][0:-2]
    
    # Remove blank space
    for i in range(len(split)):
        if split[i][0] == ' ':
            split[i] = split[i][1:]
    
    lon = [float(str.split(v, ' ')[0]) for v in split]
    lat = [float(str.split(v, ' ')[1]) for v in split]
    # Create ring polygon
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for i in range(len(lon)):
        ring.AddPoint(lon[i], lat[i])
    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)    
    return poly
    
def loc(vlon, vlat, px, py):
    x0 = (vlon - px)**2
    y0 = (vlat - py)**2
    
    x = np.nonzero(x0 == np.min(x0))[0][0]
    y = np.nonzero(y0 == np.min(y0))[0][0]
    return x, y

def plot_map(pos, title, extent, nlon, nlat, var, vmin, vmax):
    delta=2
    new_ext = [ extent[0]-delta, extent[2]+delta, extent[1]-delta, extent[3]+delta ]
    #pos = [left, bottom, width, height]
    ax = plt.axes(pos, projection = proj)
    ax.set_title(title)
    ax.set_extent(new_ext, proj)

    # Add a background image
    ax.stock_img()
    fname = os.path.join(main_dir + '//Maps//', 'natural-earth-1_large2048px.jpg')
    ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=2)

    # Plot the var
    im = ax.pcolormesh(nlon, nlat, var, vmin=vmin, vmax=vmax, cmap='jet', transform=proj, zorder=3)

    # Plot the states
    shapefile = list(shpreader.Reader(map_provinces).geometries())
    ax.add_geometries(shapefile, proj, edgecolor='black',facecolor='none', linewidth=0.1, zorder=4)
    # Add countries
    shapefile = list(shpreader.Reader(map_countries).geometries())
    ax.add_geometries(shapefile, proj, edgecolor='black',facecolor='none', linewidth=0.2, zorder=5)
    # Add continents
    shapefile = list(shpreader.Reader(map_coastline).geometries())
    ax.add_geometries(shapefile, proj, edgecolor='black',facecolor='none', linewidth=0.6, zorder=6)
	
    # Plot colorbar
    ax_divider = make_axes_locatable(ax)
    cax = ax_divider.append_axes("bottom", size="10%", pad="15%",axes_class=plt.Axes)
    plt.colorbar(im, cax=cax, orientation='horizontal')

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Start the time counter
print('Script started.')
start = t.time()  

# Fila name
arq = (sys.argv[1])
path = arq

# Open data
nc  = Dataset(arq, 'r')
lat = nc.variables['Latitude'][:]
lon = nc.variables['Longitude'][:]
par = nc.variables['Pressure'][:]             # hPa
tar = nc.variables['Temperature'][:]          # K
mix = nc.variables['H2O_MR'][:]               # Kg/kg
qlt = nc.variables['Quality_Flag'][:]
ttt = nc.variables['Time']


# Verifying if the granule is inside the region of interest
extent_user = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]

inside = False

print("Monitored Extent: ")
print("Min Lon: ", extent_user[0])
print("Min Lat: ", extent_user[1])
print("Max Lon: ", extent_user[2])
print("Max Lat: ", extent_user[3])

print("Granule Extent: ")
print("Min Lon: ", min(lon[:]))
print("Min Lat: ", max(lon[:]))
print("Max Lon: ", min(lat[:]))
print("Max Lat: ", max(lat[:]))

print("Result: ")
if (extent_user[0] <= min(lon[:]) <= extent_user[2]) or (extent_user[0] <= max(lon[:]) <= extent_user[2]):
	if (extent_user[1] <= min(lat[:]) <= extent_user[3]) or (extent_user[1] <= max(lat[:]) <= extent_user[3]):
		inside = True
		print("The granule is on the monitored region.")
	else:
		print("The granule is not on the monitored region.")
else:
	print("The granule is not on the monitored region.")
	
if (inside == True):	
	
	# Parameters geographic
	geospatial_bounds = geometry(nc.geospatial_bounds)
	geo_array         = extractCoordinates2NumpyArray(geospatial_bounds)
	extent            = [min(lon), min(lat), max(lon), max(lat)]
	tempo             = num2date(ttt[:], ttt.units, ttt.calendar)
	nc.close()

	# Criando matriz interpolada de dados
	region = [lon.min(), lon.max(), lat.min(), lat.max()]

	# Informations to map
	proj = ccrs.PlateCarree() # Define the projection

	# Dimensão da matriz
	nf, nz = np.shape(par)

	# Calculando coisas
	hg = np.zeros(nf)       # Altura geopotencial
	ea = np.zeros((nf, nz)) # Pressão parcial de vapor
	ed = np.zeros((nf, nz)) # Pressão parcial de ar seco
	rh = np.zeros((nf, nz)) # Umidade Relativa
	td = np.zeros((nf, nz)) # Temperatura do ponto de orvalho
	ik = np.zeros(nf) 		# Índice K
	tt = np.zeros(nf) 		# Índice Total Totals
	wp = np.zeros(nf)       # Água Precipitável
	sw = np.zeros(nf)       # Índice Showalter

	cp = np.zeros((nf, 3))  # CAPE (ML, SB, MU)
	ci = np.zeros((nf, 3))  # CINE (ML, SB, MU)
	for i in range(nf):
		# Calculando altura
		hg=1000*(Tb/((par[i, :]/1100)**((Rstar_a*Lb/gravity*M)))-Tb)/Lb
		# Calculando pressão parcial do vapor de água
		ea[i, :] = MixR2VaporPress(mix[i, :], par[i, :]*100)
		# Calculando a pressão parcial de ar seco
		ed[i, :] = es(tar[i, :]-273.15)
		# Calculando a umidade relativa
		rh[i, :] = (ea[i, :]/ed[i, :])*100
		# Calculando Temperatura do ponto de orvalho
		td[i, :] = DewPoint(ea[i, :])
		# Calculando Índice K e Total Totals
		ik[i], tt[i] = TTK(tar[i, :]-273.15, par[i, :], td[i, :])
		# Calculando água precipitável
		wp[i] = wh2o(par[i, :][::-1],tar[i, :][::-1]-273.15,td[i, :][::-1])
		# Calculando Showalter entre 850 e 500 hPa
		aa = (par[i, :] - 850) ** 2
		bb = np.nonzero(aa == min(aa))
		t_lower = tar[i, bb]-273
		td_lower = td[i, bb]
		cc = (par[i, :] - 500) ** 2
		dd = np.nonzero(cc == min(cc))
		t_upper = tar[i, dd]-273
		td_upper = td[i, dd]
		sw[i] = showalter_index_bolton1(t_lower, t_upper, td_lower, p_lower=850.0, p_upper=500.0)[0]
		# Calculando CAPE e CINE
		# Automatically generate a parcel based on the sounding characteristics
		#     Escolha um dos seguintes tipos de parcela:
		#     - Mixed Layer  : 'ml'
		#     - Surface Based: 'sb'
		#     - Most Unstable: 'mu'
		method = ('ml', 'sb', 'mu')
		count=0
		for met in method:
			dtemp = tar[i, :] - td[i, :]
			if np.any(dtemp <= 0):
				cp[i, count] = np.nan
				ci[i, count] = np.nan       
				continue
			# Obtem informacoes termodinamicas das parcelas para os tres tipos de parcela considerados
			info_parcel = get_parcel(hg[::-1], par[i, :][::-1], tar[i, :][::-1]-273.15, td[i, :][::-1], met)
			startp, startt, startdp = info_parcel[0], info_parcel[1], info_parcel[2]
			if startt <= startdp:
				cp[i, count] = np.nan
				ci[i, count] = np.nan
			else:
				calc = get_cape(hg[::-1], par[i, :][::-1], tar[i, :][::-1]-273.15, td[i, :][::-1], startp, startt, startdp, totalcape=True)
				cp[i, count] = calc[3]
				ci[i, count] = calc[4]
			count+=1

	vlon = np.arange(region[0], region[1], .25)
	vlat = np.arange(region[3], region[2], -.25)

	mlon, mlat = np.meshgrid(vlon, vlat)
	# CAPE (Mixed Layer) - J.Kg-1
	cpml=griddata((lon, lat), cp[:, 0], (mlon, mlat), method='nearest')
	cpml, nlon, nlat = cut_image(cpml, geospatial_bounds, [mlon.min(), mlat.min(), mlon.max(), mlat.max()])

	# CAPE (Surface Based) - J.Kg-1
	cpsb=griddata((lon, lat), cp[:, 1], (mlon, mlat), method='nearest')
	cpsb, _, _ = cut_image(cpsb, geospatial_bounds, [mlon.min(), mlat.min(), mlon.max(), mlat.max()])

	# CAPE (Most Unstable) - J.Kg-1
	cpmu=griddata((lon, lat), cp[:, 2], (mlon, mlat), method='nearest')
	cpmu, _, _ = cut_image(cpmu, geospatial_bounds, [mlon.min(), mlat.min(), mlon.max(), mlat.max()])

	# CINE - J.Kg-1
	cine=griddata((lon, lat), ci[:, 2], (mlon, mlat), method='nearest')
	cine, _, _ = cut_image(cine, geospatial_bounds, [mlon.min(), mlat.min(), mlon.max(), mlat.max()])

	# Precipitable Water - Kg.m-2 - mm
	prec=griddata((lon, lat), wp, (mlon, mlat), method='nearest')
	prec, _, _ = cut_image(prec, geospatial_bounds, [mlon.min(), mlat.min(), mlon.max(), mlat.max()])

	# Showalter Index - Celsius degrees
	show=griddata((lon, lat), sw, (mlon, mlat), method='nearest')
	show, _, _ = cut_image(show, geospatial_bounds, [mlon.min(), mlat.min(), mlon.max(), mlat.max()])

	# K Index - Celsius degrees
	kind=griddata((lon, lat), ik, (mlon, mlat), method='nearest')
	kind, _, _ = cut_image(kind, geospatial_bounds, [mlon.min(), mlat.min(), mlon.max(), mlat.max()])

	# Total Totals - Celsius degrees
	ttin=griddata((lon, lat), tt, (mlon, mlat), method='nearest')
	ttin, _, _ = cut_image(ttin, geospatial_bounds, [mlon.min(), mlat.min(), mlon.max(), mlat.max()])

	for i in range(len(lon)):
	
		#print("")
		#print("Current Lon: ", lon[i])
		#print("Min Lon:", extent_user[0])
		#print("Max Lon:", extent_user[2])
		
		#print("Current Lat: ",lat[i])
		#print("Min Lat:", extent_user[1])
		#print("Max Lat:", extent_user[3])
		
		# Checking if the data point is inside the monitor region:		
		if (extent_user[0] <= lon[i] <= extent_user[2]):
			if (extent_user[1] <= lat[i] <= extent_user[3]):
				print("Plotting NUCAPS on the following coordinate:", lat[i], lon[i])
				
				# Plotando Skew-T
				sounding = np.zeros((len(par[0, :]), 11))
				sounding[:, 0] = par[i, :][::-1]
				sounding[:, 1] = hg[::-1]
				sounding[:, 2] = tar[i, :][::-1]-273.15
				sounding[:, 3] = td[i, :][::-1]
				sounding[:, 4] = rh[i, :][::-1]
				sounding[:, 5] = mix[i, :][::-1]*1000.
				sounding[:, 6] = 0
				sounding[:, 7] = 0
				sounding[:, 8] = theta(tar[i, :][::-1], par[i, :][::-1])
				sounding[:, 9] = 0
				sounding[:, 10] = 0
				
				columns = [
					"pressure",     # hPa
					"height",       # meters
					"temperature",  # C
					"dewpoint",     # C
					"rh",           # %
					"mixing_ratio", # g/kg
					"direction",    # degrees
					"sknt",         # knots
					"theta",        # K
					"us",           # m/s
					"vs",           # m/s
				]
					
				sound = pd.DataFrame(sounding, columns=columns)
				
				fig = plt.figure(1, figsize=(14, 8))
				# Skew-T
				#             x   y   tx  ty
				ax = plt.axes([0.08, 0.07, 0.44, 0.85])
				titulo = 'NUCAPS - {}             lat: {:02.2f} lon: {:03.2f}'.format(
					tempo[i].strftime('%Y/%m/%d %H:%M:%S UTC'), lat[i], lon[i])
				plot_skewt(sound, ax=ax, title=titulo,
								  lift_parcel=True, plot_winds=False, diags=["CAPE", ],
								  label_altitudes=True)
				
				# Plot Points of pixels---------------------------------------
				indval = np.nonzero(qlt == 0)
				indinv = np.nonzero(qlt == 1)
				indpre = np.nonzero(qlt == 9)
				
				lon_valid, lat_valid = lon[indval], lat[indval]
				lon_inval, lat_inval = lon[indinv], lat[indinv]
				lon_inpre, lat_inpre = lon[indpre], lat[indpre]
				
				ax = plt.axes([0.37, 0.798, 0.15, 0.15], projection=proj)
				
				# Add a background image
				#ax.stock_img()
				fname = os.path.join(main_dir + '//Maps//', 'natural-earth-1_large2048px.jpg')
				ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=2)
				
				ax.add_patch(mpatches.Rectangle(xy=[extent_user[0], extent_user[1]], width=extent_user[2]-extent_user[0], height=extent_user[3]-extent_user[1], fill = True, facecolor='orange', alpha=0.6, transform=ccrs.PlateCarree(), zorder = 3))
				
				ax.plot(lon_valid, lat_valid, color='green', marker='o', markersize=3, linestyle = 'None', transform=ccrs.Geodetic(), zorder=4) 
				ax.plot(lon_inval, lat_inval, color='yellow', marker='o', markersize=3, linestyle = 'None', transform=ccrs.Geodetic(), zorder=5) 
				ax.plot(lon_inpre, lat_inpre, color='red', marker='o', markersize=3, linestyle = 'None', transform=ccrs.Geodetic(), zorder=6) 
				
				ax.plot(lon[i], lat[i], color='darkred', marker='o', markerfacecolor='None', linestyle = 'None', markersize=4, transform=ccrs.Geodetic(), zorder=7) 
				
				# Add states and provinces
				shapefile = list(shpreader.Reader(map_provinces).geometries())
				ax.add_geometries(shapefile, proj, edgecolor='black',facecolor='none', linewidth=0.1, zorder=8)
				# Add countries
				shapefile = list(shpreader.Reader(map_countries).geometries())
				ax.add_geometries(shapefile, proj, edgecolor='black',facecolor='none', linewidth=0.2, zorder=9)    
				# Add continents
				shapefile = list(shpreader.Reader(map_coastline).geometries())
				ax.add_geometries(shapefile, proj, edgecolor='black',facecolor='none', linewidth=0.6, zorder=10)    
				ax.set_extent([min(lon)-2, max(lon)+2, min(lat)-2, max(lat)+2], ccrs.PlateCarree())
				
				# Plot map indicating position granule----------------------
				lon_map, lat_map = geo_array[:, 0], geo_array[:, 1]
				ax = plt.axes([0.3215, 0.579, 0.247, 0.247], projection=proj)
				
				# Add a background image
				#ax.stock_img()
				fname = os.path.join(main_dir + '//Maps//', 'natural-earth-1_large2048px.jpg')
				ax.imshow(imread(fname), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90], zorder=2)
				
				ax.add_patch(mpatches.Rectangle(xy=[extent_user[0], extent_user[1]], width=extent_user[2]-extent_user[0], height=extent_user[3]-extent_user[1], fill = True, facecolor='orange', alpha=0.6, transform=ccrs.PlateCarree(), zorder = 3))
				
				# Plot the granule
				ax.set_extent([-175, -5, -80, 80], proj)
				ax.plot(geo_array[:, 0], geo_array[:, 1], '-r', transform=ccrs.Geodetic(), zorder=4) 
			
				# Add states and provinces
				shapefile = list(shpreader.Reader(map_provinces).geometries())
				ax.add_geometries(shapefile, proj, edgecolor='gray',facecolor='none', linewidth=0.1, zorder=5)
				# Add countries
				shapefile = list(shpreader.Reader(map_countries).geometries())
				ax.add_geometries(shapefile, proj, edgecolor='black',facecolor='none', linewidth=0.15, zorder=6)    
				# Add continents
				shapefile = list(shpreader.Reader(map_coastline).geometries())
				ax.add_geometries(shapefile, proj, edgecolor='black',facecolor='none', linewidth=0.2, zorder=7)    
				
				transform = ccrs.PlateCarree()._as_mpl_transform(ax)
				
				ax.plot(-168.00, -42.00, color='green', marker='o', linestyle = 'None', markersize=4, transform=ccrs.Geodetic(), zorder=8)
				ax.annotate('Clear or Partly Cloudy', xy=(-162.00, -38.00), xycoords=transform, fontsize=7, ha='left', va='top')
			
				ax.plot(-168.00, -52.00, color='yellow', marker='o', linestyle = 'None', markersize=4, transform=ccrs.Geodetic(), zorder=8)
				ax.annotate('Cloudy Conditions', xy=(-162.00, -48.00), xycoords=transform, fontsize=7, ha='left', va='top')
				
				ax.plot(-168.00, -62.00, color='red', marker='o', linestyle = 'None', markersize=4, transform=ccrs.Geodetic(), zorder=8)				
				ax.annotate('Precipitating Cloudy', xy=(-162.00, -58.00), xycoords=transform, fontsize=7, ha='left', va='top')
				
				# Precipitable Water
				vmin=0
				vmax=80
				plot_map([0.53, 0.62, .2, .4], r'Precipitable Water (Kg.m$^-$$^2$)', extent, nlon, nlat, prec, vmin, vmax)
				# Showalter index
				vmin=-20
				vmax=20
				plot_map([0.53, 0.40, .2, .4], 'Showalter Index (C)', extent, nlon, nlat, show, vmin, vmax)
				# K index
				vmin=0
				vmax=50
				plot_map([0.53, 0.18, .2, .4], 'K Index (C)', extent, nlon, nlat, kind, vmin, vmax)
				# TT index
				vmin=1
				vmax=70
				plot_map([0.53, -0.04, .2, .4], 'Total Totals Index (C)', extent, nlon, nlat, ttin, vmin, vmax)
				# CAPE ML Index
				vmin=0
				vmax=1500
				plot_map([0.75, 0.62, .2, .4], r'CAPE ML (J.Kg$^-$$^1$)', extent, nlon, nlat, cpml, vmin, vmax)
				# CAPE SB Index
				vmin=0
				vmax=1000
				plot_map([0.75, 0.40, .2, .4], 'CAPE SB (J.Kg$^-$$^1$)', extent, nlon, nlat, cpsb, vmin, vmax)
				# CAPE MU INDEX
				vmin=0
				vmax=5000
				plot_map([0.75, 0.18, .2, .4], 'CAPE MU (J.Kg$^-$$^1$)', extent, nlon, nlat, cpmu, vmin, vmax)
				# CINE
				vmin=-1000
				vmax=0
				plot_map([0.75, -0.04, .2, .4], 'CINE (J.Kg$^-$$^1$)', extent, nlon, nlat, cine, vmin, vmax)

				# Insert logo inpe    
				#my_logo = plt.imread(main_dir + '//Logos//my_logo.png')
				#newax = fig.add_axes([0.01, 0.03, 0.10, 0.10], anchor='SW', zorder=1) #  [left, bottom, width, height]. All quantities are in fractions of figure width and height.
				#newax.imshow(my_logo)
				#newax.axis('off')

				im = plt.imread(main_dir + '//Logos//inpe_cptec.jpg')
				ax = fig.add_axes([0.92, -.02, 0.07, 0.07], anchor='NE', zorder=-1)
				plt.setp(plt.gca(), frame_on=False, xticks=(), yticks=())
				ax.imshow(im)
				
				#im = plt.imread('inpe_cptec.jpg')
				#im = plt.imread(main_dir + '//Logos//my_logo.png')
				#ax = fig.add_axes([0.92, 0.0, 0.06, 0.06], anchor='NE', zorder=-1)
				#plt.setp(plt.gca(), frame_on=False, xticks=(), yticks=())
				#ax.imshow(im)
				
				#---------------------------------------------------------------------------------------------
				#---------------------------------------------------------------------------------------------
				satellite = 'N20'
				product = 'NUCAPS_SEC'
				
				# Create the satellite output directory if it doesn't exist
				out_dir = main_dir + '//Output//' + satellite
				if not os.path.exists(out_dir):
					os.mkdir(out_dir)

				# Create the product output directory if it doesn't exist
				out_dir = main_dir + '//Output//' + satellite + '//' + product + '//'
				if not os.path.exists(out_dir):
					os.mkdir(out_dir)
				#---------------------------------------------------------------------------------------------
				#---------------------------------------------------------------------------------------------
   
				# Save fig
				plt.savefig(out_dir + 'N20_NUCAPS_SEC_' + tempo[i].strftime('%Y%m%d%H%M%S') + '_' + str(i).zfill(2) + '.png'.format(i), bbox_inches='tight', pad_inches=0)
				
				# Update the animation
				nfiles = 60
				update(satellite, product, nfiles)

				#plt.show()
				plt.clf()
				plt.close('all')
				
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

