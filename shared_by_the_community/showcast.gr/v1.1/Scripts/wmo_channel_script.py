#####################################################
#Python Sript to Support EUMETCast WMO-RA-VI Channel#
#####################################################
# In WMO-RA-VI Channel several useful files are delivered from UK MetOffice and DWD,
# in terms of SFC analysis and numerical prediction maps.
# This script manipulates those supporting files and store them to idinvidual folders
# for further elaboration and supoprt of showcast app.
#####################################################################################

import os
import shutil

#########################################
# Source and Destinations Folder Section#
#########################################

#Define the path to the EUMETCast Channel WMO-RA-VI folder
source_channel = '/home/data/eumetcast/bas/WMO-RA-VI/'

#Define the destination folder for DWD Meteograms
dwd_meteograms = '/db/Output/wmo_ra_vi/DWD_Meteograms'

#Define the destination folder for DWD Maps
dwd_maps = '/db/Output/wmo_ra_vi/DWD_Maps'

#Define the destination folder for ECMWF forecast Maps
ecmwf_forecasts = '/db/Output/wmo_ra_vi/ECMWF_Forecasts'

#Define the destination folder for UK MetOffice Maps
ukmo_maps = '/db/Output/wmo_ra_vi/UKMO_Maps'

##########################
# Checking Folder Section#
##########################

# Checking existance of the destination folders, in case they do not exist it creates them
# The necessary folders are: DWD_Meteograms, DWD_Maps, ECMWF_Forecasts and UKMO_Maps

if not os.path.exists(dwd_meteograms):
    os.makedirs(dwd_meteograms)
if not os.path.exists(dwd_maps):
    os.makedirs(dwd_maps)
if not os.path.exists(ecmwf_forecasts):
    os.makedirs(ecmwf_forecasts)
if not os.path.exists(ukmo_maps):
    os.makedirs(ukmo_maps)

#Check all files in source and if they match the criteria move them to destination folders
print("Distributing wmo ra vi files")
for f in os.listdir(source_channel):
    if f[:10]=='Z__C_EDZW_':
        if f[31:39]== 'waf_swc_':
            shutil.move(source_channel +f, ukmo_maps)
        if f[24:39]== '_fax01,egrr_bhv':
            shutil.move(source_channel +f, ukmo_maps)
        if f[24:39]== '_fax01,egrr_bwk':
            shutil.move(source_channel +f, ukmo_maps)
        if f[24:30]== '_meg01':
            shutil.move(source_channel +f, dwd_meteograms)
        if f[24:47]== '_tka01,ana_bwkman_dwdna':
            shutil.move(source_channel +f, dwd_maps)
        if f[24:35]== '_nwv01,ico_':
            shutil.move(source_channel +f, dwd_maps)
        if f[31:36]== 'ecmwf':
            shutil.move(source_channel +f, ecmwf_forecasts)

#########################################    
#Delete files from source folder Section#
#########################################

#Delete all the others files which are irellevant to our scope from the source folder
print("Deleting wmo ra vi files not being used")
for f in os.listdir(source_channel):
    try:
        os.remove(source_channel+f)
    except Exception as ex:
        print(ex)
    