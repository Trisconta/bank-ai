""" generichandler.py -- Generic text data handler.

(c)2026  Henrique Moreira
"""

class DataSequence:
    """ Generic container for a sequence of parsed items.
    Child classes are expected to populate self._data with dictionaries.
    """
    def __init__(self, data=None, name="d"):
        self.name = name
        self._data = [] if data is None else data

    def add(self, item:dict):
        """Append a parsed dictionary to the internal sequence."""
        assert isinstance(item, dict), name
        self._data.append(item)

    def all(self):
        """Return the full list of parsed items."""
        return self._data

    def parts_list(self, parts):
        """ Returns the list of shown parts. """
        res = [
            f"{idx}/{len(parts)}: {self._soft_text(part)}"
            for idx, part in enumerate(parts, 1)
        ]
        return res

    def _soft_text(self, astr):
        if astr is None:
            return "null"
        return astr.replace("\n", "\\n")

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)
