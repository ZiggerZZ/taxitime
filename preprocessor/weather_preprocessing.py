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

def join_to_weather(airport_df, weather_data_grouped):
	
	'''
	Input original airport dataframe and treated weather dataframe and return a dataframe joined on day that has 
	all columns from both dataframes, excluding the join keys
	'''
	weather_data_grouped['DATE'] = weather_data_grouped.DATE.apply(split_date_time,1) #change to timestamp
	weather_data_grouped['DATE_join'] = weather_data_grouped['DATE'].astype(str) #create join col
	airport_df['landing_day_join'] = airport_df['actual_landing_time'].dt.date.astype(str) #create join col


	# merge weather data and airport df
	df_weather = airport_df.merge(weather_data_grouped, how='left', left_on='landing_day_join', right_on='DATE_join')

	df_weather.drop(['DATE', 'DATE_join', 'landing_day_join', 'index'], axis = 1, inplace = True)
	weather_data_grouped.drop(['DATE', 'DATE_join'], axis=1, inplace = True)

	return df_weather

weather_data_grouped.to_csv('../data/weather_data.csv', index=False)

