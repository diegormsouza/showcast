#######################################################################################################
# LICENSE
# Copyright (C) 2020 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL
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
__copyright__ = "Copyright (C) 2020 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL"
__credits__ = ["Diego Souza"]
__license__ = "GPL"
__version__ = "2.1.0"
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
# SHOWCast directory:
main_dir = dirname(dirname(dirname(abspath(__file__))))

# Python environment (Script parent dir + python env)
osystem = platform.system()
if osystem == "Windows":
    python_env = main_dir + '//Miniconda3//envs//showcast//' 
else:
    python_env = main_dir + '//Miniconda3//envs//showcast//bin//' 
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# QT Plugin path
os.environ['QT_PLUGIN_PATH'] = python_env + "Library//plugins//"

# Interval in seconds
seconds = 1

# Call the function for the first time without the interval
print("\n")
print("------------- Calling Monitor Script --------------")
print("")
script = python_env + 'python ' + main_dir + '//Cloud//Scripts//pda_aws_download_config.py' 
print(script)
os.system(script)
print("------------- Monitor Script Executed -------------")
print("Waiting for next call. The interval is", seconds, "seconds.")
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------	
# Scheduler function
s = sched.scheduler(time.time, time.sleep)

def call_monitor(sc): 
	# Call the function for the first time without the interval
	print("\n")
	print("------------- Calling Monitor Script --------------")
	print("")
	script = python_env + 'python ' + main_dir + '//Cloud//Scripts//pda_aws_download_config.py'
	print(script)
	os.system(script)
	print("------------- Monitor Script Executed -------------")
	print("Waiting for next call. The interval is", seconds, "seconds.")
	s.enter(seconds, 1, call_monitor, (sc,))
	
# Call the monitor
s.enter(seconds, 1, call_monitor, (s,))
s.run()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

