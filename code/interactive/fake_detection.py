from __future__ import division

import csv
import numpy
from sklearn.externals import joblib
import argparse
import requests
import json

googleField = 'https://maps.googleapis.com/maps/api/geocode/json?'
googleKey = 'AIzaSyD_VpEeAmvHVFRb94Pz1LF7l_SoLHepnow'
weatherKey = 'd9dcaa3fac6a59b265ee62ad1e45aa3b'
weatherField1 = 'https://api.darksky.net/forecast/'
weatherField2 = '?exclude=hourly,flags,isd-stations,daily'

def get_lat_lng(city, state):
	j = requests.get(url=googleField + 'address=' + city + ',' + state + '&key=' + googleKey).json()
	lat = j['results'][0]['geometry']['location']['lat']
	lng = j['results'][0]['geometry']['location']['lng']
	return lat,lng

def get_weather(opts, lat, lng):
	time = opts.y + '-' + opts.m + '-' + opts.d + 'T' + opts.t
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
	numeric_feature = numpy.array([lat, lng, int(opts.t.split(':')[0]), le_shape.transform([opts.shape])[0],
			   			 le_weather.transform([weather_dict['summary'].lower()])[0], weather_dict['visibility']])
	description_feature = vectorizer.transform([opts.sum])
	summary_svm_result = summary_svm.predict(description_feature)[0]
	summary_log_result = summary_log.predict(description_feature)[0]
	numeric_svm_result = numeric_svm.predict([numeric_feature])[0]
	result = (numeric_svm_result * 850 + summary_log_result * 796 + summary_svm_result * 802) / 2448
	if result < 0.5:
		print('fake')
	else:
		print('true')

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
	# (true_features, fake_features) = load_database(c)
	# train_labels = [1] * len(true_features) + [0] * len(fake_features)
	# train_features = numpy.array(list(true_features) + list(fake_features))
	# # score_num_svm = numeric_svm.score(train_features, train_labels)
	# # print('numeric_svm accuracy: ' + str(score_num_svm))
	# predict_result = numeric_svm.predict(train_features)
	# print('numeric_svm -- confusion matrix:')
	# print(confusion_matrix(train_labels, predict_result))


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-y', required = False, default = '2017', help = 'year')
	parser.add_argument('-m', required = True, help = 'month')
	parser.add_argument('-d', required = True, help = 'day')
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