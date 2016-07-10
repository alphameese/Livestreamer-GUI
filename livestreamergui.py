import sys
import os
import pickle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class LivestreamerGUI(QWidget):

	def __init__(self):
		super().__init__()

		# Checks to see if recent stream file exists, if it doesn't initialize the list
		if os.path.exists("save.p"):
			with open("save.p", "rb") as f:
				self.recent_streams = pickle.load(f)
		else:
			self.recent_streams = ["Recently watched"]

		# Creates selection of radio buttons to choose stream quality
		quality = [QRadioButton("Source"), QRadioButton("High"), QRadioButton("Medium"), QRadioButton("Low"), QRadioButton("Mobile")]
		quality[0].setChecked(True)

		# Creates combo box to show recently watched streams
		self.comboBox = QComboBox()

		# Creates a single line edit box
		self.le = QLineEdit(self)
		self.le.setPlaceholderText("Stream name")
		
		# Creates a button to open the stream
		self.btn = QPushButton('Open Stream', self)
		self.btn.clicked.connect(self.open_stream)

		# Creates a group for the buttons
		self.quality_button_group = QButtonGroup()

		# Sets a vertical layout
		button_layout = QVBoxLayout()

		# Adds radio buttons to button group
		for i in range(len(quality)):
			button_layout.addWidget(quality[i])
			self.quality_button_group.addButton(quality[i], i)

		# Add recently watched streams from file
		for i in range(len(self.recent_streams)):
			self.comboBox.addItem(self.recent_streams[i])

		# Add remaining buttons to layout
		button_layout.addWidget(self.comboBox)
		button_layout.addWidget(self.le)
		button_layout.addWidget(self.btn)

		self.setLayout(button_layout)

		self.setWindowTitle("Livestreamer GUI")

	# Create popup box with error message
	def show_dialog(self):
		msg_box = QMessageBox()
		msg_box.setText("Stream name only.")
		msg_box.setWindowTitle("Error")
		ret = msg_box.exec_()

	# Called when button is pressed to open the stream
	def open_stream(self):
		stream_name = self.le.text()
		chosen_stream = self.comboBox.currentText()
		s_quality = self.quality_button_group.checkedButton().text().lower()

		# First check if a stream name is manually input
		if stream_name:
			if "twitch.tv" in stream_name:
				self.show_dialog()
				
			else:
				# Check if manual input is in the list of recent streams and remove it
				if stream_name in self.recent_streams:
					self.recent_streams.remove(stream_name)

				# Re-add to top of the list
				self.recent_streams.insert(1, stream_name)

				# If list is greater than 5 remove the last item
				if len(self.recent_streams) > 5:
					self.recent_streams.pop()

				# Update recent stream file
				with open("save.p", "wb") as f:
					pickle.dump(self.recent_streams, f)

				self.close()

				# Open livestreamer program
				os.system("livestreamer twitch.tv/{0} {1}".format(stream_name, s_quality))

		# If a recent stream isn't chosen and there is a recent stream in the list, play last played stream
		elif not self.comboBox.currentIndex() and len(self.recent_streams) > 1:
			self.close()

			# Run livestreamer program
			os.system("livestreamer twitch.tv/{0} {1}".format(self.recent_streams[1], s_quality))

		# Check if recent stream list exists and if it does play selected stream
		elif len(self.recent_streams) > 1:

			# Remove chosen stream and re-add to top of list
			self.recent_streams.remove(chosen_stream)
			self.recent_streams.insert(1, chosen_stream)

			# Update recent stream file
			with open("save.p", "wb") as f:
				pickle.dump(self.recent_streams, f)

			self.close()

			# Open livestreamer program
			os.system("livestreamer twitch.tv/{0} {1}".format(chosen_stream, s_quality))

		else:
			print("Invalid selection.")

if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	lsgui = LivestreamerGUI()
	lsgui.show()
	sys.exit(app.exec_())
