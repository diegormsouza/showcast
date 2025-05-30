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
__credits__ = ["Diego Souza", "Ricardo Valenti", "Gustavo Rodriguez"]
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
from datetime import datetime, timedelta                     # Library to convert julian day to dd-mm-yyyy
import numpy as np                                           # Scientific computing with Python
import time as t                                             # Time access and conversion
import sys                                                   # Import the "system specific parameters and functions" module
import math                                                  # Import math
import os                                                    # Miscellaneous operating system interfaces
import glob                                                  # Unix style pathname pattern expansion
from os.path import dirname, abspath                         # Return a normalized absolutized version of the pathname path 
import warnings                                              # Warning control
warnings.filterwarnings("ignore")
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()  

# SHOWCast directory:
main_dir = dirname(dirname(abspath(__file__)))

# Image path
path = (sys.argv[1])

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Extracting information from the file name

# Print the file characteristics
header = path[path.find("T_")+2:path.find("_C")]
t1t2 = header[0:2]
a1a2 = header[2:4]
ii = header[4:6]
cccc = header[6:10]
time = header[10:16]
import ntpath
file = ntpath.basename(path)
folder = path.rsplit('T',1)[0]
info = path[path.find("KWBC_")+5:path.find(".txt")]
date = info[0:8]

print('\n')
print("============================")
print("File name: ", file)
print("Folder name: ", folder)
print("ISCS header: ", header)
print("T1T2: ", t1t2)
print("A1A2: ", a1a2)
print("ii: ", ii)
print("CCCC: ", cccc)
print("Time: ", time)
print("Info: ", info)
print("Date: ", date)
print("============================")
print('\n')

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Listing all the available messages

# File identifier
identifier = '*' + t1t2 + a1a2 + '*'
print ("Message identifier: ", identifier)
print('\n')

# Create the list that will store the file names
iscs_files = []
    
# Add to the list the files in the dir that matches the identifier
for filename in sorted(glob.glob(folder + identifier), key=os.path.getmtime):
    iscs_files.append(filename)
    
print("Number of messages: ", len(iscs_files))    
print('\n')

print("Messages found:")
print(*iscs_files, sep='\n')
print('\n')

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Keeping only the messages from the latest file date

# Number of files kept
iscs_files = [ x for x in iscs_files if date in x ]

print("Number of messages kept: ", len(iscs_files))    
print('\n')

print("Messages kept:")
print(*iscs_files, sep='\n')
print('\n')

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Create the ISCS output directory if it doesn't exist
out_dir = main_dir + '//Output//' + 'ISC'
if not os.path.exists(out_dir):
   os.mkdir(out_dir)

# Create the product output directory if it doesn't exist
out_dir = main_dir + '//Output//' + 'ISC' + '//' + 'SMETAR' + '//'
if not os.path.exists(out_dir):
   os.mkdir(out_dir)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Comparing the messages with the log to check if there's a new message

# If the log file doesn't exist for the date, remove the main message file
from pathlib import Path
my_file = Path(main_dir + '//Logs//iscs-smetar_log_' + date[0:4] + "-" + date[4:6] + "-" + date[6:8] + '.txt')

if not my_file.is_file():
    try:
        os.remove(out_dir + 'iscs-smetar.txt')
        # If the iscs output file doesn't exist yet, create one
        file = open(out_dir + 'iscs-smetar.txt', 'a')
        file.close()
        # Write the final file title
        with open(out_dir + 'iscs-smetar.txt', 'a') as main_file:             
            main_file.write('---------------------------------------------------------------------------') 
            main_file.write('\n')
            main_file.write('\n')
            main_file.write("                            METAR MESSAGES")
            main_file.write('\n')
            main_file.write('\n')
            main_file.write("T1T2: ")
            main_file.write(t1t2)
            main_file.write('\n')
            main_file.write("A1A2: ")
            main_file.write(a1a2)
            main_file.write('\n')
            main_file.write('\n')
            main_file.write("Date: ")
            main_file.write(date[0:4] + "-" + date[4:6] + "-" + date[6:8])
            main_file.write('\n')
            main_file.write('\n')
                
        main_file.close()
       
    except OSError:
        pass
    
# If the iscs log file for this date doesn't exist yet, create one
file = open(main_dir + '//Logs//iscs-smetar_log_' + date[0:4] + "-" + date[4:6] + "-" + date[6:8] + '.txt', 'a')
file.close()

# Put all file names on the iscs log in a list
log = []
with open(main_dir + '//Logs//iscs-smetar_log_' + date[0:4] + "-" + date[4:6] + "-" + date[6:8] + '.txt') as f:
    log = f.readlines()
f.close()
 
# Remove the line feeds
log = [x.strip() for x in log]

# Count the new ISCS Messages
matches = sum(el in iscs_files for el in log)
new_messages = len(iscs_files) - matches
print("New Messages: ", new_messages)
print('\n')

if (new_messages > 0):
    
    '''
    import tkinter as tk
    from tkinter import messagebox
 
    root = tk.Tk()
    root.overrideredirect(1)
    root.withdraw()
    messagebox.showinfo("METAR Warning:", "You have " + str(new_messages) + " new message(s)!")
    root.destroy()
    '''
    from tkinter import Tk
    from tkinter.messagebox import Message 
    from _tkinter import TclError

    TIME_TO_WAIT = 10000 # in milliseconds 
    root = Tk() 
    root.withdraw()
    try:
        root.after(TIME_TO_WAIT, root.destroy) 
        Message(title="METAR Warning:", message="You have " + str(new_messages) + " new message(s)!", master=root).show()
    except TclError:
        pass

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

# Writing the the messages on a single file

# If the iscs output file doesn't exist yet, create one
file = open(out_dir + 'iscs-smetar.txt', 'a')
file.close()

with open(main_dir + '//Logs//iscs-smetar_log_' + date[0:4] + "-" + date[4:6] + "-" + date[6:8] + '.txt', 'a') as f:
    # Compare the iscs file list with the log
    # Loop through all the files
    for x in iscs_files:
    # If a file is not on the log, put it on the log
        if x not in log:
            f.write(x + '\n')
            
            # Write the final file
            with open(out_dir + 'iscs-smetar.txt', 'a') as main_file:
                with open(x) as iscs_file:
                    msg_data = iscs_file.read()
                iscs_file.close()
                
                main_file.write('---------------------------------------------------------------------------') 
                main_file.write('\n')
                main_file.write('\n')
                main_file.write("Message File: ")
                main_file.write(ntpath.basename(x))
                main_file.write('\n')
                main_file.write('\n')
                main_file.write(msg_data)
                main_file.write('\n')           
           
            main_file.close()
            
            print(iscs_files[-1])
            print(x)
            print("")
            
            if (x == iscs_files[-1]):
                # Write the final file
                with open(out_dir + 'iscs-smetar.txt', 'a') as main_file:
                    main_file.write('########################### END OF MESSAGE SET ############################') 
                    main_file.write('\n')   
                    main_file.write('\n')    
                main_file.close()
f.close()
    
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------    

# Write the final file
#with open(out_dir + 'iscs-surface.txt', 'a') as f:
    # Compare the iscs file list with the log
    # Loop through all the files
#    for x in f:
#       with open(x) as iscs_file:
#            msg_data = f.read()
   
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------  
    
# Total processing time
print('Total processing time:', round((t.time() - start),2), 'seconds.') 
