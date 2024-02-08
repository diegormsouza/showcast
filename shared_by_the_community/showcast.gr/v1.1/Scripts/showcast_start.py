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
import time         # Scheduler library
import os, sys      # Miscellaneous operating system interfaces
import datetime     # Basic date and time types
import threading
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# USER CONFIGURATION BEGIN
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Python environment path (Windows)
#python_env = 'C://Users//user//Miniconda3//envs//showcast//'
# Python environment path (Linux)
python_env = '/home/satellite/miniconda3/envs/showcast/bin/'
#python_env = '/root/miniconda3/envs/showcast/bin/'
#------------------------------------------------------------------------------------------------------

# Showcast ingestion directory (Windows)
#shc_dir = 'D://VLAB//GNC-Samples-2019-01-12//'
# Showcast ingestion directory (Linux)
shc_dir = '/home/data/eumetcast/'
#------------------------------------------------------------------------------------------------------

# Number of days and hours to keep files in the Output directory
# The number of hours will be added to the number of days
# e.g: Delete files older than 5 hours (max_days = 0 / max_hours = 5)
# e.g: Delete files older than 1 day and 2 hours (max_days = 1 / max_hours = 2)
max_days = 4
max_hours = 0

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# USER CONFIGURATION END
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Interval in seconds
SECONDS_TO_WAIT = 60

# calling showcast_config.py with arguments
def call_monitor():
    print("\n------------- Calling Monitor Script --------------")
    print("new thread:",threading.currentThread().getName(),threading.get_ident())
    script = python_env + 'python showcast_config.py' + ' ' + python_env + ' ' + shc_dir
    os.system(script)
    print("\n------------- Monitor Script Executed -------------")
    print("used thread:",threading.currentThread().getName())
    print("Waiting for next call in", SECONDS_TO_WAIT, "seconds.\n")

    # Deleting files older than "x" days + "x" hours inside the "/db/Output/" external folder
    # Also deleted from remove-files.sh bash script
    dir_to_search = '..//..//Output/'
    for dirpath, dirnames, filenames in os.walk(dir_to_search):
        for file in filenames:
            curpath = os.path.join(dirpath, file)
            file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
            if datetime.datetime.now() - file_modified > datetime.timedelta(days=max_days,hours=max_hours):
                os.remove(curpath)

# begin new threads every SECONDS_TO_WAIT although previous threads still working for producing images
def thread_job():
    print(time.ctime())
    print(threading.get_ident())
    th=threading.Thread(target=call_monitor)
    th.start()
    threading.Timer(SECONDS_TO_WAIT, thread_job).start()

# Call the function for the first time
if __name__ == "__main__":
    thread_job()