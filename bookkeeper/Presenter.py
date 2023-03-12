"""
Модуль Presenter описывает функциональность посредника
"""

import bookkeeper.repository.sqlite_repository as sr
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense


def get_category_by_pk(pk: int):
    """
    Возвращает категорию по pk
    """
    repository = sr.category_factory()
    category = repository.get(pk)
    return category


def get_budget_data():
    """
    Возвращает список значений строк таблицы Budget
    """
    repository = sr.budget_factory()
    budget_data = []
    items = repository.get_all()
    for item in items:
        budget_data.append([item.period, item.amount, item.budget])
    labels = ['', 'Сумма', 'Бюджет']
    return budget_data, labels


def get_category_data():
    """
    Возвращает список значений строк таблицы Category
    """
    repository = sr.category_factory()
    category_data = []
    items = repository.get_all()
    for item in items:
        category_data.append(item.name)
    return category_data


def get_expense_data():
    """
    Возвращает список значений строк таблицы Expense
    """
    repository = sr.expense_factory()
    expense_data = []
    items = repository.get_all()
    for item in items:
        expense_data.append(
            [item.amount, get_category_by_pk(item.category).name, item.expense_date,
             item.comment])
    labels = ['Сумма', 'Категория', 'Дата', 'Комментарии']
    return expense_data, labels


def add_expense(amount: int, category: int, comment: str = ''):
    """
    Добавляет расход в БД
    """
    repository_expense = sr.expense_factory()
    expense = Expense(amount=amount, category=category, comment=comment)
    repository_expense.add(expense)

    repository_budget = sr.budget_factory()
    for i in range(1, 4):
        current_budget = repository_budget.get(i)
        current_budget.amount += amount
        repository_budget.update(current_budget)


def add_category(name: str):
    """
    Добавляет категорию в БД
    """
    repository = sr.category_factory()
    return repository.add(Category(name=name))


def clear_data():
    """
    Удаляет все строки из таблиц Expense и Category, и обнуляет в таблице Budget столбец
    amount
    """
    repository = sr.expense_factory()
    repository.delete_all()
    repository = sr.category_factory()
    repository.delete_all()
    repository = sr.budget_factory()
    for i in range(1, 4):
        current_budget = repository.get(i)
        current_budget.amount = 0
        repository.update(current_budget)


def get_category_indeces():
    """
    Возвращает все pk в таблице Category
    """
    repository = sr.category_factory()
    category_data = []
    items = repository.get_all()
    for item in items:
        category_data.append(item.pk)
    return category_data


def delete_category(pk: int):
    """
    Удаляет категорию из БД по pk
    """
    repository = sr.category_factory()
    repository.delete(pk)
