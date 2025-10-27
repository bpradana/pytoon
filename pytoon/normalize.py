"""Normalization utilities converting arbitrary Python objects to JsonValue."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from math import copysign, isfinite
from typing import Any, Dict

from .types import JsonArray, JsonValue


def normalize_value(value: Any) -> JsonValue:
    """Normalize arbitrary input into a JsonValue-friendly structure."""
    if value is None:
        return None

    if isinstance(value, (str, bool)):
        return value

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if isinstance(value, float):
            if not isfinite(value):
                return None
            if value == 0.0 and copysign(1.0, value) == -1.0:
                return 0
        return value

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    if is_dataclass(value):
        return normalize_value(asdict(value))

    if isinstance(value, (set, frozenset)):
        return [normalize_value(v) for v in value]

    if isinstance(value, Mapping):
        normalized: Dict[str, JsonValue] = {}
        for key, item in value.items():
            normalized[str(key)] = normalize_value(item)
        return normalized

    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [normalize_value(item) for item in value]

    return None


def is_json_primitive(value: Any) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def is_json_array(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def is_json_object(value: Any) -> bool:
    return isinstance(value, Mapping)


def is_array_of_primitives(value: JsonArray) -> bool:
    return all(is_json_primitive(item) for item in value)


def is_array_of_arrays(value: JsonArray) -> bool:
    return all(is_json_array(item) for item in value)


def is_array_of_objects(value: JsonArray) -> bool:
    return all(is_json_object(item) for item in value)
