import requests
import csv

field1 = 'https://api.darksky.net/forecast/'
field2 = '?exclude=hourly,flags,isd-stations,daily'
#key = '7193dc40aac9e7daa65bdc3863d7b932'


geo_reader = csv.reader(open('../../data/location_info.csv', 'r', encoding='utf-8'))
ufo_reader = csv.reader(open('../../data/file_ufo_clean.csv', 'r', encoding='utf-8'))
ufo_writer = csv.writer(open('../../data/file_ufo_weather.csv', 'w', encoding='utf-8'))

#read location information
next(geo_reader, None)
geo_id_list = []
for geo in geo_reader:
    geo_id_list.append(geo[0])

#read ufo information

ufo_writer.writerow(['event_id'.encode('utf-8'), 'time'.encode('utf-8'), 'city'.encode('utf-8'), 'state'.encode('utf-8'), 'shape'.encode('utf-8'),
                             'duration'.encode('utf-8'), 'summary'.encode('utf-8'), 'location_id'.encode('utf-8')])
next(ufo_reader, None)
ufo_list = []
for ufo in ufo_reader:
    if ufo[7] in geo_id_list and 'T' in ufo[1]:
        ufo_writer.writerow(ufo)







'''
j = requests.get(url=field1+key+'/33.4255104,-111.9400054,1980-10-7T13:00:00'+field2)
if j:
    print(j.content.current)
    print(j)

print(j)'''