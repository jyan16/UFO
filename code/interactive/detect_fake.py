from __future__ import division

import csv
import sqlite3
import util
from tokenizer import Tokenizer
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from sklearn.linear_model import LogisticRegression
import random
from sklearn.externals import joblib
import argparse

def load_file(file_path):
	confidence = []
	description = []
	with open(file_path, 'r', encoding='latin1') as file_reader:
		reader = csv.reader(file_reader, delimiter=',', quotechar='"')
		next(reader, None)
		for row in reader:
			text = row[9].lower()
			if 'nuforc' in text or 'hoax' in text:
				confidence.append(0)
				description.append(row[9])
			else:
				confidence.append(1)
				description.append(row[9])
	return (confidence, description)

def load_database(c):

	#load preprocessing model
	le_shape = joblib.load('../models/shape_trans.pkl')
	le_weather = joblib.load('../models/weather_trans.pkl')

	#load data
	train_features = []
	novelty_features = []
	for row in c.execute('''SELECT e.lat, e.lng, e.time, e.shape, w.summary, w.visibility, e.summary
	                        FROM events e, weathers w
	                        WHERE e.year>=1950 AND e.year<=2017 AND e.event_id=w.event_id
	                     '''):
		text = row[6].lower()
		if 'nuforc' in text or 'hoax' in text:
			novelty_features.append([row[0], row[1], int(row[2].split(':')[0]), le_shape.transform([row[3].lower()])[0],
						  le_weather.transform([row[4].lower()])[0], row[5]])
		else:
			train_features.append([row[0], row[1], int(row[2].split(':')[0]), le_shape.transform([row[3].lower()])[0],
						  le_weather.transform([row[4].lower()])[0], row[5]])

	#preprocessing data

	return (numpy.array(train_features), numpy.array(novelty_features))

def test(c):
	#load models
	vectorizer = joblib.load('../models/vectorizer.pkl')
	numeric_svm = joblib.load('../models/numeric_svm.pkl')
	summary_log = joblib.load('../models/summary_log.pkl')
	summary_svm = joblib.load('../models/summary_svm.pkl')

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
	parser.add_argument('-y', required = False, default = '2017')
	parser.add_argument('-m', required = True)
	parser.add_argument('-d', required = True)
	parser.add_argument('-h', required = True,)
	opts = parser.parse_args()
	print('what the fuck')

	conn = sqlite3.connect('../../data/my_ufo.db')
	c = conn.cursor()
	test(c)




if __name__ == '__main__':
	main()