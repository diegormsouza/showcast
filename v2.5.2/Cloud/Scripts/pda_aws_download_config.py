#######################################################################################################
# LICENSE
# Copyright (C) 2021 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU 
# General Public License as published by the Free Software Foundation, either version 3 of the License, 
# or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without 
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General 
# Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. 
# If not, see http://www.gnu.org/licenses/.
#######################################################################################################
"""
INSTRUCTIONS FOR USERS:

1-) On the "ingest_folder" variable, choose the main folder where the data will be downloaded.

2-) On BUCKETS, choose the satellites you want to download data from (noaa-goes16 or noaa-goes17) 

3-) For each product on the product list, choose:

	- First line: If the product should be downloaded (True) or not (False).

	- Second line: AWS product name (don't change it!)

	- Third line: Which channels should be downloaded for each selected "True" product. The products that 
	  has 'False' on the channels list, are not channel based.

	- Third line (for MESOSCALE only): Which mesoscale sector(s) you wanto to download. 

	- Fourth line: Which minutes (scans) should be downloaded for each selected "True" product. The default 
	  options are the ones available for each product. For example the "SST" is an hourly product, so only 
	  the option '00' is available for it.

	- Fifth line: The folder you want to store your data. In the end, data will be stored on:
	  ingest_folder + product folder + Band (if the product is channel based)
	  Note: The default folder names are just suggestions. Change it to any name you want / need.
	  Also, when downloading GOES-17 data, the folder name will be changed to "GOES-S" instead of "GOES-R"

IMPORTANT: This script was created for the SHOWCast utility, however it might be used as a standalone script
By default, it assumes it is inside a folder called "Cloud" and inside this "Cloud" folder you must have a 
"Logs" folder and an "Apps" folder, with the Rclone software in it. To download Rclone, please access:
https://rclone.org/downloads/	

Note: If you want to use this script to download historical data, just manually change YEAR, JULIAN DAY and 
HOUR, keeping UTC_DIFF as 0 (zero).
"""
__author__ = "Diego Souza"
__copyright__ = "Copyright (C) 2021 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL"
__credits__ = ["Diego Souza", "Demilson Quintão"]
__license__ = "GPL"
__version__ = "2.5.0"
__maintainer__ = "Diego Souza"
__email__ = "diego.souza@inpe.br"
__status__ = "Production"
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Required modules
#------------------------------------------------------------------------------------------------------
import os           					# Miscellaneous operating system interfaces
import subprocess   					# The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
import datetime     					# Basic date and time types
import platform     					# Access to underlying platform’s identifying data
import time as t    					# Time access and conversion
import re           					# Regular expression operations
from os.path import dirname, abspath    # Return a normalized absolutized version of the pathname path 
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Start the time counter
print('Script started.')
start = t.time()  

# Main ingest folder - Where your downloaded data will be stored
ingest_folder = "C://VLAB//Cloud//"       # Windows example
#ingest_folder = "//data//VLAB//Cloud//"  # Linux example

#------------------------------------------------------------------------------------------------------
# PRODUCT SELECTION BY USER
#------------------------------------------------------------------------------------------------------

# Select the desired bucket, in this case, the satellite(s)
BUCKETS = ['noaa-goes19'] # Choose from ['noaa-goes16', 'noaa-goes17', 'noaa-goes18', 'noaa-goes19'] or all

#------------------------------------------------------------------------------------------------------
# ABI L1B BANDS
#------------------------------------------------------------------------------------------------------

# ABI L1b Radiances - CONUS
ABI_L1b_RadC         = False 
ABI_L1b_RadC_Product = 'ABI-L1b-RadC'
ABI_L1b_RadC_Channel = ['C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16']
ABI_L1b_RadC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L1b_RadC_Folders = 'GOES-R-RadC-Imagery//'

# ABI L1b Radiances - FULL DISK
ABI_L1b_RadF         = False 
ABI_L1b_RadF_Product = 'ABI-L1b-RadF'
ABI_L1b_RadF_Channel = ['C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16']
ABI_L1b_RadF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L1b_RadF_Folders = 'GOES-R-RadF-Imagery//'

# ABI L1b Radiances - MESOSCALE
ABI_L1b_RadM         = False 
ABI_L1b_RadM_Product = 'ABI-L1b-RadM'
ABI_L1b_RadM_Channel = ['C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16']
ABI_L1b_RadM_Mesoscl = ['M1', 'M2'] 
ABI_L1b_RadM_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
ABI_L1b_RadM_Folders = 'GOES-R-RadM-Imagery//'

#------------------------------------------------------------------------------------------------------
# ABI L2 BANDS
#------------------------------------------------------------------------------------------------------

# ABI L2 Cloud and Moisture Imagery - CONUS
ABI_L2_CMIPC         = False 
ABI_L2_CMIPC_Product = 'ABI-L2-CMIPC'
ABI_L2_CMIPC_Channel = ['C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16']
ABI_L2_CMIPC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L2_CMIPC_Folders = 'GOES-R-CMIPC-Imagery//'

# ABI L2 Cloud and Moisture Imagery - FULL DISK
ABI_L2_CMIPF         = True 
ABI_L2_CMIPF_Product = 'ABI-L2-CMIPF'
ABI_L2_CMIPF_Channel = ['C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16']
ABI_L2_CMIPF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_CMIPF_Folders = 'GOES-R-CMI-Imagery//'

# ABI L2 Cloud and Moisture Imagery - MESOSCALE
ABI_L2_CMIPM         = False 
ABI_L2_CMIPM_Product = 'ABI-L2-CMIPM'
ABI_L2_CMIPM_Channel = ['C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16']
ABI_L2_CMIPM_Mesoscl = ['M1', 'M2']
ABI_L2_CMIPM_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
ABI_L2_CMIPM_Folders = 'GOES-R-CMIPM-Imagery//'

#------------------------------------------------------------------------------------------------------
# ABI L2 MULTI-BAND FORMAT
#------------------------------------------------------------------------------------------------------

# ABI L2 Cloud and Moisture Imagery (Multi-Band Format) - CONUS
ABI_L2_MCMIPC         = False 
ABI_L2_MCMIPC_Product = 'ABI-L2-MCMIPC'
ABI_L2_MCMIPC_Channel = ['False']
ABI_L2_MCMIPC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L2_MCMIPC_Folders = 'GOES-R-MCMIPC-Imagery//'

# ABI L2 Cloud and Moisture Imagery (Multi-Band Format) - FULL DISK
ABI_L2_MCMIPF         = False 
ABI_L2_MCMIPF_Product = 'ABI-L2-MCMIPF'
ABI_L2_MCMIPF_Channel = ['False']
ABI_L2_MCMIPF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_MCMIPF_Folders = 'GOES-R-MCMIPF-Imagery//'

# ABI L2 Cloud and Moisture Imagery (Multi-Band Format) - MESOSCALE
ABI_L2_MCMIPM         = False 
ABI_L2_MCMIPM_Product = 'ABI-L2-MCMIPM'
ABI_L2_MCMIPM_Channel = ['False']
ABI_L2_MCMIPM_Mesoscl = ['M1', 'M2']
ABI_L2_MCMIPM_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
ABI_L2_MCMIPM_Folders = 'GOES-R-MCMIPM-Imagery//'

#------------------------------------------------------------------------------------------------------
# ABI L2 PRODUCTS
#------------------------------------------------------------------------------------------------------

# ABI L2 Cloud Top Height - CONUS
ABI_L2_ACHAC         = False 
ABI_L2_ACHAC_Product = 'ABI-L2-ACHAC'
ABI_L2_ACHAC_Channel = ['False']
ABI_L2_ACHAC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L2_ACHAC_Folders = 'GOES-R-Level-2-Products//ACHAC//'

# ABI L2 Cloud Top Height - FULL DISK
ABI_L2_ACHAF         = False 
ABI_L2_ACHAF_Product = 'ABI-L2-ACHAF'
ABI_L2_ACHAF_Channel = ['False']
ABI_L2_ACHAF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_ACHAF_Folders = 'GOES-R-Level-2-Products//ACHAF//'

# ABI L2 Cloud Top Height - MESOSCALE
ABI_L2_ACHAM         = False 
ABI_L2_ACHAM_Product = 'ABI-L2-ACHAM'
ABI_L2_ACHAM_Channel = ['False']
ABI_L2_ACHAM_Mesoscl = ['M1', 'M2']
ABI_L2_ACHAM_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
ABI_L2_ACHAM_Folders = 'GOES-R-Level-2-Products//ACHAM//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Cloud Top Temperature - FULL DISK
ABI_L2_ACHTF         = False 
ABI_L2_ACHTF_Product = 'ABI-L2-ACHTF'
ABI_L2_ACHTF_Channel = ['False']
ABI_L2_ACHTF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_ACHTF_Folders = 'GOES-R-Level-2-Products//ACHTF//'

# ABI L2 Cloud Top Temperature - MESOSCALE
ABI_L2_ACHTM         = False 
ABI_L2_ACHTM_Product = 'ABI-L2-ACHTM'
ABI_L2_ACHTM_Channel = ['False']
ABI_L2_ACHTM_Mesoscl = ['M1', 'M2']
ABI_L2_ACHTM_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
ABI_L2_ACHTM_Folders = 'GOES-R-Level-2-Products//ACHTM//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Clear Sky Masks - CONUS
ABI_L2_ACMC         = False 
ABI_L2_ACMC_Product = 'ABI-L2-ACMC'
ABI_L2_ACMC_Channel = ['False']
ABI_L2_ACMC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L2_ACMC_Folders = 'GOES-R-Level-2-Products//ACMC//'

# ABI L2 Clear Sky Masks - FULL DISK
ABI_L2_ACMF         = False 
ABI_L2_ACMF_Product = 'ABI-L2-ACMF'
ABI_L2_ACMF_Channel = ['False']
ABI_L2_ACMF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_ACMF_Folders = 'GOES-R-Level-2-Products//ACMF//'

# ABI L2 Clear Sky Masks - MESOSCALE
ABI_L2_ACMM         = False 
ABI_L2_ACMM_Product = 'ABI-L2-ACMM'
ABI_L2_ACMM_Channel = ['False']
ABI_L2_ACMM_Mesoscl = ['M1', 'M2']
ABI_L2_ACMM_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
ABI_L2_ACMM_Folders = 'GOES-R-Level-2-Products//ACMM//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Cloud Top Phase - CONUS
ABI_L2_ACTPC         = False 
ABI_L2_ACTPC_Product = 'ABI-L2-ACTPC'
ABI_L2_ACTPC_Channel = ['False']
ABI_L2_ACTPC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L2_ACTPC_Folders = 'GOES-R-Level-2-Products//ACTPC//'

# ABI L2 Cloud Top Phase - FULL DISK
ABI_L2_ACTPF         = False 
ABI_L2_ACTPF_Product = 'ABI-L2-ACTPF'
ABI_L2_ACTPF_Channel = ['False']
ABI_L2_ACTPF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_ACTPF_Folders = 'GOES-R-Level-2-Products//ACTPF//'

# ABI L2 Cloud Top Phase - MESOSCALE
ABI_L2_ACTPM         = False 
ABI_L2_ACTPM_Product = 'ABI-L2-ACTPM'
ABI_L2_ACTPM_Channel = ['False']
ABI_L2_ACTPM_Mesoscl = ['M1', 'M2']
ABI_L2_ACTPM_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
ABI_L2_ACTPM_Folders = 'GOES-R-Level-2-Products//ACTPM//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Cloud Top Phase - CONUS
ABI_L2_ADPC         = False 
ABI_L2_ADPC_Product = 'ABI-L2-ADPC'
ABI_L2_ADPC_Channel = ['False']
ABI_L2_ADPC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L2_ADPC_Folders = 'GOES-R-Level-2-Products//ADPC//'

# ABI L2 Cloud Top Phase - FULL DISK
ABI_L2_ADPF         = False 
ABI_L2_ADPF_Product = 'ABI-L2-ADPF'
ABI_L2_ADPF_Channel = ['False']
ABI_L2_ADPF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_ADPF_Folders = 'GOES-R-Level-2-Products//ADPF//'

# ABI L2 Cloud Top Phase - MESOSCALE
ABI_L2_ADPM         = False 
ABI_L2_ADPM_Product = 'ABI-L2-ADPM'
ABI_L2_ADPM_Channel = ['False']
ABI_L2_ADPM_Mesoscl = ['M1', 'M2']
ABI_L2_ADPM_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
ABI_L2_ADPM_Folders = 'GOES-R-Level-2-Products//ADPM//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Aerosol Optical Depth - CONUS
ABI_L2_AODC         = False 
ABI_L2_AODC_Product = 'ABI-L2-AODC'
ABI_L2_AODC_Channel = ['False']
ABI_L2_AODC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L2_AODC_Folders = 'GOES-R-Level-2-Products//AODC//'

# ABI L2 Aerosol Optical Depth - FULL DISK
ABI_L2_AODF         = False 
ABI_L2_AODF_Product = 'ABI-L2-AODF'
ABI_L2_AODF_Channel = ['False']
ABI_L2_AODF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_AODF_Folders = 'GOES-R-Level-2-Products//AODF//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Cloud Optical Depth - CONUS
ABI_L2_CODC         = False 
ABI_L2_CODC_Product = 'ABI-L2-CODC'
ABI_L2_CODC_Channel = ['False']
ABI_L2_CODC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L2_CODC_Folders = 'GOES-R-Level-2-Products//CODC//'

# ABI L2 Cloud Optical Depth - FULL DISK
ABI_L2_CODF         = False 
ABI_L2_CODF_Product = 'ABI-L2-CODF'
ABI_L2_CODF_Channel = ['False']
ABI_L2_CODF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_CODF_Folders = 'GOES-R-Level-2-Products//CODF//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Cloud Optical Depth - CONUS
ABI_L2_CPSC         = False 
ABI_L2_CPSC_Product = 'ABI-L2-CPSC'
ABI_L2_CPSC_Channel = ['False']
ABI_L2_CPSC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L2_CPSC_Folders = 'GOES-R-Level-2-Products//CPSC//'

# ABI L2 Cloud Particle Size - FULL DISK
ABI_L2_CPSF         = False 
ABI_L2_CPSF_Product = 'ABI-L2-CPSF'
ABI_L2_CPSF_Channel = ['False']
ABI_L2_CPSF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_CPSF_Folders = 'GOES-R-Level-2-Products//CPSF//'

# ABI L2 Cloud Particle Size - MESOSCALE
ABI_L2_CPSM         = False 
ABI_L2_CPSM_Product = 'ABI-L2-CPSM'
ABI_L2_CPSM_Channel = ['False']
ABI_L2_CPSM_Mesoscl = ['M1', 'M2']
ABI_L2_CPSM_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
ABI_L2_CPSM_Folders = 'GOES-R-Level-2-Products//CPSM//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Cloud Top Pressure - CONUS
ABI_L2_CTPC         = False 
ABI_L2_CTPC_Product = 'ABI-L2-CTPC'
ABI_L2_CTPC_Channel = ['False']
ABI_L2_CTPC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L2_CTPC_Folders = 'GOES-R-Level-2-Products//CTPC//'

# ABI L2 Cloud Top Pressure - FULL DISK
ABI_L2_CTPF         = False 
ABI_L2_CTPF_Product = 'ABI-L2-CTPF'
ABI_L2_CTPF_Channel = ['False']
ABI_L2_CTPF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_CTPF_Folders = 'GOES-R-Level-2-Products//CTPF//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Derived Motion Winds - CONUS
ABI_L2_DMWC         = False 
ABI_L2_DMWC_Product = 'ABI-L2-DMWC'
ABI_L2_DMWC_Channel = ['C02', 'C07', 'C08', 'C09', 'C10', 'C14']
ABI_L2_DMWC_Minutes = ['01', '16', '31', '46']
ABI_L2_DMWC_Folders = 'GOES-R-Level-2-Products//DMWC//'

# ABI L2 Derived Motion Winds - FULL DISK
ABI_L2_DMWF         = False 
ABI_L2_DMWF_Product = 'ABI-L2-DMWF'
ABI_L2_DMWF_Channel = ['C02', 'C07', 'C08', 'C09', 'C10', 'C14']
ABI_L2_DMWF_Minutes = ['00']
ABI_L2_DMWF_Folders = 'GOES-R-Level-2-Products//DMWF//'

# ABI L2 Derived Motion Winds - MESOSCALE
ABI_L2_DMWM         = False 
ABI_L2_DMWM_Product = 'ABI-L2-DMWM'
ABI_L2_DMWM_Channel = ['C02', 'C07', 'C08', 'C09', 'C10', 'C14']
ABI_L2_DMWM_Mesoscl = ['M1', 'M2']
ABI_L2_DMWM_Minutes = ['01', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55']
ABI_L2_DMWM_Folders = 'GOES-R-Level-2-Products//DMWM//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Derived Stability Indices - CONUS 
ABI_L2_DSIC         = False 
ABI_L2_DSIC_Product = 'ABI-L2-DSIC'
ABI_L2_DSIC_Channel = ['False']
ABI_L2_DSIC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L2_DSIC_Folders = 'GOES-R-Level-2-Products//DSIC//'

# ABI L2 Derived Stability Indices - FULL DISK 
ABI_L2_DSIF         = False 
ABI_L2_DSIF_Product = 'ABI-L2-DSIF'
ABI_L2_DSIF_Channel = ['False']
ABI_L2_DSIF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_DSIF_Folders = 'GOES-R-Level-2-Products//DSIF//'

# ABI L2 Derived Stability Indices - MESOSCALE 
ABI_L2_DSIM         = False 
ABI_L2_DSIM_Product = 'ABI-L2-DSIM'
ABI_L2_DSIM_Channel = ['False']
ABI_L2_DSIM_Mesoscl = ['M1', 'M2']
ABI_L2_DSIM_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
ABI_L2_DSIM_Folders = 'GOES-R-Level-2-Products//DSIM//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Downward Shortwave Radiation - CONUS
ABI_L2_DSRC         = False 
ABI_L2_DSRC_Product = 'ABI-L2-DSRC'
ABI_L2_DSRC_Channel = ['False']
ABI_L2_DSRC_Minutes = ['01']
ABI_L2_DSRC_Folders = 'GOES-R-Level-2-Products//DSRC//'

# ABI L2 Downward Shortwave Radiation - FULL DISK
ABI_L2_DSRF         = False 
ABI_L2_DSRF_Product = 'ABI-L2-DSRF'
ABI_L2_DSRF_Channel = ['False']
ABI_L2_DSRF_Minutes = ['00']
ABI_L2_DSRF_Folders = 'GOES-R-Level-2-Products//DSRF//'

# ABI L2 Downward Shortwave Radiation - MESOSCALE
ABI_L2_DSRM         = False 
ABI_L2_DSRM_Product = 'ABI-L2-DSRM'
ABI_L2_DSRM_Channel = ['False']
ABI_L2_DSRM_Mesoscl = ['M1', 'M2']
ABI_L2_DSRM_Minutes = ['00']
ABI_L2_DSRM_Folders = 'GOES-R-Level-2-Products//DSRM//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Fire-Hot Spot Characterization - CONUS
ABI_L2_FDCC         = False 
ABI_L2_FDCC_Product = 'ABI-L2-FDCC'
ABI_L2_FDCC_Channel = ['False']
ABI_L2_FDCC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L2_FDCC_Folders = 'GOES-R-Level-2-Products//FDCC//'

# ABI L2 Fire-Hot Spot Characterization - FULL DISK
ABI_L2_FDCF         = False 
ABI_L2_FDCF_Product = 'ABI-L2-FDCF'
ABI_L2_FDCF_Channel = ['False']
ABI_L2_FDCF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_FDCF_Folders = 'GOES-R-Level-2-Products//FDCF//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Land Surface Temperature - CONUS
ABI_L2_LSTC         = False 
ABI_L2_LSTC_Product = 'ABI-L2-LSTC'
ABI_L2_LSTC_Channel = ['False']
ABI_L2_LSTC_Minutes = ['01']
ABI_L2_LSTC_Folders = 'GOES-R-Level-2-Products//LSTC//'

# ABI L2 Land Surface Temperature - FULL DISK
ABI_L2_LSTF         = False 
ABI_L2_LSTF_Product = 'ABI-L2-LSTF'
ABI_L2_LSTF_Channel = ['False']
ABI_L2_LSTF_Minutes = ['00']
ABI_L2_LSTF_Folders = 'GOES-R-Level-2-Products//LSTF//'

# ABI L2 Land Surface Temperature - MESOSCALE
ABI_L2_LSTM         = False 
ABI_L2_LSTM_Product = 'ABI-L2-LSTM'
ABI_L2_LSTM_Channel = ['False']
ABI_L2_LSTM_Mesoscl = ['M1', 'M2']
ABI_L2_LSTM_Minutes = ['00']
ABI_L2_LSTM_Folders = 'GOES-R-Level-2-Products//LSTM//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Legacy Vertical Moisture Profile - CONUS
ABI_L2_LVMPC         = False 
ABI_L2_LVMPC_Product = 'ABI-L2-LVMPC'
ABI_L2_LVMPC_Channel = ['False']
ABI_L2_LVMPC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L2_LVMPC_Folders = 'GOES-R-Level-2-Products//LVMPC//'

# ABI L2 Legacy Vertical Moisture Profile - FULL DISK
ABI_L2_LVMPF         = False 
ABI_L2_LVMPF_Product = 'ABI-L2-LVMPF'
ABI_L2_LVMPF_Channel = ['False']
ABI_L2_LVMPF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_LVMPF_Folders = 'GOES-R-Level-2-Products//LVMPF//'

# ABI L2 Legacy Vertical Moisture Profile - MESOSCALE
ABI_L2_LVMPM         = False 
ABI_L2_LVMPM_Product = 'ABI-L2-LVMPM'
ABI_L2_LVMPM_Channel = ['False']
ABI_L2_LVMPM_Mesoscl = ['M1', 'M2']
ABI_L2_LVMPM_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
ABI_L2_LVMPM_Folders = 'GOES-R-Level-2-Products//LVMPM//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Legacy Vertical Temperature Profile - CONUS
ABI_L2_LVTPC         = False 
ABI_L2_LVTPC_Product = 'ABI-L2-LVTPC'
ABI_L2_LVTPC_Channel = ['False']
ABI_L2_LVTPC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L2_LVTPC_Folders = 'GOES-R-Level-2-Products//LVTPC//'

# ABI L2 Legacy Vertical Temperature Profile - FULL DISK
ABI_L2_LVTPF         = False 
ABI_L2_LVTPF_Product = 'ABI-L2-LVTPF'
ABI_L2_LVTPF_Channel = ['False']
ABI_L2_LVTPF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_LVTPF_Folders = 'GOES-R-Level-2-Products//LVTPF//'

# ABI L2 Legacy Vertical Temperature Profile - MESOSCALE
ABI_L2_LVTPM         = False 
ABI_L2_LVTPM_Product = 'ABI-L2-LVTPM'
ABI_L2_LVTPM_Channel = ['False']
ABI_L2_LVTPM_Mesoscl = ['M1', 'M2']
ABI_L2_LVTPM_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
ABI_L2_LVTPM_Folders = 'GOES-R-Level-2-Products//LVTPM//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Rainfall Rate - Quantitative Prediction Estimate - FULL DISK
ABI_L2_RRQPEF         = False 
ABI_L2_RRQPEF_Product = 'ABI-L2-RRQPEF'
ABI_L2_RRQPEF_Channel = ['False']
ABI_L2_RRQPEF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_RRQPEF_Folders = 'GOES-R-Level-2-Products//RRQPEF//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Reflected Shortwave Radiation - CONUS
ABI_L2_RSRC         = False 
ABI_L2_RSRC_Product = 'ABI-L2-RSRC'
ABI_L2_RSRC_Channel = ['False']
ABI_L2_RSRC_Minutes = ['01']
ABI_L2_RSRC_Folders = 'GOES-R-Level-2-Products//RSRC//'

# ABI L2 Reflected Shortwave Radiation - FULL DISK
ABI_L2_RSRF         = False 
ABI_L2_RSRF_Product = 'ABI-L2-RSRF'
ABI_L2_RSRF_Channel = ['False']
ABI_L2_RSRF_Minutes = ['00']
ABI_L2_RSRF_Folders = 'GOES-R-Level-2-Products//RSRF//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Sea Surface (Skin) Temperature - FULL DISK 
ABI_L2_SSTF         = False 
ABI_L2_SSTF_Product = 'ABI-L2-SSTF'
ABI_L2_SSTF_Channel = ['False']
ABI_L2_SSTF_Minutes = ['00']
ABI_L2_SSTF_Folders = 'GOES-R-Level-2-Products//SSTF//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Legacy Vertical Temperature Profile - CONUS
ABI_L2_TPWC         = False 
ABI_L2_TPWC_Product = 'ABI-L2-TPWC'
ABI_L2_TPWC_Channel = ['False']
ABI_L2_TPWC_Minutes = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
ABI_L2_TPWC_Folders = 'GOES-R-Level-2-Products//TPWC//'

# ABI L2 Legacy Vertical Temperature Profile - FULL DISK
ABI_L2_TPWF         = False 
ABI_L2_TPWF_Product = 'ABI-L2-TPWF'
ABI_L2_TPWF_Channel = ['False']
ABI_L2_TPWF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_TPWF_Folders = 'GOES-R-Level-2-Products//TPWF//'

# ABI L2 Legacy Vertical Temperature Profile - MESOSCALE
ABI_L2_TPWM         = False 
ABI_L2_TPWM_Product = 'ABI-L2-TPWM'
ABI_L2_TPWM_Channel = ['False']
ABI_L2_TPWM_Mesoscl = ['M1', 'M2']
ABI_L2_TPWM_Minutes = 		['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
ABI_L2_TPWM_Folders = 'GOES-R-Level-2-Products//TPWM//'

#------------------------------------------------------------------------------------------------------

# ABI L2 Volcanic Ash: Detection and Height - FULL DISK
ABI_L2_VAAF         = False 
ABI_L2_VAAF_Product = 'ABI-L2-VAAF'
ABI_L2_VAAF_Channel = ['False']
ABI_L2_VAAF_Minutes = ['00', '10', '20', '30', '40', '50']
ABI_L2_VAAF_Folders = 'GOES-R-Level-2-Products//VAAF//'

#------------------------------------------------------------------------------------------------------
# GLM L2 Lightning Detection
#------------------------------------------------------------------------------------------------------

# GLM L2 Lightning Detection
GLM_L2_LCFA         = False 
GLM_L2_LCFA_Product = 'GLM-L2-LCFA'
GLM_L2_LCFA_Channel = ['False']
GLM_L2_LCFA_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
GLM_L2_LCFA_Folders = 'GOES-R-GLM-Products//LCFA//'

#------------------------------------------------------------------------------------------------------
# SUVI PRODUCTS
#------------------------------------------------------------------------------------------------------

# Solar Ultraviolet Imager L1b Extreme Ultraviolet Fe093
SUVI_L1b_Fe093         = False 
SUVI_L1b_Fe093_Product = 'SUVI-L1b-Fe093'
SUVI_L1b_Fe093_Channel = ['False']
SUVI_L1b_Fe093_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
SUVI_L1b_Fe093_Folders = 'GOES-R-SUVI-Products//Fe093//'

# Solar Ultraviolet Imager L1b Extreme Ultraviolet Fe13
SUVI_L1b_Fe13         = False 
SUVI_L1b_Fe13_Product = 'SUVI-L1b-Fe13'
SUVI_L1b_Fe13_Channel = ['False']
SUVI_L1b_Fe13_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
SUVI_L1b_Fe13_Folders = 'GOES-R-SUVI-Products//Fe13//'

# Solar Ultraviolet Imager L1b Extreme Ultraviolet Fe131
SUVI_L1b_Fe131         = False 
SUVI_L1b_Fe131_Product = 'SUVI-L1b-Fe131'
SUVI_L1b_Fe131_Channel = ['False']
SUVI_L1b_Fe131_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
SUVI_L1b_Fe131_Folders = 'GOES-R-SUVI-Products//Fe131//'

# Solar Ultraviolet Imager L1b Extreme Ultraviolet Fe17
SUVI_L1b_Fe17         = False 
SUVI_L1b_Fe17_Product = 'SUVI-L1b-Fe17'
SUVI_L1b_Fe17_Channel = ['False']
SUVI_L1b_Fe17_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
SUVI_L1b_Fe17_Folders = 'GOES-R-SUVI-Products//Fe17//'

# Solar Ultraviolet Imager L1b Extreme Ultraviolet Fe171
SUVI_L1b_Fe171         = False 
SUVI_L1b_Fe171_Product = 'SUVI-L1b-Fe171'
SUVI_L1b_Fe171_Channel = ['False']
SUVI_L1b_Fe171_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
SUVI_L1b_Fe171_Folders = 'GOES-R-SUVI-Products//Fe171//'

# Solar Ultraviolet Imager L1b Extreme Ultraviolet Fe195
SUVI_L1b_Fe195         = False 
SUVI_L1b_Fe195_Product = 'SUVI-L1b-Fe195'
SUVI_L1b_Fe195_Channel = ['False']
SUVI_L1b_Fe195_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
SUVI_L1b_Fe195_Folders = 'GOES-R-SUVI-Products//Fe195//'

# Solar Ultraviolet Imager L1b Extreme Ultraviolet Fe284
SUVI_L1b_Fe284         = False 
SUVI_L1b_Fe284_Product = 'SUVI-L1b-Fe284'
SUVI_L1b_Fe284_Channel = ['False']
SUVI_L1b_Fe284_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
SUVI_L1b_Fe284_Folders = 'GOES-R-SUVI-Products//Fe284//'

# Solar Ultraviolet Imager L1b Extreme Ultraviolet He303
SUVI_L1b_He303         = False 
SUVI_L1b_He303_Product = 'SUVI-L1b-He303'
SUVI_L1b_He303_Channel = ['False']
SUVI_L1b_He303_Minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
SUVI_L1b_He303_Folders = 'GOES-R-SUVI-Products//He303//'

#------------------------------------------------------------------------------------------------------
# PRODUCT SELECTION END
#------------------------------------------------------------------------------------------------------

# Variable that will store the desired products
PRODUCTS = []

# DO NOT CHANGE the lines below
if (ABI_L1b_RadC == True): PRODUCTS.append(ABI_L1b_RadC_Product)
if (ABI_L1b_RadF == True): PRODUCTS.append(ABI_L1b_RadF_Product)
if (ABI_L1b_RadM == True): PRODUCTS.append(ABI_L1b_RadM_Product)
if (ABI_L2_CMIPC == True): PRODUCTS.append(ABI_L2_CMIPC_Product)
if (ABI_L2_CMIPF == True): PRODUCTS.append(ABI_L2_CMIPF_Product)
if (ABI_L2_CMIPM == True): PRODUCTS.append(ABI_L2_CMIPM_Product)
if (ABI_L2_MCMIPC == True): PRODUCTS.append(ABI_L2_MCMIPC_Product)
if (ABI_L2_MCMIPF == True): PRODUCTS.append(ABI_L2_MCMIPF_Product) 
if (ABI_L2_MCMIPM == True): PRODUCTS.append(ABI_L2_MCMIPM_Product)
if (ABI_L2_ACHAC == True): PRODUCTS.append(ABI_L2_ACHAC_Product)
if (ABI_L2_ACHAF == True): PRODUCTS.append(ABI_L2_ACHAF_Product)
if (ABI_L2_ACHAM == True): PRODUCTS.append(ABI_L2_ACHAM_Product)
if (ABI_L2_ACHTF == True): PRODUCTS.append(ABI_L2_ACHTF_Product)
if (ABI_L2_ACHTM == True): PRODUCTS.append(ABI_L2_ACHTM_Product)
if (ABI_L2_ACMC == True): PRODUCTS.append(ABI_L2_ACMC_Product)
if (ABI_L2_ACMF == True): PRODUCTS.append(ABI_L2_ACMF_Product)
if (ABI_L2_ACMM == True): PRODUCTS.append(ABI_L2_ACMM_Product)
if (ABI_L2_ACTPC == True): PRODUCTS.append(ABI_L2_ACTPC_Product)
if (ABI_L2_ACTPF == True): PRODUCTS.append(ABI_L2_ACTPF_Product)
if (ABI_L2_ACTPM == True): PRODUCTS.append(ABI_L2_ACTPM_Product)
if (ABI_L2_ADPC == True): PRODUCTS.append(ABI_L2_ADPC_Product)
if (ABI_L2_ADPF == True): PRODUCTS.append(ABI_L2_ADPF_Product)
if (ABI_L2_ADPM == True): PRODUCTS.append(ABI_L2_ADPM_Product)
if (ABI_L2_AODC == True): PRODUCTS.append(ABI_L2_AODC_Product)
if (ABI_L2_AODF == True): PRODUCTS.append(ABI_L2_AODF_Product)
if (ABI_L2_CODC == True): PRODUCTS.append(ABI_L2_CODC_Product)
if (ABI_L2_CODF == True): PRODUCTS.append(ABI_L2_CODF_Product)
if (ABI_L2_CPSC == True): PRODUCTS.append(ABI_L2_CPSC_Product)
if (ABI_L2_CPSF == True): PRODUCTS.append(ABI_L2_CPSF_Product)
if (ABI_L2_CPSM == True): PRODUCTS.append(ABI_L2_CPSM_Product)
if (ABI_L2_CTPC == True): PRODUCTS.append(ABI_L2_CTPC_Product)
if (ABI_L2_CTPF == True): PRODUCTS.append(ABI_L2_CTPF_Product)
if (ABI_L2_DMWC == True): PRODUCTS.append(ABI_L2_DMWC_Product)
if (ABI_L2_DMWF == True): PRODUCTS.append(ABI_L2_DMWF_Product)
if (ABI_L2_DMWM == True): PRODUCTS.append(ABI_L2_DMWM_Product)
if (ABI_L2_DSIC == True): PRODUCTS.append(ABI_L2_DSIC_Product)
if (ABI_L2_DSIF == True): PRODUCTS.append(ABI_L2_DSIF_Product)
if (ABI_L2_DSIM == True): PRODUCTS.append(ABI_L2_DSIM_Product)
if (ABI_L2_DSRC == True): PRODUCTS.append(ABI_L2_DSRC_Product)
if (ABI_L2_DSRF == True): PRODUCTS.append(ABI_L2_DSRF_Product)
if (ABI_L2_DSRM == True): PRODUCTS.append(ABI_L2_DSRM_Product)
if (ABI_L2_FDCC == True): PRODUCTS.append(ABI_L2_FDCC_Product)
if (ABI_L2_FDCF == True): PRODUCTS.append(ABI_L2_FDCF_Product)
if (ABI_L2_LSTC == True): PRODUCTS.append(ABI_L2_LSTC_Product)
if (ABI_L2_LSTF == True): PRODUCTS.append(ABI_L2_LSTF_Product)
if (ABI_L2_LSTM == True): PRODUCTS.append(ABI_L2_LSTM_Product)
if (ABI_L2_LVMPC == True): PRODUCTS.append(ABI_L2_LVMPC_Product)
if (ABI_L2_LVMPF == True): PRODUCTS.append(ABI_L2_LVMPF_Product)
if (ABI_L2_LVMPM == True): PRODUCTS.append(ABI_L2_LVMPM_Product)
if (ABI_L2_LVTPC == True): PRODUCTS.append(ABI_L2_LVTPC_Product)
if (ABI_L2_LVTPF == True): PRODUCTS.append(ABI_L2_LVTPF_Product)
if (ABI_L2_LVTPM == True): PRODUCTS.append(ABI_L2_LVTPM_Product)
if (ABI_L2_RRQPEF == True): PRODUCTS.append(ABI_L2_RRQPEF_Product)
if (ABI_L2_RSRC == True): PRODUCTS.append(ABI_L2_RSRC_Product)
if (ABI_L2_RSRF == True): PRODUCTS.append(ABI_L2_RSRF_Product)
if (ABI_L2_SSTF == True): PRODUCTS.append(ABI_L2_SSTF_Product)
if (ABI_L2_TPWC == True): PRODUCTS.append(ABI_L2_TPWC_Product)
if (ABI_L2_TPWF == True): PRODUCTS.append(ABI_L2_TPWF_Product)
if (ABI_L2_TPWM == True): PRODUCTS.append(ABI_L2_TPWM_Product)
if (ABI_L2_VAAF == True): PRODUCTS.append(ABI_L2_LSTF_Product)
if (GLM_L2_LCFA == True): PRODUCTS.append(GLM_L2_LCFA_Product)
if (SUVI_L1b_Fe093 == True): PRODUCTS.append(SUVI_L1b_Fe093_Product)
if (SUVI_L1b_Fe13 == True): PRODUCTS.append(SUVI_L1b_Fe13_Product)
if (SUVI_L1b_Fe131 == True): PRODUCTS.append(SUVI_L1b_Fe131_Product)
if (SUVI_L1b_Fe17 == True): PRODUCTS.append(SUVI_L1b_Fe17_Product)
if (SUVI_L1b_Fe171 == True): PRODUCTS.append(SUVI_L1b_Fe171_Product)
if (SUVI_L1b_Fe195 == True): PRODUCTS.append(SUVI_L1b_Fe195_Product)
if (SUVI_L1b_Fe284 == True): PRODUCTS.append(SUVI_L1b_Fe284_Product)
if (SUVI_L1b_He303 == True): PRODUCTS.append(SUVI_L1b_He303_Product)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# SHOWCast directory:
main_dir = dirname(dirname(dirname(abspath(__file__))))

# Detecing the O.S.
osystem = platform.system()
if osystem == "Windows": 
	extension = '.exe'
else:
	extension = ''

# Create the tmp directory if it doesn't exist
tmp_dir = main_dir + '//Cloud//Scripts//tmp//'
os.makedirs(tmp_dir, exist_ok=True)
	
print ("") 
print ("--------------------------------------------------------") 
print ("GOES-R Big Data Python / Rclone Downloader: Current Data")
print ("--------------------------------------------------------") 
print ("") 

#------------------------------------------------------------------------------------------------------
# GETTING CURRENT TIME AND DATE
#------------------------------------------------------------------------------------------------------
# Checking the current time and date based on your machine local time.
# Note: We could use an online time server, however ntp servers access is restricted in some networks.  
# You may use ntp servers if you wish.

# Get the current time in UTC
from datetime import timezone

YEAR = str(datetime.datetime.now(timezone.utc).year)                               # Year got from local machine
JULIAN_DAY = str(datetime.datetime.now(timezone.utc).timetuple().tm_yday).zfill(3) # Julian day got from local machine
HOUR = str(datetime.datetime.now(timezone.utc).hour).zfill(2)                      # Hour got from local machine corrected for UTC

# Checking if it is a leap year
import calendar
if (calendar.isleap(int(YEAR)) == True):
	last_day = 366 # if it is a leap year, the last julian day is 366
else:
	last_day = 365 # if it is NOT a leap year, the last julian day is 365

# Printing Time and Data information for user check
print("Current year, julian day and hour based on your local machine:")
print("YEAR: ", YEAR)
print("JULIAN DAY (UTC): ", JULIAN_DAY)
print("HOUR (UTC): ", HOUR)
print("")

#------------------------------------------------------------------------------------------------------
# DATA DOWNLOAD LOOP
#------------------------------------------------------------------------------------------------------

for BUCKET in BUCKETS: # Loop through satellites 

	for product in PRODUCTS: # Loop through products 

		PRODUCT = globals()[product.replace("-", "_")+"_Product"]
		CHANNEL = globals()[product.replace("-", "_")+"_Channel"]
		MINUTES = globals()[product.replace("-", "_")+"_Minutes"]
		OUTDIR  = ingest_folder + globals()[product.replace("-", "_")+"_Folders"]
		
		if (BUCKET == 'noaa-goes17'): OUTDIR = OUTDIR.replace("-R-", "-S-") # If GOES-17, replace -R- for -S- on the folders name.
   		if (BUCKET == 'noaa-goes18'): OUTDIR = OUTDIR.replace("-R-", "-T-") # If GOES-18, replace -R- for -T- on the folders name.
		if (BUCKET == 'noaa-goes19'): OUTDIR = OUTDIR.replace("-R-", "-R-") # If GOES-19, keep -R-
        
		# Create the product output directory if it doesn't exist
		if not os.path.exists(OUTDIR):
			os.makedirs(OUTDIR, exist_ok=True)
			
		# Checking if it is a Mesoscale product
		if (product[-1] == "M"): 

			MESOSCL = globals()[product.replace("-", "_")+"_Mesoscl"]

			for channel in CHANNEL:
			
				for mesoscale in MESOSCL:
				
					# Get output from rclone command, based on the desired data
					print ("--------------------------------------------------------") 
					print ("")
					print("Command used:")
					
					if osystem == "Windows": 
						#print(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'ls publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/")
						files = subprocess.check_output(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'ls publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/", shell=True)
					else:
						#print(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'ls publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/" + " --config " + main_dir + '//Cloud//Apps//' + 'rclone.conf')
						files = subprocess.check_output(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'ls publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/" + " --config " + main_dir + '//Cloud//Apps//' + 'rclone.conf', shell=True)
					
					# Change type from 'bytes' to 'string'
					files = files.decode()
					# Split files based on the new line and remove the empty item at the end.
					files = files.split('\n')
					files.remove('')
					
					if (channel != 'False'):
						# Get only the file names for an specific channel
						files = [x for x in files if channel in x ]
						OUTDIR = ingest_folder + globals()[product.replace("-", "_")+"_Folders"] + 'Band' + channel[-2:] + '//'
						if not os.path.exists(OUTDIR):
							os.makedirs(OUTDIR, exist_ok=True)
					
					# Get only the file names for an specific mesoscale sector
					files = [x for x in files if mesoscale + '-' in x ]
					
					# Get only the file names, without the file sizes
					files = [i.split(" ")[-1] for i in files]
					# Print the file names list
					#print ("File list for this particular time, date and channel:")
					#for i in files:
					#    print(i)
				
					# If there aren't files available yet
					if not files:
						print("")
						print("No files available yet... Exiting script")
						print("")
						break # No new files available in the cloud yet. Exiting the loop.
				
					print("")
					print("File Name: ", files[-1])
					print("")		
					print("Checking if the file is on the daily log...")
					# If the log file doesn't exist yet, create one
					file = open(main_dir + '//Cloud//Logs//' +'pda_aws_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a')
					file.close()
					# Put all file names on the log in a list
					log = []
				
					# Open the log to check the files already processed 
					with open(main_dir + '//Cloud//Logs//' +'pda_aws_log_' + str(datetime.datetime.now())[0:10] + '.txt') as f:
						log = f.readlines()
						# Remove the line feeds
						log = [x.strip() for x in log]
					
					# If a given file is not on the log
					if files[-1] not in log:
						print("")
						print ("Checking if the file is from a desired minute...")
					
						# Search in the file name if the image from GOES is from a desired minute.
						matches = 0 # Initialize matches
						for minute in MINUTES: 
							#print(minute)
							#print(r'(?:s.........' + str(minute) + ')..._')
							regex = re.compile(r'(?:s.........' + str(minute) + ')..._')
							finder = re.findall(regex, files[-1])
							# If "matches" is "0", it is not from a desired minute. If it is "1", we may download the file
							matches = len(finder)
							#print(matches)
							# If it is from a desired minute, exit verification loop
							if (matches == 1): break
							
						if matches == 0: # If there are no matches
							print("This is not an image from a desired minute... Exiting loop.")
							# Put the processed file on the log
							import datetime   # Basic Date and Time types
							with open(main_dir + '//Cloud//Logs//' +'pda_aws_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
								log.write(str(datetime.datetime.now()))
								log.write('\n')
								log.write(files[-1] + '\n')
								log.write('\n')
							break # This is not an image from minute 20 or 50. Exiting the loop.
						else:
							if (channel != 'False'):
								print ("")
								print ("Downloading the most recent file for channel: ", channel)
							else:
								print ("")
								print ("Downloading the most recent file: ")
							
							# Download the most recent file for this particular hour
							print(files[-1])
							if osystem == "Windows": 
								#print(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'copy publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/" + files[-1] + " " + OUTDIR)
								os.system(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'copy publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/" + files[-1] + " " + tmp_dir)
								# When the download is finished, move the file to the final directory
								import shutil
								shutil.move(tmp_dir + files[-1], OUTDIR + files[-1])
							else:
								#print(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'copy publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/" + files[-1] + " " + OUTDIR  + " --config " + main_dir + '//Cloud//Apps//' + 'rclone.conf')
								os.system(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'copy publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/" + files[-1] + " " + tmp_dir + " --config " + main_dir + '//Cloud//Apps//' + 'rclone.conf')
								# When the download is finished, move the file to the final directory
								import shutil
								shutil.move(tmp_dir + files[-1], OUTDIR + files[-1])
							print ("")
							print ("Download finished!") 
							print ("Putting the file name on the daily log...")
							print("")

							#---------------------------------------------------------------------------------------------
							#---------------------------------------------------------------------------------------------
				
							# Put the processed file on the log
							import datetime   # Basic Date and Time types
							with open(main_dir + '//Cloud//Logs//' +'pda_aws_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
								log.write(str(datetime.datetime.now()))
								log.write('\n')
								log.write(files[-1] + '\n')
								log.write('\n')
					else:
						print("This file was already downloaded.")
						print("")

		else: # It is not a meso, so doesn't include mesoscale check

			for channel in CHANNEL:
			
				# Get output from rclone command, based on the desired data
				print ("--------------------------------------------------------") 
				print ("")
				print("Command used:")
				if osystem == "Windows": 
					#print(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'ls publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/")
					files = subprocess.check_output(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'ls publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/", shell=True)
				else:
					#print(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'ls publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/" + " --config " + main_dir + '//Cloud//Apps//' + 'rclone.conf')
					files = subprocess.check_output(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'ls publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/" + " --config " + main_dir + '//Cloud//Apps//' + 'rclone.conf', shell=True)
				# Change type from 'bytes' to 'string'
				files = files.decode()
				# Split files based on the new line and remove the empty item at the end.
				files = files.split('\n')
				files.remove('')
				
				if (channel != 'False'):
					# Get only the file names for an specific channel
					files = [x for x in files if channel in x ]
					OUTDIR = ingest_folder + globals()[product.replace("-", "_")+"_Folders"] + 'Band' + channel[-2:] + '//'
					if not os.path.exists(OUTDIR):
						os.makedirs(OUTDIR, exist_ok=True)
							
				# Get only the file names, without the file sizes
				files = [i.split(" ")[-1] for i in files]
				# Print the file names list
				#print ("File list for this particular time, date and channel:")
				#for i in files:
				#    print(i)
			
				# If there aren't files available yet
				if not files:
					print("")
					print("No files available yet... Exiting script")
					print("")
					break # No new files available in the cloud yet. Exiting the loop.
			
				print("")
				print("File Name: ", files[-1])
				print("")		
				print("Checking if the file is on the daily log...")
				# If the log file doesn't exist yet, create one
				file = open(main_dir + '//Cloud//Logs//' +'pda_aws_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a')
				file.close()
				# Put all file names on the log in a list
				log = []
			
				# Open the log to check the files already processed 
				with open(main_dir + '//Cloud//Logs//' +'pda_aws_log_' + str(datetime.datetime.now())[0:10] + '.txt') as f:
					log = f.readlines()
					# Remove the line feeds
					log = [x.strip() for x in log]
				
				# If a given file is not on the log
				if files[-1] not in log:
					print("")
					print ("Checking if the file is from a desired minute...")
				
					# Search in the file name if the image from GOES is from a desired minute.
					matches = 0 # Initialize matches
					for minute in MINUTES: 
						#print(minute)
						#print(r'(?:s.........' + str(minute) + ')..._')
						regex = re.compile(r'(?:s.........' + str(minute) + ')..._')
						finder = re.findall(regex, files[-1])
						# If "matches" is "0", it is not from a desired minute. If it is "1", we may download the file
						matches = len(finder)
						#print(matches)
						# If it is from a desired minute, exit verification loop
						if (matches == 1): break
						
					if matches == 0: # If there are no matches
						print("This is not an image from a desired minute... Exiting loop.")
						# Put the processed file on the log
						import datetime   # Basic Date and Time types
						with open(main_dir + '//Cloud//Logs//' +'pda_aws_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
							log.write(str(datetime.datetime.now()))
							log.write('\n')
							log.write(files[-1] + '\n')
							log.write('\n')
						break # This is not an image from minute 20 or 50. Exiting the loop.
					else:
						if (channel != 'False'):
							print ("")
							print ("Downloading the most recent file for channel: ", channel)
						else:
							print ("")
							print ("Downloading the most recent file: ")
						
						# Download the most recent file for this particular hour
						print(files[-1])
						if osystem == "Windows": 
							#print(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'copy publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/" + files[-1] + " " + OUTDIR)
							os.system(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'copy publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/" + files[-1] + " " + tmp_dir)
							# When the download is finished, move the file to the final directory
							import shutil
							shutil.move(tmp_dir + files[-1], OUTDIR + files[-1])
						else:
							#print(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'copy publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/" + files[-1] + " " + OUTDIR  + " --config " + main_dir + '//Cloud//Apps//' + 'rclone.conf')
							os.system(main_dir + '//Cloud//Apps//' + 'rclone' + extension + " " + 'copy publicAWS:' + BUCKET + "/" + PRODUCT + "/" + YEAR + "/" + JULIAN_DAY + "/" + HOUR + "/" + files[-1] + " " + tmp_dir  + " --config " + main_dir + '//Cloud//Apps//' + 'rclone.conf')
							# When the download is finished, move the file to the final directory
							import shutil
							shutil.move(tmp_dir + files[-1], OUTDIR + files[-1])
						print ("")
						print ("Download finished!") 
						print ("Putting the file name on the daily log...")
						print("")

						#---------------------------------------------------------------------------------------------
						#---------------------------------------------------------------------------------------------
			
						# Put the processed file on the log
						import datetime   # Basic Date and Time types
						with open(main_dir + '//Cloud//Logs//' +'pda_aws_log_' + str(datetime.datetime.now())[0:10] + '.txt', 'a') as log:
							log.write(str(datetime.datetime.now()))
							log.write('\n')
							log.write(files[-1] + '\n')
							log.write('\n')
				else:
					print("This file was already downloaded.")
					print("")

#------------------------------------------------------------------------------------------------------
# SCRIPT END
#------------------------------------------------------------------------------------------------------

print('Total processing time:', round((t.time() - start),2), 'seconds.') 
print("")