# based on:
# https://www.python-course.eu/expectation_maximization_and_gaussian_mixture_models.php
# theory behind: https://www.youtube.com/watch?v=qMTuMa86NzU
# adapted to use iris dataset

import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')
from sklearn.datasets.samples_generator import make_blobs
import numpy as np
from scipy.stats import multivariate_normal
from sklearn.mixture import GaussianMixture
from sklearn.datasets import load_iris
import os

# 0. Load dataset
samples=load_iris()
X=samples.data
Y=samples.target

GMM = GaussianMixture(n_components=3).fit(X) # Instantiate and fit the model
print('Converged:',GMM.converged_) # Check if the model has converged
means = GMM.means_
covariances = GMM.covariances_


# Predict
Y = np.array([[6],[3.3],[0.5],[0.5]])
prediction = GMM.predict_proba(Y.T)
legend=['samples']
for i, percentage in enumerate(prediction[0]):
	legend.append('Cluster {}: {:000.2f} %'.format(i, percentage*100))
	#print('Cluster {}: {:000.2f} %'.format(i, percentage*100))

# Plot
fig = plt.figure(figsize=(10,10))
ax0 = fig.add_subplot(111)
ax0.scatter(X[:,0],X[:,1])
ax0.scatter(Y[0,:],Y[1,:],c='orange',zorder=10,s=100)
ax0.annotate(xy= (Y[0]+.05 ,Y[1]+.05), s='sample to predict', color='orange', fontsize=24)

colour = ['black', 'green', 'red']
# we display here only the first two features, therefor 0:2
# for all features we would need all combinations an dthen loop through all

i=0
for m,c in zip(means[:,0:2],covariances[:,0:2, 0:2]):
	multi_normal = multivariate_normal(mean=m,cov=c)
	# we create a (mesh)grid or array containing all combinations of all
	# values for the two first features
	x,y = np.meshgrid(np.sort(X[:,0]),np.sort(X[:,1]))
	XY = np.array([x.flatten(),y.flatten()]).T
	# here we use the grid to calculate all probailities for a normal distribution
	# for all combinations and the make elipses for certain level (here: default values)
	ax0.contour(np.sort(X[:,0]),
				np.sort(X[:,1]),
				multi_normal.pdf(XY).reshape(len(X),len(X)),
				colors=colour[i],
				alpha=0.3)
	ax0.scatter(m[0],m[1],c=colour[i],zorder=10,s=100)
	ax0.annotate(xy= (m[0]+.05 ,m[1]+.05), s='cluster {}'.format(i), color=colour[i], fontsize=24)
	i+=1

ax0.legend(legend)

if not os.path.isdir('result'):
	os.mkdir('result')
filename = os.path.join('result',
						'{}_{}_{}.png'.format('EM_sklearn', samples.feature_names[:1][0], samples.feature_names[1:2][0]).replace(' ', '_'))
print('File saved to {}'.format(filename))
plt.savefig(filename)
plt.show()

