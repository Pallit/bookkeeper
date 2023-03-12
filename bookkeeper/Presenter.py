import bookkeeper.repository.sqlite_repository as sr
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
import sqlite3
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Slot
import sys


def get_budget_data():
    repository = sr.budget_factory()
    budget_data = []
    items = repository.get_all()
    for item in items:
        budget_data.append([item.period, item.amount, item.budget])
    return budget_data


def get_category_data():
    repository = sr.category_factory()
    category_data = []
    items = repository.get_all()
    for item in items:
        category_data.append(item.name)
    return category_data


def get_expense_data():
    repository = sr.expense_factory()
    expense_data = []
    items = repository.get_all()
    for item in items:
        expense_data.append([item.amount, item.category, item.expense_date, item.comment])
    return expense_data


def add_expense(amount: int, category: int, comment: str = ''):
    print(amount)
    repository = sr.expense_factory()
    expense = Expense(amount=amount, category=category, comment=comment)
    repository.add(expense)

