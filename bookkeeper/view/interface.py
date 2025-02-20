"""
Модуль описывает интерфейс приложения
"""

import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
import bookkeeper.Presenter as Presenter


class CategoryRedactor(QtWidgets.QWidget):
    """
    Виджет редактирования списка категорий
    """
    def __init__(self, category_list, indeces):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)

        self.line = QtWidgets.QLineEdit()
        self.layout.addWidget(self.line)

        layout_horizon = QtWidgets.QHBoxLayout()

        self.button_add = QtWidgets.QPushButton('Добавить категорию', self)
        self.button_add.clicked.connect(self.add_category)
        layout_horizon.addWidget(self.button_add)

        self.button_delete = QtWidgets.QPushButton('Удалить категорию', self)
        self.button_delete.clicked.connect(self.delete_category)
        layout_horizon.addWidget(self.button_delete)

        self.layout.addLayout(layout_horizon)

        self.setLayout(self.layout)

        self.list = category_list

        self.indeces = indeces

    def add_category(self):
        """
        Добавление новой категории
        """
        if self.line.text() == '':
            return
        items = [self.list.itemText(i) for i in range(self.list.count())]
        if self.line.text() in items:
            data_category = Presenter.get_category_data()
            self.list.clear()
            self.list.addItems(data_category)
            self.line.clear()
            return
        index = Presenter.add_category(self.line.text())
        self.indeces.append(index)
        data_category = Presenter.get_category_data()
        self.list.clear()
        self.list.addItems(data_category)
        self.line.clear()

    def delete_category(self):
        """
        Удаление категории
        """
        if self.line.text() == '':
            return
        items = [self.list.itemText(i) for i in range(self.list.count())]
        ind = items.index(self.line.text()) if self.line.text() in items else -1
        if ind == -1:
            return
        Presenter.delete_category(self.indeces[ind])
        self.indeces.pop(ind)
        data_category = Presenter.get_category_data()
        self.list.clear()
        self.list.addItems(data_category)
        self.line.clear()


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, labels):
        super(TableModel, self).__init__()
        self._data = data
        self._labels = labels

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        if len(self._data) == 0:
            return 0
        return len(self._data[0])

    def headerData(self, section, orientation=QtCore.Qt.Horizontal,
                   role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._labels[section].format(section + 1)
        return super().headerData(section, orientation, role)


class CategoryList(QtWidgets.QWidget):
    """
    Виджет таблицы категорий
    """
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

        self.indeces = Presenter.get_category_indeces()
        self.redactor = CategoryRedactor(self.list, self.indeces)
        self.redactor.setWindowTitle('Category Redactor')
        self.redactor.resize(600, 100)

    def get_selected_data(self):
        """
        Возвращает выбранную категорию
        """
        if len(self.indeces) == 0:
            return 0
        return self.indeces[self.list.currentIndex()]

    def button_clicked(self):
        """
        Открывает окно виджет редактирования списка категорий
        """
        self.redactor.show()

    def get_list(self):
        """
        Возвращает список категорий
        """
        return self.list


class BudgetTable(QtWidgets.QWidget):
    """
    Виджет таблицы бюджета
    """
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
        """
        Возвращает таблицу бюджета
        """
        return self.table


class ExpenseTable(QtWidgets.QWidget):
    """
    Виджет расходов
    """
    def __init__(self):
        super().__init__()
        data_expense, labels_expense = Presenter.get_expense_data()
        data_budget, labels_budget = Presenter.get_budget_data()
        data_category = Presenter.get_category_data()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.layout.addWidget(QtWidgets.QLabel('Последние расходы'))

        self.table = QtWidgets.QTableView()
        self.table.setModel(TableModel(data_expense, labels_expense))
        self.layout.addWidget(self.table)

        self.budget_table = BudgetTable(data_budget, labels_budget)
        self.layout.addWidget(self.budget_table)

        layout_horizon = QtWidgets.QHBoxLayout()

        layout_horizon.addWidget(QtWidgets.QLabel('Сумма'))

        self.line = QtWidgets.QLineEdit()
        layout_horizon.addWidget(self.line)

        self.layout.addLayout(layout_horizon)

        self.category_list = CategoryList(data_category)
        self.layout.addWidget(self.category_list)

        self.button = QtWidgets.QPushButton('Добавить', self)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.button_clicked)

        self.button_reset = QtWidgets.QPushButton('Сбросить все данные', self)
        self.layout.addWidget(self.button_reset)
        self.button_reset.clicked.connect(self.reset)

        self.setLayout(self.layout)

    def button_clicked(self):
        """
        Добавляет расход
        """
        if self.line.text() == '':
            return
        if self.category_list.get_selected_data() == 0:
            return
        Presenter.add_expense(int(self.line.text()),
                              self.category_list.get_selected_data())
        data_expense, labels_expense = Presenter.get_expense_data()
        self.table.setModel(TableModel(data_expense, labels_expense))
        data_budget, labels_budget = Presenter.get_budget_data()
        self.budget_table.get_table().setModel(TableModel(data_budget, labels_budget))

    def reset(self):
        """
        Сбрасывает все данные
        """
        Presenter.clear_data()
        data_expense, labels_expense = Presenter.get_expense_data()
        self.table.setModel(TableModel(data_expense, labels_expense))
        data_budget, labels_budget = Presenter.get_budget_data()
        self.budget_table.get_table().setModel(TableModel(data_budget, labels_budget))
        self.category_list.get_list().clear()


class MainWindow(QtWidgets.QWidget):
    """
    Основное окно
    """
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.expense_table = ExpenseTable()
        self.layout.addWidget(self.expense_table)
        self.setLayout(self.layout)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.setWindowTitle('The Bookkeeper App')
window.show()
window.resize(600, 600)
app.exec()
