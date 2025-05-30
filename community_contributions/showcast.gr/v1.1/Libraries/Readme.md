# SHOWCast.GR_v1 - Frontend guide
Based on version SHOWCast_v1.4.0, developed by Diego Souza.
Modified for the needs of HNMS by RMC/LARISSA. 
Uses Eumetsat Satellites:
-METEOSAT 0° (images every 15 minutes),
-METEOSAT 9.5° - RAPID SCAN SERVICE (MSG-RSS) (images every 5 minutes),
-METEOSAT 41.5° - INDIAN OCEAN DATA COVERAGE (MSG-IODC) (images every 15 minutes)
for producing SEVIRI INDIVIDUAL CHANNELS images.
-METOP
for producing Sea Surface Temperature twice daily images
-MSG
for producing Sea Surface Temperature hourly images
Also ready images served by Eumetsat in telicast downloading directory wmo-ra-vi, are visualized.
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


** gia to fakelo
whereas FontAwesome contains the font of the functional symbols that are used (e.g. left arrow).

Carousel.js and GridGallery.js are adjusted versions from the MeteoATA project (not public yet), and extend corresponding Bootstrap functionalities.

Gifshot creates gifs from images (downloaded from Github), and wheelzoom-master allows seemless scroll zooming and panning on the carousels of Carousel.js (heavily adjusted version from the Github original). Both are used in Player_MeteoATA.

Util.js contains all the generalized functions (expected to be used by more than one file). It's adjusted from MeteoATA and has some functions that are in use there and not in this project yet.

Theme.css contains all the CSS of the project and similarly some selectors are not used here yet. Variables with the theme colors have been set on top. All the brand new selectors are contained after the last heading ("SHOWCAST ADDITIONS").

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
-python files, used to produce all images, 
-showcast service client
-bash script file for removing old data from directories. 

## Shapefiles
Directory containing coastline, states and countries files.  

## Training
Directory containing map  php backend files.  

## Utils
Directory containing labels data and xRITDecompres executables, needed for decompressing MSG HRIT files on the fly.

### ShowCast

It's the homepage and launches the other two pages.

Its first functionality is the selection of the area and satellite to be viewed. This is how it works:

The HTML contains all the tables of all the satellites for a specific area (by default FDK - Full Disk - World). The default satellite (currently MSG) is the only with tables that have the class d-block, whereas all the other tables have the class d-none, and therefore only the first are visible. By clicking another satellite name, the corresponding tables get the class d-block and the rest d-none, and this is how the user gets the feel of "switching between tabs".

Clicking other areas (EUR and GRC), a regex runs (function setArea), which changes all the parameters of links and image sources in the document correspondingly (e.g. the URL "Player_MeteoATA.html?cat=MSG&type=ASHRGB&area=FDK" becomes "Player_MeteoATA.html?cat=MSG&type=ASHRGB&area=EUR"), whereas the visible tables and therefore the selected satelite stay constant.

The second functionality is named UserView, and allows the selection of up to 4 products for quick viewing of their last 5 images. [To be continued]

## FAQ

....
