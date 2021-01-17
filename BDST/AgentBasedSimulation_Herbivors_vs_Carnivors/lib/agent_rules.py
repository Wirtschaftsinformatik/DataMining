class base:
	def __init__(self):
		pass

	def breed(*, breeders: object, day: int = 0):
		import pandas as pd
		import random
		import numpy as np

		# etwas zu rechenintensiv für einfache Fortpflanzung...
		# temp = pd.DataFrame(breeders.data.query('sex==\'female\''))
		# for breeder in temp:
		#	number=random.choice(breeders.properties.siblings)
		# 	breeders.create(number=number, day=day)

		# mit query methode

		if 'min_feed_lvl_breeding' in breeders.properties.index:
			query='sex== \'female\' and food_lvl >= {}'.format(breeders.properties.min_feed_lvl_breeding)
		else:
			query = 'sex== \'female\''

		df = pd.DataFrame(breeders.data.query(query))

		# alternativ mit filter
		# query = breeders.data.sex == 'female'
		# df = breeders.data[query]

		count = len(df.index)
		mean = np.mean(breeders.properties.siblings)
		number = int(mean * count)
		breeders.create(number=number, day=day)
		breeders.update_stats(period=day, status='breed', number=number)

	def feed(*, prey: object, predators: object, day: int):
		import pandas as pd

		print('Hunting Start....')

		pd.options.mode.chained_assignment = None

		counter_prey = 0
		counter_carnivores = 0

		for predator in predators.data.itertuples():
			longitude_range_min = max(predator.pos_long - predators.properties['action_range'], 0)
			longitude_range_max = min(predator.pos_long + predators.properties['action_range'], predators.longitude)
			latitude_range_min = max(predator.pos_lat - predators.properties['action_range'], 0)
			latitude_range_max = min(predator.pos_lat + predators.properties['action_range'], predators.latitude)

			query = '(pos_long >= {}) & (pos_long <= {}) & (pos_lat >= {}) & (pos_lat <= {})'.format(
				longitude_range_min, longitude_range_max, latitude_range_min, latitude_range_max)
			feed = int(predators.properties.max_feed_lvl - predator.food_lvl)
			df = prey.data.query(query).sort_values('born').head(feed)

			predators.data.at[predator.Index, 'food_lvl'] = int(
				max(0, predator.food_lvl + len(df.index) - predators.properties.feed_per_period))
			if predator.food_lvl == 0:
				predators.data.at[predator.Index, 'status'] = 'starved'
				predators.data.at[predator.Index, 'died'] = day
				counter_carnivores += 1
				predators.data_log = predators.data_log.append(predators.data.loc[predator.Index], ignore_index=True)
				predators.data = predators.data.drop(predator.Index)
			if not df.empty:
				df['status'] = 'hunted'
				df['died'] = day
				counter_prey += len(df.index)
				prey.data_log = prey.data_log.append(df, ignore_index=True)
				prey.data = prey.data.drop(df.index)

		predators.update_stats(period=day, status='starved', number=counter_carnivores)
		predators.update_stats(period=day, status=' avg food lvl', number='{:.3f}'.format(predators.data.food_lvl.mean()))
		prey.update_stats(period=day, status='hunted', number=counter_prey)
		prey.data.reindex()

	def relocate(*, animals: object):
		import numpy as np
		import pandas as pd
		import random

		print('Roaming Start....')

		temp = pd.DataFrame(animals.data)

		for items in temp.itertuples():
			pos_long_new = min(max(items.pos_long + random.choice(
				np.arange(- animals.properties['action_range'], animals.properties['action_range'] * 2, 1)), 0),
							   animals.longitude)
			pos_lat_new = min(max(items.pos_lat + random.choice(
				np.arange(- animals.properties['action_range'], animals.properties['action_range'] * 2, 1)), 0),
							  animals.latitude)
			animals.data.pos_long[items.Index] = pos_long_new
			animals.data.pos_lat[items.Index] = pos_lat_new

	# print('Roaming End....')

	def decease(*, animals: object, day: int):
		import numpy as np
		import pandas as pd
		import random
		from time import sleep

		print('Natural Decease Start....')

		if 'max_animal_no' in animals.properties.index:
			df = pd.DataFrame(animals.data).head(max(0, len(animals.data)-animals.properties.max_animal_no))
			if not df.empty:
				df['status'] = 'deceased'
				df['died'] = day
				number = len(df.index)
				animals.update_stats(period=day, status='deceased', number=number)
				animals.data_log = animals.data_log.append(df, ignore_index=True)
				animals.data = animals.data.drop(list(df.index))

		query = ('(born <= {}) '.format(day - animals.properties.age))
		df = animals.data.query(query)
		if not df.empty:
			df['status'] = 'deceased'
			df['died'] = day
			number = len(df.index)
			animals.update_stats(period=day, status='deceased', number=number)
			animals.data_log = animals.data_log.append(df, ignore_index=True)
			animals.data = animals.data.drop(list(df.index))

		number = len(animals.data.index)
		animals.update_stats(period=day, status='alive', number=number)


