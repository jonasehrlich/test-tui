import dataclasses
import functools
import logging

from rich.text import Text
import rich.repr
from rich.console import RenderableType
from textual.message import Message, MessageTarget
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import TreeControl, TreeNode, TreeClick

from textual import events
import typing as ty

from test_tui.test_item import TestEntry


@dataclasses.dataclass
class TestTreeEntry:
    test_item: TestEntry
    is_running: bool = False
    is_single_test: bool = False
    is_executable: bool = True



@rich.repr.auto
class TestItemClick(Message, bubble=True):
    """Message representing the click onto a test item"""
    def __init__(self, sender: MessageTarget, test_item: TestEntry) -> None:
        self.test_item = test_item
        super().__init__(sender)


class TestItemTree(TreeControl[TestTreeEntry]):
    has_focus: Reactive[bool] = Reactive(False)

    def __init__(self, name: str, test_item_source: ty.Callable[[], ty.Iterable[TestEntry]], ) -> None:
        self.test_item_source = test_item_source
        # TODO: figure out root element
        super().__init__("Tests", name=name, data=TestTreeEntry(None, is_executable=False))
        self.root.tree.guide_style = "black"


    @functools.lru_cache(maxsize=1024 * 32)
    def render_tree_label(
        self,
        node: TreeNode[TestTreeEntry],
        expanded: bool,
        is_cursor: bool,
        is_hover: bool,
        is_running: bool,
        is_single_test: bool,
        has_focus: bool,
    ) -> RenderableType:
        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }
        label = Text(node.label) if isinstance(node.label, str) else node.label
        if is_hover:
            label.stylize("underline")

        if not is_single_test:
            label.stylize("bold magenta")
            icon = "📂" if expanded else "📁"
        else:
            label.stylize("bright_green")
            icon = "📄"
            label.highlight_regex(r"\..*$", "green")

        if is_running:
            icon = "🏃"

        if label.plain.startswith("."):
            label.stylize("dim")

        if is_cursor and has_focus:
            label.stylize("reverse")

        icon_label = Text(f"{icon} ", no_wrap=True, overflow="ellipsis") + label
        icon_label.apply_meta(meta)
        return icon_label

    async def on_mount(self, event: events.Mount) -> None:
        # load tests
        ...

    def on_focus(self) -> None:
        self.has_focus = True

    def on_blur(self) -> None:
        self.has_focus = False

    async def handle_tree_click(self, message: TreeClick[TestTreeEntry]) -> None:
        dir_entry = message.node.data
        if dir_entry.is_single_test:
            await self.emit(TestItemClick(self, dir_entry.test_item))
        else:
            if not message.node.loaded:
                ...
            else:
                await message.node.toggle()

    async def load_test_item_tree(self) -> TreeNode[TestTreeEntry]:
        data = TestTreeEntry


class WidgetLogHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        ...


class LogWidget(Widget):
    """Widget containing the out """
    def get_log_handler(self) -> logging.Handler:

        ...
    ...
