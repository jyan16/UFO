from __future__ import division
import sys
import csv
import argparse
from collections import defaultdict

import util

import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from tokenizer import Tokenizer

#load data from file, assign fake labels to event that doesn't have nuforc in summary
def load_file(file_path):
	count_0 = 0
	count_1 = 0
	confidence = []
	description = []
	with open(file_path, 'r', encoding='latin1') as file_reader:
		reader = csv.reader(file_reader, delimiter=',', quotechar='"')
		next(reader, None)
		for row in reader:
			text = row[9].lower()
			if 'nuforc' in text or 'hoax' in text:
				confidence.append(0)
				count_0 += 1
			else:
				confidence.append(1)
				count_1 += 1
			description.append(row[9])
	print(count_0, count_1)
	return (confidence, description)

def main():

	tokenizer = Tokenizer()
	vectorizer = CountVectorizer(binary=True, lowercase=True, decode_error='replace', tokenizer=tokenizer)
	#vectorizer = CountVectorizer(binary=True, lowercase=True, decode_error='replace')

	# Load training text and training labels
	(training_labels, training_texts) = load_file('../../data/processed/file_ufo_lat.csv')
	# Get training features using vectorizer
	training_features = vectorizer.fit_transform(training_texts)
	# Transform training labels to numpy array (numpy.array)
	training_labels = numpy.array(training_labels)
	############################################################

	##### TRAIN THE MODEL ######################################
	# Initialize the corresponding type of the classifier
	# NOTE: Be sure to name the variable for your classifier "classifier" so that our stencil works for you!
	if opts.classifier == 'nb':
		# TODO: Initialize Naive Bayes
		classifier = BernoulliNB(binarize=None)
	elif opts.classifier == 'log':
		# TODO: Initialize Logistic Regression
		classifier = LogisticRegression()
	elif opts.classifier == 'svm':
		# TODO: Initialize SVM
		classifier = LinearSVC()
	else:
		raise Exception('Unrecognized classifier!')

	# TODO: Train your classifier using 'fit'
	classifier.fit(training_features, training_labels)
	############################################################


	###### VALIDATE THE MODEL ##################################
	# TODO: Print training mean accuracy using 'score'
	if opts.p:
		print('training mean accuracy:')
		print(classifier.score(training_features, training_labels))
	# TODO: Perform 10 fold cross validation (cross_val_score) with scoring='accuracy'
	score = cross_val_score(classifier, training_features,
							training_labels, scoring='accuracy', cv=10 )

	# TODO: Print the mean and std deviation of the cross validation score
	if opts.p:
		print('mean and std dev for cross validation scores:')
		print('mean = %f, std = %f' % (score.mean(), score.std()))

	############################################################

	##### EXAMINE THE MODEL ####################################
	if (opts.top is not None) and opts.p:
		# Print top n most informative features for positive and negative classes
		print('most informative features:')
		util.print_most_informative_features(opts.classifier, vectorizer, classifier, opts.top)
	############################################################


	##### TEST THE MODEL #######################################
	if opts.test is None:
		# Test the classifier on one sample test tweet
		# James Cameron 9:04 AM - 28 Jan 11
		test_tweet = 'ryan seacrest told me I had to get on Twitter.  So here I am.  First tweet.  I feel younger already.'
		# TODO: Extract features from the test tweet and transform them using vectorizer
		# HINT: vectorizer.transform() expects a list of tweets
		test_feature = vectorizer.transform([test_tweet])
		# TODO: Print the predicted label of the test tweet
		if opts.p:
			print('predicted label for test tweet:')
			print(classifier.predict(test_feature))


		# TODO: Print the predicted probability of each label.
		if opts.p:
			print('predicted probability for each label:')
		if opts.classifier != 'svm':
			# Use predict_proba
			print(classifier.predict_proba(test_feature))

		else:
			# Use decision_function
			print(classifier.decision_function(test_feature))

	else:
		# Test the classifier on the given test set
		# TODO: Load test labels and texts using load_file()

		(test_labels, test_texts) = load_file(opts.test)

		test_labels = numpy.array(test_labels)

		# TODO: Extract test features using vectorizer.transform()
		test_features = vectorizer.transform(test_texts)

		# TODO: Predict the labels for the test set
		test_result = classifier.predict(test_features)

		# TODO: Print mean test accuracy
		if opts.p:
			right_result = 0
			print('predicted mean accuracy:')
			for label_true, label_pred in zip(test_labels, test_result):
				if label_true == label_pred:
					right_result += 1
			print(right_result/len(test_labels))
		# TODO: Print the confusion matrix using your implementation
			print('our confusion matrix:')
			TP = FN = FP = TN = 0
			for label_true, label_pred in zip(test_labels, test_result):
				if label_true == 1 and label_pred == 1:
					TP += 1
				if label_true == 1 and label_pred == 0:
					FN += 1
				if label_true == 0 and label_pred == 1:
					FP += 1
				if label_true == 0 and label_pred == 0:
					TN += 1
			print('          Positive    Negtive')
			print('Positive  %8d    %7d' % (TP, FN))
			print('Negtive   %8d    %7d' % (FP, TN))
		# TODO: Print the confusion matrix using sklearn's implementation
			print('sklearn confusion matrix:')
			sk_confusion = confusion_matrix(test_labels, test_result)
			print('          Positive    Negtive')
			print('Positive  %8d    %7d' % (sk_confusion[1][1], sk_confusion[1][0]))
			print('Negtive   %8d    %7d' % (sk_confusion[0][1], sk_confusion[0][0]))

	############################################################


if __name__ == '__main__':
	main()
