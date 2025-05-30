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
import pygrib                                                # Provides a high-level interface to the ECWMF ECCODES C library for reading GRIB files
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
import time as t                                             # Time access and conversion
import sys                                                   # Import the "system specific parameters and functions" module
import os                                                    # Miscellaneous operating system interfaces
from os.path import dirname, abspath                         # Return a normalized absolutized version of the pathname path 
from html_update import update                               # Update the HTML animation 
import warnings                                              # Warning control
warnings.filterwarnings("ignore")
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Start the time counter
print('Script started.')
start = t.time()  

# SHOWCast directory:
main_dir = dirname(dirname(abspath(__file__)))

# For logging purposes
path = (sys.argv[1])[:-16]

# If it is for South Americas
if ('d6.gif' in path):

    # Get the other images
    path1 = path[:-5] + '1.gif'
    path2 = path[:-5] + '2.gif'
    path3 = path[:-5] + '3.gif'
    path4 = path[:-5] + '4.gif'
    path5 = path[:-5] + '5.gif'

    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------

    # Product name
    satellite = "IDK"
    product   = "SAMQPF_SEC"
            
    # Create the satellite output directory if it doesn't exist
    out_dir = main_dir + '//Output//' + satellite
    if not os.path.exists(out_dir):
       os.mkdir(out_dir)

    # Create the product output directory if it doesn't exist
    out_dir = main_dir + '//Output//' + satellite + '//' + product + '//'
    if not os.path.exists(out_dir):
       os.mkdir(out_dir)

    #------------------------------------------------------------------------------------------------------

    # Create the satellite output directory if it doesn't exist
    out_dir_html = main_dir + '//HTML//Output//' + satellite
    if not os.path.exists(out_dir_html):
       os.mkdir(out_dir_html)

    # Create the product output directory if it doesn't exist
    out_dir_html = main_dir + '//HTML//Output//' + satellite + '//' + product + '//'
    if not os.path.exists(out_dir_html):
       os.mkdir(out_dir_html)

    #------------------------------------------------------------------------------------------------------

    # Create the satellite output directory if it doesn't exist
    out_dir_quicklooks = main_dir + '//HTML//Output//Quicklooks//'
    if not os.path.exists(out_dir_quicklooks):
       os.mkdir(out_dir_quicklooks)
      
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
            
    from shutil import copyfile

    copyfile(path1, out_dir + 'IDK_SAM001_SEC.gif')
    copyfile(path2, out_dir + 'IDK_SAM002_SEC.gif')
    copyfile(path3, out_dir + 'IDK_SAM003_SEC.gif')
    copyfile(path4, out_dir + 'IDK_SAM004_SEC.gif')
    copyfile(path5, out_dir + 'IDK_SAM005_SEC.gif')
    copyfile(path,  out_dir + 'IDK_SAM006_SEC.gif')

    copyfile(path1, out_dir_html + 'IDK_SAMQPF_SEC_1.gif')
    copyfile(path2, out_dir_html + 'IDK_SAMQPF_SEC_2.gif')
    copyfile(path3, out_dir_html + 'IDK_SAMQPF_SEC_3.gif')
    copyfile(path4, out_dir_html + 'IDK_SAMQPF_SEC_4.gif')
    copyfile(path5, out_dir_html + 'IDK_SAMQPF_SEC_5.gif')
    copyfile(path,  out_dir_html + 'IDK_SAMQPF_SEC_6.gif')

    copyfile(path1, out_dir_quicklooks + 'IDK_SAM001_SEC_quicklook.png')
    copyfile(path2, out_dir_quicklooks + 'IDK_SAM002_SEC_quicklook.png')
    copyfile(path3, out_dir_quicklooks + 'IDK_SAM003_SEC_quicklook.png')
    copyfile(path4, out_dir_quicklooks + 'IDK_SAM004_SEC_quicklook.png')
    copyfile(path5, out_dir_quicklooks + 'IDK_SAM005_SEC_quicklook.png')
    copyfile(path,  out_dir_quicklooks + 'IDK_SAM006_SEC_quicklook.png')

else: # If it is for Caribbean
    print("Caribbean")
    
    path1 = path.replace('crb3_','crb1_')
    path2 = path.replace('crb3_','crb2_')
    path3 = path
    
    path4 = path1.replace('_east','_central')
    path5 = path2.replace('_east','_central')
    path6 = path3.replace('_east','_central')

    path7 = path1.replace('_east','_west')
    path8 = path2.replace('_east','_west')
    path9 = path3.replace('_east','_west')

    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------

    # Product name
    satellite = "IDK"
    product   = "CRWQPF_SEC"
            
    # Create the satellite output directory if it doesn't exist
    out_dir = main_dir + '//Output//' + satellite
    if not os.path.exists(out_dir):
       os.mkdir(out_dir)

    # Create the product output directory if it doesn't exist
    out_dir = main_dir + '//Output//' + satellite + '//' + product + '//'
    if not os.path.exists(out_dir):
       os.mkdir(out_dir)

    #------------------------------------------------------------------------------------------------------

    # Create the satellite output directory if it doesn't exist
    out_dir_html = main_dir + '//HTML//Output//' + satellite
    if not os.path.exists(out_dir_html):
       os.mkdir(out_dir_html)

    # Create the product output directory if it doesn't exist
    out_dir_html = main_dir + '//HTML//Output//' + satellite + '//' + product + '//'
    if not os.path.exists(out_dir_html):
       os.mkdir(out_dir_html)

    #------------------------------------------------------------------------------------------------------

    # Create the satellite output directory if it doesn't exist
    out_dir_quicklooks = main_dir + '//HTML//Output//Quicklooks//'
    if not os.path.exists(out_dir_quicklooks):
       os.mkdir(out_dir_quicklooks)
      
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    

    from shutil import copyfile

    copyfile(path7, out_dir + 'IDK_CRW001_SEC.gif')
    copyfile(path8, out_dir + 'IDK_CRW002_SEC.gif')
    copyfile(path9, out_dir + 'IDK_CRW003_SEC.gif')

    copyfile(path7, out_dir_html + 'IDK_CRWQPF_SEC_1.gif')
    copyfile(path8, out_dir_html + 'IDK_CRWQPF_SEC_2.gif')
    copyfile(path9, out_dir_html + 'IDK_CRWQPF_SEC_3.gif')

    copyfile(path7, out_dir_quicklooks + 'IDK_CRW01W_SEC_quicklook.png')
    copyfile(path8, out_dir_quicklooks + 'IDK_CRW02W_SEC_quicklook.png')
    copyfile(path9, out_dir_quicklooks + 'IDK_CRW03W_SEC_quicklook.png')

    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    

    # Product name
    satellite = "IDK"
    product   = "CRCQPF_SEC"
            
    # Create the satellite output directory if it doesn't exist
    out_dir = main_dir + '//Output//' + satellite
    if not os.path.exists(out_dir):
       os.mkdir(out_dir)

    # Create the product output directory if it doesn't exist
    out_dir = main_dir + '//Output//' + satellite + '//' + product + '//'
    if not os.path.exists(out_dir):
       os.mkdir(out_dir)

    #------------------------------------------------------------------------------------------------------

    # Create the satellite output directory if it doesn't exist
    out_dir_html = main_dir + '//HTML//Output//' + satellite
    if not os.path.exists(out_dir_html):
       os.mkdir(out_dir_html)

    # Create the product output directory if it doesn't exist
    out_dir_html = main_dir + '//HTML//Output//' + satellite + '//' + product + '//'
    if not os.path.exists(out_dir_html):
       os.mkdir(out_dir_html)

    #------------------------------------------------------------------------------------------------------

    # Create the satellite output directory if it doesn't exist
    out_dir_quicklooks = main_dir + '//HTML//Output//Quicklooks//'
    if not os.path.exists(out_dir_quicklooks):
       os.mkdir(out_dir_quicklooks)
      
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    

    from shutil import copyfile

    copyfile(path4, out_dir + 'IDK_CRC001_SEC.gif')
    copyfile(path5, out_dir + 'IDK_CRC002_SEC.gif')
    copyfile(path6, out_dir + 'IDK_CRC003_SEC.gif')

    copyfile(path4, out_dir_html + 'IDK_CRCQPF_SEC_1.gif')
    copyfile(path5, out_dir_html + 'IDK_CRCQPF_SEC_2.gif')
    copyfile(path6, out_dir_html + 'IDK_CRCQPF_SEC_3.gif')

    copyfile(path4, out_dir_quicklooks + 'IDK_CRC01C_SEC_quicklook.png')
    copyfile(path5, out_dir_quicklooks + 'IDK_CRC02C_SEC_quicklook.png')
    copyfile(path6, out_dir_quicklooks + 'IDK_CRC03C_SEC_quicklook.png')

    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------ 

    # Product name
    satellite = "IDK"
    product   = "CREQPF_SEC"
            
    # Create the satellite output directory if it doesn't exist
    out_dir = main_dir + '//Output//' + satellite
    if not os.path.exists(out_dir):
       os.mkdir(out_dir)

    # Create the product output directory if it doesn't exist
    out_dir = main_dir + '//Output//' + satellite + '//' + product + '//'
    if not os.path.exists(out_dir):
       os.mkdir(out_dir)

    #------------------------------------------------------------------------------------------------------

    # Create the satellite output directory if it doesn't exist
    out_dir_html = main_dir + '//HTML//Output//' + satellite
    if not os.path.exists(out_dir_html):
       os.mkdir(out_dir_html)

    # Create the product output directory if it doesn't exist
    out_dir_html = main_dir + '//HTML//Output//' + satellite + '//' + product + '//'
    if not os.path.exists(out_dir_html):
       os.mkdir(out_dir_html)

    #------------------------------------------------------------------------------------------------------

    # Create the satellite output directory if it doesn't exist
    out_dir_quicklooks = main_dir + '//HTML//Output//Quicklooks//'
    if not os.path.exists(out_dir_quicklooks):
       os.mkdir(out_dir_quicklooks)
      
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    

    from shutil import copyfile

    copyfile(path1, out_dir + 'IDK_CRE001_SEC.gif')
    copyfile(path2, out_dir + 'IDK_CRE002_SEC.gif')
    copyfile(path3, out_dir + 'IDK_CRE003_SEC.gif')

    copyfile(path1, out_dir_html + 'IDK_CREQPF_SEC_1.gif')
    copyfile(path2, out_dir_html + 'IDK_CREQPF_SEC_2.gif')
    copyfile(path3, out_dir_html + 'IDK_CREQPF_SEC_3.gif')

    copyfile(path1, out_dir_quicklooks + 'IDK_CRE01E_SEC_quicklook.png')
    copyfile(path2, out_dir_quicklooks + 'IDK_CRE02E_SEC_quicklook.png')
    copyfile(path3, out_dir_quicklooks + 'IDK_CRE03E_SEC_quicklook.png')

    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------ 
    
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Put the processed file on the log
import datetime # Basic Date and Time types
import pathlib  # Object-oriented filesystem paths
# Get the file modification time
mtime = datetime.datetime.fromtimestamp(pathlib.Path(path).stat().st_mtime).strftime('%Y%m%d%H%M%S')
# Write to the log
with open(main_dir + '//Logs//gnc_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
    log.write(str(datetime.datetime.now()))
    log.write('\n')
    log.write(path + '_c' + mtime + '\n')
    log.write('\n')

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Total processing time
print('Total processing time:', round((t.time() - start),2), 'seconds.') 
