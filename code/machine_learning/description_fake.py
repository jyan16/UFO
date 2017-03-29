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
				if random.randint(1,10)==1:
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
						  le_weather.transform([row[4].lower()])[0]])
		else:
			train_features.append([row[0], row[1], int(row[2].split(':')[0]), le_shape.transform([row[3].lower()])[0],
						  le_weather.transform([row[4].lower()])[0]])

	train_features = preprocessing.scale(train_features)
	novelty_features = preprocessing.scale(novelty_features)

	return (train_features, novelty_features)

def classifier_svm():
	#preprocessing summary data
	tokenizer = Tokenizer()
	vectorizer = CountVectorizer(binary=True, lowercase=True, decode_error='replace', tokenizer=tokenizer)
	(training_labels, training_texts) = load_file('../../data/processed/file_ufo_lat.csv')
	training_features = vectorizer.fit_transform(training_texts)
	training_labels = numpy.array(training_labels)

	#using svm to train data
	classifier_svm = svm.SVC(kernel = 'rbf')
	classifier_svm.fit(training_features, training_labels)

	#training accuracy
	print('training mean accuracy:')
	print(classifier_svm.score(training_features, training_labels))

	#confusion matrix
	predict_result = classifier_svm.predict(training_features)
	print('confusion matrix:')
	print(confusion_matrix(training_labels, predict_result))

def outlier_svm():
	(training_features, novelty_features)= load_database(c)
	classifier = svm.OneClassSVM()
	classifier.fit(training_features)
	predict_result = classifier.predict(novelty_features)
	print(confusion_matrix([-1] * len(novelty_features), predict_result))
def main():

	#classifier_svm()
	#load data from my_ufo.db
	conn = sqlite3.connect('../../data/my_ufo.db')
	c = conn.cursor()
	outlier_svm()




if __name__ == '__main__':
	main()
