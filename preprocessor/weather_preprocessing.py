import pandas as pd
import numpy as np
from math import floor

# import weather data
weather_link = 'https://raw.githubusercontent.com/ZiggerZZ/taxitime/master/Taxi-time%20Prediction%20Data/2.%20Weather%20data/weather_data_prep.csv'
weather = pd.read_csv(weather_link)

rename_dict = {'WSF2': 'fastest_2_minute_wind_speed',
 'WSF5': 'fastest_5_second_wind_speed',
 'PRCP': 'precipitation',
 'SNWD': 'snow_depth',
 'WDF2': 'direction_of_fastest_2_minute_wind',
 'AWND': 'average_wind_speed',
 'WDF5': 'direction_of_fastest_5_second_wind',
 'PGTM': 'peak_gust_time',
 'TMAX': 'maximum_temperature',
 'TAVG': 'average_temperature',
 'TMIN': 'minimum_temperature',
 'WT03': 'thunder',
 'WT02': 'heavy_fog_or_heaving_freezing_fog',
 'WT01': 'fog,_ice_fog,_or_freezing_fog_(incl_heavy_fog)',
 'WT08': 'smoke_or_haze',
 'SNOW': 'snowfall'}

weather.rename(columns=rename_dict, inplace = True)

not_used_weather = ['peak_gust_time', # no values
 'snowfall', # all 0
 'snow_depth', # all 0
 'maximum_temperature', # correlated with average_temperature
 'minimum_temperature', # correlated with average_temperature
 'fastest_5_second_wind_speed', # correlated with 2 minute wind speed, keep 2 min bc more correlated with actual landing time
]
weather.drop(not_used_weather, axis = 1, inplace = True)

boolean_fields = ['fog,_ice_fog,_or_freezing_fog_(incl_heavy_fog)',
                  'heavy_fog_or_heaving_freezing_fog',
                  'thunder',
                  'smoke_or_haze']

# replace nulls with 0
weather[boolean_fields] = weather[boolean_fields].fillna(0)

# weather data is not unique by day, so for now we will take the average of each column 
weather_data_grouped = weather.groupby('DATE', as_index=False).mean()

weather_data_grouped.to_csv('../data/weather_data.csv', index=False)

