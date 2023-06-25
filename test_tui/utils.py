from __future__ import annotations
from rich import console
import collections
import collections.abc
import typing as ty
from collections import UserList


T = ty.TypeVar("T")

class ProxyMutableSequence(collections.abc.MutableSequence[T]):
    def __init__(self, data: collections.abc.MutableSequence) -> None:
        self._type = type(data)
        self.data = data

    def __repr__(self):
        return repr(self.data)

    def __rich__(self):
        return console.Group(*self.data)

    def __contains__(self, item: T):
        return item in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i: int):
        if isinstance(i, slice):
            return self.__class__(self.data[i])
        else:
            return self.data[i]

    def __setitem__(self, i, item):
        self.data[i] = item

    def __delitem__(self, i):
        del self.data[i]

    def __mul__(self, n):
        return self.__class__(self.data * n)

    __rmul__ = __mul__

    def __imul__(self, n):
        self.data *= n
        return self

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["data"] = self.__dict__["data"][:]
        return inst

    def append(self, item):
        self.data.append(item)

    def insert(self, i, item):
        self.data.insert(i, item)

    def pop(self, i=-1):
        return self.data.pop(i)

    def remove(self, item):
        self.data.remove(item)

    def clear(self):
        self.data.clear()

    def copy(self):
        return self.__class__(self)

    def count(self, item):
        return self.data.count(item)

    def index(self, item, *args):
        return self.data.index(item, *args)

    def reverse(self):
        self.data.reverse()

    def extend(self, other):
        if isinstance(other, UserList):
            self.data.extend(other.data)
        else:
            self.data.extend(other)
