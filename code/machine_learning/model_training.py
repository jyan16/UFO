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
from sklearn.externals import joblib


#load summary data for text classifier
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

#load database for numerical classifier
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
	train_labels = []
	for row in c.execute('''SELECT e.lat, e.lng, e.time, e.shape, w.summary, w.visibility, e.summary
	                        FROM events e, weathers w
	                        WHERE e.year>=1950 AND e.year<=2017 AND e.event_id=w.event_id
	                     '''):
		text = row[6].lower()
		train_features.append([row[0], row[1], int(row[2].split(':')[0]), le_shape.transform([row[3].lower()])[0],
							   le_weather.transform([row[4].lower()])[0], row[5]])
		if 'nuforc' in text or 'hoax' in text:
			train_labels.append(0)
		else:
			train_labels.append(1)


	return (numpy.array(train_labels), numpy.array(train_features))

def classifier_text_svm(training_labels, training_features):
	print('training svm......')
	classifier_svm = svm.SVC(class_weight = {0:10}, kernel='linear', probability=True)
	classifier_svm.fit(training_features, training_labels)
	joblib.dump(classifier_svm, '../models/summary_svm.pkl')  # save summary svm
	# score = cross_val_score(classifier_svm, training_features, training_labels, scoring='accuracy')
	# print(score)
	# print('SVM -- cross validation mean and std:')
	# print(score.mean(), score.std())
	predict_result = classifier_svm.predict(training_features)
	print('SVM -- confusion matrix:')
	print(confusion_matrix(training_labels, predict_result))
	print('***********************************************************************')
	return classifier_svm

def classifier_text_log(training_labels, training_features):
	print('training logistic regression......')
	classifier_logistic = LogisticRegression(class_weight={0:10})
	classifier_logistic.fit(training_features, training_labels)
	joblib.dump(classifier_logistic, '../models/summary_log.pkl') #save summary logistic
	# score = cross_val_score(classifier_logistic, training_features, training_labels, scoring='accuracy', cv=cv)
	# print(score)
	# print('Logistic -- cross validation mean and std:')
	# print(score.mean(), score.std())
	predict_result = classifier_logistic.predict(training_features)
	print('Logistic -- confusion matrix:')
	print(confusion_matrix(training_labels, predict_result))
	return classifier_logistic

def classifier_text():
	print('*********The following result is based on UFO description summary**********')
	#defining cross validation score parameter cv
	# cv = ShuffleSplit(n_splits=5, test_size=0.2)

	#################
	#initialize data#
	#################
	tokenizer = Tokenizer()
	vectorizer = CountVectorizer(binary=True, lowercase=True, decode_error='replace', tokenizer=tokenizer)
	(training_labels, training_texts) = load_file('../../data/processed/file_ufo_lat.csv')
	training_features = vectorizer.fit_transform(training_texts)
	joblib.dump(vectorizer,'../models/vectorizer.pkl') #save vectorizer
	training_labels = numpy.array(training_labels)

	####################
	#training svm model#
	####################
	classifier_svm = classifier_text_svm(training_labels, training_features)
	util.print_most_informative_features('svm', vectorizer, classifier_svm)

	####################
	#training log model#
	####################
	classifier_log = classifier_text_log(training_labels, training_features)
	util.print_most_informative_features('log', vectorizer, classifier_log)


def classifier_num_svm(training_labels, training_features):
	print('training svm......')
	classifier_svm = svm.SVC(kernel = 'rbf', class_weight={0:12}, probability=True)
	classifier_svm.fit(training_features, training_labels)
	joblib.dump(classifier_svm, '../models/numeric_svm.pkl')  # save numeric svm
	# score = cross_val_score(classifier_svm, train_features, train_labels, scoring='accuracy', cv=cv)
	# print(score)
	# print('SVM -- cross validation mean and std:')
	# print(score.mean(), score.std())
	predict_result = classifier_svm.predict(training_features)
	print('SVM -- confusion matrix:')
	print(confusion_matrix(training_labels, predict_result))
	print('parameter:')
	classifier_svm.get_params()
	print('***********************************************************************')
	return classifier_svm


	############################################
	#below we train model with numeric features#
	############################################

def classifier_num(c):
	print('*********The following result is based on UFO numerical data**********')
	#defining cross validation score parameter cv
	# cv = ShuffleSplit(n_splits=5, test_size=0.2)

	#################
	#initialize data#
	#################
	(training_labels, training_features) = load_database(c)
	#svm
	classifier_svm = classifier_num_svm(training_labels, training_features)

	#Since our data is really imbalanced, here we don't even need to try Naive Bayes...


def main():
	#connect to database
	# conn = sqlite3.connect('../../data/my_ufo.db')
	# c = conn.cursor()
	#
	# classifier_num(c)
	# outlier_svm(c)
	classifier_text()







if __name__ == '__main__':
	main()
