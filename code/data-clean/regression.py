import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

#This script fit the number of sightings with year, population and area of a state


#connection to database
conn = sqlite3.connect('../../data/my_ufo.db')
c = conn.cursor()

#getting data

data_list = []
x_train = []
y_train = []

for row in c.execute('''SELECT e.year, population, area, count(*)
                        FROM events e, populations p, areas a
                        WHERE e.year>=1980 AND e.year<=2016 AND e.state=p.state AND e.state=a.state
                        GROUP BY e.state, e.year'''):

	x_train.append([row[0], row[1], row[2]])
	y_train.append([row[3]])



featurizer = preprocessing.PolynomialFeatures(degree=3)
X_train_transform = featurizer.fit_transform(x_train)
regressor = LinearRegression()
regressor.fit(X_train_transform, y_train)
#xx_quadratic = quadratic_featurizer.transform(np.array(x_list).reshape(np.array(x_list).shape[0], 1))
print(regressor.score(X_train_transform, y_train))

'''
#le_state = preprocessing.LabelEncoder().fit(list(set(x_list)))
#x_list = le_state.transform(x_list)
#train_data_list = [[item1, item2] for item1, item2 in zip(x_list, y_list)]
train_data_list = y_list
quadratic_featurizer = preprocessing.PolynomialFeatures(degree=3)
quadratic_feature = quadratic_featurizer.fit(train_data_list)
regressor = LinearRegression()
regressor.fit(quadratic_feature, z_list)
print(regressor.score(quadratic_feature, z_list))'''