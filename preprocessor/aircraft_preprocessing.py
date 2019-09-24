import pandas as pd 
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# load raw data from github
link_ac = 'https://raw.githubusercontent.com/ZiggerZZ/taxitime/master/Taxi-time%20Prediction%20Data/1.%20AC%20characteristics/ACchar.csv'
ac = pd.read_csv(link_ac)

# filter manufacturer & ICAO with Airport Data Aircrafts
ac = ac[np.isin(ac["Manufacturer"],["Airbus","Boeing","Boeing (McDonnell Douglas)","Bombardier","Embraer","McDonnell Douglas"])]
ac = ac[np.isin(ac["ICAO Code"], df["acType"].unique())]
ac = ac.replace("tbd",np.nan)
ac = ac.replace("same?",np.nan)
ac = ac.replace('2018-Jul-3',np.nan)
ac = ac.replace('#VALUE!',np.nan)

####################################
## Alter Data Schema
####################################

ac["Wingspan, ft"] = ac["Wingspan, ft"].astype(float)
ac["Length, ft"] = ac["Length, ft"].astype(float)
ac["Tail Height, ft\n(@ OEW)"] = ac["Tail Height, ft\n(@ OEW)"].astype(float)
ac["Wheelbase, ft"] = ac["Wheelbase, ft"].astype(float)
ac["Cockpit to Main Gear (CMG)"] = ac["Cockpit to Main Gear (CMG)"].astype(float)
ac["MGW\n(Outer to Outer)"] = ac["MGW\n(Outer to Outer)"].astype(float)
ac["MTOW"] = ac["MTOW"].str.replace(",", "").astype(float)
ac["Max Ramp\nMax Taxi"] = ac["Max Ramp\nMax Taxi"].str.replace(",", "").astype(float)
ac["Parking Area (WS x Length), sf"] = ac["Parking Area (WS x Length), sf"].str.replace(",", "").astype(float)

####################################
## Create Dim Proxy: PCA to combine aircraft dimensions into one feature
####################################

# group aircraft data by ICAO so that there is one row per airplane model
ac_icao = ac.groupby(["ICAO Code"]).min().reset_index()
ac_icao = ac_icao.rename(columns= {"ICAO Code":"acType"})

# columsn to be combined
scaled_pca = ac_icao[["Wingspan, ft","Length, ft","Tail Height, ft\n(@ OEW)","Wheelbase, ft"]]

# scale data as library function only centers it
# perform PCA to combine aircraft size features
scaler = StandardScaler()
scaled_pca[["Wingspan, ft","Length, ft","Tail Height, ft\n(@ OEW)","Wheelbase, ft"]] = scaler.transform(scaled_pca)

pca = PCA(n_components=1)
princ_comp = pca.fit_transform(scaled_pca)
pca_df = pd.DataFrame(data = princ_comp, columns = ['dim_proxy'])

# drop unused columns
ac_icao = ac_icao.drop(list(scaled_pca.columns) + ["Manufacturer","Model","AAC","ADG","Cockpit to Main Gear (CMG)","MGW\n(Outer to Outer)","Wake Category","Years Manufactured","Note","Parking Area (WS x Length), sf"], axis=1)
ac_final = pd.concat([ac_icao,pca_df], axis=1)

ac_final.to_csv('../data/aircraft_data.csv', index=False)
