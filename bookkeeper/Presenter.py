import bookkeeper.repository.sqlite_repository as sr
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
import sqlite3
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Slot
import sys
from inspect import get_annotations


def get_category_by_pk(pk: int):
    repository = sr.category_factory()
    category = repository.get(pk)
    return category


def get_budget_data():
    repository = sr.budget_factory()
    budget_data = []
    items = repository.get_all()
    for item in items:
        budget_data.append([item.period, item.amount, item.budget])
    labels = ['', 'Сумма', 'Бюджет']
    return budget_data, labels


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
        expense_data.append([item.amount, get_category_by_pk(item.category).name, item.expense_date, item.comment])
    labels = ['Сумма', 'Категория', 'Дата', 'Комментарии']
    return expense_data, labels


def add_expense(amount: int, category: int, comment: str = ''):
    print(amount)
    repository = sr.expense_factory()
    expense = Expense(amount=amount, category=category, comment=comment)
    repository.add(expense)

