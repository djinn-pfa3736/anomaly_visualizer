import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QTableView, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QAction, QFileDialog, QDialog, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

import pandas as pd
import numpy as np

import pdb

class MainControl(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.input_file_label = QLabel('Input CSV File Name: ')

        self.file_name = QLineEdit()
        # self.setCentralWidget(self.file_name)

        self.choose_button = QPushButton("Choose", self)
        self.load_button = QPushButton("Load", self)

        self.choose_button.clicked.connect(self.choose_file)
        self.load_button.clicked.connect(self.load_file)

        """
        box = QHBoxLayout()
        self.setLayout(box)

        box.addWidget(self.input_file_label)
        box.addWidget(self.file_name)
        box.addWidget(self.choose_button)
        box.addWidget(self.load_button)
        """

        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(10)

        grid.addWidget(self.input_file_label, 1, 0)
        grid.addWidget(self.file_name, 1, 1, 1, 3)
        grid.addWidget(self.choose_button, 1, 4)
        grid.addWidget(self.load_button, 1, 5)

        # self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Anomary Visualizer')
        self.show()

    def choose_file(self):

        csv_name = QFileDialog.getOpenFileName(self, 'Open csv file', './')

        if csv_name[0]:
            self.file_name.setText(csv_name[0])

    def load_file(self):
        df = pd.read_csv(self.file_name.displayText())
        table_window = TableWindow()
        table_window.create_table(df)

        table_window.show()

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
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

class TableWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.subwindow = QDialog(parent)
        box = QHBoxLayout()
        self.subwindow.setLayout(box)

        self.table = QTableView(parent)
        box.addWidget(self.table)

    def create_table(self, df):
        self.model = TableModel(df)
        self.table.setModel(self.model)

    def show(self):
        self.subwindow.exec_()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainControl()
    sys.exit(app.exec_())
