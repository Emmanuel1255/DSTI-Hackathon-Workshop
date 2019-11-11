from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt



# create new figure, axes instances.
#fig=plt.figure()
#ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
fig = plt.figure(figsize=(12,9))

m = Basemap(projection='mill',
            llcrnrlat= -90,
            llcrnrlon= -180,
            urcrnrlat= 90,
            urcrnrlon= 180,
            resolution='c')

xs=[]
ys=[]

deplat = float(lat_lon[0]); deplon = float(lat_lon[1])
xpt, ypt = m(deplon, deplat)
xs.append(xpt)
ys.append(ypt)
m.plot(xpt, ypt, 'r^', markersize=10)



arrlat = float(lat_lon2[0]); arrlon = float(lat_lon2[1])
xpt, ypt = m(arrlon, arrlat)
xs.append(xpt)
ys.append(ypt)
m.plot(xpt, ypt, 'g*', markersize=10)
m.drawcoastlines()
m.fillcontinents()
m.shadedrelief()
#m.etopo()
plt.title('Airport Location')
m.plot(xs, ys, color='b', linewidth=3, label='Flight 112')
# draw parallels
#m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
# draw meridians
#m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])

plt.show()

import time
import requests
import logging
import pprint
import csv

currentTime = int(time.time())  # currentTime in second
startTime = currentTime - 3600 * 48  # 48h in the past
username = "pdtpatrick"
password = "u3!WL2uC0dxu"


def call_api(airport, startTime, endTime):
    """Call opensky API and return all departures

    begin = now - days ago
    end = now
    """
    time.sleep(10)
    URL = f"https://opensky-network.org/api/flights/departure?airport={airport}&begin={startTime}&end={endTime}"
    logging.info(f"URL is now: {URL}")
    r = requests.get(URL, auth=(username, password))
    if r.status_code == 404:
        logging.error("Cannot find data")
        return None
    assert len(r.json()) != 0
    return r.json()


airport_name = "KSEA"

depatures = call_api('KLGA', startTime, currentTime)
print(len(depatures))


def read_airport(filename: str):
    keys = ["id", "name", "city", "country", "IATA", "ICAO",
            "latitude", "longitude", "altitude", "timezone",
            "dst", "tz", "type", "source"]
    airports = [a for a in
                csv.DictReader(open(filename, encoding="utf-8"), delimiter=',', quotechar='"', fieldnames=keys)]

    return airports  # [15:25]


airports = read_airport("airports.csv")

#print(f'{airports} \n')
dictionary_ = {}


for i in airports:
    key = i['ICAO']
    dictionary_[key] = [i['latitude'],i['longitude']]


def getLocation(airport):
    return dictionary_[airport]


lat_lon = getLocation("KSEA")

lat_lon2 = getLocation("EHKD")

#print(getLocation("KSEA"))


def flight_information(dep,arr):
    dep_loc = getLocation(dep)
    arr_loc = getLocation(arr)
    temp = []
    temp.append(dep_loc)
    temp.append(arr_loc)
    return temp


for departure in depatures:
    flight_dep = departure['estDepartureAirport']
    flight_arr = departure['estArrivalAirport']
    # print(flight_arr)
    flight_loc = flight_information(flight_dep,flight_arr)
    print(flight_information(flight_dep,flight_arr))
    show_flight(flight_loc)

