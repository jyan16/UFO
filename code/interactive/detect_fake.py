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

def load_database(c):
	le_shape = joblib.load('../models/shape_trans.pkl')
	le_weather = joblib.load('../models/weather_trans.pkl')
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

	train_features = preprocessing.scale(train_features)
	novelty_features = preprocessing.scale(novelty_features)
	return (numpy.array(train_features), numpy.array(novelty_features))
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-year', required = True, default = '2017')
	opts = parser.parse_args()
	print('what the fuck')

	conn = sqlite3.connect('../../data/my_ufo.db')
	c = conn.cursor()



if __name__ == '__main__':
	main()