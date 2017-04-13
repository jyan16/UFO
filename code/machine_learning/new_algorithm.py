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
from sklearn.neighbors import KNeighborsClassifier


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
	# joblib.dump(le_weather, '../models/weather_trans.pkl') #save le_weather

	shape_list = []
	for row in c.execute('''SELECT distinct shape
	                        FROM events'''):
		shape_list.append(row[0].lower())
	le_shape = preprocessing.LabelEncoder().fit(shape_list)
	# joblib.dump(le_shape, '../models/shape_trans.pkl') #save le_shape

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


def classifier_text_knn(training_labels, training_features):
	print('training KNN......')
	classifier_knn = KNeighborsClassifier(n_neighbors=10)
	classifier_knn.fit(training_features, training_labels)
	predict_result = classifier_knn.predict(training_features)
	print('KNN -- confusion matrix:')
	print(confusion_matrix(training_labels, predict_result))
	return classifier_knn


def classifier_text():
	print('*********The following result is based on UFO description summary**********')
	tokenizer = Tokenizer()
	vectorizer = CountVectorizer(binary=True, lowercase=True, decode_error='replace', tokenizer=tokenizer)
	(training_labels, training_texts) = load_file('../../data/processed/file_ufo_lat.csv')
	training_features = vectorizer.fit_transform(training_texts)
	training_labels = numpy.array(training_labels)
	classifier_knn = classifier_text_knn(training_labels, training_features)

def classifier_num(c):
	print('*********The following result is based on UFO numerical features**********')
	(training_labels, training_features) = load_database(c)
	classifier_knn = classifier_text_knn(training_labels, training_features)

def main():
	# classifier_text()
	conn = sqlite3.connect('../../data/my_ufo.db')
	c = conn.cursor()
	classifier_num(c)

if __name__ == '__main__':
	main()