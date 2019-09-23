import pandas as pd 
import numpy as np


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

link_ac = 'https://raw.githubusercontent.com/ZiggerZZ/taxitime/master/Taxi-time%20Prediction%20Data/1.%20AC%20characteristics/ACchar.csv'
link_ap = 'https://raw.githubusercontent.com/ZiggerZZ/taxitime/master/data/airport_data.csv'
ac = pd.read_csv(link_ac)
df = pd.read_csv(link_ap)

df = df.apply(lambda x: clean_ac(x), axis=1)

# filter manufacturer & ICAO with Airport Data Aircrafts
ac = ac[np.isin(ac["Manufacturer"],["Airbus","Boeing","Boeing (McDonnell Douglas)","Bombardier","Embraer","McDonnell Douglas"])]
ac = ac[np.isin(ac["ICAO Code"], df["acType"].unique())]
ac = ac.replace("tbd",np.nan)
ac = ac.replace("same?",np.nan)
ac = ac.replace('2018-Jul-3',np.nan)
ac = ac.replace('#VALUE!',np.nan)

ac["Wingspan, ft"] = ac["Wingspan, ft"].astype(float)
ac["Length, ft"] = ac["Length, ft"].astype(float)
ac["Tail Height, ft\n(@ OEW)"] = ac["Tail Height, ft\n(@ OEW)"].astype(float)
ac["Wheelbase, ft"] = ac["Wheelbase, ft"].astype(float)
ac["Cockpit to Main Gear (CMG)"] = ac["Cockpit to Main Gear (CMG)"].astype(float)
ac["MGW\n(Outer to Outer)"] = ac["MGW\n(Outer to Outer)"].astype(float)
ac["MTOW"] = ac["MTOW"].str.replace(",", "").astype(float)
ac["Max Ramp\nMax Taxi"] = ac["Max Ramp\nMax Taxi"].str.replace(",", "").astype(float)
ac["Parking Area (WS x Length), sf"] = ac["Parking Area (WS x Length), sf"].str.replace(",", "").astype(float)

# group aircraft data by ICAO so that there is one row per airplane model
ac_icao = ac.groupby(["ICAO Code"]).min().reset_index()
ac_icao = ac_icao.rename(columns= {"ICAO Code":"acType"})

scaled_pca = ac_icao[["Wingspan, ft","Length, ft","Tail Height, ft\n(@ OEW)","Wheelbase, ft"]]

# scale data as library function only centers it
# perform PCA to combine aircraft size features
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
print(scaler.fit(scaled_pca))
scaled_pca[["Wingspan, ft","Length, ft","Tail Height, ft\n(@ OEW)","Wheelbase, ft"]] = scaler.transform(scaled_pca)

from sklearn.decomposition import PCA

pca = PCA(n_components=1)
princ_comp = pca.fit_transform(scaled_pca)
pca_df = pd.DataFrame(data = princ_comp, columns = ['dim_proxy'])

ac_icao = ac_icao.drop(list(scaled_pca.columns) + ["Manufacturer","Model","AAC","ADG","Cockpit to Main Gear (CMG)","MGW\n(Outer to Outer)","Wake Category","Years Manufactured","Note","Parking Area (WS x Length), sf"], axis=1)
ac_final = pd.concat([ac_icao,pca_df], axis=1)

ac_final.to_csv('../data/aircraft_data.csv', index=False)
