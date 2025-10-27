"""Utility for accumulating formatted lines with indentation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .types import Depth


@dataclass
class LineWriter:
    indent_size: int
    _lines: List[str] = field(default_factory=list, init=False)
    _indentation: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._indentation = " " * self.indent_size

    def push(self, depth: Depth, content: str) -> None:
        indent = self._indentation * depth
        self._lines.append(f"{indent}{content}")

    def to_string(self) -> str:
        return "\n".join(self._lines)
