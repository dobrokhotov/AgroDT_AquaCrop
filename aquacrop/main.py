import os
from tools.meteo_downloader import get_nasa_power_meteo_data
from tools.elevation_downloader import get_elevation_by_point
from models.fao_56_reference_evapotranspiration import et0_calculation

#USER DEFINED PARAMETERS

#Latitude in degrees (from -90 to 90)
latitude = 59.425032
#Longitude in degrees (from -180 to 180)
longitude = 30.031902
# Simulation start date (yyyymmdd)
simulation_start = 20230401
#Simulation end date (yyyymmdd)
simulation_end = 20230901
#Output folder
outputs = './outputs'

#GET ELEVATION (ALTITUDE)
altitude = get_elevation_by_point(latitude=latitude,
                                  longitude=longitude)

#DOWNLOAD METEODATA FROM NASAPOWER AND WRITE TO JSON RETURN METEOFILENAME
meteofile_name = get_nasa_power_meteo_data(latitude=latitude,
                                      longitude=longitude,
                                      date_start=simulation_start,
                                      date_end=simulation_end,
                                      output=outputs)


#CALCULATE ET0 (REFERENCE EVAPOTRANSPIRATION) AND WRITE TO CSV
meteofile_path = os.path.join(outputs, meteofile_name)
meteofile_et0_out_name = 'ET0_' + meteofile_name.split('json')[0] + 'csv'
meteofile_et0_out_path = os.path.join(outputs, meteofile_et0_out_name)
meteo_df = et0_calculation(latitude=latitude,
                           altitude=altitude,
                           output_path=meteofile_et0_out_path,
                           meteofile_path=meteofile_path)

