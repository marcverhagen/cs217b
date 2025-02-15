"""

Printing a map of all airports

https://www.dataquest.io/blog/python-pandas-databases/

pip install --upgrade pip
pip install matplotlib
pip install --upgrade matplotlib
pip install basemap

Also requires downloading a flights.db database from the link above.

"""

import sqlite3
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


conn = sqlite3.connect("flights.db")
cursor = conn.cursor()

cursor.execute("select * from airlines limit 5;")
results = cursor.fetchall()	
print(results)

query = "select cast(longitude as float), cast(latitude as float) from airports;"

coords = cursor.execute(query).fetchall()
print(len(coords), 'coordinates')

m = Basemap(
		projection='merc', llcrnrlat=-80, urcrnrlat=80,
		llcrnrlon=-180, urcrnrlon=180, lat_ts=20, resolution='c')
m.drawcoastlines()
m.drawmapboundary()

x, y = m([l[0] for l in coords], [l[1] for l in coords])
m.scatter(x, y, 1, marker='o', color='red')
plt.show()
