"""
Модель бюджета
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Budget:
    """
    Бюджет.
    period - временной период
    amount - кол-во затраченных средств
    budget - выделенный бюджет
    pk - id записи в базе данных
    """
    period: str
    amount: int
    budget: int
    pk: int = 0
