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
g16_band02 = True # GOES-16 L2 CMI - FULL DISK - Band 02
g16_band07 = True # GOES-16 L2 CMI - FULL DISK - Band 07
g16_band08 = True # GOES-16 L2 CMI - FULL DISK - Band 08
g16_band09 = True # GOES-16 L2 CMI - FULL DISK - Band 09
g16_band13 = True # GOES-16 L2 CMI - FULL DISK - Band 13
g16_band14 = True # GOES-16 L2 CMI - FULL DISK - Band 14
g16_band15 = True # GOES-16 L2 CMI - FULL DISK - Band 15

# GOES-16 - BANDS COMPOSITES / MULTISPECTRAL IMAGERY / GLM
g16_fcolor = True # GOES-16 False Color (Band 02 and Band13)
g16_ircl13 = True # GOES-16 IR Clouds (Band 13 with Blue Marble)
g16_irce13 = True # GOES-16 IR Clouds Enhanced (Band 13 [enhanced] with Blue Marble)
g16_swdiff = True # GOES-16 Split Window Difference
g16_glmirc = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (5 min density)

# GOES-16 RGB COMPOSITES
g16_armrgb = True # GOES-16 Airmass RGB
g16_clprgb = True # GOES-16 Cloud Phase RGB
g16_conrgb = True # GOES-16 Convection RGB
g16_dcprgb = True # GOES-16 Day Cloud Phase RGB
g16_dlcrgb = True # GOES-16 Day Land Cloud RGB
g16_dmprgb = True # GOES-16 Day Microphysics RGB
g16_dstrgb = True # GOES-16 Dust RGB
g16_nmprgb = True # GOES-16 Night Microphysics RGB
g16_ntcrgb = True # GOES-16 Natural True Color RGB

# GOES-16 BASELINE PRODUCTS
g16_cldhgt = True # GOES-16 L2 ACHAF - Cloud Top Height
g16_cldtmp = True # GOES-16 L2 ACHTF - Cloud Top Temperature
g16_cldmsk = True # GOES-16 L2 ACMF - Clear Sky Masks
g16_cldpha = True # GOES-16 L2 ACTPF - Cloud Top Phase
g16_aerdet = True # GOES-16 L2 ADPF - Aerosol Detection
g16_aeropt = True # GOES-16 L2 AODF - Aerosol Optical Depth
g16_cldopt = True # GOES-16 L2 CODF - Cloud Optical Depth
g16_cldpas = True # GOES-16 L2 CPSF - Cloud Particle Size
g16_cldpre = True # GOES-16 L2 CTPF - Cloud Top Pressure
g16_dmwf14 = True # GOES-16 L2 DMWF-C14 - Derived Motion Winds Band 14
g16_dsifpr = True # GOES-16 L2 DSIF - Derived Stability Index
g16_dsradi = True # GOES-16 L2 DSRF - Downward Shortwave Radiation
g16_firmsk = True # GOES-16 L2 FDCF - Fire-Hot Spot Characterization
g16_snowco = True # GOES-16 L2 FSCF - Snow Cover
g16_lstskn = True # GOES-16 L2 LSTF - Land Surface (Skin) Temperature
g16_rrqpef = True # GOES-16 L2 RRQPEF - Rainfall Rate - Quanti Pred. Estim
g16_rsradi = True # GOES-16 L2 RSRF - Reflected Shortwave Radiation
g16_sstskn = True # GOES-16 L2 SSTF - Sea Surface (Skin) Temperature
g16_totpwa = True # GOES-16 L2 TPWF - Total Precipitable Water
g16_vaafpr = True # GOES-16 L2 VAAF - Volcanic Ash

# GOES-17 - ABI INDIVIDUAL BANDS
g17_band02 = True # GOES-17 L2 CMI - FULL DISK - Band 02
g17_band07 = True # GOES-17 L2 CMI - FULL DISK - Band 07
g17_band08 = True # GOES-17 L2 CMI - FULL DISK - Band 08
g17_band09 = True # GOES-17 L2 CMI - FULL DISK - Band 09
g17_band13 = True # GOES-17 L2 CMI - FULL DISK - Band 13
g17_band14 = True # GOES-17 L2 CMI - FULL DISK - Band 14
g17_band15 = True # GOES-17 L2 CMI - FULL DISK - Band 15

# GOES-17 - BANDS COMPOSITES / MULTISPECTRAL IMAGERY
g17_fcolor = True # GOES-17 False Color (Band 02 and Band13)
g17_ircl13 = True # GOES-17 IR Clouds (Band 13 with Blue Marble)
g17_irce13 = True # GOES-17 IR Clouds Enhanced (Band 13 [enhanced] with Blue Marble)
g17_swdiff = True # GOES-17 Split Window Difference
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
############################################################
# FILE PROCESSING AND LOG FUNCTION
############################################################
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
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
############################################################
# GOES-16 L2 CMI - FULL DISK - Band 02
############################################################
if g16_band02:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band02//'
    identifier = '*L2-CMIPF-M*C02_G16*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

############################################################
# GOES-16 L2 CMI - FULL DISK - Band 07
############################################################
if g16_band07:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km    
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band07//'
    identifier = '*L2-CMIPF-M*C07_G16*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	
    
############################################################
# GOES-16 L2 CMI - FULL DISK - Band 08
############################################################
if g16_band08:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band08//'
    identifier = '*L2-CMIPF-M*C08_G16*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

############################################################
# GOES-16 L2 CMI - FULL DISK - Band 09
############################################################
if g16_band09:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band09//'
    identifier = '*L2-CMIPF-M*C09_G16*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

############################################################
# GOES-16 L2 CMI - FULL DISK - Band 13
############################################################
if g16_band13:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G16*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

############################################################
# GOES-16 L2 CMI - FULL DISK - Band 14
############################################################
if g16_band14:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km   
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band14//'
    identifier = '*L2-CMIPF-M*C14_G16*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

############################################################
# GOES-16 L2 CMI - FULL DISK - Band 15
############################################################
if g16_band15:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band15//'
    identifier = '*L2-CMIPF-M*C15_G16*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	    

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

############################################################
# GOES-16 False Color (Band 02 and Band13)
############################################################
if g16_fcolor:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band02//'
    identifier = '*L2-CMIPF-M*C02_G16*.nc'
    composite = '_FCO'
    script = python_env + 'python process_g1X_false_color.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
############################################################
# GOES-16 IR Clouds (Band 13 with Blue Marble)
############################################################
if g16_ircl13:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G16*.nc'
    composite = '_IRC'
    script = python_env + 'python process_g1X_ir_clouds.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 IR Clouds Enhanced (Band 13 [enhanced] with Blue Marble)
############################################################
if g16_irce13:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G16*.nc'
    composite = '_IRE'
    script = python_env + 'python process_g1X_ir_clouds_enhance.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 Split Window Difference
############################################################
if g16_swdiff:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G16*.nc'
    composite = '_SWD'
    script = python_env + 'python process_g1X_swd.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 GLM - Geostationary Lightning Mapper (5 min density)
############################################################
if g16_glmirc:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-GLM-Products//'
    identifier = '*GLM*.nc'
    composite = ''
    script = python_env + 'python process_g16_glm_clouds.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    
############################################################
# GOES-16 Airmass RGB
############################################################
if g16_armrgb:
    max_files = 1
    extent = [-105.0, -60.0, -15.0, 20.0] 
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_ARMS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_proj.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
############################################################
# GOES-16 Cloud Phase RGB
############################################################
if g16_clprgb:
    max_files = 1
    extent = [-105.0, -60.0, -15.0, 20.0]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_CLPS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_proj.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
############################################################
# GOES-16 Convection RGB
############################################################
if g16_conrgb:
    max_files = 1
    extent = [-105.0, -60.0, -15.0, 20.0]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_CONS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_proj.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
############################################################
# GOES-16 Day Cloud Phase RGB
############################################################
if g16_dcprgb:
    max_files = 1
    extent = [-105.0, -60.0, -15.0, 20.0]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_DCPS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_proj.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
############################################################
# GOES-16 Day Land Cloud RGB
############################################################
if g16_dlcrgb:
    max_files = 1
    extent = [-105.0, -60.0, -15.0, 20.0]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_DLCS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_proj.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
############################################################
# GOES-16 Day Microphysics RGB
############################################################
if g16_dmprgb:
    max_files = 1
    extent = [-105.0, -60.0, -15.0, 20.0]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_DMPS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_proj.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
############################################################
# GOES-16 Dust RGB
############################################################
if g16_dstrgb:
    max_files = 1
    extent = [-105.0, -60.0, -15.0, 20.0]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_DSTS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_proj.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
############################################################
# GOES-16 Night Microphysics RGB
############################################################
if g16_nmprgb:
    max_files = 1
    extent = [-105.0, -60.0, -15.0, 20.0]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_NMPS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_proj.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
############################################################
# GOES-16 Natural True Color RGB
############################################################
if g16_ntcrgb:
    max_files = 1
    extent = [-105.0, -60.0, -15.0, 20.0]
    resolution = 2 # Max Res.: 2 km  
    prod_dir = gnc_dir + 'GOES-R-RGB-Composites//'
    identifier = 'G16_NTCS07_*.tif'
    composite = ''
    script = python_env + 'python process_g16_rgb_proj.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

############################################################
# GOES-16 L2 ACHAF - Cloud Top Height
############################################################
if g16_cldhgt:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 10 # Max Res.: 10 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//ACHAF//'
    identifier = '*ACHAF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 ACHTF - Cloud Top Temperature
############################################################
if g16_cldtmp:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//ACHTF//'
    identifier = '*ACHTF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 ACMF - Clear Sky Masks
############################################################
if g16_cldmsk:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//ACMF//'
    identifier = '*ACMF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 ACTPF - Cloud Top Phase
############################################################
if g16_cldpha:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//ACTPF//'
    identifier = '*ACTPF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 ADPF - Aerosol Detection
############################################################
if g16_aerdet:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//ADPF//'
    identifier = '*ADPF*.nc'
    composite = ''
    script = python_env + 'python process_g16_adpf.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
############################################################
# GOES-16 L2 AODF - Aerosol Optical Depth
############################################################
if g16_aeropt:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//AODF//'
    identifier = '*AODF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 CODF - Cloud Optical Depth
############################################################
if g16_cldopt:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 4 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//CODF//'
    identifier = '*CODF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 CPSF - Cloud Particle Size
############################################################
if g16_cldpas:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//CPSF//'
    identifier = '*CPSF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 CTPF - Cloud Top Pressure
############################################################
if g16_cldpre:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 10 # Max Res.: 10 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//CTPF//'
    identifier = '*CTPF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 DMWF-C14 - Derived Motion Winds Band 14
############################################################
if g16_dmwf14:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 2 # Max Res.: 10 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//DMWF-C14//'
    identifier = '*DMWF*.nc'
    composite = '_CLD'
    script = python_env + 'python process_g16_dmw_clouds.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
############################################################
# GOES-16 L2 DSIF - Derived Stability Index
############################################################
if g16_dsifpr:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 10 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//DSIF//'
    identifier = '*DSIF*.nc'
    composite = ''
    script = python_env + 'python process_g16_dsif.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 DSRF - Downward Shortwave Radiation
############################################################
if g16_dsradi:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 25 # Max Res.: 25 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//DSRF//'
    identifier = '*DSRF*.nc'
    composite = ''
    script = python_env + 'python process_g16_rad.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
############################################################
# GOES-16 L2 FDCF - Fire-Hot Spot Characterization
############################################################
if g16_firmsk:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 2 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//FDCF//'
    identifier = '*FDCF*.nc'
    composite = ''
    script = python_env + 'python process_g16_fdfc.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 FSCF - Snow Cover
############################################################
if g16_snowco:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//FSCF//'
    identifier = '*FSCF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
############################################################
# GOES-16 L2 LSTF - Land Surface (Skin) Temperature
############################################################
if g16_lstskn:
    max_files = 1 
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 10 # Max Res.: 10 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//LSTF//'
    identifier = '*LSTF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 RRQPEF - Rainfall Rate - Quanti Pred. Estimate
############################################################
if g16_rrqpef:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//RRQPEF//'
    identifier = '*RRQPEF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 RSRF - Reflected Shortwave Radiation
############################################################
if g16_rsradi:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 25 # Max Res.: 25 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//RSRF//'
    identifier = '*RSRF*.nc'
    composite = ''
    script = python_env + 'python process_g16_rad.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 SSTF - Sea Surface (Skin) Temperature
############################################################
if g16_sstskn:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//SSTF//'
    identifier = '*SSTF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 TPWF - Total Precipitable Water
############################################################
if g16_totpwa:
    max_files = 1 
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 10 # Max Res.: 10 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//TPWF//'
    identifier = '*TPWF*.nc'
    composite = ''
    script = python_env + 'python process_g16_baseline.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-16 L2 VAAF - Volcanic Ash
############################################################
if g16_vaafpr:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-R-Level-2-Products//VAAF//'
    identifier = '*VAAF*.nc'
    composite = ''
    script = python_env + 'python process_g16_vaaf.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

############################################################
# GOES-17 L2 CMI - FULL DISK - Band 02
############################################################
if g17_band02:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 1 km
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band02//'
    identifier = '*L2-CMIPF-M*C02_G17*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

############################################################
# GOES-17 L2 CMI - FULL DISK - Band 07
############################################################
if g17_band07:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km    
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band07//'
    identifier = '*L2-CMIPF-M*C07_G17*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	
    
############################################################
# GOES-17 L2 CMI - FULL DISK - Band 08
############################################################
if g17_band08:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km    
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band08//'
    identifier = '*L2-CMIPF-M*C08_G17*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

############################################################
# GOES-17 L2 CMI - FULL DISK - Band 09
############################################################
if g17_band09:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km    
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band09//'
    identifier = '*L2-CMIPF-M*C09_G17*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

############################################################
# GOES-17 L2 CMI - FULL DISK - Band 13
############################################################
if g17_band13:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km    
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G17*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

############################################################
# GOES-17 L2 CMI - FULL DISK - Band 14
############################################################
if g17_band14:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km    
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band14//'
    identifier = '*L2-CMIPF-M*C14_G17*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	

############################################################
# GOES-17 L2 CMI - FULL DISK - Band 15
############################################################
if g17_band15:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km    
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band15//'
    identifier = '*L2-CMIPF-M*C15_G17*.nc'
    composite = ''
    script = python_env + 'python process_g1X_bands.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)	    

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

############################################################
# GOES-17 False Color (Band 02 and Band13)
############################################################
if g17_fcolor:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band02//'
    identifier = '*L2-CMIPF-M*C02_G17*.nc'
    composite = '_FCO'
    script = python_env + 'python process_g1X_false_color.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
############################################################
# GOES-17 IR Clouds (Band 13 with Blue Marble)
############################################################
if g17_ircl13:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G17*.nc'
    composite = '_IRC'
    script = python_env + 'python process_g1X_ir_clouds.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-17 IR Clouds Enhanced (Band 13 [enhanced] with Blue Marble)
############################################################
if g17_irce13:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G17*.nc'
    composite = '_IRE'
    script = python_env + 'python process_g1X_ir_clouds_enhance.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)

############################################################
# GOES-17 Split Window Difference
############################################################
if g17_swdiff:
    max_files = 1
    extent = [0.0, 0.0, 0.0, 0.0] # Region selection not available for this product yet
    resolution = 8 # Max Res.: 2 km
    prod_dir = gnc_dir + 'GOES-S-CMI-Imagery//Band13//'
    identifier = '*L2-CMIPF-M*C13_G17*.nc'
    composite = '_SWD'
    script = python_env + 'python process_g1X_swd.py'
    procProduct(prod_dir, identifier, composite, script, extent[0], extent[1], extent[2], extent[3], resolution)
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

print("##############  SHOWCAST MONITOR ENDED  ##############")
print('Ended at:', datetime.datetime.now())
print('Number of products processed:', prod_count)
print('Total processing time:', t.time() - start, 'seconds')
print("\n")
