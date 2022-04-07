# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ci95poh/PycharmProjects/QT2/my_window.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Widget(object):
	def setupUi(self, Widget):
		Widget.setObjectName("Widget")
		Widget.resize(612, 645)
		self.gridLayoutWidget = QtWidgets.QWidget(Widget)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 531, 90))
		self.gridLayoutWidget.setObjectName("gridLayoutWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem, 2, 3, 1, 1)
		spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.gridLayout.addItem(spacerItem1, 5, 0, 1, 1)
		self.textEdit = QtWidgets.QTextEdit(self.gridLayoutWidget)
		self.textEdit.setObjectName("textEdit")
		self.gridLayout.addWidget(self.textEdit, 2, 2, 1, 1)
		spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)
		self.pushButton = PushButton(self.gridLayoutWidget)
		self.pushButton.setMaximumSize(QtCore.QSize(100, 100))
		self.pushButton.setObjectName("pushButton")
		self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
		spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.gridLayout.addItem(spacerItem3, 3, 0, 1, 1)
		self.verticalLayoutWidget = QtWidgets.QWidget(Widget)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 100, 531, 431))
		self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")
		self.my_widget = my_widget(self.verticalLayoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.my_widget.sizePolicy().hasHeightForWidth())
		self.my_widget.setSizePolicy(sizePolicy)
		self.my_widget.setMinimumSize(QtCore.QSize(100, 100))
		self.my_widget.setMaximumSize(QtCore.QSize(1000, 1000))
		self.my_widget.setObjectName("my_widget")
		self.verticalLayout.addWidget(self.my_widget)

		self.retranslateUi(Widget)
		QtCore.QMetaObject.connectSlotsByName(Widget)

	def retranslateUi(self, Widget):
		_translate = QtCore.QCoreApplication.translate
		Widget.setWindowTitle(_translate("Widget", "Widget"))
		self.pushButton.setText(_translate("Widget", "PushButton"))


from my_widget import my_widget
from pushbutton import PushButton
