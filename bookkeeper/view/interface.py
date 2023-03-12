import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Slot
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


class CategoryList(QtWidgets.QWidget):
    def __init__(self, data_budget):
        super().__init__()
        self.layout = QtWidgets.QHBoxLayout(self)

        self.text = QtWidgets.QLabel('Категория')
        self.layout.addWidget(self.text)

        self.list = QtWidgets.QComboBox()
        self.layout.addWidget(self.list)

        self.button = QtWidgets.QPushButton('Редактировать', self)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)


class BudgetTable(QtWidgets.QWidget):
    def __init__(self, data_budget):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)

        self.text = QtWidgets.QLabel('Бюджет')
        self.layout.addWidget(self.text)

        self.table = QtWidgets.QTableView()
        self.model = TableModel(data_budget)
        self.table.setModel(self.model)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)


class ExpenseTable(QtWidgets.QWidget):
    def __init__(self, data_budget, data_category, data_expense):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)

        self.text = QtWidgets.QLabel('Последние расходы')
        self.layout.addWidget(self.text)

        self.table = QtWidgets.QTableView()
        self.model = TableModel(data_expense)
        self.table.setModel(self.model)
        self.layout.addWidget(self.table)

        self.budgetTable = BudgetTable(data_budget)
        self.layout.addWidget(self.budgetTable)

        self.layoutHorizon1 = QtWidgets.QHBoxLayout()

        self.text2 = QtWidgets.QLabel('Сумма')
        self.layoutHorizon1.addWidget(self.text2)

        self.line = QtWidgets.QLineEdit()
        self.layoutHorizon1.addWidget(self.line)

        self.layout.addLayout(self.layoutHorizon1)

        self.categoryList = CategoryList(data_category)
        self.layout.addWidget(self.categoryList)

        self.button = QtWidgets.QPushButton('Добавить', self)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)


class MainWindow(QtWidgets.QWidget):
    def __init__(self, data_budget, data_category, data_expense):
        super().__init__()
        data = [
            [4, 9, 2],
            [1, 0, 0],
            [3, 5, 0],
            [3, 3, 2],
            [7, 8, 9],
        ]
        self.layout = QtWidgets.QVBoxLayout(self)
        self.expenseTable = ExpenseTable(data, 1, data_expense)
        self.layout.addWidget(self.expenseTable)
        self.setLayout(self.layout)



app = QtWidgets.QApplication(sys.argv)
rep = SqliteRepository('test.sqlite', Expense)
data = []
rows = rep.get_all()
for obj in rows:
    data.append([obj.amount, obj.category, obj.expense_date, obj.comment])
print(data)
window = MainWindow(1, 1, data)
window.setWindowTitle('The Bookkeeper App')
window.show()
window.resize(600, 600)
app.exec_()
