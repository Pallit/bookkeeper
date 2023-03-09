from bookkeeper.repository.sqlite_repository import SqliteRepository
from dataclasses import dataclass

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


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)