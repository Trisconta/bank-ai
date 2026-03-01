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
    date_mov: str
    date_val: str
    val_diff: float
    balance: float
    description: str
    description_hash: str
    raw: Movement

    def __str__(self):
        """ Standard pretty print """
        return self._pretty_str()

    def _pretty_str(self):
        """ Standard pretty print """
        dat = f"{self.date_mov:>10} {self.date_val:>10}"
        astr = (
            f"[{self.an_id:06d}]  "
            f"{dat}  "
            f"{self.val_diff:>10.2f} "
            f"{self.balance:>12.2f} ; "
            f"{self.description}"
        )
        return astr

    def _pretty_str2(self):
        """ Alternative pretty print """
        dat = f"{self.date_mov:>11},{self.date_val:>11}"
        val = self.val_diff
        desc = self.description
        astr = f"[{self.an_id:>06}] {dat} {val:>10.2f} {self.balance:>12.2f} ; {desc}"
        return astr



def indexed_movements(movements, idx_stt=1001, date_fmt="%d-%m-%Y"):
    """ Index movements but sort by date! """
    def parse_date(d):
        return datetime.strptime(d, date_fmt)

    mov = index_movements(
        sorted(movements, key=lambda m: parse_date(m.mov_date)),
        idx_stt,
    )
    return mov


def index_movements(movements, idx_stt=1001):
    """ Indexes movements! """
    def clean_description(desc):
        return re.sub(r"[^A-Za-z0-9]", "", desc).upper()

    def hash_description(clean):
        return hashlib.md5(clean.encode()).hexdigest()

    indexed = []
    same_str = "-" * 10
    for idx, m in enumerate(movements, idx_stt):
        clean = clean_description(m.description)
        hsh = hash_description(clean)
        a_diff = 0.0 if m.credit is None else float(m.credit)
        a_diff -= 0.0 if m.debit is None else float(m.debit)
        m_idx = IndexedMovement(
            an_id=idx,
            date_mov=m.mov_date,
            date_val=same_str if m.mov_date == m.value_date else m.value_date,
            val_diff=a_diff,
            balance=m.balance,
            description=m.description,
            description_hash=hsh,
            raw=m,
        )
        print(":::", idx, m_idx)
        indexed.append(
            m_idx,
        )
    return indexed
