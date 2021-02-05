import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.preprocessing import MinMaxScaler
import  kneed

potatos = pd.read_csv('kartoffeln.csv')
# initial cleanup
# remove leading and trailing blanks
potatos.columns = potatos.columns.str.strip()
# the data are pandas dataframe -> potatos.drop()
potatos = potatos.drop(['kartoffel'], axis=1)  # drop index column
# do data type check and conversion
dtypes_after_read = potatos.dtypes
# change the class to category -> must not be not scaled!
potatos['kartoffelart'] = potatos['kartoffelart'].astype('category')
dtypes_after_cleanup = potatos.dtypes

X = potatos.iloc[:, :-1]
labels = potatos.columns
y = potatos['kartoffelart']

scaler = MinMaxScaler()
X = scaler.fit_transform(X)
# print(tabulate(X))

n_cluster = [2, 3, 5, 12]
n_cluster = range(3,21,2)


silhouette_data = pd.DataFrame(columns=['number_of_clusters', 'silhouette_score_avg', 'sample_silhouette_values','RAND_index','model_predict'])

for k in n_cluster:
	model = KMeans(n_clusters=k,
				   random_state=0,
				   n_init=10,
				   max_iter=300)
	model_predict = model.fit_predict(X)
	silhouette_score_avg = silhouette_score(X, model_predict)
	sample_silhouette_values = silhouette_samples(X, model_predict)
	sse = model.inertia_

	# # Create a subplot with 1 row and 2 columns
	# fig, (ax1, ax2) = plt.subplots(1, 2)
	# fig.set_size_inches(18, 7)
	#
	# # The 1st subplot is the silhouette plot
	# # The silhouette coefficient can range from -1, 1
	# # ax1.set_xlim([-1, 1])
	# # The (k+1)*10 is for inserting blank space between silhouette
	# # plots of individual clusters, to demarcate them clearly.
	# ax1.set_ylim([0, len(X) + (k + 1) * 10])
	#
	# y_lower = 10
	# for i in range(k):
	# 	# Aggregate the silhouette scores for samples belonging to
	# 	# cluster i, and sort them
	# 	ith_cluster_silhouette_values = sample_silhouette_values[model_predict == i]
	# 	ith_cluster_silhouette_values.sort()
	#
	# 	size_cluster_i = ith_cluster_silhouette_values.shape[0]
	# 	# equiviliant
	# 	size_cluster_i = len(ith_cluster_silhouette_values)
	#
	# 	y_upper = y_lower + size_cluster_i
	#
	# 	color = cm.nipy_spectral(float(i) / k)
	# 	ax1.fill_betweenx(np.arange(y_lower, y_upper),
	# 					  0, ith_cluster_silhouette_values,
	# 					  facecolor=color, edgecolor=color, alpha=0.7)
	#
	# 	# Label the silhouette plots with their cluster numbers at the middle
	# 	ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
	#
	# 	# Compute the new y_lower for next plot
	# 	y_lower = y_upper + 10  # 10 for the 0 samples
	#
	# ax1.set_title("The silhouette plot for the various clusters.")
	# ax1.set_xlabel("The silhouette coefficient values")
	# ax1.set_ylabel("Cluster label")
	#
	# # The vertical line for average silhouette score of all the values
	# ax1.axvline(x=silhouette_score_avg, color="red", linestyle="--")
	#
	# # 2nd Plot showing the actual clusters formed
	# colors = cm.nipy_spectral(model_predict.astype(float) / k)
	# ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
	# 			c=colors, edgecolor='k')
	#
	# # Labeling the clusters
	# centers = model.cluster_centers_
	# # Draw white circles at cluster centers
	# ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
	# 			c="white", alpha=1, s=200, edgecolor='k')
	#
	# for i, c in enumerate(centers):
	# 	ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
	# 				s=50, edgecolor='k')
	#
	# ax2.set_title("The visualization of the clustered data.")
	# ax2.set_xlabel("Feature space for the 1st feature")
	# ax2.set_ylabel("Feature space for the 2nd feature")
	#
	# plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
	# 			  "with n_clusters = {:d}".format(k)),
	# 			 fontsize=14, fontweight='bold')
	#
	# plt.show()

	silhouette_data_dict = dict(number_of_clusters=k,
								silhouette_score_avg=silhouette_score(X, model_predict),
								sample_silhouette_values=silhouette_samples(X, model_predict),
								model_predict=model_predict,
								sse=sse)
	silhouette_data = silhouette_data.append(silhouette_data_dict, ignore_index=True)

max_avg = silhouette_data['silhouette_score_avg'].max()
best_k = silhouette_data[silhouette_data['silhouette_score_avg'] == max_avg]['number_of_clusters'][0]
# print('Best Silhouette Coefficient with number of clusters {:d}'.format(best_k))
#
# fig, ax = plt.subplots(1, 2)
# fig.set_size_inches(18, 7)
# x = silhouette_data['number_of_clusters']
# y = silhouette_data['sse']
# ax[1].set_xlabel('Number of cluster')
# ax[1].set_ylabel('SSE')
# ax[1].set_title('SSE Plot')
# ax[1].plot(x, y)
# ax[1].scatter(x, y, marker='o', c="white", alpha=1, s=200, edgecolor='k')
# ax[1].axvline(x=best_k, color="red", linestyle="--")
# best_k = kneed.KneeLocator(n_cluster ,silhouette_data['sse']).elbow
# ax[1].axvline(x=best_k, color="blue", linestyle="-.")
#
#
# x = silhouette_data['number_of_clusters']
# y = silhouette_data['silhouette_score_avg']
# ax[0].set_xlabel('Number of cluster')
# ax[0].xaxis.set_major_locator(MaxNLocator(integer=True))
# ax[0].set_ylabel('avg Silhouette Score')
# ax[0].set_ylim(0, 1)
# ax[0].set_title('Silhouette Plot')
# ax[0].plot(x, y, )
# ax[0].scatter(x, y, marker='o', c="white", alpha=1, s=200, edgecolor='k')
# ax[0].axvline(x=best_k, color="red", linestyle="--")

plt.show()

model_predict = silhouette_data[silhouette_data['number_of_clusters'] == best_k]
model_predict = model_predict[0][4]
print(model_predict)