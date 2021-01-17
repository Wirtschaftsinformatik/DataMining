class base(object):
	def __init__(self):
		import pandas as pd
		import numpy as np
		import random
		import os
		import datetime

		# setup environment

		self.longitude = 100
		self.latitude = 100
		self.days = 100
		random.seed(1)

		self.dir_home = os.getcwd()

		# define save directory

		date_time = datetime.datetime.now().strftime('%Y%d%m_%H%M')
		if not os.path.isdir('results'):
			os.mkdir('results')
		if not os.path.isdir(os.path.join('results', date_time)):
			os.mkdir(os.path.join('results', date_time))
		self.dir_result = os.path.join('results', date_time)

		# define agent properties

		attributes = np.dtype([('id', int),
							   ('sex', str),
							   ('status', str),
							   ('born', int),
							   ('died', int),
							   ('pos_long', int),
							   ('pos_lat', int),
							   ('food_lvl', int),
							   ('siblings', int)])

		temp = np.empty(1, dtype=attributes)
		self.data_sample = pd.DataFrame(data=temp)
		self.data_sample.set_index('id', inplace=True)
		# self.sample.drop(0, axis=0)

		# attributes = ['id', 'sex','status','born','died','pos_long','lvl_food','siblings']
		# self.sample = pd.DataFrame(columns=attributes)
		# self.sample.set_index('id', inplace=True)

		attributes = np.dtype([('period', int),
							   ('count', str),
							   ('status', str),
							   ('type', str)])

		temp = np.empty(1, dtype=attributes)

		self.properties = pd.Series({'initial_no': 1000,
									 'action_range': 5,
									 'sex': (['male', 'female']),
									 'food_lvl': 3,
									 'siblings': ([0, 1, 2]),
									 'age': 5,
									 'type': 'na',
									 'stat_cause': (['hunted', 'deceased', 'starved'])
									 })

		self.data_stats_sample = pd.DataFrame(data=temp)

		self.data = pd.DataFrame()
		self.data_stats = pd.DataFrame()
		self.data_log = pd.DataFrame()

	def create(self, *, number=1, day=0):
		import itertools
		import numpy as np
		import pandas as pd
		import random

		longitude = self.longitude
		latitude = self.latitude

		position = list(itertools.product(np.arange(longitude), np.arange(latitude)))
		sex = self.properties['sex']
		food = self.properties['food_lvl']
		siblings = self.properties['siblings']
		temp = pd.DataFrame(self.data_sample)
		animals = pd.DataFrame()
		for i in range(0, number):
			# temp['id'] = i
			temp['sex'] = random.choice(sex)
			temp['status'] = 'live'
			temp['born'] = day
			temp['pos_long'] = int(random.choice(position)[0])
			temp['pos_lat'] = random.choice(position)[1]
			temp['food_lvl'] = food
			if temp['sex'][0] == 'female':
				temp['siblings'] = random.choice(siblings)
			animals = animals.append(temp, ignore_index=True)
		animals.reindex()
		self.data = self.data.append(animals, ignore_index=True)

	def update_stats(self, *, status: object = 'na', period: int = 0, number: int = -1):
		"""

		:param status:
		:param period:
		:param number:
		:return:
		"""

		import pandas as pd

		df = pd.DataFrame(self.data_stats_sample)
		df['count'] = number
		# df['count'] = len(object.data.index)
		df['period'] = period
		df['status'] = status
		df['type'] = self.properties.type

		self.data_stats = self.data_stats.append(df, ignore_index=True)

	def cleanup(self):
		pass

	def save_results(self, *, object: object, filename: str, period: int = None):
		"""

		:param object:
		:param filename:
		:return:
		"""

		import os
		import matplotlib.pyplot as plt

		if period is None:
			period = self.days

		try:
			filename = os.path.join(self.dir_result,
									'{!s}_day_{!s}'.format(filename, str(period).zfill(len(str(self.days)))))
			if object.__module__.__contains__('matplotlib.figure'):
				plt.savefig(filename, format='png')
			elif object.__module__.__contains__('pandas.core.frame'):
				if os.path.isfile(filename):
					object.to_csv(filename, sep=',', index_label='index', mode='a', header=False)
				else:
					object.to_csv(filename, sep=',', index_label='index', mode='a', header=True)
			else:
				print('No save method implemented for that object')
		except:
			pass
		finally:
			pass


class herbivores(base):
	def __init__(self) -> object:
		super().__init__()
		import pandas as pd

		self.properties['initial_no'] = 1000
		self.properties['type'] = 'herbivores'
		self.properties['death_cause'] = ['hunted', 'deceased']
		self.properties['age']=10
		self.properties['max_animal_no'] = 5000


class carnivores(base):
	def __init__(self) -> object:
		super().__init__()
		import pandas as pd

		self.properties['initial_no'] = 50
		#self.properties['siblings'] = ([1])
		self.properties['type'] = 'carnivores'
		self.properties['death_cause'] = ['deceased', 'starved']
		self.properties['max_feed_lvl'] = 10
		self.properties['min_feed_lvl_breeding'] = 6
		self.properties['feed_per_period'] = 2
		self.properties['age'] = 4
		self.properties['siblings']: ([0, 1])
