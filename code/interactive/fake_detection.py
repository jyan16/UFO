from __future__ import division

import csv
import numpy
from sklearn.externals import joblib
import argparse
import requests
import json
from sklearn import preprocessing
import sqlite3


googleField = 'https://maps.googleapis.com/maps/api/geocode/json?'
googleKey = 'AIzaSyD_VpEeAmvHVFRb94Pz1LF7l_SoLHepnow'
weatherKey = 'd9dcaa3fac6a59b265ee62ad1e45aa3b'
weatherField1 = 'https://api.darksky.net/forecast/'
weatherField2 = '?exclude=hourly,flags,isd-stations,daily'

def load_database(c):
	summary_list = []
	for row in c.execute('''SELECT distinct summary
	                        FROM weathers'''):
		summary_list.append(row[0].lower())
	le_weather = preprocessing.LabelEncoder().fit(summary_list)
	joblib.dump(le_weather, '../models/weather_trans.pkl') #save le_weather

	shape_list = []
	for row in c.execute('''SELECT distinct shape
	                        FROM events'''):
		shape_list.append(row[0].lower())
	le_shape = preprocessing.LabelEncoder().fit(shape_list)
	joblib.dump(le_shape, '../models/shape_trans.pkl') #save le_shape

	train_features = []
	# novelty_features = []
	train_label = []
	for row in c.execute('''SELECT e.lat, e.lng, e.time, e.shape, w.summary, w.visibility, e.summary
	                        FROM events e, weathers w
	                        WHERE e.year>=1950 AND e.year<=2017 AND e.event_id=w.event_id
	                     '''):
		text = row[6].lower()
		train_features.append([row[0], row[1], int(row[2].split(':')[0]), le_shape.transform([row[3].lower()])[0],
							   le_weather.transform([row[4].lower()])[0], row[5]])
		if 'nuforc' in text or 'hoax' in text:
			train_label.append(0)
		else:
			train_label.append(1)


	return (numpy.array(train_label), numpy.array(train_features))

def get_lat_lng(city, state):
	j = requests.get(url=googleField + 'address=' + city + ',' + state + '&key=' + googleKey).json()
	lat = j['results'][0]['geometry']['location']['lat']
	lng = j['results'][0]['geometry']['location']['lng']
	return lat,lng

def get_weather(opts, lat, lng):
	time = opts.d + 'T' + opts.t + ':00'
	query =  str(lat) + ',' + str(lng) + ',' + time
	weather = requests.get(url = weatherField1 + weatherKey + '/' + query + weatherField2).json()
	weather = weather['currently']
	return weather


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
	# summary_svm = joblib.load('../models/summary_svm.pkl')
	# numeric_tree = joblib.load('../models/numeric_tree.pkl')
	# summary_tree = joblib.load('../models/summary_tree.pkl')

	lat, lng = get_lat_lng(opts.c, opts.s)
	weather_dict = get_weather(opts, lat, lng)
	numeric_feature = numpy.array([lat, lng, int(opts.t.split(':')[0]), le_shape.transform([opts.shape.lower()])[0],
			   			 le_weather.transform([weather_dict['summary'].lower()])[0], weather_dict['visibility']])
	description_feature = vectorizer.transform([opts.sum])


	summary_log_prob = summary_log.predict_proba(description_feature)
	# summary_log_result = summary_log.predict(description_feature)
	# print('log_summary', summary_log_result, summary_log_prob)

	summary_tree_prob = summary_tree.predict_proba(description_feature)
	# summary_tree_result = summary_tree.predict(description_feature)
	# print('tree_summary', summary_tree_result, summary_tree_prob)

	numeric_svm_prob = numeric_svm.predict_proba([numeric_feature])
	# numeric_svm_result = numeric_svm.predict([numeric_feature])
	# print('svm_numeric', numeric_svm_result, numeric_svm_prob)

	numeric_tree_prob = numeric_tree.predict_proba([numeric_feature])
	# numeric_tree_result = numeric_tree.predict([numeric_feature])
	# print('tree_numeric', numeric_tree_result, numeric_tree_prob)

	result = (summary_log_prob[0][1] + summary_tree_prob[0][1] + numeric_svm_prob[0][1] + numeric_tree_prob[0][1]) / 4
	print(result)


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
	opts = parser.parse_args()
	opts.sum = ' '.join(opts.sum.lower().split('_'))
	test(opts)





if __name__ == '__main__':
	main()