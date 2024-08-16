from dataclasses import dataclass
from typing import Callable


@dataclass
class Name:
    name: str
    gender: str
    count: int


@dataclass
class Source:
    name: str
    fetch: Callable[[], dict[int, list[Name]]]
