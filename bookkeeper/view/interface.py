import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
import inspect


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class MainWindow(QtWidgets.QWidget):
    def __init__(self, dataExpense, dataCategory, dataBudget):
        super().__init__()

        self.text1 = QtWidgets.QLabel('Последние расходы')
        self.table1 = QtWidgets.QTableView()
        self.text2 = QtWidgets.QLabel('Бюджет')
        self.table2 = QtWidgets.QTableView()
        self.text3 = QtWidgets.QLabel('Сумма')
        self.line = QtWidgets.QLineEdit()
        self.text4 = QtWidgets.QLabel('Категория')
        self.list = QtWidgets.QComboBox()
        self.button1 = QtWidgets.QPushButton('Редактировать', self)
        self.button2 = QtWidgets.QPushButton('Добавить', self)
        data = [
            [4, 9, 2],
            [1, 0, 0],
            [3, 5, 0],
            [3, 3, 2],
            [7, 8, 9],
        ]

        self.model1 = TableModel(dataExpense)
        self.table1.setModel(self.model1)
        self.model2 = TableModel(data)
        self.table2.setModel(self.model2)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text1)
        self.layout.addWidget(self.table1)
        self.layout.addWidget(self.text2)
        self.layout.addWidget(self.table2)
        self.layoutHorizon1 = QtWidgets.QHBoxLayout()
        self.layoutHorizon1.addWidget(self.text3)
        self.layoutHorizon1.addWidget(self.line)
        self.layout.addLayout(self.layoutHorizon1)
        self.layoutHorizon2 = QtWidgets.QHBoxLayout()
        self.layoutHorizon2.addWidget(self.text4)
        self.layoutHorizon2.addWidget(self.list)
        self.layoutHorizon2.addWidget(self.button1)
        self.layout.addLayout(self.layoutHorizon2)
        self.layoutHorizon3 = QtWidgets.QHBoxLayout()
        self.layoutHorizon3.addWidget(self.button2)
        self.layout.addLayout(self.layoutHorizon3)


app = QtWidgets.QApplication(sys.argv)
rep = SqliteRepository('test.sqlite', Expense)
data = []
rows = rep.get_all()
for obj in rows:
    data.append([obj.amount, obj.category, obj.expense_date, obj.comment])
print(data)
window = MainWindow(data, 1, 1)
window.setWindowTitle('The Bookkeeper App')
window.show()
window.resize(600, 600)
app.exec_()
