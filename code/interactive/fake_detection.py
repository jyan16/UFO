from __future__ import division
from porter_stemmer import PorterStemmer
import csv
import numpy
from sklearn.externals import joblib
import argparse
import requests
import json
from sklearn import preprocessing
import sqlite3
import re
############################################################
#this script gives back probability of new sighting events,#
#and insert this new events into my_ufo.db under ../data/  #
############################################################

googleField = 'https://maps.googleapis.com/maps/api/geocode/json?'
googleKey = 'AIzaSyD_VpEeAmvHVFRb94Pz1LF7l_SoLHepnow'
weatherKey = 'd9dcaa3fac6a59b265ee62ad1e45aa3b'
weatherField1 = 'https://api.darksky.net/forecast/'
weatherField2 = '?exclude=hourly,flags,isd-stations,daily'
stop = {'the', 'is', 'on', 'a', 'to', 'of', 's'}

def insert_db(result, weather_dict, summary, opts):
	conn = sqlite3.connect('./data/my_ufo.db')
	c = conn.cursor()
	for row in c.execute('''SELECT max(event_id) FROM events'''):
		index = row[0]
	index += 1
	date = opts.d.split('-')
	time = opts.t + ':00'

	score = (result['sum_log'] + result['sum_tree'] + result['num_svm'] + result['num_tree']) / 4
	if score >=0.5:
		label = 1
	else:
		label = 0

	insert_event = [index, date[0], date[1], date[2], time, opts.c, opts.s,
					opts.shape, opts.dur, summary, result['lat'], result['lng'], label]

	insert_weather = [index, weather_dict['summary'].lower(), weather_dict['icon'], weather_dict['temperature'],
					  weather_dict['apparentTemperature'], weather_dict['dewPoint'], weather_dict['humidity'],
					  weather_dict['windSpeed'], weather_dict['windBearing'], weather_dict['visibility'], weather_dict['pressure']]
	c.execute('''INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', tuple(insert_event))
	c.execute('''INSERT INTO weathers VALUES (?,?,?,?,?,?,?,?,?,?,?)''', tuple(insert_weather))
	conn.commit()
	conn.close()
def get_lat_lng(city, state):
	j = requests.get(url=googleField + 'address=' + city + ',' + state + '&key=' + googleKey).json()
	lat = j['results'][0]['geometry']['location']['lat']
	lng = j['results'][0]['geometry']['location']['lng']
	return lat,lng

def get_weather(opts, lat, lng):
	time = opts.d + 'T' + opts.t + ':00'
	query = str(lat) + ',' + str(lng) + ',' + time
	weather = requests.get(url = weatherField1 + weatherKey + '/' + query + weatherField2).json()
	weather = weather['currently']
	return weather

def clean_summary(summary):
	summary = ' '.join(summary.lower().split('_'))
	summary = re.sub(r'\(\(.*\)\)', '', summary)
	summary = re.sub(r'\W', ' ', summary)
	summary_list = summary.split()
	summary_list = list(filter(lambda x: x not in stop, summary_list))
	summary_list = list(filter(lambda x: x[0] < '0' or x[0] > '9', summary_list))
	summary_list = [PorterStemmer().stem(word, 0, len(word) - 1) for word in summary_list]
	summary = ' '.join(summary_list)
	return summary
def test(opts):

	#load models
	le_shape = joblib.load('./code/models/shape_trans.pkl')
	le_weather = joblib.load('./code/models/weather_trans.pkl')
	vectorizer = joblib.load('./code/models/vectorizer.pkl')
	numeric_svm = joblib.load('./code/models/numeric_svm.pkl')
	summary_log = joblib.load('./code/models/summary_log.pkl')
	numeric_tree = joblib.load('./code/models/numeric_tree.pkl')
	summary_tree = joblib.load('./code/models/summary_tree.pkl')

	# le_shape = joblib.load('../models/shape_trans.pkl')
	# le_weather = joblib.load('../models/weather_trans.pkl')
	# vectorizer = joblib.load('../models/vectorizer.pkl')
	# numeric_svm = joblib.load('../models/numeric_svm.pkl')
	# summary_log = joblib.load('../models/summary_log.pkl')
	# numeric_tree = joblib.load('../models/numeric_tree.pkl')
	# summary_tree = joblib.load('../models/summary_tree.pkl')

	result = {}
	lat, lng = get_lat_lng(opts.c, opts.s)
	result['lat'] = lat
	result['lng'] = lng
	weather_dict = get_weather(opts, lat, lng)
	result['weather'] = weather_dict['summary']
	result['visibility'] = weather_dict['visibility']
	numeric_feature = numpy.array([lat, lng, int(opts.t.split(':')[0]), le_shape.transform([opts.shape.lower()])[0],
			   			 le_weather.transform([weather_dict['summary'].lower()])[0], weather_dict['visibility']])
	summary = clean_summary(opts.sum)
	description_feature = vectorizer.transform([summary])

	summary_log_prob = summary_log.predict_proba(description_feature)
	result['sum_log'] = summary_log_prob[0][1]
	# summary_log_result = summary_log.predict(description_feature)
	# print('log_summary', summary_log_result, summary_log_prob)


	summary_tree_prob = summary_tree.predict_proba(description_feature)
	result['sum_tree'] = summary_tree_prob[0][1]
	# summary_tree_result = summary_tree.predict(description_feature)
	# print('tree_summary', summary_tree_result, summary_tree_prob)


	# numeric_svm_prob = numeric_svm.predict_proba([numeric_feature])
	# result['num_svm'] = numeric_svm_prob[0][1]
	numeric_svm_result = numeric_svm.predict([numeric_feature])
	result['num_svm'] = numeric_svm_result[0]

	numeric_tree_prob = numeric_tree.predict_proba([numeric_feature])
	result['num_tree'] = numeric_tree_prob[0][1]
	# numeric_tree_result = numeric_tree.predict([numeric_feature])
	# print('tree_numeric', numeric_tree_result, numeric_tree_prob)
	# result = (summary_log_prob[0][1] + summary_tree_prob[0][1] + numeric_svm_prob[0][1] + numeric_tree_prob[0][1]) / 4

	tmp = str(result)
	tmp = re.sub("'", '"', tmp)
	print(tmp)
	insert_db(result, weather_dict, summary, opts)


def main():
	parser = argparse.ArgumentParser()
	# parser.add_argument('-y', required = False, default = '2017', help = 'year')
	# parser.add_argument('-m', required = True, help = 'month')
	parser.add_argument('-d', required = True, help = 'date')
	parser.add_argument('-t', required = True, help = 'time')
	parser.add_argument('-sum', required = True, help = 'description')
	parser.add_argument('-shape', required=True, help='shape')
	parser.add_argument('-c', required = True, help = 'city name')
	parser.add_argument('-s', required = True, help = 'state name')
	parser.add_argument('-dur', required = False, help = 'duration')
	opts = parser.parse_args()
	# opts.sum = ' '.join(opts.sum.lower().split('_'))

	test(opts)





if __name__ == '__main__':
	main()