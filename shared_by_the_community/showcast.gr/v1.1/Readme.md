# SHOWCast.GR - Frontend guide
Based on version SHOWCast_v1.4.0, developed by [Diego Souza](https://geonetcast.wordpress.com).
Modified for the needs of HNMS by RMC/LARISSA. 
Suggested installing miniconda environment. 
Installing details to [Diego Souza](https://geonetcast.wordpress.com/2019/11/06/showcast-simple-visualization-for-gnc-a/) website.
Using Eumetsat Satellites:
* METEOSAT 0° serving images every 15 minutes ,
* METEOSAT 9.5° - RAPID SCAN SERVICE (MSG-RSS) serving images every 5 minutes,
* METEOSAT 41.5° - INDIAN OCEAN DATA COVERAGE (MSG-IODC) serving images every 15 minutes,
for producing SEVIRI INDIVIDUAL CHANNELS images and Sea Surface Temperature hourly images.
* METOP
for producing Sea Surface Temperature images twice daily 

Also fixed images served by Eumetsat in telicast downloading directory wmo-ra-vi, are visualized.
All images are produced and kept alive for 3 days in an external folder Output, prefered to be in other part of HDD, like the Eumetsat raw images downloading folder.
Last Update: Sep 2020

## Colortables
Directory containing the cpt files, used for images color mapping.

## Guides
Directoty containing pdf guides of Satellite products for the user. 

## HTML & JS
Directories containing frontend html files SHOWCast, Player_MeteoATA, Player_wmo and UserView with their js corresponding files.

## Legends
Directoty containing the legends for the images.

## Libraries
Directory containing the rest js utilites and libraries as bootstrap and jquery.

## Logos
Directory containing the icons for logos

## Logs
Directory containing the daily log files for used satellite images and old files removing script 

## Maps
Directory containing map images used for data backgrounds. 

## PHP
Directory containing map  php backend files. 

## Scripts
Directory containing 
* python files, used to produce all images, 
* showcast service client for keeping showcast alive
* bash script file for removing old data from directories. 

## Shapefiles
Directory containing coastline, states and countries files.  

## Training
Directory containing nothing. 

## Utils
Directory containing labels data and xRITDecompres executables, needed for decompressing MSG HRIT files on the fly.


## FAQ

....
# SHOWCast.GR_v1.1 - Frontend guide (18-Sep-2020)
Creation of a symlink in /var/www/html/SHOWCast.GR redirecting to the current version of SHOWCast.GR (eg SHOWCast.GR_v1.1)
In order to set the path at the files once and don't have to change it, at every new version 
Files that have relative path to SHOWCast directory(ies):
	/etc/systemd/system/showcast.service
	/var/www/html/.htaccess
	../Scripts/
		showcast_client
		remove-files.sh
	/var/spool/cron/root
 
 
# 2020-10-20 Kyparlis
Try to make a secondary html page to show the log file