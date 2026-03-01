""" bmovement.py -- Bank movement class

(c)2026  Henrique Moreira
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from bankai.bank import to_dec


@dataclass
class Movement:
    """ Bare: Movement class! """
    mov_date: str
    value_date: str
    description: str
    debit: Optional[Decimal]
    credit: Optional[Decimal]
    balance: Decimal
    provisional: Decimal
    category: str

    @staticmethod
    def from_dict(d: dict) -> "Movement":
        """ Converts a TxuMovement into this class dictionary. """
        res = Movement(
            mov_date=d["MovementDate"],
            value_date=d["ValueDate"],
            description=d["Description"],
            debit=to_decimal(d["Debit"]),
            credit=to_decimal(d["Credit"]),
            balance=to_decimal(d["Balance"]),
            provisional=to_decimal(d["Provisional"]),
            category=d["Category"],
        )
        return res


def to_decimal(value):
    """ Wrapper for bank.to_dec() """
    return to_dec(value)
