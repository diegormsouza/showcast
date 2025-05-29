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
import sched, time                    # Scheduler library
import os, sys                        # Miscellaneous operating system interfaces   
from os.path import dirname, abspath  # Return a normalized absolutized version of the pathname path 
import datetime                       # Basic date and time types   
import platform                       # To check which OS is being used
#------------------------------------------------------------------------------------------------------

# SHOWCast process number
showcast_process = sys.argv[1]

print("SHOWCast process number: ", showcast_process)

#------------------------------------------------------------------------------------------------------
# USER CONFIGURATION BEGIN
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Ingestion directory (AVOID USING DIRECTORIES WITH SPACES)
ingest_dir = 'D://data//fazzt//'      # Windows Example - Change it according to your GNC-A Station
#ingest_dir = '//data//fazzt//'       # Linux Example - Change it according to your GNC-A Station
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Number of days and hours to keep files in the Output directory 
# The number of hours will be added to the number of days
# e.g: Delete files older than 5 hours (max_days = 0 / max_hours = 5) 
# e.g: Delete files older than 1 day and 2 hours (max_days = 1 / max_hours = 2) 
max_days = 3
max_hours = 0
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# USER CONFIGURATION END
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# SHOWCast directory:
showcast_dir = dirname(dirname(abspath(__file__)))

# Python environment (Script parent dir + python env)
osystem = platform.system()
if osystem == "Windows":
    python_env = showcast_dir + '//Miniconda3//envs//showcast//' 
else:
    python_env = showcast_dir + '//Miniconda3//envs//showcast//bin//' 
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# QT Plugin path
os.environ['QT_PLUGIN_PATH'] = python_env + "Library//plugins//"

# Interval in seconds
seconds = 1

# Call the function for the first time without the interval
print("\n")
print("------------- Calling Monitor Script --------------")
script = python_env + 'python ' + showcast_dir + '//Scripts//showcast_config.py' + ' ' + python_env + ' ' + ingest_dir + ' ' + showcast_process
os.system(script)
print("------------- Monitor Script Executed -------------")
print("Waiting for next call. The interval is", seconds, "seconds.")

# Deleting files older than "x" days + "x" hours inside the "SHOWCast/Output/" folder structure  
dir_to_search = showcast_dir + '//Output//'
for dirpath, dirnames, filenames in os.walk(dir_to_search):
    for file in filenames:
        curpath = os.path.join(dirpath, file)
        file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
        if datetime.datetime.now() - file_modified > datetime.timedelta(days=max_days,hours=max_hours):
            #print(curpath)
            os.remove(curpath)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------	
# Scheduler function
s = sched.scheduler(time.time, time.sleep)

def call_monitor(sc): 
    print("\n")
    print("------------- Calling Monitor Script --------------")
    script = python_env + 'python ' + showcast_dir + '//Scripts//showcast_config.py' + ' ' + python_env + ' ' + ingest_dir	+ ' ' + showcast_process	
    os.system(script)
    print("------------- Monitor Script Executed -------------")
    print("Waiting for next call. The interval is", seconds, "seconds.")	
    s.enter(seconds, 1, call_monitor, (sc,))
    # Keep calling the monitor
      
    # Deleting files older than "x" days + "x" hours inside the "SHOWCast/Output/" folder structure  
    dir_to_search = showcast_dir + '//Output//'
    for dirpath, dirnames, filenames in os.walk(dir_to_search):
        for file in filenames:
            curpath = os.path.join(dirpath, file)
            file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
            if datetime.datetime.now() - file_modified > datetime.timedelta(days=max_days,hours=max_hours):
                #print(curpath)
                os.remove(curpath)
            
# Call the monitor
s.enter(seconds, 1, call_monitor, (s,))
s.run()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

