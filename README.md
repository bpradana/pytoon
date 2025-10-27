PyTOON
======

PyTOON is a Python port of the excellent [`toon`](https://github.com/johannschopplich/toon) project by Johann Schopplich. It converts arbitrary Python data structures into the same concise, human-readable text representation produced by the original TypeScript encoder.

The goal of this repository is feature parity with the source project while offering a first-class experience for Python applications and tooling.

Features
--------
- Normalises native Python types (dicts, lists, dataclasses, sets, `datetime`, numeric edge cases, etc.) to a JSON-like value space before encoding.
- Produces the familiar Toon text format with support for inline arrays, tabular object arrays, and deeply nested structures.
- Configurable indentation, row delimiter (`','`, `'|'`, `'\t'`), and optional length marker flag (`[#N]` style headers).
- Safe string quoting and escaping rules that match the upstream implementation.
- Lightweight dependency-free package targeting Python 3.8+.

Installation
------------

```bash
pip install pytoon-encoder
```

If you are working from this repository, install it in editable mode:

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
        "length_marker": "#",            # renders headers as [#N]
    },
)
```

Output:

```
items[#2|]{id|name}:
  1|Ada
  2|Bob
```

Testing
-------

Tests are implemented with Python's standard `unittest` framework:

```bash
python3 -m unittest discover -s tests
```

To ensure behaviour matches upstream, we recommend porting and expanding the fixture coverage found in `docs/toon-main/test/index.test.ts`.

Project Structure
-----------------

- `pytoon/` – Core encoder modules (`constants`, `normalize`, `primitives`, `encoders`, `writer`).
- `tests/` – Unit tests that exercise key encoding scenarios.

Versioning & Compatibility
--------------------------

PyTOON targets Python 3.8+ and strives to remain aligned with the latest upstream `toon` behaviour. Breaking changes to the text format will only occur alongside upstream updates and will be noted in release notes.

Contributing
------------

Contributions are welcome! To get started:

1. Fork and clone the repository.
2. Create a virtual environment for Python 3.8 or newer.
3. Install in editable mode with testing extras: `pip install -e .`.
4. Run `python3 -m unittest discover -s tests` before submitting a pull request.

When porting behaviour from the TypeScript project, please include links or references to the corresponding upstream implementation and tests for easier review.

License
-------

PyTOON retains the licensing of the original [`toon`](https://github.com/johannschopplich/toon) project. Refer to `LICENSE` for details.
