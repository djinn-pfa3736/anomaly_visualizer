import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pyper

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class MainWindow(QWidget):
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)

		self.filtered = None

		self.status = False

		self.init_ui()

	def init_ui(self):

		self.input_file_label = QLabel('Input CSV File Name: ')
		self.file_name = QLineEdit()
		self.choose_button = QPushButton("Choose Data CSV", self)
		self.load_button = QPushButton("Load", self)

		self.choose_button.clicked.connect(self.choose_file)
		self.load_button.clicked.connect(self.load_file)

		# self.filtered_window_label = QLabel('Load Filtered Wave from Window')
		# self.filtered_window_button = QPushButton('Load from Window')
		# self.filtered_window_button.clicked.connect(wave_load_window)

		self.filtered_file_label = QLabel('Load Filtered Weve from File: ')
		self.wave_file_name = QLineEdit()
		self.wave_choose_button = QPushButton("Choose Wave CSV", self)
		self.wave_load_button = QPushButton("Load from File", self)

		self.wave_choose_button.clicked.connect(self.wave_choose_file)
		self.wave_load_button.clicked.connect(self.wave_load_file)

		self.status_label = QLabel('Status: Anomaly Detection NOT READY...')
		self.execute_button = QPushButton('Detect Anomalies')
		self.execute_button.clicked.connect(self.detect_anomaly)

		grid = QGridLayout()
		self.setLayout(grid)
		grid.setSpacing(10)

		grid.addWidget(self.input_file_label, 0, 0)
		grid.addWidget(self.file_name, 0, 1, 1, 2)
		grid.addWidget(self.choose_button, 0, 3)
		grid.addWidget(self.load_button, 0, 4)

		# grid.addWidget(self.filtered_window_label1, 1, 0)
		# grid.addWidget(self.filtered_window_button, 1, 4)

		grid.addWidget(self.filtered_file_label, 1, 0)
		grid.addWidget(self.wave_file_name, 1, 1, 1, 2)
		grid.addWidget(self.wave_choose_button, 1, 3)
		grid.addWidget(self.wave_load_button, 1, 4)

		grid.addWidget(self.status_label, 2, 0)
		grid.addWidget(self.execute_button, 2, 4)

		self.setWindowTitle('Anomaly Visualizer')
		self.show()
	
	def detect_anomaly(self):

		if self.status:
			self.detection_window = DetectionWindow(self.filtered, self)
			self.detection_window.setWindowTitle('Anomaly Detection Window')
			self.detection_window.show()

	def choose_file(self):
		csv_name = QFileDialog.getOpenFileName(self, 'Open CSV File', './')
		if csv_name[0]:
			self.file_name.setText(csv_name[0])

	def wave_choose_file(self):
		csv_name = QFileDialog.getOpenFileName(self, 'Open Wave CSV File', './')
		if csv_name[0]:
			self.wave_file_name.setText(csv_name[0])


	def load_file(self):

		self.df = pd.read_csv(self.file_name.displayText())

		self.table_window = TableWindow(mode = 'data', parent = self)
		self.table_window.create_table(self.df)

		self.table_window.show()

	def wave_load_file(self):

		self.filtered = pd.read_csv(self.wave_file_name.displayText(), index_col = 0)

		self.wave_table_window = TableWindow(mode = 'wave', parent = self)
		self.wave_table_window.create_table(self.filtered)

		self.wave_table_window.show()
		self.status_label.setText('Anomaly Detection IS READY!!')
		self.status = True

	def wave_load_window(self):
		self.filtered = self.table_window.get_filtered_wave()

class DetectionWindow(QWidget):
	def __init__(self, filtered, parent = None):
		super(DetectionWindow, self).__init__()

		self.filtered = filtered
		self.parent = parent

		grid = QGridLayout()
		self.setLayout(grid)

		self.detection_start_days_label = QLabel("Detection Starting Days: ")
		self.detection_start_days = QLineEdit()		
		self.detection_end_days_label = QLabel("Detection Ending Days: ")
		self.detection_end_days = QLineEdit()

		self.detection_target_length_label = QLabel("Target Interval Length(Days): ")
		self.detection_target_length = QLineEdit()
		self.detection_searching_length_label = QLabel("Searching Interval Length(Days): ")
		self.detection_searching_length = QLineEdit()

		self.method_label = QLabel("Similarity Measure: ")
		self.method_combobox = QComboBox()
		self.method_combobox.addItems(['Correlation', 'Euclid', 'Absolute'])

		self.year_label = QLabel("Searching Interval Length(Years): ")
		self.year = QLineEdit()

		self.detect_button_same = QPushButton('Detect in Same Year')
		self.detect_button_same.clicked.connect(self.start_detection_same)

		self.detect_button_different = QPushButton('Detect in Different Year')
		self.detect_button_different.clicked.connect(self.start_detection_different)

		grid.addWidget(self.detection_start_days_label, 0, 0)
		grid.addWidget(self.detection_start_days, 0, 1)
		grid.addWidget(self.detection_end_days_label, 0, 2)
		grid.addWidget(self.detection_end_days, 0, 3)

		grid.addWidget(self.detection_target_length_label, 1, 0)
		grid.addWidget(self.detection_target_length, 1, 1)
		grid.addWidget(self.detection_searching_length_label, 1, 2)
		grid.addWidget(self.detection_searching_length, 1, 3)

		grid.addWidget(self.method_label, 2, 0)
		grid.addWidget(self.method_combobox, 2, 1)
		grid.addWidget(self.year_label, 2, 2)
		grid.addWidget(self.year, 2, 3)

		grid.addWidget(self.detect_button_same, 3, 2)
		grid.addWidget(self.detect_button_different, 3, 3)

	def start_detection_same(self):
		r = pyper.R(use_numpy='True', use_pandas='True')
		r.assign('filtered.wave', self.filtered.iloc[:,0])

		r.assign('start.days', int(self.detection_start_days.displayText()))
		r.assign('end.days', int(self.detection_end_days.displayText()))
		r.assign('interval.len', int(self.detection_target_length.displayText()))
		r.assign('searching.len', int(self.detection_searching_length.displayText()))

		tmp = self.method_combobox.currentText()
		if tmp == 'Correlation':
			method = 'cor'
		elif tmp == 'Euclid':
			method = 'euc'
		elif tmp == 'Absolute':
			method = 'abs'

		r.assign('method', method)

		r('source("./rscripts/CalcSimMedianVec.R")')
		print(r('sim.vec <- CalcSimMedianVec(filtered.wave[,1], start.days, end.days, interval.len, searching.len, method)'))

		self.sim_vec = r.get('sim.vec')		
		print(self.sim_vec)

		r('png("sim_hist.png")')
		r('hist(sim.vec, col="#FF000099", border="white")')
		r('dev.off()')
		print(r('ls()'))

		self.sim_plot_window = PlotWindow()
		self.sim_plot_window.plot_image("sim_hist.png")
		self.sim_plot_window.show()

	def start_detection_different(self):
		r = pyper.R(use_numpy='True', use_pandas='True')
		r.assign('filtered.wave', self.filtered)
		r.assign('start.days', int(self.detection_start_days.displayText()))
		r.assign('end.days', int(self.detection_end_days.displayText()))
		r.assign('interval.len', int(self.detection_target_length.displayText()))
		r.assign('searching.len', int(self.detection_searching_length.displayText()))
		r.assign('method', self.method_combobox.currentText())
		r.assign('year', int(self.year.displayText))

		tmp = self.method_combobox.currentText()
		if tmp == 'Correlation':
			method = 'cor'
		elif tmp == 'Euclid':
			method = 'euc'
		elif tmp == 'Absolute':
			method = 'abs'

		r('source("./rscripts/CalcSimMedianVecOverYears.R")')
		r('sim.vec <- CalcSimMedianVecOverYears(filtered.wave, start.days, end.days, year, interval.len, searching.len, method)')
		
		r('png("sim_hist.png")')
		r('hist(sim.vec)')
		r('dev.off()')

		print(r('ls()'))

		self.sim_vec = r.get('sim.vec')		

		self.sim_plot_window = PlotWindow()
		self.sim_plot_window.plot_image("sim_hist.png")
		self.sim_plot_window.show()

class TableWindow(QWidget):
	def __init__(self, mode, parent = None):

		# super(TableWindow, self).__init__(parent)
		super(TableWindow, self).__init__()

		self.parent = parent

		grid = QGridLayout()
		self.setLayout(grid)

		self.table_view = QTableView(parent)

		self.plot_label = QLabel("Column Number(Area Number): ")
		self.plot_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.plot_label.setAlignment(Qt.AlignCenter)

		self.column_number = QLineEdit()

		self.plot_button = QPushButton("Plot", self)
		self.plot_button.clicked.connect(self.plot_column)

		self.region_min_label = QLabel("Starting Days: ")
		self.region_min_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.region_min_label.setAlignment(Qt.AlignRight)

		self.region_min = QLineEdit()
		self.region_max_label = QLabel("Ending Days: ")
		self.region_max_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.region_max_label.setAlignment(Qt.AlignRight)
		self.region_max = QLineEdit()

		if mode == 'data':
			self.max_wavelen_label = QLabel('Cutoff Wave Length(Days): ')
			self.max_wavelen = QLineEdit()

			self.apply_button = QPushButton("Apply Highpass Filter", self)
			self.apply_button.clicked.connect(self.apply_bandpass)

			self.save_label = QLabel('Input File Name: ')
			self.save_file_name = QLineEdit()

			self.save_button = QPushButton("Save Filtered Wave", self)
			self.save_button.clicked.connect(self.save_wave)

		grid.addWidget(self.table_view, 0, 0, 5, 6)

		grid.addWidget(self.plot_label, 6, 0)
		grid.addWidget(self.column_number, 6, 1)

		grid.addWidget(self.region_min_label, 6, 2)
		grid.addWidget(self.region_min, 6, 3)

		grid.addWidget(self.region_max_label, 6, 4)
		grid.addWidget(self.region_max, 6, 5)

		grid.addWidget(self.plot_button, 7, 5)

		if mode == 'data':
			grid.addWidget(self.max_wavelen_label, 8, 0)
			grid.addWidget(self.max_wavelen, 8, 1)
			grid.addWidget(self.apply_button, 8, 5)

			grid.addWidget(self.save_label, 9, 0)
			grid.addWidget(self.save_file_name, 9, 1)
			grid.addWidget(self.save_button, 9, 5)

	def apply_bandpass(self):
		target_column = int(self.column_number.displayText())

		r = pyper.R(use_numpy='True', use_pandas='True')
		r.assign('df', self.df)
		r.assign('target.column', target_column)
		r.assign('max.wave.len', int(self.max_wavelen.displayText()))
		r('source("./rscripts/ApplyBandpassFilter.R")')
		r('library(signal)')
		r('filtered <- ApplyBandpassFilter(df[,target.column], 365, 365/max.wave.len, 365/2)')
		r('png("filtered_wave.png")')
		r('plot(filtered, type="l", xlab="", ylab="")')
		r('dev.off()')
		print(r('ls()'))
		self.filtered = r.get('filtered')

		self.filtered_plot_window = PlotWindow()
		self.filtered_plot_window.plot_image("filtered_wave.png")
		self.filtered_plot_window.show()

		# self.filtered = np.array(self.filtered)
		self.filtered = pd.DataFrame({"Values": self.filtered}, index=np.arange(len(self.filtered)))

		print(self.filtered)

		self.parent.filtered = self.filtered
		self.parent.status_label.setText('Anomaly Detection IS READY!!')
		self.parent.status = True

	def save_wave(self):
		file_name = self.save_file_name.displayText()
		if file_name == '':
			self.filtered.to_csv("filtered_wave.csv")
		else:
			self.filtered.to_csv(file_name)

	def get_filtered_wave(self):
		return self.filtered

	def create_table(self, df):
		self.model = TableModel(df)
		self.table_view.setModel(self.model)
		self.df = df

	def plot_column(self):
		column_number = int(self.column_number.displayText())
		region_min = int(self.region_min.displayText())
		region_max = int(self.region_max.displayText())
		# Not implemented...

		r = pyper.R(use_numpy='True', use_pandas='True')
		r.assign('df', self.df)
		r.assign('target.column', column_number)
		r.assign('reg.min', region_min)
		r.assign('reg.max', region_max)

		r('png("selected_column.png")')
		r('plot(df[reg.min:reg.max, target.column], xlab="", ylab="", type="l")')
		r('dev.off()')

		self.column_plot_window = PlotWindow()
		self.column_plot_window.plot_image("selected_column.png")
		self.column_plot_window.show()

class TableModel(QAbstractTableModel):

	def __init__(self, data):
		super(TableModel, self).__init__()
		self._data = data

	def data(self, index, role):
		if role == Qt.DisplayRole:
			value = self._data.iloc[index.row(), index.column()]
			return str(value)

	def rowCount(self, index):
		return self._data.shape[0]

	def columnCount(self, index):
		return self._data.shape[1]

	def headerData(self, section, orientation, role):
		if role == Qt.DisplayRole:
			if orientation == Qt.Horizontal:
				return str(self._data.columns[section])
			elif orientation == Qt.Vertical:
				return str(self._data.index[section])

class PlotWindow(QWidget):
	def __init__(self, parent = None):
		super(PlotWindow, self).__init__(parent)
		self.box = QHBoxLayout(parent)
		self.setLayout(self.box)

	def plot_image(self, file_path):

		image_label = QLabel(self)
		pixmap = QPixmap(file_path)
		image_label.setPixmap(pixmap)
		
		self.resize(pixmap.width(), pixmap.height())
		self.box.addWidget(image_label)

app = QApplication(sys.argv)
mainWin = MainWindow()
mainWin.show()
sys.exit(app.exec_())
