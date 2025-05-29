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
__version__ = "2.4.0"
__maintainer__ = "Diego Souza"
__email__ = "diego.souza@inpe.br"
__status__ = "Production"
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Required modules
#--------------------------------
import glob                           # Unix style pathname pattern expansion
import os                             # Miscellaneous operating system interfaces
from os.path import dirname, abspath  # Return a normalized absolutized version of the pathname path 
import sys                            # Import the "system specific parameters and functions" module
import datetime                       # Basic Date and Time types
import time as t                      # Time access and conversion
from shutil import copyfile           # Copy files
from PIL import Image                 # Python Imaging Library 
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
def update(satellite, product, nfiles, outdir, vis_dir):
    # Start the time counter
    #print('Script started.')
    #start = t.time() 
	
    # Create the visualization directory if it doesn't exist
    out_dir = vis_dir
    
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    # Create the satellite output directory if it doesn't exist
    out_dir = vis_dir + satellite
	
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    # Create the product output directory if it doesn't exist
    out_dir = vis_dir + satellite + '//' + product + '//'
    
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
        
    # Read all the file names in the Output dir as a list
    files = []
    
    # Directory
    directory = outdir + satellite + '//' + product + '//'
    
    # File identifier
    identifier = satellite + "_" + product + '*.png'
    
    # Rename identifier
    rename_id = satellite + "_" + product + '_'
    
    # Add to the list the files in the dir that matches the identifier
    for filename in sorted(glob.glob(directory + identifier)):
        files.append(filename)
    
    # Maximum number of frames 
    max_files = nfiles  
    
    # Keep on the list only the max number of files
    files = files[-max_files:]
    
    # Copy the files to the HTML Output folder, following the HTML naming convention
    for idx, val in enumerate(files):
        src = val
        dst = out_dir + rename_id + str(idx + 1) + '.png'
        copyfile(src, dst)
        
    # Get the number of files on the folder
    num_files = len(files)
    # Get the difference of desired files and available files
    diff_files = max_files - num_files
    
    # If there are less files than the maximum HTML animation files, repeat the last one "x" times
    if diff_files > 0:
        for i in range(diff_files):
            #print(num_files + i + 1)
            dst = out_dir + rename_id + str(num_files + i + 1) + '.png'
            copyfile(files[-1], dst)
    
    # Create the quicklook directory if it doesn't exist
    out_dir = vis_dir + 'QuickLooks//'
    
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
        
    # Create the thumbnail of the last file
    thumb_dir = vis_dir + 'QuickLooks//' + rename_id + 'quicklook.png'
    copyfile(files[-1], dst)
    im = Image.open(files[-1])
    size = (1024,1024)
    im.thumbnail(size)
    im.save(thumb_dir)
    
    #print('Total processing time:', round((t.time() - start),2), 'seconds.') 

