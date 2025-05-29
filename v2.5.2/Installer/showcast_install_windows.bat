@echo off
setlocal

echo:
echo ----------------------------------
echo Welcome to the SHOWCast Installer!
echo ----------------------------------
echo:
echo Step 1-) Miniconda will be installed.
echo:

:PROMPT
SET /P AREYOUSURE=Do you want to proceed (Y/[N])? 
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END

:: Get the SHOWCast main directory
for %%I in ("%~dp0.") do for %%J in ("%%~dpI.") do set ParentFolderName=%%~dpnxJ

:: Check if Miniconda is already installed
IF EXIST %ParentFolderName%\Miniconda3\ (
	echo:
	echo The Miniconda3 folder already exists in your SHOWCast directory at:
    echo %ParentFolderName%\Miniconda3
    echo If you want to reinstall it, delete the Miniconda3 folder and 
    echo execute this installer again.
) ELSE (
	:: if not, install Miniconda
	echo:
	echo Miniconda installation directory: %ParentFolderName%\Miniconda3\
	echo:
	echo Installing Miniconda... [this will take some minutes]
	echo:
	start /wait "" %~dp0/Miniconda3/Miniconda3-py39_4.10.3-Windows-x86_64.exe /InstallationType=JustMe /RegisterPython=0 /S /D=%ParentFolderName%\Miniconda3
	echo Miniconda installation finished.
)

echo:
echo Step 2-) Installing Mamba for faster environment creation...
echo:

call %ParentFolderName%\Miniconda3\condabin\conda install mamba -n base -c conda-forge --yes

echo:
echo Step 3-) The SHOWCast environment will be created.
echo:

:PROMPT2
SET /P AREYOUSURE=Do you want to proceed (Y/[N])? 
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END

:: Check if the showcast env is already created
IF EXIST %ParentFolderName%\Miniconda3\envs\showcast\ (
	echo:
   	echo The showcast environment already exists in your Miniconda3 directory at:
    echo %ParentFolderName%\Miniconda3\envs\showcast
    echo If you want to reinstall it, delete the showcast env folder and
    echo execute this installer again.
) ELSE (
	:: if not, update conda (optional) and create the showcast env with mamba
	echo:
	echo Updating conda... [this may take some minutes]
	echo:
	call %ParentFolderName%\Miniconda3\condabin\conda update -n base -c defaults conda --yes
	echo:
	echo Creating the SHOWCast environment with Mamba... [this will take some minutes]
	echo:
	call %ParentFolderName%\Miniconda3\condabin\mamba env create -f %ParentFolderName%\Installer\Miniconda3\environment.yml
)

:END
endlocal

echo:
PAUSE