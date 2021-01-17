import itertools
import os

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.datasets import load_iris, load_wine, load_breast_cancer
from sklearn.preprocessing import StandardScaler


def initialise(*, data=None):
	if not os.path.isdir('result'):
		os.mkdir('result')

	if len(data.target_names) != None:
		k = len(data.target_names)
	else:
		k = imput('Please specify the number of clusters')
	return k


def myKMEANS(*, data=None, k=1):
	'''

	:param data:
	:param k:  number of cluster
	:return:
	'''
	method = 'k-means++'  # kmeans classic will be 'random'
	kmeans = KMeans(n_clusters=k, init=method, n_init=1, random_state=666)
	result = kmeans.fit_predict(data)
	return result


def myAGNES(*, data=None, k=1):
	'''

	:param data:
	:param k: number of cluster
	:return:
	'''
	distance = 'euclidean'
	linkage = 'ward'
	agnes = AgglomerativeClustering(n_clusters=k, affinity=distance, linkage=linkage)
	result = agnes.fit_predict(data)
	return result


def myDBSCAN(*, data=None):
	'''

	:param data:
	:return:
	'''
	distance = 'euclidean'
	dbscan = DBSCAN(metric=distance)
	result = dbscan.fit_predict(data)
	# amend the result by one to match other cluster results
	result += 1
	return result


def MyScaler(*, data=None):
	'''

	:param data:
	:return:
	'''
	scaler = StandardScaler()
	data_scaled = scaler.fit_transform(data)
	return data_scaled


def myPlot(*, data=None, target=None):
	if target is not None:
		# get all feature combination in 2 dimensions
		feature_names_2D = list(itertools.combinations(data.feature_names, 2))

		# define the number of plots
		n = len(target.columns)
		m = len(feature_names_2D)

		# define some graphical properties
		colours = ['blue', 'red', 'black', 'green']  # make it fancy
		markers = ['+', '.', 'o', '*']
		marker_size = 100
		# marker_size = input("Specify marker size (default: 100) :")
		# if len(marker_size)==0:
		# 	marker_size=100
		# else:
		# 	marker_size=int(marker_size)

		# loop through all feature combinations
		for ii, feature_combination in enumerate(feature_names_2D):
			fig, ax = plt.subplots(nrows=1, ncols=n, constrained_layout=True)
			fig_size = 10
			fig.set_size_inches(fig_size * len(target.columns), fig_size)

			# loop through all models
			for i, model_ in enumerate(target.columns):
				ax[i].set_title(model_, fontsize=25)

				# since we combine the feature names, we first have to get the colum index
				X_column_index = data.feature_names.index(feature_names_2D[0][0])
				Y_column_index = data.feature_names.index(feature_names_2D[0][1])

				# now we select the data with the index from above
				X = data.data[:, X_column_index]
				Y = data.data[:, Y_column_index]

				# specify diagram details
				X_border_dist = (X.max() - X.min()) * .1
				Y_border_dist = (Y.max() - Y.min()) * .1
				ax[i].set_xlim(X.min() - X_border_dist, X.max() + X_border_dist)
				ax[i].set_ylim(Y.min() - Y_border_dist, Y.max() + Y_border_dist)
				ax[i].set_xlabel(feature_names_2D[ii][0], fontsize=20)
				ax[i].set_ylabel(feature_names_2D[ii][1], fontsize=20)

				for index in range(len(X)):
					# marker_size=40
					marker = markers[target[model_][index]]  # marker depending on the target class
					colour = colours[target[model_][index]]  # color depending on the target class
					ax[i].scatter(x=X[index], y=Y[index], s=marker_size, marker=marker, color=colour)
#			plt.tight_layout(rect=[0, 0.1, 1, 0.8])
			plt.subplots_adjust(top=0.85)

			#fig.suptitle("comparison between {} for different algorithm".format(feature_combination), fontsize=30)
			filename = os.path.join('result',
								'kmeans_agnes_dbscan_{}_{}.png'.format(feature_combination[0], feature_combination[1]).replace(' ', '_'))
			print('File saved to {}'.format(filename))
			plt.savefig(filename)
			plt.show()
		plt.close()


#######################################################################################
# Comparison of different Cluster algorithm
#######################################################################################

data = load_iris()

#######################################################################################
# preprocessing
#######################################################################################

k = initialise(data=data)
dataScaled = MyScaler(data=data.data)

#######################################################################################
# modeling
#######################################################################################

model = pd.DataFrame()
model['Original'] = data.target
model['Kmeans'] = myKMEANS(data=dataScaled, k=k)
model['Agnes'] = myAGNES(data=dataScaled, k=k)
model['Dbscan'] = myDBSCAN(data=dataScaled)

#######################################################################################
# deploy
#######################################################################################

myPlot(data=data, target=model)
# reduced set for testing
# myPlot(data=data, target=model.iloc[:, [0, 1]])
