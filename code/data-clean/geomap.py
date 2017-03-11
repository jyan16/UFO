import googlemaps
import requests
import re
import csv



field = 'https://maps.googleapis.com/maps/api/geocode/json?'

j = requests.get(url=field+'address=(UK/England)'+'&key=AIzaSyDLN-xK0p13MpS8RQffOVRbwtqYEdv6YZg').json()
a=j['results'][0]['geometry']['location']['lat']
b=j['results'][0]['geometry']['location']['lng']
print(a)
print(b)
