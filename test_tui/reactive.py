from __future__ import annotations

import collections
import collections.abc
import functools
import typing as ty
import io
from textual import reactive
from textual._types import MessageTarget
import sys
from test_tui.utils.proxy_sequence import ProxyDeque, ProxyMutableSequence

if ty.TYPE_CHECKING:
    from textual.app import App
    from textual.widget import Widget

    Reactable = ty.Union[Widget, App]
    from textual._types import MessageTarget

MutableSequenceType = ty.TypeVar("MutableSequenceType", bound=collections.abc.MutableSequence)


class ReactiveStringIO(reactive.Reactive[str]):
    def __init__(
        self,
        *,
        layout: bool = False,
        repaint: bool = True,
    ) -> None:
        super()
        self.layout = layout
        self.repaint = repaint
        self.stream = io.StringIO()

    def __set_name__(self, owner: ty.Type[MessageTarget], name: str) -> None:

        if hasattr(owner, f"compute_{name}"):
            try:
                computes = getattr(owner, "__computes")
            except AttributeError:
                computes = []
                setattr(owner, "__computes", computes)
            computes.append(name)

        self.name = name
        self.internal_name = f"__{name}"
        setattr(owner, self.internal_name, self._default)

    def __get__(self, obj: Reactable, obj_type: type[object]) -> io.StringIO:
        sequence = getattr(obj, self.internal_name)
        self._patch_mutating_methods(sequence, obj)
        return sequence

    def __set__(self, obj: Reactable, value: io.StringIO) -> None:
        value = self._wrap_in_proxy(value)
        self._patch_mutating_methods(value, obj)
        return super().__set__(obj, value)


    def flush(self) -> None:
        ...
        return super().flush()

    @property
    def closed(self) -> bool: ...
    @property
    def line_buffering(self) -> bool: ...
    if sys.version_info >= (3, 7):
        @property
        def write_through(self) -> bool: ...
        def reconfigure(
            self,
            *,
            encoding: str | None = ...,
            errors: str | None = ...,
            newline: str | None = ...,
            line_buffering: bool | None = ...,
            write_through: bool | None = ...,
        ) -> None: ...
    # These are inherited from TextIOBase, but must exist in the stub to satisfy mypy.
    def __enter__(self) -> io.StringIO:

        return self.stream

    def __iter__(self) -> Iterator[str]: ...  # type: ignore[override]
    def __next__(self) -> str: ...  # type: ignore[override]
    def writelines(self, __lines: Iterable[str]) -> None: ...  # type: ignore[override]
    def readline(self, __size: int = ...) -> str: ...  # type: ignore[override]
    def readlines(self, __hint: int = ...) -> list[str]: ...  # type: ignore[override]
    def seek(self, __cookie: int, __whence: int = ...) -> int: ...

_MUTABLE_SEQUENCE_MUTATING_METHODS = (
    collections.abc.MutableSequence.append,
    collections.abc.MutableSequence.extend,
    collections.abc.MutableSequence.clear,
    collections.abc.MutableSequence.reverse,
    collections.abc.MutableSequence.pop,
    collections.abc.MutableSequence.insert,
    collections.abc.MutableSequence.remove,
    collections.abc.MutableSequence.__setitem__,
    collections.abc.MutableSequence.__delitem__,
)

_DEQUE_MUTATING_METHODS = _MUTABLE_SEQUENCE_MUTATING_METHODS + (
    collections.deque.appendleft,
    collections.deque.extendleft,
    collections.deque.popleft,
)


class ReactiveMutableSequence(reactive.Reactive[MutableSequenceType]):
    """
    Create a reactive object that wraps a mutable sequence.

    The mutable sequence is wrapped into a Proxy object which allows mutating methods to be patched in order to make
    them reactive.
    """

    def __init__(
        self,
        data: MutableSequenceType,
        *,
        layout: bool = False,
        repaint: bool = True,
    ) -> None:

        self._default = self._wrap_in_proxy(data)
        self.layout = layout
        self.repaint = repaint

    @staticmethod
    def _wrap_in_proxy(sequence: collections.abc.MutableSequence):
        if isinstance(sequence, collections.deque):
            return ProxyDeque(sequence)
        else:
            return ProxyMutableSequence(sequence)

    def __set_name__(self, owner: ty.Type[MessageTarget], name: str) -> None:

        if hasattr(owner, f"compute_{name}"):
            try:
                computes = getattr(owner, "__computes")
            except AttributeError:
                computes = []
                setattr(owner, "__computes", computes)
            computes.append(name)

        self.name = name
        self.internal_name = f"__{name}"
        setattr(owner, self.internal_name, self._default)

    def __get__(self, obj: Reactable, obj_type: type[object]) -> MutableSequenceType:
        sequence = getattr(obj, self.internal_name)
        self._patch_mutating_methods(sequence, obj)
        return sequence

    def __set__(self, obj: Reactable, value: collections.abc.MutableSequence) -> None:
        value = self._wrap_in_proxy(value)
        self._patch_mutating_methods(value, obj)
        return super().__set__(obj, value)

    def _patch_mutating_methods(self, sequence: collections.abc.MutableSequence, parent: Reactable):
        """
        Patch all the mutating methods on the mutable sequence with a callable that checks the watchers
        and triggers a refresh
        """
        if getattr(sequence, "__mutating_methods_patched__", False):
            return

        if isinstance(sequence, collections.deque):
            mutating_methods = _DEQUE_MUTATING_METHODS
        else:
            mutating_methods = _MUTABLE_SEQUENCE_MUTATING_METHODS

        for abstract_method in mutating_methods:

            def wraps():
                method = getattr(sequence, abstract_method.__name__)

                @functools.wraps(method)
                def wrapper(*args, **kwargs):
                    sequence = getattr(parent, self.internal_name)
                    old_value = sequence.copy()
                    result = method(*args, **kwargs)
                    self.check_watchers(parent, self.name, old_value)

                    if self.layout:
                        parent.refresh(layout=True)
                    elif self.repaint:
                        parent.refresh()
                    return result

                return wrapper

            setattr(sequence, abstract_method.__name__, wraps())

        setattr(sequence, "__mutating_methods_patched__", True)
