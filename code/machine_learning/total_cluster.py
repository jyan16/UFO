import numpy as np
from sklearn.cluster import KMeans
import sqlite3
from sklearn import preprocessing
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

#This script tries to cluster ufo report file to see their clusters and similarities to each other
conn = sqlite3.connect('../../data/my_ufo.db')
c = conn.cursor()


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

event_data = []
label_list = []
for row in c.execute('''SELECT e.lat, e.lng, e.time, e.shape, w.summary, w.windSpeed, w.visibility
                        FROM events e, weathers w
                        WHERE e.year>=1950 AND e.year<=2017 AND e.event_id=w.event_id
                     '''):
	event_data.append([row[0], row[1], int(row[2].split(':')[0]),
					   le_weather.transform([row[4].lower()])[0], row[5], row[6]])
	label_list.append(le_shape.transform([row[3].lower()])[0])
event_data = preprocessing.scale(event_data)
label_list = np.array(label_list)
classifier = SVC()
classifier.fit(event_data, label_list)

test_result = classifier.predict(event_data)

sk_confusion = confusion_matrix(label_list, test_result)
print(sk_confusion)
#print(classifier.score(event_data, label_list))
#score = cross_val_score(classifier, event_data,
#						label_list, scoring='accuracy', cv=10)
#print('mean and std dev for cross validation scores:')
#print('mean = %f, std = %f' % (score.mean(), score.std()))

'''#K-Means
for i in range(2, 11):
	kmeans = KMeans(n_clusters=i, random_state=0).fit(event_data)
	print('' + str(i) + ':' + str(metrics.silhouette_score(event_data, kmeans.labels_, metric='euclidean')))
'''
