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
		
		self.favorites = ["Choose a favorite"]
		if len(self.favorites) < 2:
			if os.path.exists("save.p"):
				with open("save.p", "rb") as f:
					self.favorites = pickle.load(f)

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
		for i in range(len(self.favorites)):
			self.comboBox.addItem(self.favorites[i])

		button_layout.addWidget(self.comboBox)
		button_layout.addWidget(self.le)
		button_layout.addWidget(self.btn)

		self.setLayout(button_layout)

		self.setWindowTitle("Livestreamer GUI")

	def open_stream(self):
		stream = self.le.text()
		favorite_stream = self.comboBox.currentText()
		print(favorite_stream)
		s_quality = (self.quality_button_group.checkedButton().text()).lower()
		if not stream:
			self.close()
			os.system("livestreamer twitch.tv/{0} {1}".format(favorite_stream, s_quality))
		else:
			temp = [stream]
			if not stream in self.favorites:
				temp += self.favorites
				self.favorites = temp
				self.favorites[0], self.favorites[1] = self.favorites[1], self.favorites[0]
			if len(self.favorites) > 5:
				self.favorites.pop()
			with open("save.p", "wb") as f:
				pickle.dump(self.favorites, f)
			self.close()
			os.system("livestreamer twitch.tv/{0} {1}".format(stream, s_quality))	

if __name__ == '__main__':
	 
	app = QApplication(sys.argv)
	lsgui = LivestreamerGUI()
	lsgui.show()
	sys.exit(app.exec_())
