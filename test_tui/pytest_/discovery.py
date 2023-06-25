from __future__ import annotations
import inspect
import pytest
import typing as ty
from test_tui.test_item import TestEntry

from collections import UserList

def discover(pytest_args: ty.Sequence[str]) -> ty.Iterable[TestEntry]:
    pytest_args = list(_adjust_pytest_args(pytest_args))
    collector = TestCollector()
    return_code = pytest.main(pytest_args, plugins=[collector])
    if return_code == 5:
        # No tests were discovered
        ...

    elif return_code != 0:
        raise RuntimeError("Error collecting tests")
    if not collector._started:
        raise RuntimeError("Pytest discovery did not start")

    return list(collector.tests)




class TestCollection:
    """Iterable container of collected tests"""

    def __init__(self) -> None:
        self._tests = list()

    def reset(self):
        self._tests = list()

    def add_test(self, test):
        test_item = convert_to_test_item(test)
        self._tests.append(test_item)

    def __iter__(self):
        return iter(self._tests)

    def __contains__(self, other):
        return other in self._tests

def convert_to_test_item(item: _pytest.python.Function) -> TestEntry:
    line_number = inspect.getsourcelines(item.function)
    return TestEntry(item.nodeid, )
    ...

class TestCollector:
    """This is a pytest plugin that collects the discovered tests."""

    def __init__(self):
        self.tests = TestCollection()
        self._started = False

    # Relevant plugin hooks:
    #  https://docs.pytest.org/en/latest/reference.html#collection-hooks

    def pytest_collection_modifyitems(self, session, config, items):
        self._started = True
        self.tests.reset()
        for item in items:
            self.tests.add_test(item)

    # This hook is not specified in the docs, so we also provide
    # the "modifyitems" hook just in case.
    def pytest_collection_finish(self, session):
        self._started = True
        try:
            items = session.items
        except AttributeError:
            # TODO: Is there an alternative?
            return
        # self._tests.reset()
        for item in items:
            self.tests.add_test(item)


def _adjust_pytest_args(pytest_args: ty.Sequence[str]) -> ty.Sequence[str]:
    """Return a corrected copy of the given pytest CLI args."""
    pytestargs = list(pytest_args) if pytest_args else []
    # Duplicate entries should be okay.
    pytestargs.insert(0, "--collect-only")
    return pytestargs


if __name__ == "__main__":
    import os

    os.chdir("/home/jonas/projects/github/argparse-shell")

    pytest.main(["--collect-only"], plugins=[TestCollector()])
