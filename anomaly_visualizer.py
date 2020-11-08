#Codersarts python Assignment Help by top rated Expert
#If you need any help then contact to codersarts offcial website
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QTableView, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QAction, QFileDialog, QDialog, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

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
        grid.addWidget(self.file_name, 0, 1, 0, 2)
        grid.addWidget(self.choose_button, 0, 3)
        grid.addWidget(self.load_button, 0, 4)

        self.setWindowTitle('Anomary Visualizer')
        self.show()

    def choose_file(self):
        csv_name = QFileDialog.getOpenFileName(self, 'Open CSV File', './')
        if csv_name[0]:
            self.file_name.setText(csv_name[0])

    def load_file(self):

        df = pd.read_csv(self.file_name.displayText())

        self.table_window = TableWindow()
        self.table_window.create_table(df)

        self.table_window.show()

class TableWindow(QWidget):
    def __init__(self, parent = None):
        super(TableWindow, self).__init__(parent)
        grid = QGridLayout()
        self.setLayout(grid)

        self.table_view = QTableView(parent)

        self.plot_label = QLabel("Input Column Number to Plot")
        self.column_number = QLineEdit()
        self.plot_button = QPushButton("Plot", self)

        grid.addWidget(self.table_view, 0, 0, 5, 3)
        grid.addWidget(self.plot_label, 6, 0)
        grid.addWidget(self.column_number, 6, 1)
        grid.addWidget(self.plot_button, 6, 2)

    def create_table(self, df):
        self.model = TableModel(df)
        self.table_view.setModel(self.model)

class TableModel(QtCore.QAbstractTableModel):

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

app = QApplication(sys.argv)
mainWin =MainWindow()
mainWin.show()
sys.exit(app.exec_())
