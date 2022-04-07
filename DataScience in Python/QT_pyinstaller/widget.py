# This Python file uses the following encoding: utf-8
import os
import random
import sys
from pathlib import Path

# Ensure using PyQt5 backend
import numpy as np
from PySide2 import QtGui
from PySide2.QtCore import QFile
from PySide2.QtCore import QTimer
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog
from matplotlib.backends.backend_qtagg import (FigureCanvasQTAgg as FigureCanvas,
                                               NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


# matplotlib.use('QT5Agg')


class my_widget(QWidget):

	def __init__(self, parent=None):
		# initialise QWidget
		QWidget.__init__(self, parent)
		# create a "drawing place" (canvas) from mathplotlib  Figure()!!!
		self.canvas = FigureCanvas(Figure())
		# define the layout in QT where the mathplotlib later should be plotted
		grid_layout = QVBoxLayout()
		# marry QT and mathplot
		grid_layout.addWidget(self.canvas)
		# add the navigation bar from mathplot to the QT
		grid_layout.addWidget(NavigationToolbar(self.canvas, self))
		# from here normal mathplot behaviour
		self.canvas.axes = self.canvas.figure.add_subplot(111)
		self.setLayout(grid_layout)


class Widget(QWidget):
	# inherit everything from Class QWidget
	def __init__(self):
		# make myself to top class and execute __init__ from QWidget
		super(Widget, self).__init__()
		# initialise specific form
		self.load_ui()

	def load_ui(self):
		# enable load of separate ui file
		loader = QUiLoader()
		# tell the form that I have a custom class
		loader.registerCustomWidget(my_widget)
		# specify the external form location
		ui_form = os.path.join('forms', 'my_window.ui')
		# get application path
		path = os.fspath(Path(__file__).resolve().parent / ui_form)
		# specify what the external form is and load
		ui_file = QFile(path)
		ui_file.open(QFile.ReadOnly)
		self.ui = loader.load(ui_file, self)

		ui_file.close()

		# define the slots and the resulting actions (method calls)
		self.ui.pushButton.clicked.connect(self.start_timer)
		self.ui.pushButton_2.clicked.connect(self.stop_timer)
		self.ui.pushButton_3.clicked.connect(self.exit_app)

		self.ui.pushButton_4.clicked.connect(self.getDirectoryName)
		self.ui.pushButton_5.clicked.connect(self.getFileName)

		# give the ui file some defaults
		self.initUI()

	def initUI(self):
		# self.setGeometry(300, 300, 250, 150)
		self.cwd = os.getcwd()
		self.setWindowTitle('MyTitle')
		file = os.path.join(self.cwd, 'forms', 'web.png')
		self.setWindowIcon(QtGui.QIcon(file))
		self.ui.label.setText("Initial")

	# self.show()

	def start_timer(self):
		# custom method
		self.timer = QTimer()
		self.timer.setInterval(100)
		self.timer.timeout.connect(self.update_plot)
		self.timer.start()
		self.ui.label.setText("On")

	def stop_timer(self):
		# custom method
		try:
			self.timer.stop()
			self.ui.label.setText("Off")
		except:
			pass

	def update_plot(self):
		# custom method
		fs = 500
		f = random.randint(1, 100)
		ts = 1 / fs
		var1 = int(self.ui.spinBox.value())
		length_of_signal = var1
		t = np.linspace(0, 1, length_of_signal)
		cosinus_signal = np.cos(2 * np.pi * f * t)
		sinus_signal = np.sin(2 * np.pi * f * t)
		# make sure my_widget is empty
		self.ui.my_widget.canvas.axes.clear()
		self.ui.my_widget.canvas.axes.plot(t, cosinus_signal)
		self.ui.my_widget.canvas.axes.plot(t, sinus_signal)
		self.ui.my_widget.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
		self.ui.my_widget.canvas.axes.set_title('Cosinus - Sinus Signals')
		self.ui.textBrowser.append('Random Frequence: {}'.format(str(f)))
		# the draw() method is inherited from  QWidget!
		self.ui.my_widget.canvas.draw()

	def getDirectoryName(self):
		''' Called when the user presses the Browse button
	   '''
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		dirName = QFileDialog.getExistingDirectory(None, caption="Please select directory")
		if dirName:
			self.ui.label_2.setText(dirName)
			self.ui.textBrowser.append('Variable containing directory is dirName: {}'.format(str(dirName)))

	def getFileName(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(None, "Please select file", "",
		                                          "All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			self.ui.label_3.setText(fileName)
			self.ui.textBrowser.append('Variable containing directory is fileName: {}'.format(str(fileName)))

	def exit_app(self):
		sys.exit(app.exec_())


if __name__ == "__main__":
	# Aufruf des Frames QApplication (Basic Appearance)
	app = QApplication([])
	# instantiation, initialise and Assign Class Widget (see above)
	widget = Widget()
	# call method show
	widget.show()
	# destroy all on exit
	sys.exit(app.exec_())
