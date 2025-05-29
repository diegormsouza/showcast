#!/bin/bash
echo ----------------------
echo "Cloud Download Start"
echo ----------------------
echo
echo "Cloud download will be executed."
echo

parentdir="$(dirname "$(pwd)")"
#echo $parentdir

# Check if the showcast env is already created
if [ -d "$parentdir/Miniconda3/envs/showcast" ]; then
	echo "Calling cloud_download_config.py"
	echo $parentdir/Miniconda3/envs/showcast/bin/python $parentdir/Cloud/Scripts/grb_unidata_download_config.py
	$parentdir/Miniconda3/envs/showcast/bin/python $parentdir/Cloud/Scripts/grb_unidata_download_config.py
	echo
else	# if not, show a message to the user	
	echo The showcast env is not created. Please create it using the installer found at
	echo $(pwd)/Installer/showcast_install_linux.sh
	echo and start the Cloud Download utility again.	
fi		

echo
read -p "Finished. Press any key to exit ..."
