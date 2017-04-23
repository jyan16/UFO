import matplotlib.pyplot as plt
import xlrd
from IPython.display import Image
from sklearn.externals import joblib
from sklearn import tree
from sklearn.datasets import load_iris
import pydotplus
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
if __name__=='__main__':
	draw_tree()