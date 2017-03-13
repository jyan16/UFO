import requests
import re
import csv


#This python program gets lat and lng of location
def check(lat, lng):
    return True if 25<lat<49 and -125<lng<-66 else False

field = 'https://maps.googleapis.com/maps/api/geocode/json?'

#add your key here
key = 'AIzaSyD_VpEeAmvHVFRb94Pz1LF7l_SoLHepnow'

#change the value of i

def get_lng_lat():
    i=5

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

def combine():
    info_writer = csv.writer(open('../../data/location_info.csv', 'w', encoding='utf-8'))
    info_writer.writerow(['location_id', 'city', 'state', 'lat', 'lng'])
    for i in range(1,11):
        info_reader = csv.reader(open('../../data/location_raw/location_'+str(i)+'_info.csv', 'r', encoding='utf-8'))
        for row in info_reader:
            try:
                info_writer.writerow([row[0], row[1].split(',')[0], row[1].split(',')[1], row[2], row[3]])
            except:
                print('error')


if __name__ == '__main__':
    #get_lng_lat()
    combine()
