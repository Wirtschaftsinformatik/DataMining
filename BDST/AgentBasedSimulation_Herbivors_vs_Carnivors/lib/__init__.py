import pandas as pd
import os

class initialise:
	def __init__(self):
		import sys
		import os

		gettrace = getattr(sys, 'gettrace', None)
		global my_debuger

		if gettrace is None:
			print('No sys.gettrace')
		elif gettrace():
			my_debuger = True
			my_debuger = False
		else:
			my_debuger = False
