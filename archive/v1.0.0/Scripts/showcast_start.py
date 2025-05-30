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
import sched, time # Scheduler library
import os          # Miscellaneous operating system interfaces         
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Python environment (Windows)
python_env = 'C://Users//dsouza//Miniconda3//envs//showcast//'
# Python environment (Linux)
#python_env = '//dados//miniconda3//envs//showcast//bin//'
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# GEONETCast-Americas ingestion directory (Windows)
gnc_dir = 'D://GEONETCast//'
# GEONETCast-Americas ingestion directory (Linux)
#gnc_dir = '//dados//GEONETCast//'
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Interval in seconds
seconds = 10

# Call the function for the first time without the interval
print("\n")
print("------------- Calling Monitor Script --------------")
script = python_env + 'python showcast_config.py' + ' ' + python_env + ' ' + gnc_dir		
os.system(script)
print("------------- Monitor Script Executed -------------")
print("Waiting for next call. The interval is", seconds, "seconds.")
	
# Scheduler function
s = sched.scheduler(time.time, time.sleep)

def call_monitor(sc): 
    print("\n")
    print("------------- Calling Monitor Script --------------")
    script = python_env + 'python showcast_config.py' + ' ' + python_env + ' ' + gnc_dir		
    os.system(script)
    print("------------- Monitor Script Executed -------------")
    print("Waiting for next call. The interval is", seconds, "seconds.")	
    s.enter(seconds, 1, call_monitor, (sc,))
    # Keep calling the monitor
	
# Call the monitor
s.enter(seconds, 1, call_monitor, (s,))
s.run()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

