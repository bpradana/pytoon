PyTOON
======

PyTOON is a Python port of the excellent [`toon`](https://github.com/johannschopplich/toon) project by Johann Schopplich. It converts arbitrary Python data structures into the same concise, human-readable text representation produced by the original TypeScript encoder.

The goal of this repository is feature parity with the upstream project while providing a first-class experience for Python applications and tooling.

Contents
--------
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Normalization Reference](#normalization-reference)
- [Encoding Behaviour](#encoding-behaviour)
- [Options](#options)
- [Advanced Usage](#advanced-usage)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Versioning & Compatibility](#versioning--compatibility)
- [Contributing](#contributing)
- [License](#license)

Features
--------
- Normalises native Python types (dicts, lists, dataclasses, sets, `datetime`, numeric edge cases, etc.) to a JSON-like value space before encoding.
- Produces the familiar Toon text format with support for inline arrays, tabular object arrays, and deeply nested structures.
- Configurable indentation, row delimiter (`','`, `'|'`, `'\t'`), and optional length marker flag (`[#N]` style headers).
- Safe string quoting and escaping rules that match the upstream implementation.
- Pure-Python, dependency-free package targeting Python 3.8+.

Installation
------------

```bash
pip install pytoon-encoder
```

Working from a clone of this repository? Install in editable mode:

```bash
pip install -e .
```

Quick Start
-----------

```python
from pytoon import encode

payload = {
    "user": {
        "id": 123,
        "name": "Ada",
        "tags": ["reading", "gaming"],
        "active": True,
        "prefs": [],
    }
}

print(encode(payload))
```

Output:

```
user:
  id: 123
  name: Ada
  tags[2]: reading,gaming
  active: true
  prefs[0]:
```

Normalization Reference
-----------------------

PyTOON first normalises values into a JSON-compatible shape. The table below mirrors the upstream Toon rules:

| Python value                                  | Normalised result                         | Notes                                                                 |
|-----------------------------------------------|-------------------------------------------|-----------------------------------------------------------------------|
| `None`                                        | `None`                                    | Encodes as `null`.                                                    |
| `bool`, `int`, `float`                        | Same numeric/boolean value                | Floats that are `NaN`, `±inf` become `None`; `-0.0` becomes `0`.      |
| `str`                                         | Same string                               | Subject to quoting/escaping rules during encoding.                    |
| `datetime`, `date`                            | ISO-8601 string                           | Uses `.isoformat()`.                                                  |
| `set`, `frozenset`                            | List of normalised elements               | Order is the iteration order of the set.                              |
| `list`, `tuple`, other sequences (not bytes)  | List of normalised elements               | Preserves order.                                                      |
| `dict`, `Mapping`                             | Dict with stringified keys                | Keys are coerced with `str(key)`; values normalised recursively.      |
| `dataclass` instances                         | Dict via `dataclasses.asdict`             | Deep conversion, then recurses.                                       |
| Unsupported objects, functions, generators    | `None`                                    | Matches behaviour of upstream encoder.                                |

Encoding Behaviour
------------------

PyTOON selects the most legible format while preserving structure:

- **Objects** render as `key: value` lines in insertion order. Empty objects emit just `key:`.
- **Arrays of primitives** appear inline: `tags[3]: a,b,c`.
- **Arrays of objects** become tabular if every object shares identical primitive keys. Otherwise, items are rendered as `-` list entries.
- **Arrays of arrays** with primitive inner arrays become nested lists; mixed or non-primitive inner arrays fall back to expanded list items.
- **Mixed arrays** (primitives, objects, arrays combined) always degrade to list entries.
- **Strings** remain unquoted only if they contain no structural characters, delimiters, leading/trailing whitespace, or ambiguous literals (`"true"`, `"42"`, etc.). Otherwise, they are quoted and escaped.

See [`examples/basic_usage.py`](examples/basic_usage.py) for ready-to-run scenarios.

Options
-------

`encode` accepts an optional `EncodeOptions` dictionary that mirrors the TypeScript API:

```python
from pytoon import encode, DELIMITERS

encode(
    {"items": [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Bob"}]},
    {
        "indent": 4,
        "delimiter": DELIMITERS["pipe"],  # or ',' / '\t'
        "length_marker": "#",             # renders headers as [#N]
    },
)
```

Output:

```
items[#2|]{id|name}:
  1|Ada
  2|Bob
```

Option reference:

| Option          | Type                 | Default | Description                                                                                 |
|-----------------|----------------------|---------|---------------------------------------------------------------------------------------------|
| `indent`        | `int`                | `2`     | Spaces per indentation level for nested structures.                                         |
| `delimiter`     | `','`, `'|'`, `'\t'` | `','`   | Active delimiter for inline arrays and tabular rows.                                        |
| `length_marker` | `'#'` or `False`     | `False` | When `'#'`, emits headers like `[#3]`; helpful when the consumer expects marked lengths.    |

Advanced Usage
--------------

- **Pre-normalisation**: Import `normalize_value` from `pytoon.normalize` to convert data once, then reuse the normalised structure across multiple encodings or transport layers.
- **Direct value encoding**: `pytoon.encoders.encode_value` accepts a pre-normalised JSON value plus resolved options, allowing integration with custom line writers or alternative indentation strategies.
- **Custom delimiters**: The `DELIMITERS` constant exposes the supported delimiter characters. Pass alternate values (e.g. `DELIMITERS["tab"]`) to match TSV-style pipelines.
- **Examples**: The [`examples/`](examples/README.md) directory contains scripts that highlight default behaviour and option combinations. Extend these for domain-specific onboarding material.
- **Automation**: `.github/workflows/ci.yml` runs unit tests on every push and publishes tagged releases (`v*`) to PyPI once tests pass.

Testing
-------

Tests use Python's built-in `unittest` framework:

```bash
python3 -m unittest discover -s tests
```

When porting new behaviour from `toon`, add corresponding tests here to keep parity strong.

Project Structure
-----------------

- `pytoon/` – Core encoder modules (`constants`, `normalize`, `primitives`, `encoders`, `writer`).
- `tests/` – Unit tests covering primitives, objects, arrays, options, and edge cases.
- `examples/` – Runnable scripts that demonstrate practical usage patterns.

Versioning & Compatibility
--------------------------

PyTOON targets Python 3.8+ and strives to remain aligned with the latest upstream `toon` behaviour. Breaking format changes follow upstream and will be clearly documented in release notes.

Contributing
------------

Contributions are welcome! To get started:

1. Fork and clone the repository.
2. Create a virtual environment for Python 3.8 or newer.
3. Install in editable mode with dev extras: `pip install -e .[dev]`.
4. Run `python3 -m unittest discover -s tests` before submitting a pull request.

License
-------

PyTOON retains the licensing of the original [`toon`](https://github.com/johannschopplich/toon) project. Refer to [`LICENSE`](LICENSE) for details.
