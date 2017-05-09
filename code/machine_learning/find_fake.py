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
from sklearn.externals import joblib
from sklearn.tree import DecisionTreeClassifier
import argparse


def load_numeric(c):

	le_shape = joblib.load('../models/shape_trans.pkl')
	le_weather = joblib.load('../models/weather_trans.pkl')

	# load features and labels
	train_features = []
	train_labels = []
	event_id_list = []
	for row in c.execute('''SELECT e.lat, e.lng, e.time, e.shape, w.summary, w.visibility, e.label, e.event_id
	                        FROM events e, weathers w
	                        WHERE e.year>=1950 AND e.year<=2017 AND e.event_id=w.event_id
	                     '''):
		train_features.append([row[0], row[1], int(row[2].split(':')[0]), le_shape.transform([row[3].lower()])[0],
							   le_weather.transform([row[4].lower()])[0], row[5]])
		train_labels.append(int(row[6]))
		event_id_list.append(row[7])
	return numpy.array(train_labels), numpy.array(train_features), event_id_list

def main():
	conn = sqlite3.connect('../../data/processed/my_ufo.db')
	c = conn.cursor()
	numeric_svm = joblib.load('../models/numeric_svm.pkl')
	train_labels, train_features, event_id_list = load_numeric(c)
	label_predict = numeric_svm.predict(train_features)
	prob_predict = numeric_svm.predict_proba(train_features)
	result = []
	for label, prob in zip(label_predict, prob_predict):
		result.append((label, prob))
	print(result)

if __name__ == '__main__':
	main()