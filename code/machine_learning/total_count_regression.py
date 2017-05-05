import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
import numpy as np
import math
#This script fit the number of sightings with year, population and area of a state


#connection to database
conn = sqlite3.connect('../../data/my_ufo.db')
c = conn.cursor()

#getting data



year = []
y_train = []
x_train = []
for row in c.execute('''SELECT e.year, count(*) 
						FROM events e
						WHERE CAST(e.year AS SIGNED)>=1980 AND CAST(e.year AS SIGNED)<=2016
						GROUP BY e.year
						ORDER BY e.year asc'''):
	year.append([int(row[0])])
	y_train.append(row[1])

population = []
for row in c.execute('''SELECT sum(population)
						FROM populations
						WHERE year>=1980 AND year<=2016
						GROUP BY year
						ORDER BY year asc'''):
	population.append([math.log(row[0])])

for item1, item2 in zip(year, population):
	x_train.append(item1 + item2)



featurizer = preprocessing.PolynomialFeatures(degree=4)
X_train_transform = featurizer.fit_transform(x_train)
regressor = LinearRegression()
regressor.fit(X_train_transform, y_train)
print(regressor.score(X_train_transform, y_train))
X_test = featurizer.transform([2017, 19.60386])
print(regressor.predict(X_test))

