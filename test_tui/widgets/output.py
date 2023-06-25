from __future__ import annotations

import collections
import collections.abc
import typing as ty

from rich import console, style
from textual import message, widget, messages
from test_tui.reactive import ReactiveMutableSequence


class ContentChange(message.Message):
    """Message that the content of the widget has changed"""

class OutputWidget(widget.Widget):
    content = ReactiveMutableSequence[ty.MutableSequence[console.RenderableType]](collections.deque(maxlen=1000))

    def render(self) -> console.Group:
        return console.Group(*self.content)

    async def watch_content(self, _new_value):

        await self.emit(messages.Update(self, self))
