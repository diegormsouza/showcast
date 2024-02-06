#!/bin/bash
echo
echo ----------------------------------
echo "Welcome to the SHOWCast Installer!"
echo ----------------------------------
echo

echo "Step 1-) Miniconda will be installed."
echo

read -p "Do you want to proceed (Y/[N])? " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
	# Get the SHOWCast main directory
	parentdir="$(dirname "$(pwd)")"
	
	# Check if Miniconda is already installed	
	if [ -d "$parentdir/Miniconda3" ]; then
		echo
    	echo "The Miniconda3 folder already exists in your SHOWCast directory at:"
    	echo "$parentdir/Miniconda3"
    	echo "If you want to reinstall it, delete the Miniconda3 folder and"
    	echo "execute this installer again."
    else	# if not, install Miniconda 	  	
		echo
		echo "Miniconda installation directory: $parentdir/Miniconda3/"
		echo
		echo "Installing Miniconda... [this will take some minutes]"
		echo
		sh ./Miniconda3/Miniconda3-py39_4.10.3-Linux-x86_64.sh -b -p $parentdir/Miniconda3
		echo "Miniconda installation finished."
	fi
	
	echo
	echo "Step 2-) The SHOWCast environment will be created."
	echo
	read -p "Do you want to proceed (Y/[N])? " -n 1 -r
	echo
	
	if [[ $REPLY =~ ^[Yy]$ ]]; then
		# Check if the showcast env is already created
		if [ -d "$parentdir/Miniconda3/envs/showcast" ]; then
			echo
    		echo "The showcast environment already exists in your Miniconda3 directory at:"
    		echo "$parentdir/Miniconda3/envs/showcast"
    		echo "If you want to reinstall it, delete the showcast env folder and  "
    		echo "execute this installer again."
    	else	# if not, update conda and create the showcast env  	
			echo
			echo "Updating conda... [this may take some minutes]"
			echo
			$parentdir/Miniconda3/condabin/conda update -n base -c defaults conda --yes
			echo "Creating the SHOWCast environment... [this will take some minutes]"
			$parentdir/Miniconda3/condabin/conda env create -f $parentdir/Installer/Miniconda3/environment.yml		
		fi		
	fi
fi
echo
read -p "Finished. Press any key to exit ..."
