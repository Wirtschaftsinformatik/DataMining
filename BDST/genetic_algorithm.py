import itertools
import math
import os
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

X_SIZE = 10
Y_SIZE = 10
NUMBER_OF_NODES = 20
NUMBER_OF_LINKS = 30  # not used (all nodes are linked to each other
POPULATION_SIZE = 10
NUMBER_OF_ITERATIONS = 3000
MUTATION_PROBABILITY = .5  # normed between 0 and 1


class environment:
	def __init__(self):
		# create nodes
		node_list = []
		# set random points
		random.seed(666)
		for node in range(NUMBER_OF_NODES):
			node_x = random.randrange(0, X_SIZE, 1)
			node_y = random.randrange(0, Y_SIZE, 1)
			node_list.append([node, node_x, node_y])

		self.node_list = node_list

		# make all links between all nodes
		link_list = list(itertools.combinations(node_list, 2))
		self.link_list = link_list

		# calc all distances between all nodes using pythagoras
		dist_matrix = np.zeros((NUMBER_OF_NODES, NUMBER_OF_NODES))
		for row in link_list:
			x_diff = abs(row[0][1] - row[1][1])
			y_diff = abs(abs(row[0][2] - row[1][2]))
			dist = math.sqrt((x_diff) ** 2 + (y_diff) ** 2)
			dist_matrix[row[0][0], row[1][0]] = dist
			dist_matrix[row[1][0], row[0][0]] = dist

		self.dist_matrix = dist_matrix

		self.sample_name = list(np.arange(1, int(NUMBER_OF_ITERATIONS + POPULATION_SIZE), 1))
		self.sample = pd.DataFrame(columns=['route', 'dist_total', 'ID', 'generation'])

		if not os.path.isdir('result'):
			os.mkdir('result')

	def get_dist_matrix(self):
		return self.dist_matrix

	def get_node_list(self):
		return self.node_list

	def get_link_list(self):
		return self.link_list

	def get_sample_name(self):
		name = self.sample_name.pop(0)
		return name

	def plot_all(self, samples=None, title=""):

		figure, axs = plt.subplots(1)
		#plt.ion()
		start_node = self.node_list[0]
		nodes = np.array(self.node_list)
		links = np.array(self.link_list)

		# for step in range(0, NUMBER_OF_ITERATIONS, 1):
		for step in [0, NUMBER_OF_ITERATIONS-1]:
			axs.cla()
			#axs.collections.remove()
			axs.set_xlim(-1, X_SIZE+1)
			axs.set_ylim(-1, Y_SIZE+1)
			axs.scatter(start_node[1], start_node[2], label='Start-End Node', color='black', zorder=2)
			axs.scatter(nodes[1:, 1], nodes[1:, 2], label='Node', zorder=1, color='orange')

			for link in links:
				x = list(link[:, 1])
				y = list(link[:, 2])
				axs.plot(x, y, color='green', zorder=0, linestyle=':', linewidth=.25)

			for i, txt in enumerate(nodes):
				if i == 0:
					axs.annotate('Start-End Node', (nodes[0, 1], nodes[0, 2]), zorder=2)
				else:
					axs.annotate('{}'.format(i), (nodes[i, 1], nodes[i, 2]), zorder=2)

			line_colour = 'red'
			line_strength = 1.5
			route = samples.iloc[step]['route']
			for i, leg in enumerate(route[:-1]):
				from_node = route[i]
				to_node = route[i + 1]
				x = [nodes[from_node][1], nodes[to_node][1]]
				y = [nodes[from_node][2], nodes[to_node][2]]
				axs.plot(x, y, color=line_colour, zorder=1, linestyle='-', linewidth=line_strength)
			figure.suptitle('Step {}'.format(step))


			filename=os.path.join('result', 'genetic_algorith_route_step_{}.png'.format(step))
			figure.savefig(filename)

			figure.show()
			# figure.canvas.draw()
			# figure.canvas.flush_events()

		figure2, axs2 = plt.subplots(1)
		axs2.set_xlim(0, len(samples))
		axs2.set_ylabel('km')
		axs2.set_ylim(0, math.ceil(samples['dist_total'].max())+10)
		x=np.arange(0, len(samples),1)
		y=samples['dist_total']
		axs2.plot(x, y)
		plt.title('Distances')
		filename=os.path.join('result', 'genetic_algorith_distances.png'.format(step))
		plt.savefig(filename)
		plt.show()

		# plt.legend(loc='best')
		#tab = axs[1].table(cellText=samples.values, colLabels=list(samples.columns), loc='center')
		#tab.set_fontsize(40)

class actions:
	def __init__(self, environment=None):
		self.environment = environment

	def initial_breed(self, environment=None):
		sample = pd.DataFrame(environment.sample)
		node_list = environment.get_node_list()
		tmp = list(np.arange(1, len(node_list), 1))
		route = random.sample(tmp, NUMBER_OF_NODES - 1)
		route.insert(0, 0)
		route.append(0)
		sample['route'] = [route]
		sample['ID'] = self.environment.get_sample_name()
		sample['generation'] = 0
		return sample

	def eval_fitness(self, sample=None):
		route = sample['route'][0]
		dist_total = 0
		for pos in range(0, len(route) - 1):
			from_node = route[pos]
			to_node = route[pos + 1]
			dist_total += self.environment.dist_matrix[from_node, to_node]
		return dist_total

	def crossover(self, samples=None, method='elite'):
		if method == 'elite':
			parent_route_1 = 1
			parent_route_2 = 2

		if method == 'tournament':
			parent_1=np.random.choice(samples.index, p=list((samples['dist_total'])/samples['dist_total'].sum()))
			parent_2=np.random.choice(samples.index, p=list((samples['dist_total'])/samples['dist_total'].sum()))

		parent_route_1 = samples.loc[parent_1]['route'][1:-1]
		parent_route_2 = samples.loc[parent_2]['route'][1:-1]

		# cut the dominant part of the route (without start and end point)
		start = 0
		end = len(parent_route_1)
		while end - start > round(len(parent_route_1) / 3, 0) or end - start < 2:
			cut_point_a = random.randrange(0, len(parent_route_1))
			cut_point_b = random.randrange(0, len(parent_route_1))
			start = min(cut_point_a, cut_point_b)
			end = max(cut_point_a, cut_point_b)

		dominant_route = parent_route_1[start:end]
		child_route = np.zeros(NUMBER_OF_NODES - 1).astype(int)
		for node in range(start, end):
			child_route[node] = int(parent_route_1[node])
		for pos in list(np.where(child_route == 0))[0]:
			try:
				node = parent_route_2.pop(0)
			except:
				print('{}'.format(len(samples)))
				print('{}'.format(len(samples)))
			while node in dominant_route and len(parent_route_2) > 0:
				node = parent_route_2.pop(0)
			child_route[pos] = int(node)
		child_route = child_route.tolist()
		child_route.insert(0, 0)
		child_route.append(0)
		sample = pd.DataFrame(columns=samples.columns)
		sample['route'] = [child_route]
		sample['ID'] = self.environment.get_sample_name()
		sample['generation'] = samples.loc[1]['generation'] + 1
		# print('sample breed')
		return sample

	def mutate(self, sample=None):
		probability = random.random()
		if probability <= MUTATION_PROBABILITY:
			route = sample['route'][0][1:-1]
			swap_pos_1 = random.choice(np.arange(len(route)))
			swap_pos_2 = swap_pos_1
			while swap_pos_2 == swap_pos_1:
				swap_pos_2 = random.choice(np.arange(len(route)))
			node_a = route[swap_pos_1]
			node_b = route[swap_pos_2]

			sample['route'][0][swap_pos_1+1] = node_b
			sample['route'][0][swap_pos_2+1] = node_a
			# print('sample mutated')
		return sample

	def live_and_let_die(self, samples):
		survivor = samples[:POPULATION_SIZE]
		# print('samples removed')
		return survivor

	def determine_rank(self, *, samples=None):
		samples['Rank'] = samples['dist_total'].rank(method='first').astype(int)
		samples = samples.set_index(['Rank']).sort_index()
		return samples


if __name__ == "__main__":
	# base setup
	myEnvironment = environment()
	mySamples = myEnvironment.sample
	bestRoute = myEnvironment.sample
	# bestRoute = myEnvironment.bestRoute
	bestRoute=mySamples
	myActions = actions(environment=myEnvironment)
	for i in range(0, POPULATION_SIZE):
		mySample = myActions.initial_breed(environment=myEnvironment)
		mySample['dist_total'] = myActions.eval_fitness(sample=mySample)
		mySamples = mySamples.append(mySample)
	mySamples = myActions.determine_rank(samples=mySamples)
	bestRoute = bestRoute.append(mySamples.iloc[0], ignore_index=True)


	# evolution
	for i in range(1, NUMBER_OF_ITERATIONS):
		title = 'generation {}'.format(i)
		mySample = myActions.crossover(samples=mySamples, method='tournament')
		mySample = myActions.mutate(sample=mySample)
		mySample['dist_total'] = myActions.eval_fitness(sample=mySample)
		mySamples = mySamples.append(mySample, sort=True)
		mySamples = myActions.determine_rank(samples=mySamples)
		if len(mySamples) % POPULATION_SIZE == 0:
			# at certain point of time let samples die to avoid inbreed....
			mySamples = myActions.live_and_let_die(mySamples)
		#print('i: {}    {}'.format(int(i), str(mySamples.iloc[0]['route'])))
		bestRoute = bestRoute.append(mySamples.iloc[0], ignore_index=True)

	myEnvironment.plot_all(samples=bestRoute)
	# print(bestRoute['route'])
