import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv(r'C:\Users\dnguy\source\repos\WebScrappingTest\coord_data_tiny.csv')
#print(df.longitude.min())
#print(df.longitude.max())
#print(df.latitude.min())
#print(df.latitude.max())

bounds = [df.longitude.min(), df.longitude.max(), df.latitude.min(), df.latitude.max()]

ruh_m = plt.imread(r'C:\Users\dnguy\source\repos\MappingGISData\map.png')

fig, ax = plt.subplots(figsize=(8,7))
ax.scatter(df.longitude, df.latitude, zorder=1, alpha= 0.4, c='r', s=30)
ax.set_title('Plotting Route Data on Evanston Map')
ax.set_xlim(bounds[0],bounds[1])
ax.set_ylim(bounds[2],bounds[3])
ax.imshow(ruh_m, zorder=0, extent = bounds, aspect= 'equal')
plt.show()


#from arcgis.gis import GIS
#gis = GIS("https://www.arcgis.com", "dnguyen2048", "zO78vcJ75F~K")
#map1 = gis.map("Palm Springs, CA")
#map1
