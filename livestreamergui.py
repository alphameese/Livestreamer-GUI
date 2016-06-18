import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class LivestreamerGUI(QWidget):

	def __init__(self):
		super().__init__()

		quality = [QRadioButton("Mobile"), QRadioButton("Low"), QRadioButton("Medium"), QRadioButton("High"), QRadioButton("Source")]
		quality[0].setChecked(True)

		self.btn = QPushButton('Open Stream', self)
		self.btn.clicked.connect(self.open_stream)

		self.le = QLineEdit(self)
		self.le.setPlaceholderText("Stream name")

		button_layout = QVBoxLayout()

		self.quality_button_group = QButtonGroup()

		for i in range(len(quality)):
			button_layout.addWidget(quality[i])
			self.quality_button_group.addButton(quality[i], i)

		button_layout.addWidget(self.le)
		button_layout.addWidget(self.btn)

		self.setLayout(button_layout)

		self.setWindowTitle("Livestreamer GUI")

	def open_stream(self):
		stream = self.le.text()
		s_quality = (self.quality_button_group.checkedButton().text()).lower()
		self.close()
		os.system("livestreamer twitch.tv/{0} {1}".format(stream, s_quality))

if __name__ == '__main__':
	 
	app = QApplication(sys.argv)
	lsgui = LivestreamerGUI()
	lsgui.show()
	sys.exit(app.exec_())
