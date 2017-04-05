import matplotlib.pyplot as plt

#draw cross validation result for weighted svm classifier
cross_validation_score_mean = [0.9543, 0.9706, 0.9748, 0.9758, 0.9761, 0.9766,
						  		0.9764, 0.9759, 0.9758, 0.9755, 0.9752, 0.9750, 0.9748]
cross_validation_score_std = [0.001635, 0.000810, 0.001503, 0.000806, 0.000762, 0.000889,
							  0.000727, 0.001038, 0.001237, 0.000553, 0.001077, 0.000601, 0.000958]
x = [1,2,3,4,5,6,7,8,9,10,11,12,13]

fig1, ax1_fig1 = plt.subplots()
ax2_fig1 = ax1_fig1.twinx()
ax1_fig1.plot(x, cross_validation_score_mean, linewidth = 3, color = '#BE4B48')
ax1_fig1.set_ylim([0.95,0.98])
ax1_fig1.set_ylabel('accuracy mean')
ax1_fig1.set_xlabel("weight of class '0'")
ax2_fig1.plot(x, cross_validation_score_std, linewidth = 1, color = '#4A7EBB')
ax2_fig1.set_ylim([0,0.004])
ax2_fig1.set_ylabel('accuracy std')
plt.title('weighted SVM with numeric features')
plt.show()