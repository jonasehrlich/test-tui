import itertools
import pathlib
import random

from test_tui.test_tree import  TestTree
from test_tui.test_item import TestEntry, DirEntry


import typing as ty

import sys

from rich.syntax import Syntax
from rich.traceback import Traceback

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.reactive import var
from textual.widgets import Tree, Header, Footer

def loader():
    core_path = pathlib.Path("package/core/test")
    core_tests1_name = "test_something"
    core_tests1 = (
        TestEntry(
            core_path / core_tests1_name,
            random.randint(10, 300),
            f"TestSomething.test_{idx:04d}",
        )
        for idx in range(3)
    )

    core_tests2_name = "test_something1"
    core_tests2 = (
        TestEntry(
            core_path / core_tests2_name,
            random.randint(10, 300),
            f"TestSomething.test_{idx:04d}",
        )
        for idx in range(3)
    )

    module_path = pathlib.Path("package/module/test")
    module_tests1_name = "test_something"
    module_tests1 = (
        TestEntry(
            module_path / module_tests1_name,
            random.randint(10, 300),
            f"TestSomething.test_{idx:04d}",
        )
        for idx in range(3)
    )
    for test_item in itertools.chain(core_tests1, core_tests2, module_tests1):
        yield test_item


TreeItem = ty.TypeVar("TreeItem", TestEntry, DirEntry)




class TreeProvider(ty.Generic[TreeItem]):
    data: ty.Dict[str, TreeItem]

    def __init__(self, loader: ty.Callable[[], ty.AsyncIterable[TestEntry]]) -> None:
        self.loader = loader

    async def reload(self):
        """Reload the tree items from the loader and refill the data tree"""

        async for item in self.loader():
            ...

    def get_sub_items(self, id: str):
        ...


class TestItemTree(Tree[ty.Union[TestEntry, DirEntry]]):
    ...

class TreeTest(App):

    # CSS_PATH = "code_browser.css"
    BINDINGS = [
        ("f", "toggle_files", "Toggle Files"),
        ("q", "quit", "Quit"),
    ]

    show_tree = var(True)

    def watch_show_tree(self, show_tree: bool) -> None:
        """Called when show_tree is modified."""
        self.set_class(show_tree, "-show-tree")

    def compose(self) -> ComposeResult:
        """Compose our UI."""
        path = "./" if len(sys.argv) < 2 else sys.argv[1]
        yield Header()
        yield Container(
            TestTree(path, id="tree-view"),
            # Vertical(Static(id="code", expand=True), id="code-view"),
        )
        yield Footer()

    # def on_mount(self, event: events.Mount) -> None:
    #     self.query_one(DirectoryTree).focus()

    def on_directory_tree_file_selected(self, event: .FileClick) -> None:
        """Called when the user click a file in the directory tree."""
        event.stop()
        code_view = self.query_one("#code", Static)
        try:
            syntax = Syntax.from_path(
                event.path,
                line_numbers=True,
                word_wrap=False,
                indent_guides=True,
                theme="github-dark",
            )
        except Exception:
            code_view.update(Traceback(theme="github-dark", width=None))
            self.sub_title = "ERROR"
        else:
            code_view.update(syntax)
            self.query_one("#code-view").scroll_home(animate=False)
            self.sub_title = event.path

    def action_toggle_files(self) -> None:
        """Called in response to key binding."""
        self.show_tree = not self.show_tree


if __name__ == "__main__":
    TreeTest().run()
