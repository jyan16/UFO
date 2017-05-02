import matplotlib.pyplot as plt
import xlrd
from IPython.display import Image
from sklearn.externals import joblib
from sklearn import tree
from sklearn.datasets import load_iris
import pydotplus
import sqlite3
import numpy as np
#get data from excel
def draw_score():
	excel = xlrd.open_workbook('../../documentation/RESULT.xlsx')
	table = excel.sheet_by_index(1)

	cross = []
	tp = []
	score = []
	weight = []
	for i in range(1,56):
		row = table.row_values(i)
		weight.append(row[1])
		cross.append(row[6])
		tp.append(row[7])
		score.append(row[8])


	#plot data
	plt.figure(figsize = (10,7))
	plt.subplot(2,2,1)
	plt.plot(weight[0:17], cross[0:17], 'b-')
	plt.plot(weight[0:17], tp[0:17], 'r-')
	plt.plot(weight[0:17], score[0:17], 'g-')
	plt.title('num_svm')


	plt.subplot(2,2,2)
	plt.plot(weight[17:36], cross[17:36], 'b-')
	plt.plot(weight[17:36], tp[17:36], 'r-')
	plt.plot(weight[17:36], score[17:36], 'g-')
	plt.title('text_log')

	ax = plt.subplot(2,2,3)
	a = plt.plot(weight[37:], cross[37:], 'b-')
	b = plt.plot(weight[37:], tp[37:], 'r-')
	c = plt.plot(weight[37:], score[37:], 'g-')
	plt.title('text_svm')

	ax.legend(['cross_valid_score', 'recall', 'judge_score'], loc = 1, bbox_to_anchor = (1.9, 0.6), borderaxespad = 0.)
	plt.show()
def draw_tree():
	numeric_tree = joblib.load('../models/numeric_tree.pkl')
	feature_names = ['lat', 'lng', 'time', 'shape', 'weather', 'visibility']
	class_names = ['fake', 'true']
	dot_data = tree.export_graphviz(numeric_tree, out_file=None,
									feature_names=feature_names,
									class_names=class_names,
									filled=True, rounded=True,
									special_characters=True)
	graph = pydotplus.graph_from_dot_data(dot_data)
	Image(graph.create_png())
def draw_regression():
	conn = sqlite3.connect('../../data/my_ufo.db')
	c = conn.cursor()
	year = []
	count_year = []
	for row in c.execute('''SELECT e.year, count(*) 
							FROM events e
							WHERE CAST(e.year AS SIGNED)>=1980 AND CAST(e.year AS SIGNED)<=2016
							GROUP BY e.year
							ORDER BY e.year asc'''):
		year.append(int(row[0]))
		count_year.append(row[1])


	population = []
	for row in c.execute('''SELECT sum(population)
							FROM populations
							WHERE year>=1980 AND year<=2016
							GROUP BY year
							ORDER BY year asc'''):
		population.append(row[0])

	population = list(np.log(population))
	fig = plt.figure()

	ax1 = fig.add_subplot(111)
	ax1.plot(year, count_year)
	ax1.set_ylabel('Sighting Number')
	ax1.set_ylim(min(count_year), max(count_year))
	ax1.set_xlabel('year')
	ax2 = ax1.twinx()
	ax2.plot(year, population, 'r')
	ax2.set_ylabel('Population')
	ax2.set_ylim(min(population), max(population))

	plt.show()
def draw_duration():
	excel = xlrd.open_workbook('../../documentation/RESULT.xlsx')
	table = excel.sheet_by_index(2)
	state = []
	x = range(1,56)
	margin_mean = []

	for i in range(0, 55):
		row = table.row_values(i)
		state.append(row[0])
		margin_mean.append(row[1])

	plt.scatter(x, margin_mean, marker='o', color='c')
	plt.plot(x, margin_mean)
	plt.xticks(x, state, fontsize=5)
	plt.xlabel('state name')
	plt.ylabel('estimated marginal means')
	plt.show()
if __name__=='__main__':
	draw_regression()