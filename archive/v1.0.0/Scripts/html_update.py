# Python Script Example: New Script Pack
#---------------------------------------------------------------------------------------------
# Required modules
import glob                 # Unix style pathname pattern expansion
import os                   # Miscellaneous operating system interfaces
import sys                  # Import the "system specific parameters and functions" module
import datetime             # Basic Date and Time types
import time as t            # Time access and conversion
from shutil import copyfile # Copy files
from PIL import Image
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
def update(satellite, product):
    # Start the time counter
    #print('Script started.')
    #start = t.time() 

    # Create the satellite output directory if it doesn't exist
    out_dir = '..//HTML//Output//' + satellite
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    # Create the product output directory if it doesn't exist
    out_dir = '..//HTML//Output//' + satellite + '//' + product + '//'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
        
    # Read all the file names in the Output dir as a list
    files = []
    
    # Directory
    directory = '..//Output//' + satellite + '//' + product + '//'
    
    # File identifier
    identifier = satellite + "_" + product + '*.png'
    
    # Rename identifier
    rename_id = satellite + "_" + product + '_'
    
    # Add to the list the files in the dir that matches the identifier
    for filename in sorted(glob.glob(directory + identifier)):
        files.append(filename)
    
    # Maximum number of frames 
    max_files = 20  
    
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
    
    # Create the thumbnail of the last file
    thumb_dir = '..//HTML//Output//QuickLooks//' + rename_id + 'quicklook.png'
    copyfile(files[-1], dst)
    im = Image.open(files[-1])
    size = (1024,1024)
    im.thumbnail(size)
    im.save(thumb_dir)
    
    #print('Total processing time:', round((t.time() - start),2), 'seconds.') 

