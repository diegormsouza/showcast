@echo off
setlocal

echo --------------------
echo Cloud Download Start
echo --------------------
echo:
echo Cloud download will be executed.
echo:

for %%I in ("%~dp0.") do for %%J in ("%%~dpI.") do set ParentFolderName=%%~dpnxJ
:: echo %ParentFolderName%

:: Check if the showcast env is already created
IF EXIST %ParentFolderName%\Miniconda3\envs\showcast\ (
	echo Activating the showcast env:
	echo %ParentFolderName%\Miniconda3\condabin\conda activate showcast
	call %ParentFolderName%\Miniconda3\condabin\conda activate showcast
	echo:
	echo Calling cloud_download_config.py
	echo %ParentFolderName%\Miniconda3\envs\showcast\python.exe %~dp0Scripts\pda_aws_download_start.py
	call %ParentFolderName%\Miniconda3\envs\showcast\python.exe %~dp0Scripts\pda_aws_download_start.py
) ELSE (
	:: if not, show a message to the user
	echo The showcast env is not created. Please create it using the installer found at
	echo %ParentFolderName%\Installer\showcast_install_windows.bat
	echo and start the Cloud Download utility again.	
)

echo:
PAUSE