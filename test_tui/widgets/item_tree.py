import dataclasses
import functools

from rich.text import Text
import rich.repr
from rich.console import RenderableType
from textual import reactive, message
from textual.widgets import TreeControl, TreeNode, TreeClick

from textual import events
import typing as ty

from test_tui.test_item import TestEntry


@dataclasses.dataclass
class TreeEntry:
    test_item: TestEntry
    is_running: bool = False
    is_single_test: bool = False
    is_executable: bool = True



@rich.repr.auto
class ItemClick(message.Message, bubble=True):
    """Message representing the click onto a  item"""
    def __init__(self, sender: message.MessageTarget, test_item: TestEntry) -> None:
        self.test_item = test_item
        super().__init__(sender)


class ItemTree(TreeControl[TreeEntry]):
    has_focus = reactive.Reactive(False)

    def __init__(self, name: str, test_item_source: ty.Callable[[], ty.Iterable[TestEntry]], ) -> None:
        self.test_item_source = test_item_source
        # TODO: figure out root element
        super().__init__("Tests", name=name, data=TreeEntry(None, is_executable=False))
        self.root.tree.guide_style = "black"


    @functools.lru_cache(maxsize=1024 * 32)
    def render_tree_label(
        self,
        node: TreeNode[TreeEntry],
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

    async def handle_tree_click(self, message: TreeClick[TreeEntry]) -> None:
        dir_entry = message.node.data
        if dir_entry.is_single_test:
            await self.emit(ItemClick(self, dir_entry.test_item))
        else:
            if not message.node.loaded:
                ...
            else:
                await message.node.toggle()

    async def load_test_item_tree(self) -> TreeNode[TreeEntry]:
        data = TreeEntry
