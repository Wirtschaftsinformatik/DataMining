import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

iris = load_iris()
iris['data'] = iris['data'][:, [1, 2]]

X_train, X_test, y_train, y_test = train_test_split(iris['data'],
                                                    iris['target'],
                                                    test_size=0.33,
                                                    random_state=666
                                                    )

steps = [
	('scaler', StandardScaler()),
	('knn', KNeighborsClassifier())
]

param_grid = {'knn__n_neighbors': np.arange(3, 25, 2),
              'knn__leaf_size': np.arange(2, 25, 2)}
pipe = Pipeline(steps=steps)
grid = GridSearchCV(pipe, param_grid=param_grid, cv=5)
grid.fit(X_train, y_train)
grid.score(X_test, y_test)
print('Best parameters: {}'.format(grid.best_params_))
print('Best scores: {}'.format(grid.best_score_))
pipe = grid.best_estimator_

pipe = grid.best_estimator_

# store the pipeline

pd.to_pickle(pipe, 'pipeline.pickle')
pipe2 = pd.read_pickle('pipeline.pickle')
print(pipe2)

from mlxtend.plotting import plot_decision_regions
# Plotting decision region

import matplotlib.pyplot as plt

plot_decision_regions(iris['data'],
                      iris['target'],
                      # clf=pipe.named_steps['knn'],
                      clf=grid,
                      legend=2
                      )
plt.xlabel(iris['feature_names'][1])
plt.ylabel(iris['feature_names'][2])
plt.title('Knn with K=' + str(grid.best_params_['knn__n_neighbors']))
plt.show()
