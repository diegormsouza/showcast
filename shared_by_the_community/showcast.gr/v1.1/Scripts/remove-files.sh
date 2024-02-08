#!/bin/sh
# In order to remove files of Tellicast - Showcast processes

echo `date`

# The folder where Tellicast saves files
FolderToDbFiles="/home/data"
MinsOlderThan="+1440"

find "$FolderToDbFiles" -name "*" -type f -mmin "$MinsOlderThan" -ls
find "$FolderToDbFiles" -name "*" -type f -mmin "$MinsOlderThan" -exec rm -f {} \;

# The folders where SHOWcast saves files. Not used any more. SHOWcast output folder --> /db/Output
#FolderToDbFiles="../Output"
#MinsOlderThan="+1440"
#find "$FolderToDbFiles" -name "*" -type f -mmin "$MinsOlderThan" -ls
#find "$FolderToDbFiles" -name "*" -type f -mmin "$MinsOlderThan" -exec rm -f {} \;


FolderToDbFiles="/db/Output/Thumbnails"
MinsOlderThan="+45"
find "$FolderToDbFiles" -not -path "*MTP/*" -name "*" -type f -mmin "$MinsOlderThan" -ls
find "$FolderToDbFiles" -not -path "*MTP/*" -name "*" -type f -mmin "$MinsOlderThan" -exec rm -f {} \;


FolderToDbFiles="/db/Output/wmo_ra_vi/"
DaysOlderThan="+1"
find "$FolderToDbFiles" -name "*" -type f -mtime "$DaysOlderThan" -ls
find "$FolderToDbFiles" -name "*" -type f -mtime "$DaysOlderThan" -exec rm -f {} \;


FolderToDbFiles="/db/Output/"
DaysOlderThan="+1"
find "$FolderToDbFiles" -name "*" -type f -mtime "$DaysOlderThan" -ls
find "$FolderToDbFiles" -name "*" -type f -mtime "$DaysOlderThan" -exec rm -f {} \;


FolderToDbFiles="/var/www/html/SHOWCast.GR/Logs/"
DaysOlderThan="+3"
find "$FolderToDbFiles" -name "*" -type f -mtime "$DaysOlderThan" -ls
find "$FolderToDbFiles" -name "*" -type f -mtime "$DaysOlderThan" -exec rm -f {} \;