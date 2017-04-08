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
	le_scale = joblib.load('../models/data_scale.pkl')

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
	train_features = le_scale.transform(train_features)
	novelty_features = le_scale.transform(novelty_features)

	return (numpy.array(train_features), numpy.array(novelty_features))

def test(c):
	#load models
	vectorizer = joblib.load('../models/vectorizer.pkl')
	numeric_outlier = joblib.load('../models/numeric_outlier.pkl')
	numeric_svm = joblib.load('../models/numeric_svm.pkl')
	summary_log = joblib.load('../models/summary_log.pkl')
	summary_svm = joblib.load('../models/summary_svm.pkl')

	#load data

	print('*********The following result is based on UFO description summary**********')
	(true_features, fake_features) = load_database(c)



	(training_labels, training_texts) = load_file('../../data/processed/file_ufo_lat.csv')
	training_features = vectorizer.transform(training_texts)



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-year', required = True, default = '2017')
	opts = parser.parse_args()
	print('what the fuck')

	conn = sqlite3.connect('../../data/my_ufo.db')
	c = conn.cursor()
	test(c)




if __name__ == '__main__':
	main()