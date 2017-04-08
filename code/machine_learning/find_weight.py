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

#connect to database
conn = sqlite3.connect('../../data/my_ufo.db')
c = conn.cursor()

#load summary data from file, assign fake labels to event that doesn't have nuforc in summary
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

#load other data from table weathers and events, with scale and numerical processing
def load_database(c):
	summary_list = []
	for row in c.execute('''SELECT distinct summary
	                        FROM weathers'''):
		summary_list.append(row[0].lower())
	le_weather = preprocessing.LabelEncoder().fit(summary_list)
	shape_list = []
	for row in c.execute('''SELECT distinct shape
	                        FROM events'''):
		shape_list.append(row[0].lower())
	le_shape = preprocessing.LabelEncoder().fit(shape_list)
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

def check():
	print('*********The following result is based on UFO numerical data**********')
	#defining cross validation score parameter cv
	cv = ShuffleSplit(n_splits=5, test_size=0.2)

	#init data
	(true_features, fake_features) = load_database(c)
	train_labels = [1] * len(true_features) + [0] * len(fake_features)
	train_features = numpy.array(list(true_features) + list(fake_features))

	#logistic regression
	for i in range(1, 20):
		print('training logistic regression with weight: ' + str(i) + '......')
		classifier_lr = LogisticRegression(class_weight={0:i})
		classifier_lr.fit(train_features, train_labels)
		score = cross_val_score(classifier_lr, train_features, train_labels, scoring='accuracy', cv=cv)
		print(score)
		print('cross validation mean and std:')
		print(score.mean(), score.std())
		predict_result = classifier_lr.predict(train_features)
		print('confusion matrix:')
		print(confusion_matrix(train_labels, predict_result))
		print('******************************************************************')
	#svm
	for i in range(1, 13):
		print('training svm with weight: ' + str(i) + '......')
		classifier_svm = svm.SVC(kernel = 'rbf', class_weight={0:i})
		classifier_svm.fit(train_features, train_labels)
		score = cross_val_score(classifier_svm, train_features, train_labels, scoring='accuracy', cv=cv)
		print(score)
		print('cross validation mean and std:')
		print(score.mean(), score.std())
		predict_result = classifier_svm.predict(train_features)
		print('confusion matrix:')
		print(confusion_matrix(train_labels, predict_result))
		print('******************************************************************')

	print('*********The following result is based on UFO description summary**********')
	#defining cross validation score parameter cv
	cv = ShuffleSplit(n_splits=5, test_size=0.2)
	#init data
	tokenizer = Tokenizer()
	vectorizer = CountVectorizer(binary=True, lowercase=True, decode_error='replace', tokenizer=tokenizer)
	(training_labels, training_texts) = load_file('../../data/processed/file_ufo_lat.csv')
	training_features = vectorizer.fit_transform(training_texts)
	training_labels = numpy.array(training_labels)

	#using logistic regression to train data
	for i in range(1, 20):
		print('training logistic regression with weight: ' + str(i) + '......')
		classifier_logistic = LogisticRegression(class_weight={0:i})
		classifier_logistic.fit(training_features, training_labels)
		score = cross_val_score(classifier_logistic, training_features, training_labels, scoring='accuracy', cv=cv)
		print(score)
		print('Logistic -- cross validation mean and std:')
		print(score.mean(), score.std())
		predict_result = classifier_logistic.predict(training_features)
		print('Logistic -- confusion matrix:')
		print(confusion_matrix(training_labels, predict_result))
		print('******************************************************************')

	#using svm to train data
	for i in range(1, 13):
		print('training svm with weight: ' + str(i) + '......')
		classifier_svm = svm.SVC(kernel = 'rbf', class_weight = {0:i})
		classifier_svm.fit(training_features, training_labels)
		score = cross_val_score(classifier_svm, training_features, training_labels, scoring='accuracy', cv=cv)
		print(score)
		print('SVM -- cross validation mean and std:')
		print(score.mean(), score.std())
		predict_result = classifier_svm.predict(training_features)
		print('SVM -- confusion matrix:')
		print(confusion_matrix(training_labels, predict_result))
		print('******************************************************************')

	for i in range(1, 20):
		print('training svm with weight: ' + str(i) + '......')
		classifier_lsvm = svm.LinearSVC(class_weight = {0:i})
		classifier_lsvm.fit(training_features, training_labels)
		score = cross_val_score(classifier_lsvm, training_features, training_labels, scoring='accuracy', cv=cv)
		print(score)
		print('LinearSVM -- cross validation mean and std:')
		print(score.mean(), score.std())
		predict_result = classifier_lsvm.predict(training_features)
		print('LinearSVM -- confusion matrix:')
		print(confusion_matrix(training_labels, predict_result))
		print('******************************************************************')



if __name__ == '__main__':
	check()