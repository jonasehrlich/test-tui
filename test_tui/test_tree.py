
from __future__ import annotations
from textual.widgets import TreeControl
from .test_item import TestEntry
import functools
import typing as ty

class TestTree(TreeControl[TestEntry]):
    ...
    def __init__(        self,
        loader: ty.Callable[[], ty.AsyncGenerator[None, TestEntry]],
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None) -> None:
        self._loader = loader
        super().__init__("tests", data, name=name, id=id, classes=classes)

    def render_tree_label(
        self,
        node: TreeNode[TestEntry],
        is_dir: bool,
        expanded: bool,
        is_cursor: bool,
        is_hover: bool,
        has_focus: bool,
    ) -> RenderableType:
        ...

    async def load_tests(self):
        async for test_item in self._loader():
            ...

    async def on_mount(self) -> None:
        await self.load_tests()


    def on_styles_updated(self) -> None:
        self.render_tree_label.cache_clear()
