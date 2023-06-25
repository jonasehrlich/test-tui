import unittest
import logging
import functools


class TestSomething(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logging.basicConfig(level=logging.INFO)

    @classmethod
    def tearDownClass(cls) -> None:
        logging.root.handlers = list()

    def test_pass(self):
        ...


    def test_logging(self):
        ...
