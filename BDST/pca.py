# import required packages
####################################################################################################
import os
import warnings

import matplotlib.pyplot as plt  # load ploting package
import numpy as np  # always good for matrices
from sklearn.datasets import load_iris  # load sample datasets
from sklearn.decomposition import PCA  # load scikit learn package
from sklearn.preprocessing import StandardScaler  # to standardise (z-transform) the data

warnings.filterwarnings('ignore', category=UserWarning)

####################################################################################################
# load data (must be imported first...) and explore
####################################################################################################
samples = load_iris()
# samples = load_breast_cancer()

print('\nsamples.DESCR:\n {}'.format(samples.DESCR))  # get description of the dataset
print('\nsamples.feature_names:\n {}'.format(samples.feature_names))  # get feature names
print('\nsamples.data[:1]:\n {}'.format(samples.data[:1]))  # get the first sample
print('\nsamples.target_names:\n {}'.format(samples.target_names))  # get the target class values
print('\nsamples.target:\n {}'.format(samples.target))  # get the target column

####################################################################################################
# preprocessing
####################################################################################################

scaler = StandardScaler()  # instantiate StandardScaler into scaler
samples_X_scaled = scaler.fit_transform(samples.data)

####################################################################################################
# modelling
####################################################################################################

pca = PCA(random_state=666, n_components=2)  # create pca instance of PCA with parameter
# (here: random seed and number of new components)
samples_pca = pca.fit_transform(samples_X_scaled)  # transform the features and fits
# them in one step, can be done separate
print('\noriginal shape (row, column) {}'.format(
	samples.data.shape))  # its an  array of the type (Zeile, Spalte)
print('pca shape (row, column) {}'.format(
	samples_pca.shape))  # its an  array of the type (Zeile, Spalte)
print('\nPCA component composition for first feature\n{}'.format(pca.components_[:,0]))
print('\nFirst PCA component composition for all feature\n{}'.format(pca.components_[0, :]))
print('\nExplained variance: \n{}'.format(pca.explained_variance_))
print('\n Covariance: \n{}'.format(pca.get_covariance()))

####################################################################################################
# plot the result
####################################################################################################

fig = plt.figure()  # create figure instance (that's where you plot ...
plt.xlim(samples_pca[:, 0].min() - 1, samples_pca[:, 0].max() + 1)  # set the axis limits depending
plt.ylim(samples_pca[:, 1].min() - 1, samples_pca[:, 1].max() + 1)  # on the data gor current figure
# samples_tsne[:, 1] - READ: get all data of the second column... (count starts with 0!)

colours = ['blue', 'red', 'black', 'green']  # make it fancy
markers = ['+', '.', 'o', '*']


# for i in range(len(samples.target)):  # go through all samples
# 	plt.scatter(x=samples_pca[i, 0],  # set the type of plot and link it to the data
# 				y=samples_pca[i, 1],
# 				s=10,
# 				marker=markers[samples.target[i]],
# 				color=colours[samples.target[i]])  # color depending on the target class

for pos, i in enumerate(np.unique(samples.target)):
	x=samples_pca[np.where(samples.target == i, ),0]
	y=samples_pca[np.where(samples.target == i, ),1]
	plt.scatter(x=x,  # set the type of plot and link it to the data
				y=y,
				s=5,
				marker=markers[pos],
				color=colours[pos], # color depending on the target class
				label = samples.target_names[pos])

# plt.gca().set_aspect('equal') # make a square plot
plt.xlabel('PCA component 0')
plt.ylabel('PCA component 1')
plt.legend()
filename = os.path.join('result',
						'pca_{}.png'.format('scatter'))
print('File saved to {}'.format(filename))
plt.show()  # finally show the plot
plt.close()

####################################################################################################
# evaluate the result
####################################################################################################

fig_2 = plt.figure()
#plt.matshow(pca.components_, cmap='Reds', aspect='auto')
plt.matshow(pca.components_, cmap='Reds', aspect=0.1) # create heatmap (display array as heatmap)
plt.colorbar()
plt.yticks([0,1], ['1. Component','2. Component'], va='top')
plt.ylabel('Components')
plt.xticks(np.arange(len(samples.feature_names)),samples.feature_names, rotation = 60, ha='left', rotation_mode="anchor" )
plt.xlabel('Features', )
filename = os.path.join('result',
						'pca_{}.png'.format('heatmap'))
print('File saved to {}'.format(filename))
plt.show()
plt.close()