import dataclasses
import pathlib
import typing as ty


@dataclasses.dataclass
class TestEntry:
    """Dataclass representation of a single test"""

    path: pathlib.Path
    line_number: ty.Union[int, ty.Literal["*"]]
    id: str


@dataclasses.dataclass()
class DirEntry:
    path: pathlib.Path
    is_dir: bool
