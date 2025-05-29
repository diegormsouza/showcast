#######################################################################################################
# LICENSE
# Copyright (C) 2025 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL
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
__copyright__ = "Copyright (C) 2025 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL"
__credits__ = ["Diego Souza"]
__license__ = "GPL"
__version__ = "2.5.2"
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

print(path)
# If it is for South Americas
if ('d1.gif' in path):

    # Get the other images
    path1 = path[:-5] + '1.gif'
    path2 = path[:-5] + '2.gif'
    path3 = path[:-5] + '3.gif'

    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------

    # Product name
    satellite = "IDK"
    product   = "SAMQPF_SEC"
            
    # Create the satellite output directory if it doesn't exist
    out_dir = (sys.argv[7]) + satellite
    if not os.path.exists(out_dir):
       os.mkdir(out_dir)

    # Create the product output directory if it doesn't exist
    out_dir = (sys.argv[7]) + satellite + '//' + product + '//'
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
    from PIL.WebPImagePlugin import Image

    copyfile(path1, out_dir + 'IDK_SAM001_SEC.gif')   
    copyfile(path2, out_dir + 'IDK_SAM002_SEC.gif')
    copyfile(path3, out_dir + 'IDK_SAM003_SEC.gif')
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------

    copyfile(path1, out_dir_html + 'IDK_SAMQPF_SEC_1.gif')
    copyfile(path2, out_dir_html + 'IDK_SAMQPF_SEC_2.gif')
    copyfile(path3, out_dir_html + 'IDK_SAMQPF_SEC_3.gif')

    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------

    copyfile(path1, out_dir_quicklooks + 'IDK_SAM001_SEC_quicklook.png')
    copyfile(path2, out_dir_quicklooks + 'IDK_SAM002_SEC_quicklook.png')
    copyfile(path3, out_dir_quicklooks + 'IDK_SAM003_SEC_quicklook.png')

    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    
    # Convert to webp
    im = Image.open(out_dir + 'IDK_SAM001_SEC.gif')
    im.save(out_dir + 'IDK_SAM001_SEC.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir + 'IDK_SAM002_SEC.gif')
    im.save(out_dir + 'IDK_SAM002_SEC.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir + 'IDK_SAM003_SEC.gif')
    im.save(out_dir + 'IDK_SAM003_SEC.webp', format = "WebP", lossless = True)
    im.close()

    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    
    # Convert to webp
    im = Image.open(out_dir_quicklooks + 'IDK_SAM001_SEC_quicklook.png')
    im.save(out_dir_quicklooks + 'IDK_SAM001_SEC_quicklook.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_quicklooks + 'IDK_SAM002_SEC_quicklook.png')
    im.save(out_dir_quicklooks + 'IDK_SAM002_SEC_quicklook.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_quicklooks + 'IDK_SAM003_SEC_quicklook.png')
    im.save(out_dir_quicklooks + 'IDK_SAM003_SEC_quicklook.webp', format = "WebP", lossless = True)
    im.close()
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    
    os.remove(out_dir + 'IDK_SAM001_SEC.gif') 
    os.remove(out_dir + 'IDK_SAM002_SEC.gif')        
    os.remove(out_dir + 'IDK_SAM003_SEC.gif')

    os.remove(out_dir_html + 'IDK_SAMQPF_SEC_1.gif')
    os.remove(out_dir_html + 'IDK_SAMQPF_SEC_2.gif')   
    os.remove(out_dir_html + 'IDK_SAMQPF_SEC_3.gif')

    os.remove(out_dir_quicklooks + 'IDK_SAM001_SEC_quicklook.png')
    os.remove(out_dir_quicklooks + 'IDK_SAM002_SEC_quicklook.png')    
    os.remove(out_dir_quicklooks + 'IDK_SAM003_SEC_quicklook.png')
    
elif ('crb1.gif' in path):
    print("Central America + Caribbean Forecast - QPF and 850 HPA Winds")
    
    # Get the other images
    path1 = path[:-5] + '1.gif'
    path2 = path[:-5] + '2.gif'
    path3 = path[:-5] + '3.gif'

    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------

    # Product name
    satellite = "IDK"
    product   = "CRWQPF_SEC"
            
    # Create the satellite output directory if it doesn't exist
    out_dir = (sys.argv[7]) + satellite
    if not os.path.exists(out_dir):
       os.mkdir(out_dir)

    # Create the product output directory if it doesn't exist
    out_dir = (sys.argv[7]) + satellite + '//' + product + '//'
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
    from PIL.WebPImagePlugin import Image
    
    copyfile(path1, out_dir + 'IDK_CRW001_SEC.gif')
    copyfile(path2, out_dir + 'IDK_CRW002_SEC.gif')
    copyfile(path3, out_dir + 'IDK_CRW003_SEC.gif')

    copyfile(path1, out_dir_html + 'IDK_CRWQPF_SEC_1.gif')
    copyfile(path2, out_dir_html + 'IDK_CRWQPF_SEC_2.gif')
    copyfile(path3, out_dir_html + 'IDK_CRWQPF_SEC_3.gif')

    copyfile(path1, out_dir_quicklooks + 'IDK_CRW01W_SEC_quicklook.png')
    copyfile(path2, out_dir_quicklooks + 'IDK_CRW02W_SEC_quicklook.png')
    copyfile(path3, out_dir_quicklooks + 'IDK_CRW03W_SEC_quicklook.png')
    
    # Convert to webp
    im = Image.open(out_dir + 'IDK_CRW001_SEC.gif')
    im.save(out_dir + 'IDK_CRW001_SEC.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir + 'IDK_CRW002_SEC.gif')
    im.save(out_dir + 'IDK_CRW002_SEC.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir + 'IDK_CRW003_SEC.gif')
    im.save(out_dir + 'IDK_CRW003_SEC.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_html + 'IDK_CRWQPF_SEC_1.gif')
    im.save(out_dir_html + 'IDK_CRWQPF_SEC_1.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_html + 'IDK_CRWQPF_SEC_2.gif')
    im.save(out_dir_html + 'IDK_CRWQPF_SEC_2.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_html + 'IDK_CRWQPF_SEC_3.gif')
    im.save(out_dir_html + 'IDK_CRWQPF_SEC_3.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_quicklooks + 'IDK_CRW01W_SEC_quicklook.png')
    im.save(out_dir_quicklooks + 'IDK_CRW01W_SEC_quicklook.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_quicklooks + 'IDK_CRW02W_SEC_quicklook.png')
    im.save(out_dir_quicklooks + 'IDK_CRW02W_SEC_quicklook.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_quicklooks + 'IDK_CRW03W_SEC_quicklook.png')
    im.save(out_dir_quicklooks + 'IDK_CRW03W_SEC_quicklook.webp', format = "WebP", lossless = True)
    im.close()
    
    os.remove(out_dir + 'IDK_CRW001_SEC.gif') 
    os.remove(out_dir + 'IDK_CRW002_SEC.gif')        
    os.remove(out_dir + 'IDK_CRW003_SEC.gif')

    os.remove(out_dir_html + 'IDK_CRWQPF_SEC_1.gif')
    os.remove(out_dir_html + 'IDK_CRWQPF_SEC_2.gif')   
    os.remove(out_dir_html + 'IDK_CRWQPF_SEC_3.gif')

    os.remove(out_dir_quicklooks + 'IDK_CRW01W_SEC_quicklook.png')
    os.remove(out_dir_quicklooks + 'IDK_CRW02W_SEC_quicklook.png')    
    os.remove(out_dir_quicklooks + 'IDK_CRW03W_SEC_quicklook.png')
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    

elif ('westcrb_00.gif' in path):
    print("West Caribbean Surface Analysis")
    
    # Get the other images
    path1 = path[:-6] + '00.gif'
    path2 = path[:-6] + '06.gif'
    path3 = path[:-6] + '12.gif'
    path4 = path[:-6] + '18.gif'

    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------

    # Product name
    satellite = "IDK"
    product   = "WECSUR_SEC"
            
    # Create the satellite output directory if it doesn't exist
    out_dir = (sys.argv[7]) + satellite
    if not os.path.exists(out_dir):
       os.mkdir(out_dir)

    # Create the product output directory if it doesn't exist
    out_dir = (sys.argv[7]) + satellite + '//' + product + '//'
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
    from PIL.WebPImagePlugin import Image
    
    copyfile(path1, out_dir + 'IDK_WEC000_SEC.gif')
    copyfile(path2, out_dir + 'IDK_WEC006_SEC.gif')
    copyfile(path3, out_dir + 'IDK_WEC012_SEC.gif')
    copyfile(path3, out_dir + 'IDK_WEC018_SEC.gif')

    copyfile(path1, out_dir_html + 'IDK_WEC000_SEC_1.gif')
    copyfile(path2, out_dir_html + 'IDK_WEC006_SEC_2.gif')
    copyfile(path3, out_dir_html + 'IDK_WEC012_SEC_3.gif')
    copyfile(path3, out_dir_html + 'IDK_WEC018_SEC_3.gif')

    copyfile(path1, out_dir_quicklooks + 'IDK_WEC000_SEC_quicklook.png')
    copyfile(path2, out_dir_quicklooks + 'IDK_WEC006_SEC_quicklook.png')
    copyfile(path3, out_dir_quicklooks + 'IDK_WEC012_SEC_quicklook.png')
    copyfile(path3, out_dir_quicklooks + 'IDK_WEC018_SEC_quicklook.png')
    
    # Convert to webp
    im = Image.open(out_dir + 'IDK_WEC000_SEC.gif')
    im.save(out_dir + 'IDK_WEC000_SEC.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir + 'IDK_WEC006_SEC.gif')
    im.save(out_dir + 'IDK_WEC006_SEC.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir + 'IDK_WEC012_SEC.gif')
    im.save(out_dir + 'IDK_WEC012_SEC.webp', format = "WebP", lossless = True)
    im.close()

    # Convert to webp
    im = Image.open(out_dir + 'IDK_WEC018_SEC.gif')
    im.save(out_dir + 'IDK_WEC018_SEC.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_html + 'IDK_WEC000_SEC_1.gif')
    im.save(out_dir_html + 'IDK_WEC000_SEC_1.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_html + 'IDK_WEC006_SEC_2.gif')
    im.save(out_dir_html + 'IDK_WEC006_SEC_2.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_html + 'IDK_WEC012_SEC_3.gif')
    im.save(out_dir_html + 'IDK_WEC012_SEC_3.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_html + 'IDK_WEC018_SEC_3.gif')
    im.save(out_dir_html + 'IDK_WEC018_SEC_3.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_quicklooks + 'IDK_WEC000_SEC_quicklook.png')
    im.save(out_dir_quicklooks + 'IDK_WEC000_SEC_quicklook.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_quicklooks + 'IDK_WEC006_SEC_quicklook.png')
    im.save(out_dir_quicklooks + 'IDK_WEC006_SEC_quicklook.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_quicklooks + 'IDK_WEC012_SEC_quicklook.png')
    im.save(out_dir_quicklooks + 'IDK_WEC012_SEC_quicklook.webp', format = "WebP", lossless = True)
    im.close()
    
    # Convert to webp
    im = Image.open(out_dir_quicklooks + 'IDK_WEC018_SEC_quicklook.png')
    im.save(out_dir_quicklooks + 'IDK_WEC018_SEC_quicklook.webp', format = "WebP", lossless = True)
    im.close()
    
    os.remove(out_dir + 'IDK_WEC000_SEC.gif') 
    os.remove(out_dir + 'IDK_WEC006_SEC.gif')        
    os.remove(out_dir + 'IDK_WEC012_SEC.gif')
    os.remove(out_dir + 'IDK_WEC018_SEC.gif')

    os.remove(out_dir_html + 'IDK_WEC000_SEC_1.gif')
    os.remove(out_dir_html + 'IDK_WEC006_SEC_2.gif')   
    os.remove(out_dir_html + 'IDK_WEC012_SEC_3.gif')
    os.remove(out_dir_html + 'IDK_WEC018_SEC_3.gif')

    os.remove(out_dir_quicklooks + 'IDK_WEC000_SEC_quicklook.png')
    os.remove(out_dir_quicklooks + 'IDK_WEC006_SEC_quicklook.png')    
    os.remove(out_dir_quicklooks + 'IDK_WEC012_SEC_quicklook.png')
    os.remove(out_dir_quicklooks + 'IDK_WEC018_SEC_quicklook.png')
    
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
