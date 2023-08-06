from collections import UserDict
from typing import Tuple, Iterable


class AttrDict(object):
    """
    A dictionary whose key can be accessed using "." notation
    """

    def __init__(self):
        super().__setattr__("d", {})

    def __getattr__(self, item: str):
        return super().__getattribute__("d")[item]

    def __setattr__(self, key: str, value):
        super().__getattribute__("d")[key] = value

    def __len__(self) -> int:
        return len(super().__getattribute__("d"))

    def __iter__(self):
        return iter(super().__getattribute__("d"))

    def items(self) -> Iterable[Tuple[str, any]]:
        yield from super().__getattribute__("d").items()
