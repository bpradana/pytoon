"""Constants used by the pytoon encoder."""

from __future__ import annotations

from typing import Dict, Final, Literal

# List markers
LIST_ITEM_MARKER: Final[str] = "-"
LIST_ITEM_PREFIX: Final[str] = "- "

# Structural characters
COMMA: Final[Literal[","]] = ","
COLON: Final[str] = ":"
SPACE: Final[str] = " "
PIPE: Final[Literal["|"]] = "|"

# Brackets and braces
OPEN_BRACKET: Final[str] = "["
CLOSE_BRACKET: Final[str] = "]"
OPEN_BRACE: Final[str] = "{"
CLOSE_BRACE: Final[str] = "}"

# Literals
NULL_LITERAL: Final[str] = "null"
TRUE_LITERAL: Final[str] = "true"
FALSE_LITERAL: Final[str] = "false"

# Escape characters
BACKSLASH: Final[str] = "\\"
DOUBLE_QUOTE: Final[str] = '"'
NEWLINE: Final[str] = "\n"
CARRIAGE_RETURN: Final[str] = "\r"
TAB: Final[Literal["\t"]] = "\t"
DelimiterKey = Literal["comma", "tab", "pipe"]
Delimiter = Literal[",", "\t", "|"]

DELIMITERS: Dict[DelimiterKey, Delimiter] = {
    "comma": COMMA,
    "tab": TAB,
    "pipe": PIPE,
}

DEFAULT_DELIMITER: Final[Delimiter] = DELIMITERS["comma"]
