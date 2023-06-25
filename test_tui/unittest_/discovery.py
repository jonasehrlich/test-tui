import inspect
import pathlib
import typing as ty
import unittest

from test_tui.test_item import TestEntry


def generate_test_cases(suite: unittest.TestSuite) -> ty.Generator[unittest.TestCase, None, None]:
    """Unpack test suites to single test cases

    :param suite: Test suite to unpack
    :type suite: unittest.TestSuite
    :return: Generator that recursively yields test cases
    :rtype: ty.Generator[unittest.TestCase, None, None]
    :yield: Test case
    :rtype: Iterator[ty.Generator[unittest.TestCase, None, None]]
    """
    for test in suite:
        if isinstance(test, unittest.TestCase):
            yield test
        else:
            for test_case in generate_test_cases(test):
                yield test_case


def get_sourceline(obj: ty.Any) -> ty.Union[int, ty.Literal["*"]]:
    """Get the line an object is defined in the source file

    :param obj: Object to get the source line of
    :type obj: ty.Any
    :return: Source line in the file or a literal asterisk
    :rtype: ty.Union[int, ty.Literal["*"]]
    """
    try:
        source, line_number = inspect.getsourcelines(obj)
    except:
        try:
            # this handles `tornado` case we need a better
            # way to get to the wrapped function.
            # This is a temporary solution
            source, line_number = inspect.getsourcelines(obj.orig_method)
        except:
            return "*"

    for idx, line in enumerate(source):
        if line.strip().startswith(("def", "async def")):
            return line_number + idx
    return "*"


def get_sourcefile(obj: unittest.TestCase) -> ty.Union[None, pathlib.Path]:
    """Get the path to the source file of a unittest TestCase object

    :param obj: Python unittest TestCase
    :type obj: unittest.TestCase
    :return: Path to the source file where the test is defined, returns None if there is no way to find the path
    :rtype: ty.Union[None, pathlib.Path]
    """
    source_file = inspect.getsourcefile(obj.__class__)
    if source_file is not None:
        source_file = pathlib.Path(source_file)
    return source_file


def discover(start_dir: pathlib.Path, pattern: str) -> ty.Iterable[TestEntry]:
    loader = unittest.TestLoader()
    suite = loader.discover(str(start_dir), pattern=pattern)
    loader_errors = list()

    for test_case in generate_test_cases(suite):
        test_id = test_case.id()
        test_method = getattr(test_case, test_case._testMethodName)
        if test_id.startswith("unittest.loader._FailedTest"):
            # TODO: handle a loader error
            ...
        else:
            yield TestEntry(test_id, get_sourceline(test_method), get_sourcefile(test_case))
