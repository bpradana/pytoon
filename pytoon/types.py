"""Type definitions for the pytoon encoder."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Mapping, MutableMapping, Sequence, TypedDict

from .constants import Delimiter

JsonPrimitive = str | int | float | bool | None
JsonObject = MutableMapping[str, "JsonValue"] | Mapping[str, "JsonValue"]
JsonArray = Sequence["JsonValue"]
JsonValue = JsonPrimitive | JsonObject | JsonArray


class EncodeOptions(TypedDict, total=False):
    indent: int
    delimiter: Delimiter
    length_marker: Literal["#", False]


@dataclass(slots=True, frozen=True)
class ResolvedEncodeOptions:
    indent: int
    delimiter: Delimiter
    length_marker: Literal["#", False]


Depth = int
