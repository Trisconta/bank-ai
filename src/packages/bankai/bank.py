""" bank.py -- Textual bank movements

(c)2026  Henrique Moreira
"""

# pylint: disable=missing-function-docstring,raise-missing-from

from decimal import Decimal, ROUND_HALF_UP
from bankai.generichandler import DataSequence


class BankMov(DataSequence):
    """ Bank movements handler. """
    def __init__(self, fname, name="m"):
        super().__init__(name=name)
        self._ori_name = fname
        self._parse = self._reader(fname)

    def get_me(self):
        return self._parse

    def _reader(self, fname:str):
        """ Reads text input. """
        obj = BankTransactionParser(name=fname)
        with open(fname, "r", encoding="ascii") as fdin:
            text = fdin.read()
        obj.parse_text_lines(text)
        return obj


class BankTransactionParser(DataSequence):
    """ Parses semicolon-separated bank transaction lines into CamelCase dictionaries.
    Expected format:
		1. MovementDate
		2. ValueDate (DataValor)
		3. Description
		4. Debit
		5. Credit
		6. Balance
		7. Fix ('='), or provisional balance
		8. Category
    """
    def __init__(self, name="b"):
        """ Initializer, calls super-class. """
        super().__init__(name=name)
        self._head = ""
        self._items = {}

    def header(self):
        """ Returns the relevant part of header. """
        return self._head[1:].strip() if self._head else ""

    def content(self):
        return self._data

    def indexed(self):
        return self._items

    def parse_text_lines(self, raw_text: str):
        """ Parse multiple lines separated by newline.
        Adds each parsed dictionary to self._data.
        """
        lines = [
            (idx, line)
            for idx, line in enumerate(raw_text.replace("\r", "").splitlines(), 1)
            if line.rstrip() and (idx <= 1 or line.strip()[0] !='#')
        ]
        self._data, self._head, self._items = [], "", {}
        if not lines:
            return []
        _, head = lines[0]
        if head[0] == "#":
            self._head = head
            cont = lines[1:]
        else:
            cont = lines
        for idx, line in cont:
            item = self.parse_line(line, idx)
            self.add(item)
            self._items[idx] = item
        return cont

    def parse_line(self, raw_line:str, idx:int=0) -> dict:
        """ Line string parsing. """
        parts = [
            p.strip() if p.strip() else None
            for p in raw_line.split(";")
        ]
        if len(parts) != 8:
            raise ValueError(
                f"Invalid record format: expected 8 fields, got {len(parts)}: {self.parts_list(parts)}"
            )
        parts = [None] + parts
        mov_date = parts[1]
        value_date = parts[2]
        description = parts[3]
        debit = float(parts[4]) if parts[4] else None
        credit = float(parts[5]) if parts[5] else None
        balance = float(parts[6])
        prov = parts[7]	# '=' or provisional
        if prov == "=":
            prov = balance
        else:
            try:
                prov = float(prov)
            except ValueError:
                raise ValueError(
                    f"Expected '=' or balance in field 7, got {prov}, idx={idx}, {parts[1:]}"
                )
        category = parts[8]
        dct = {
            "MovementDate": mov_date,
            "ValueDate": value_date,
            "Description": description,
            "Debit": debit,
            "Credit": credit,
            "Balance": balance,
            "Provisional": prov,
            "Category": category,
        }
        return dct


def to_dec(value):
    """ Returns Decimal from string. """
    if value is None:
        return None
    aval = Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return aval
