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
"""
INSTRUCTIONS FOR USERS:

1-) On the "ingest_folder" variable, choose the main folder where the data will be downloaded.

2-) On BUCKETS, choose the satellites you want to download data from (noaa-goes16 or noaa-goes17) 

3-) For each product on the product list, choose:

	- First line: If the product should be downloaded (True) or not (False).

	- Second line: AWS product name (don't change it!)

	- Third line: Which channels should be downloaded for each selected "True" product. The products that 
	  has 'False' on the channels list, are not channel based.

	- Third line (for MESOSCALE only): Which mesoscale sector(s) you wanto to download. 

	- Fourth line: Which minutes (scans) should be downloaded for each selected "True" product. The default 
	  options are the ones available for each product. For example the "SST" is an hourly product, so only 
	  the option '00' is available for it.

	- Fifth line: The folder you want to store your data. In the end, data will be stored on:
	  ingest_folder + product folder + Band (if the product is channel based)
	  Note: The default folder names are just suggestions. Change it to any name you want / need.
	  Also, when downloading GOES-17 data, the folder name will be changed to "GOES-S" instead of "GOES-R"

4-) On the UTC_DIFF variable, insert how many hours you are behind (-) or ahead (+) UTC.
	If your machine time / date is already configured for UTC, leave it as 0 (zero).
	
IMPORTANT: This script was created for the SHOWCast utility, however it might be used as a standalone script
By default, it assumes it is inside a folder called "Cloud" and inside this "Cloud" folder you must have a 
"Logs" folder and an "Apps" folder, with the Rclone software in it. To download Rclone, please access:
https://rclone.org/downloads/	

Note: If you want to use this script to download historical data, just manually change YEAR, JULIAN DAY and 
HOUR, keeping UTC_DIFF as 0 (zero).
"""
__author__ = "Diego Souza"
__copyright__ = "Copyright (C) 2021 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL"
__credits__ = ["Diego Souza"]
__license__ = "GPL"
__version__ = "2.2.1"
__maintainer__ = "Diego Souza"
__email__ = "diego.souza@inpe.br"
__status__ = "Production"
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Required modules
#------------------------------------------------------------------------------------------------------
import os           					# Miscellaneous operating system interfaces
import subprocess   					# The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
import datetime     					# Basic date and time types
import platform     					# Access to underlying platform’s identifying data
import time as t    					# Time access and conversion
import re           					# Regular expression operations
from os.path import dirname, abspath    # Return a normalized absolutized version of the pathname path 

from siphon.catalog import TDSCatalog   # Code to support reading and parsing catalog files from a THREDDS Data Server (TDS)
import urllib.request                   # Defines functions and classes which help in opening URLs
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()  

# Main ingest folder - Where your downloaded data will be stored
ingest_folder = "C://VLAB//Cloud//"       # Windows example
#ingest_folder = "//data//VLAB//Cloud//"  # Linux example

#------------------------------------------------------------------------------------------------------
# PRODUCT SELECTION BY USER
#------------------------------------------------------------------------------------------------------

# Select the desired bucket, in this case, the satellite(s)
SATELLITES = ['goes16'] # Choose from ['goes16', 'goes17'] or both
PLATFORM = ['GRB16'] # Choose from ['GRB16', 'GRB17'] or both

#------------------------------------------------------------------------------------------------------
# ABI L1B BANDS
#------------------------------------------------------------------------------------------------------

# ABI L1b Radiances - CONUS
ABI_L1b_RadC          = False 
ABI_L1b_RadC_Dataset  = 'ABI'
ABI_L1b_RadC_Sector   = 'CONUS'
ABI_L1b_RadC_Channel  = ['Channel01', 'Channel02', 'Channel03', 'Channel04', 'Channel05', 'Channel06', 'Channel07', 'Channel08', 'Channel09', 'Channel10', 'Channel11', 'Channel12', 'Channel13', 'Channel14', 'Channel15', 'Channel16']
ABI_L1b_RadC_Minutes  = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L1b_RadC_Folders  = 'GOES-R-RadC-Imagery//'

# ABI L1b Radiances - FULL DISK
ABI_L1b_RadF         = True 
ABI_L1b_RadF_Dataset = 'ABI'
ABI_L1b_RadF_Sector  = 'FullDisk'
ABI_L1b_RadF_Channel = ['Channel01', 'Channel03', 'Channel04', 'Channel05', 'Channel06', 'Channel07', 'Channel08', 'Channel09', 'Channel10', 'Channel11', 'Channel12', 'Channel13', 'Channel14', 'Channel15', 'Channel16']
ABI_L1b_RadF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L1b_RadF_Folders = 'GOES-R-RadF-Imagery//'

# ABI L1b Radiances - MESOSCALE 1
ABI_L1b_RadM1         = False 
ABI_L1b_RadM1_Dataset = 'ABI'
ABI_L1b_RadM1_Sector  = 'Mesoscale-1'
ABI_L1b_RadM1_Channel = ['Channel01', 'Channel02', 'Channel03', 'Channel04', 'Channel05', 'Channel06', 'Channel07', 'Channel08', 'Channel09', 'Channel10', 'Channel11', 'Channel12', 'Channel13', 'Channel14', 'Channel15', 'Channel16']
ABI_L1b_RadM1_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
ABI_L1b_RadM1_Folders = 'GOES-R-RadM-Imagery//'

# ABI L1b Radiances - MESOSCALE 2
ABI_L1b_RadM2         = False 
ABI_L1b_RadM2_Dataset = 'ABI'
ABI_L1b_RadM2_Sector  = 'Mesoscale-2'
ABI_L1b_RadM2_Channel = ['Channel01', 'Channel02', 'Channel03', 'Channel04', 'Channel05', 'Channel06', 'Channel07', 'Channel08', 'Channel09', 'Channel10', 'Channel11', 'Channel12', 'Channel13', 'Channel14', 'Channel15', 'Channel16']
ABI_L1b_RadM2_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
ABI_L1b_RadM2_Folders = 'GOES-R-RadM-Imagery//'

#------------------------------------------------------------------------------------------------------
# PRODUCT SELECTION END
#------------------------------------------------------------------------------------------------------

# Variable that will store the desired products
PRODUCTS = []

# DO NOT CHANGE the lines below
if (ABI_L1b_RadC == True): PRODUCTS.append('ABI_L1b_RadC')
if (ABI_L1b_RadF == True): PRODUCTS.append('ABI_L1b_RadF')
if (ABI_L1b_RadM1 == True): PRODUCTS.append('ABI_L1b_RadM1')
if (ABI_L1b_RadM2 == True): PRODUCTS.append('ABI_L1b_RadM2')

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# SHOWCast directory:
main_dir = dirname(dirname(dirname(abspath(__file__))))

print ("") 
print ("--------------------------------------------------------") 
print ("GOES-R UNIDATA THREDDS Downloader: Current Data")
print ("--------------------------------------------------------") 
print ("") 

date = 'current'
''' NOT NECESSARY TO DETECT TIME AND DATE - UNIDATA HAS A "CURRENT" FOLDER
#------------------------------------------------------------------------------------------------------
# GETTING CURRENT TIME AND DATE
#------------------------------------------------------------------------------------------------------
# Checking the current time and date based on your machine local time.
# Note: We could use an online time server, however ntp servers access is restricted in some networks.  
# You may use ntp servers if you wish.

UTC_DIFF = -3 # How many hours you are behind (-) or ahead (+) UTC. If your machine is already on UTC, leave it as 0 (zero). 

YEAR = str(datetime.datetime.now().year)                      # Year got from local machine
JULIAN_DAY = str(datetime.datetime.now().timetuple().tm_yday) # Julian day got from local machine
HOUR = str(datetime.datetime.now().hour - UTC_DIFF).zfill(2)  # Hour got from local machine corrected for UTC

# Checking if it is a leap year
import calendar
if (calendar.isleap(int(YEAR)) == True):
	last_day = 366 # if it is a leap year, the last julian day is 366
else:
	last_day = 365 # if it is NOT a leap year, the last julian day is 365

# Correcting HOUR and JULIAN DAY, if you are not UTC. If you are on UTC, nothing will be done
if (int(HOUR) > 23):
	if (int(JULIAN_DAY) >= last_day):
		YEAR = str(int(YEAR) + 1)
	HOUR = str(int(HOUR) - 24).zfill(2)
	JULIAN_DAY = str(int(JULIAN_DAY) + 1)

# Printing Time and Data information for user check
print("Current year, julian day and hour based on your local machine:")
print("YEAR: ", YEAR)
print("JULIAN DAY (LOCAL): ", str(datetime.datetime.now().timetuple().tm_yday))
print("JULIAN DAY (UTC): ", JULIAN_DAY)
print("HOUR (LOCAL): ", str(datetime.datetime.now().hour))
print("HOUR (UTC): ", HOUR)
print("")
'''
#------------------------------------------------------------------------------------------------------
# DATA DOWNLOAD LOOP
#------------------------------------------------------------------------------------------------------

# Unidate THREDDS Data Server Catalog URL
base_cat_url = 'https://thredds-test.unidata.ucar.edu/thredds/catalog/satellite/{satellite}/{platform}/{dataset}/{sector}/{channel}/{date}/catalog.xml'
 
for satellite in SATELLITES: # Loop through satellites 

	if (satellite == 'goes16'):
		platform = 'GRB16'
	elif (satellite == 'goes17'):
		platform = 'GRB17'
	
	for product in PRODUCTS: # Loop through products 

		DATASET = globals()[product + "_Dataset"]
		SECTOR = globals()[product + "_Sector"]
		CHANNEL = globals()[product + "_Channel"]
		MINUTES = globals()[product + "_Minutes"]
		OUTDIR  = ingest_folder + globals()[product + "_Folders"]
		
		#print(satellite)
		#print(DATASET)
		#print(SECTOR)
		#print(CHANNEL)
		#print(MINUTES)
		#print(OUTDIR)
			
		for channel in CHANNEL:
		
			OUTDIR = ingest_folder + globals()[product + "_Folders"] + 'Band' + channel[-2:] + '//'
			if not os.path.exists(OUTDIR):
				os.makedirs(OUTDIR, exist_ok=True)
			
			# Get output from rclone command, based on the desired data
			print ("--------------------------------------------------------") 
			print ("")
			print("Command used:")
			
			cat_url = base_cat_url.format(satellite = satellite, platform = platform, dataset = DATASET, sector = SECTOR, date = date, channel=channel)
			print(cat_url)
			
			# Access the catalog
			cat = TDSCatalog(cat_url)
			# Get the latest dataset available
			ds = cat.datasets[-1]
						
			print("")
			print("File Name: ", ds)
			print("")		
			print("Checking if the file is on the daily log...")
			# If the log file doesn't exist yet, create one
			file = open(main_dir + '//Cloud//Logs//' + 'grb_unidata_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a')
			file.close()
			# Put all file names on the log in a list
			log = []
			
			# Open the log to check the files already processed 
			with open(main_dir + '//Cloud//Logs//' + 'grb_unidata_log_' + str(datetime.datetime.now())[0:10] + '.txt') as f:
				log = f.readlines()
				# Remove the line feeds
				log = [x.strip() for x in log]
			
			# If a given file is not on the log
			if ds not in log:
				print("")
				print ("Checking if the file is from a desired minute...")
			
				# Search in the file name if the image from GOES is from a desired minute.
				matches = 0 # Initialize matches
				for minute in MINUTES: 
					#print(minute)
					#print(r'(?:s.........' + str(minute) + ')..._')
					regex = re.compile(r'(?:s.........' + str(minute) + ')..._')
					finder = re.findall(regex, str(ds))
					# If "matches" is "0", it is not from a desired minute. If it is "1", we may download the file
					matches = len(finder)
					#print(matches)
					# If it is from a desired minute, exit verification loop
					if (matches == 1): break
					
				if matches == 0: # If there are no matches
					print("This is not an image from a desired minute... Exiting loop.")
					# Put the processed file on the log
					import datetime   # Basic Date and Time types
					with open(main_dir + '//Cloud//Logs//' + 'grb_unidata_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
						log.write(str(datetime.datetime.now()))
						log.write('\n')
						log.write(ds + '\n')
						log.write('\n')
					break # This is not an image from minute 20 or 50. Exiting the loop.
				else:
					print ("")
					print ("Downloading the most recent file for channel: ", channel)
					
					# Get the URL
					url = ds.access_urls['HTTPServer']
					# Download the most recent file for this particular hour
					urllib.request.urlretrieve(url, OUTDIR + str(ds))					
					print ("")
					print ("Download finished!") 
					print ("Putting the file name on the daily log...")
					print("")

					#---------------------------------------------------------------------------------------------
					#---------------------------------------------------------------------------------------------
		
					# Put the processed file on the log
					import datetime   # Basic Date and Time types
					with open(main_dir + '//Cloud//Logs//' + 'grb_unidata_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
						log.write(str(datetime.datetime.now()))
						log.write('\n')
						log.write(str(ds) + '\n')
						log.write('\n')
			
			else:
				print("This file was already downloaded.")
				print("")			

#------------------------------------------------------------------------------------------------------
# SCRIPT END
#------------------------------------------------------------------------------------------------------

print('Total processing time:', round((t.time() - start),2), 'seconds.') 
