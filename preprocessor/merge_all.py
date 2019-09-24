import pandas as pd
from split_date import split_date_time

link_ac = '../data/aircraft_data.csv'
# link_ap = '../data/airport_data.csv'
test_link_ap = '../data/test_airport_data.csv'
link_weather = '../data/weather_data.csv'

df = pd.read_csv(test_link_ap)
ac = pd.read_csv(link_ac)
we = pd.read_csv(link_weather)

ac_dict = {
 'A319-SL':'A319',
 'A320/2':'A320',
 'A321/2':'A321',
 'A330/2':'A332',
 'A330/3':'A333',
 'A350/9':'A359',
 'B717/2':'B712',
 'B737/7':'B737',
 'B737/7-WL':'B737',
 'B737/8':'B738',
 'B737/8-WL':'B738',
 'B737/9':'B739',
 'B737/9-WL':'B739',
 'B757/2':'B752',
 'B757/2-WL':'B752',
 'B757/3':'B753',
 'B757/3-WL':'B753',
 'B767/3':'B763',
 'B767/3-WL':'B763',
 'B767/4':'B764',
 'B777/2':'B772',
 'B777/2-LR':'B772',
 'CRJ/2':'CRJ2',
 'CRJ/7':'CRJ7',
 'CRJ/9':'CRJ7',
 'CS/100':'CS100',
 'CS100':'CS100',
 'E175':'E170',
 'MD90/3':'B712'} 

def clean_ac(df):
	'''
	standardize aircraft models in the airport data
	'''
	if (len(str(df["acType"])) > 4):
		df["acType"] = ac_dict[df["acType"]]
	elif (df["acType"] == "MD88" or df["acType"] == "MD90"):
		df["acType"] = "B712" # Boeing renamed M88 and M90 to B717 after buying MD
	return df

# clean aircraft types in airport data to match
df = df.apply(lambda x: clean_ac(x), axis=1)

# merge aircraft data
df = pd.merge(df, ac, how="left", on="acType", )

# remove rows that didn't exist in the aircraft file
df = df[~df['MTOW'].isnull()]

# merge weather data
we['DATE'] = we.DATE.apply(split_date_time,1) #change to timestamp
we['DATE_join'] = we['DATE'].astype(str) #create join col

df['actual_landing_time'] = pd.to_datetime(df['actual_landing_time'])
df['landing_day_join'] = df['actual_landing_time'].dt.date.astype(str) #create join col

# merge weather data and airport df
df = df.merge(we, how='left', left_on='landing_day_join', right_on='DATE_join')
df.drop(['DATE', 'DATE_join', 'landing_day_join', 'index'], axis = 1, inplace = True)

df.to_csv('../data/test_complete_data.csv', index=False)