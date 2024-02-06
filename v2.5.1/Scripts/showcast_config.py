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
__version__ = "2.5.0"
__maintainer__ = "Diego Souza"
__email__ = "diego.souza@inpe.br"
__status__ = "Production"

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Required Libraries 
import glob                           # Unix style pathname pattern expansion
import os                             # Miscellaneous operating system interfaces
import sys                            # Import the "system specific parameters and functions" module
from os.path import dirname, abspath  # Return a normalized absolutized version of the pathname path 
import datetime                       # Basic Date and Time types
import time as t                      # Time access and conversion

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

start = t.time()  # Start the time counter

# Python environment
python_env = sys.argv[1]

# Ingestion directory
ingest_dir = sys.argv[2]

# SHOWCast directory:
showcast_dir = dirname(dirname(abspath(__file__)))

# SHOWCast process number
showcast_process = int(sys.argv[3])

# SHOWCast visualization directory
vis_dir = sys.argv[4]

# Variable that will store the desired products
products = []

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Select the products that will be processed:

#######################################################################################################
# GOES-16 - ABI INDIVIDUAL BANDS (FROM GEONETCAST-AMERICAS AND / OR CLOUD)
#######################################################################################################

#------------------------------------------------------------------------------------------------------
g16_band01_fdk            = True # GOES-16 L2 CMI - Band 01 - FULL DISK 

g16_band01_fdk_process    = 1                                                         # Process cicle for this product 
g16_band01_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band01//'               # Folder where the data is found
g16_band01_fdk_identifier = '*L2-CMIPF-M*C01_G16*.nc'                                 # Unique string on the file name
g16_band01_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band01_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_band01_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band01_fdk_config     = ''                                                        # Configuration string
g16_band01_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_band01_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band01_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band01_sec            = True # GOES-16 L2 CMI - Band 01 - USER SECTOR 

g16_band01_sec_process    = 1                                                         # Process cicle for this product 
g16_band01_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band01//'               # Folder where the data is found
g16_band01_sec_identifier = '*L2-CMIPF-M*C01_G16*.nc'                                 # Unique string on the file name
g16_band01_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band01_sec_extent     = [-54.0, -28.0, -43.0, -18.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band01_sec_resolution = 1  # Max Res.: 1 km                                       # Final plot resolution
g16_band01_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band01_sec_config     = '_SEC'                                                    # Configuration string
g16_band01_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band01_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band01_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band02_fdk            = True # GOES-16 L2 CMI - Band 02 - FULL DISK 

g16_band02_fdk_process    = 1                                                         # Process cicle for this product 
g16_band02_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band02//'               # Folder where the data is found
g16_band02_fdk_identifier = '*L2-CMIPF-M*C02_G16*.nc'                                 # Unique string on the file name
g16_band02_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band02_fdk_resolution = 8  # Max Res.: 1 km                                       # Final plot resolution
g16_band02_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band02_fdk_config     = ''                                                        # Configuration string
g16_band02_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_band02_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band02_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band02_sec            = True # GOES-16 L2 CMI - Band 02 - USER SECTOR 

g16_band02_sec_process    = 1                                                         # Process cicle for this product 
g16_band02_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band02//'               # Folder where the data is found
g16_band02_sec_identifier = '*L2-CMIPF-M*C02_G16*.nc'                                 # Unique string on the file name
g16_band02_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band02_sec_extent     = [-54.0, -28.0, -43.0, -18.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band02_sec_resolution = 1  # Max Res.: 1 km                                       # Final plot resolution
g16_band02_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band02_sec_config     = '_SEC'                                                    # Configuration string
g16_band02_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band02_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band02_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band03_fdk            = True # GOES-16 L2 CMI - Band 03 - FULL DISK 

g16_band03_fdk_process    = 1                                                         # Process cicle for this product 
g16_band03_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band03//'               # Folder where the data is found
g16_band03_fdk_identifier = '*L2-CMIPF-M*C03_G16*.nc'                                 # Unique string on the file name
g16_band03_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band03_fdk_resolution = 8  # Max Res.: 1 km                                       # Final plot resolution
g16_band03_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band03_fdk_config     = ''                                                        # Configuration string
g16_band03_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_band03_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band03_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band03_sec            = True # GOES-16 L2 CMI - Band 03 - USER SECTOR 

g16_band03_sec_process    = 1                                                         # Process cicle for this product 
g16_band03_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band03//'               # Folder where the data is found
g16_band03_sec_identifier = '*L2-CMIPF-M*C03_G16*.nc'                                 # Unique string on the file name
g16_band03_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band03_sec_extent     = [-54.0, -28.0, -43.0, -18.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band03_sec_resolution = 1  # Max Res.: 1 km                                       # Final plot resolution
g16_band03_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band03_sec_config     = '_SEC'                                                    # Configuration string
g16_band03_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band03_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band03_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band04_fdk            = True # GOES-16 L2 CMI - Band 04 - FULL DISK 

g16_band04_fdk_process    = 1                                                         # Process cicle for this product 
g16_band04_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band04//'               # Folder where the data is found
g16_band04_fdk_identifier = '*L2-CMIPF-M*C04_G16*.nc'                                 # Unique string on the file name
g16_band04_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band04_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_band04_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band04_fdk_config     = ''                                                        # Configuration string
g16_band04_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_band04_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band04_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band04_sec            = True # GOES-16 L2 CMI - Band 04 - USER SECTOR 

g16_band04_sec_process    = 1                                                         # Process cicle for this product 
g16_band04_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band04//'               # Folder where the data is found
g16_band04_sec_identifier = '*L2-CMIPF-M*C04_G16*.nc'                                 # Unique string on the file name
g16_band04_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band04_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band04_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_band04_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band04_sec_config     = '_SEC'                                                    # Configuration string
g16_band04_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band04_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band04_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band05_fdk            = True # GOES-16 L2 CMI - Band 05 - FULL DISK 

g16_band05_fdk_process    = 1                                                         # Process cicle for this product 
g16_band05_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band05//'               # Folder where the data is found
g16_band05_fdk_identifier = '*L2-CMIPF-M*C05_G16*.nc'                                 # Unique string on the file name
g16_band05_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band05_fdk_resolution = 8  # Max Res.: 1 km                                       # Final plot resolution
g16_band05_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band05_fdk_config     = ''                                                        # Configuration string
g16_band05_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_band05_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band05_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band05_sec            = True # GOES-16 L2 CMI - Band 05 - USER SECTOR 

g16_band05_sec_process    = 1                                                         # Process cicle for this product 
g16_band05_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band05//'               # Folder where the data is found
g16_band05_sec_identifier = '*L2-CMIPF-M*C05_G16*.nc'                                 # Unique string on the file name
g16_band05_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band05_sec_extent     = [-54.0, -28.0, -43.0, -18.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band05_sec_resolution = 1  # Max Res.: 1 km                                       # Final plot resolution
g16_band05_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band05_sec_config     = '_SEC'                                                    # Configuration string
g16_band05_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band05_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band05_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band06_fdk            = True # GOES-16 L2 CMI - Band 06 - FULL DISK 

g16_band06_fdk_process    = 1                                                         # Process cicle for this product 
g16_band06_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band06//'               # Folder where the data is found
g16_band06_fdk_identifier = '*L2-CMIPF-M*C06_G16*.nc'                                 # Unique string on the file name
g16_band06_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band06_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_band06_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band06_fdk_config     = ''                                                        # Configuration string
g16_band06_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_band06_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band06_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band06_sec            = True # GOES-16 L2 CMI - Band 06 - USER SECTOR 

g16_band06_sec_process    = 1                                                         # Process cicle for this product 
g16_band06_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band06//'               # Folder where the data is found
g16_band06_sec_identifier = '*L2-CMIPF-M*C06_G16*.nc'                                 # Unique string on the file name
g16_band06_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band06_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band06_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_band06_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band06_sec_config     = '_SEC'                                                    # Configuration string
g16_band06_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band06_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band06_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band07_fdk            = True # GOES-16 L2 CMI - Band 07 - FULL DISK 

g16_band07_fdk_process    = 1                                                         # Process cicle for this product 
g16_band07_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band07//'               # Folder where the data is found
g16_band07_fdk_identifier = '*L2-CMIPF-M*C07_G16*.nc'                                 # Unique string on the file name
g16_band07_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band07_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_band07_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band07_fdk_config     = ''                                                        # Configuration string
g16_band07_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_radb01_sec_output     = showcast_dir + '//Output//'                               # Output folder
g16_band07_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band07_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band07_sec            = True # GOES-16 L2 CMI - Band 07 - USER SECTOR 

g16_band07_sec_process    = 1                                                         # Process cicle for this product 
g16_band07_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band07//'               # Folder where the data is found
g16_band07_sec_identifier = '*L2-CMIPF-M*C07_G16*.nc'                                 # Unique string on the file name
g16_band07_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band07_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band07_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_band07_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band07_sec_config     = '_SEC'                                                    # Configuration string
g16_band07_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band07_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band07_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band08_fdk            = True # GOES-16 L2 CMI - Band 08 - FULL DISK 

g16_band08_fdk_process    = 1                                                         # Process cicle for this product 
g16_band08_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band08//'               # Folder where the data is found
g16_band08_fdk_identifier = '*L2-CMIPF-M*C08_G16*.nc'                                 # Unique string on the file name
g16_band08_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band08_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_band08_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band08_fdk_config     = ''                                                        # Configuration string
g16_band08_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_band08_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band08_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band08_sec            = True # GOES-16 L2 CMI - Band 08 - USER SECTOR 

g16_band08_sec_process    = 1                                                         # Process cicle for this product 
g16_band08_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band08//'               # Folder where the data is found
g16_band08_sec_identifier = '*L2-CMIPF-M*C08_G16*.nc'                                 # Unique string on the file name
g16_band08_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band08_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band08_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_band08_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band08_sec_config     = '_SEC'                                                    # Configuration string
g16_band08_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band08_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band08_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band09_fdk            = True # GOES-16 L2 CMI - Band 09 - FULL DISK 

g16_band09_fdk_process    = 1                                                         # Process cicle for this product 
g16_band09_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band09//'               # Folder where the data is found
g16_band09_fdk_identifier = '*L2-CMIPF-M*C09_G16*.nc'                                 # Unique string on the file name
g16_band09_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band09_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_band09_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band09_fdk_config     = ''                                                        # Configuration string
g16_band09_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_band09_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band09_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band09_sec            = True # GOES-16 L2 CMI - Band 09 - USER SECTOR 

g16_band09_sec_process    = 1                                                         # Process cicle for this product 
g16_band09_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band09//'               # Folder where the data is found
g16_band09_sec_identifier = '*L2-CMIPF-M*C09_G16*.nc'                                 # Unique string on the file name
g16_band09_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band09_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band09_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_band09_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band09_sec_config     = '_SEC'                                                    # Configuration string
g16_band09_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band09_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band09_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band10_fdk            = True # GOES-16 L2 CMI - Band 10 - FULL DISK 

g16_band10_fdk_process    = 1                                                         # Process cicle for this product 
g16_band10_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band10//'               # Folder where the data is found
g16_band10_fdk_identifier = '*L2-CMIPF-M*C10_G16*.nc'                                 # Unique string on the file name
g16_band10_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band10_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_band10_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band10_fdk_config     = ''                                                        # Configuration string
g16_band10_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_band10_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band10_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band10_sec            = True # GOES-16 L2 CMI - Band 10 - USER SECTOR 

g16_band10_sec_process    = 1                                                         # Process cicle for this product 
g16_band10_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band10//'               # Folder where the data is found
g16_band10_sec_identifier = '*L2-CMIPF-M*C10_G16*.nc'                                 # Unique string on the file name
g16_band10_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band10_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band10_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_band10_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band10_sec_config     = '_SEC'                                                    # Configuration string
g16_band10_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band10_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band10_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band11_fdk            = True # GOES-16 L2 CMI - Band 11 - FULL DISK 

g16_band11_fdk_process    = 1                                                         # Process cicle for this product 
g16_band11_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band11//'               # Folder where the data is found
g16_band11_fdk_identifier = '*L2-CMIPF-M*C11_G16*.nc'                                 # Unique string on the file name
g16_band11_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band11_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_band11_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band11_fdk_config     = ''                                                        # Configuration string
g16_band11_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_band11_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band11_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band11_sec            = True # GOES-16 L2 CMI - Band 11 - USER SECTOR 

g16_band11_sec_process    = 1                                                         # Process cicle for this product 
g16_band11_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band11//'               # Folder where the data is found
g16_band11_sec_identifier = '*L2-CMIPF-M*C11_G16*.nc'                                 # Unique string on the file name
g16_band11_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band11_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band11_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_band11_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band11_sec_config     = '_SEC'                                                    # Configuration string
g16_band11_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band11_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band11_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band12_fdk            = True # GOES-16 L2 CMI - Band 12 - FULL DISK 

g16_band12_fdk_process    = 1                                                         # Process cicle for this product 
g16_band12_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band12//'               # Folder where the data is found
g16_band12_fdk_identifier = '*L2-CMIPF-M*C12_G16*.nc'                                 # Unique string on the file name
g16_band12_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band12_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_band12_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band12_fdk_config     = ''                                                        # Configuration string
g16_band12_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_band12_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band12_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band12_sec            = True # GOES-16 L2 CMI - Band 12 - USER SECTOR 

g16_band12_sec_process    = 1                                                         # Process cicle for this product 
g16_band12_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band12//'               # Folder where the data is found
g16_band12_sec_identifier = '*L2-CMIPF-M*C12_G16*.nc'                                 # Unique string on the file name
g16_band12_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band12_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band12_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_band12_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band12_sec_config     = '_SEC'                                                    # Configuration string
g16_band12_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band12_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band12_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band13_fdk            = True # GOES-16 L2 CMI - Band 13 - FULL DISK 

g16_band13_fdk_process    = 1                                                         # Process cicle for this product 
g16_band13_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band13//'               # Folder where the data is found
g16_band13_fdk_identifier = '*L2-CMIPF-M*C13_G16*.nc'                                 # Unique string on the file name
g16_band13_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band13_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_band13_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band13_fdk_config     = ''                                                        # Configuration string
g16_band13_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_band13_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band13_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band13_sec            = True # GOES-16 L2 CMI - Band 13 - USER SECTOR 

g16_band13_sec_process    = 1                                                         # Process cicle for this product 
g16_band13_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band13//'               # Folder where the data is found
g16_band13_sec_identifier = '*L2-CMIPF-M*C13_G16*.nc'                                 # Unique string on the file name
g16_band13_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band13_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band13_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_band13_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band13_sec_config     = '_SEC'                                                    # Configuration string
g16_band13_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band13_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band13_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band14_fdk            = True # GOES-16 L2 CMI - Band 14 - FULL DISK 

g16_band14_fdk_process    = 1                                                         # Process cicle for this product 
g16_band14_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band14//'               # Folder where the data is found
g16_band14_fdk_identifier = '*L2-CMIPF-M*C14_G16*.nc'                                 # Unique string on the file name
g16_band14_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band14_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_band14_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band14_fdk_config     = ''                                                        # Configuration string
g16_band14_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_band14_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band14_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band14_sec            = True # GOES-16 L2 CMI - Band 14 - USER SECTOR 

g16_band14_sec_process    = 1                                                         # Process cicle for this product 
g16_band14_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band14//'               # Folder where the data is found
g16_band14_sec_identifier = '*L2-CMIPF-M*C14_G16*.nc'                                 # Unique string on the file name
g16_band14_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band14_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band14_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_band14_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band14_sec_config     = '_SEC'                                                    # Configuration string
g16_band14_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band14_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band14_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band15_fdk            = True # GOES-16 L2 CMI - Band 15 - FULL DISK 

g16_band15_fdk_process    = 1                                                         # Process cicle for this product 
g16_band15_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band15//'               # Folder where the data is found
g16_band15_fdk_identifier = '*L2-CMIPF-M*C15_G16*.nc'                                 # Unique string on the file name
g16_band15_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band15_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_band15_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band15_fdk_config     = ''                                                        # Configuration string
g16_band15_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_band15_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band15_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band15_sec            = True # GOES-16 L2 CMI - Band 15 - USER SECTOR 

g16_band15_sec_process    = 1                                                         # Process cicle for this product 
g16_band15_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band15//'               # Folder where the data is found
g16_band15_sec_identifier = '*L2-CMIPF-M*C15_G16*.nc'                                 # Unique string on the file name
g16_band15_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band15_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band15_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_band15_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band15_sec_config     = '_SEC'                                                    # Configuration string
g16_band15_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band15_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band15_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band16_fdk            = True # GOES-16 L2 CMI - Band 16 - FULL DISK 

g16_band16_fdk_process    = 1                                                         # Process cicle for this product 
g16_band16_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band16//'               # Folder where the data is found
g16_band16_fdk_identifier = '*L2-CMIPF-M*C16_G16*.nc'                                 # Unique string on the file name
g16_band16_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_band16_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_band16_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band16_fdk_config     = ''                                                        # Configuration string
g16_band16_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g16_band16_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band16_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_band16_sec            = True # GOES-16 L2 CMI - Band 16 - USER SECTOR 

g16_band16_sec_process    = 1                                                         # Process cicle for this product 
g16_band16_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band16//'               # Folder where the data is found
g16_band16_sec_identifier = '*L2-CMIPF-M*C16_G16*.nc'                                 # Unique string on the file name
g16_band16_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_band16_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_band16_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_band16_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_band16_sec_config     = '_SEC'                                                    # Configuration string
g16_band16_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g16_band16_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_band16_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GOES-16 - ABI INDIVIDUAL L1B [RADIANCES] BANDS (FROM THE CLOUD - NEED TO ACTIVATE THE CLOUD MODULE!)
#######################################################################################################

#------------------------------------------------------------------------------------------------------
g16_radb01_fdk            = True # GOES-16 L1b RadF - Band 01 - FULL DISK 

g16_radb01_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb01_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band01//'              # Folder where the data is found
g16_radb01_fdk_identifier = '*L1b-RadF-M*C01_G16*.nc'                                 # Unique string on the file name
g16_radb01_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb01_fdk_resolution = 8  # Max Res.: 1 km                                       # Final plot resolution
g16_radb01_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb01_fdk_config     = ''                                                        # Configuration string
g16_radb01_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb01_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb01_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb01_sec            = True # GOES-16 L1b RadF - Band 01 - USER SECTOR 

g16_radb01_sec_process    = 1                                                         # Process cicle for this product 
g16_radb01_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band01//'              # Folder where the data is found
g16_radb01_sec_identifier = '*L1b-RadF-M*C01_G16*.nc'                                 # Unique string on the file name
g16_radb01_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb01_sec_extent     = [-54.0, -28.0, -43.0, -18.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb01_sec_resolution = 1  # Max Res.: 1 km                                       # Final plot resolution
g16_radb01_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb01_sec_config     = '_SEC'                                                    # Configuration string
g16_radb01_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb01_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb01_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb02_fdk            = True # GOES-16 L1b RadF - Band 02 - FULL DISK 

g16_radb02_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb02_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band02//'              # Folder where the data is found
g16_radb02_fdk_identifier = '*L1b-RadF-M*C02_G16*.nc'                                 # Unique string on the file name
g16_radb02_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb02_fdk_resolution = 8  # Max Res.: 0.5 km                                     # Final plot resolution
g16_radb02_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb02_fdk_config     = ''                                                        # Configuration string
g16_radb02_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb02_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb02_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb02_sec            = True # GOES-16 L1b RadF - Band 02 - USER SECTOR 

g16_radb02_sec_process    = 1                                                         # Process cicle for this product 
g16_radb02_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band02//'              # Folder where the data is found
g16_radb02_sec_identifier = '*L1b-RadF-M*C02_G16*.nc'                                 # Unique string on the file name
g16_radb02_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb02_sec_extent     = [-54.0, -28.0, -43.0, -18.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb02_sec_resolution = 1  # Max Res.: 0.5 km                                     # Final plot resolution
g16_radb02_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb02_sec_config     = '_SEC'                                                    # Configuration string
g16_radb02_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb02_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb02_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb03_fdk            = True # GOES-16 L1b RadF - Band 03 - FULL DISK 

g16_radb03_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb03_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band03//'              # Folder where the data is found
g16_radb03_fdk_identifier = '*L1b-RadF-M*C03_G16*.nc'                                 # Unique string on the file name
g16_radb03_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb03_fdk_resolution = 8  # Max Res.: 1 km                                       # Final plot resolution
g16_radb03_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb03_fdk_config     = ''                                                        # Configuration string
g16_radb03_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb03_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb03_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb03_sec            = True # GOES-16 L1b RadF - Band 03 - USER SECTOR 

g16_radb03_sec_process    = 1                                                         # Process cicle for this product 
g16_radb03_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band03//'              # Folder where the data is found
g16_radb03_sec_identifier = '*L1b-RadF-M*C03_G16*.nc'                                 # Unique string on the file name
g16_radb03_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb03_sec_extent     = [-54.0, -28.0, -43.0, -18.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb03_sec_resolution = 1  # Max Res.: 1 km                                       # Final plot resolution
g16_radb03_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb03_sec_config     = '_SEC'                                                    # Configuration string
g16_radb03_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb03_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb03_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb04_fdk            = True # GOES-16 L1b RadF - Band 04 - FULL DISK 

g16_radb04_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb04_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band04//'              # Folder where the data is found
g16_radb04_fdk_identifier = '*L1b-RadF-M*C04_G16*.nc'                                 # Unique string on the file name
g16_radb04_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb04_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_radb04_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb04_fdk_config     = ''                                                        # Configuration string
g16_radb04_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb04_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb04_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb04_sec            = True # GOES-16 L1b RadF - Band 04 - USER SECTOR 

g16_radb04_sec_process    = 1                                                         # Process cicle for this product 
g16_radb04_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band04//'              # Folder where the data is found
g16_radb04_sec_identifier = '*L1b-RadF-M*C04_G16*.nc'                                 # Unique string on the file name
g16_radb04_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb04_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb04_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_radb04_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb04_sec_config     = '_SEC'                                                    # Configuration string
g16_radb04_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb04_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb04_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb05_fdk            = True # GOES-16 L1b RadF - Band 05 - FULL DISK 

g16_radb05_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb05_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band05//'              # Folder where the data is found
g16_radb05_fdk_identifier = '*L1b-RadF-M*C05_G16*.nc'                                 # Unique string on the file name
g16_radb05_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb05_fdk_resolution = 8  # Max Res.: 1 km                                       # Final plot resolution
g16_radb05_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb05_fdk_config     = ''                                                        # Configuration string
g16_radb05_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb05_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb05_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb05_sec            = True # GOES-16 L1b RadF - Band 05 - USER SECTOR 

g16_radb05_sec_process    = 1                                                         # Process cicle for this product 
g16_radb05_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band05//'              # Folder where the data is found
g16_radb05_sec_identifier = '*L1b-RadF-M*C05_G16*.nc'                                 # Unique string on the file name
g16_radb05_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb05_sec_extent     = [-54.0, -28.0, -43.0, -18.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb05_sec_resolution = 1  # Max Res.: 1 km                                       # Final plot resolution
g16_radb05_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb05_sec_config     = '_SEC'                                                    # Configuration string
g16_radb05_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb05_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb05_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb06_fdk            = True # GOES-16 L1b RadF - Band 06 - FULL DISK 

g16_radb06_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb06_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band06//'              # Folder where the data is found
g16_radb06_fdk_identifier = '*L1b-RadF-M*C06_G16*.nc'                                 # Unique string on the file name
g16_radb06_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb06_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_radb06_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb06_fdk_config     = ''                                                        # Configuration string
g16_radb06_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb06_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb06_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb06_sec            = True # GOES-16 L1b RadF - Band 06 - USER SECTOR 

g16_radb06_sec_process    = 1                                                         # Process cicle for this product 
g16_radb06_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band06//'              # Folder where the data is found
g16_radb06_sec_identifier = '*L1b-RadF-M*C06_G16*.nc'                                 # Unique string on the file name
g16_radb06_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb06_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb06_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_radb06_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb06_sec_config     = '_SEC'                                                    # Configuration string
g16_radb06_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb06_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb06_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb07_fdk            = True # GOES-16 L1b RadF - Band 07 - FULL DISK 

g16_radb07_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb07_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band07//'              # Folder where the data is found
g16_radb07_fdk_identifier = '*L1b-RadF-M*C07_G16*.nc'                                 # Unique string on the file name
g16_radb07_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb07_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_radb07_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb07_fdk_config     = ''                                                        # Configuration string
g16_radb07_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb07_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb07_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb07_sec            = True # GOES-16 L1b RadF - Band 07 - USER SECTOR 

g16_radb07_sec_process    = 1                                                         # Process cicle for this product 
g16_radb07_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band07//'              # Folder where the data is found
g16_radb07_sec_identifier = '*L1b-RadF-M*C07_G16*.nc'                                 # Unique string on the file name
g16_radb07_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb07_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb07_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_radb07_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb07_sec_config     = '_SEC'                                                    # Configuration string
g16_radb07_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb07_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb07_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb08_fdk            = True # GOES-16 L1b RadF - Band 08 - FULL DISK 

g16_radb08_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb08_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band08//'              # Folder where the data is found
g16_radb08_fdk_identifier = '*L1b-RadF-M*C08_G16*.nc'                                 # Unique string on the file name
g16_radb08_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb08_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_radb08_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb08_fdk_config     = ''                                                        # Configuration string
g16_radb08_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb08_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb08_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb08_sec            = True # GOES-16 L1b RadF - Band 08 - USER SECTOR 

g16_radb08_sec_process    = 1                                                         # Process cicle for this product 
g16_radb08_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band08//'              # Folder where the data is found
g16_radb08_sec_identifier = '*L1b-RadF-M*C08_G16*.nc'                                 # Unique string on the file name
g16_radb08_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb08_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb08_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_radb08_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb08_sec_config     = '_SEC'                                                    # Configuration string
g16_radb08_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb08_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb08_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb09_fdk            = True # GOES-16 L1b RadF - Band 09 - FULL DISK 

g16_radb09_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb09_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band09//'              # Folder where the data is found
g16_radb09_fdk_identifier = '*L1b-RadF-M*C09_G16*.nc'                                 # Unique string on the file name
g16_radb09_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb09_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_radb09_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb09_fdk_config     = ''                                                        # Configuration string
g16_radb09_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb09_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb09_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb09_sec            = True # GOES-16 L1b RadF - Band 09 - USER SECTOR 

g16_radb09_sec_process    = 1                                                         # Process cicle for this product 
g16_radb09_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band09//'              # Folder where the data is found
g16_radb09_sec_identifier = '*L1b-RadF-M*C09_G16*.nc'                                 # Unique string on the file name
g16_radb09_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb09_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb09_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_radb09_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb09_sec_config     = '_SEC'                                                    # Configuration string
g16_radb09_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb09_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb09_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb10_fdk            = True # GOES-16 L1b RadF - Band 10 - FULL DISK 

g16_radb10_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb10_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band10//'              # Folder where the data is found
g16_radb10_fdk_identifier = '*L1b-RadF-M*C10_G16*.nc'                                 # Unique string on the file name
g16_radb10_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb10_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_radb10_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb10_fdk_config     = ''                                                        # Configuration string
g16_radb10_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb10_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb10_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb10_sec            = True # GOES-16 L1b RadF - Band 10 - USER SECTOR 

g16_radb10_sec_process    = 1                                                         # Process cicle for this product 
g16_radb10_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band10//'              # Folder where the data is found
g16_radb10_sec_identifier = '*L1b-RadF-M*C10_G16*.nc'                                 # Unique string on the file name
g16_radb10_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb10_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb10_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_radb10_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb10_sec_config     = '_SEC'                                                    # Configuration string
g16_radb10_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb10_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb10_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb11_fdk            = True # GOES-16 L1b RadF - Band 11 - FULL DISK 

g16_radb11_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb11_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band11//'              # Folder where the data is found
g16_radb11_fdk_identifier = '*L1b-RadF-M*C11_G16*.nc'                                 # Unique string on the file name
g16_radb11_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb11_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_radb11_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb11_fdk_config     = ''                                                        # Configuration string
g16_radb11_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb11_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb11_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb11_sec            = True # GOES-16 L1b RadF - Band 11 - USER SECTOR 

g16_radb11_sec_process    = 1                                                         # Process cicle for this product 
g16_radb11_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band11//'              # Folder where the data is found
g16_radb11_sec_identifier = '*L1b-RadF-M*C11_G16*.nc'                                 # Unique string on the file name
g16_radb11_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb11_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb11_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_radb11_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb11_sec_config     = '_SEC'                                                    # Configuration string
g16_radb11_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb11_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb11_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb12_fdk            = True # GOES-16 L1b RadF - Band 12 - FULL DISK 

g16_radb12_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb12_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band12//'              # Folder where the data is found
g16_radb12_fdk_identifier = '*L1b-RadF-M*C12_G16*.nc'                                 # Unique string on the file name
g16_radb12_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb12_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_radb12_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb12_fdk_config     = ''                                                        # Configuration string
g16_radb12_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb12_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb12_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb12_sec            = True # GOES-16 L1b RadF - Band 12 - USER SECTOR 

g16_radb12_sec_process    = 1                                                         # Process cicle for this product 
g16_radb12_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band12//'              # Folder where the data is found
g16_radb12_sec_identifier = '*L1b-RadF-M*C12_G16*.nc'                                 # Unique string on the file name
g16_radb12_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb12_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb12_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_radb12_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb12_sec_config     = '_SEC'                                                    # Configuration string
g16_radb12_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb12_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb12_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb13_fdk            = True # GOES-16 L1b RadF - Band 13 - FULL DISK 

g16_radb13_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb13_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band13//'              # Folder where the data is found
g16_radb13_fdk_identifier = '*L1b-RadF-M*C13_G16*.nc'                                 # Unique string on the file name
g16_radb13_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb13_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_radb13_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb13_fdk_config     = ''                                                        # Configuration string
g16_radb13_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb13_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb13_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb13_sec            = True # GOES-16 L1b RadF - Band 13 - USER SECTOR 

g16_radb13_sec_process    = 1                                                         # Process cicle for this product 
g16_radb13_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band13//'              # Folder where the data is found
g16_radb13_sec_identifier = '*L1b-RadF-M*C13_G16*.nc'                                 # Unique string on the file name
g16_radb13_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb13_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb13_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_radb13_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb13_sec_config     = '_SEC'                                                    # Configuration string
g16_radb13_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb13_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb13_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb14_fdk            = True # GOES-16 L1b RadF - Band 14 - FULL DISK 

g16_radb14_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb14_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band14//'              # Folder where the data is found
g16_radb14_fdk_identifier = '*L1b-RadF-M*C14_G16*.nc'                                 # Unique string on the file name
g16_radb14_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb14_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_radb14_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb14_fdk_config     = ''                                                        # Configuration string
g16_radb14_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb14_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb14_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb14_sec            = True # GOES-16 L1b RadF - Band 14 - USER SECTOR 

g16_radb14_sec_process    = 1                                                         # Process cicle for this product 
g16_radb14_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band14//'              # Folder where the data is found
g16_radb14_sec_identifier = '*L1b-RadF-M*C14_G16*.nc'                                 # Unique string on the file name
g16_radb14_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb14_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb14_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_radb14_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb14_sec_config     = '_SEC'                                                    # Configuration string
g16_radb14_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb14_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb14_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb15_fdk            = True # GOES-16 L1b RadF - Band 15 - FULL DISK 

g16_radb15_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb15_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band15//'              # Folder where the data is found
g16_radb15_fdk_identifier = '*L1b-RadF-M*C15_G16*.nc'                                 # Unique string on the file name
g16_radb15_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb15_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_radb15_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb15_fdk_config     = ''                                                        # Configuration string
g16_radb15_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb15_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb15_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb15_sec            = True # GOES-16 L1b RadF - Band 15 - USER SECTOR 

g16_radb15_sec_process    = 1                                                         # Process cicle for this product 
g16_radb15_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band15//'              # Folder where the data is found
g16_radb15_sec_identifier = '*L1b-RadF-M*C15_G16*.nc'                                 # Unique string on the file name
g16_radb15_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb15_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb15_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_radb15_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb15_sec_config     = '_SEC'                                                    # Configuration string
g16_radb15_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb15_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb15_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb16_fdk            = True # GOES-16 L1b RadF - Band 16 - FULL DISK 

g16_radb16_fdk_process    = 1                                                         # Process cicle for this product 
g16_radb16_fdk_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band16//'              # Folder where the data is found
g16_radb16_fdk_identifier = '*L1b-RadF-M*C16_G16*.nc'                                 # Unique string on the file name
g16_radb16_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb16_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_radb16_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb16_fdk_config     = ''                                                        # Configuration string
g16_radb16_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_fdk.py'  # Script to activate
g16_radb16_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb16_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_radb16_sec            = True# GOES-16 L1b RadF - Band 16 - USER SECTOR 

g16_radb16_sec_process    = 1                                                         # Process cicle for this product 
g16_radb16_sec_directory  = ingest_dir + 'GOES-R-RadF-Imagery//Band16//'              # Folder where the data is found
g16_radb16_sec_identifier = '*L1b-RadF-M*C16_G16*.nc'                                 # Unique string on the file name
g16_radb16_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_radb16_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_radb16_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_radb16_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_radb16_sec_config     = '_SEC'                                                    # Configuration string
g16_radb16_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_rad_sec.py'  # Script to activate
g16_radb16_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_radb16_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
#######################################################################################################
# GOES-16 RGB COMPOSITES
#######################################################################################################
#------------------------------------------------------------------------------------------------------
g16_24hrgb_fdk            = True # GOES-16 24h Microphysics RGB - FULL DISK

g16_24hrgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_24hrgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band15//'               # Folder where the data is found
g16_24hrgb_fdk_identifier = '*L2-CMIPF-M*C15_G16*.nc'                                 # Unique string on the file name
g16_24hrgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_24hrgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_24hrgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_24hrgb_fdk_config     = '_24H'                                                    # Configuration string
g16_24hrgb_fdk_script     = showcast_dir + '//Scripts//process_g16_24hrgb_fdk.py'     # Script to activate
g16_24hrgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_24hrgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_24hrgb_sec            = True # GOES-16 24h Microphysics RGB - USER SECTOR

g16_24hrgb_sec_process    = 1                                                         # Process cicle for this product 
g16_24hrgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band15//'               # Folder where the data is found
g16_24hrgb_sec_identifier = '*L2-CMIPF-M*C15_G16*.nc'                                 # Unique string on the file name
g16_24hrgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_24hrgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_24hrgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_24hrgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_24hrgb_sec_config     = '_24S'                                                    # Configuration string
g16_24hrgb_sec_script     = showcast_dir + '//Scripts//process_g16_24hrgb_sec.py'     # Script to activate
g16_24hrgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_24hrgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_armrgb_fdk            = True # GOES-16 Airmass RGB - FULL DISK

g16_armrgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_armrgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band08//'               # Folder where the data is found
g16_armrgb_fdk_identifier = '*L2-CMIPF-M*C08_G16*.nc'                                 # Unique string on the file name
g16_armrgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_armrgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_armrgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_armrgb_fdk_config     = '_ARM'                                                    # Configuration string
g16_armrgb_fdk_script     = showcast_dir + '//Scripts//process_g16_armrgb_fdk.py'     # Script to activate
g16_armrgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_armrgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_armrgb_sec            = True # GOES-16 Airmass RGB - USER SECTOR

g16_armrgb_sec_process    = 1                                                         # Process cicle for this product 
g16_armrgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band08//'               # Folder where the data is found
g16_armrgb_sec_identifier = '*L2-CMIPF-M*C08_G16*.nc'                                 # Unique string on the file name
g16_armrgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_armrgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_armrgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_armrgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_armrgb_sec_config     = '_ARS'                                                    # Configuration string
g16_armrgb_sec_script     = showcast_dir + '//Scripts//process_g16_armrgb_sec.py'     # Script to activate
g16_armrgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_armrgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_ashrgb_fdk            = True # GOES-16 Ash RGB - FULL DISK

g16_ashrgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_ashrgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band15//'               # Folder where the data is found
g16_ashrgb_fdk_identifier = '*L2-CMIPF-M*C15_G16*.nc'                                 # Unique string on the file name
g16_ashrgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_ashrgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_ashrgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_ashrgb_fdk_config     = '_ASH'                                                    # Configuration string
g16_ashrgb_fdk_script     = showcast_dir + '//Scripts//process_g16_ashrgb_fdk.py'     # Script to activate
g16_ashrgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_ashrgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_ashrgb_sec            = True # GOES-16 Ash RGB - USER SECTOR

g16_ashrgb_sec_process    = 1                                                         # Process cicle for this product 
g16_ashrgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band15//'               # Folder where the data is found
g16_ashrgb_sec_identifier = '*L2-CMIPF-M*C15_G16*.nc'                                 # Unique string on the file name
g16_ashrgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_ashrgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_ashrgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_ashrgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_ashrgb_sec_config     = '_ASS'                                                    # Configuration string
g16_ashrgb_sec_script     = showcast_dir + '//Scripts//process_g16_ashrgb_sec.py'     # Script to activate
g16_ashrgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_ashrgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_clprgb_fdk            = True # GOES-16 Cloud Phase RGB - FULL DISK

g16_clprgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_clprgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band05//'               # Folder where the data is found
g16_clprgb_fdk_identifier = '*L2-CMIPF-M*C05_G16*.nc'                                 # Unique string on the file name
g16_clprgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_clprgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_clprgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_clprgb_fdk_config     = '_CLP'                                                    # Configuration string
g16_clprgb_fdk_script     = showcast_dir + '//Scripts//process_g16_clprgb_fdk.py'     # Script to activate
g16_clprgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_clprgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_clprgb_sec            = True # GOES-16 Cloud Phase RGB - USER SECTOR

g16_clprgb_sec_process    = 1                                                         # Process cicle for this product 
g16_clprgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band05//'               # Folder where the data is found
g16_clprgb_sec_identifier = '*L2-CMIPF-M*C05_G16*.nc'                                 # Unique string on the file name
g16_clprgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_clprgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_clprgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_clprgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_clprgb_sec_config     = '_CLS'                                                    # Configuration string
g16_clprgb_sec_script     = showcast_dir + '//Scripts//process_g16_clprgb_sec.py'     # Script to activate
g16_clprgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_clprgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dccrgb_fdk            = True # GOES-16 Day Cloud Convection RGB - FULL DISK

g16_dccrgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_dccrgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band02//'               # Folder where the data is found
g16_dccrgb_fdk_identifier = '*L2-CMIPF-M*C02_G16*.nc'                                 # Unique string on the file name
g16_dccrgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_dccrgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_dccrgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dccrgb_fdk_config     = '_DCC'                                                    # Configuration string
g16_dccrgb_fdk_script     = showcast_dir + '//Scripts//process_g16_dccrgb_fdk.py'     # Script to activate
g16_dccrgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dccrgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dccrgb_sec            = True # GOES-16 Day Cloud Convection RGB - USER SECTOR

g16_dccrgb_sec_process    = 1                                                         # Process cicle for this product 
g16_dccrgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band02//'               # Folder where the data is found
g16_dccrgb_sec_identifier = '*L2-CMIPF-M*C02_G16*.nc'                                 # Unique string on the file name
g16_dccrgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_dccrgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_dccrgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_dccrgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dccrgb_sec_config     = '_DCS'                                                    # Configuration string
g16_dccrgb_sec_script     = showcast_dir + '//Scripts//process_g16_dccrgb_sec.py'     # Script to activate
g16_dccrgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dccrgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dcprgb_fdk            = True # GOES-16 Day Cloud Phase RGB - FULL DISK

g16_dcprgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_dcprgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band13//'               # Folder where the data is found
g16_dcprgb_fdk_identifier = '*L2-CMIPF-M*C13_G16*.nc'                                 # Unique string on the file name
g16_dcprgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_dcprgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_dcprgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dcprgb_fdk_config     = '_DCP'                                                    # Configuration string
g16_dcprgb_fdk_script     = showcast_dir + '//Scripts//process_g16_dcprgb_fdk.py'     # Script to activate
g16_dcprgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dcprgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dcprgb_sec            = True # GOES-16 Day Cloud Phase RGB - USER SECTOR

g16_dcprgb_sec_process    = 1                                                         # Process cicle for this product 
g16_dcprgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band13//'               # Folder where the data is found
g16_dcprgb_sec_identifier = '*L2-CMIPF-M*C13_G16*.nc'                                 # Unique string on the file name
g16_dcprgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_dcprgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_dcprgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_dcprgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dcprgb_sec_config     = '_DCS'                                                    # Configuration string
g16_dcprgb_sec_script     = showcast_dir + '//Scripts//process_g16_dcprgb_sec.py'     # Script to activate
g16_dcprgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dcprgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_conrgb_fdk            = True # GOES-16 Convection RGB - FULL DISK

g16_conrgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_conrgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band08//'               # Folder where the data is found
g16_conrgb_fdk_identifier = '*L2-CMIPF-M*C08_G16*.nc'                                 # Unique string on the file name
g16_conrgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_conrgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_conrgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_conrgb_fdk_config     = '_CON'                                                    # Configuration string
g16_conrgb_fdk_script     = showcast_dir + '//Scripts//process_g16_conrgb_fdk.py'     # Script to activate
g16_conrgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_conrgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_conrgb_sec            = True # GOES-16 Convection RGB - USER SECTOR

g16_conrgb_sec_process    = 1                                                         # Process cicle for this product 
g16_conrgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band08//'               # Folder where the data is found
g16_conrgb_sec_identifier = '*L2-CMIPF-M*C08_G16*.nc'                                 # Unique string on the file name
g16_conrgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_conrgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_conrgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_conrgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_conrgb_sec_config     = '_COS'                                                    # Configuration string
g16_conrgb_sec_script     = showcast_dir + '//Scripts//process_g16_conrgb_sec.py'     # Script to activate
g16_conrgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_conrgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dlcrgb_fdk            = True # GOES-16 Day Land Cloud RGB - FULL DISK

g16_dlcrgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_dlcrgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band05//'               # Folder where the data is found
g16_dlcrgb_fdk_identifier = '*L2-CMIPF-M*C05_G16*.nc'                                 # Unique string on the file name
g16_dlcrgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_dlcrgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_dlcrgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dlcrgb_fdk_config     = '_DLC'                                                        # Configuration string
g16_dlcrgb_fdk_script     = showcast_dir + '//Scripts//process_g16_dlcrgb_fdk.py'     # Script to activate
g16_dlcrgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dlcrgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dlcrgb_sec            = True # GOES-16 Day Land Cloud RGB - USER SECTOR

g16_dlcrgb_sec_process    = 1                                                         # Process cicle for this product 
g16_dlcrgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band05//'               # Folder where the data is found
g16_dlcrgb_sec_identifier = '*L2-CMIPF-M*C05_G16*.nc'                                 # Unique string on the file name
g16_dlcrgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_dlcrgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_dlcrgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_dlcrgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dlcrgb_sec_config     = '_DLS'                                                    # Configuration string
g16_dlcrgb_sec_script     = showcast_dir + '//Scripts//process_g16_dlcrgb_sec.py'     # Script to activate
g16_dlcrgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dlcrgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dlfrgb_fdk            = True # GOES-16 Day Land Cloud RGB - FULL DISK

g16_dlfrgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_dlfrgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band06//'               # Folder where the data is found
g16_dlfrgb_fdk_identifier = '*L2-CMIPF-M*C06_G16*.nc'                                 # Unique string on the file name
g16_dlfrgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_dlfrgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_dlfrgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dlfrgb_fdk_config     = '_DFR'                                                        # Configuration string
g16_dlfrgb_fdk_script     = showcast_dir + '//Scripts//process_g16_dlfrgb_fdk.py'     # Script to activate
g16_dlfrgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dlfrgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dlfrgb_sec            = True # GOES-16 Day Land Cloud RGB - USER SECTOR

g16_dlfrgb_sec_process    = 1                                                         # Process cicle for this product 
g16_dlfrgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band06//'               # Folder where the data is found
g16_dlfrgb_sec_identifier = '*L2-CMIPF-M*C06_G16*.nc'                                 # Unique string on the file name
g16_dlfrgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_dlfrgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_dlfrgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_dlfrgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dlfrgb_sec_config     = '_DFS'                                                    # Configuration string
g16_dlfrgb_sec_script     = showcast_dir + '//Scripts//process_g16_dlfrgb_sec.py'     # Script to activate
g16_dlfrgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dlfrgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dmprgb_fdk            = True # GOES-16 Day Microphysics RGB - FULL DISK

g16_dmprgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_dmprgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band07//'               # Folder where the data is found
g16_dmprgb_fdk_identifier = '*L2-CMIPF-M*C07_G16*.nc'                                 # Unique string on the file name
g16_dmprgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_dmprgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_dmprgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dmprgb_fdk_config     = '_DMP'                                                    # Configuration string
g16_dmprgb_fdk_script     = showcast_dir + '//Scripts//process_g16_dmprgb_fdk.py'     # Script to activate
g16_dmprgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dmprgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dmprgb_sec            = True # GOES-16 Day Microphysics RGB - USER SECTOR

g16_dmprgb_sec_process    = 1                                                         # Process cicle for this product 
g16_dmprgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band07//'               # Folder where the data is found
g16_dmprgb_sec_identifier = '*L2-CMIPF-M*C07_G16*.nc'                                 # Unique string on the file name
g16_dmprgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_dmprgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_dmprgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_dmprgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dmprgb_sec_config     = '_DMS'                                                    # Configuration string
g16_dmprgb_sec_script     = showcast_dir + '//Scripts//process_g16_dmprgb_sec.py'     # Script to activate
g16_dmprgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dmprgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dsfrgb_fdk            = True # GOES-16 Day Snow Fog RGB - FULL DISK

g16_dsfrgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_dsfrgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band03//'               # Folder where the data is found
g16_dsfrgb_fdk_identifier = '*L2-CMIPF-M*C03_G16*.nc'                                 # Unique string on the file name
g16_dsfrgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_dsfrgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_dsfrgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dsfrgb_fdk_config     = '_DSF'                                                    # Configuration string
g16_dsfrgb_fdk_script     = showcast_dir + '//Scripts//process_g16_dsfrgb_fdk.py'     # Script to activate
g16_dsfrgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dsfrgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dsfrgb_sec            = True # GOES-16 Day Snow Fog RGB - USER SECTOR

g16_dsfrgb_sec_process    = 1                                                         # Process cicle for this product 
g16_dsfrgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band03//'               # Folder where the data is found
g16_dsfrgb_sec_identifier = '*L2-CMIPF-M*C03_G16*.nc'                                 # Unique string on the file name
g16_dsfrgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_dsfrgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_dsfrgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_dsfrgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dsfrgb_sec_config     = '_DSS'                                                    # Configuration string
g16_dsfrgb_sec_script     = showcast_dir + '//Scripts//process_g16_dsfrgb_sec.py'     # Script to activate
g16_dsfrgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dsfrgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dwvrgb_fdk            = True # GOES-16 Differential Water Vapor RGB - FULL DISK

g16_dwvrgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_dwvrgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band10//'               # Folder where the data is found
g16_dwvrgb_fdk_identifier = '*L2-CMIPF-M*C10_G16*.nc'                                 # Unique string on the file name
g16_dwvrgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_dwvrgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_dwvrgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dwvrgb_fdk_config     = '_DWV'                                                    # Configuration string
g16_dwvrgb_fdk_script     = showcast_dir + '//Scripts//process_g16_dwvrgb_fdk.py'     # Script to activate
g16_dwvrgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dwvrgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dwvrgb_sec            = True # GOES-16 Differential Water Vapor RGB - USER SECTOR

g16_dwvrgb_sec_process    = 1                                                         # Process cicle for this product 
g16_dwvrgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band10//'               # Folder where the data is found
g16_dwvrgb_sec_identifier = '*L2-CMIPF-M*C10_G16*.nc'                                 # Unique string on the file name
g16_dwvrgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_dwvrgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_dwvrgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_dwvrgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dwvrgb_sec_config     = '_DWS'                                                    # Configuration string
g16_dwvrgb_sec_script     = showcast_dir + '//Scripts//process_g16_dwvrgb_sec.py'     # Script to activate
g16_dwvrgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dwvrgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dstrgb_fdk            = True # GOES-16 Dust RGB - FULL DISK

g16_dstrgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_dstrgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band15//'               # Folder where the data is found
g16_dstrgb_fdk_identifier = '*L2-CMIPF-M*C15_G16*.nc'                                 # Unique string on the file name
g16_dstrgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_dstrgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_dstrgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dstrgb_fdk_config     = '_DST'                                                    # Configuration string
g16_dstrgb_fdk_script     = showcast_dir + '//Scripts//process_g16_dstrgb_fdk.py'     # Script to activate
g16_dstrgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dstrgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dstrgb_sec            = True # GOES-16 Dust RGB - USER SECTOR

g16_dstrgb_sec_process    = 1                                                         # Process cicle for this product 
g16_dstrgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band15//'               # Folder where the data is found
g16_dstrgb_sec_identifier = '*L2-CMIPF-M*C15_G16*.nc'                                 # Unique string on the file name
g16_dstrgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_dstrgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_dstrgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_dstrgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dstrgb_sec_config     = '_DSS'                                                    # Configuration string
g16_dstrgb_sec_script     = showcast_dir + '//Scripts//process_g16_dstrgb_sec.py'     # Script to activate
g16_dstrgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dstrgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_fcorgb_fdk            = True # GOES-16 False Color RGB - FULL DISK

g16_fcorgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_fcorgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band01//'               # Folder where the data is found
g16_fcorgb_fdk_identifier = '*L2-CMIPF-M*C01_G16*.nc'                                 # Unique string on the file name
g16_fcorgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_fcorgb_fdk_resolution = 8  # Max Res.: 1 km                                       # Final plot resolution
g16_fcorgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_fcorgb_fdk_config     = '_FCO'                                                    # Configuration string
g16_fcorgb_fdk_script     = showcast_dir + '//Scripts//process_g16_fcorgb_fdk.py'     # Script to activate
g16_fcorgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_fcorgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_fcorgb_sec            = True # GOES-16 False Color RGB - USER SECTOR

g16_fcorgb_sec_process    = 1                                                         # Process cicle for this product 
g16_fcorgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band01//'               # Folder where the data is found
g16_fcorgb_sec_identifier = '*L2-CMIPF-M*C01_G16*.nc'                                 # Unique string on the file name
g16_fcorgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_fcorgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_fcorgb_sec_resolution = 2  # Max Res.: 1 km                                       # Final plot resolution
g16_fcorgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_fcorgb_sec_config     = '_FCS'                                                    # Configuration string
g16_fcorgb_sec_script     = showcast_dir + '//Scripts//process_g16_fcorgb_sec.py'     # Script to activate
g16_fcorgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_fcorgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_ftprgb_fdk            = True # GOES-16 Fire Temperature RGB - FULL DISK

g16_ftprgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_ftprgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band07//'               # Folder where the data is found
g16_ftprgb_fdk_identifier = '*L2-CMIPF-M*C07_G16*.nc'                                 # Unique string on the file name
g16_ftprgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_ftprgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_ftprgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_ftprgb_fdk_config     = '_FTP'                                                    # Configuration string
g16_ftprgb_fdk_script     = showcast_dir + '//Scripts//process_g16_ftprgb_fdk.py'     # Script to activate
g16_ftprgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_ftprgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_ftprgb_sec            = True # GOES-16 Fire Temperature RGB - USER SECTOR

g16_ftprgb_sec_process    = 1                                                         # Process cicle for this product 
g16_ftprgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band07//'               # Folder where the data is found
g16_ftprgb_sec_identifier = '*L2-CMIPF-M*C07_G16*.nc'                                 # Unique string on the file name
g16_ftprgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_ftprgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_ftprgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_ftprgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_ftprgb_sec_config     = '_FTS'                                                    # Configuration string
g16_ftprgb_sec_script     = showcast_dir + '//Scripts//process_g16_ftprgb_sec.py'     # Script to activate
g16_ftprgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_ftprgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_ntcrgb_fdk            = True # GOES-16 Natural True Color RGB - FULL DISK

g16_ntcrgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_ntcrgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band01//'               # Folder where the data is found
g16_ntcrgb_fdk_identifier = '*L2-CMIPF-M*C01_G16*.nc'                                 # Unique string on the file name
g16_ntcrgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_ntcrgb_fdk_resolution = 8  # Max Res.: 1 km                                       # Final plot resolution
g16_ntcrgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_ntcrgb_fdk_config     = '_NTC'                                                    # Configuration string
g16_ntcrgb_fdk_script     = showcast_dir + '//Scripts//process_g16_ntcrgb_fdk.py'     # Script to activate
g16_ntcrgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_ntcrgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_ntcrgb_sec            = True # GOES-16 Natural True Color RGB - USER SECTOR

g16_ntcrgb_sec_process    = 1                                                         # Process cicle for this product 
g16_ntcrgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band01//'               # Folder where the data is found
g16_ntcrgb_sec_identifier = '*L2-CMIPF-M*C01_G16*.nc'                                 # Unique string on the file name
g16_ntcrgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_ntcrgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_ntcrgb_sec_resolution = 2  # Max Res.: 1 km                                       # Final plot resolution
g16_ntcrgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_ntcrgb_sec_config     = '_NTS'                                                    # Configuration string
g16_ntcrgb_sec_script     = showcast_dir + '//Scripts//process_g16_ntcrgb_sec.py'     # Script to activate
g16_ntcrgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_ntcrgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_nmprgb_fdk            = True # GOES-16 Day Cloud Phase RGB - FULL DISK

g16_nmprgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_nmprgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band15//'               # Folder where the data is found
g16_nmprgb_fdk_identifier = '*L2-CMIPF-M*C15_G16*.nc'                                 # Unique string on the file name
g16_nmprgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_nmprgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_nmprgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_nmprgb_fdk_config     = '_NMP'                                                    # Configuration string
g16_nmprgb_fdk_script     = showcast_dir + '//Scripts//process_g16_nmprgb_fdk.py'     # Script to activate
g16_nmprgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_nmprgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_nmprgb_sec            = True # GOES-16 Day Cloud Phase RGB - USER SECTOR

g16_nmprgb_sec_process    = 1                                                         # Process cicle for this product 
g16_nmprgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band15//'               # Folder where the data is found
g16_nmprgb_sec_identifier = '*L2-CMIPF-M*C15_G16*.nc'                                 # Unique string on the file name
g16_nmprgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_nmprgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_nmprgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_nmprgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_nmprgb_sec_config     = '_NMS'                                                    # Configuration string
g16_nmprgb_sec_script     = showcast_dir + '//Scripts//process_g16_nmprgb_sec.py'     # Script to activate
g16_nmprgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_nmprgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_swvrgb_fdk            = True # GOES-16 Simple Water Vapor RGB - FULL DISK

g16_swvrgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_swvrgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band10//'               # Folder where the data is found
g16_swvrgb_fdk_identifier = '*L2-CMIPF-M*C10_G16*.nc'                                 # Unique string on the file name
g16_swvrgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_swvrgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_swvrgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_swvrgb_fdk_config     = '_SVV'                                                    # Configuration string
g16_swvrgb_fdk_script     = showcast_dir + '//Scripts//process_g16_swvrgb_fdk.py'     # Script to activate
g16_swvrgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_swvrgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_swvrgb_sec            = True # GOES-16 Simple Water Vapor RGB - USER SECTOR

g16_swvrgb_sec_process    = 1                                                         # Process cicle for this product 
g16_swvrgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band10//'               # Folder where the data is found
g16_swvrgb_sec_identifier = '*L2-CMIPF-M*C10_G16*.nc'                                 # Unique string on the file name
g16_swvrgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_swvrgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_swvrgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_swvrgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_swvrgb_sec_config     = '_SVS'                                                    # Configuration string
g16_swvrgb_sec_script     = showcast_dir + '//Scripts//process_g16_swvrgb_sec.py'     # Script to activate
g16_swvrgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_swvrgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_so2rgb_fdk            = True # GOES-16 SO2 RGB - FULL DISK

g16_so2rgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_so2rgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band09//'               # Folder where the data is found
g16_so2rgb_fdk_identifier = '*L2-CMIPF-M*C09_G16*.nc'                                 # Unique string on the file name
g16_so2rgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_so2rgb_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_so2rgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_so2rgb_fdk_config     = '_SO2'                                                    # Configuration string
g16_so2rgb_fdk_script     = showcast_dir + '//Scripts//process_g16_so2rgb_fdk.py'     # Script to activate
g16_so2rgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_so2rgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_so2rgb_sec            = True # GOES-16 SO2 RGB - USER SECTOR

g16_so2rgb_sec_process    = 1                                                         # Process cicle for this product 
g16_so2rgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band09//'               # Folder where the data is found
g16_so2rgb_sec_identifier = '*L2-CMIPF-M*C09_G16*.nc'                                 # Unique string on the file name
g16_so2rgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_so2rgb_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_so2rgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_so2rgb_sec_config     = '_SOS'                                                    # Configuration string
g16_so2rgb_sec_script     = showcast_dir + '//Scripts//process_g16_so2rgb_sec.py'     # Script to activate
g16_so2rgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_so2rgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_trurgb_fdk            = True # GOES-16 True Color RGB - FULL DISK

g16_trurgb_fdk_process    = 1                                                         # Process cicle for this product 
g16_trurgb_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band01//'               # Folder where the data is found
g16_trurgb_fdk_identifier = '*L2-CMIPF-M*C01_G16*.nc'                                 # Unique string on the file name
g16_trurgb_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_trurgb_fdk_resolution = 8  # Max Res.: 1 km                                       # Final plot resolution
g16_trurgb_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_trurgb_fdk_config     = '_TRU'                                                    # Configuration string
g16_trurgb_fdk_script     = showcast_dir + '//Scripts//process_g16_trurgb_fdk.py'     # Script to activate
g16_trurgb_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_trurgb_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_trurgb_sec            = True # GOES-16 True Color RGB - FULL DISK

g16_trurgb_sec_process    = 1                                                         # Process cicle for this product 
g16_trurgb_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band01//'               # Folder where the data is found
g16_trurgb_sec_identifier =  '*L2-CMIPF-M*C01_G16*.nc'                                # Unique string on the file name
g16_trurgb_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_trurgb_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_trurgb_sec_resolution = 2  # Max Res.: 1 km                                       # Final plot resolution
g16_trurgb_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_trurgb_sec_config     = '_TRS'                                                    # Configuration string
g16_trurgb_sec_script     = showcast_dir + '//Scripts//process_g16_trurgb_sec.py'     # Script to activate
g16_trurgb_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_trurgb_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GOES-16 BASELINE PRODUCTS (FROM GEONETCAST-AMERICAS AND / OR CLOUD)
#######################################################################################################

#------------------------------------------------------------------------------------------------------
g16_cldhgt_fdk            = True # GOES-16 L2 ACHAF - Cloud Top Height - FULL DISK

g16_cldhgt_fdk_process    = 1                                                         # Process cicle for this product 
g16_cldhgt_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//ACHAF//'           # Folder where the data is found
g16_cldhgt_fdk_identifier = '*ACHAF*.nc'                                              # Unique string on the file name
g16_cldhgt_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_cldhgt_fdk_resolution = 8  # Max Res.: 10 km                                      # Final plot resolution
g16_cldhgt_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_cldhgt_fdk_config     = ''                                                        # Configuration string
g16_cldhgt_fdk_script     = showcast_dir + '//Scripts//process_g16_baseline_fdk.py'   # Script to activate
g16_cldhgt_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_cldhgt_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_cldhgt_sec            = True # GOES-16 L2 ACHAF - Cloud Top Height - USER SECTOR

g16_cldhgt_sec_process    = 1                                                         # Process cicle for this product 
g16_cldhgt_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//ACHAF//'           # Folder where the data is found
g16_cldhgt_sec_identifier = '*ACHAF*.nc'                                              # Unique string on the file name
g16_cldhgt_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_cldhgt_sec_extent     = [-105.0, -60.0, -15.0, 20.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_cldhgt_sec_resolution = 10  # Max Res.: 10 km                                     # Final plot resolution
g16_cldhgt_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_cldhgt_sec_config     = '_SEC'                                                    # Configuration string
g16_cldhgt_sec_script     = showcast_dir + '//Scripts//process_g16_baseline_sec.py'   # Script to activate
g16_cldhgt_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_cldhgt_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_cldtmp_fdk            = True # GOES-16 L2 ACHTF - Cloud Top Temperature - FULL DISK

g16_cldtmp_fdk_process    = 1                                                         # Process cicle for this product 
g16_cldtmp_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//ACHTF//'           # Folder where the data is found
g16_cldtmp_fdk_identifier = '*ACHTF*.nc'                                              # Unique string on the file name
g16_cldtmp_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_cldtmp_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_cldtmp_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_cldtmp_fdk_config     = ''                                                        # Configuration string
g16_cldtmp_fdk_script     = showcast_dir + '//Scripts//process_g16_baseline_fdk.py'   # Script to activate
g16_cldtmp_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_cldtmp_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_cldtmp_sec            = True # GOES-16 L2 ACHTF - Cloud Top Temperature - USER SECTOR

g16_cldtmp_sec_process    = 1                                                         # Process cicle for this product 
g16_cldtmp_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//ACHTF//'           # Folder where the data is found
g16_cldtmp_sec_identifier = '*ACHTF*.nc'                                              # Unique string on the file name
g16_cldtmp_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_cldtmp_sec_extent     = [-105.0, -60.0, -15.0, 20.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_cldtmp_sec_resolution = 10  # Max Res.: 2 km                                      # Final plot resolution
g16_cldtmp_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_cldtmp_sec_config     = '_SEC'                                                    # Configuration string
g16_cldtmp_sec_script     = showcast_dir + '//Scripts//process_g16_baseline_sec.py'   # Script to activate
g16_cldtmp_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_cldtmp_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_cldmsk_fdk            = True # GOES-16 L2 ACMF - Clear Sky Masks - FULL DISK

g16_cldmsk_fdk_process    = 1                                                         # Process cicle for this product 
g16_cldmsk_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//ACMF//'            # Folder where the data is found
g16_cldmsk_fdk_identifier = '*ACMF*.nc'                                               # Unique string on the file name
g16_cldmsk_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_cldmsk_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_cldmsk_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_cldmsk_fdk_config     = ''                                                        # Configuration string
g16_cldmsk_fdk_script     = showcast_dir + '//Scripts//process_g16_baseline_fdk.py'   # Script to activate
g16_cldmsk_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_cldmsk_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_cldmsk_sec            = True # GOES-16 L2 ACMF - Clear Sky Masks - USER SECTOR

g16_cldmsk_sec_process    = 1                                                         # Process cicle for this product 
g16_cldmsk_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//ACMF//'            # Folder where the data is found
g16_cldmsk_sec_identifier = '*ACMF*.nc'                                               # Unique string on the file name
g16_cldmsk_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_cldmsk_sec_extent     = [-105.0, -60.0, -15.0, 20.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_cldmsk_sec_resolution = 10  # Max Res.: 2 km                                      # Final plot resolution
g16_cldmsk_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_cldmsk_sec_config     = '_SEC'                                                    # Configuration string
g16_cldmsk_sec_script     = showcast_dir + '//Scripts//process_g16_baseline_sec.py'   # Script to activate
g16_cldmsk_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_cldmsk_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_cldpha_fdk            = True # GOES-16 L2 ACTPF - Cloud Top Phase - FULL DISK

g16_cldpha_fdk_process    = 1                                                         # Process cicle for this product 
g16_cldpha_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//ACTPF//'           # Folder where the data is found
g16_cldpha_fdk_identifier = '*ACTPF*.nc'                                              # Unique string on the file name
g16_cldpha_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_cldpha_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_cldpha_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_cldpha_fdk_config     = ''                                                        # Configuration string
g16_cldpha_fdk_script     = showcast_dir + '//Scripts//process_g16_baseline_fdk.py'   # Script to activate
g16_cldpha_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_cldpha_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_cldpha_sec            = True # GOES-16 L2 ACTPF - Cloud Top Phase - USER SECTOR

g16_cldpha_sec_process    = 1                                                         # Process cicle for this product 
g16_cldpha_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//ACTPF//'           # Folder where the data is found
g16_cldpha_sec_identifier = '*ACTPF*.nc'                                              # Unique string on the file name
g16_cldpha_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_cldpha_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_cldpha_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_cldpha_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_cldpha_sec_config     = '_SEC'                                                    # Configuration string
g16_cldpha_sec_script     = showcast_dir + '//Scripts//process_g16_baseline_sec.py'   # Script to activate
g16_cldpha_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_cldpha_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_aerdet_fdk            = True # GOES-16 L2 ADPF - Aerosol Detection - FULL DISK

g16_aerdet_fdk_process    = 1                                                         # Process cicle for this product 
g16_aerdet_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//ADPF//'            # Folder where the data is found
g16_aerdet_fdk_identifier = '*ADPF*.nc'                                               # Unique string on the file name
g16_aerdet_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_aerdet_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_aerdet_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_aerdet_fdk_config     = ''                                                        # Configuration string
g16_aerdet_fdk_script     = showcast_dir + '//Scripts//process_g16_adpf_fdk.py'       # Script to activate
g16_aerdet_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_aerdet_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_aerdet_sec            = True # GOES-16 L2 ADPF - Aerosol Detection - USER SECTOR

g16_aerdet_sec_process    = 1                                                         # Process cicle for this product 
g16_aerdet_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//ADPF//'            # Folder where the data is found
g16_aerdet_sec_identifier = '*ADPF*.nc'                                               # Unique string on the file name
g16_aerdet_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_aerdet_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_aerdet_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_aerdet_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_aerdet_sec_config     = '_SEC'                                                    # Configuration string
g16_aerdet_sec_script     = showcast_dir + '//Scripts//process_g16_adpf_sec.py'       # Script to activate
g16_aerdet_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_aerdet_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_aeropt_fdk            = True # GOES-16 L2 AODF - Aerosol Optical Depth - FULL DISK

g16_aeropt_fdk_process    = 1                                                         # Process cicle for this product 
g16_aeropt_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//AODF//'            # Folder where the data is found
g16_aeropt_fdk_identifier = '*AODF*.nc'                                               # Unique string on the file name
g16_aeropt_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_aeropt_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_aeropt_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_aeropt_fdk_config     = ''                                                        # Configuration string
g16_aeropt_fdk_script     = showcast_dir + '//Scripts//process_g16_baseline_fdk.py'   # Script to activate
g16_aeropt_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_aeropt_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_aeropt_sec            = True # GOES-16 L2 AODF - Aerosol Optical Depth - USER SECTOR

g16_aeropt_sec_process    = 1                                                         # Process cicle for this product 
g16_aeropt_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//AODF//'            # Folder where the data is found
g16_aeropt_sec_identifier = '*AODF*.nc'                                               # Unique string on the file name
g16_aeropt_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_aeropt_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_aeropt_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_aeropt_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_aeropt_sec_config     = '_SEC'                                                    # Configuration string
g16_aeropt_sec_script     = showcast_dir + '//Scripts//process_g16_baseline_sec.py'   # Script to activate
g16_aeropt_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_aeropt_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_cldopt_fdk            = True # GOES-16 L2 CODF - Cloud Optical Depth - FULL DISK

g16_cldopt_fdk_process    = 1                                                         # Process cicle for this product 
g16_cldopt_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//CODF//'            # Folder where the data is found
g16_cldopt_fdk_identifier = '*CODF*.nc'                                               # Unique string on the file name
g16_cldopt_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_cldopt_fdk_resolution = 8  # Max Res.: 4 km                                       # Final plot resolution
g16_cldopt_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_cldopt_fdk_config     = ''                                                        # Configuration string
g16_cldopt_fdk_script     = showcast_dir + '//Scripts//process_g16_baseline_fdk.py'   # Script to activate
g16_cldopt_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_cldopt_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_cldopt_sec            = True # GOES-16 L2 CODF - Cloud Optical Depth - USER SECTOR

g16_cldopt_sec_process    = 1                                                         # Process cicle for this product 
g16_cldopt_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//CODF//'            # Folder where the data is found
g16_cldopt_sec_identifier = '*CODF*.nc'                                               # Unique string on the file name
g16_cldopt_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_cldopt_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_cldopt_sec_resolution = 4  # Max Res.: 4 km                                       # Final plot resolution
g16_cldopt_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_cldopt_sec_config     = '_SEC'                                                    # Configuration string
g16_cldopt_sec_script     = showcast_dir + '//Scripts//process_g16_baseline_sec.py'   # Script to activate
g16_cldopt_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_cldopt_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_cldpas_fdk            = True # GOES-16 L2 CPSF - Cloud Particle Size - FULL DISK

g16_cldpas_fdk_process    = 1                                                         # Process cicle for this product 
g16_cldpas_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//CPSF//'            # Folder where the data is found
g16_cldpas_fdk_identifier = '*CPSF*.nc'                                               # Unique string on the file name
g16_cldpas_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_cldpas_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_cldpas_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_cldpas_fdk_config     = ''                                                        # Configuration string
g16_cldpas_fdk_script     = showcast_dir + '//Scripts//process_g16_baseline_fdk.py'   # Script to activate
g16_cldpas_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_cldpas_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_cldpas_sec            = True # GOES-16 L2 CODF - Cloud Optical Depth - USER SECTOR

g16_cldpas_sec_process    = 1                                                         # Process cicle for this product 
g16_cldpas_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//CPSF//'            # Folder where the data is found
g16_cldpas_sec_identifier = '*CPSF*.nc'                                               # Unique string on the file name
g16_cldpas_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_cldpas_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_cldpas_sec_resolution = 4  # Max Res.: 2 km                                       # Final plot resolution
g16_cldpas_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_cldpas_sec_config     = '_SEC'                                                    # Configuration string
g16_cldpas_sec_script     = showcast_dir + '//Scripts//process_g16_baseline_sec.py'   # Script to activate
g16_cldpas_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_cldpas_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_cldpre_fdk            = True # GOES-16 L2 CTPF - Cloud Top Pressure - FULL DISK

g16_cldpre_fdk_process    = 1                                                         # Process cicle for this product 
g16_cldpre_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//CTPF//'            # Folder where the data is found
g16_cldpre_fdk_identifier = '*CTPF*.nc'                                               # Unique string on the file name
g16_cldpre_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_cldpre_fdk_resolution = 10  # Max Res.: 10 km                                     # Final plot resolution
g16_cldpre_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_cldpre_fdk_config     = ''                                                        # Configuration string
g16_cldpre_fdk_script     = showcast_dir + '//Scripts//process_g16_baseline_fdk.py'   # Script to activate
g16_cldpre_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_cldpre_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_cldpre_sec            = True # GOES-16 L2 CTPF - Cloud Top Pressure - USER SECTOR

g16_cldpre_sec_process    = 1                                                         # Process cicle for this product 
g16_cldpre_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//CTPF//'            # Folder where the data is found
g16_cldpre_sec_identifier = '*CTPF*.nc'                                               # Unique string on the file name
g16_cldpre_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_cldpre_sec_extent     = [-105.0, -60.0, -15.0, 20.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_cldpre_sec_resolution = 10  # Max Res.: 10 km                                     # Final plot resolution
g16_cldpre_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_cldpre_sec_config     = '_SEC'                                                    # Configuration string
g16_cldpre_sec_script     = showcast_dir + '//Scripts//process_g16_baseline_sec.py'   # Script to activate
g16_cldpre_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_cldpre_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dmwf14_fdk            = True # GOES-16 L2 DMWF-C14 - Derived Motion Winds Band 14 - FULL DISK

g16_dmwf14_fdk_process    = 1                                                         # Process cicle for this product 
g16_dmwf14_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//DMWF-C14//'        # Folder where the data is found
g16_dmwf14_fdk_identifier = '*DMWF*.nc'                                               # Unique string on the file name
g16_dmwf14_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_dmwf14_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_dmwf14_fdk_interval   = '00'                                                      # Processing interval
g16_dmwf14_fdk_config     = '_CLD'                                                    # Configuration string
g16_dmwf14_fdk_script     = showcast_dir + '//Scripts//process_g16_dmw_clouds_fdk.py' # Script to activate
g16_dmwf14_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dmwf14_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dmwf14_sec            = True # GOES-16 L2 DMWF-C14 - Derived Motion Winds Band 14 - USER SECTOR

g16_dmwf14_sec_process    = 1                                                         # Process cicle for this product 
g16_dmwf14_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//DMWF-C14//'        # Folder where the data is found
g16_dmwf14_sec_identifier = '*DMWF*.nc'                                               # Unique string on the file name
g16_dmwf14_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_dmwf14_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_dmwf14_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_dmwf14_sec_interval   = '00'                                                      # Processing interval
g16_dmwf14_sec_config     = '_CLS'                                                    # Configuration string
g16_dmwf14_sec_script     = showcast_dir + '//Scripts//process_g16_dmw_clouds_sec.py' # Script to activate
g16_dmwf14_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dmwf14_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dsifpr_fdk            = True # GOES-16 L2 DSIF - Derived Stability Index - FULL DISK

g16_dsifpr_fdk_process    = 1                                                         # Process cicle for this product 
g16_dsifpr_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//DSIF//'            # Folder where the data is found
g16_dsifpr_fdk_identifier = '*DSIF*.nc'                                               # Unique string on the file name
g16_dsifpr_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_dsifpr_fdk_resolution = 10  # Max Res.: 10 km                                     # Final plot resolution
g16_dsifpr_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dsifpr_fdk_config     = ''                                                        # Configuration string
g16_dsifpr_fdk_script     = showcast_dir + '//Scripts//process_g16_dsif_fdk.py'       # Script to activate
g16_dsifpr_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dsifpr_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dsifpr_sec            = True # GGOES-16 L2 DSIF - Derived Stability Index - USER SECTOR

g16_dsifpr_sec_process    = 1                                                         # Process cicle for this product 
g16_dsifpr_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//DSIF//'            # Folder where the data is found
g16_dsifpr_sec_identifier = '*DSIF*.nc'                                               # Unique string on the file name
g16_dsifpr_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_dsifpr_sec_extent     = [-105.0, -60.0, -15.0, 20.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_dsifpr_sec_resolution = 10  # Max Res.: 10 km                                     # Final plot resolution
g16_dsifpr_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_dsifpr_sec_config     = '_SEC'                                                    # Configuration string
g16_dsifpr_sec_script     = showcast_dir + '//Scripts//process_g16_dsif_sec.py'       # Script to activate
g16_dsifpr_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dsifpr_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dsradi_fdk            = True # GOES-16 L2 DSRF - Downward Shortwave Radiation - FULL DISK

g16_dsradi_fdk_process    = 1                                                         # Process cicle for this product 
g16_dsradi_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//DSRF//'            # Folder where the data is found
g16_dsradi_fdk_identifier = '*DSRF*.nc'                                               # Unique string on the file name
g16_dsradi_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_dsradi_fdk_resolution = 2  # Max Res.: 25 km (but you may select higher res plots)# Final plot resolution
g16_dsradi_fdk_interval   = '00'                                                      # Processing interval
g16_dsradi_fdk_config     = ''                                                        # Configuration string
g16_dsradi_fdk_script     = showcast_dir + '//Scripts//process_g16_rad_fdk.py'        # Script to activate
g16_dsradi_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dsradi_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_dsradi_sec            = True # GOES-16 L2 DSRF - Downward Shortwave Radiation - USER SECTOR

g16_dsradi_sec_process    = 1                                                         # Process cicle for this product 
g16_dsradi_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//DSRF//'            # Folder where the data is found
g16_dsradi_sec_identifier = '*DSRF*.nc'                                               # Unique string on the file name
g16_dsradi_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_dsradi_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_dsradi_sec_resolution = 2  # Max Res.: 25 km (but you may select higher res plots)# Final plot resolution
g16_dsradi_sec_interval   = '00'                                                      # Processing interval
g16_dsradi_sec_config     = '_SEC'                                                    # Configuration string
g16_dsradi_sec_script     = showcast_dir + '//Scripts//process_g16_rad_sec.py'        # Script to activate
g16_dsradi_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_dsradi_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_firmsk_fdk            = True # GOES-16 L2 FDCF - Fire-Hot Spot Characterization - FULL DISK

g16_firmsk_fdk_process    = 1                                                         # Process cicle for this product 
g16_firmsk_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//FDCF//'            # Folder where the data is found
g16_firmsk_fdk_identifier = '*FDCF*.nc'                                               # Unique string on the file name
g16_firmsk_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_firmsk_fdk_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_firmsk_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_firmsk_fdk_config     = ''                                                        # Configuration string
g16_firmsk_fdk_script     = showcast_dir + '//Scripts//process_g16_fdfc_fdk.py'       # Script to activate
g16_firmsk_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_firmsk_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_firmsk_sec            = True # GOES-16 L2 FDCF - Fire-Hot Spot Characterization - USER SECTOR

g16_firmsk_sec_process    = 1                                                         # Process cicle for this product 
g16_firmsk_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//FDCF//'            # Folder where the data is found
g16_firmsk_sec_identifier = '*FDCF*.nc'                                               # Unique string on the file name
g16_firmsk_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_firmsk_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_firmsk_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_firmsk_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_firmsk_sec_config     = '_SEC'                                                    # Configuration string
g16_firmsk_sec_script     = showcast_dir + '//Scripts//process_g16_fdfc_sec.py'       # Script to activate
g16_firmsk_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_firmsk_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_snowco_fdk            = True # GOES-16 L2 FSCF - Snow Cover - FULL DISK

g16_snowco_fdk_process    = 1                                                         # Process cicle for this product 
g16_snowco_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//FSCF//'            # Folder where the data is found
g16_snowco_fdk_identifier = '*FSCF*.nc'                                               # Unique string on the file name
g16_snowco_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_snowco_fdk_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_snowco_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_snowco_fdk_config     = ''                                                        # Configuration string
g16_snowco_fdk_script     = showcast_dir + '//Scripts//process_g16_baseline_fdk.py'   # Script to activate
g16_snowco_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_snowco_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_snowco_sec            = True # GOES-16 L2 FSCF - Snow Cover - USER SECTOR

g16_snowco_sec_process    = 1                                                         # Process cicle for this product 
g16_snowco_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//FSCF//'            # Folder where the data is found
g16_snowco_sec_identifier = '*FSCF*.nc'                                               # Unique string on the file name
g16_snowco_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_snowco_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_snowco_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_snowco_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_snowco_sec_config     = '_SEC'                                                    # Configuration string
g16_snowco_sec_script     = showcast_dir + '//Scripts//process_g16_baseline_sec.py'   # Script to activate
g16_snowco_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_snowco_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_lstskn_fdk            = True # GOES-16 L2 LSTF - Land Surface (Skin) Temperature - FULL DISK

g16_lstskn_fdk_process    = 1                                                         # Process cicle for this product 
g16_lstskn_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//LSTF//'            # Folder where the data is found
g16_lstskn_fdk_identifier = '*LST*.nc'                                                # Unique string on the file name
g16_lstskn_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_lstskn_fdk_resolution = 10  # Max Res.: 2 km                                      # Final plot resolution
g16_lstskn_fdk_interval   = '00'                                                      # Processing interval
g16_lstskn_fdk_config     = ''                                                        # Configuration string
g16_lstskn_fdk_script     = showcast_dir + '//Scripts//process_g16_baseline_fdk.py'   # Script to activate
g16_lstskn_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_lstskn_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_lstskn_sec            = True # GOES-16 L2 LSTF - Land Surface (Skin) Temperature - USER SECTOR

g16_lstskn_sec_process    = 1                                                         # Process cicle for this product 
g16_lstskn_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//LSTF//'            # Folder where the data is found
g16_lstskn_sec_identifier = '*LST*.nc'                                                # Unique string on the file name
g16_lstskn_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_lstskn_sec_extent     = [-105.0, -60.0, -15.0, 20.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_lstskn_sec_resolution = 10  # Max Res.: 2 km                                      # Final plot resolution
g16_lstskn_sec_interval   = '00'                                                      # Processing interval
g16_lstskn_sec_config     = '_SEC'                                                    # Configuration string
g16_lstskn_sec_script     = showcast_dir + '//Scripts//process_g16_baseline_sec.py'   # Script to activate
g16_lstskn_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_lstskn_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_rrqpef_fdk            = True # GOES-16 L2 RRQPEF - Rainfall Rate - Quanti Pred. Estimate - FULL DISK

g16_rrqpef_fdk_process    = 1                                                         # Process cicle for this product 
g16_rrqpef_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//RRQPEF//'          # Folder where the data is found
g16_rrqpef_fdk_identifier = '*RRQPEF*.nc'                                             # Unique string on the file name
g16_rrqpef_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_rrqpef_fdk_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_rrqpef_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_rrqpef_fdk_config     = ''                                                        # Configuration string
g16_rrqpef_fdk_script     = showcast_dir + '//Scripts//process_g16_baseline_fdk.py'   # Script to activate
g16_rrqpef_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_rrqpef_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_rrqpef_sec            = True # GOES-16 L2 RRQPEF - Rainfall Rate - Quanti Pred. Estimate - USER SECTOR

g16_rrqpef_sec_process    = 1                                                         # Process cicle for this product 
g16_rrqpef_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//RRQPEF//'          # Folder where the data is found
g16_rrqpef_sec_identifier = '*RRQPEF*.nc'                                             # Unique string on the file name
g16_rrqpef_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_rrqpef_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_rrqpef_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_rrqpef_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_rrqpef_sec_config     = '_SEC'                                                    # Configuration string
g16_rrqpef_sec_script     = showcast_dir + '//Scripts//process_g16_baseline_sec.py'   # Script to activate
g16_rrqpef_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_rrqpef_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_rsradi_fdk            = True # GOES-16 L2 RSRF - Reflected Shortwave Radiation - FULL DISK

g16_rsradi_fdk_process    = 1                                                         # Process cicle for this product 
g16_rsradi_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//RSRF//'            # Folder where the data is found
g16_rsradi_fdk_identifier = '*RSRF*.nc'                                               # Unique string on the file name
g16_rsradi_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_rsradi_fdk_resolution = 2 # Max Res.: 25 km (but you may select higher res plots) # Final plot resolution
g16_rsradi_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_rsradi_fdk_config     = ''                                                        # Configuration string
g16_rsradi_fdk_script     = showcast_dir + '//Scripts//process_g16_rad_fdk.py'        # Script to activate
g16_rsradi_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_rsradi_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_rsradi_sec            = True # GOES-16 L2 RSRF - Reflected Shortwave Radiation - USER SECTOR

g16_rsradi_sec_process    = 1                                                         # Process cicle for this product 
g16_rsradi_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//RSRF//'            # Folder where the data is found
g16_rsradi_sec_identifier = '*RSRF*.nc'                                               # Unique string on the file name
g16_rsradi_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_rsradi_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_rsradi_sec_resolution = 2 # Max Res.: 25 km (but you may select higher res plots) # Final plot resolution
g16_rsradi_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_rsradi_sec_config     = '_SEC'                                                    # Configuration string
g16_rsradi_sec_script     = showcast_dir + '//Scripts//process_g16_rad_sec.py'        # Script to activate
g16_rsradi_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_rsradi_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_sstskn_fdk            = True # GOES-16 L2 SSTF - Sea Surface (Skin) Temperature - FULL DISK

g16_sstskn_fdk_process    = 1                                                         # Process cicle for this product 
g16_sstskn_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//SSTF//'            # Folder where the data is found
g16_sstskn_fdk_identifier = '*SSTF*.nc'                                               # Unique string on the file name
g16_sstskn_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_sstskn_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_sstskn_fdk_interval   = '00'                                                      # Processing interval
g16_sstskn_fdk_config     = ''                                                        # Configuration string
g16_sstskn_fdk_script     = showcast_dir + '//Scripts//process_g16_baseline_fdk.py'   # Script to activate
g16_sstskn_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_sstskn_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_sstskn_sec            = True # GOES-16 L2 SSTF - Sea Surface (Skin) Temperature - USER SECTOR

g16_sstskn_sec_process    = 1                                                         # Process cicle for this product 
g16_sstskn_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//SSTF//'            # Folder where the data is found
g16_sstskn_sec_identifier = '*SSTF*.nc'                                               # Unique string on the file name
g16_sstskn_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_sstskn_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_sstskn_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_sstskn_sec_interval   = '00'                                                      # Processing interval
g16_sstskn_sec_config     = '_SEC'                                                    # Configuration string
g16_sstskn_sec_script     = showcast_dir + '//Scripts//process_g16_baseline_sec.py'   # Script to activate
g16_sstskn_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_sstskn_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_totpwa_fdk            = True # GOES-16 L2 TPWF - Total Precipitable Water - FULL DISK

g16_totpwa_fdk_process    = 1                                                         # Process cicle for this product 
g16_totpwa_fdk_directory  = ingest_dir + 'GOES-R-Level-2-Products//TPWF//'            # Folder where the data is found
g16_totpwa_fdk_identifier = '*TPWF*.nc'                                               # Unique string on the file name
g16_totpwa_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_totpwa_fdk_resolution = 10  # Max Res.: 10 km                                     # Final plot resolution
g16_totpwa_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_totpwa_fdk_config     = ''                                                        # Configuration string
g16_totpwa_fdk_script     = showcast_dir + '//Scripts//process_g16_baseline_fdk.py'   # Script to activate
g16_totpwa_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_totpwa_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_totpwa_sec            = True # GOES-16 L2 TPWF - Total Precipitable Water - USER SECTOR

g16_totpwa_sec_process    = 1                                                         # Process cicle for this product 
g16_totpwa_sec_directory  = ingest_dir + 'GOES-R-Level-2-Products//TPWF//'            # Folder where the data is found
g16_totpwa_sec_identifier = '*TPWF*.nc'                                               # Unique string on the file name
g16_totpwa_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_totpwa_sec_extent     = [-105.0, -60.0, -15.0, 20.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_totpwa_sec_resolution = 10  # Max Res.: 10 km                                     # Final plot resolution
g16_totpwa_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_totpwa_sec_config     = '_SEC'                                                    # Configuration string
g16_totpwa_sec_script     = showcast_dir + '//Scripts//process_g16_baseline_sec.py'   # Script to activate
g16_totpwa_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_totpwa_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GOES-16 - BANDS COMPOSITES / MULTISPECTRAL IMAGERY 
#######################################################################################################

#------------------------------------------------------------------------------------------------------
g16_fcolor_fdk            = True # GOES-16 False Color - Band 02 and Band 13 - FULL DISK

g16_fcolor_fdk_process    = 1                                                         # Process cicle for this product 
g16_fcolor_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band02//'               # Folder where the data is found
g16_fcolor_fdk_identifier = '*L2-CMIPF-M*C02_G16*.nc'                                 # Unique string on the file name
g16_fcolor_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_fcolor_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_fcolor_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_fcolor_fdk_config     = '_FCO'                                                    # Configuration string
g16_fcolor_fdk_script     = showcast_dir + '//Scripts//process_g1X_false_color_fdk.py'# Script to activate
g16_fcolor_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_fcolor_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_fcolor_sec            = True # GOES-16 False Color - Band 02 and Band 13 - USER SECTOR

g16_fcolor_sec_process    = 1                                                         # Process cicle for this product 
g16_fcolor_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band02//'               # Folder where the data is found
g16_fcolor_sec_identifier = '*L2-CMIPF-M*C02_G16*.nc'                                 # Unique string on the file name
g16_fcolor_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_fcolor_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_fcolor_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_fcolor_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_fcolor_sec_config     = '_FCS'                                                    # Configuration string
g16_fcolor_sec_script     = showcast_dir + '//Scripts//process_g1X_false_color_sec.py'# Script to activate
g16_fcolor_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_fcolor_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_ircl13_fdk            = True # GOES-16 IR Clouds - Band 13 with Blue Marble - FULL DISK

g16_ircl13_fdk_process    = 1                                                         # Process cicle for this product 
g16_ircl13_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band13//'               # Folder where the data is found
g16_ircl13_fdk_identifier = '*L2-CMIPF-M*C13_G16*.nc'                                 # Unique string on the file name
g16_ircl13_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_ircl13_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_ircl13_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_ircl13_fdk_config     = '_IRC'                                                    # Configuration string
g16_ircl13_fdk_script     = showcast_dir + '//Scripts//process_g1X_ir_clouds_fdk.py'  # Script to activate
g16_ircl13_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_ircl13_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_ircl13_sec            = True # GOES-16 IR Clouds - Band 13 with Blue Marble - USER SECTOR

g16_ircl13_sec_process    = 1                                                         # Process cicle for this product 
g16_ircl13_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band13//'               # Folder where the data is found
g16_ircl13_sec_identifier = '*L2-CMIPF-M*C13_G16*.nc'                                 # Unique string on the file name
g16_ircl13_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_ircl13_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_ircl13_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_ircl13_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_ircl13_sec_config     = '_IRS'                                                    # Configuration string
g16_ircl13_sec_script     = showcast_dir + '//Scripts//process_g1X_ir_clouds_sec.py'  # Script to activate
g16_ircl13_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_ircl13_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_irce13_fdk            = True # GOES-16 IR Clouds Enhanced - Band 13 [enhanced] with Blue Marble - FULL DISK

g16_irce13_fdk_process    = 1                                                                # Process cicle for this product 
g16_irce13_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band13//'                      # Folder where the data is found
g16_irce13_fdk_identifier = '*L2-CMIPF-M*C13_G16*.nc'                                        # Unique string on the file name
g16_irce13_fdk_max_files  = 1                                                                # Max number of historical files to be processed
g16_irce13_fdk_resolution = 8  # Max Res.: 2 km                                              # Final plot resolution
g16_irce13_fdk_interval   = '00,10,20,30,40,50'                                              # Processing interval
g16_irce13_fdk_config     = '_IRE'                                                           # Configuration string
g16_irce13_fdk_script     = showcast_dir + '//Scripts//process_g1X_ir_clouds_enhance_fdk.py' # Script to activate
g16_irce13_fdk_output     = showcast_dir + '//Output//'                                      # Output folder

products.append('g16_irce13_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_irce13_sec            = True # GOES-16 IR Clouds Enhanced - Band 13 [enhanced] with Blue Marble - USER SECTOR

g16_irce13_sec_process    = 1                                                                # Process cicle for this product 
g16_irce13_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band13//'                      # Folder where the data is found
g16_irce13_sec_identifier = '*L2-CMIPF-M*C13_G16*.nc'                                        # Unique string on the file name
g16_irce13_sec_max_files  = 1                                                                # Max number of historical files to be processed
g16_irce13_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                                     # [min_lon, min_lat, max_lon, max_lat]
g16_irce13_sec_resolution = 2  # Max Res.: 2 km                                              # Final plot resolution
g16_irce13_sec_interval   = '00,10,20,30,40,50'                                              # Processing interval
g16_irce13_sec_config     = '_IES'                                                           # Configuration string
g16_irce13_sec_script     = showcast_dir + '//Scripts//process_g1X_ir_clouds_enhance_sec.py' # Script to activate
g16_irce13_sec_output     = showcast_dir + '//Output//'                                      # Output folder

products.append('g16_irce13_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_swdiff_fdk            = True # GOES-16 Split Window Difference - FULL DISK

g16_swdiff_fdk_process    = 1                                                         # Process cicle for this product 
g16_swdiff_fdk_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band13//'               # Folder where the data is found
g16_swdiff_fdk_identifier = '*L2-CMIPF-M*C13_G16*.nc'                                 # Unique string on the file name
g16_swdiff_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_swdiff_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_swdiff_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_swdiff_fdk_config     = '_SWD'                                                    # Configuration string
g16_swdiff_fdk_script     = showcast_dir + '//Scripts//process_g1X_swd_fdk.py'        # Script to activate
g16_swdiff_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_swdiff_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_swdiff_sec            = True # GOES-16 Split Window Difference - USER SECTOR

g16_swdiff_sec_process    = 1                                                         # Process cicle for this product 
g16_swdiff_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band13//'               # Folder where the data is found
g16_swdiff_sec_identifier = '*L2-CMIPF-M*C13_G16*.nc'                                 # Unique string on the file name
g16_swdiff_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_swdiff_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_swdiff_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_swdiff_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g16_swdiff_sec_config     = '_SWS'                                                    # Configuration string
g16_swdiff_sec_script     = showcast_dir + '//Scripts//process_g1X_swd_sec.py'        # Script to activate
g16_swdiff_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_swdiff_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_salpro_sec            = True # GOES-16 Saharan Air Layer Tracking Product - USER SECTOR

g16_salpro_sec_process    = 1                                                         # Process cicle for this product 
g16_salpro_sec_directory  = ingest_dir + 'GOES-R-CMI-Imagery//Band13//'               # Folder where the data is found
g16_salpro_sec_identifier = '*L2-CMIPF-M*C13_G16*.nc'                                 # Unique string on the file name
g16_salpro_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_salpro_sec_extent     = [-100.0, 0.0, -13.0, 40.0]                                # [min_lon, min_lat, max_lon, max_lat]
g16_salpro_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_salpro_sec_interval   = '00'                                                      # Processing interval
g16_salpro_sec_config     = '_SAS'                                                    # Configuration string
g16_salpro_sec_script     = showcast_dir + '//Scripts//process_g1X_sal_sec.py'        # Script to activate
g16_salpro_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_salpro_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GOES-16 GLM (GEOSTATIONARY LIGHTNING MAPPER) - SUGGESTION: PUT IN A DEDICATED PROCESS
#######################################################################################################

#------------------------------------------------------------------------------------------------------
g16_glm20s_fdk            = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (20s) - FULL DISK

g16_glm20s_fdk_process    = 1                                                         # Process cicle for this product 
g16_glm20s_fdk_directory  = ingest_dir + 'GOES-R-GLM-Products//'                      # Folder where the data is found
g16_glm20s_fdk_identifier = 'OR_GLM*.nc'                                              # Unique string on the file name
g16_glm20s_fdk_max_files  = 10                                                        # Max number of historical files to be processed
g16_glm20s_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_glm20s_fdk_interval   = ''                                                        # Processing interval
g16_glm20s_fdk_config     = ''                                                        # Configuration string
g16_glm20s_fdk_script     = showcast_dir + '//Scripts//process_g16_glm_20s_fdk.py'    # Script to activate
g16_glm20s_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_glm20s_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_glm20s_sec            = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (20s) - USER SECTOR

g16_glm20s_sec_process    = 1                                                         # Process cicle for this product 
g16_glm20s_sec_directory  = ingest_dir + 'GOES-R-GLM-Products//'                      # Folder where the data is found
g16_glm20s_sec_identifier = 'OR_GLM*.nc'                                              # Unique string on the file name
g16_glm20s_sec_max_files  = 10                                                        # Max number of historical files to be processed
g16_glm20s_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_glm20s_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_glm20s_sec_interval   = ''                                                        # Processing interval
g16_glm20s_sec_config     = '_SEC'                                                    # Configuration string
g16_glm20s_sec_script     = showcast_dir + '//Scripts//process_g16_glm_20s_sec.py'    # Script to activate
g16_glm20s_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_glm20s_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_glir20_fdk            = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (20s) + GOES-16 Band 13 - FULL DISK

g16_glir20_fdk_process    = 1                                                         # Process cicle for this product 
g16_glir20_fdk_directory  = ingest_dir + 'GOES-R-GLM-Products//'                      # Folder where the data is found
g16_glir20_fdk_identifier = 'OR_GLM*.nc'                                              # Unique string on the file name
g16_glir20_fdk_max_files  = 10                                                        # Max number of historical files to be processed
g16_glir20_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_glir20_fdk_interval   = ''                                                        # Processing interval
g16_glir20_fdk_config     = '_IRF'                                                    # Configuration string
g16_glir20_fdk_script     = showcast_dir + '//Scripts//process_g16_glm_ir_20s_fdk.py' # Script to activate
g16_glir20_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_glir20_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_glir20_sec            = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (20s) + GOES-16 Band 13 - USER SECTOR

g16_glir20_sec_process    = 1                                                         # Process cicle for this product 
g16_glir20_sec_directory  = ingest_dir + 'GOES-R-GLM-Products//'                      # Folder where the data is found
g16_glir20_sec_identifier = 'OR_GLM*.nc'                                              # Unique string on the file name
g16_glir20_sec_max_files  = 10                                                        # Max number of historical files to be processed
g16_glir20_sec_extent     = [-58.0, -30.0, -43.0, -15.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_glir20_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_glir20_sec_interval   = ''                                                        # Processing interval
g16_glir20_sec_config     = '_IRS'                                                    # Configuration string
g16_glir20_sec_script     = showcast_dir + '//Scripts//process_g16_glm_ir_20s_sec.py' # Script to activate
g16_glir20_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_glir20_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_glmtra_fdk            = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (Tracking) + GOES-16 Band 13 - FULL DISK

g16_glmtra_fdk_process    = 1                                                         # Process cicle for this product 
g16_glmtra_fdk_directory  = ingest_dir + 'GOES-R-GLM-Products//'                      # Folder where the data is found
g16_glmtra_fdk_identifier = 'OR_GLM*.nc'                                              # Unique string on the file name
g16_glmtra_fdk_max_files  = 30                                                        # Max number of historical files to be processed
g16_glmtra_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_glmtra_fdk_interval   = ''                                                        # Processing interval
g16_glmtra_fdk_config     = '_TRA'                                                    # Configuration string
g16_glmtra_fdk_script     = showcast_dir + '//Scripts//process_g16_glm_tra_fdk.py'    # Script to activate
g16_glmtra_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_glmtra_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_glmtra_sec            = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (Tracking) + GOES-16 Band 13 - USER SECTOR

g16_glmtra_sec_process    = 1                                                         # Process cicle for this product 
g16_glmtra_sec_directory  = ingest_dir + 'GOES-R-GLM-Products//'                      # Folder where the data is found
g16_glmtra_sec_identifier = 'OR_GLM*.nc'                                              # Unique string on the file name
g16_glmtra_sec_max_files  = 30                                                        # Max number of historical files to be processed
g16_glmtra_sec_extent     = [-58.0, -30.0, -43.0, -15.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_glmtra_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_glmtra_sec_interval   = ''                                                        # Processing interval
g16_glmtra_sec_config     = '_TRS'                                                    # Configuration string
g16_glmtra_sec_script     = showcast_dir + '//Scripts//process_g16_glm_tra_sec.py'    # Script to activate
g16_glmtra_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_glmtra_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_glmden_fdk            = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (Density) + GOES-16 Band 13 - FULL DISK

g16_glmden_fdk_process    = 1                                                         # Process cicle for this product 
g16_glmden_fdk_directory  = ingest_dir + 'GOES-R-GLM-Products//'                      # Folder where the data is found
g16_glmden_fdk_identifier = 'OR_GLM*.nc'                                              # Unique string on the file name
g16_glmden_fdk_max_files  = 60                                                        # Max number of historical files to be processed
g16_glmden_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_glmden_fdk_interval   = ''                                                        # Processing interval
g16_glmden_fdk_config     = '_DEN'                                                    # Configuration string
g16_glmden_fdk_script     = showcast_dir + '//Scripts//process_g16_glm_den_fdk.py'    # Script to activate
g16_glmden_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_glmden_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_glmden_sec            = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (Density) + GOES-16 Band 13 - USER SECTOR

g16_glmden_sec_process    = 1                                                         # Process cicle for this product 
g16_glmden_sec_directory  = ingest_dir + 'GOES-R-GLM-Products//'                      # Folder where the data is found
g16_glmden_sec_identifier = 'OR_GLM*.nc'                                              # Unique string on the file name
g16_glmden_sec_max_files  = 60                                                        # Max number of historical files to be processed
g16_glmden_sec_extent     = [-55.0, -25.0, -40.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_glmden_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_glmden_sec_interval   = ''                                                        # Processing interval
g16_glmden_sec_config     = '_DES'                                                    # Configuration string
g16_glmden_sec_script     = showcast_dir + '//Scripts//process_g16_glm_den_sec.py'    # Script to activate
g16_glmden_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_glmden_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_glmhea_fdk            = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (Heatmap) + GOES-16 Band 13 - FULL DISK

g16_glmhea_fdk_process    = 1                                                         # Process cicle for this product 
g16_glmhea_fdk_directory  = ingest_dir + 'GOES-R-GLM-Products//'                      # Folder where the data is found
g16_glmhea_fdk_identifier = 'OR_GLM*.nc'                                              # Unique string on the file name
g16_glmhea_fdk_max_files  = 60                                                        # Max number of historical files to be processed
g16_glmhea_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g16_glmhea_fdk_interval   = ''                                                        # Processing interval
g16_glmhea_fdk_config     = '_HEA'                                                    # Configuration string
g16_glmhea_fdk_script     = showcast_dir + '//Scripts//process_g16_glm_hea_fdk.py'    # Script to activate
g16_glmhea_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_glmhea_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_glmhea_sec            = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (Heatmap) + GOES-16 Band 13 - USER SECTOR

g16_glmhea_sec_process    = 1                                                         # Process cicle for this product 
g16_glmhea_sec_directory  = ingest_dir + 'GOES-R-GLM-Products//'                      # Folder where the data is found
g16_glmhea_sec_identifier = 'OR_GLM*.nc'                                              # Unique string on the file name
g16_glmhea_sec_max_files  = 60                                                        # Max number of historical files to be processed
g16_glmhea_sec_extent     = [-55.0, -25.0, -40.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_glmhea_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_glmhea_sec_interval   = ''                                                        # Processing interval
g16_glmhea_sec_config     = '_HES'                                                    # Configuration string
g16_glmhea_sec_script     = showcast_dir + '//Scripts//process_g16_glm_hea_sec.py'    # Script to activate
g16_glmhea_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_glmhea_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_glmirc_fdk            = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (5 min density) - FULL DISK

g16_glmirc_fdk_process    = 1                                                         # Process cicle for this product 
g16_glmirc_fdk_directory  = ingest_dir + 'GOES-R-GLM-Products//'                      # Folder where the data is found
g16_glmirc_fdk_identifier = 'GLM_*.nc'                                                # Unique string on the file name
g16_glmirc_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g16_glmirc_fdk_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_glmirc_fdk_interval   = ''                                                        # Processing interval
g16_glmirc_fdk_config     = ''                                                        # Configuration string
g16_glmirc_fdk_script     = showcast_dir + '//Scripts//process_g16_glm_clouds_fdk.py' # Script to activate
g16_glmirc_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_glmirc_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g16_glmirc_sec            = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (5 min density) - USER SECTOR

g16_glmirc_sec_process    = 1                                                         # Process cicle for this product 
g16_glmirc_sec_directory  = ingest_dir + 'GOES-R-GLM-Products//'                      # Folder where the data is found
g16_glmirc_sec_identifier = 'GLM_*.nc'                                                # Unique string on the file name
g16_glmirc_sec_max_files  = 1                                                         # Max number of historical files to be processed
g16_glmirc_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g16_glmirc_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g16_glmirc_sec_interval   = ''                                                        # Processing interval
g16_glmirc_sec_config     = '_SEC'                                                    # Configuration string
g16_glmirc_sec_script     = showcast_dir + '//Scripts//process_g16_glm_clouds_sec.py' # Script to activate
g16_glmirc_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g16_glmirc_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GOES-16 and GOES-17 Mosaic
#######################################################################################################

#------------------------------------------------------------------------------------------------------
g1X_b13mos_sec            = True # GOES-16 L2 GLM - Geostationary Lightning Mapper (5 min density) - USER SECTOR

g1X_b13mos_sec_process    = 1                                                         # Process cicle for this product 
g1X_b13mos_sec_directory  = ingest_dir + 'GOES-S-CMI-Imagery//Band13//'               # Folder where the data is found
g1X_b13mos_sec_identifier = '*L2-CMIPF-M*C13_G17*.nc'                                 # Unique string on the file name
g1X_b13mos_sec_max_files  = 1                                                         # Max number of historical files to be processed
g1X_b13mos_sec_extent     = [-120.0, 0.0, -75.0, 45.0]                                # [min_lon, min_lat, max_lon, max_lat]
g1X_b13mos_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g1X_b13mos_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g1X_b13mos_sec_config     = '_MOS'                                                    # Configuration string
g1X_b13mos_sec_script     = showcast_dir + '//Scripts//process_g1X_b13_mosaic_sec.py' # Script to activate
g1X_b13mos_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g1X_b13mos_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GOES-17 - ABI INDIVIDUAL BANDS
#######################################################################################################

#------------------------------------------------------------------------------------------------------
g17_band02_fdk            = True # GOES-17 L2 CMI - Band 02 - FULL DISK 

g17_band02_fdk_process    = 1                                                         # Process cicle for this product 
g17_band02_fdk_directory  = ingest_dir + 'GOES-S-CMI-Imagery//Band02//'               # Folder where the data is found
g17_band02_fdk_identifier = '*L2-CMIPF-M*C02_G17*.nc'                                 # Unique string on the file name
g17_band02_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g17_band02_fdk_resolution = 8                                                         # Final plot resolution
g17_band02_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g17_band02_fdk_config     = ''                                                        # Configuration string
g17_band02_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g17_band02_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g17_band02_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g17_band02_sec            = True # GOES-17 L2 CMI - Band 02 - USER SECTOR 

g17_band02_sec_process    = 1                                                         # Process cicle for this product 
g17_band02_sec_directory  = ingest_dir + 'GOES-S-CMI-Imagery//Band02//'               # Folder where the data is found
g17_band02_sec_identifier = '*L2-CMIPF-M*C02_G17*.nc'                                 # Unique string on the file name
g17_band02_sec_max_files  = 1                                                         # Max number of historical files to be processed
g17_band02_sec_extent     = [-120.0, 0.0, -75.0, 45.0]                                # [min_lon, min_lat, max_lon, max_lat]
g17_band02_sec_resolution = 1                                                         # Final plot resolution
g17_band02_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g17_band02_sec_config     = '_SEC'                                                    # Configuration string
g17_band02_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g17_band02_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g17_band02_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g17_band09_fdk            = True # GOES-17 L2 CMI - Band 09 - FULL DISK 

g17_band09_fdk_process    = 1                                                         # Process cicle for this product 
g17_band09_fdk_directory  = ingest_dir + 'GOES-S-CMI-Imagery//Band09//'               # Folder where the data is found
g17_band09_fdk_identifier = '*L2-CMIPF-M*C09_G17*.nc'                                 # Unique string on the file name
g17_band09_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g17_band09_fdk_resolution = 8                                                         # Final plot resolution
g17_band09_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g17_band09_fdk_config     = ''                                                        # Configuration string
g17_band09_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g17_band09_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g17_band09_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g17_band09_sec            = True # GOES-17 L2 CMI - Band 09 - USER SECTOR 

g17_band09_sec_process    = 1                                                         # Process cicle for this product 
g17_band09_sec_directory  = ingest_dir + 'GOES-S-CMI-Imagery//Band09//'               # Folder where the data is found
g17_band09_sec_identifier = '*L2-CMIPF-M*C09_G17*.nc'                                 # Unique string on the file name
g17_band09_sec_max_files  = 1                                                         # Max number of historical files to be processed
g17_band09_sec_extent     = [-120.0, 0.0, -75.0, 45.0]                                # [min_lon, min_lat, max_lon, max_lat]
g17_band09_sec_resolution = 1                                                         # Final plot resolution
g17_band09_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g17_band09_sec_config     = '_SEC'                                                    # Configuration string
g17_band09_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g17_band09_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g17_band09_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g17_band13_fdk            = True # GOES-17 L2 CMI - Band 13 - FULL DISK 

g17_band13_fdk_process    = 1                                                         # Process cicle for this product 
g17_band13_fdk_directory  = ingest_dir + 'GOES-S-CMI-Imagery//Band13//'               # Folder where the data is found
g17_band13_fdk_identifier = '*L2-CMIPF-M*C13_G17*.nc'                                 # Unique string on the file name
g17_band13_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g17_band13_fdk_resolution = 8                                                         # Final plot resolution
g17_band13_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g17_band13_fdk_config     = ''                                                        # Configuration string
g17_band13_fdk_script     = showcast_dir + '//Scripts//process_g1X_bands_fdk.py'      # Script to activate
g17_band13_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g17_band13_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g17_band13_sec            = True # GOES-17 L2 CMI - Band 13 - USER SECTOR 

g17_band13_sec_process    = 1                                                         # Process cicle for this product 
g17_band13_sec_directory  = ingest_dir + 'GOES-S-CMI-Imagery//Band13//'               # Folder where the data is found
g17_band13_sec_identifier = '*L2-CMIPF-M*C13_G17*.nc'                                 # Unique string on the file name
g17_band13_sec_max_files  = 1                                                         # Max number of historical files to be processed
g17_band13_sec_extent     = [-120.0, 0.0, -75.0, 45.0]                                # [min_lon, min_lat, max_lon, max_lat]
g17_band13_sec_resolution = 1                                                         # Final plot resolution
g17_band13_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g17_band13_sec_config     = '_SEC'                                                    # Configuration string
g17_band13_sec_script     = showcast_dir + '//Scripts//process_g1X_bands_sec.py'      # Script to activate
g17_band13_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g17_band13_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GOES-17 - BANDS COMPOSITES / MULTISPECTRAL IMAGERY
#######################################################################################################

#------------------------------------------------------------------------------------------------------
g17_fcolor_fdk            = True # GOES-17 False Color - Band 02 and Band 13 - FULL DISK

g17_fcolor_fdk_process    = 1                                                         # Process cicle for this product 
g17_fcolor_fdk_directory  = ingest_dir + 'GOES-S-CMI-Imagery//Band02//'               # Folder where the data is found
g17_fcolor_fdk_identifier = '*L2-CMIPF-M*C02_G17*.nc'                                 # Unique string on the file name
g17_fcolor_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g17_fcolor_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g17_fcolor_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g17_fcolor_fdk_config     = '_FCO'                                                    # Configuration string
g17_fcolor_fdk_script     = showcast_dir + '//Scripts//process_g1X_false_color_fdk.py'# Script to activate
g17_fcolor_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g17_fcolor_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g17_fcolor_sec            = True # GOES-17 False Color - Band 02 and Band 13 - USER SECTOR

g17_fcolor_sec_process    = 1                                                         # Process cicle for this product 
g17_fcolor_sec_directory  = ingest_dir + 'GOES-S-CMI-Imagery//Band02//'               # Folder where the data is found
g17_fcolor_sec_identifier = '*L2-CMIPF-M*C02_G17*.nc'                                 # Unique string on the file name
g17_fcolor_sec_max_files  = 1                                                         # Max number of historical files to be processed
g17_fcolor_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g17_fcolor_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g17_fcolor_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g17_fcolor_sec_config     = '_FCS'                                                    # Configuration string
g17_fcolor_sec_script     = showcast_dir + '//Scripts//process_g1X_false_color_sec.py'# Script to activate
g17_fcolor_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g17_fcolor_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g17_ircl13_fdk            = True # GOES-17 IR Clouds - Band 13 with Blue Marble - FULL DISK

g17_ircl13_fdk_process    = 1                                                         # Process cicle for this product 
g17_ircl13_fdk_directory  = ingest_dir + 'GOES-S-CMI-Imagery//Band13//'               # Folder where the data is found
g17_ircl13_fdk_identifier = '*L2-CMIPF-M*C13_G17*.nc'                                 # Unique string on the file name
g17_ircl13_fdk_max_files  = 1                                                         # Max number of historical files to be processed
g17_ircl13_fdk_resolution = 8  # Max Res.: 2 km                                       # Final plot resolution
g17_ircl13_fdk_interval   = '00,10,20,30,40,50'                                       # Processing interval
g17_ircl13_fdk_config     = '_IRC'                                                    # Configuration string
g17_ircl13_fdk_script     = showcast_dir + '//Scripts//process_g1X_ir_clouds_fdk.py'  # Script to activate
g17_ircl13_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g17_ircl13_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g17_ircl13_sec            = True # GOES-17 IR Clouds - Band 13 with Blue Marble - USER SECTOR

g17_ircl13_sec_process    = 1                                                         # Process cicle for this product 
g17_ircl13_sec_directory  = ingest_dir + 'GOES-S-CMI-Imagery//Band13//'               # Folder where the data is found
g17_ircl13_sec_identifier = '*L2-CMIPF-M*C13_G17*.nc'                                 # Unique string on the file name
g17_ircl13_sec_max_files  = 1                                                         # Max number of historical files to be processed
g17_ircl13_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
g17_ircl13_sec_resolution = 2  # Max Res.: 2 km                                       # Final plot resolution
g17_ircl13_sec_interval   = '00,10,20,30,40,50'                                       # Processing interval
g17_ircl13_sec_config     = '_IRS'                                                    # Configuration string
g17_ircl13_sec_script     = showcast_dir + '//Scripts//process_g1X_ir_clouds_sec.py'  # Script to activate
g17_ircl13_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('g17_ircl13_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g17_irce13_fdk            = True # GOES-17 IR Clouds Enhanced - Band 13 [enhanced] with Blue Marble - FULL DISK

g17_irce13_fdk_process    = 1                                                                # Process cicle for this product 
g17_irce13_fdk_directory  = ingest_dir + 'GOES-S-CMI-Imagery//Band13//'                      # Folder where the data is found
g17_irce13_fdk_identifier = '*L2-CMIPF-M*C13_G17*.nc'                                        # Unique string on the file name
g17_irce13_fdk_max_files  = 1                                                                # Max number of historical files to be processed
g17_irce13_fdk_resolution = 8  # Max Res.: 2 km                                              # Final plot resolution
g17_irce13_fdk_interval   = '00,10,20,30,40,50'                                              # Processing interval
g17_irce13_fdk_config     = '_IRE'                                                           # Configuration string
g17_irce13_fdk_script     = showcast_dir + '//Scripts//process_g1X_ir_clouds_enhance_fdk.py' # Script to activate
g17_irce13_fdk_output     = showcast_dir + '//Output//'                                      # Output folder

products.append('g17_irce13_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
g17_irce13_sec            = True # GOES-17 IR Clouds Enhanced - Band 13 [enhanced] with Blue Marble - USER SECTOR

g17_irce13_sec_process    = 1                                                                # Process cicle for this product 
g17_irce13_sec_directory  = ingest_dir + 'GOES-S-CMI-Imagery//Band13//'                      # Folder where the data is found
g17_irce13_sec_identifier = '*L2-CMIPF-M*C13_G17*.nc'                                        # Unique string on the file name
g17_irce13_sec_max_files  = 1                                                                # Max number of historical files to be processed
g17_irce13_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                                     # [min_lon, min_lat, max_lon, max_lat]
g17_irce13_sec_resolution = 2  # Max Res.: 2 km                                              # Final plot resolution
g17_irce13_sec_interval   = '00,10,20,30,40,50'                                              # Processing interval
g17_irce13_sec_config     = '_IES'                                                           # Configuration string
g17_irce13_sec_script     = showcast_dir + '//Scripts//process_g1X_ir_clouds_enhance_sec.py' # Script to activate
g17_irce13_sec_output     = showcast_dir + '//Output//'                                      # Output folder

products.append('g17_irce13_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# METEOSAT PRODUCTS (YOU MAY SELECT WHICH MSG SUBPRODUCT YOU WANT TO PROCESS INSIDE THE PYTHON SCRIPT!)
#######################################################################################################

#------------------------------------------------------------------------------------------------------
msg_produc_fdk            = True # METEOSAT - 0 Degree (IMAGERY AND RGB'S) - FULL DISK

msg_produc_fdk_process    = 1                                                         # Process cicle for this product 
msg_produc_fdk_directory  = ingest_dir + 'MSG-0degree//IMG-3h//'                      # Folder where the data is found
msg_produc_fdk_identifier = '*-EPI______-*'                                           # Unique string on the file name
msg_produc_fdk_max_files  = 1                                                         # Max number of historical files to be processed
msg_produc_fdk_resolution = 8  # Max Res.: 3 km                                       # Final plot resolution
msg_produc_fdk_interval   = ''                                                        # Processing interval
msg_produc_fdk_config     = ''                                                        # Configuration string
msg_produc_fdk_script     = showcast_dir + '//Scripts//process_msg_bands_rgb_fdk.py'  # Script to activate
msg_produc_fdk_output     = showcast_dir + '//Output//'                               # Output folder

products.append('msg_produc_fdk') # Add the product to the list
#------------------------------------------------------------------------------------------------------
msg_produc_sec            = True # METEOSAT - 0 Degree (IMAGERY AND RGB'S) - USER SECTOR

msg_produc_sec_process    = 1                                                         # Process cicle for this product 
msg_produc_sec_directory  = ingest_dir + 'MSG-0degree//IMG-3h//'                      # Folder where the data is found
msg_produc_sec_identifier = '*-EPI______-*'                                           # Unique string on the file name
msg_produc_sec_max_files  = 1                                                         # Max number of historical files to be processed
msg_produc_sec_extent     = [-63.0, -35.0, -35.0, -10.0]                              # [min_lon, min_lat, max_lon, max_lat]
msg_produc_sec_resolution = 3  # Max Res.: 3 km                                       # Final plot resolution
msg_produc_sec_interval   = ''                                                        # Processing interval
msg_produc_sec_config     = '_SEC'                                                    # Configuration string
msg_produc_sec_script     = showcast_dir + '//Scripts//process_msg_bands_rgb_sec.py'  # Script to activate
msg_produc_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('msg_produc_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GCOM-W1 IMAGERY AND PRODUCTS
#######################################################################################################

#------------------------------------------------------------------------------------------------------
gcm_imager_sec            = True # GCOM-W1 - IMAGERY

gcm_imager_sec_process    = 1                                                           # Process cicle for this product 
gcm_imager_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//G-IMAGERY//'                  # Folder where the data is found
gcm_imager_sec_identifier = 'AMSR2-MBT*'                                                # Unique string on the file name
gcm_imager_sec_max_files  = 3                                                           # Max number of historical files to be processed
gcm_imager_sec_extent     = [-156.0, -60.0, 6.00, 60.0]                                 # [min_lon, min_lat, max_lon, max_lat]
gcm_imager_sec_resolution = 10  # Max Res.: 10 km                                       # Final plot resolution
gcm_imager_sec_interval   = ''                                                          # Processing interval
gcm_imager_sec_config     = ''                                                          # Configuration string
gcm_imager_sec_script     = showcast_dir + '//Scripts//process_gcm_imagery_products.py' # Script to activate
gcm_imager_sec_output     = showcast_dir + '//Output//'                                 # Output folder

products.append('gcm_imager_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gcm_soilmo_sec            = True # GCOM-W1 - SOIL MOISTURE and LAND COVER

gcm_soilmo_sec_process    = 1                                                           # Process cicle for this product 
gcm_soilmo_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//G-SOILMOISTURE//'             # Folder where the data is found
gcm_soilmo_sec_identifier = 'AMSR2-SOIL*'                                               # Unique string on the file name
gcm_soilmo_sec_max_files  = 3                                                           # Max number of historical files to be processed
gcm_soilmo_sec_extent     = [-156.0, -60.0, 6.00, 60.0]                                 # [min_lon, min_lat, max_lon, max_lat]
gcm_soilmo_sec_resolution = 10  # Max Res.: 10 km                                       # Final plot resolution
gcm_soilmo_sec_interval   = ''                                                          # Processing interval
gcm_soilmo_sec_config     = ''                                                          # Configuration string
gcm_soilmo_sec_script     = showcast_dir + '//Scripts//process_gcm_imagery_products.py' # Script to activate
gcm_soilmo_sec_output     = showcast_dir + '//Output//'                                  # Output folder

products.append('gcm_soilmo_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gcm_oceanp_sec            = True # GCOM-W1 - CLW, SST, TPW, WSPD

gcm_oceanp_sec_process    = 1                                                           # Process cicle for this product 
gcm_oceanp_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//G-OCEAN//'                    # Folder where the data is found
gcm_oceanp_sec_identifier = 'AMSR2-OCEAN*'                                              # Unique string on the file name
gcm_oceanp_sec_max_files  = 3                                                           # Max number of historical files to be processed
gcm_oceanp_sec_extent     = [-156.00, -65.00, 6.00, 65.00]                              # [min_lon, min_lat, max_lon, max_lat]
gcm_oceanp_sec_resolution = 10  # Max Res.: 10 km                                       # Final plot resolution
gcm_oceanp_sec_interval   = ''                                                          # Processing interval
gcm_oceanp_sec_config     = ''                                                          # Configuration string
gcm_oceanp_sec_script     = showcast_dir + '//Scripts//process_gcm_imagery_products.py' # Script to activate
gcm_oceanp_sec_output     = showcast_dir + '//Output//'                                 # Output folder

products.append('gcm_oceanp_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gcm_precip_sec            = True # GCOM-W1 - RAIN RATE, CONVECTIVE PREC, PROBABILITY

gcm_precip_sec_process    = 1                                                           # Process cicle for this product 
gcm_precip_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//G-PRECIPITATION//'            # Folder where the data is found
gcm_precip_sec_identifier = 'AMSR2-PRECIP*'                                             # Unique string on the file name
gcm_precip_sec_max_files  = 3                                                           # Max number of historical files to be processed
gcm_precip_sec_extent     = [-180.0, -90.0, 180.0, 90.0]                                # [min_lon, min_lat, max_lon, max_lat]
gcm_precip_sec_resolution = 10  # Max Res.: 10 km                                       # Final plot resolution
gcm_precip_sec_interval   = ''                                                          # Processing interval
gcm_precip_sec_config     = ''                                                          # Configuration string
gcm_precip_sec_script     = showcast_dir + '//Scripts//process_gcm_imagery_products.py' # Script to activate
gcm_precip_sec_output     = showcast_dir + '//Output//'                                 # Output folder

products.append('gcm_precip_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gcm_icepro_sec            = True # GCOM-W1 - SEA ICE NH

gcm_icepro_sec_process    = 1                                                           # Process cicle for this product 
gcm_icepro_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//G-SEAICE//'                   # Folder where the data is found
gcm_icepro_sec_identifier = 'AMSR2-SEAICE-NH*'                                          # Unique string on the file name
gcm_icepro_sec_max_files  = 3                                                           # Max number of historical files to be processed
gcm_icepro_sec_extent     = [-180.0, -90.0, 180.0, 90.0]                                # [min_lon, min_lat, max_lon, max_lat]
gcm_icepro_sec_resolution = 10  # Max Res.: 10 km                                       # Final plot resolution
gcm_icepro_sec_interval   = ''                                                          # Processing interval
gcm_icepro_sec_config     = ''                                                          # Configuration string
gcm_icepro_sec_script     = showcast_dir + '//Scripts//process_gcm_imagery_products.py' # Script to activate
gcm_icepro_sec_output     = showcast_dir + '//Output//'                                 # Output folder

products.append('gcm_icepro_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gcm_icepro_sec            = True # GCOM-W1 - SEA ICE SH

gcm_icepro_sec_process    = 1                                                           # Process cicle for this product 
gcm_icepro_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//G-SEAICE//'                   # Folder where the data is found
gcm_icepro_sec_identifier = 'AMSR2-SEAICE-SH*'                                          # Unique string on the file name
gcm_icepro_sec_max_files  = 3                                                           # Max number of historical files to be processed
gcm_icepro_sec_extent     = [-180.0, -90.0, 180.0, 90.0]                                # [min_lon, min_lat, max_lon, max_lat]
gcm_icepro_sec_resolution = 10  # Max Res.: 10 km                                       # Final plot resolution
gcm_icepro_sec_interval   = ''                                                          # Processing interval
gcm_icepro_sec_config     = ''                                                          # Configuration string
gcm_icepro_sec_script     = showcast_dir + '//Scripts//process_gcm_imagery_products.py' # Script to activate
gcm_icepro_sec_output     = showcast_dir + '//Output//'                                 # Output folder

products.append('gcm_icepro_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gcm_snowpr_sec            = True # GCOM-W1 - SNOW COVER, SNOW DEPTH, SWE

gcm_snowpr_sec_process    = 1                                                           # Process cicle for this product 
gcm_snowpr_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//G-SNOW//'                     # Folder where the data is found
gcm_snowpr_sec_identifier = 'AMSR2-SNOW*'                                               # Unique string on the file name
gcm_snowpr_sec_max_files  = 3                                                           # Max number of historical files to be processed
gcm_snowpr_sec_extent     = [-156.00, 0.00, -45.00, 75.00]                              # [min_lon, min_lat, max_lon, max_lat]
gcm_snowpr_sec_resolution = 10  # Max Res.: 10 km                                       # Final plot resolution
gcm_snowpr_sec_interval   = ''                                                          # Processing interval
gcm_snowpr_sec_config     = ''                                                          # Configuration string
gcm_snowpr_sec_script     = showcast_dir + '//Scripts//process_gcm_imagery_products.py' # Script to activate
gcm_snowpr_sec_output     = showcast_dir + '//Output//'                                 # Output folder

products.append('gcm_snowpr_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# HOURLY GLOBAL BLENDED PRODUCTS
#######################################################################################################

#------------------------------------------------------------------------------------------------------
mul_btpwpr_sec            = True # Hourly Global Blended Total Precipitable Water

mul_btpwpr_sec_process    = 1                                                         # Process cicle for this product 
mul_btpwpr_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//BTPW//'                     # Folder where the data is found
mul_btpwpr_sec_identifier = 'BHP-TPW*'                                                # Unique string on the file name
mul_btpwpr_sec_max_files  = 3                                                         # Max number of historical files to be processed
mul_btpwpr_sec_extent     = [-180.0, -71.0, 180.0, 71.0]                              # [min_lon, min_lat, max_lon, max_lat]
mul_btpwpr_sec_resolution = 8  # Max Res.: 16 km                                      # Final plot resolution
mul_btpwpr_sec_interval   = ''                                                        # Processing interval
mul_btpwpr_sec_config     = ''                                                        # Configuration string
mul_btpwpr_sec_script     = showcast_dir + '//Scripts//process_jps_btpw_v2.py'        # Script to activate
mul_btpwpr_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('mul_btpwpr_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
mul_bpctpr_sec            = True # Hourly Global Blended Total Precipitable Water Anomaly

mul_bpctpr_sec_process    = 1                                                         # Process cicle for this product 
mul_bpctpr_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//BTPW//'                     # Folder where the data is found
mul_bpctpr_sec_identifier = 'BHP-PCT*'                                                # Unique string on the file name
mul_bpctpr_sec_max_files  = 3                                                         # Max number of historical files to be processed
mul_bpctpr_sec_extent     = [-180.0, -71.0, 180.0, 71.0]                              # [min_lon, min_lat, max_lon, max_lat]
mul_bpctpr_sec_resolution = 8  # Max Res.: 16 km                                      # Final plot resolution
mul_bpctpr_sec_interval   = ''                                                        # Processing interval
mul_bpctpr_sec_config     = ''                                                        # Configuration string
mul_bpctpr_sec_script     = showcast_dir + '//Scripts//process_jps_btpw_v2.py'        # Script to activate
mul_bpctpr_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('mul_bpctpr_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
mul_rainpr_sec            = True # Hourly Global Rain Rate

mul_rainpr_sec_process    = 1                                                         # Process cicle for this product 
mul_rainpr_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//BTPW//'                     # Folder where the data is found
mul_rainpr_sec_identifier = 'BHP-RR*'                                                 # Unique string on the file name
mul_rainpr_sec_max_files  = 3                                                         # Max number of historical files to be processed
mul_rainpr_sec_extent     = [-180.0, -71.0, 180.0, 71.0]                              # [min_lon, min_lat, max_lon, max_lat]
mul_rainpr_sec_resolution = 8  # Max Res.: 16 km                                      # Final plot resolution
mul_rainpr_sec_interval   = ''                                                        # Processing interval
mul_rainpr_sec_config     = ''                                                        # Configuration string
mul_rainpr_sec_script     = showcast_dir + '//Scripts//process_jps_btpw_v2.py'        # Script to activate
mul_rainpr_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('mul_rainpr_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# FLOOD MAPPING PRODUCTS
#######################################################################################################

#------------------------------------------------------------------------------------------------------
fld_abihly_sec            = True # GOES-16 ABI Hourly Composite

fld_abihly_sec_process    = 1                                                                    # Process cicle for this product 
fld_abihly_sec_directory  = ingest_dir + 'CIMSS//Flood-ABI//'                                    # Folder where the data is found
fld_abihly_sec_identifier = '*part004*'                                                          # Unique string on the file name
fld_abihly_sec_max_files  = 3                                                                    # Max number of historical files to be processed
fld_abihly_sec_extent     = [-52.0, -5.0, -47.0, 0.0] # Recommended using a max of 5 x 5 degree  # [min_lon, min_lat, max_lon, max_lat]
fld_abihly_sec_resolution = 1  # Max Res.: 1 km                                                  # Final plot resolution
fld_abihly_sec_interval   = ''                                                                   # Processing interval
fld_abihly_sec_config     = ''                                                                   # Configuration string
fld_abihly_sec_script     = showcast_dir + '//Scripts//process_flood_mapping.py'                 # Script to activate
fld_abihly_sec_output     = showcast_dir + '//Output//'                                          # Output folder

products.append('fld_abihly_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
fld_joinva_sec            = True # Joint VIIRS / ABI flood product (daily)

fld_joinva_sec_process    = 1                                                                    # Process cicle for this product 
fld_joinva_sec_directory  = ingest_dir + 'CIMSS//Flood-Joint//'                                  # Folder where the data is found
fld_joinva_sec_identifier = '*part041*'                                                          # Unique string on the file name
fld_joinva_sec_max_files  = 3                                                                    # Max number of historical files to be processed
fld_joinva_sec_extent     = [-52.0, -5.0, -47.0, 0.0] # Recommended using a max of 5 x 5 degree  # [min_lon, min_lat, max_lon, max_lat]
fld_joinva_sec_resolution = 0.375 # Max Res.: 0.375 km                                           # Final plot resolution
fld_joinva_sec_interval   = ''                                                                   # Processing interval
fld_joinva_sec_config     = ''                                                                   # Configuration string
fld_joinva_sec_script     = showcast_dir + '//Scripts//process_flood_mapping.py'                 # Script to activate
fld_joinva_sec_output     = showcast_dir + '//Output//'                                          # Output folder

products.append('fld_joinva_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
fld_vrs5da_sec            = True # Suomi-NPP and NOAA-20 VIIRS 5-day Composite (daily)

fld_vrs5da_sec_process    = 1                                                                    # Process cicle for this product 
fld_vrs5da_sec_directory  = ingest_dir + 'CIMSS//Flood-Composite//'                              # Folder where the data is found
fld_vrs5da_sec_identifier = '*part041*'                                                          # Unique string on the file name
fld_vrs5da_sec_max_files  = 3                                                                    # Max number of historical files to be processed
fld_vrs5da_sec_extent     = [-52.0, -5.0, -47.0, 0.0] # Recommended using a max of 5 x 5 degree  # [min_lon, min_lat, max_lon, max_lat]
fld_vrs5da_sec_resolution = 0.375 # Max Res.: 0.375 km                                           # Final plot resolution
fld_vrs5da_sec_interval   = ''                                                                   # Processing interval
fld_vrs5da_sec_config     = ''                                                                   # Configuration string
fld_vrs5da_sec_script     = showcast_dir + '//Scripts//process_flood_mapping.py'                 # Script to activate
fld_vrs5da_sec_output     = showcast_dir + '//Output//'                                          # Output folder

products.append('fld_vrs5da_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# METOP GLOBAL SST
#######################################################################################################

#------------------------------------------------------------------------------------------------------
mtp_glbsst_sec            = True # METOP - Global Sea Surface Temperature

mtp_glbsst_sec_process    = 1                                                         # Process cicle for this product 
mtp_glbsst_sec_directory  = ingest_dir + 'EUMETSAT//'                                 # Folder where the data is found
mtp_glbsst_sec_identifier = '*MTOP-GLBSST*'                                           # Unique string on the file name
mtp_glbsst_sec_max_files  = 5                                                         # Max number of historical files to be processed
mtp_glbsst_sec_extent     = [-180.0, -70.0, 180.0, 80.0]                              # [min_lon, min_lat, max_lon, max_lat]
mtp_glbsst_sec_resolution = 16 # Max Res.: 6 km                                       # Final plot resolution
mtp_glbsst_sec_interval   = ''                                                        # Processing interval
mtp_glbsst_sec_config     = ''                                                        # Configuration string
mtp_glbsst_sec_script     = showcast_dir + '//Scripts//process_mtp_gblsst_sec.py'     # Script to activate
mtp_glbsst_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('mtp_glbsst_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# SEA ICE PRODUCTS
#######################################################################################################

#------------------------------------------------------------------------------------------------------
mul_sitype_sec            = True # Sea Ice Type (Northern Hemisphere)

mul_sitype_sec_process    = 1                                                         # Process cicle for this product 
mul_sitype_sec_directory  = ingest_dir + 'EUMETSAT//'                                 # Folder where the data is found
mul_sitype_sec_identifier = '*MULT-GL_NH_TYPEn*.gz'                                   # Unique string on the file name
mul_sitype_sec_max_files  = 1                                                         # Max number of historical files to be processed
mul_sitype_sec_extent     = [-180.0, -80.0, 180.0, 80.0]                              # [min_lon, min_lat, max_lon, max_lat]
mul_sitype_sec_resolution = 10 # Max Res.: 10 km                                      # Final plot resolution
mul_sitype_sec_interval   = ''                                                        # Processing interval
mul_sitype_sec_config     = ''                                                        # Configuration string
mul_sitype_sec_script     = showcast_dir + '//Scripts//process_ice.py'                # Script to activate
mul_sitype_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('mul_sitype_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
mul_sitype_sec            = True # Sea Ice Type (Southern Hemisphere)

mul_sitype_sec_process    = 1                                                         # Process cicle for this product 
mul_sitype_sec_directory  = ingest_dir + 'EUMETSAT//'                                 # Folder where the data is found
mul_sitype_sec_identifier = '*MULT-GL_SH_TYPEn*.gz'                                   # Unique string on the file name
mul_sitype_sec_max_files  = 1                                                         # Max number of historical files to be processed
mul_sitype_sec_extent     = [-180.0, -80.0, 180.0, 80.0]                              # [min_lon, min_lat, max_lon, max_lat]
mul_sitype_sec_resolution = 10 # Max Res.: 10 km                                      # Final plot resolution
mul_sitype_sec_interval   = ''                                                        # Processing interval
mul_sitype_sec_config     = ''                                                        # Configuration string
mul_sitype_sec_script     = showcast_dir + '//Scripts//process_ice.py'                # Script to activate
mul_sitype_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('mul_sitype_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
mul_siedge_sec            = True # Sea Ice Edge (Northern Hemisphere)

mul_siedge_sec_process    = 1                                                         # Process cicle for this product 
mul_siedge_sec_directory  = ingest_dir + 'EUMETSAT//'                                 # Folder where the data is found
mul_siedge_sec_identifier = '*MULT-GL_NH_EDGEn*.gz'                                   # Unique string on the file name
mul_siedge_sec_max_files  = 1                                                         # Max number of historical files to be processed
mul_siedge_sec_extent     = [-180.0, -80.0, 180.0, 80.0]                              # [min_lon, min_lat, max_lon, max_lat]
mul_siedge_sec_resolution = 10 # Max Res.: 10 km                                      # Final plot resolution
mul_siedge_sec_interval   = ''                                                        # Processing interval
mul_siedge_sec_config     = ''                                                        # Configuration string
mul_siedge_sec_script     = showcast_dir + '//Scripts//process_ice.py'                # Script to activate
mul_siedge_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('mul_siedge_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
mul_siedge_sec            = True # Sea Ice Edge (Southern Hemisphere)

mul_siedge_sec_process    = 1                                                         # Process cicle for this product 
mul_siedge_sec_directory  = ingest_dir + 'EUMETSAT//'                                 # Folder where the data is found
mul_siedge_sec_identifier = '*MULT-GL_SH_EDGEn*.gz'                                   # Unique string on the file name
mul_siedge_sec_max_files  = 1                                                         # Max number of historical files to be processed
mul_siedge_sec_extent     = [-180.0, -80.0, 180.0, 80.0]                              # [min_lon, min_lat, max_lon, max_lat]
mul_siedge_sec_resolution = 10 # Max Res.: 10 km                                      # Final plot resolution
mul_siedge_sec_interval   = ''                                                        # Processing interval
mul_siedge_sec_config     = ''                                                        # Configuration string
mul_siedge_sec_script     = showcast_dir + '//Scripts//process_ice.py'                # Script to activate
mul_siedge_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('mul_siedge_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
dms_siconc_sec            = True # DMSP SSMIS Sea Ice Concentration (Northern Hemisphere)

dms_siconc_sec_process    = 1                                                         # Process cicle for this product 
dms_siconc_sec_directory  = ingest_dir + 'EUMETSAT//'                                 # Folder where the data is found
dms_siconc_sec_identifier = '*MULT-GL_NH_CONCn*.gz'                                   # Unique string on the file name
dms_siconc_sec_max_files  = 1                                                         # Max number of historical files to be processed
dms_siconc_sec_extent     = [-180.0, -80.0, 180.0, 80.0]                              # [min_lon, min_lat, max_lon, max_lat]
dms_siconc_sec_resolution = 10 # Max Res.: 10 km                                      # Final plot resolution
dms_siconc_sec_interval   = ''                                                        # Processing interval
dms_siconc_sec_config     = ''                                                        # Configuration string
dms_siconc_sec_script     = showcast_dir + '//Scripts//process_ice.py'                # Script to activate
dms_siconc_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('dms_siconc_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
dms_siconc_sec            = True # DMSP SSMIS Sea Ice Concentration (Southern Hemisphere)

dms_siconc_sec_process    = 1                                                         # Process cicle for this product 
dms_siconc_sec_directory  = ingest_dir + 'EUMETSAT//'                                 # Folder where the data is found
dms_siconc_sec_identifier = '*MULT-GL_SH_CONCn*.gz'                                   # Unique string on the file name
dms_siconc_sec_max_files  = 1                                                         # Max number of historical files to be processed
dms_siconc_sec_extent     = [-180.0, -80.0, 180.0, 80.0]                              # [min_lon, min_lat, max_lon, max_lat]
dms_siconc_sec_resolution = 10 # Max Res.: 10 km                                      # Final plot resolution
dms_siconc_sec_interval   = ''                                                        # Processing interval
dms_siconc_sec_config     = ''                                                        # Configuration string
dms_siconc_sec_script     = showcast_dir + '//Scripts//process_ice.py'                # Script to activate
dms_siconc_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('dms_siconc_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
dms_siemis_sec            = True # DMSP AMSU / SSMIS Sea Ice Emissivity (Northern Hemisphere)

dms_siemis_sec_process    = 1                                                         # Process cicle for this product 
dms_siemis_sec_directory  = ingest_dir + 'EUMETSAT//'                                 # Folder where the data is found
dms_siemis_sec_identifier = '*DMSP-GL_NH_EMIS*.gz'                                    # Unique string on the file name
dms_siemis_sec_max_files  = 1                                                         # Max number of historical files to be processed
dms_siemis_sec_extent     = [-180.0, -80.0, 180.0, 80.0]                              # [min_lon, min_lat, max_lon, max_lat]
dms_siemis_sec_resolution = 10 # Max Res.: 10 km                                      # Final plot resolution
dms_siemis_sec_interval   = ''                                                        # Processing interval
dms_siemis_sec_config     = ''                                                        # Configuration string
dms_siemis_sec_script     = showcast_dir + '//Scripts//process_ice.py'                # Script to activate
dms_siemis_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('dms_siemis_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
dms_siemis_sec            = True # DMSP AMSU / SSMIS Sea Ice Emissivity (Southern Hemisphere)

dms_siemis_sec_process    = 1                                                         # Process cicle for this product 
dms_siemis_sec_directory  = ingest_dir + 'EUMETSAT//'                                 # Folder where the data is found
dms_siemis_sec_identifier = '*DMSP-GL_SH_EMIS*.gz'                                    # Unique string on the file name
dms_siemis_sec_max_files  = 1                                                         # Max number of historical files to be processed
dms_siemis_sec_extent     = [-180.0, -80.0, 180.0, 80.0]                              # [min_lon, min_lat, max_lon, max_lat]
dms_siemis_sec_resolution = 10 # Max Res.: 10 km                                      # Final plot resolution
dms_siemis_sec_interval   = ''                                                        # Processing interval
dms_siemis_sec_config     = ''                                                        # Configuration string
dms_siemis_sec_script     = showcast_dir + '//Scripts//process_ice.py'                # Script to activate
dms_siemis_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('dms_siemis_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# NUCAPS SOUNDINGS - SUGGESTION: PUT IN A DEDICATED PROCESS
#######################################################################################################

#------------------------------------------------------------------------------------------------------
n20_nucaps_sec            = True # NUCAPS SOUNDINGS

n20_nucaps_sec_process    = 1                                                         # Process cicle for this product 
n20_nucaps_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//NUCAPS//'                   # Folder where the data is found
n20_nucaps_sec_identifier = 'NUCAPS-EDR*'                                             # Unique string on the file name
n20_nucaps_sec_max_files  = 300                                                       # Max number of historical files to be processed
n20_nucaps_sec_extent     = [-54.0, -28.0, -43.0, -18.0]                              # Recommended using a max of 5 x 5 degree  # [min_lon, min_lat, max_lon, max_lat]
n20_nucaps_sec_resolution = 1 # Max Res.: 1 km                                        # Final plot resolution
n20_nucaps_sec_interval   = ''                                                        # Processing interval
n20_nucaps_sec_config     = ''                                                        # Configuration string
n20_nucaps_sec_script     = showcast_dir + '//Scripts//process_nucaps.py'             # Script to activate
n20_nucaps_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('n20_nucaps_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# MULTIMISSION FIRE / HOT SPOTS (INPE SHAPEFILES)
#######################################################################################################

#------------------------------------------------------------------------------------------------------
mul_firein_sec            = True # MULTIMISSION FIRE / HOTSPOTS - INPE

mul_firein_sec_process    = 1                                                         # Process cicle for this product 
mul_firein_sec_directory  = ingest_dir + 'INPE//'                                     # Folder where the data is found
mul_firein_sec_identifier = 'INPE_MVF_*.gz'                                           # Unique string on the file name
mul_firein_sec_max_files  = 1                                                         # Max number of historical files to be processed
mul_firein_sec_resolution = 0 # Max Res.: N/A                                         # Final plot resolution
mul_firein_sec_interval   = ''                                                        # Processing interval
mul_firein_sec_config     = ''                                                        # Configuration string
mul_firein_sec_script     = showcast_dir + '//Scripts//process_mul_fires.py'          # Script to activate
mul_firein_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('mul_firein_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# BLENDED TOAST - DAILY TOTAL OZONE
#######################################################################################################

#------------------------------------------------------------------------------------------------------
jps_tstngl_sec            = True # TOAST - SNPP OMPS & NOAA-20 CrIS DAILY TOTAL OZONE - GLOBAL

jps_tstngl_sec_process    = 1                                                         # Process cicle for this product 
jps_tstngl_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//TOAST//'                    # Folder where the data is found
jps_tstngl_sec_identifier = '*j01_CRIN_j01_OMPS*'                                     # Unique string on the file name
jps_tstngl_sec_max_files  = 1                                                         # Max number of historical files to be processed
jps_tstngl_sec_extent     = [-180.0, -90.0, 180.0, 90.0]                              # [min_lon, min_lat, max_lon, max_lat]
jps_tstngl_sec_resolution = 8                                                         # Final plot resolution
jps_tstngl_sec_interval   = ''                                                        # Processing interval
jps_tstngl_sec_config     = ''                                                        # Configuration string
jps_tstngl_sec_script     = showcast_dir + '//Scripts//process_jps_tstngl_sec.py'     # Script to activate
jps_tstngl_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('jps_tstngl_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
jps_tstnnh_sec            = True # TOAST - SNPP OMPS & NOAA-20 CrIS DAILY TOTAL OZONE - NORTHERN HEMISPHERE

jps_tstnnh_sec_process    = 1                                                         # Process cicle for this product 
jps_tstnnh_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//TOAST//'                    # Folder where the data is found
jps_tstnnh_sec_identifier = '*j01_CRIN_j01_OMPS*'                                     # Unique string on the file name
jps_tstnnh_sec_max_files  = 1                                                         # Max number of historical files to be processed
jps_tstnnh_sec_extent     = [-180.0, -90.0, 180.0, 90.0]                              # [min_lon, min_lat, max_lon, max_lat]
jps_tstnnh_sec_resolution = 8                                                         # Final plot resolution
jps_tstnnh_sec_interval   = ''                                                        # Processing interval
jps_tstnnh_sec_config     = '_NHP'                                                    # Configuration string
jps_tstnnh_sec_script     = showcast_dir + '//Scripts//process_jps_tstnnh_sec.py'     # Script to activate
jps_tstnnh_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('jps_tstnnh_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
jps_tstnsh_sec            = True # TOAST - SNPP OMPS & NOAA-20 CrIS DAILY TOTAL OZONE - SOUTHERN HEMISPHERE

jps_tstnsh_sec_process    = 1                                                         # Process cicle for this product 
jps_tstnsh_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//TOAST//'                    # Folder where the data is found
jps_tstnsh_sec_identifier = '*j01_CRIN_j01_OMPS*'                                     # Unique string on the file name
jps_tstnsh_sec_max_files  = 1                                                         # Max number of historical files to be processed
jps_tstnsh_sec_extent     = [-180.0, -90.0, 180.0, 90.0]                              # [min_lon, min_lat, max_lon, max_lat]
jps_tstnsh_sec_resolution = 8                                                         # Final plot resolution
jps_tstnsh_sec_interval   = ''                                                        # Processing interval
jps_tstnsh_sec_config     = '_SHP'                                                    # Configuration string
jps_tstnsh_sec_script     = showcast_dir + '//Scripts//process_jps_tstnsh_sec.py'     # Script to activate
jps_tstnsh_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('jps_tstnsh_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GFS MODEL 0.5 DEGREE - SOUTH AMERICA - 00Z RUN (SET AS TRUE ONLY SAM OR ONLY CRB!)
#######################################################################################################

#------------------------------------------------------------------------------------------------------
gfs_2mtems_00z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - 2 M TEMPERATURE

gfs_2mtems_00z_process    = 1                                                         # Process cicle for this product 
gfs_2mtems_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_2mtems_00z_identifier = 'gfs.sam.t00z.f120'                                       # Unique string on the file name
gfs_2mtems_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_2mtems_00z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_2mtems_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_2mtems_00z_interval   = ''                                                        # Processing interval
gfs_2mtems_00z_config     = '_001'                                                    # Configuration string
gfs_2mtems_00z_script     = showcast_dir + '//Scripts//process_gfs_2mtemp_sec.py'     # Script to activate
gfs_2mtems_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_2mtems_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_accprs_00z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - ACCUMULATED PRECIPITACION 

gfs_accprs_00z_process    = 1                                                         # Process cicle for this product 
gfs_accprs_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_accprs_00z_identifier = 'gfs.sam.t00z.f120'                                       # Unique string on the file name
gfs_accprs_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_accprs_00z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_accprs_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_accprs_00z_interval   = ''                                                        # Processing interval
gfs_accprs_00z_config     = '_002'                                                    # Configuration string
gfs_accprs_00z_script     = showcast_dir + '//Scripts//process_gfs_accpre_sec.py'     # Script to activate
gfs_accprs_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_accprs_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_prtmss_00z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - PRESSION REDUCED TO MEAN SEA LEVEL

gfs_prtmss_00z_process    = 1                                                         # Process cicle for this product 
gfs_prtmss_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_prtmss_00z_identifier = 'gfs.sam.t00z.f120'                                       # Unique string on the file name
gfs_prtmss_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_prtmss_00z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_prtmss_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_prtmss_00z_interval   = ''                                                        # Processing interval
gfs_prtmss_00z_config     = '_003'                                                    # Configuration string
gfs_prtmss_00z_script     = showcast_dir + '//Scripts//process_gfs_prtmsl_sec.py'     # Script to activate
gfs_prtmss_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_prtmss_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_gdinds_00z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - GALVEZ DAVISON INDEX

gfs_gdinds_00z_process    = 1                                                         # Process cicle for this product 
gfs_gdinds_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_gdinds_00z_identifier = 'gfs.sam.t00z.f120'                                       # Unique string on the file name
gfs_gdinds_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_gdinds_00z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_gdinds_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_gdinds_00z_interval   = ''                                                        # Processing interval
gfs_gdinds_00z_config     = '_004'                                                    # Configuration string
gfs_gdinds_00z_script     = showcast_dir + '//Scripts//process_gfs_gdindx_sec.py'     # Script to activate
gfs_gdinds_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_gdinds_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_gh500s_00z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - RELATIVE VORTICITY AND GEOPOTENTIAL HEIGHT 500 hPa

gfs_gh500s_00z_process    = 1                                                         # Process cicle for this product 
gfs_gh500s_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_gh500s_00z_identifier = 'gfs.sam.t00z.f120'                                       # Unique string on the file name
gfs_gh500s_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_gh500s_00z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_gh500s_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_gh500s_00z_interval   = ''                                                        # Processing interval
gfs_gh500s_00z_config     = '_005'                                                    # Configuration string
gfs_gh500s_00z_script     = showcast_dir + '//Scripts//process_gfs_ghv500_sec.py'     # Script to activate
gfs_gh500s_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_gh500s_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_psgwrs_00z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - PSML + GEOP. DIF. (1000-850 hPa) + WINDS (925 hPa) + MEAN RH (1000~400 hPa)

gfs_psgwrs_00z_process    = 1                                                         # Process cicle for this product 
gfs_psgwrs_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_psgwrs_00z_identifier = 'gfs.sam.t00z.f120'                                       # Unique string on the file name
gfs_psgwrs_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_psgwrs_00z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_psgwrs_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_psgwrs_00z_interval   = ''                                                        # Processing interval
gfs_psgwrs_00z_config     = '_006'                                                    # Configuration string
gfs_psgwrs_00z_script     = showcast_dir + '//Scripts//process_gfs_psgwrh_sec.py'     # Script to activate
gfs_psgwrs_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_psgwrs_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_pwcaps_00z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - PRECIPITABLE WATER & CAPE

gfs_pwcaps_00z_process    = 1                                                         # Process cicle for this product 
gfs_pwcaps_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_pwcaps_00z_identifier = 'gfs.sam.t00z.f120'                                       # Unique string on the file name
gfs_pwcaps_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_pwcaps_00z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_pwcaps_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_pwcaps_00z_interval   = ''                                                        # Processing interval
gfs_pwcaps_00z_config     = '_007'                                                    # Configuration string
gfs_pwcaps_00z_script     = showcast_dir + '//Scripts//process_gfs_pwcape_sec.py'     # Script to activate
gfs_pwcaps_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_pwcaps_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_sphcls_00z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - SPECIFIC HUMIDITY > 70% @ 800, 500 & 300 hPa 

gfs_sphcls_00z_process    = 1                                                         # Process cicle for this product 
gfs_sphcls_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_sphcls_00z_identifier = 'gfs.sam.t00z.f120'                                       # Unique string on the file name
gfs_sphcls_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_sphcls_00z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_sphcls_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_sphcls_00z_interval   = ''                                                        # Processing interval
gfs_sphcls_00z_config     = '_008'                                                    # Configuration string
gfs_sphcls_00z_script     = showcast_dir + '//Scripts//process_gfs_sphcld_sec.py'     # Script to activate
gfs_sphcls_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_sphcls_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws200s_00z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - WIND SPEED AND DIRECTION - 200 hPa

gfs_ws200s_00z_process    = 1                                                         # Process cicle for this product 
gfs_ws200s_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws200s_00z_identifier = 'gfs.sam.t00z.f120'                                       # Unique string on the file name
gfs_ws200s_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws200s_00z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws200s_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws200s_00z_interval   = ''                                                        # Processing interval
gfs_ws200s_00z_config     = '_009'                                                    # Configuration string
gfs_ws200s_00z_script     = showcast_dir + '//Scripts//process_gfs_wsd200_sec.py'     # Script to activate
gfs_ws200s_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws200s_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws500s_00z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - WIND SPEED AND DIRECTION - 500 hPa

gfs_ws500s_00z_process    = 1                                                         # Process cicle for this product 
gfs_ws500s_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws500s_00z_identifier = 'gfs.sam.t00z.f120'                                       # Unique string on the file name
gfs_ws500s_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws500s_00z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws500s_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws500s_00z_interval   = ''                                                        # Processing interval
gfs_ws500s_00z_config     = '_010'                                                    # Configuration string
gfs_ws500s_00z_script     = showcast_dir + '//Scripts//process_gfs_wsd500_sec.py'     # Script to activate
gfs_ws500s_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws500s_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws700s_00z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - WIND SPEED AND DIRECTION - 700 hPa

gfs_ws700s_00z_process    = 1                                                         # Process cicle for this product 
gfs_ws700s_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws700s_00z_identifier = 'gfs.sam.t00z.f120'                                       # Unique string on the file name
gfs_ws700s_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws700s_00z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws700s_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws700s_00z_interval   = ''                                                        # Processing interval
gfs_ws700s_00z_config     = '_011'                                                    # Configuration string
gfs_ws700s_00z_script     = showcast_dir + '//Scripts//process_gfs_wsd700_sec.py'     # Script to activate
gfs_ws700s_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws700s_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws850s_00z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - WIND SPEED AND DIRECTION - 850 hPa

gfs_ws850s_00z_process    = 1                                                         # Process cicle for this product 
gfs_ws850s_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws850s_00z_identifier = 'gfs.sam.t00z.f120'                                       # Unique string on the file name
gfs_ws850s_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws850s_00z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws850s_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws850s_00z_interval   = ''                                                        # Processing interval
gfs_ws850s_00z_config     = '_012'                                                    # Configuration string
gfs_ws850s_00z_script     = showcast_dir + '//Scripts//process_gfs_wsd850_sec.py'     # Script to activate
gfs_ws850s_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws850s_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_pwcpts_00z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - PSML / WIND 10 m / CLOUDS / PREC / THICKNESS (500-1000 hPa)

gfs_pwcpts_00z_process    = 1                                                         # Process cicle for this product 
gfs_pwcpts_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_pwcpts_00z_identifier = 'gfs.sam.t00z.f120'                                       # Unique string on the file name
gfs_pwcpts_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_pwcpts_00z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_pwcpts_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_pwcpts_00z_interval   = ''                                                        # Processing interval
gfs_pwcpts_00z_config     = '_013'                                                    # Configuration string
gfs_pwcpts_00z_script     = showcast_dir + '//Scripts//process_gfs_pwcpth_sec.py'     # Script to activate
gfs_pwcpts_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_pwcpts_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
#######################################################################################################
# GFS MODEL 0.5 DEGREE - SOUTH AMERICA - 12Z RUN (SET AS TRUE ONLY SAM OR ONLY CRB!)
#######################################################################################################

#------------------------------------------------------------------------------------------------------
gfs_2mtems_12z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - 2 M TEMPERATURE

gfs_2mtems_12z_process    = 1                                                         # Process cicle for this product 
gfs_2mtems_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_2mtems_12z_identifier = 'gfs.sam.t12z.f120'                                       # Unique string on the file name
gfs_2mtems_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_2mtems_12z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_2mtems_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_2mtems_12z_interval   = ''                                                        # Processing interval
gfs_2mtems_12z_config     = '_001'                                                    # Configuration string
gfs_2mtems_12z_script     = showcast_dir + '//Scripts//process_gfs_2mtemp_sec.py'     # Script to activate
gfs_2mtems_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_2mtems_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_accprs_12z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - ACCUMULATED PRECIPITACION 

gfs_accprs_12z_process    = 1                                                         # Process cicle for this product 
gfs_accprs_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_accprs_12z_identifier = 'gfs.sam.t12z.f120'                                       # Unique string on the file name
gfs_accprs_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_accprs_12z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_accprs_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_accprs_12z_interval   = ''                                                        # Processing interval
gfs_accprs_12z_config     = '_002'                                                    # Configuration string
gfs_accprs_12z_script     = showcast_dir + '//Scripts//process_gfs_accpre_sec.py'     # Script to activate
gfs_accprs_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_accprs_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_prtmss_12z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - PRESSION REDUCED TO MEAN SEA LEVEL

gfs_prtmss_12z_process    = 1                                                         # Process cicle for this product 
gfs_prtmss_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_prtmss_12z_identifier = 'gfs.sam.t12z.f120'                                       # Unique string on the file name
gfs_prtmss_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_prtmss_12z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_prtmss_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_prtmss_12z_interval   = ''                                                        # Processing interval
gfs_prtmss_12z_config     = '_003'                                                    # Configuration string
gfs_prtmss_12z_script     = showcast_dir + '//Scripts//process_gfs_prtmsl_sec.py'     # Script to activate
gfs_prtmss_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_prtmss_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_gdinds_12z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - GALVEZ DAVISON INDEX

gfs_gdinds_12z_process    = 1                                                         # Process cicle for this product 
gfs_gdinds_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_gdinds_12z_identifier = 'gfs.sam.t12z.f120'                                       # Unique string on the file name
gfs_gdinds_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_gdinds_12z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_gdinds_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_gdinds_12z_interval   = ''                                                        # Processing interval
gfs_gdinds_12z_config     = '_004'                                                    # Configuration string
gfs_gdinds_12z_script     = showcast_dir + '//Scripts//process_gfs_gdindx_sec.py'     # Script to activate
gfs_gdinds_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_gdinds_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_gh500s_12z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - RELATIVE VORTICITY AND GEOPOTENTIAL HEIGHT 500 hPa

gfs_gh500s_12z_process    = 1                                                         # Process cicle for this product 
gfs_gh500s_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_gh500s_12z_identifier = 'gfs.sam.t12z.f120'                                       # Unique string on the file name
gfs_gh500s_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_gh500s_12z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_gh500s_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_gh500s_12z_interval   = ''                                                        # Processing interval
gfs_gh500s_12z_config     = '_005'                                                    # Configuration string
gfs_gh500s_12z_script     = showcast_dir + '//Scripts//process_gfs_ghv500_sec.py'     # Script to activate
gfs_gh500s_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_gh500s_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_psgwrs_12z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - PSML + GEOP. DIF. (1000-850 hPa) + WINDS (925 hPa) + MEAN RH (1000~400 hPa)

gfs_psgwrs_12z_process    = 1                                                         # Process cicle for this product 
gfs_psgwrs_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_psgwrs_12z_identifier = 'gfs.sam.t12z.f120'                                       # Unique string on the file name
gfs_psgwrs_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_psgwrs_12z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_psgwrs_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_psgwrs_12z_interval   = ''                                                        # Processing interval
gfs_psgwrs_12z_config     = '_006'                                                    # Configuration string
gfs_psgwrs_12z_script     = showcast_dir + '//Scripts//process_gfs_psgwrh_sec.py'     # Script to activate
gfs_psgwrs_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_psgwrs_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_pwcaps_12z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - PRECIPITABLE WATER & CAPE

gfs_pwcaps_12z_process    = 1                                                         # Process cicle for this product 
gfs_pwcaps_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_pwcaps_12z_identifier = 'gfs.sam.t12z.f120'                                       # Unique string on the file name
gfs_pwcaps_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_pwcaps_12z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_pwcaps_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_pwcaps_12z_interval   = ''                                                        # Processing interval
gfs_pwcaps_12z_config     = '_007'                                                    # Configuration string
gfs_pwcaps_12z_script     = showcast_dir + '//Scripts//process_gfs_pwcape_sec.py'     # Script to activate
gfs_pwcaps_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_pwcaps_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_sphcls_12z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - SPECIFIC HUMIDITY > 70% @ 800, 500 & 300 hPa 

gfs_sphcls_12z_process    = 1                                                         # Process cicle for this product 
gfs_sphcls_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_sphcls_12z_identifier = 'gfs.sam.t12z.f120'                                       # Unique string on the file name
gfs_sphcls_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_sphcls_12z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_sphcls_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_sphcls_12z_interval   = ''                                                        # Processing interval
gfs_sphcls_12z_config     = '_008'                                                    # Configuration string
gfs_sphcls_12z_script     = showcast_dir + '//Scripts//process_gfs_sphcld_sec.py'     # Script to activate
gfs_sphcls_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_sphcls_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws200s_12z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - WIND SPEED AND DIRECTION - 200 hPa

gfs_ws200s_12z_process    = 1                                                         # Process cicle for this product 
gfs_ws200s_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws200s_12z_identifier = 'gfs.sam.t12z.f120'                                       # Unique string on the file name
gfs_ws200s_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws200s_12z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws200s_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws200s_12z_interval   = ''                                                        # Processing interval
gfs_ws200s_12z_config     = '_009'                                                    # Configuration string
gfs_ws200s_12z_script     = showcast_dir + '//Scripts//process_gfs_wsd200_sec.py'     # Script to activate
gfs_ws200s_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws200s_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws500s_12z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - WIND SPEED AND DIRECTION - 500 hPa

gfs_ws500s_12z_process    = 1                                                         # Process cicle for this product 
gfs_ws500s_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws500s_12z_identifier = 'gfs.sam.t12z.f120'                                       # Unique string on the file name
gfs_ws500s_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws500s_12z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws500s_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws500s_12z_interval   = ''                                                        # Processing interval
gfs_ws500s_12z_config     = '_010'                                                    # Configuration string
gfs_ws500s_12z_script     = showcast_dir + '//Scripts//process_gfs_wsd500_sec.py'     # Script to activate
gfs_ws500s_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws500s_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws700s_12z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - WIND SPEED AND DIRECTION - 700 hPa

gfs_ws700s_12z_process    = 1                                                         # Process cicle for this product 
gfs_ws700s_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws700s_12z_identifier = 'gfs.sam.t12z.f120'                                       # Unique string on the file name
gfs_ws700s_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws700s_12z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws700s_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws700s_12z_interval   = ''                                                        # Processing interval
gfs_ws700s_12z_config     = '_011'                                                    # Configuration string
gfs_ws700s_12z_script     = showcast_dir + '//Scripts//process_gfs_wsd700_sec.py'     # Script to activate
gfs_ws700s_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws700s_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws850s_12z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - WIND SPEED AND DIRECTION - 850 hPa

gfs_ws850s_12z_process    = 1                                                         # Process cicle for this product 
gfs_ws850s_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws850s_12z_identifier = 'gfs.sam.t12z.f120'                                       # Unique string on the file name
gfs_ws850s_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws850s_12z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws850s_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws850s_12z_interval   = ''                                                        # Processing interval
gfs_ws850s_12z_config     = '_012'                                                    # Configuration string
gfs_ws850s_12z_script     = showcast_dir + '//Scripts//process_gfs_wsd850_sec.py'     # Script to activate
gfs_ws850s_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws850s_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_pwcpts_12z            = True # GFS MODEL 0.5 DEGREE - SOUTH AMERICA - PSML / WIND 10 m / CLOUDS / PREC / THICKNESS (500-1000 hPa)

gfs_pwcpts_12z_process    = 1                                                         # Process cicle for this product 
gfs_pwcpts_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_pwcpts_12z_identifier = 'gfs.sam.t12z.f120'                                       # Unique string on the file name
gfs_pwcpts_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_pwcpts_12z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_pwcpts_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_pwcpts_12z_interval   = ''                                                        # Processing interval
gfs_pwcpts_12z_config     = '_013'                                                    # Configuration string
gfs_pwcpts_12z_script     = showcast_dir + '//Scripts//process_gfs_pwcpth_sec.py'     # Script to activate
gfs_pwcpts_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_pwcpts_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - 00Z RUN (SET AS TRUE ONLY SAM OR ONLY CRB!)
#######################################################################################################

#------------------------------------------------------------------------------------------------------
gfs_2mtemc_00z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - 2 M TEMPERATURE

gfs_2mtemc_00z_process    = 1                                                         # Process cicle for this product 
gfs_2mtemc_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_2mtemc_00z_identifier = 'gfs.crb.t00z.f120'                                       # Unique string on the file name
gfs_2mtemc_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_2mtemc_00z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_2mtemc_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_2mtemc_00z_interval   = ''                                                        # Processing interval
gfs_2mtemc_00z_config     = '_001'                                                    # Configuration string
gfs_2mtemc_00z_script     = showcast_dir + '//Scripts//process_gfs_2mtemp_sec.py'     # Script to activate
gfs_2mtemc_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_2mtemc_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_accprc_00z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - ACCUMULATED PRECIPITACION 

gfs_accprc_00z_process    = 1                                                         # Process cicle for this product 
gfs_accprc_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_accprc_00z_identifier = 'gfs.crb.t00z.f120'                                       # Unique string on the file name
gfs_accprc_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_accprc_00z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_accprc_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_accprc_00z_interval   = ''                                                        # Processing interval
gfs_accprc_00z_config     = '_002'                                                    # Configuration string
gfs_accprc_00z_script     = showcast_dir + '//Scripts//process_gfs_accpre_sec.py'     # Script to activate
gfs_accprc_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_accprc_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_prtmsc_00z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - PRESSION REDUCED TO MEAN SEA LEVEL

gfs_prtmsc_00z_process    = 1                                                         # Process cicle for this product 
gfs_prtmsc_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_prtmsc_00z_identifier = 'gfs.crb.t00z.f120'                                       # Unique string on the file name
gfs_prtmsc_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_prtmsc_00z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_prtmsc_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_prtmsc_00z_interval   = ''                                                        # Processing interval
gfs_prtmsc_00z_config     = '_003'                                                    # Configuration string
gfs_prtmsc_00z_script     = showcast_dir + '//Scripts//process_gfs_prtmsl_sec.py'     # Script to activate
gfs_prtmsc_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_prtmsc_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_gdindc_00z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - GALVEZ DAVISON INDEX

gfs_gdindc_00z_process    = 1                                                         # Process cicle for this product 
gfs_gdindc_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_gdindc_00z_identifier = 'gfs.crb.t00z.f120'                                       # Unique string on the file name
gfs_gdindc_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_gdindc_00z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_gdindc_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_gdindc_00z_interval   = ''                                                        # Processing interval
gfs_gdindc_00z_config     = '_004'                                                    # Configuration string
gfs_gdindc_00z_script     = showcast_dir + '//Scripts//process_gfs_gdindx_sec.py'     # Script to activate
gfs_gdindc_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_gdindc_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_gh500c_00z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - RELATIVE VORTICITY AND GEOPOTENTIAL HEIGHT 500 hPa

gfs_gh500c_00z_process    = 1                                                         # Process cicle for this product 
gfs_gh500c_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_gh500c_00z_identifier = 'gfs.crb.t00z.f120'                                       # Unique string on the file name
gfs_gh500c_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_gh500c_00z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_gh500c_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_gh500c_00z_interval   = ''                                                        # Processing interval
gfs_gh500c_00z_config     = '_005'                                                    # Configuration string
gfs_gh500c_00z_script     = showcast_dir + '//Scripts//process_gfs_ghv500_sec.py'     # Script to activate
gfs_gh500c_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_gh500c_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_psgwrc_00z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - PSML + GEOP. DIF. (1000-850 hPa) + WINDS (925 hPa) + MEAN RH (1000~400 hPa)

gfs_psgwrc_00z_process    = 1                                                         # Process cicle for this product 
gfs_psgwrc_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_psgwrc_00z_identifier = 'gfs.crb.t00z.f120'                                       # Unique string on the file name
gfs_psgwrc_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_psgwrc_00z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_psgwrc_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_psgwrc_00z_interval   = ''                                                        # Processing interval
gfs_psgwrc_00z_config     = '_006'                                                    # Configuration string
gfs_psgwrc_00z_script     = showcast_dir + '//Scripts//process_gfs_psgwrh_sec.py'     # Script to activate
gfs_psgwrc_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_psgwrc_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_pwcapc_00z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - PRECIPITABLE WATER & CAPE

gfs_pwcapc_00z_process    = 1                                                         # Process cicle for this product 
gfs_pwcapc_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_pwcapc_00z_identifier = 'gfs.crb.t00z.f120'                                       # Unique string on the file name
gfs_pwcapc_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_pwcapc_00z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_pwcapc_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_pwcapc_00z_interval   = ''                                                        # Processing interval
gfs_pwcapc_00z_config     = '_007'                                                    # Configuration string
gfs_pwcapc_00z_script     = showcast_dir + '//Scripts//process_gfs_pwcape_sec.py'     # Script to activate
gfs_pwcapc_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_pwcapc_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_sphclc_00z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - SPECIFIC HUMIDITY > 70% @ 800, 500 & 300 hPa 

gfs_sphclc_00z_process    = 1                                                         # Process cicle for this product 
gfs_sphclc_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_sphclc_00z_identifier = 'gfs.crb.t00z.f120'                                       # Unique string on the file name
gfs_sphclc_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_sphclc_00z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_sphclc_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_sphclc_00z_interval   = ''                                                        # Processing interval
gfs_sphclc_00z_config     = '_008'                                                    # Configuration string
gfs_sphclc_00z_script     = showcast_dir + '//Scripts//process_gfs_sphcld_sec.py'     # Script to activate
gfs_sphclc_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_sphclc_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws200c_00z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - WIND SPEED AND DIRECTION - 200 hPa

gfs_ws200c_00z_process    = 1                                                         # Process cicle for this product 
gfs_ws200c_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws200c_00z_identifier = 'gfs.crb.t00z.f120'                                       # Unique string on the file name
gfs_ws200c_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws200c_00z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws200c_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws200c_00z_interval   = ''                                                        # Processing interval
gfs_ws200c_00z_config     = '_009'                                                    # Configuration string
gfs_ws200c_00z_script     = showcast_dir + '//Scripts//process_gfs_wsd200_sec.py'     # Script to activate
gfs_ws200c_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws200c_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws500c_00z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - WIND SPEED AND DIRECTION - 500 hPa

gfs_ws500c_00z_process    = 1                                                         # Process cicle for this product 
gfs_ws500c_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws500c_00z_identifier = 'gfs.crb.t00z.f120'                                       # Unique string on the file name
gfs_ws500c_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws500c_00z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws500c_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws500c_00z_interval   = ''                                                        # Processing interval
gfs_ws500c_00z_config     = '_010'                                                    # Configuration string
gfs_ws500c_00z_script     = showcast_dir + '//Scripts//process_gfs_wsd500_sec.py'     # Script to activate
gfs_ws500c_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws500c_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws700c_00z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - WIND SPEED AND DIRECTION - 700 hPa

gfs_ws700c_00z_process    = 1                                                         # Process cicle for this product 
gfs_ws700c_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws700c_00z_identifier = 'gfs.crb.t00z.f120'                                       # Unique string on the file name
gfs_ws700c_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws700c_00z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws700c_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws700c_00z_interval   = ''                                                        # Processing interval
gfs_ws700c_00z_config     = '_011'                                                    # Configuration string
gfs_ws700c_00z_script     = showcast_dir + '//Scripts//process_gfs_wsd700_sec.py'     # Script to activate
gfs_ws700c_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws700c_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws850c_00z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - WIND SPEED AND DIRECTION - 850 hPa

gfs_ws850c_00z_process    = 1                                                         # Process cicle for this product 
gfs_ws850c_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws850c_00z_identifier = 'gfs.crb.t00z.f120'                                       # Unique string on the file name
gfs_ws850c_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws850c_00z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws850c_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws850c_00z_interval   = ''                                                        # Processing interval
gfs_ws850c_00z_config     = '_012'                                                    # Configuration string
gfs_ws850c_00z_script     = showcast_dir + '//Scripts//process_gfs_wsd850_sec.py'     # Script to activate
gfs_ws850c_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws850c_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_pwcptc_00z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - PSML / WIND 10 m / CLOUDS / PREC / THICKNESS (500-1000 hPa)

gfs_pwcptc_00z_process    = 1                                                         # Process cicle for this product 
gfs_pwcptc_00z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_pwcptc_00z_identifier = 'gfs.crb.t00z.f120'                                       # Unique string on the file name
gfs_pwcptc_00z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_pwcptc_00z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_pwcptc_00z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_pwcptc_00z_interval   = ''                                                        # Processing interval
gfs_pwcptc_00z_config     = '_013'                                                    # Configuration string
gfs_pwcptc_00z_script     = showcast_dir + '//Scripts//process_gfs_pwcpth_sec.py'     # Script to activate
gfs_pwcptc_00z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_pwcptc_00z') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - 12Z RUN (SET AS TRUE ONLY SAM OR ONLY CRB!)
#######################################################################################################

#------------------------------------------------------------------------------------------------------
gfs_2mtemc_12z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - 2 M TEMPERATURE

gfs_2mtemc_12z_process    = 1                                                         # Process cicle for this product 
gfs_2mtemc_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_2mtemc_12z_identifier = 'gfs.crb.t12z.f120'                                       # Unique string on the file name
gfs_2mtemc_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_2mtemc_12z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_2mtemc_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_2mtemc_12z_interval   = ''                                                        # Processing interval
gfs_2mtemc_12z_config     = '_001'                                                    # Configuration string
gfs_2mtemc_12z_script     = showcast_dir + '//Scripts//process_gfs_2mtemp_sec.py'     # Script to activate
gfs_2mtemc_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_2mtemc_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_accprc_12z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - ACCUMULATED PRECIPITACION 

gfs_accprc_12z_process    = 1                                                         # Process cicle for this product 
gfs_accprc_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_accprc_12z_identifier = 'gfs.crb.t12z.f120'                                       # Unique string on the file name
gfs_accprc_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_accprc_12z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_accprc_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_accprc_12z_interval   = ''                                                        # Processing interval
gfs_accprc_12z_config     = '_002'                                                    # Configuration string
gfs_accprc_12z_script     = showcast_dir + '//Scripts//process_gfs_accpre_sec.py'     # Script to activate
gfs_accprc_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_accprc_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_prtmsc_12z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - PRESSION REDUCED TO MEAN SEA LEVEL

gfs_prtmsc_12z_process    = 1                                                         # Process cicle for this product 
gfs_prtmsc_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_prtmsc_12z_identifier = 'gfs.crb.t12z.f120'                                       # Unique string on the file name
gfs_prtmsc_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_prtmsc_12z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_prtmsc_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_prtmsc_12z_interval   = ''                                                        # Processing interval
gfs_prtmsc_12z_config     = '_003'                                                    # Configuration string
gfs_prtmsc_12z_script     = showcast_dir + '//Scripts//process_gfs_prtmsl_sec.py'     # Script to activate
gfs_prtmsc_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_prtmsc_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_gdindc_12z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - GALVEZ DAVISON INDEX

gfs_gdindc_12z_process    = 1                                                         # Process cicle for this product 
gfs_gdindc_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_gdindc_12z_identifier = 'gfs.crb.t12z.f120'                                       # Unique string on the file name
gfs_gdindc_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_gdindc_12z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_gdindc_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_gdindc_12z_interval   = ''                                                        # Processing interval
gfs_gdindc_12z_config     = '_004'                                                    # Configuration string
gfs_gdindc_12z_script     = showcast_dir + '//Scripts//process_gfs_gdindx_sec.py'     # Script to activate
gfs_gdindc_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_gdindc_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_gh500c_12z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - RELATIVE VORTICITY AND GEOPOTENTIAL HEIGHT 500 hPa

gfs_gh500c_12z_process    = 1                                                         # Process cicle for this product 
gfs_gh500c_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_gh500c_12z_identifier = 'gfs.crb.t12z.f120'                                       # Unique string on the file name
gfs_gh500c_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_gh500c_12z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_gh500c_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_gh500c_12z_interval   = ''                                                        # Processing interval
gfs_gh500c_12z_config     = '_005'                                                    # Configuration string
gfs_gh500c_12z_script     = showcast_dir + '//Scripts//process_gfs_ghv500_sec.py'     # Script to activate
gfs_gh500c_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_gh500c_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_psgwrc_12z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - PSML + GEOP. DIF. (1000-850 hPa) + WINDS (925 hPa) + MEAN RH (1000~400 hPa)

gfs_psgwrc_12z_process    = 1                                                         # Process cicle for this product 
gfs_psgwrc_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_psgwrc_12z_identifier = 'gfs.crb.t12z.f120'                                       # Unique string on the file name
gfs_psgwrc_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_psgwrc_12z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_psgwrc_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_psgwrc_12z_interval   = ''                                                        # Processing interval
gfs_psgwrc_12z_config     = '_006'                                                    # Configuration string
gfs_psgwrc_12z_script     = showcast_dir + '//Scripts//process_gfs_psgwrh_sec.py'     # Script to activate
gfs_psgwrc_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_psgwrc_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_pwcapc_12z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - PRECIPITABLE WATER & CAPE

gfs_pwcapc_12z_process    = 1                                                         # Process cicle for this product 
gfs_pwcapc_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_pwcapc_12z_identifier = 'gfs.crb.t12z.f120'                                       # Unique string on the file name
gfs_pwcapc_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_pwcapc_12z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_pwcapc_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_pwcapc_12z_interval   = ''                                                        # Processing interval
gfs_pwcapc_12z_config     = '_007'                                                    # Configuration string
gfs_pwcapc_12z_script     = showcast_dir + '//Scripts//process_gfs_pwcape_sec.py'     # Script to activate
gfs_pwcapc_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_pwcapc_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_sphclc_12z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - SPECIFIC HUMIDITY > 70% @ 800, 500 & 300 hPa 

gfs_sphclc_12z_process    = 1                                                         # Process cicle for this product 
gfs_sphclc_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_sphclc_12z_identifier = 'gfs.crb.t12z.f120'                                       # Unique string on the file name
gfs_sphclc_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_sphclc_12z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_sphclc_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_sphclc_12z_interval   = ''                                                        # Processing interval
gfs_sphclc_12z_config     = '_008'                                                    # Configuration string
gfs_sphclc_12z_script     = showcast_dir + '//Scripts//process_gfs_sphcld_sec.py'     # Script to activate
gfs_sphclc_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_sphclc_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws200c_12z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - WIND SPEED AND DIRECTION - 200 hPa

gfs_ws200c_12z_process    = 1                                                         # Process cicle for this product 
gfs_ws200c_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws200c_12z_identifier = 'gfs.crb.t12z.f120'                                       # Unique string on the file name
gfs_ws200c_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws200c_12z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws200c_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws200c_12z_interval   = ''                                                        # Processing interval
gfs_ws200c_12z_config     = '_009'                                                    # Configuration string
gfs_ws200c_12z_script     = showcast_dir + '//Scripts//process_gfs_wsd200_sec.py'     # Script to activate
gfs_ws200c_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws200c_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws500c_12z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - WIND SPEED AND DIRECTION - 500 hPa

gfs_ws500c_12z_process    = 1                                                         # Process cicle for this product 
gfs_ws500c_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws500c_12z_identifier = 'gfs.crb.t12z.f120'                                       # Unique string on the file name
gfs_ws500c_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws500c_12z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws500c_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws500c_12z_interval   = ''                                                        # Processing interval
gfs_ws500c_12z_config     = '_010'                                                    # Configuration string
gfs_ws500c_12z_script     = showcast_dir + '//Scripts//process_gfs_wsd500_sec.py'     # Script to activate
gfs_ws500c_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws500c_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws700c_12z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - WIND SPEED AND DIRECTION - 700 hPa

gfs_ws700c_12z_process    = 1                                                         # Process cicle for this product 
gfs_ws700c_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws700c_12z_identifier = 'gfs.crb.t12z.f120'                                       # Unique string on the file name
gfs_ws700c_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws700c_12z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws700c_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws700c_12z_interval   = ''                                                        # Processing interval
gfs_ws700c_12z_config     = '_011'                                                    # Configuration string
gfs_ws700c_12z_script     = showcast_dir + '//Scripts//process_gfs_wsd700_sec.py'     # Script to activate
gfs_ws700c_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws700c_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_ws850c_12z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - WIND SPEED AND DIRECTION - 850 hPa

gfs_ws850c_12z_process    = 1                                                         # Process cicle for this product 
gfs_ws850c_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_ws850c_12z_identifier = 'gfs.crb.t12z.f120'                                       # Unique string on the file name
gfs_ws850c_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_ws850c_12z_extent     = [-119.0, -1.0, -42.0, 37.0]# Max:[-119.0,-1.0,-42.0,37.0] # [min_lon, min_lat, max_lon, max_lat]
gfs_ws850c_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_ws850c_12z_interval   = ''                                                        # Processing interval
gfs_ws850c_12z_config     = '_012'                                                    # Configuration string
gfs_ws850c_12z_script     = showcast_dir + '//Scripts//process_gfs_wsd850_sec.py'     # Script to activate
gfs_ws850c_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_ws850c_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------
gfs_pwcptc_12z            = False # GFS MODEL 0.5 DEGREE - CENTRAL AMERICA + CARIBBEAN - PSML / WIND 10 m / CLOUDS / PREC / THICKNESS (500-1000 hPa)

gfs_pwcptc_12z_process    = 1                                                         # Process cicle for this product 
gfs_pwcptc_12z_directory  = ingest_dir + 'MARN-El Salvador//'                         # Folder where the data is found
gfs_pwcptc_12z_identifier = 'gfs.crb.t12z.f120'                                       # Unique string on the file name
gfs_pwcptc_12z_max_files  = 1                                                         # Max number of historical files to be processed
gfs_pwcptc_12z_extent     = [-88.0, -60.0, -30.0, 8.00]# Max:[-88.0,-60.0,-30.0,8.00] # [min_lon, min_lat, max_lon, max_lat]
gfs_pwcptc_12z_resolution = 4 # Max Res.: N/A                                         # Final plot resolution
gfs_pwcptc_12z_interval   = ''                                                        # Processing interval
gfs_pwcptc_12z_config     = '_013'                                                    # Configuration string
gfs_pwcptc_12z_script     = showcast_dir + '//Scripts//process_gfs_pwcpth_sec.py'     # Script to activate
gfs_pwcptc_12z_output     = showcast_dir + '//Output//'                               # Output folder

products.append('gfs_pwcptc_12z') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# FORECAST CHARTS
#######################################################################################################

#------------------------------------------------------------------------------------------------------
idk_samqpf_sec            = True # QUANTITATIVE PRECIP. FORECASTS FOR DAYS 1-6 (SOUTH AMERICA)

idk_samqpf_sec_process    = 1                                                         # Process cicle for this product 
idk_samqpf_sec_directory  = ingest_dir + 'RANET//'                                    # Folder where the data is found
idk_samqpf_sec_identifier = 'd6.gif'                                                  # Unique string on the file name
idk_samqpf_sec_max_files  = 1                                                         # Max number of historical files to be processed
idk_samqpf_sec_resolution = 0 # Max Res.: N/A                                         # Final plot resolution
idk_samqpf_sec_interval   = ''                                                        # Processing interval
idk_samqpf_sec_config     = ''                                                        # Configuration string
idk_samqpf_sec_script     = showcast_dir + '//Scripts//process_idk_idkqpf_sec.py'     # Script to activate
idk_samqpf_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('idk_samqpf_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
idk_crbqpf_sec            = True # QUANTITATIVE PRECIP. FORECASTS FOR DAYS 1-6 (CENTRAL AMERICA AND CARIBBEAN)

idk_crbqpf_sec_process    = 1                                                         # Process cicle for this product 
idk_crbqpf_sec_directory  = ingest_dir + 'RANET//'                                    # Folder where the data is found
idk_crbqpf_sec_identifier = 'crb3_east.gif'                                           # Unique string on the file name
idk_crbqpf_sec_max_files  = 1                                                         # Max number of historical files to be processed
idk_crbqpf_sec_resolution = 0 # Max Res.: N/A                                         # Final plot resolution
idk_crbqpf_sec_interval   = ''                                                        # Processing interval
idk_crbqpf_sec_config     = ''                                                        # Configuration string
idk_crbqpf_sec_script     = showcast_dir + '//Scripts//process_idk_idkqpf_sec.py'     # Script to activate
idk_crbqpf_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('idk_crbqpf_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# ISCS - INTERNATIONAL SERVICES AND COMMUNICATION SYSTEMS - SUGGESTION: PUT IN A DEDICATED PROCESS
#######################################################################################################

#------------------------------------------------------------------------------------------------------
ics_atrodn_sec            = True # ISCS-ANLZ-CLIMATE - NORTH ATLANTIC AREA

ics_atrodn_sec_process    = 1                                                         # Process cicle for this product 
ics_atrodn_sec_directory  = ingest_dir + 'ISCS-ANLZ-CLIMATE//'                        # Folder where the data is found
ics_atrodn_sec_identifier = '*T_AXNT*'                                                # Unique string on the file name
ics_atrodn_sec_max_files  = 1                                                         # Max number of historical files to be processed
ics_atrodn_sec_resolution = 0 # Max Res.: N/A                                         # Final plot resolution
ics_atrodn_sec_interval   = ''                                                        # Processing interval
ics_atrodn_sec_config     = ''                                                        # Configuration string
ics_atrodn_sec_script     = showcast_dir + '//Scripts//process_isc_atrodn_sec.py'     # Script to activate
ics_atrodn_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('ics_atrodn_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
ics_atrode_sec            = True # ISCS-ANLZ-CLIMATE - EASTERN PACIFIC AREA

ics_atrode_sec_process    = 1                                                         # Process cicle for this product 
ics_atrode_sec_directory  = ingest_dir + 'ISCS-ANLZ-CLIMATE//'                        # Folder where the data is found
ics_atrode_sec_identifier = '*T_AXPZ*'                                                # Unique string on the file name
ics_atrode_sec_max_files  = 1                                                         # Max number of historical files to be processed
ics_atrode_sec_resolution = 0 # Max Res.: N/A                                         # Final plot resolution
ics_atrode_sec_interval   = ''                                                        # Processing interval
ics_atrode_sec_config     = ''                                                        # Configuration string
ics_atrode_sec_script     = showcast_dir + '//Scripts//process_isc_atrode_sec.py'     # Script to activate
ics_atrode_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('ics_atrode_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
ics_ssynop_sec            = True # ISCS-SURFACE - SYNOP

ics_ssynop_sec_process    = 1                                                         # Process cicle for this product 
ics_ssynop_sec_directory  = ingest_dir + 'ISCS-SURFACE//'                             # Folder where the data is found
ics_ssynop_sec_identifier = '*T_SMBO*'                                                # Unique string on the file name
ics_ssynop_sec_max_files  = 1                                                         # Max number of historical files to be processed
ics_ssynop_sec_resolution = 0 # Max Res.: N/A                                         # Final plot resolution
ics_ssynop_sec_interval   = ''                                                        # Processing interval
ics_ssynop_sec_config     = ''                                                        # Configuration string
ics_ssynop_sec_script     = showcast_dir + '//Scripts//process_isc_ssynop_sec.py'     # Script to activate
ics_ssynop_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('ics_ssynop_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
ics_sbuoys_sec            = True # ISCS-SURFACE - DRIFTING BUOYS

ics_sbuoys_sec_process    = 1                                                         # Process cicle for this product 
ics_sbuoys_sec_directory  = ingest_dir + 'ISCS-SURFACE//'                             # Folder where the data is found
ics_sbuoys_sec_identifier = '*T_SSVX*'                                                # Unique string on the file name
ics_sbuoys_sec_max_files  = 1                                                         # Max number of historical files to be processed
ics_sbuoys_sec_resolution = 0 # Max Res.: N/A                                         # Final plot resolution
ics_sbuoys_sec_interval   = ''                                                        # Processing interval
ics_sbuoys_sec_config     = ''                                                        # Configuration string
ics_sbuoys_sec_script     = showcast_dir + '//Scripts//process_isc_sbuoys_sec.py'     # Script to activate
ics_sbuoys_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('ics_sbuoys_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
ics_smetar_sec            = True # ISCS-SURFACE - METAR

ics_smetar_sec_process    = 1                                                         # Process cicle for this product 
ics_smetar_sec_directory  = ingest_dir + 'ISCS-SURFACE//'                             # Folder where the data is found
ics_smetar_sec_identifier = '*T_SAAG*'                                                # Unique string on the file name
ics_smetar_sec_max_files  = 1                                                         # Max number of historical files to be processed
ics_smetar_sec_resolution = 0 # Max Res.: N/A                                         # Final plot resolution
ics_smetar_sec_interval   = ''                                                        # Processing interval
ics_smetar_sec_config     = ''                                                        # Configuration string
ics_smetar_sec_script     = showcast_dir + '//Scripts//process_isc_smetar_sec.py'     # Script to activate
ics_smetar_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('ics_smetar_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
ics_sspeci_sec            = True # ISCS-SURFACE - SPECI

ics_sspeci_sec_process    = 1                                                         # Process cicle for this product 
ics_sspeci_sec_directory  = ingest_dir + 'ISCS-SURFACE//'                             # Folder where the data is found
ics_sspeci_sec_identifier = '*T_SPBZ*'                                                # Unique string on the file name
ics_sspeci_sec_max_files  = 1                                                         # Max number of historical files to be processed
ics_sspeci_sec_resolution = 0 # Max Res.: N/A                                         # Final plot resolution
ics_sspeci_sec_interval   = ''                                                        # Processing interval
ics_sspeci_sec_config     = ''                                                        # Configuration string
ics_sspeci_sec_script     = showcast_dir + '//Scripts//process_isc_sspeci_sec.py'     # Script to activate
ics_sspeci_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('ics_sspeci_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
ics_ftafms_sec            = True # ISCS-FCAST - TAF

ics_ftafms_sec_process    = 1                                                         # Process cicle for this product 
ics_ftafms_sec_directory  = ingest_dir + 'ISCS-FCAST//'                               # Folder where the data is found
ics_ftafms_sec_identifier = '*T_FCAJ*'                                                # Unique string on the file name
ics_ftafms_sec_max_files  = 1                                                         # Max number of historical files to be processed
ics_ftafms_sec_resolution = 0 # Max Res.: N/A                                         # Final plot resolution
ics_ftafms_sec_interval   = ''                                                        # Processing interval
ics_ftafms_sec_config     = ''                                                        # Configuration string
ics_ftafms_sec_script     = showcast_dir + '//Scripts//process_isc_ftafms_sec.py'     # Script to activate
ics_ftafms_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('ics_ftafms_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
ics_wsigme_sec            = True # ISCS-WARN - SIGMETS

ics_wsigme_sec_process    = 1                                                         # Process cicle for this product 
ics_wsigme_sec_directory  = ingest_dir + 'ISCS-WARN//'                                # Folder where the data is found
ics_wsigme_sec_identifier = '*T_WSAG*'                                                # Unique string on the file name
ics_wsigme_sec_max_files  = 1                                                         # Max number of historical files to be processed
ics_wsigme_sec_resolution = 0 # Max Res.: N/A                                         # Final plot resolution
ics_wsigme_sec_interval   = ''                                                         # Processing interval
ics_wsigme_sec_config     = ''                                                        # Configuration string
ics_wsigme_sec_script     = showcast_dir + '//Scripts//process_isc_wsigme_sec.py'     # Script to activate
ics_wsigme_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('ics_wsigme_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
ics_wairme_sec            = True # ISCS-WARN - AIRMETS

ics_wairme_sec_process    = 1                                                         # Process cicle for this product 
ics_wairme_sec_directory  = ingest_dir + 'ISCS-WARN//'                                # Folder where the data is found
ics_wairme_sec_identifier = '*T_WABZ*'                                                # Unique string on the file name
ics_wairme_sec_max_files  = 1                                                         # Max number of historical files to be processed
ics_wairme_sec_resolution = 0 # Max Res.: N/A                                         # Final plot resolution
ics_wairme_sec_interval   = ''                                                        # Processing interval
ics_wairme_sec_config     = ''                                                        # Configuration string
ics_wairme_sec_script     = showcast_dir + '//Scripts//process_isc_wairme_sec.py'     # Script to activate
ics_wairme_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('ics_wairme_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
ics_fvolca_sec            = True # ISCS-FCAST - VOLCANIC ASH

ics_fvolca_sec_process    = 1                                                         # Process cicle for this product 
ics_fvolca_sec_directory  = ingest_dir + 'ISCS-FCAST//'                               # Folder where the data is found
ics_fvolca_sec_identifier = '*T_FVAG*'                                                # Unique string on the file name
ics_fvolca_sec_max_files  = 1                                                         # Max number of historical files to be processed
ics_fvolca_sec_resolution = 0 # Max Res.: N/A                                         # Final plot resolution
ics_fvolca_sec_interval   = ''                                                        # Processing interval
ics_fvolca_sec_config     = ''                                                        # Configuration string
ics_fvolca_sec_script     = showcast_dir + '//Scripts//process_isc_fvolca_sec.py'     # Script to activate
ics_fvolca_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('ics_fvolca_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
ics_wtsuna_sec            = True # ISCS-WARN - TSUNAMI

ics_wtsuna_sec_process    = 1                                                         # Process cicle for this product 
ics_wtsuna_sec_directory  = ingest_dir + 'ISCS-WARN//'                                # Folder where the data is found
ics_wtsuna_sec_identifier = '*T_WE*'                                                  # Unique string on the file name
ics_wtsuna_sec_max_files  = 10                                                        # Max number of historical files to be processed
ics_wtsuna_sec_resolution = 0 # Max Res.: N/A                                         # Final plot resolution
ics_wtsuna_sec_interval   = ''                                                        # Processing interval
ics_wtsuna_sec_config     = ''                                                        # Configuration string
ics_wtsuna_sec_script     = showcast_dir + '//Scripts//process_isc_wtsuna_sec.py'     # Script to activate
ics_wtsuna_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('ics_wtsuna_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
ics_wvolca_sec            = True # ISCS-WARN - VOLCANIC ASH

ics_wvolca_sec_process    = 1                                                         # Process cicle for this product 
ics_wvolca_sec_directory  = ingest_dir + 'ISCS-WARN//'                                # Folder where the data is found
ics_wvolca_sec_identifier = '*T_WVEQ*'                                                # Unique string on the file name
ics_wvolca_sec_max_files  = 1                                                         # Max number of historical files to be processed
ics_wvolca_sec_resolution = 0 # Max Res.: N/A                                         # Final plot resolution
ics_wvolca_sec_interval   = ''                                                        # Processing interval
ics_wvolca_sec_config     = ''                                                        # Configuration string
ics_wvolca_sec_script     = showcast_dir + '//Scripts//process_isc_wvolca_sec.py'     # Script to activate
ics_wvolca_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('ics_wvolca_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# ALWP - ADVECTED LAYERED PRECIPITABLE WATER
#######################################################################################################

#------------------------------------------------------------------------------------------------------
jps_alpw01_sec            = True # ADVECTED LAYER PRECIPITABLE WATER PRODUCT (Sfc - 850 mb)

jps_alpw01_sec_process    = 1                                                             # Process cicle for this product 
jps_alpw01_sec_directory  = ingest_dir + 'CIRA//'                                         # Folder where the data is found
jps_alpw01_sec_identifier = '*ADVECT_COMPOSITE*'                                          # Unique string on the file name
jps_alpw01_sec_max_files  = 1                                                             # Max number of historical files to be processed
jps_alpw01_sec_extent     = [-85.0, -55.0, -24.9, 12.6]# Max:[-180.0,-71.0,180.0,71.0]    # [min_lon, min_lat, max_lon, max_lat]
jps_alpw01_sec_resolution = 8 # Max Res.: N/A                                             # Final plot resolution
jps_alpw01_sec_interval   = ''                                                            # Processing interval
jps_alpw01_sec_config     = '_850'                                                        # Configuration string
jps_alpw01_sec_script     = showcast_dir + '//Scripts//process_jps_alpwat_single_sec.py'  # Script to activate
jps_alpw01_sec_output     = showcast_dir + '//Output//'                                   # Output folder

products.append('jps_alpw01_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
jps_alpw02_sec            = True # ADVECTED LAYER PRECIPITABLE WATER PRODUCT (850 - 700 mb)

jps_alpw02_sec_process    = 1                                                             # Process cicle for this product 
jps_alpw02_sec_directory  = ingest_dir + 'CIRA//'                                         # Folder where the data is found
jps_alpw02_sec_identifier = '*ADVECT_COMPOSITE*'                                          # Unique string on the file name
jps_alpw02_sec_max_files  = 1                                                             # Max number of historical files to be processed
jps_alpw02_sec_extent     = [-85.0, -55.0, -24.9, 12.6]# Max:[-180.0,-71.0,180.0,71.0]    # [min_lon, min_lat, max_lon, max_lat]
jps_alpw02_sec_resolution = 8 # Max Res.: N/A                                             # Final plot resolution
jps_alpw02_sec_interval   = ''                                                            # Processing interval
jps_alpw02_sec_config     = '_700'                                                        # Configuration string
jps_alpw02_sec_script     = showcast_dir + '//Scripts//process_jps_alpwat_single_sec.py'  # Script to activate
jps_alpw02_sec_output     = showcast_dir + '//Output//'                                   # Output folder

products.append('jps_alpw02_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
jps_alpw03_sec            = True # ADVECTED LAYER PRECIPITABLE WATER PRODUCT (700 - 500 mb)

jps_alpw03_sec_process    = 1                                                             # Process cicle for this product 
jps_alpw03_sec_directory  = ingest_dir + 'CIRA//'                                         # Folder where the data is found
jps_alpw03_sec_identifier = '*ADVECT_COMPOSITE*'                                          # Unique string on the file name
jps_alpw03_sec_max_files  = 1                                                             # Max number of historical files to be processed
jps_alpw03_sec_extent     = [-85.0, -55.0, -24.9, 12.6]# Max:[-180.0,-71.0,180.0,71.0]    # [min_lon, min_lat, max_lon, max_lat]
jps_alpw03_sec_resolution = 8 # Max Res.: N/A                                             # Final plot resolution
jps_alpw03_sec_interval   = ''                                                            # Processing interval
jps_alpw03_sec_config     = '_500'                                                        # Configuration string
jps_alpw03_sec_script     = showcast_dir + '//Scripts//process_jps_alpwat_single_sec.py'  # Script to activate
jps_alpw03_sec_output     = showcast_dir + '//Output//'                                   # Output folder

products.append('jps_alpw03_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
jps_alpw04_sec            = True # ADVECTED LAYER PRECIPITABLE WATER PRODUCT (500 - 300 mb)

jps_alpw04_sec_process    = 1                                                             # Process cicle for this product 
jps_alpw04_sec_directory  = ingest_dir + 'CIRA//'                                         # Folder where the data is found
jps_alpw04_sec_identifier = '*ADVECT_COMPOSITE*'                                          # Unique string on the file name
jps_alpw04_sec_max_files  = 1                                                             # Max number of historical files to be processed
jps_alpw04_sec_extent     = [-85.0, -55.0, -24.9, 12.6]# Max:[-180.0,-71.0,180.0,71.0]    # [min_lon, min_lat, max_lon, max_lat]
jps_alpw04_sec_resolution = 8 # Max Res.: N/A                                             # Final plot resolution
jps_alpw04_sec_interval   = ''                                                            # Processing interval
jps_alpw04_sec_config     = '_300'                                                        # Configuration string
jps_alpw04_sec_script     = showcast_dir + '//Scripts//process_jps_alpwat_single_sec.py'  # Script to activate
jps_alpw04_sec_output     = showcast_dir + '//Output//'                                   # Output folder

products.append('jps_alpw04_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# SST - NOAA CORAL REEF WATCH DAILY 5km
#######################################################################################################

#------------------------------------------------------------------------------------------------------
mul_sstcor_sec            = True # SST - NOAA CORAL REEF WATCH DAILY 5km - USER SECTOR

mul_sstcor_sec_process    = 1                                                         # Process cicle for this product 
mul_sstcor_sec_directory  = ingest_dir + 'NOAA-NESDIS//'                              # Folder where the data is found
mul_sstcor_sec_identifier = 'coraltemp*'                                              # Unique string on the file name
mul_sstcor_sec_max_files  = 1                                                         # Max number of historical files to be processed
mul_sstcor_sec_extent     = [-180.0, -70.0, 180.0, 80.0]                              # [min_lon, min_lat, max_lon, max_lat]
mul_sstcor_sec_resolution = 16 # Max Res.: 5 km                                       # Final plot resolution
mul_sstcor_sec_interval   = ''                                                        # Processing interval
mul_sstcor_sec_config     = ''                                                        # Configuration string
mul_sstcor_sec_script     = showcast_dir + '//Scripts//process_sst_coralre_sec.py'    # Script to activate
mul_sstcor_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('mul_sstcor_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# SST ANOMALY - NOAA CORAL REEF WATCH DAILY 5km
#######################################################################################################

#------------------------------------------------------------------------------------------------------
mul_sstano_sec            = True # SST ANOMALY - NOAA CORAL REEF WATCH DAILY 5km - USER SECTOR

mul_sstano_sec_process    = 1                                                         # Process cicle for this product 
mul_sstano_sec_directory  = ingest_dir + 'NOAA-NESDIS//'                              # Folder where the data is found
mul_sstano_sec_identifier = 'ct5km_ssta*'                                             # Unique string on the file name
mul_sstano_sec_max_files  = 1                                                         # Max number of historical files to be processed
mul_sstano_sec_extent     = [-180.0, -70.0, 180.0, 80.0]                              # [min_lon, min_lat, max_lon, max_lat]
mul_sstano_sec_resolution = 16 # Max Res.: 5 km                                       # Final plot resolution
mul_sstano_sec_interval   = ''                                                        # Processing interval
mul_sstano_sec_config     = ''                                                        # Configuration string
mul_sstano_sec_script     = showcast_dir + '//Scripts//process_sst_anomaly_sec.py'    # Script to activate
mul_sstano_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('mul_sstano_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# 7-DAY SST TREND - NOAA CORAL REEF WATCH DAILY 5km
#######################################################################################################

#------------------------------------------------------------------------------------------------------
mul_ssttre_sec            = True # 7-DAY SST TREND - NOAA CORAL REEF WATCH DAILY 5km - USER SECTOR

mul_ssttre_sec_process    = 1                                                         # Process cicle for this product 
mul_ssttre_sec_directory  = ingest_dir + 'NOAA-NESDIS//'                              # Folder where the data is found
mul_ssttre_sec_identifier = 'ct5km_sst-trend-7d*'                                     # Unique string on the file name
mul_ssttre_sec_max_files  = 1                                                         # Max number of historical files to be processed
mul_ssttre_sec_extent     = [-180.0, -70.0, 180.0, 80.0]                              # [min_lon, min_lat, max_lon, max_lat]
mul_ssttre_sec_resolution = 16 # Max Res.: 5 km                                       # Final plot resolution
mul_ssttre_sec_interval   = ''                                                        # Processing interval
mul_ssttre_sec_config     = ''                                                        # Configuration string
mul_ssttre_sec_script     = showcast_dir + '//Scripts//process_sst_7dtrend_sec.py'    # Script to activate
mul_ssttre_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('mul_ssttre_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# NOAA-20 - CHLOROPHYLL-A CONCENTRATION
#######################################################################################################

#------------------------------------------------------------------------------------------------------
jps_ocrgvy_sec            = True # NOAA-20 - CHLOROPHYLL-A CONCENTRATION - REGION VY

jps_ocrgvy_sec_process    = 1                                                         # Process cicle for this product 
jps_ocrgvy_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//OC//'                       # Folder where the data is found
jps_ocrgvy_sec_identifier = 'VR1VCW_*VY*.nc'                                          # Unique string on the file name
jps_ocrgvy_sec_max_files  = 1                                                         # Max number of historical files to be processed
jps_ocrgvy_sec_extent     = [-120.0, 0.0, -60.0, 44.0]# Max:[-120.0, 0.0, -60.0, 44.0]# [min_lon, min_lat, max_lon, max_lat]
jps_ocrgvy_sec_resolution = 4 # Max Res.: 0.750 km                                    # Final plot resolution
jps_ocrgvy_sec_interval   = ''                                                        # Processing interval
jps_ocrgvy_sec_config     = ''                                                        # Configuration string
jps_ocrgvy_sec_script     = showcast_dir + '//Scripts//process_jps_oceanc_sec.py'     # Script to activate
jps_ocrgvy_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('jps_ocrgvy_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
jps_ocrgwy_sec            = True # NOAA-20 - CHLOROPHYLL-A CONCENTRATION - REGION WY

jps_ocrgwy_sec_process    = 1                                                         # Process cicle for this product 
jps_ocrgwy_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//OC//'                       # Folder where the data is found
jps_ocrgwy_sec_identifier = 'VR1VCW_*WY*.nc'                                          # Unique string on the file name
jps_ocrgwy_sec_max_files  = 1                                                         # Max number of historical files to be processed
jps_ocrgwy_sec_extent     = [-60.0, 0.0, 0.0, 44.0]# Max:[-60.0, 0.0, 0.0, 44.0]      # [min_lon, min_lat, max_lon, max_lat]
jps_ocrgwy_sec_resolution = 4 # Max Res.: 0.750 km                                    # Final plot resolution
jps_ocrgwy_sec_interval   = ''                                                        # Processing interval
jps_ocrgwy_sec_config     = ''                                                        # Configuration string
jps_ocrgwy_sec_script     = showcast_dir + '//Scripts//process_jps_oceanc_sec.py'     # Script to activate
jps_ocrgwy_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('jps_ocrgwy_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
jps_ocrgvx_sec            = True # NOAA-20 - CHLOROPHYLL-A CONCENTRATION - REGION VX

jps_ocrgvx_sec_process    = 1                                                         # Process cicle for this product 
jps_ocrgvx_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//OC//'                       # Folder where the data is found
jps_ocrgvx_sec_identifier = 'VR1VCW_*VX*.nc'                                          # Unique string on the file name
jps_ocrgvx_sec_max_files  = 1                                                         # Max number of historical files to be processed
jps_ocrgvx_sec_extent     = [-120, -44.0, -60.0, 0.0]# Max:[-120.0, -44.0, -60.0, 0.0]# [min_lon, min_lat, max_lon, max_lat]
jps_ocrgvx_sec_resolution = 4 # Max Res.: 0.750 km                                    # Final plot resolution
jps_ocrgvx_sec_interval   = ''                                                        # Processing interval
jps_ocrgvx_sec_config     = ''                                                        # Configuration string
jps_ocrgvx_sec_script     = showcast_dir + '//Scripts//process_jps_oceanc_sec.py'     # Script to activate
jps_ocrgvx_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('jps_ocrgvx_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
jps_ocrgwx_sec            = True # NOAA-20 - CHLOROPHYLL-A CONCENTRATION - REGION WX

jps_ocrgwx_sec_process    = 1                                                         # Process cicle for this product 
jps_ocrgwx_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//OC//'                       # Folder where the data is found
jps_ocrgwx_sec_identifier = 'VR1VCW_*WX*.nc'                                          # Unique string on the file name
jps_ocrgwx_sec_max_files  = 1                                                         # Max number of historical files to be processed
jps_ocrgwx_sec_extent     = [-60.0, -44.0, -0.0, 0.0]# Max:[-60.0, -44.0, -0.0, 0.0]  # [min_lon, min_lat, max_lon, max_lat]
jps_ocrgwx_sec_resolution = 4 # Max Res.: 0.750 km                                    # Final plot resolution
jps_ocrgwx_sec_interval   = ''                                                        # Processing interval
jps_ocrgwx_sec_config     = ''                                                        # Configuration string
jps_ocrgwx_sec_script     = showcast_dir + '//Scripts//process_jps_oceanc_sec.py'     # Script to activate
jps_ocrgwx_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('jps_ocrgwx_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
jps_ocrgvw_sec            = True # NOAA-20 - CHLOROPHYLL-A CONCENTRATION - REGION VW

jps_ocrgvw_sec_process    = 1                                                         # Process cicle for this product 
jps_ocrgvw_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//OC//'                       # Folder where the data is found
jps_ocrgvw_sec_identifier = 'VR1VCW_*VW*.nc'                                          # Unique string on the file name
jps_ocrgvw_sec_max_files  = 1                                                         # Max number of historical files to be processed
jps_ocrgvw_sec_extent     = [-120, -89.0, -60.0, -44.0]# Max:[-120, -8.09, -60.0, -44]# [min_lon, min_lat, max_lon, max_lat]
jps_ocrgvw_sec_resolution = 4 # Max Res.: 0.750 km                                    # Final plot resolution
jps_ocrgvw_sec_interval   = ''                                                        # Processing interval
jps_ocrgvw_sec_config     = ''                                                        # Configuration string
jps_ocrgvw_sec_script     = showcast_dir + '//Scripts//process_jps_oceanc_sec.py'     # Script to activate
jps_ocrgvw_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('jps_ocrgvw_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
jps_ocrgwu_sec            = True # NOAA-20 - CHLOROPHYLL-A CONCENTRATION - REGION WU

jps_ocrgwu_sec_process    = 1                                                         # Process cicle for this product 
jps_ocrgwu_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//OC//'                       # Folder where the data is found
jps_ocrgwu_sec_identifier = 'VR1VCW_*WU*.nc'                                          # Unique string on the file name
jps_ocrgwu_sec_max_files  = 1                                                         # Max number of historical files to be processed
jps_ocrgwu_sec_extent     = [-60.0, -89.0, 0.0, -44.0]# Max:[-60.0, -89.0, 0.0, -44.0]# [min_lon, min_lat, max_lon, max_lat]
jps_ocrgwu_sec_resolution = 4 # Max Res.: 0.750 km                                    # Final plot resolution
jps_ocrgwu_sec_interval   = ''                                                        # Processing interval
jps_ocrgwu_sec_config     = ''                                                        # Configuration string
jps_ocrgwu_sec_script     = showcast_dir + '//Scripts//process_jps_oceanc_sec.py'     # Script to activate
jps_ocrgwu_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('jps_ocrgwu_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# JPSS - VIIRS VEGETATION PRODUCTS
#######################################################################################################

#------------------------------------------------------------------------------------------------------
jps_gblgvf_sec            = True # JPSS - GREEN VEGETATION FRACTION - GLOBAL - 4km 

jps_gblgvf_sec_process    = 1                                                         # Process cicle for this product 
jps_gblgvf_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//VEGETATION//'               # Folder where the data is found
jps_gblgvf_sec_identifier = 'GVF-WKL-GLB*.nc'                                         # Unique string on the file name
jps_gblgvf_sec_max_files  = 1                                                         # Max number of historical files to be processed
jps_gblgvf_sec_extent     = [-150.0, -60.0, -20.0, 70.0]# Max:[-180, -80, 180, 80]    # [min_lon, min_lat, max_lon, max_lat]
jps_gblgvf_sec_resolution = 4 # Max Res.: 4 km                                        # Final plot resolution
jps_gblgvf_sec_interval   = ''                                                        # Processing interval
jps_gblgvf_sec_config     = ''                                                        # Configuration string
jps_gblgvf_sec_script     = showcast_dir + '//Scripts//process_jps_gblgvf_sec.py'     # Script to activate
jps_gblgvf_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('jps_gblgvf_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
jps_ndvita_sec            = True # JPSS - NORMALIZED DIFFERENCE VEGETATION INDEX AT TOP OF ATMOSPHERE (TOA) - GLOBAL - 4km 

jps_ndvita_sec_process    = 1                                                         # Process cicle for this product 
jps_ndvita_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//VEGETATION//'               # Folder where the data is found
jps_ndvita_sec_identifier = 'VI-WKL-GLB*.nc'                                          # Unique string on the file name
jps_ndvita_sec_max_files  = 1                                                         # Max number of historical files to be processed
jps_ndvita_sec_extent     = [-150.0, -60.0, -20.0, 70.0]# Max:[-180, -80, 180, 80]    # [min_lon, min_lat, max_lon, max_lat]
jps_ndvita_sec_resolution = 4 # Max Res.: 4 km                                        # Final plot resolution
jps_ndvita_sec_interval   = ''                                                        # Processing interval
jps_ndvita_sec_config     = '_NDA'                                                    # Configuration string
jps_ndvita_sec_script     = showcast_dir + '//Scripts//process_jps_vegidx_sec.py'     # Script to activate
jps_ndvita_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('jps_ndvita_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
jps_ndvitc_sec            = True # JPSS - NORMALIZED DIFFERENCE VEGETATION INDEX AT TOP OF CANOPY (TOC) - GLOBAL - 4km 

jps_ndvitc_sec_process    = 1                                                         # Process cicle for this product 
jps_ndvitc_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//VEGETATION//'               # Folder where the data is found
jps_ndvitc_sec_identifier = 'VI-WKL-GLB*.nc'                                          # Unique string on the file name
jps_ndvitc_sec_max_files  = 1                                                         # Max number of historical files to be processed
jps_ndvitc_sec_extent     = [-150.0, -60.0, -20.0, 70.0]# Max:[-180, -80, 180, 80]    # [min_lon, min_lat, max_lon, max_lat]
jps_ndvitc_sec_resolution = 4 # Max Res.: 4 km                                        # Final plot resolution
jps_ndvitc_sec_interval   = ''                                                        # Processing interval
jps_ndvitc_sec_config     = '_NDC'                                                    # Configuration string
jps_ndvitc_sec_script     = showcast_dir + '//Scripts//process_jps_vegidx_sec.py'     # Script to activate
jps_ndvitc_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('jps_ndvitc_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------
jps_evitoc_sec            = True # JPSS - ENHANCED VEGETATION INDEX AT TOP OF CANOPY (TOC) - GLOBAL - 4km 

jps_evitoc_sec_process    = 1                                                         # Process cicle for this product 
jps_evitoc_sec_directory  = ingest_dir + 'JPSS//PRODUCTS//VEGETATION//'               # Folder where the data is found
jps_evitoc_sec_identifier = 'VI-WKL-GLB*.nc'                                          # Unique string on the file name
jps_evitoc_sec_max_files  = 1                                                         # Max number of historical files to be processed
jps_evitoc_sec_extent     = [-150.0, -60.0, -20.0, 70.0]# Max:[-180, -80, 180, 80]    # [min_lon, min_lat, max_lon, max_lat]
jps_evitoc_sec_resolution = 4 # Max Res.: 4 km                                        # Final plot resolution
jps_evitoc_sec_interval   = ''                                                        # Processing interval
jps_evitoc_sec_config     = '_EVC'                                                    # Configuration string
jps_evitoc_sec_script     = showcast_dir + '//Scripts//process_jps_vegidx_sec.py'     # Script to activate
jps_evitoc_sec_output     = showcast_dir + '//Output//'                               # Output folder

products.append('jps_evitoc_sec') # Add the product to the list
#------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# FILE PROCESSING AND LOG FUNCTION
#######################################################################################################

def procProduct(prod_dir, identifier, config, script, min_lon, min_lat, max_lon, max_lat, resolution, output, vis_dir, interval):

    # Create the list that will store the file names
    gnc_files = []
    
    # Add to the list the files in the dir that matches the identifier
    for filename in sorted(glob.glob(prod_dir+identifier)):
        
        # If the identifier is for a file that doesn't change its name:
        if (identifier ==  'gfs.sam.t00z.f120') or (identifier ==  'gfs.sam.t12z.f120') \
        or (identifier ==  'gfs.crb.t00z.f120') or (identifier ==  'gfs.crb.t12z.f120') \
        or (identifier == 'd6.gif') or (identifier == 'crb3_east.gif'):
            import datetime # Basic Date and Time types
            import pathlib  # Object-oriented filesystem paths
            # Get the file modification time
            mtime = datetime.datetime.fromtimestamp(pathlib.Path(filename).stat().st_mtime).strftime('%Y%m%d%H%M%S')
            gnc_files.append(os.path.normpath(filename + config + '_c' + mtime))
        else: # If the files have unique names 
            gnc_files.append(os.path.normpath(filename + config))
        
        #print("\n")
        #print("PRODDIR: ", prod_dir+identifier)
        #print("PRODNAM: ", filename + config + '_' + mtime) 
        #print("\n")
    
    # Keep on the list only the max number of files
    gnc_files = gnc_files[-max_files:]

    import datetime # Basic Date and Time types
    # If the gnc log file doesn't exist yet, create one
    file = open(showcast_dir + '//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a')
    file.close()

    # Put all file names on the gnc log in a list
    log = []
    with open(showcast_dir + '//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt') as f:
        log = f.readlines()
 
    # Remove the line feeds
    log = [x.strip() for x in log]
 
    # Compare the gnc file list with the log
    # Loop through all the files
    for x in gnc_files:
    # If a file is not on the log, process it
      if x not in log:
          print('Processing the following file:\n', str(x))
          print('Script used:\n', script)
          global prod_count
          prod_count = prod_count + 1
          #print('Command used:\n', script + ' "' + str(x) + '" ' + str(min_lon) + ' ' + str(min_lat) + ' ' + str(max_lon) + ' ' + str(max_lat) + ' ' + str(resolution) + ' ' + output + ' ' + vis_dir + ' ' + interval)
          os.system(script + ' "' + str(x) + '" ' + str(min_lon) + ' ' + str(min_lat) + ' ' + str(max_lon) + ' ' + str(max_lat) + ' ' + str(resolution) + ' ' + output + ' ' + vis_dir + ' ' + interval)
          print('\n')  
          
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

print("\n")
print("############## SHOWCAST MONITOR STARTED ##############")
print("Started at:", datetime.datetime.now())
print("\n")

# Create a counter to identify how many products have been processed in the run
prod_count = 0

# Identifier for channel composites init
config = ''

# Extent init
extent = [0.0, 0.0, 0.0, 0.0]

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

#######################################################################################################
# PROCESSING EACH SELECTED PRODUCT
#######################################################################################################

for product in products: # Loop through products 
    
    process    = globals()[product + "_process"]                                    # Process cicle for this product 
    directory  = globals()[product + "_directory"]                                  # Folder where the data is found
    identifier = globals()[product + "_identifier"]                                 # Unique string on the file name
    max_files  = globals()[product + "_max_files"]                                  # Max number of historical files to be processed
    if (product + "_extent") in globals(): extent = globals()[product + "_extent"]  # [min_lon, min_lat, max_lon, max_lat]
    resolution = globals()[product + "_resolution"]                                 # Final plot resolution
    interval   = globals()[product + "_interval"]                                   # Processing interval
    config     = globals()[product + "_config"]                                     # Configuration string
    output     = globals()[product + "_output"]                                     # Output folder
    script     = python_env + 'python ' + globals()[product + "_script"]            # Script to activate

     
    # Call the processing routine, if the product is set to True and if the product process is equal to the current SHOWCast process
    if (globals()[product] == True) and (globals()[product + "_process"] == showcast_process):
        procProduct(directory, identifier, config, script, extent[0], extent[1], extent[2], extent[3], resolution, output, vis_dir, interval)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

print("\n")
print("##############  SHOWCAST MONITOR ENDED  ##############")
print('Ended at:', datetime.datetime.now())
print('Number of products processed:', prod_count)
print('Total processing time:', round((t.time() - start),2), 'seconds')
print("\n")

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------