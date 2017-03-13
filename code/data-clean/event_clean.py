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
pattern_3 = re.compile(r'(.+)\(.*\)')
index = 1

location_list = []
#for each row in file_ufo.csv
for row in event_reader:
    print(index)
    index += 1
    try:
        match_1 = pattern_1.findall(row[0])
        match_2 = pattern_2.findall(row[0])
        tmp = [index, match_2[0][6:-9].encode('utf-8')]

        for i in range(1,len(match_1)-1):
            tmp.append(match_1[i][14:-5].encode('utf-8'))

        #eliminate invalid item
        if '<BR>' not in str(tmp[2]) and 'unknown' not in str(tmp[2].lower()) and 'unspecified' not in str(tmp[2].lower())\
                and '<BR>' not in str(tmp[3]) and '?' not in str(tmp[2]):
            if '(' in str(tmp[2]):
                location = pattern_3.match(str(tmp[2])[2:-1]).group(1)

            else:
                location = str(tmp[2])[2:-1]+','+str(tmp[3])[2:-1]
            if location not in location_list:
                location_list.append(location)
            tmp.append(location_list.index(location))
            event_clean_list.append(tmp)
    except:
        print('error')

#write file_ufo_clean.csv
event_clean_file = open('../../data/file_ufo_clean.csv', 'w', encoding='utf-8')
event_clean_writer = csv.writer(event_clean_file)
event_clean_writer.writerow(['event_id'.encode('utf-8'), 'time'.encode('utf-8'), 'city'.encode('utf-8'), 'state'.encode('utf-8'), 'shape'.encode('utf-8'),
                             'duration'.encode('utf-8'), 'summary'.encode('utf-8'), 'location_id'.encode('utf-8')])


for item in event_clean_list:

    try:
        #format date
        time_list = str(item[1]).split(' ')
        day_list = time_list[0][2:].split('/')
        if day_list[2]<='17':
            day_list[2] = '20'+day_list[2]
        if len(day_list[1])==1:
            day_list[1] = '0'+day_list[1]
        if len(day_list[0])==1:
            day_list[0] = '0'+day_list[0]
        time = day_list[2]+'-'+day_list[0]+'-'+day_list[1]+'T'+time_list[1][0:-1]+':00'
        item[1] = time.encode('utf-8')
    except:
        print('error')
    #writing to file_ufo_clean
    event_clean_writer.writerow(item)







def separate():
    for i in range(1,11):
        location_file = open('../../data/location_'+str(i)+'.csv', 'w', encoding='utf-8')
        location_writer = csv.writer(location_file)
        #location_writer.writerow(['location_id'.encode('utf-8'), 'location'.encode('utf-8')])
        for j in range(2400*(i-1), min(2400*i,len(location_list))):
            location_writer.writerow([j, location_list[j]])
