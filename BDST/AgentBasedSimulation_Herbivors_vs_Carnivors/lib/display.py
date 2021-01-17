class base:
	def __init__(self, *, herbivores: object, carnivores: object, environment: object):
		import matplotlib.pyplot as plt
		import os
		import io
		import datetime

		self.colormap = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']

		# setup map
		# dont stop after display
		plt.ion()

		fig = plt.figure()
		ax_h = plt.subplot2grid((3, 2), (2, 0), colspan=1, rowspan=1)
		ax_h.set_autoscale_on(True)
		ax_h.set_title(label='Herbivores')
		ax_h.axis('off')

		ax_c = plt.subplot2grid((3, 2), (2, 1), colspan=1, rowspan=1)  # , adjustable='box', aspect='equal')
		ax_c.set_autoscale_on(True)
		ax_c.axis('off')
		ax_c.set_title(label='Carnivores')

		ax_ch = plt.subplot2grid((3, 2), (0, 0), colspan=2, rowspan=2, adjustable='box', aspect='equal')
		ax_ch.set_autoscale_on(False)
		ax_ch.set_ylim(0, environment.latitude)
		ax_ch.set_xlim(0, environment.longitude)
		ax_ch.set_title(label='Map: Herbivores & Carnivores')
		ax_ch.grid()
		ax_ch.tick_params(
			axis='both',
			which='both',
			bottom=False,
			left=False,
			labelbottom=False,
			labelleft=False
		)

		self.ax_ch_h_res = ax_ch.scatter(herbivores.data.pos_long, herbivores.data.pos_lat, c='green',
										 marker='s',
										 alpha=.5)
		self.ax_ch_c_res = ax_ch.scatter(carnivores.data.pos_long, carnivores.data.pos_lat, c='red', marker='s',
										 alpha=.5)

		fig.suptitle('Period: 0')
		fig.tight_layout()
		fig.show()

		self.fig = fig
		self.ax_h = ax_h
		self.ax_h_save = ax_h
		self.ax_c = ax_c
		self.ax_c_save = ax_c
		self.ax_ch = ax_ch

		# setup stats

		plt.ion()
		fig_stat = plt.figure()
		ax_cart_c = plt.subplot2grid((4, 2), (2, 0), colspan=2, rowspan=2, adjustable='box')
		ax_cart_c.set_autoscale_on('y')
		ax_cart_c.set_xlim(0, environment.days)
		ax_cart_c.set_title(label='Carnivores')
		ax_cart_c.grid()
		ax_cart_c.tick_params(
			axis='both',
			which='both',
			bottom=True,
			left=True,
			labelbottom=True,
			labelleft=True
		)

		ax_cart_h = plt.subplot2grid((4, 2), (0, 0), colspan=2, rowspan=2, adjustable='box')
		ax_cart_h.set_autoscale_on('y')
		ax_cart_h.set_xlim(0, environment.days)
		ax_cart_h.set_title(label='Herbivores')
		ax_cart_h.grid()
		ax_cart_h.tick_params(
			axis='both',
			which='both',
			bottom=True,
			left=True,
			labelbottom=True,
			labelleft=True
		)
		fig_stat.tight_layout()
		fig_stat.show()

		self.environment = environment
		self.fig_stat = fig_stat
		self.ax_cart_h = ax_cart_h
		self.ax_cart_c = ax_cart_c

	def displaymap(self, *, herbivores: object, carnivores: object, day: int, filters: int = None):
		'''
		Visualisation
		:param herbivores:
		:param carnivores:
		:param day:
		:param filters:
		:return: None
		'''
		import matplotlib.pyplot as plt
		import time

		if filters != None:
			for filter in filters:
				carnivores.filter = carnivores[carnivores.data[filter] == filters[filter]]
				herbivores.filter = herbivores[herbivores.data[filter] == filters[filter]]
		else:
			carnivores.filter = carnivores.data
			herbivores.filter = herbivores.data

		cell_text = []
		query = 'period == {}'.format(day)
		table = herbivores.data_stats.query(query)[['period', 'status', 'count']]
		for row in range(len(table)):
			cell_text.append(table.iloc[row])
		# self.ax_h.cla()
		self.ax_h = self.ax_h_save
		self.ax_h.table(cellText=cell_text, colLabels=['days', 'status', 'count'], loc='center')

		cell_text = []
		query = 'period == {}'.format(day)
		table = carnivores.data_stats.query(query)[['period', 'status', 'count']]
		for row in range(len(table)):
			cell_text.append(table.iloc[row])
		# self.ax_c.cla()
		self.ax_c = self.ax_c_save
		self.ax_c.table(cellText=cell_text, colLabels=['days', 'status', 'count'], loc='center')

		self.ax_ch_h_res.remove()
		self.ax_ch_h_res = self.ax_ch.scatter(herbivores.filter.pos_long, herbivores.filter.pos_lat, c='green',
											  marker='s',
											  alpha=.5)
		self.ax_ch_c_res.remove()
		self.ax_ch_c_res = self.ax_ch.scatter(carnivores.filter.pos_long, carnivores.filter.pos_lat, c='red',
											  marker='s',
											  alpha=1)

		self.fig.suptitle('Period: {!s}'.format(day))
		self.fig.tight_layout()
		self.fig.canvas.flush_events()

	# time.sleep(1)
	# filename = os.path.join(carnivores.dir_result,
	# 						'map_day_{!s}'.format(str(day).zfill(len(str(int(max(self.ax_ch_h_res.get_xlim())))))))
	# plt.pyplot.savefig(filename, format='png')

	def displaystats(self, *, herbivores: object, carnivores: object, day: int, filters: int = None):
		'''
		Displaying stats for plot
		:param herbivores:
		:param carnivores:
		:param day:
		:param filters:
		:return: None
		'''

		import matplotlib as plt
		import pandas as pd
		import os

		if not herbivores.data_stats.empty:
			causes = sorted(set(herbivores.data_stats.status) | set(herbivores.properties.death_cause))
			for i, cause in enumerate(causes):
				query = 'status == \'{!s}\''.format(cause)
				df = herbivores.data_stats.query(query)[['period', 'count']]
				x = df['period']
				y = df['count']
				self.ax_cart_h.plot(x, y, color=self.colormap[i])
			self.ax_cart_h.legend(causes, loc='best')

		if not carnivores.data_stats.empty:
			causes = sorted(set(carnivores.data_stats.status) | set(carnivores.properties.death_cause))
			causes.remove(' avg food lvl')
			for i, cause in enumerate(causes):
				query = 'status == \'{!s}\''.format(cause)
				df = carnivores.data_stats.query(query)[['period', 'count']]
				x = df['period']
				y = df['count']
				self.ax_cart_c.plot(x, y, color=self.colormap[i])
			self.ax_cart_c.legend(causes, loc='best')

		self.fig_stat.tight_layout()
		self.fig_stat.show()

		if day == self.environment.days:
			self.environment.save_results(filename='2_distr_stats_charts', object=self.fig_stat, period=day)
		self.environment.save_results(filename='2_distr_stats_maps', object=self.fig, period=day)

		if len(herbivores.data_log.index) > 0:
			self.environment.save_results(filename='3_log_herbivores', object=herbivores.data_log)
			herbivores.data_log = herbivores.data_log.truncate(after=-1)
		if len(carnivores.data_log.index) > 0:
			self.environment.save_results(filename='3_log_carnivores', object=carnivores.data_log)
			carnivores.data_log = carnivores.data_log.truncate(after=-1)
