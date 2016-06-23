import sys
import os
import pickle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class LivestreamerGUI(QWidget):

	def __init__(self):
		super().__init__()

		quality = [QRadioButton("Source"), QRadioButton("High"), QRadioButton("Medium"), QRadioButton("Low"), QRadioButton("Mobile")]
		quality[0].setChecked(True)
		
		self.recent_streams = ["Recently watched"]
		if os.path.exists("save.p"):
			with open("save.p", "rb") as f:
				self.recent_streams = pickle.load(f)

		self.btn = QPushButton('Open Stream', self)
		self.btn.clicked.connect(self.open_stream)

		self.le = QLineEdit(self)
		self.le.setPlaceholderText("Stream name")

		button_layout = QVBoxLayout()

		self.quality_button_group = QButtonGroup()

		for i in range(len(quality)):
			button_layout.addWidget(quality[i])
			self.quality_button_group.addButton(quality[i], i)

		self.comboBox = QComboBox()
		for i in range(len(self.recent_streams)):
			self.comboBox.addItem(self.recent_streams[i])

		button_layout.addWidget(self.comboBox)
		button_layout.addWidget(self.le)
		button_layout.addWidget(self.btn)

		self.setLayout(button_layout)

		self.setWindowTitle("Livestreamer GUI")

	def open_stream(self):
		stream = self.le.text()
		recent_stream = self.comboBox.currentText()
		s_quality = self.quality_button_group.checkedButton().text().lower()
		if stream:
			temp = [stream]
			if stream in self.recent_streams:
				self.recent_streams.remove(stream)
			self.recent_streams.insert(1, stream)
			if len(self.recent_streams) > 5:
				self.recent_streams.pop()
			with open("save.p", "wb") as f:
				pickle.dump(self.recent_streams, f)
			self.close()
			os.system("livestreamer twitch.tv/{0} {1}".format(stream, s_quality))
		else:
			self.recent_streams.remove(recent_stream)
			self.recent_streams.insert(1, recent_stream)
			with open("save.p", "wb") as f:
				pickle.dump(self.recent_streams, f)
			self.close()
			os.system("livestreamer twitch.tv/{0} {1}".format(recent_stream, s_quality))

if __name__ == '__main__':
	 
	app = QApplication(sys.argv)
	lsgui = LivestreamerGUI()
	lsgui.show()
	sys.exit(app.exec_())
