import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pyper

import pandas as pd
import numpy as np

class MainWindow(QWidget):
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		self.init_ui()

	def init_ui(self):

		self.input_file_label = QLabel('Input CSV File Name: ')
		self.file_name = QLineEdit()
		self.choose_button = QPushButton("Choose", self)
		self.load_button = QPushButton("Load", self)

		self.choose_button.clicked.connect(self.choose_file)
		self.load_button.clicked.connect(self.load_file)

		grid = QGridLayout()
		self.setLayout(grid)
		grid.setSpacing(10)

		grid.addWidget(self.input_file_label, 0, 0)
		grid.addWidget(self.file_name, 0, 1, 1, 2)
		grid.addWidget(self.choose_button, 0, 3)
		grid.addWidget(self.load_button, 0, 4)

		self.setWindowTitle('Anomaly Visualizer')
		self.show()
	
	def choose_file(self):
		csv_name = QFileDialog.getOpenFileName(self, 'Open CSV File', './')
		if csv_name[0]:
			self.file_name.setText(csv_name[0])

	def load_file(self):

		self.df = pd.read_csv(self.file_name.displayText())

		self.table_window = TableWindow()
		self.table_window.create_table(self.df)

		self.table_window.show()

class TableWindow(QWidget):
	def __init__(self, parent = None):
		super(TableWindow, self).__init__(parent)
		grid = QGridLayout()
		self.setLayout(grid)

		self.table_view = QTableView(parent)

		self.plot_label = QLabel("Column Number to Plot: ")
		self.plot_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.plot_label.setAlignment(Qt.AlignCenter)

		self.column_number = QLineEdit()

		self.plot_button = QPushButton("Plot", self)
		self.plot_button.clicked.connect(self.plot_column)

		self.region_min_label = QLabel("Plot Region Min: ")
		self.region_min_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.region_min_label.setAlignment(Qt.AlignRight)

		self.region_min = QLineEdit()
		self.region_max_label = QLabel("Plot Region Max: ")
		self.region_max_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.region_max_label.setAlignment(Qt.AlignRight)
		self.region_max = QLineEdit()

		self.max_wavelen_label = QLabel('Maximum Wave Length(Days): ')
		self.max_wavelen = QLineEdit()

		self.apply_button = QPushButton("Apply Highpass Filter", self)
		self.apply_button.clicked.connect(self.apply_bandpass)

		grid.addWidget(self.table_view, 0, 0, 5, 6)

		grid.addWidget(self.plot_label, 6, 0)
		grid.addWidget(self.column_number, 6, 1)

		grid.addWidget(self.region_min_label, 6, 2)
		grid.addWidget(self.region_min, 6, 3)

		grid.addWidget(self.region_max_label, 6, 4)
		grid.addWidget(self.region_max, 6, 5)

		grid.addWidget(self.plot_button, 7, 5)

		grid.addWidget(self.max_wavelen_label, 8, 0)
		grid.addWidget(self.max_wavelen, 8, 1)
		grid.addWidget(self.apply_button, 8, 5)

	def apply_bandpass(self):
		target_column = int(self.column_number.displayText())

		r = pyper.R(use_numpy='True', use_pandas='True')
		r.assign('df', self.df)
		r.assign('target.column', target_column)
		r.assign('max.wave.len', int(self.max_wavelen.displayText()))
		r('source("./rscripts/ApplyBandpassFilter.R")')
		print(r('filtered <- ApplyBandpassFilter(df[,target.column], 365, 365/max.wave.len, 365/2)'))
		r('png("filtered_wave.png")')
		print(r('plot(filtered, type="l", xlab="", ylab="")'))
		r('dev.off()')
		self.filtered_plot_window = PlotWindow()
		self.filtered_plot_window.plot_image("filtered_wave.png")
		self.filtered_plot_window.show()

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
