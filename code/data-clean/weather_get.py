import requests
import csv
import json


#This script gathers weather data from darksky via API

field1 = 'https://api.darksky.net/forecast/'
field2 = '?exclude=hourly,flags,isd-stations,daily'
key = ''


geo_reader = csv.reader(open('../../data/location_info.csv', 'r', encoding='utf-8'))
ufo_reader = csv.reader(open('../../data/file_ufo_clean.csv', 'r', encoding='utf-8'))
ufo_file = open('../../data/file_ufo_lat.csv', 'w', encoding='utf-8')
ufo_writer = csv.writer(ufo_file)
weather_file = open('../../data/file_ufo_weather.csv', 'w', encoding='utf-8')
weather_writer = csv.writer(weather_file)

#read location information
next(geo_reader, None)
geo_id_list = []
geo_list = []
for geo in geo_reader:
    geo_id_list.append(geo[0])
    geo_list.append(geo)


ufo_writer.writerow(['event_id', 'year', 'month', 'day', 'time', 'city', 'state', 'shape', 'duration', 'summary', 'lat', 'lng'])
next(ufo_reader, None)

weather_writer.writerow(['event_id', 'summary', 'icon', 'temperature', 'apparentTemperature','dewPoint', 'humidity', 'windSpeed',
                        'windBearing', 'visibility', 'pressure'])
ufo_list = []

index = 1
for ufo in ufo_reader:
    print(index)
    index += 1
    if index%500==0:

        #using close and open to write in the file
        ufo_file.close()
        ufo_file = open('../../data/file_ufo_lat.csv', 'a+',encoding='utf-8')
        ufo_writer = csv.writer(ufo_file)

        weather_file.close()
        weather_file = open('../../data/file_ufo_weather.csv', 'a+',encoding='utf-8')
        weather_writer = csv.writer(weather_file)


    if ufo[7] in geo_id_list and 'T' in ufo[1]:
        geo = geo_list[geo_id_list.index(ufo[7])][3:5]
        date = ufo[1][2:-1].split('T')[0].split('-')

        hour = ufo[1][2:-1].split('T')[1]
        query = geo[0]+','+geo[1]+','+ufo[1][2:-1]
        ufo = [ufo[0]]+date+[hour]+ufo[2:-1]+geo
        ufo_writer.writerow(ufo)

        try:
            weather = requests.get(url=field1+key+'/'+query+field2).json()
            weather = weather['currently']
            tmp = [ufo[0], weather['summary'], weather['icon'], weather['temperature'], weather['apparentTemperature'],
                       weather['dewPoint'], weather['humidity'], weather['windSpeed'], weather['windBearing'], weather['visibility'],
                       weather['pressure']]
            weather_writer.writerow(tmp)
        except:
            print('error')

