from dataclasses import dataclass


@dataclass(slots=True)
class Budget:

    period: str
    amount: int
    budget: int
    pk: int = 0
