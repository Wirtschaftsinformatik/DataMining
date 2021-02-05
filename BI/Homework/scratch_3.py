import numpy as np
import pandas as pd
from tabulate import tabulate
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import MinMaxScaler

potatos = pd.read_csv('kartoffeln.csv')
# initial cleanup
# remove leading and trailing blanks
potatos.columns = potatos.columns.str.strip()
# the data are pandas dataframe -> potatos.drop()
potatos.drop(['kartoffel'], axis=1)  # drop index column
# do data type check and conversion
dtypes_after_read = potatos.dtypes
# change the class to category -> must not be not scaled!
potatos['kartoffelart'] = potatos['kartoffelart'].astype('category')
dtypes_after_cleanup = potatos.dtypes

X = potatos.iloc[:, :-1]
y = potatos['kartoffelart']

# separate train and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, train_size=.7, random_state=0)

# do standardisation
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
# test set only transform!
X_test = scaler.transform(X_test)

print(tabulate(X_train[:10,:]))

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
gs.fit(X_train)

y_test_prediction = gs.predict(X_test)
best_estimator = gs.best_estimator_
best_score = gs.best_score_
print('Best estimator (on training se!): '.format(best_estimator))
print('Best score (on training se!): '.format(best_score))

prediction = pd.DataFrame(y_test, y_test_prediction, columns= ['Actual', 'Prediction'])

str(gs)
