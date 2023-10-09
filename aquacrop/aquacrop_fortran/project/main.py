import os
import shutil
from aquacrop.tools.meteo_downloader import get_nasa_power_meteo_data
from aquacrop.tools.elevation_downloader import get_elevation_by_point
from aquacrop.tools.format_aquacrop import format_aquacrop_meteo, format_aquacrop_calendar, modify_aquacrop_crop, get_crop_parameters_dict
from aquacrop.models.fao_56_reference_evapotranspiration import et0_calculation

#USER DEFINED PARAMETERS
#Project name
project_name = 'Menkovo_2023'
#Latitude in degrees (from -90 to 90)
latitude = 59.425032
#Longitude in degrees (from -180 to 180)
longitude = 30.031902
# Simulation start date (yyyymmdd)
simulation_start = 20230401
#Simulation end date (yyyymmdd)
simulation_end = 20230901
#Onset of the growing period (yyyymmdd)
growing_season_start = 20230425
#Output folder
outputs = 'C:/Users/user/Documents/AgroDT_AquaCrop/aquacrop/outputs/'
#Project folder
aquacrop_project_path = 'C:/Users/user/Documents/AGRODT_AquaCrop/aquacrop/aquacrop_fortran/project'
aquacrop_data = os.path.join(aquacrop_project_path, 'DATA')
#Define crop
# CROP LIST: crop_list = os.listdir('./CROPS')
# CROP PARAMETERS: crop_parameters = get_crop_parameters_dict(cropfile_path=os.path.join(aquacrop_project_path, 'CROPS', crop))
crop = 'Canola.CRO'
#Crop parameters to modify
crop_parameters_dict_modify = {'Maximum canopy cover (CCx) in fraction soil cover': '0.70'}

#GET ELEVATION (ALTITUDE)
altitude = get_elevation_by_point(latitude=latitude,
                                  longitude=longitude)

#DOWNLOAD METEODATA FROM NASAPOWER AND WRITE TO JSON RETURN METEOFILENAME
meteofile_name = 'nasa_power_{date_start}_{date_end}_{latitude}_{longitude}.json'.format(longitude=longitude,
                                                                                   latitude=latitude,
                                                                                   date_start=simulation_start,
                                                                                   date_end=simulation_end)
get_nasa_power_meteo_data(latitude=latitude,
                                      longitude=longitude,
                                      date_start=simulation_start,
                                      date_end=simulation_end,
                                      output=outputs,
                                      filename=meteofile_name)


#CALCULATE ET0 (REFERENCE EVAPOTRANSPIRATION) AND WRITE TO CSV
meteofile_path = os.path.join(outputs, meteofile_name)
meteofile_et0_out_name = 'ET0_' + meteofile_name.split('json')[0] + 'csv'
meteofile_et0_out_path = os.path.join(outputs, meteofile_et0_out_name)
meteo_df = et0_calculation(latitude=latitude,
                           altitude=altitude,
                           output_path=meteofile_et0_out_path,
                           meteofile_path=meteofile_path)


#TRANSFORM METEO CSV FILE TO AQUACROP CLIMATE FILES (.CLI)
format_aquacrop_meteo(project_name=project_name,
                      meteocsvfile_path=meteofile_et0_out_path,
                      data_path=aquacrop_data)

#CREATE CALENDAR FILE (.CAL)
format_aquacrop_calendar(project_name=project_name,
                         growing_season_start=growing_season_start,
                         data_path=aquacrop_data
                         )

#MODIFY CROP PARAMETERS
#Copy crop file from ./CROPS to ./DATA folder
crop_src = os.path.join(aquacrop_project_path, 'CROPS', crop)
crop_dst = os.path.join(aquacrop_project_path, 'DATA', crop)
shutil.copyfile(crop_src, crop_dst)

cropfile_folder = os.path.join(aquacrop_project_path, 'DATA')

modify_aquacrop_crop(project_name=project_name,
                     parameters_dict_modify=crop_parameters_dict_modify,
                     cropfile_folder=cropfile_folder,
                     cropfile=crop)


#RUN AQUACROP
os.system('aquacrop.exe')