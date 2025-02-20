from bookkeeper.repository.sqlite_repository import SqliteRepository, category_factory, \
    budget_factory, expense_factory
from dataclasses import dataclass
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense

import pytest
import sqlite3


@dataclass(slots=True, eq=True)
class Custom:
    value: int = 0
    pk: int = 0


@pytest.fixture
def custom_class():
    return Custom


@pytest.fixture
def repo():
    with sqlite3.connect('test.sqlite') as con:
        cur = con.cursor()
        cur.execute('DROP TABLE IF EXISTS custom')
        cur.execute('CREATE TABLE custom (pk INTEGER, value INTEGER, PRIMARY KEY (pk))')
    con.close()
    return SqliteRepository('test.sqlite', Custom)


def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None


def test_delete_all(repo, custom_class):
    obj = custom_class()
    obj2 = custom_class()
    repo.add(obj)
    repo.add(obj2)
    repo.delete_all()
    assert repo.get(1) is None
    assert repo.get(2) is None


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_delete_unexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(1)


def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects


def test_budget():
    repo = budget_factory()
    budget = Budget('День', 0, 1000, 1)
    assert repo.get(1) == budget


def test_category():
    repo = category_factory()
    category = Category('Яблоко', 1)
    pk = repo.add(category)
    assert repo.get(pk) == category


def test_expense():
    repo = expense_factory()
    expense = Expense(amount=1, category=1, comment=' ')
    pk = repo.add(expense)
    print(expense.expense_date)
    assert repo.get(pk).amount == expense.amount
    assert repo.get(pk).category == expense.category
    assert repo.get(pk).comment == expense.comment
    assert repo.get(pk).expense_date == str(expense.expense_date)
    assert repo.get(pk).added_date == str(expense.added_date)
