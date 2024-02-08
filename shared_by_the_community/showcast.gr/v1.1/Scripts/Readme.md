# SHOWCast.GR_v1 - Scripts

## showcast_start.py.
Defines 
* Python environment (python_env) folder and 
* eumetsat products downloading folder (shc_dir).
Uses threads to call showcast_config.py and start processes every 60 seconds.

## showcast_config.py.
In this script are selected if true:
* Satellites to use for processing
* Sectors to be used for images boxes
* Python scripts to start processes

## process_msg_channels.py
### Producing all MSG images using HRIT files
xritDecompress uses by default the system tmp directory to decompress downloaded data on the fly.
Satpy loads data on scene.
Matplotlib plots data, bountaries, coastlines etc to images.
Images are saved in directory /var/www/html/Output which is prefered to be a link to another HDD.

## process_mtp_sst_fdk.py
Uses METOP satellite data, downloaded two times per day and produces Global  Sea Surface Temperature image.
Reads NetCDF files.

## process_msg_sst_eur.py
Uses MSG satellite data, downloaded hourly and produces Sector Sea Surface Temperature image.
Reads NetCDF files.

## process_msg_sst_gr.py
Uses MSG satellite data, downloaded hourly and produces Greek Sector Sea Surface Temperature image.
Reads NetCDF files.

## wmo_channel_script.py
Supports EUMETCast WMO-RA-VI Channel
In WMO-RA-VI Channel several useful files are delivered from UK MetOffice and DWD,
in terms of SFC analysis and numerical prediction maps.
This script manipulates those supporting files and store them to idinvidual folders
for further elaboration and supoprt of showcast app.

## cpt_convert.py
Converts cpt files to matplotlib readable files.

## remove-files.sh
Bash script used in order to remove old files of Tellicast and Showcast processed images.
Executed from users crontab and saves log file to folder Logs.

## showcast_client
This client is executed by the service /etc/systemd/system/showcast.service
showcast.service is used to keep alive showcast processes even though user is loged out.