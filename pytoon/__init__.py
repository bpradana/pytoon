"""Public API for the pytoon encoder."""

from __future__ import annotations

from typing import Any

from .constants import DEFAULT_DELIMITER, DELIMITERS, Delimiter, DelimiterKey
from .encoders import encode_value
from .normalize import normalize_value
from .types import (
    EncodeOptions,
    JsonArray,
    JsonObject,
    JsonPrimitive,
    JsonValue,
    ResolvedEncodeOptions,
)

__all__ = [
    "encode",
    "DEFAULT_DELIMITER",
    "DELIMITERS",
    "Delimiter",
    "DelimiterKey",
    "JsonPrimitive",
    "JsonArray",
    "JsonObject",
    "JsonValue",
    "EncodeOptions",
    "ResolvedEncodeOptions",
]


def encode(input_value: Any, options: EncodeOptions | None = None) -> str:
    normalized = normalize_value(input_value)
    resolved_options = _resolve_options(options)
    return encode_value(normalized, resolved_options)


def _resolve_options(options: EncodeOptions | None) -> ResolvedEncodeOptions:
    indent = options.get("indent", 2) if options else 2
    delimiter = (
        options.get("delimiter", DEFAULT_DELIMITER) if options else DEFAULT_DELIMITER
    )
    length_marker = options.get("length_marker", False) if options else False
    return ResolvedEncodeOptions(
        indent=indent, delimiter=delimiter, length_marker=length_marker
    )
