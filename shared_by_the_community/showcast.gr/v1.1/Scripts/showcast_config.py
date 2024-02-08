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
# Modified for the needs of HNMS by RMC/LARISSA
# Using MET Satellites
# Last Update: Sep 2020
#######################################################################################################

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Required Libraries
import glob       # Unix style pathname pattern expansion
import os         # Miscellaneous operating system interfaces
import sys        # Import the "system specific parameters and functions" module
import datetime   # Basic Date and Time types
import time as t  # Time access and conversion
import threading
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
start = t.time()  # Start the time counter
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Select the products that will be processed:

#================= Satellite MSG (0.0)       ==========================================================
msg_products = True # Activate/Deactivate METEOSAT Bands and RGB's                           //////////
#------------------------------------------------------------------------------------------------------

msg_fdk = True   # Activate/Deactivate MSG (0.0)  Bands and RGB's - FULL DISK
msg_eu  = True   # Activate/Deactivate MSG (0.0)  Bands and RGB's - EUROPE SECTOR
msg_gr  = True   # Activate/Deactivate MSG (0.0)  Bands and RGB's - GREECE SECTOR

msg_sectors = ''
if (msg_fdk == True): msg_sectors += '_FDK,'
if (msg_eu  == True): msg_sectors += '_EU,'
if (msg_gr  == True): msg_sectors += '_GR'

#================= Satellite MSG (0,9.5E) RSS ==========================================================
msg_RSS_products = True # Activate/Deactivate METEOSAT Bands and RGB's                      ////////////
#-------------------------------------------------------------------------------------------------------

msg_RSS_fdk = False  # Activate/Deactivate MSG (0,9.5E) RSS Bands and RGB's - FULL DISK
msg_RSS_eu  = True   # Activate/Deactivate MSG (0,9.5E) RSS Bands and RGB's - EUROPE SECTOR
msg_RSS_gr  = False  # Activate/Deactivate MSG (0,9.5E) RSS Bands and RGB's - GREECE SECTOR

msg_RSS_sectors = ''
if (msg_RSS_fdk == True): msg_RSS_sectors += '_FDK,'
if (msg_RSS_eu  == True): msg_RSS_sectors += '_EU,'
if (msg_RSS_gr  == True): msg_RSS_sectors += '_GR'


#================= Satellite MSG (0,41.5E) IODC ========================================================
msg_IODC_products = True # Activate/Deactivate METEOSAT Bands and RGB's                    /////////////
#-------------------------------------------------------------------------------------------------------

msg_IODC_fdk = False   # Activate/Deactivate MSG (0,41.5E) IODC Bands and RGB's - FULL DISK
msg_IODC_eu  = False   # Activate/Deactivate MSG (0,41.5E) IODC Bands and RGB's - EUROPE SECTOR
msg_IODC_gr  = True    # Activate/Deactivate MSG (0,41.5E) IODC Bands and RGB's - GREECE SECTOR

msg_IODC_sectors = ''
if (msg_IODC_fdk == True): msg_IODC_sectors += '_FDK,'
if (msg_IODC_eu  == True): msg_IODC_sectors += '_EU,'
if (msg_IODC_gr  == True): msg_IODC_sectors += '_GR'


#=================  METOP GLOBAL SST ===================================================================
mtp_glbsst_glb = True # Activate/Deactivate METOP - Global Sea Surface Temperature
mtp_glbsst_sec = True # Activate/Deactivate METOP - hourly Global Sea Surface Temperature EU
mtp_glbsst_gr  = True  # Activate/Deactivate METOP - hourly Global Sea Surface Temperature GRE

#== WMO IMAGES FROM FOLDER WMO-RA-VI ===================================================================
wmo_ra_vi_folder = True

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# get Python environment from showcast-start.py
python_env = sys.argv[1]

# get Satellite ingestion directory from showcast-start.py
shc_dir = sys.argv[2]

# Max number of unprocessed files the script will process at the same run
max_files = 2
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#######################################################################################################
# FILE PROCESSING AND LOG FUNCTION
#######################################################################################################
def procProduct(prod_dir, identifier, script, min_lon, min_lat, max_lon, max_lat, resolution, satellite="",sectors=""):
    # Create the list that will store the file names
    gnc_files = []

    # Add to the list the files in the dir that matches the identifier
    for filename in sorted(glob.glob(prod_dir + identifier)):
        gnc_files.append(filename)

    # Keep on the list only the max number of files
    gnc_files = gnc_files[-max_files:]

    # If the gnc day log file doesn't exist yet, create one
    file = open('..//Logs//shc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a')
    file.close()

    # Put all file names on the gnc log in a list
    log = []
    with open('..//Logs//shc_log_' + str(datetime.datetime.now())[0:10] + '.txt') as f:
        log = f.readlines()

    # Remove the line feeds
    log = [x.strip() for x in log]

    # Compare the gnc file list with the log
    # Loop through all the files
    for x in gnc_files:
    # If a file is not on the log, process it
        if x not in log:
            print('Processing product:\n', x,"\n")
            print('Script used:\n', script,"\n")
            global prod_count
            prod_count = prod_count + 1
            os.system(script + ' ' + x + ' ' + str(min_lon) + ' ' + str(min_lat) + ' ' + str(max_lon) + ' ' + str(max_lat) + ' ' + str(resolution)+ ' '  + str(satellite)+ ' ' + str(sectors))
            print('\n')

# Run the script wmo_channel_script.py to distribute wmo files
def wmo_distributor():
#    script_wmo = python_env + 'python /var/www/html/SHOWCast.GR_v1/Scripts/wmo_channel_script.py'
    script_wmo = python_env + 'python wmo_channel_script.py'
    os.system(script_wmo)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

print("\n############## SHOWCAST MONITOR STARTED ##############")
print("Started at:", datetime.datetime.now(),"\n")

# Create a counter to identify how many products have been processed in the run
prod_count = 0

# Extent init [-x,-y,x,y]
#extent = [0.0, 0.0, 0.0, 0.0]
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#######################################################################################################
# METEOSAT - 0 Degree (IMAGERY AND RGB'S) - FULL DISK process_msg_channels
#######################################################################################################
if msg_products:
    max_files = 1
    satellite="MSG"
    extent = [0.0, 0.0, 0.0, 0.0]
    resolution = 5 # Max Res.: 3 km
    prod_dir = shc_dir + '/bas/EUMETSAT_Data_Channel_2/'
    identifier = 'H-000-MSG*-EPI______-*'
    script = python_env + 'python process_msg_channels.py'
    th=threading.Thread(target=procProduct,args=(prod_dir, identifier, script, extent[0], extent[1], extent[2], extent[3], resolution, satellite,  msg_sectors))
    th.start()



#####################################################################################################
# METEOSAT - RSS - 9.5 Degrees EAST RSS (IMAGERY AND RGB'S) - FULL DISK
#######################################################################################################
if msg_RSS_products:
    max_files = 1
    satellite="MSG_RSS"
    extent = [0.0, 0.0, 0.0, 0.0]
    resolution = 5 # Max Res.: 3 km
    prod_dir = shc_dir + '/bas/EUMETSAT_Data_Channel_5/'
    identifier = 'H-000-MSG*-EPI______-*'
    script = python_env + 'python process_msg_channels.py'
    th=threading.Thread(target=procProduct,args=(prod_dir, identifier, script, extent[0], extent[1], extent[2], extent[3], resolution, satellite,  msg_RSS_sectors))
    th.start()



#####################################################################################################
# METEOSAT - IODC - 41.5 Degrees EAST (IMAGERY AND RGB'S) - FULL DISK
#######################################################################################################
if msg_IODC_products:
    max_files = 1
    satellite="MSG_IODC"
    extent = [0.0, 0.0, 0.0, 0.0]
    resolution = 5 # Max Res.: 3 km
    prod_dir = shc_dir + '/bas/E1B-GEO-1/'
    identifier = 'H-000-MSG*-EPI______-*'
    script = python_env + 'python process_msg_channels.py'
    th=threading.Thread(target=procProduct,args=(prod_dir, identifier,  script, extent[0], extent[1], extent[2], extent[3], resolution, satellite,  msg_IODC_sectors))
    th.start()



############################################################
# METOP Global Sea Surface Temperature
############################################################
if mtp_glbsst_glb:
    max_files = 1
    extent = [-180.0, -80.0, 180.0, 80.0]
    resolution = 6 # Max Res.: 6 km
    prod_dir = shc_dir + '/bas/E1B-SAF-1/'
    identifier = '*MTOP-GLBSST*'# 2 per day
    script = python_env + 'python process_mtp_sst_fdk.py'
    th=threading.Thread(target=procProduct,args=(prod_dir, identifier, script, extent[0], extent[1], extent[2], extent[3], resolution))
    th.start()

############################################################
# Hourly METOP section  Sea Surface Temperature
############################################################
if mtp_glbsst_sec:
    max_files = 1
    # extent = [-180.0, -80.0, 180.0, 80.0]
    extent = [-60.0, -60.0, 60.0, 60.0]
    resolution = 6 # Max Res.: 6 km
    prod_dir = shc_dir + '/bas/E1B-SAF-1/'
    identifier = 'S-OSI_-FRA_-MSG_-H__SST_FIELD**'# 1 per hour
    script = python_env + 'python process_msg_sst_eur.py'
    th=threading.Thread(target=procProduct,args=(prod_dir, identifier, script, extent[0], extent[1], extent[2], extent[3], resolution))
    th.start()

############################################################
# Hourly METOP Greece section Sea Surface Temperature
############################################################
if mtp_glbsst_gr:
    max_files = 1
#    extent = [-180.0, -80.0, 180.0, 80.0]
    extent = [18, 34, 32, 42]
    resolution = 3 # Max Res.: 6 km
    prod_dir = shc_dir + '/bas/E1B-SAF-1/'
    identifier = 'S-OSI_-FRA_-MSG_-H__SST_FIELD**'# 1 per hour
    script = python_env + 'python process_msg_sst_gr.py'
    th=threading.Thread(target=procProduct,args=(prod_dir, identifier, script, extent[0], extent[1], extent[2], extent[3], resolution))
    th.start()

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

############################################################
# WMO-RA-VI FOLDER IMAGES distribute
############################################################
if wmo_ra_vi_folder:
    th=threading.Thread(target=wmo_distributor)
    th.start()

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

