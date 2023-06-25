from __future__ import annotations

import functools
import io
import typing as ty

from rich import console
from textual import messages, widget

AnyIO_T = ty.TypeVar("AnyIO_T", bound=io.IOBase)


def patch_stream_flush(stream: AnyIO_T, flush_cb: ty.Callable[[], None]) -> AnyIO_T:
    def get_wrapper():
        orig_flush = stream.flush

        @functools.wraps(orig_flush)
        def wrapper():
            orig_flush()
            flush_cb()

        return wrapper

    stream.flush = get_wrapper()
    return stream


class StreamWidget(widget.Widget):
    def __init__(self, stream: io.StringIO | None = None, name: str | None = None) -> None:
        super().__init__(name)
        stream = stream or io.StringIO()
        self.stream = patch_stream_flush(stream, self._handle_stream_flush)

    def _handle_stream_flush(self):
        self.emit_no_wait(messages.Update(self, self))

    def render(self) -> console.RenderableType:
        return self.stream.getvalue()
