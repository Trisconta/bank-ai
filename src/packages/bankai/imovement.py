""" imovement.py -- Indexed movement class/ function(s)

(c)2026  Henrique Moreira
"""

import re
import hashlib
from datetime import datetime
from dataclasses import dataclass
from .bmovement import Movement


@dataclass
class IndexedMovement:
    """ Bare: Indexed Bank Movement """
    an_id: int
    date: str
    balance: float
    description: str
    description_hash: str
    raw: Movement


def index_movements(movements, idx_stt=1001):
    """ Indexes movements! """
    def parse_date(d):
        return datetime.strptime(d, "%d-%m-%Y")

    def clean_description(desc):
        return re.sub(r"[^A-Za-z0-9]", "", desc).upper()

    def hash_description(clean):
        return hashlib.md5(clean.encode()).hexdigest()

    # Sort by MovementDate
    sorted_movs = sorted(
       movements, key=lambda m: parse_date(m.mov_date)
    )
    indexed = []
    for idx, m in enumerate(sorted_movs, idx_stt):
        clean = clean_description(m.description)
        hsh = hash_description(clean)
        indexed.append(
            IndexedMovement(
                an_id=idx,
                date=m.mov_date,
                balance=m.balance,
                description=m.description,
                description_hash=hsh,
                raw=m,
            )
        )
    return indexed
