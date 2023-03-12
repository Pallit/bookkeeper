import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Slot
from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
import inspect
import bookkeeper.Presenter as Presenter


class CategoryRedactor(QtWidgets.QWidget):
    def __init__(self, category_list):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)

        self.line = QtWidgets.QLineEdit()
        self.layout.addWidget(self.line)

        self.button = QtWidgets.QPushButton('Добавить категорию', self)
        self.button.clicked.connect(self.button_clicked)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

        self.list = category_list

    def button_clicked(self):
        print("debug")
        Presenter.add_category(self.line.text())
        data_category = Presenter.get_category_data()
        self.list.clear()
        self.list.addItems(data_category)


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, labels):
        super(TableModel, self).__init__()
        self._data = data
        self._labels = labels

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

    def headerData(self, section, orientation=QtCore.Qt.Horizontal, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._labels[section].format(section + 1)
        return super().headerData(section, orientation, role)


class CategoryList(QtWidgets.QWidget):
    def __init__(self, data_category):
        super().__init__()
        self.layout = QtWidgets.QHBoxLayout(self)

        self.text = QtWidgets.QLabel('Категория')
        self.layout.addWidget(self.text)

        self.list = QtWidgets.QComboBox()
        self.list.addItems(data_category)
        self.layout.addWidget(self.list)

        self.button = QtWidgets.QPushButton('Редактировать', self)
        self.button.clicked.connect(self.button_clicked)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

        self.redactor = CategoryRedactor(self.list)
        self.redactor.setWindowTitle('Category Redactor')
        self.redactor.resize(600, 100)

    def get_list_data(self):
        return [self.list.itemText(i) for i in range(self.list.count())]

    def get_selected_data(self):
        return self.list.currentIndex() + 1

    def button_clicked(self):
        self.redactor.show()


class BudgetTable(QtWidgets.QWidget):
    def __init__(self, data_budget, labels_budget):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)

        self.text = QtWidgets.QLabel('Бюджет')
        self.layout.addWidget(self.text)

        self.table = QtWidgets.QTableView()
        self.table.setModel(TableModel(data_budget, labels_budget))
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

    def get_table(self):
        return self.table


class ExpenseTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        data_expense, labels_expense = Presenter.get_expense_data()
        data_budget, labels_budget = Presenter.get_budget_data()
        data_category = Presenter.get_category_data()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.text = QtWidgets.QLabel('Последние расходы')
        self.layout.addWidget(self.text)

        self.table = QtWidgets.QTableView()
        self.table.setModel(TableModel(data_expense, labels_expense))
        self.layout.addWidget(self.table)

        self.budgetTable = BudgetTable(data_budget, labels_budget)
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
        self.button.clicked.connect(self.button_clicked)

        self.setLayout(self.layout)

    def button_clicked(self):
        Presenter.add_expense(int(self.line.text()), self.categoryList.get_selected_data())
        data_expense, labels_expense = Presenter.get_expense_data()
        self.table.setModel(TableModel(data_expense, labels_expense))
        data_budget, labels_budget = Presenter.get_budget_data()
        self.budgetTable.get_table().setModel(TableModel(data_budget, labels_budget))


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.expenseTable = ExpenseTable()
        self.layout.addWidget(self.expenseTable)
        self.setLayout(self.layout)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.setWindowTitle('The Bookkeeper App')
window.show()
window.resize(600, 600)
app.exec()
