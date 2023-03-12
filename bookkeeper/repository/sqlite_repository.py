"""
Модуль описывает репозиторий, работающий в sqlite
"""

import sqlite3

from typing import Any, Optional
from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense


class SqliteRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий в sqlite. Хранит данные в БД.
    """

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        self.type = cls

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        names = ', '.join(self.fields.keys())
        placeholders = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({placeholders})',
                values
            )
            obj.pk = cur.lastrowid if cur.lastrowid is not None else 0
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'SELECT * FROM {self.table_name} WHERE pk={pk}')
            row = cur.fetchall()
        con.close()
        obj: Optional[T]
        obj = self.type(*row[0][1:], pk) if len(row) != 0 else None
        return obj

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        objects = []
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'SELECT * FROM {self.table_name}')
            rows = cur.fetchall()
        con.close()
        for row in rows:
            objects.append(self.type(*row[1:], row[0]))
        return objects

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'SELECT * FROM {self.table_name} WHERE pk={pk}')
            rows = cur.fetchall()
            if len(rows) == 0:
                raise KeyError()
            cur.execute(f'DELETE FROM {self.table_name} WHERE pk={pk}')
        con.close()

    def delete_all(self) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'DELETE FROM {self.table_name} WHERE True')
        con.close()

    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        names = ' = ? , '.join(self.fields.keys()) + ' = ?'
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'UPDATE {self.table_name} SET {names} WHERE pk={obj.pk}',
                values
            )
        con.close()


def budget_factory():
    with sqlite3.connect('test.sqlite') as con:
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS budget (pk INTEGER, period TEXT, amount INTEGER, budget INTEGER, '
                    'PRIMARY KEY (pk))')
        cur.execute("INSERT INTO budget(pk, period, amount, budget) SELECT 1, 'День', 0, 1000 "
                    "WHERE NOT EXISTS(SELECT 1 FROM budget WHERE pk = 1)")
        cur.execute("INSERT INTO budget(pk, period, amount, budget) SELECT 2, 'Неделя', 0, 7000 "
                    "WHERE NOT EXISTS(SELECT 1 FROM budget WHERE pk = 2)")
        cur.execute("INSERT INTO budget(pk, period, amount, budget) SELECT 3, 'Месяц', 0, 30000 "
                    "WHERE NOT EXISTS(SELECT 1 FROM budget WHERE pk = 3)")
    con.close()
    return SqliteRepository('test.sqlite', Budget)


def category_factory():
    with sqlite3.connect('test.sqlite') as con:
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS category (pk INTEGER, name TEXT, parent INTEGER, PRIMARY KEY (pk))')
    con.close()
    return SqliteRepository('test.sqlite', Category)


def expense_factory():
    with sqlite3.connect('test.sqlite') as con:
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS expense (pk INTEGER, amount INTEGER, category INTEGER, expense_date '
                    'DATETIME, added_date DATETIME, PRIMARY KEY (pk))')
    con.close()
    return SqliteRepository('test.sqlite', Expense)
