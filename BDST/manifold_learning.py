	# import required packages
####################################################################################################
import matplotlib.pyplot as plt  # load ploting package
from sklearn.datasets import load_breast_cancer, load_iris  # load sample datasets
from sklearn.manifold import TSNE  # load scikit learn package
from sklearn.preprocessing import StandardScaler
import os


####################################################################################################
# load data (must be imported first...) and explore
####################################################################################################
samples = load_iris()
#samples = load_breast_cancer()

print('\nsamples.DESCR\n#################\n {}'.format(samples.DESCR))  # get description of the dataset
print('\nsamples.feature_names\n#################\n {}'.format(samples.feature_names))  # get feature names
print('\nsamples.data[:1]\n#################\n {}'.format(samples.data[:1]))  # get the first sample
print('\nsamples.target_names\n#################\n {}'.format(samples.target_names))  # get the target class values
print('\nsamples.target\n#################\n {}'.format(samples.target))  # get the target column

####################################################################################################
# preprocessing
####################################################################################################

scaler=StandardScaler() # instantiate StandardScaler into scaler
samples_X_scaled = scaler.fit_transform(samples.data) # get all information to perform the
# standardisation and apply it to the data
# alternative
# scaler.fit(samples.data) #  get all information to perform the standardisation
# samples_X_scaled =scaler.transform(samples.data) # transform the data

####################################################################################################
# modelling
####################################################################################################

tsne = TSNE(random_state=666)  # create tsne instance of TSNE with parameter (here: random seed)
samples_tsne = tsne.fit_transform(
	samples_X_scaled)  # transform the features and fits them in one step, can be done separate
print('\nsamples_tsne.shape\n#################\n(row, column) {}'.format(
	samples_tsne.shape))  # its an  array of the type (Zeile, Spalte)

####################################################################################################
# plot the result
####################################################################################################

fig = plt.figure()  # create figure instance (that's where you plot ...
plt.xlim(samples_tsne[:, 0].min() - 1, samples_tsne[:, 0].max() + 1)  # set the axis limits depending
plt.ylim(samples_tsne[:, 1].min() - 1, samples_tsne[:, 1].max() + 1)  # on the data gor current figure
# samples_tsne[:, 1] - READ: get all data of the second column... (count starts with 0!)

colours = ['blue', 'red', 'black']  # make it fancy
markers = ['+', '.', 'o']

for i in range(len(samples.target)):  # go through all samples
	plt.scatter(x=samples_tsne[i, 0],  # set the type of plot and link it to the data
				y=samples_tsne[i, 1],
				s=10, # change the size of the markers
				marker=markers[samples.target[i]],
				color=colours[samples.target[i]])  # color depending on the target class

plt.xlabel('t-SNE new feature 0')
plt.ylabel('t-SNE new feature 1')
plt.show()  # finally show the plot
filename = os.path.join('result',
						'manifold_learning.png')
print('File saved to {}'.format(filename))
plt.close()
