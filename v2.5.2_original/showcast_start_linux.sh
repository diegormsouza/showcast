#!/bin/bash
# Select the number of SHOWCast parallel processes
declare -i num_process=1

echo --------------
echo "SHOWCast Start"
echo --------------
echo
echo "SHOWCast will be executed."
echo

# Check if the showcast env is already created
if [ -d "$(pwd)/Miniconda3/envs/showcast" ]; then

	echo "Calling showcast_cleaner.py"
	gnome-terminal --tab -e 'bash -c "$(pwd)/Miniconda3/envs/showcast/bin/python Scripts/showcast_cleaner.py; exec bash"' 

	echo "Calling showcast_start.py"
	for i in $( seq 1 $num_process)
	do
		#gnome-terminal --tab -e 'bash -c "echo $(pwd)/Miniconda3/envs/showcast/bin/python Scripts/showcast_start.py '$i'; exec bash"' 
		gnome-terminal --tab -e 'bash -c "$(pwd)/Miniconda3/envs/showcast/bin/python Scripts/showcast_start.py '$i'; exec bash"' 
	done	
	
else	# if not, show a message to the user	
	echo The showcast env is not created. Please create it using the installer found at
	echo $(pwd)/Installer/showcast_install_linux.sh
	echo and start SHOWCast again.	
fi		

echo
read -p "Finished. Press any key to exit ..."
