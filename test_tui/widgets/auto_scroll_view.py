import typing as ty

from rich import console, style
from textual import reactive, widget, widgets, messages, message


class AutoScrollView(widgets.ScrollView):
    def __init__(self, *args, auto_scroll_target: ty.Literal["top", "bottom"] = "bottom", **kwargs):
        self.auto_scroll_target = auto_scroll_target
        super().__init__(*args, **kwargs)

    @property
    def auto_scroll_enabled(self) -> bool:
        """Return whether auto scroll is enabled.

        Auto scroll is only enabled if the current scroll position is at the `auto_scroll_target`"""
        if self.auto_scroll_target == "top":
            target = 0
        else:
            target = self.window.virtual_size.height

        return self.y != target

    def get_auto_scroll_target_line(self) -> int:
        if self.auto_scroll_target == "top":
            return 0
        return self.window.virtual_size.height


    async def handle_window_change(self, message: message.Message) -> None:
        if self.auto_scroll_enabled:
            self.scroll_in_to_view(self.get_auto_scroll_target_line())
        return await super().handle_window_change(message)
