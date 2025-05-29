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
# If not, see http://www.gnu.org/licenses/.
#######################################################################################################
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Required Libraries 
import glob       # Unix style pathname pattern expansion
import os         # Miscellaneous operating system interfaces
import sys        # Import the "system specific parameters and functions" module
import datetime   # Basic Date and Time types
import time as t  # Time access and conversion
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
start = t.time()  # Start the time counter
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Select the products that will be processed:

# GOES-16 - ABI INDIVIDUAL BANDS
g16_band02_fdk = True # GOES-16 L2 CMI - Band 02 - FULL DISK 
g16_band02_sec = True # GOES-16 L2 CMI - Band 02 - USER SECTOR 
g16_band07_fdk = True # GOES-16 L2 CMI - Band 07 - FULL DISK 
g16_band07_sec = True # GOES-16 L2 CMI - Band 07 - USER SECTOR 
g16_band08_fdk = True # GOES-16 L2 CMI - Band 08 - FULL DISK 
g16_band08_sec = True # GOES-16 L2 CMI - Band 08 - USER SECTOR 
g16_band09_fdk = True # GOES-16 L2 CMI - Band 09 - FULL DISK 
g16_band09_sec = True # GOES-16 L2 CMI - Band 09 - USER SECTOR 
g16_band13_fdk = True # GOES-16 L2 CMI - Band 13 - FULL DISK 
g16_band13_sec = True # GOES-16 L2 CMI - Band 13 - USER SECTOR 
g16_band14_fdk = True # GOES-16 L2 CMI - Band 14 - FULL DISK 
g16_band14_sec = True # GOES-16 L2 CMI - Band 14 - USER SECTOR 
g16_band15_fdk = True # GOES-16 L2 CMI - Band 15 - FULL DISK 
g16_band15_sec = True # GOES-16 L2 CMI - Band 15 - USER SECTOR 

# GOES-16 - BANDS COMPOSITES / MULTISPECTRAL IMAGERY / GLM
g16_fcolor_fdk = True # GOES-16 False Color - Band 02 and Band 13 - FULL DISK 
g16_fcolor_sec = True # GOES-16 False Color - Band 02 and Band 13 - USER SECTOR 
g16_ircl13_fdk = True # GOES-16 IR Clouds - Band 13 with Blue Marble - FULL DISK 
g16_ircl13_sec = True # GOES-16 IR Clouds - Band 13 with Blue Marble - USER SECTOR 
g16_irce13_fdk = True # GOES-16 IR Clouds Enhanced - Band 13 [enhanced] with Blue Marble - FULL DISK 
g16_irce13_sec = True # GOES-16 IR Clouds Enhanced - Band 13 [enhanced] with Blue Marble - USER SECTOR 
g16_swdiff_fdk = True # GOES-16 Split Window Difference - FULL DISK
g16_swdiff_sec = True # GOES-16 Split Window Difference - USER SECTOR
g16_glmirc_fdk = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (5 min density) - FULL DISK
g16_glmirc_sec = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (5 min density) - USER SECTOR

# GOES-16 RGB COMPOSITES
g16_armrgb_fdk = True # GOES-16 Airmass RGB - FULL DISK
g16_armrgb_sec = True # GOES-16 Airmass RGB - USER SECTOR
g16_clprgb_fdk = True # GOES-16 Cloud Phase RGB - FULL DISK
g16_clprgb_sec = True # GOES-16 Cloud Phase RGB - USER SECTOR
g16_conrgb_fdk = True # GOES-16 Convection RGB - FULL DISK
g16_conrgb_sec = True # GOES-16 Convection RGB - USER SECTOR
g16_dcprgb_fdk = True # GOES-16 Day Cloud Phase RGB - FULL DISK
g16_dcprgb_sec = True # GOES-16 Day Cloud Phase RGB - USER SECTOR
g16_dlcrgb_fdk = True # GOES-16 Day Land Cloud RGB - FULL DISK
g16_dlcrgb_sec = True # GOES-16 Day Land Cloud RGB - USER SECTOR
g16_dmprgb_fdk = True # GOES-16 Day Microphysics RGB - FULL DISK
g16_dmprgb_sec = True # GOES-16 Day Microphysics RGB - USER SECTOR
g16_dstrgb_fdk = True # GOES-16 Dust RGB - FULL DISK
g16_dstrgb_sec = True # GOES-16 Dust RGB - USER SECTOR
g16_nmprgb_fdk = True # GOES-16 Night Microphysics RGB - FULL DISK
g16_nmprgb_sec = True # GOES-16 Night Microphysics RGB - USER SECTOR
g16_ntcrgb_fdk = True # GOES-16 Natural True Color RGB - FULL DISK
g16_ntcrgb_sec = True # GOES-16 Natural True Color RGB - USER SECTOR
g16_trurgb_fdk = True # GOES-16 True Color RGB - FULL DISK
g16_trurgb_sec = True # GOES-16 True Color RGB - USER SECTOR

# GOES-16 BASELINE PRODUCTS
g16_cldhgt_fdk = True # GOES-16 L2 ACHAF - Cloud Top Height - FULL DISK
g16_cldhgt_sec = True # GOES-16 L2 ACHAF - Cloud Top Height - USER SECTOR
g16_cldtmp_fdk = True # GOES-16 L2 ACHTF - Cloud Top Temperature - FULL DISK
g16_cldtmp_sec = True # GOES-16 L2 ACHTF - Cloud Top Temperature - USER SECTOR
g16_cldmsk_fdk = True # GOES-16 L2 ACMF - Clear Sky Masks - FULL DISK
g16_cldmsk_sec = True # GOES-16 L2 ACMF - Clear Sky Masks - USER SECTOR
g16_cldpha_fdk = True # GOES-16 L2 ACTPF - Cloud Top Phase - FULL DISK
g16_cldpha_sec = True # GOES-16 L2 ACTPF - Cloud Top Phase - USER SECTOR
g16_aerdet_fdk = True # GOES-16 L2 ADPF - Aerosol Detection - FULL DISK
g16_aerdet_sec = True # GOES-16 L2 ADPF - Aerosol Detection - USER SECTOR
g16_aeropt_fdk = True # GOES-16 L2 AODF - Aerosol Optical Depth - FULL DISK
g16_aeropt_sec = True # GOES-16 L2 AODF - Aerosol Optical Depth - USER SECTOR
g16_cldopt_fdk = True # GOES-16 L2 CODF - Cloud Optical Depth - FULL DISK
g16_cldopt_sec = True # GOES-16 L2 CODF - Cloud Optical Depth - USER SECTOR
g16_cldpas_fdk = True # GOES-16 L2 CPSF - Cloud Particle Size - FULL DISK
g16_cldpas_sec = True # GOES-16 L2 CPSF - Cloud Particle Size - USER SECTOR
g16_cldpre_fdk = True # GOES-16 L2 CTPF - Cloud Top Pressure - FULL DISK
g16_cldpre_sec = True # GOES-16 L2 CTPF - Cloud Top Pressure - USER SECTOR
g16_dmwf14_fdk = True # GOES-16 L2 DMWF-C14 - Derived Motion Winds Band 14 - FULL DISK
g16_dmwf14_sec = True # GOES-16 L2 DMWF-C14 - Derived Motion Winds Band 14 - USER SECTOR
g16_dsifpr_fdk = True # GOES-16 L2 DSIF - Derived Stability Index - FULL DISK
g16_dsifpr_sec = True # GOES-16 L2 DSIF - Derived Stability Index - USER SECTOR
g16_dsradi_fdk = True # GOES-16 L2 DSRF - Downward Shortwave Radiation - FULL DISK
g16_dsradi_sec = True # GOES-16 L2 DSRF - Downward Shortwave Radiation - USER SECTOR
g16_firmsk_fdk = True # GOES-16 L2 FDCF - Fire-Hot Spot Characterization - FULL DISK
g16_firmsk_sec = True # GOES-16 L2 FDCF - Fire-Hot Spot Characterization - USER SECTOR
g16_snowco_fdk = True # GOES-16 L2 FSCF - Snow Cover - FULL DISK
g16_snowco_sec = True # GOES-16 L2 FSCF - Snow Cover - USER SECTOR
g16_lstskn_fdk = True # GOES-16 L2 LSTF - Land Surface (Skin) Temperature - FULL DISK
g16_lstskn_sec = True # GOES-16 L2 LSTF - Land Surface (Skin) Temperature - USER SECTOR
g16_rrqpef_fdk = True # GOES-16 L2 RRQPEF - Rainfall Rate - Quanti Pred. Estim - FULL DISK
g16_rrqpef_sec = True # GOES-16 L2 RRQPEF - Rainfall Rate - Quanti Pred. Estim - USER SECTOR
g16_rsradi_fdk = True # GOES-16 L2 RSRF - Reflected Shortwave Radiation - FULL DISK
g16_rsradi_sec = True # GOES-16 L2 RSRF - Reflected Shortwave Radiation - USER SECTOR
g16_sstskn_fdk = True # GOES-16 L2 SSTF - Sea Surface (Skin) Temperature - FULL DISK
g16_sstskn_sec = True # GOES-16 L2 SSTF - Sea Surface (Skin) Temperature - USER SECTOR
g16_totpwa_fdk = True # GOES-16 L2 TPWF - Total Precipitable Water - FULL DISK
g16_totpwa_sec = True # GOES-16 L2 TPWF - Total Precipitable Water - USER SECTOR
g16_vaafpr_fdk = True # GOES-16 L2 VAAF - Volcanic Ash - FULL DISK
g16_vaafpr_sec = True # GOES-16 L2 VAAF - Volcanic Ash - USER SECTOR

# GOES-17 - ABI INDIVIDUAL BANDS
g17_band02_fdk = True # GOES-17 L2 CMI - Band 02 - FULL DISK 
g17_band02_sec = True # GOES-17 L2 CMI - Band 02 - USER SECTOR 
g17_band07_fdk = True # GOES-17 L2 CMI - Band 07 - FULL DISK 
g17_band07_sec = True # GOES-17 L2 CMI - Band 07 - USER SECTOR 
g17_band08_fdk = True # GOES-17 L2 CMI - Band 08 - FULL DISK 
g17_band08_sec = True # GOES-17 L2 CMI - Band 08 - USER SECTOR 
g17_band09_fdk = True # GOES-17 L2 CMI - Band 09 - FULL DISK 
g17_band09_sec = True # GOES-17 L2 CMI - Band 09 - USER SECTOR 
g17_band13_fdk = True # GOES-17 L2 CMI - Band 13 - FULL DISK 
g17_band13_sec = True # GOES-17 L2 CMI - Band 13 - USER SECTOR 
g17_band14_fdk = True # GOES-17 L2 CMI - Band 14 - FULL DISK 
g17_band14_sec = True # GOES-17 L2 CMI - Band 14 - USER SECTOR 
g17_band15_fdk = True # GOES-17 L2 CMI - Band 15 - FULL DISK 
g17_band15_sec = True # GOES-17 L2 CMI - Band 15 - USER SECTOR 

# GOES-17 - BANDS COMPOSITES / MULTISPECTRAL IMAGERY
g17_fcolor_fdk = True # GOES-17 False Color - Band 02 and Band 13 - FULL DISK 
g17_fcolor_sec = True # GOES-17 False Color - Band 02 and Band 13 - USER SECTOR 
g17_ircl13_fdk = True # GOES-17 IR Clouds - Band 13 with Blue Marble - FULL DISK 
g17_ircl13_sec = True # GOES-17 IR Clouds - Band 13 with Blue Marble - USER SECTOR 
g17_irce13_fdk = True # GOES-17 IR Clouds Enhanced - Band 13 [enhanced] with Blue Marble - FULL DISK 
g17_irce13_sec = True # GOES-17 IR Clouds Enhanced - Band 13 [enhanced] with Blue Marble - USER SECTOR 
g17_swdiff_fdk = True # GOES-17 Split Window Difference - FULL DISK 
g17_swdiff_sec = True # GOES-17 Split Window Difference - USER SECTOR

# METEOSAT PRODUCTS (YOU MAY SELECT WHICH MSG SUBPRODUCT YOU WANT TO PROCESS INSIDE THE PYTHON SCRIPT!)
msg_produc_fdk = True # METEOSAT Bands and RGB's - FULL DISK
msg_produc_sec = True # METEOSAT Bands and RGB's - USER SECTOR

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Python environment
python_env = sys.argv[1]

# GEONETCast-Americas ingestion directory
gnc_dir = sys.argv[2]

# Max number of unprocessed files the script will process at the same run
max_files = 1
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#######################################################################################################
# FILE PROCESSING AND LOG FUNCTION
#######################################################################################################
def procProduct(prod_dir, identifier, composite, script, min_lon, min_lat, max_lon, max_lat, resolution):
    # Create the list that will store the file names
    gnc_files = []
    
    # Add to the list the files in the dir that matches the identifier
    for filename in sorted(glob.glob(prod_dir+identifier)):
        gnc_files.append(filename + composite)
    
    # Keep on the list only the max number of files
    gnc_files = gnc_files[-max_files:]
    
    # If the gnc log file doesn't exist yet, create one
    file = open('..//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a')
    file.close()

    # Put all file names on the gnc log in a list
    log = []
    with open('..//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt') as f:
        log = f.readlines()
 
    # Remove the line feeds
    log = [x.strip() for x in log]
 
    # Compare the gnc file list with the log
    # Loop through all the files
    for x in gnc_files:
    # If a file is not on the log, process it
      if x not in log:
          print('Processing product:\n', x)
          print('Script used:\n', script)
          global prod_count
          prod_count = prod_count + 1
          os.system(script + ' ' + x + ' ' + str(min_lon) + ' ' + str(min_lat) + ' ' + str(max_lon) + ' ' + str(max_lat) + ' ' + str(resolution))
          print('\n')          
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
print("\n")
print("############## SHOWCAST MONITOR STARTED ##############")
print("Started at:", datetime.datetime.now())
print("\n")

# Create a counter to identify how many products have been processed in the run
prod_count = 0

# Identifier for channel composites
composite = ''

# Extent init
extent = [0.0, 0.0, 0.0, 0.0]
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#######################################################################################################
# GOES-16 L2 CMI - Band 02 - FULL DISK 
#######################################################################################################
if g16_band02_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band02//'
    identifier = '*L2-CMIPF-M*C02_G16*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

#######################################################################################################
# GOES-16 L2 CMI - Band 02 - USER SECTOR 
#######################################################################################################
if g16_band02_sec:
    max_files = 1
    extent = [-54.0, -28.0, -43.0, -18.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 1 # Max Res.: 1 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band02//'
    identifier = '*L2-CMIPF-M*C02_G16*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g1X_bands_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	
    
#######################################################################################################
# GOES-16 L2 CMI - Band 07 - FULL DISK 
#######################################################################################################
if g16_band07_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km    
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band07//'
    identifier = '*L2-CMIPF-M*C07_G16*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	
    
#######################################################################################################
# GOES-16 L2 CMI - Band 07 - USER SECTOR 
#######################################################################################################
if g16_band07_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band07//'
    identifier = '*L2-CMIPF-M*C07_G16*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g1X_bands_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	
    
#######################################################################################################
# GOES-16 L2 CMI - Band 08 - FULL DISK 
#######################################################################################################
if g16_band08_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band08//'
    identifier = '*L2-CMIPF-M*C08_G16*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

#######################################################################################################
# GOES-16 L2 CMI - Band 08 - USER SECTOR 
#######################################################################################################
if g16_band08_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band08//'
    identifier = '*L2-CMIPF-M*C08_G16*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g1X_bands_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	
    
#######################################################################################################
# GOES-16 L2 CMI - Band 09 - FULL DISK 
#######################################################################################################
if g16_band09_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band09//'
    identifier = '*L2-CMIPF-M*C09_G16*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

#######################################################################################################
# GOES-16 L2 CMI - Band 09 - USER SECTOR 
#######################################################################################################
if g16_band09_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band09//'
    identifier = '*L2-CMIPF-M*C09_G16*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g1X_bands_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	
    
#######################################################################################################
# GOES-16 L2 CMI - Band 13 - FULL DISK 
#######################################################################################################
if g16_band13_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G16*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

#######################################################################################################
# GOES-16 L2 CMI - Band 13 - USER SECTOR 
#######################################################################################################
if g16_band13_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G16*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g1X_bands_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	
    
#######################################################################################################
# GOES-16 L2 CMI - Band 14 - FULL DISK 
#######################################################################################################
if g16_band14_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km   
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band14//'
    identifier = '*L2-CMIPF-M*C14_G16*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

#######################################################################################################
# GOES-16 L2 CMI - Band 14 - USER SECTOR 
#######################################################################################################
if g16_band14_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band14//'
    identifier = '*L2-CMIPF-M*C14_G16*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g1X_bands_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	
    
#######################################################################################################
# GOES-16 L2 CMI - Band 15 - FULL DISK 
#######################################################################################################
if g16_band15_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band15//'
    identifier = '*L2-CMIPF-M*C15_G16*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	    

#######################################################################################################
# GOES-16 L2 CMI - Band 15 - USER SECTOR 
#######################################################################################################
if g16_band15_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band15//'
    identifier = '*L2-CMIPF-M*C15_G16*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g1X_bands_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GOES-16 False Color - Band 02 and Band 13 - FULL DISK
#######################################################################################################
if g16_fcolor_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 1 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band02//'
    identifier = '*L2-CMIPF-M*C02_G16*.nc'
    composite = '_FCO'
    script = python_env + 'python process_g1X_false_color_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 False Color - Band 02 and Band 13 - USER SECTOR 
#######################################################################################################
if g16_fcolor_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band02//'
    identifier = '*L2-CMIPF-M*C02_G16*.nc'
    composite = '_FCS'
    script = python_env + 'python process_g1X_false_color_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 IR Clouds - Band 13 with Blue Marble - FULL DISK
#######################################################################################################
if g16_ircl13_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G16*.nc'
    composite = '_IRC'
    script = python_env + 'python process_g1X_ir_clouds_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 IR Clouds - Band 13 with Blue Marble - USER SECTOR
#######################################################################################################
if g16_ircl13_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G16*.nc'
    composite = '_IRS'
    script = python_env + 'python process_g1X_ir_clouds_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 IR Clouds Enhanced - Band 13 [enhanced] with Blue Marble - FULL DISK
#######################################################################################################
if g16_irce13_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G16*.nc'
    composite = '_IRE'
    script = python_env + 'python process_g1X_ir_clouds_enhance_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 IR Clouds Enhanced - Band 13 [enhanced] with Blue Marble - USER SECTOR
#######################################################################################################
if g16_irce13_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G16*.nc'
    composite = '_IES'
    script = python_env + 'python process_g1X_ir_clouds_enhance_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 Split Window Difference - FULL DISK 
#######################################################################################################
if g16_swdiff_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G16*.nc'
    composite = '_SWD'
    script = python_env + 'python process_g1X_swd_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 Split Window Difference - USER SECTOR
#######################################################################################################
if g16_swdiff_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G16*.nc'
    composite = '_SWS'
    script = python_env + 'python process_g1X_swd_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 GLM - Geostationary Lightning Mapper (5 min density) - FULL DISK
#######################################################################################################
if g16_glmirc_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-GLM-Products//'
    identifier = '*GLM*.nc'
    composite = ''
    script = python_env + 'python process_g16_glm_clouds_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 GLM - Geostationary Lightning Mapper (5 min density) - USER SECTOR
#######################################################################################################
if g16_glmirc_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-GLM-Products//'
    identifier = '*GLM*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_glm_clouds_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)


#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GOES-16 Airmass RGB - FULL DISK
#######################################################################################################
if g16_armrgb_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_ARMS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 Airmass RGB - USER SECTOR
#######################################################################################################
if g16_armrgb_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_ARMS07_*.tif'
    composite = '_SEC'
    script = python_env + 'python process_g16_rgb_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 Cloud Phase RGB - FULL DISK
#######################################################################################################
if g16_clprgb_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_CLPS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 Cloud Phase RGB - USER SECTOR
#######################################################################################################
if g16_clprgb_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_CLPS07_*.tif'
    composite = '_SEC'
    script = python_env + 'python process_g16_rgb_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 Convection RGB - FULL DISK
#######################################################################################################
if g16_conrgb_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_CONS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 Convection RGB - USER SECTOR
#######################################################################################################
if g16_conrgb_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_CONS07_*.tif'
    composite = '_SEC'
    script = python_env + 'python process_g16_rgb_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 Day Cloud Phase RGB - FULL DISK
#######################################################################################################
if g16_dcprgb_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_DCPS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 Day Cloud Phase RGB - USER SECTOR
#######################################################################################################
if g16_dcprgb_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_DCPS07_*.tif'
    composite = '_SEC'
    script = python_env + 'python process_g16_rgb_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 Day Land Cloud RGB - FULL DISK
#######################################################################################################
if g16_dlcrgb_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_DLCS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 Day Land Cloud RGB - USER SECTOR
#######################################################################################################
if g16_dlcrgb_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_DLCS07_*.tif'
    composite = '_SEC'
    script = python_env + 'python process_g16_rgb_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 Day Microphysics RGB - FULL DISK
#######################################################################################################
if g16_dmprgb_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_DMPS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 Day Microphysics RGB - USER SECTOR
#######################################################################################################
if g16_dmprgb_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_DMPS07_*.tif'
    composite = '_SEC'
    script = python_env + 'python process_g16_rgb_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 Dust RGB - FULL DISK
#######################################################################################################
if g16_dstrgb_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_DSTS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 Dust RGB - USER SECTOR
#######################################################################################################
if g16_dstrgb_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_DSTS07_*.tif'
    composite = '_SEC'
    script = python_env + 'python process_g16_rgb_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 Night Microphysics RGB - FULL DISK
#######################################################################################################
if g16_nmprgb_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_NMPS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 Night Microphysics RGB - USER SECTOR
#######################################################################################################
if g16_nmprgb_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_NMPS07_*.tif'
    composite = '_SEC'
    script = python_env + 'python process_g16_rgb_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 Natural True Color RGB - FULL DISK
#######################################################################################################
if g16_ntcrgb_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_NTCS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 Natural True Color RGB - USER SECTOR
#######################################################################################################
if g16_ntcrgb_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_NTCS07_*.tif'
    composite = '_SEC'
    script = python_env + 'python process_g16_rgb_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 True Color RGB - FULL DISK
#######################################################################################################
if g16_trurgb_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km / NOTE: This is processing demanding! Use 2 km if using a powerful workstation 
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_NTCS07_*.tif'
    composite = '_TRU'
    script = python_env + 'python process_g16_rgb_true_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 True Color RGB - USER SECTOR
#######################################################################################################
if g16_trurgb_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km 
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_NTCS07_*.tif'
    composite = '_TRS'
    script = python_env + 'python process_g16_rgb_true_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GOES-16 L2 ACHAF - Cloud Top Height - FULL DISK
#######################################################################################################
if g16_cldhgt_fdk:
    max_files = 1
    resolution = 10 # Max Res.: 10 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//ACHAF//'
    identifier = '*ACHAF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 ACHAF - Cloud Top Height - USER SECTOR
#######################################################################################################
if g16_cldhgt_sec:
    max_files = 1
    extent = [-105.0, -60.0, -15.0, 20.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 10 # Max Res.: 10 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//ACHAF//'
    identifier = '*ACHAF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_baseline_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 ACHTF - Cloud Top Temperature - FULL DISK
#######################################################################################################
if g16_cldtmp_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//ACHTF//'
    identifier = '*ACHTF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 ACHTF - Cloud Top Temperature - USER SECTOR
#######################################################################################################
if g16_cldtmp_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//ACHTF//'
    identifier = '*ACHTF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_baseline_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 ACMF - Clear Sky Masks - FULL DISK
#######################################################################################################
if g16_cldmsk_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//ACMF//'
    identifier = '*ACMF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 ACMF - Clear Sky Masks - USER SECTOR
#######################################################################################################
if g16_cldmsk_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//ACMF//'
    identifier = '*ACMF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_baseline_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 ACTPF - Cloud Top Phase - FULL DISK
#######################################################################################################
if g16_cldpha_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//ACTPF//'
    identifier = '*ACTPF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 ACTPF - Cloud Top Phase - USER SECTOR
#######################################################################################################
if g16_cldpha_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//ACTPF//'
    identifier = '*ACTPF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_baseline_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 ADPF - Aerosol Detection - FULL DISK
#######################################################################################################
if g16_aerdet_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//ADPF//'
    identifier = '*ADPF*.nc'
    composite = ''
    script = python_env + 'python process_g16_adpf_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 ADPF - Aerosol Detection - USER SECTOR
#######################################################################################################
if g16_aerdet_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//ADPF//'
    identifier = '*ADPF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_adpf_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 AODF - Aerosol Optical Depth - FULL DISK
#######################################################################################################
if g16_aeropt_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//AODF//'
    identifier = '*AODF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 AODF - Aerosol Optical Depth - USER SECTOR
#######################################################################################################
if g16_aeropt_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//AODF//'
    identifier = '*AODF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_baseline_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 CODF - Cloud Optical Depth - FULL DISK
#######################################################################################################
if g16_cldopt_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 4 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//CODF//'
    identifier = '*CODF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 CODF - Cloud Optical Depth - USER SECTOR
#######################################################################################################
if g16_cldopt_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 4 # Max Res.: 4 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//CODF//'
    identifier = '*CODF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_baseline_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 CPSF - Cloud Particle Size - FULL DISK
#######################################################################################################
if g16_cldpas_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//CPSF//'
    identifier = '*CPSF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 CPSF - Cloud Particle Size - USER SECTOR
#######################################################################################################
if g16_cldpas_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//CPSF//'
    identifier = '*CPSF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_baseline_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 CTPF - Cloud Top Pressure - FULL DISK
#######################################################################################################
if g16_cldpre_fdk:
    max_files = 1
    resolution = 10 # Max Res.: 10 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//CTPF//'
    identifier = '*CTPF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 CTPF - Cloud Top Pressure - USER SECTOR
#######################################################################################################
if g16_cldpre_sec:
    max_files = 1
    extent = [-105.0, -60.0, -15.0, 20.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 10 # Max Res.: 10 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//CTPF//'
    identifier = '*CTPF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_baseline_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 DMWF-C14 - Derived Motion Winds Band 14 - FULL DISK
#######################################################################################################
if g16_dmwf14_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//DMWF-C14//'
    identifier = '*DMWF*.nc'
    composite = '_CLD'
    script = python_env + 'python process_g16_dmw_clouds_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 DMWF-C14 - Derived Motion Winds Band 14 - USER SECTOR
#######################################################################################################
if g16_dmwf14_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//DMWF-C14//'
    identifier = '*DMWF*.nc'
    composite = '_CLS'
    script = python_env + 'python process_g16_dmw_clouds_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 DSIF - Derived Stability Index - FULL DISK
#######################################################################################################
if g16_dsifpr_fdk:
    max_files = 1
    resolution = 10 # Max Res.: 10 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//DSIF//'
    identifier = '*DSIF*.nc'
    composite = ''
    script = python_env + 'python process_g16_dsif_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 DSIF - Derived Stability Index - USER SECTOR
#######################################################################################################
if g16_dsifpr_sec:
    max_files = 1
    extent = [-105.0, -60.0, -15.0, 20.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 10 # Max Res.: 10 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//DSIF//'
    identifier = '*DSIF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_dsif_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 DSRF - Downward Shortwave Radiation - FULL DISK
#######################################################################################################
if g16_dsradi_fdk:
    max_files = 1
    resolution = 2 # Max Res.: 25 km (but you may select higher res plots)
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//DSRF//'
    identifier = '*DSRF*.nc'
    composite = ''
    script = python_env + 'python process_g16_rad_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 DSRF - Downward Shortwave Radiation - USER SECTOR
#######################################################################################################
if g16_dsradi_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 25 km (but you may select higher res plots)
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//DSRF//'
    identifier = '*DSRF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_rad_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 FDCF - Fire-Hot Spot Characterization - FULL DISK
#######################################################################################################
if g16_firmsk_fdk:
    max_files = 1
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//FDCF//'
    identifier = '*FDCF*.nc'
    composite = ''
    script = python_env + 'python process_g16_fdfc_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 FDCF - Fire-Hot Spot Characterization - USER SECTOR
#######################################################################################################
if g16_firmsk_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//FDCF//'
    identifier = '*FDCF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_fdfc_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 FSCF - Snow Cover - FULL DISK
#######################################################################################################
if g16_snowco_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//FSCF//'
    identifier = '*FSCF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 FSCF - Snow Cover - USER SECTOR
#######################################################################################################
if g16_snowco_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km 
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//FSCF//'
    identifier = '*FSCF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_baseline_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 LSTF - Land Surface (Skin) Temperature - FULL DISK
#######################################################################################################
if g16_lstskn_fdk:
    max_files = 1 
    resolution = 10 # Max Res.: 10 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//LSTF//'
    identifier = '*LSTF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 LSTF - Land Surface (Skin) Temperature - USER SECTOR
#######################################################################################################
if g16_lstskn_sec:
    max_files = 1 
    extent = [-105.0, -60.0, -15.0, 20.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 10 # Max Res.: 10 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//LSTF//'
    identifier = '*LSTF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_baseline_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 RRQPEF - Rainfall Rate - Quanti Pred. Estimate - FULL DISK
#######################################################################################################
if g16_rrqpef_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//RRQPEF//'
    identifier = '*RRQPEF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 RRQPEF - Rainfall Rate - Quanti Pred. Estimate - USER SECTOR
#######################################################################################################
if g16_rrqpef_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//RRQPEF//'
    identifier = '*RRQPEF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_baseline_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 RSRF - Reflected Shortwave Radiation - FULL DISK
#######################################################################################################
if g16_rsradi_fdk:
    max_files = 1
    resolution = 2 # Max Res.: 25 km (but you may select higher res plots)
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//RSRF//'
    identifier = '*RSRF*.nc'
    composite = ''
    script = python_env + 'python process_g16_rad_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 RSRF - Reflected Shortwave Radiation - USER SECTOR
#######################################################################################################
if g16_rsradi_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 25 km (but you may select higher res plots)
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//RSRF//'
    identifier = '*RSRF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_rad_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 SSTF - Sea Surface (Skin) Temperature - FULL DISK
#######################################################################################################
if g16_sstskn_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//SSTF//'
    identifier = '*SSTF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 SSTF - Sea Surface (Skin) Temperature - USER SECTOR
#######################################################################################################
if g16_sstskn_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//SSTF//'
    identifier = '*SSTF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_baseline_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 TPWF - Total Precipitable Water - FULL DISK
#######################################################################################################
if g16_totpwa_fdk:
    max_files = 1 
    resolution = 10 # Max Res.: 10 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//TPWF//'
    identifier = '*TPWF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 TPWF - Total Precipitable Water - USER SECTOR
#######################################################################################################
if g16_totpwa_sec:
    max_files = 1 
    extent = [-105.0, -60.0, -15.0, 20.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 10 # Max Res.: 10 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//TPWF//'
    identifier = '*TPWF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_baseline_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-16 L2 VAAF - Volcanic Ash - FULL DISK
#######################################################################################################
if g16_vaafpr_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//VAAF//'
    identifier = '*VAAF*.nc'
    composite = ''
    script = python_env + 'python process_g16_vaaf_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-16 L2 VAAF - Volcanic Ash - USER SECTOR
#######################################################################################################
if g16_vaafpr_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//VAAF//'
    identifier = '*VAAF*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g16_vaaf_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GOES-17 L2 CMI - Band 02 - FULL DISK
#######################################################################################################
if g17_band02_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 1 km
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band02//'
    identifier = '*L2-CMIPF-M*C02_G17*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

#######################################################################################################
# GOES-17 L2 CMI - Band 02 - USER SECTOR
#######################################################################################################
if g17_band02_sec:
    max_files = 1
    extent = [-120.0, 0.0, -75.0, 45.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band02//'
    identifier = '*L2-CMIPF-M*C02_G17*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g1X_bands_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	    

#######################################################################################################
# GOES-17 L2 CMI - Band 07 - FULL DISK
#######################################################################################################
if g17_band07_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km    
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band07//'
    identifier = '*L2-CMIPF-M*C07_G17*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

#######################################################################################################
# GOES-17 L2 CMI - Band 07 - USER SECTOR
#######################################################################################################
if g17_band07_sec:
    max_files = 1
    extent = [-120.0, 0.0, -75.0, 45.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band07//'
    identifier = '*L2-CMIPF-M*C07_G17*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g1X_bands_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	
    
#######################################################################################################
# GOES-17 L2 CMI - Band 08 - FULL DISK
#######################################################################################################
if g17_band08_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km    
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band08//'
    identifier = '*L2-CMIPF-M*C08_G17*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

#######################################################################################################
# GOES-17 L2 CMI - Band 08 - USER SECTOR
#######################################################################################################
if g17_band08_sec:
    max_files = 1
    extent = [-120.0, 0.0, -75.0, 45.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band08//'
    identifier = '*L2-CMIPF-M*C08_G17*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g1X_bands_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-17 L2 CMI - Band 09 - FULL DISK
#######################################################################################################
if g17_band09_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km    
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band09//'
    identifier = '*L2-CMIPF-M*C09_G17*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

#######################################################################################################
# GOES-17 L2 CMI - Band 09 - USER SECTOR
#######################################################################################################
if g17_band09_sec:
    max_files = 1
    extent = [-120.0, 0.0, -75.0, 45.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band09//'
    identifier = '*L2-CMIPF-M*C09_G17*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g1X_bands_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-17 L2 CMI - Band 13 - FULL DISK
#######################################################################################################
if g17_band13_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km    
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G17*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

#######################################################################################################
# GOES-17 L2 CMI - Band 13 - USER SECTOR
#######################################################################################################
if g17_band13_sec:
    max_files = 1
    extent = [-120.0, 0.0, -75.0, 45.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G17*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g1X_bands_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-17 L2 CMI - Band 14 - FULL DISK
#######################################################################################################
if g17_band14_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km    
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band14//'
    identifier = '*L2-CMIPF-M*C14_G17*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

#######################################################################################################
# GOES-17 L2 CMI - Band 14 - USER SECTOR
#######################################################################################################
if g17_band14_sec:
    max_files = 1
    extent = [-120.0, 0.0, -75.0, 45.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band14//'
    identifier = '*L2-CMIPF-M*C14_G17*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g1X_bands_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-17 L2 CMI - Band 15 - FULL DISK
#######################################################################################################
if g17_band15_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km    
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band15//'
    identifier = '*L2-CMIPF-M*C15_G17*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	    

#######################################################################################################
# GOES-17 L2 CMI - Band 15 - USER SECTOR
#######################################################################################################
if g17_band15_sec:
    max_files = 1
    extent = [-120.0, 0.0, -75.0, 45.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band15//'
    identifier = '*L2-CMIPF-M*C15_G17*.nc'
    composite = '_SEC'
    script = python_env + 'python process_g1X_bands_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GOES-17 False Color - Band 02 and Band 13 - FULL DISK
#######################################################################################################
if g17_fcolor_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band02//'
    identifier = '*L2-CMIPF-M*C02_G17*.nc'
    composite = '_FCO'
    script = python_env + 'python process_g1X_false_color_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-17 False Color - Band 02 and Band 13 - USER SECTOR
#######################################################################################################
if g17_fcolor_sec:
    max_files = 1
    extent = [-120.0, 0.0, -75.0, 45.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 1 km
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band02//'
    identifier = '*L2-CMIPF-M*C02_G17*.nc'
    composite = '_FCS'
    script = python_env + 'python process_g1X_false_color_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-17 IR Clouds - Band 13 with Blue Marble - FULL DISK
#######################################################################################################
if g17_ircl13_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G17*.nc'
    composite = '_IRC'
    script = python_env + 'python process_g1X_ir_clouds_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-17 IR Clouds - Band 13 with Blue Marble - USER SECTOR
#######################################################################################################
if g17_ircl13_sec:
    max_files = 1
    extent = [-120.0, 0.0, -75.0, 45.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G17*.nc'
    composite = '_IRS'
    script = python_env + 'python process_g1X_ir_clouds_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-17 IR Clouds Enhanced - Band 13 [enhanced] with Blue Marble - FULL DISK
#######################################################################################################
if g17_irce13_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G17*.nc'
    composite = '_IRE'
    script = python_env + 'python process_g1X_ir_clouds_enhance_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-17 IR Clouds Enhanced - Band 13 [enhanced] with Blue Marble - USER SECTOR
#######################################################################################################
if g17_irce13_sec:
    max_files = 1
    extent = [-120.0, 0.0, -75.0, 45.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G17*.nc'
    composite = '_IES'
    script = python_env + 'python process_g1X_ir_clouds_enhance_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#######################################################################################################
# GOES-17 Split Window Difference - FULL DISK
#######################################################################################################
if g17_swdiff_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G17*.nc'
    composite = '_SWD'
    script = python_env + 'python process_g1X_swd_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# GOES-17 Split Window Difference - USER SECTOR
#######################################################################################################
if g17_swdiff_sec:
    max_files = 1
    extent = [-120.0, 0.0, -75.0, 45.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G17*.nc'
    composite = '_SWS'
    script = python_env + 'python process_g1X_swd_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# METEOSAT - 0 Degree (IMAGERY AND RGB'S) - FULL DISK
#######################################################################################################
if msg_produc_fdk:
    max_files = 1
    resolution = 8 # Max Res.: 3 km
    prod_dir = gnc_dir + 'MSG-0degree//IMG-3h//'
    identifier = '*-EPI______-*'
    composite = ''
    script = python_env + 'python process_msg_bands_rgb_fdk.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#######################################################################################################
# METEOSAT - 0 Degree (IMAGERY AND RGB'S) - USER SECTOR
#######################################################################################################
if msg_produc_sec:
    max_files = 1
    extent = [-63.0, -35.0, -35.0, -10.0] # [min_lon, min_lat, max_lon, max_lat]
    resolution = 3 # Max Res.: 3 km
    prod_dir = gnc_dir + 'MSG-0degree//IMG-3h//'
    identifier = '*-EPI______-*'
    composite = '_SEC'
    script = python_env + 'python process_msg_bands_rgb_sec.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
 
print("##############  SHOWCAST MONITOR ENDED  ##############")
print('Ended at:', datetime.datetime.now())
print('Number of products processed:', prod_count)
print('Total processing time:', t.time() - start, 'seconds')
print("\n")
