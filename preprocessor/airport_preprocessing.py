import pandas as pd
import numpy as np
from collections import Counter
from split_date import split_date_time

link = 'https://raw.githubusercontent.com/ZiggerZZ/taxitime/master/Taxi-time%20Prediction%20Data/0.%20Airport%20data/Airport_Data.csv'
df = pd.read_csv(link)


def get_traffic_metric(row, df):
    
    # TODO: change to a more efficient function
    
    index = row['index']
    df = df[max(index - 1000,0) :index-1] 
    count = len(df[(df['actual_inblock_time_sec'] > row['actual_landing_time_sec']) &
                       (df['actual_landing_time_sec'] < row['actual_landing_time_sec'])])
    return count

def get_runway_traffic_metric(row, df):
    # change to a more efficient 
    index = row['index']
    df = df[max(index - 1000,0) :index-1]
    count = len(df[(df['actual_inblock_time_sec'] > row['actual_landing_time_sec']) &
                       (df['actual_landing_time_sec'] < row['actual_landing_time_sec']) & 
                       (df['runway'] == row['runway'])])
    return count

def count_elem_in_list(input_list):
    cnt = Counter()
    for word in input_list:
        cnt[word] += 1
    return dict(cnt)

def get_all_runway_traffic_metric(row, df):
    # change to a more efficient 
    index = row['index']
    
    df = df[max(index - 1000,0) :index]
    match = df[(df['actual_inblock_time_sec'] > row['actual_landing_time_sec']) &
                        (df['actual_landing_time_sec'] < row['actual_landing_time_sec'])]
    runways = match['runway'].values
    runways_dict = count_elem_in_list(runways)
    return runways_dict

not_used = [
 'ship', # slack
 'partition', # only one value
 'mode_s',
 'status',
 'sqt',
 'stand_last_change',
 'stand_scheduled',
 'aldt_received',
 'stand_prepared',
 'stand_auto_start',
 'stand_active',
 'stand_docking',
 'aibt_received',
 'vdgs_in',
 'plb_on',
 'pca_on',
 'gpu_on',
 'towbar_on',
 'pca_off',
 'gpu_off',
 'acars_out',
 'vdgs_out',
 'stand_free',
 'roll',
 'speed',
 'last_distance_to_gate',
 'last_in_sector',
 'acReg']

df.drop(columns = not_used, inplace = True)
df = df[df['aibt'] != 'aibt'] # drop 159 weird rows
df = df.dropna(subset=['aldt','aibt']) # drop NA for arrival and block time 

# Rename and convert columns
df['actual_landing_time'] = df.aldt.apply(split_date_time)
df['actual_inblock_time'] = df.aibt.apply(split_date_time)

df['t'] = df['actual_inblock_time'] - df['actual_landing_time']
df['t_minutes'] = df['t'].apply(lambda x: x.seconds/60)

df['scheduled_time_off'] = df.sto.apply(split_date_time)
df['estimated_inblock_time'] = df.eibt.apply(split_date_time)
df['calculated_inblock_time'] = df.cibt.apply(split_date_time)
df['chocks_on'] = df.chocks_on.apply(split_date_time)
df['estimated_off_block_time'] = df.eobt.apply(split_date_time)
df['actual_off_block_time'] = df.aobt.apply(split_date_time)
df['actual_take_off_time'] = df.atot.apply(split_date_time)

# Drop old columns
df.plb_off.isnull().sum() == df.shape[0] # all values are NaN so it's dropped
colToDrop = ['aldt', 'aibt', 'sto', 'eibt', 'cibt', 'chocks_on', 'plb_off', 'eobt', 'aobt', 'atot']
df.drop(columns = colToDrop, inplace= True)


# Remove empty columns
df.drop(columns = ['estimated_off_block_time', 'actual_off_block_time', 'actual_take_off_time'], inplace= True)
df.dropna(inplace = True)

# remove outliers
treshold = 200
df = df[df.t_minutes < treshold] 

# change actual_landing_time to a day level
df["date"] = df.actual_landing_time.dt.date
df.groupby("date").mean().plot(figsize = (20, 8))

# add time data
df['week_of_year'] = df.actual_landing_time.dt.week
dayOfWeek={0
           :'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
df['day_of_week'] = df.actual_landing_time.dt.dayofweek.map(dayOfWeek)
df['minutes_of_day'] = df.actual_landing_time.dt.hour * 60 + df.actual_landing_time.dt.minute

# epoch time
minimum_time = df.actual_landing_time.min()
df['total_minutes'] = (df.actual_landing_time - minimum_time).apply(lambda x: x.seconds/60)
df['minute_of_week'] = (df.actual_landing_time.dt.dayofweek*1440) + (df.actual_landing_time.dt.hour*60) + df.actual_landing_time.dt.minute
df['land_to_off'] = (df['scheduled_time_off'] - df['actual_landing_time']).apply(lambda x: x.seconds/60)
df['t_min_estimated'] = (df['estimated_inblock_time'] - df['actual_landing_time']).apply(lambda x: x.seconds/60)
df['t_min_calculated'] = (df['calculated_inblock_time'] - df['actual_landing_time']).apply(lambda x: x.seconds/60)

# add traffic metric which counts the number of planes on the grounds for a particular arrival
df = df.sort_values('actual_landing_time', ascending=True)
df.reset_index(drop = True)

df['index'] = df.index # create column with index
df['actual_landing_time_sec'] = df['actual_landing_time'].astype('int64')
df['actual_inblock_time_sec'] = df['actual_inblock_time'].astype('int64')

print('traffic metric start')
# count all planes on grounds at arrival
df['traffic_metric'] = df.apply(lambda x: get_traffic_metric(x, df),1)

print('traffic metric runway start')
# count only planes that were on the same runway at arrival
df['traffic_metric_runway'] = df.apply(lambda x: get_runway_traffic_metric(x,df),1)

print('runway start')
# count the planes on other runways at time of arrival
df['runway_dict'] = df.apply(lambda x: get_all_runway_traffic_metric(x,df),1)

df['traffic_metric_runway_1']  = df['runway_dict'].apply(lambda x: x.get('RUNWAY01'),1)
df['traffic_metric_runway_2']  = df['runway_dict'].apply(lambda x: x.get('RUNWAY02'),1)
df['traffic_metric_runway_3']  = df['runway_dict'].apply(lambda x: x.get('RUNWAY03'),1)
df['traffic_metric_runway_4']  = df['runway_dict'].apply(lambda x: x.get('RUNWAY04'),1)
df['traffic_metric_runway_5']  = df['runway_dict'].apply(lambda x: x.get('RUNWAY05'),1)
df['traffic_metric_runway_6']  = df['runway_dict'].apply(lambda x: x.get('RUNWAY06'),1)
df['traffic_metric_runway_7']  = df['runway_dict'].apply(lambda x: x.get('RUNWAY07'),1)
df['traffic_metric_runway_8']  = df['runway_dict'].apply(lambda x: x.get('RUNWAY08'),1)
df['traffic_metric_runway_9']  = df['runway_dict'].apply(lambda x: x.get('RUNWAY09'),1)
df['traffic_metric_runway_10']  = df['runway_dict'].apply(lambda x: x.get('RUNWAY10'),1)
# df.drop('runway_dict',inplace=True)

df.to_csv('../data/airport_data.csv', index=False)
