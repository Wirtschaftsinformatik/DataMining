version = "0.0.2"

import sys


class main(QtWidgets.QDialog):
	def __init__(self, parent=None):
		global HOME
		HOME = os.getcwd()
		super().__init__(parent)
		self.ui = uic.loadUi("main.ui", self)

		# GUI initialisieren
		pass
		#self.ui.progressBar1.setValue(0)
		#self.ui.Version.setText(str(version))

		# Slots einrichten
		pass
		#self.ui.pushButtonReadFile.clicked.connect(self.ReadFile)

	def button_clicked_begin(self):
		#self.ui.pushButtonXing_Start.setEnabled(False)
		pass

	def button_clicked_end(self):
		#self.ui.pushButtonXing_Start.setEnabled(True)
		pass

	def Exit(self):
		self.close()


app = QtWidgets.QApplication(sys.argv)
dialog=main()
dialog.show()
sys.exit(app.exec_())