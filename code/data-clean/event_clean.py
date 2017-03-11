import csv
import re
import json
import requests

def check(lat, lng):
    return True if 25<lat<49 and -125<lng<-66 else False




field = 'https://maps.googleapis.com/maps/api/geocode/json?'

event_file = open('../../data/file_ufo.csv', 'r', encoding='utf-8')
event_reader = csv.reader(event_file)
next(event_reader, None)


event_clean_list = []
pattern_1 = re.compile(r'COLOR=#000000>.+?</TD>')
pattern_2 = re.compile(r'.html>.+?</A></TD>')
index = 1


#for each row in file_ufo.csv
for row in event_reader:
    print(index)
    index += 1
    match_1 = pattern_1.findall(row[0])
    match_2 = pattern_2.findall(row[0])
    tmp = [match_2[0][6:-9].encode('utf-8')]

    for i in range(1,len(match_1)-1):
        tmp.append(match_1[i][14:-5].encode('utf-8'))

    #eliminate invalid item
    if '<BR>' not in str(tmp[1]) and 'unknown' not in str(tmp[1].lower()) and 'unspecified' not in str(tmp[1].lower())\
            and '<BR>' not in str(tmp[2]) and '?' not in str(tmp[1]):
        query = str(tmp[1])+','+str(tmp[2])

        #query longitude and latitude
        try:
            j = requests.get(url=field+'address='+query+'&key=AIzaSyDLN-xK0p13MpS8RQffOVRbwtqYEdv6YZg').json()
            if check(j['results'][0]['geometry']['location']['lat'], j['results'][0]['geometry']['location']['lng']):
                tmp.append(j['results'][0]['geometry']['location']['lat'])
                tmp.append(j['results'][0]['geometry']['location']['lng'])
                event_clean_list.append(tmp)
        except:
            print('error')


#write file_ufo_clean.csv
event_clean_file = open('../../data/file_ufo_clean.csv', 'w', encoding='utf-8')
event_clean_writer = csv.writer(event_clean_file)
event_clean_writer.writerow(['time'.encode('utf-8'), 'city'.encode('utf-8'), 'state'.encode('utf-8'), 'shape'.encode('utf-8'),
                             'duration'.encode('utf-8'), 'summary'.encode('utf-8'), 'lat'.encode('utf-8'), 'lng'.encode('utf-8')])

for item in event_clean_list:
    event_clean_writer.writerow(item)

