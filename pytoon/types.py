"""Type definitions for the pytoon encoder."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Mapping, MutableMapping, Sequence, TypedDict, Union

from .constants import Delimiter

JsonPrimitive = Union[str, int, float, bool, None]
JsonObject = Union[MutableMapping[str, "JsonValue"], Mapping[str, "JsonValue"]]
JsonArray = Sequence["JsonValue"]
JsonValue = Union[JsonPrimitive, JsonObject, JsonArray]


class EncodeOptions(TypedDict, total=False):
    indent: int
    delimiter: Delimiter
    length_marker: Literal["#", False]


@dataclass(frozen=True)
class ResolvedEncodeOptions:
    indent: int
    delimiter: Delimiter
    length_marker: Literal["#", False]


Depth = int
