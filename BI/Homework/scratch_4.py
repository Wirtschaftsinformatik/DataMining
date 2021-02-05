import numpy as np
import pandas as pd
from tabulate import tabulate
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px



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
labels=potatos.columns
y = potatos['kartoffelart']

scaler = MinMaxScaler()
X = scaler.fit_transform(X)
print(tabulate(X))

algorithm = KMeans()

parameters = {'n_clusters': [2, 3, 5, 12],
			  'algorithm': ['auto'],
			  'random_state': [0],
			  'max_iter': [300]
			  }
scores = ['precision', 'recall']

gs = GridSearchCV(algorithm,
				  parameters,
				  return_train_score=True,
				  cv=10
				  )
gs.get_params()
gs.fit(X)

best_estimator = gs.best_estimator_
best_score = gs.best_score_
best_parameter = 'get.parameter(sgs)'
y_predict = gs.predict(X)

#X_predict = X + pd.DataFrame(y)

print('Best estimator {}: '.format(best_estimator))
print('Best score {}: '.format(best_score))

X = pd.DataFrame(X, columns=labels[0:-1])
Xy = pd.concat([X, y], axis=1)

fig = px.parallel_coordinates(Xy, color='kartoffelart')
fig.show()

y_predict = pd.DataFrame(y_predict, columns=['kartoffelart'])
Xy = pd.concat([X, y_predict], axis=1)

fig = px.parallel_coordinates(Xy, color='kartoffelart')
fig.show()

import matplotlib.pyplot as plt
import itertools

# Black removed and is used for noise instead.
colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
fig, ax = plt.subplots(n_dim, n_dim)


n_dim = X.shape[1]
l_dim = np.arange(0, n_dim)
views = list(itertools.product(l_dim, l_dim))

for view in views:
	for k, col in zip(unique_labels, colors):
		if k == -1:
			# Black used for noise.
			col = [0, 0, 0, 1]

		class_member_mask = (labels == k)

		xy = X[class_member_mask & core_samples_mask]
		# plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
		# 		 markeredgecolor='k', markersize=14)
		ax[view[0], view[1]].plot(xy[:, view[0]], xy[:, view[1]], 'o', markersize=3)

		xy = X[class_member_mask & ~core_samples_mask]
		ax[view[0], view[1]].plot(xy[:, view[0]], xy[:, view[1]], '*', markerfacecolor=tuple(col),
								  markeredgecolor='k', markersize=1)

	ax[view[0], view[1]].set_ylabel(feature_names[view[0]], fontsize=4)
	ax[view[0], view[1]].set_xlabel(feature_names[view[1]], fontsize=4)
	ax[view[0], view[1]].tick_params(axis="both", labelsize=4)
