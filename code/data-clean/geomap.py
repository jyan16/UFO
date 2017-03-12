import googlemaps
import requests
import re
import csv

def check(lat, lng):
    return True if 25<lat<49 and -125<lng<-66 else False

field = 'https://maps.googleapis.com/maps/api/geocode/json?'

#add your key here
key = 'AIzaSyDKas4Uv-i2pOEG08AR3RTxdIGvh4PpSHI'

#change the value of i
i=1

event_file = open('../../data/location_'+str(i)+'.csv', 'r', encoding='utf-8')
event_reader = csv.reader(event_file)

event_writer = csv.writer(open('../../data/location_'+str(i)+'_info.csv', 'w', encoding='utf-8'))

geolist = []

index = 1
for row in event_reader:
    print(index)
    index += 1
    try:
        j = requests.get(url=field+'address='+str(row[1])+'&key='+key).json()
        lat = j['results'][0]['geometry']['location']['lat']
        lng = j['results'][0]['geometry']['location']['lng']
        tmp = row
        tmp.append(lat)
        tmp.append(lng)

        geolist.append(tmp)
    except:
        print('error')

for item in geolist:
    event_writer.writerow(item)

