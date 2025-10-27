"""Primitive encoding helpers."""

from __future__ import annotations

import re
from typing import Iterable, Literal

from .constants import (
    BACKSLASH,
    COMMA,
    DEFAULT_DELIMITER,
    DOUBLE_QUOTE,
    FALSE_LITERAL,
    LIST_ITEM_MARKER,
    NULL_LITERAL,
    TRUE_LITERAL,
)
from .types import JsonPrimitive


def encode_primitive(value: JsonPrimitive, delimiter: str | None = None) -> str:
    if value is None:
        return NULL_LITERAL

    if isinstance(value, bool):
        return TRUE_LITERAL if value else FALSE_LITERAL

    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)

    if isinstance(value, float):
        return _encode_number(value)

    return encode_string_literal(value, delimiter or COMMA)


def _encode_number(value: float) -> str:
    if value.is_integer():
        return str(int(value))

    text = format(value, ".15f")
    text = text.rstrip("0").rstrip(".")
    return text or "0"


def encode_string_literal(value: str, delimiter: str = COMMA) -> str:
    if is_safe_unquoted(value, delimiter):
        return value
    return f"{DOUBLE_QUOTE}{escape_string(value)}{DOUBLE_QUOTE}"


def escape_string(value: str) -> str:
    return (
        value.replace(BACKSLASH, f"{BACKSLASH}{BACKSLASH}")
        .replace(DOUBLE_QUOTE, f"{BACKSLASH}{DOUBLE_QUOTE}")
        .replace("\n", f"{BACKSLASH}n")
        .replace("\r", f"{BACKSLASH}r")
        .replace("\t", f"{BACKSLASH}t")
    )


def is_safe_unquoted(value: str, delimiter: str = COMMA) -> bool:
    if not value:
        return False

    if value != value.strip():
        return False

    if value in {TRUE_LITERAL, FALSE_LITERAL, NULL_LITERAL}:
        return False

    if _is_numeric_like(value):
        return False

    if ":" in value:
        return False

    if '"' in value or "\\" in value:
        return False

    if any(ch in value for ch in "[]{}"):
        return False

    if any(ctrl in value for ctrl in ("\n", "\r", "\t")):
        return False

    if delimiter in value:
        return False

    if value.startswith(LIST_ITEM_MARKER):
        return False

    return True


_NUMERIC_PATTERN = re.compile(r"-?\d+(?:\.\d+)?(?:e[+-]?\d+)?", re.IGNORECASE)
_LEADING_ZERO_PATTERN = re.compile(r"0\d+")


def _is_numeric_like(value: str) -> bool:
    return bool(_NUMERIC_PATTERN.fullmatch(value) or _LEADING_ZERO_PATTERN.fullmatch(value))


def encode_key(key: str) -> str:
    if _is_valid_unquoted_key(key):
        return key
    return f"{DOUBLE_QUOTE}{escape_string(key)}{DOUBLE_QUOTE}"


_KEY_PATTERN = re.compile(r"[A-Za-z_][\w.]*")


def _is_valid_unquoted_key(key: str) -> bool:
    return bool(_KEY_PATTERN.fullmatch(key))


def join_encoded_values(values: Iterable[JsonPrimitive], delimiter: str = COMMA) -> str:
    return delimiter.join(encode_primitive(value, delimiter) for value in values)


def format_header(
    length: int,
    *,
    key: str | None = None,
    fields: Iterable[str] | None = None,
    delimiter: str = COMMA,
    length_marker: Literal["#", False] = False,
) -> str:
    active_delimiter = delimiter or DEFAULT_DELIMITER
    header = ""

    if key:
        header += encode_key(key)

    marker = length_marker or ""
    delimiter_suffix = "" if active_delimiter == DEFAULT_DELIMITER else active_delimiter
    header += f"[{marker}{length}{delimiter_suffix}]"

    if fields:
        encoded_fields = (encode_key(field) for field in fields)
        header += f"{{{delimiter.join(encoded_fields)}}}"

    header += ":"
    return header
