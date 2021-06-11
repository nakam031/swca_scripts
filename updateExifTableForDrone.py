"""
Author: Hitomi Nakamura
Date: 11/30/2020
Edit Date: 
Project Name: Drone
---Note---
This script will update all the lat/long with 0 values to their group1 lat/long. 
It reads txt or csv file with 4 columns: Name of the image, latitude, longitude and altitude.

"""

import pandas as pd
import os 
table = input("Path to the EXIF Table (.txt or .csv): ")
df = pd.read_csv(table,sep=',',header=None)
df.columns = ['Name','Latitude','Longitude','Altitude']
for i,r in df.iterrows():
    
    lat = r[1]
    lon = r[2]
    name= r[0]
    if int(lat)==0 or int(lon)==0:
        groupName = name[:7]

        referenceName = groupName + '0' + '.JPG'
        referenceLat = df.loc[df['Name'] == referenceName]['Latitude']
        referenceLon = df.loc[df['Name'] == referenceName]['Longitude']
        referenceAlt = df.loc[df['Name'] == referenceName]['Altitude']
        df.at[i,'Latitude'] = referenceLat
        df.at[i,'Longitude'] = referenceLon
        df.at[i,'Altitude'] = referenceAlt
df.to_csv(table,sep=',',header=False,index=False)      


