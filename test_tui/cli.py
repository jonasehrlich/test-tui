import argparse
import typing as ty
import sys
from test_tui.unittest_ import discovery as unittest_discover


def get_unittest_discovery_parser():
    ...

def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run")
    subparsers = parser.add_subparsers()
    subparsers.add_parser("unittest")

    parser.add_argument("-s", "--start-directory", dest="start", help="Directory to start discovery ('.' default)")
    parser.add_argument("-p", "--pattern", dest="pattern", help="Pattern to match tests ('test*.py' default)")
    parser.add_argument(
        "-t",
        "--top-level-directory",
        dest="top",
        help="Top level directory of project (defaults to " "start directory)",
    )
    return parser


def main(argv: ty.Optional[ty.List[str]] = None):
    parser = get_arg_parser()
    if argv is None:
        argv = sys.argv
    namespace = parser.parse_args(argv)
    ...


if __name__ == "__main__":
    main()
