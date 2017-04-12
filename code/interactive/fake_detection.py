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
	summary_svm = joblib.load('./code/models/summary_svm.pkl')

	# le_shape = joblib.load('../models/shape_trans.pkl')
	# le_weather = joblib.load('../models/weather_trans.pkl')
	# vectorizer = joblib.load('../models/vectorizer.pkl')
	# numeric_svm = joblib.load('../models/numeric_svm.pkl')
	# summary_log = joblib.load('../models/summary_log.pkl')
	# summary_svm = joblib.load('../models/summary_svm.pkl')

	lat, lng = get_lat_lng(opts.c, opts.s)
	weather_dict = get_weather(opts, lat, lng)
	numeric_feature = numpy.array([lat, lng, int(opts.t.split(':')[0]), le_shape.transform([opts.shape.lower()])[0],
			   			 le_weather.transform([weather_dict['summary'].lower()])[0], weather_dict['visibility']])
	description_feature = vectorizer.transform([opts.sum])
	# a = summary_svm.predict(description_feature)
	# summary_svm_result = summary_svm.predict_proba(description_feature)
	summary_log_result = summary_log.predict_proba(description_feature)[0][1]
	# b = summary_log.predict(description_feature)
	numeric_svm_result = numeric_svm.predict_proba([numeric_feature])[0][1]
	# d = numeric_svm.predict([numeric_feature])
	# result = (numeric_svm_result * 850 + summary_log_result * 796 + summary_svm_result * 802) / 2448
	result = (numeric_svm_result * 850 + summary_log_result * 796) / 1646
	print(result)

	#load data to test

	# (training_labels, training_texts) = load_file('../../data/processed/file_ufo_lat.csv')
	# training_features = vectorizer.transform(training_texts)
	# training_labels = numpy.array(training_labels)
	#
	# # score_sum_svm = summary_svm.score(training_features, training_labels)
	# # print('summary_svm accuracy: ' + str(score_sum_svm))
	# predict_result = summary_svm.predict(training_features)
	# print('summary_svm -- confusion matrix:')
	# print(confusion_matrix(training_labels, predict_result))
	#
	#
	#
	# # score_sum_log = summary_log.score(training_features, training_labels)
	# # print('summary_log accuracy: ' + str(score_sum_log))
	# predict_result = summary_log.predict(training_features)
	# print('summary_log -- confusion matrix:')
	# print(confusion_matrix(training_labels, predict_result))
	#
	#
	# #load data to test
	# conn = sqlite3.connect('../../data/my_ufo.db')
	# c = conn.cursor()
	# (true_features, fake_features, event_id) = load_database(c)
	# train_labels = [1] * len(true_features) + [0] * len(fake_features)
	# train_features = numpy.array(list(true_features) + list(fake_features))
	# # # score_num_svm = numeric_svm.score(train_features, train_labels)
	# # # print('numeric_svm accuracy: ' + str(score_num_svm))
	# predict_result = numeric_svm.predict(train_features)
	# for i in range(0, len(predict_result)):
	# 	if predict_result[i]==0:
	# 		print(i)
	# print('numeric_svm -- confusion matrix:')
	# print(confusion_matrix(train_labels, predict_result))


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