import requests
import csv
import json

field1 = 'https://api.darksky.net/forecast/'
field2 = '?exclude=hourly,flags,isd-stations,daily'
key = ''


geo_reader = csv.reader(open('../../data/location_info.csv', 'r', encoding='utf-8'))
ufo_reader = csv.reader(open('../../data/file_ufo_clean.csv', 'r', encoding='utf-8'))
ufo_writer = csv.writer(open('../../data/file_ufo_weather.csv', 'w', encoding='utf-8'))

#read location information
next(geo_reader, None)
geo_id_list = []
geo_list = []
for geo in geo_reader:
    geo_id_list.append(geo[0])
    geo_list.append(geo)

#read ufo information

ufo_writer.writerow(['event_id'.encode('utf-8'), 'time'.encode('utf-8'), 'city'.encode('utf-8'), 'state'.encode('utf-8'), 'shape'.encode('utf-8'),
                             'duration'.encode('utf-8'), 'summary'.encode('utf-8'), 'lat'.encode('utf-8'), 'lng'.encode('utf-8'), 'weather'.encode('utf-8')])
next(ufo_reader, None)
ufo_list = []
for ufo in ufo_reader:
    if ufo[7] in geo_id_list and 'T' in ufo[1]:
        geo = geo_list[geo_id_list.index(ufo[7])][3:5]
        query = geo[0]+','+geo[1]+','+ufo[1][2:-1]

        '''
        try:
            weather = requests.get(url=field1+key+'/'+query+field2).json()
            weather = weather['currently']
            ufo.append(weather)

        except:
            print('error')'''

        ufo_writer.writerow(ufo[0:-1]+geo)








'''
j = requests.get(url=field1+key+'/33.4255104,-111.9400054,1980-10-7T13:00:00'+field2)
if j:
    print(j.content.current)
    print(j)

print(j)'''