import matplotlib.pyplot as plt
import xlrd


#get data from excel
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
