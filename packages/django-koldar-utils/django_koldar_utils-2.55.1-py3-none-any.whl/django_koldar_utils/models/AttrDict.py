from collections import UserDict
from typing import Tuple, Iterable


class AttrDict(object):
    """
    A dictionary whose key can be accessed using "." notation
    """

    def __init__(self):
        self.d = {}

    def __getattr__(self, item: str):
        return self.d[item]

    def __setattr__(self, key: str, value):
        self.d[key] = value

    def __len__(self) -> int:
        return len(self.d)

    def __iter__(self):
        return iter(self.d)

    def items(self) -> Iterable[Tuple[str, any]]:
        yield from self.d.items()
