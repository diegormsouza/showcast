@echo off
setlocal

:: Select the number of parallel SHOWCast processes
SET /A num_process=1

echo --------------
echo SHOWCast Start
echo --------------
echo:
echo SHOWCast will be executed.
echo:

:: Check if the showcast env is already created
IF EXIST %~dp0Miniconda3\envs\showcast\ (
	echo Activating the showcast env:
	echo %~dp0Miniconda3\condabin\conda activate showcast
	call %~dp0Miniconda3\condabin\conda activate showcast
	
	echo:
	echo Calling showcast_cleaner.py process:
	echo %~dp0Miniconda3\envs\showcast\python.exe %~dp0Scripts\showcast_cleaner.py
	start cmd.exe /K %~dp0Miniconda3\envs\showcast\python.exe %~dp0Scripts\showcast_cleaner.py

	echo:
	echo Calling showcast_start.py processes:
	
	for /l %%x in (1, 1, %num_process%) do (
		echo %~dp0Miniconda3\envs\showcast\python.exe %~dp0Scripts\showcast_start.py %%x
		start cmd.exe /K %~dp0Miniconda3\envs\showcast\python.exe %~dp0Scripts\showcast_start.py %%x
    )

) ELSE (
	:: if not, show a message to the user
	echo The showcast env is not created. Please create it using the installer found at
	echo %~dp0Installer\showcast_install_windows.bat
	echo and start SHOWCast again.	
)

echo:
PAUSE