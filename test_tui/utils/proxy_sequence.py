import collections
import collections.abc
import typing as ty

_T = ty.TypeVar("_T")


class ProxyMutableSequence(collections.abc.MutableSequence[_T]):
    """Proxy object for a mutable sequence to support patching the mutating methods"""

    def __init__(self, data: collections.abc.MutableSequence[_T]) -> None:
        self.data = data

        self.append = data.append
        self.extend = data.extend
        self.clear = data.clear
        self.reverse = data.reverse
        self.pop = data.pop
        self.remove = data.remove

    def __getattr__(self, name: str):
        return getattr(self.data, name)

    def __getitem__(self, index: ty.Union[int, slice]) -> ty.Union[_T, collections.abc.MutableSequence[_T]]:
        return self.data.__getitem__(index)

    @ty.overload
    def __setitem__(self, index: int, value: _T) -> None:
        ...

    @ty.overload
    def __setitem__(self, index: slice, value: collections.abc.Iterable[_T]) -> None:
        ...

    def __setitem__(self, index: int | slice, value: _T | collections.abc.Iterable[_T]) -> None:
        return self.data.__setitem__(index, value)

    def __delitem__(self, index: ty.Union[int, slice]) -> None:
        return self.data.__delitem__(index)

    def __len__(self) -> int:
        return self.data.__len__()

    def insert(self, index: int, value: _T) -> None:
        return self.data.insert(index, value)


class ProxyDeque(ProxyMutableSequence[_T], collections.deque[_T]):
    """Proxy object for a deque to support patching out the mutating methods"""

    def __init__(self, data: collections.deque[_T]) -> None:
        super().__init__(data)

        self.appendleft = data.appendleft
        self.extendleft = data.extendleft
        self.popleft = data.popleft
        self.rotate = data.rotate
        self.clear = data.clear
