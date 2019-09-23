import pandas as pd
from split_date import split_date_time

link_ac = 'https://raw.githubusercontent.com/ZiggerZZ/taxitime/master/data/aircraft_data.csv'
link_ap = 'https://raw.githubusercontent.com/ZiggerZZ/taxitime/master/data/airport_data.csv'
link_weather = 'https://raw.githubusercontent.com/ZiggerZZ/taxitime/master/data/weather_data.csv'

df = pd.read_csv(link_ap)
ac = pd.read_csv(link_ac)
we = pd.read_csv(link_weather)

# merge aircraft
df = pd.merge(df, ac, how="left", on="acType")

# merge weather
we['DATE'] = we.DATE.apply(split_date_time,1) #change to timestamp
we['DATE_join'] = we['DATE'].astype(str) #create join col

df['actual_landing_time'] = pd.to_datetime(df['actual_landing_time'])
df['landing_day_join'] = df['actual_landing_time'].dt.date.astype(str) #create join col

# merge weather data and airport df
df = df.merge(we, how='left', left_on='landing_day_join', right_on='DATE_join')
df.drop(['DATE', 'DATE_join', 'landing_day_join', 'index'], axis = 1, inplace = True)

df.to_csv('../data/complete_data.csv', index=False)