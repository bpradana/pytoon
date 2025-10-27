"""Simple usage examples for pytoon."""

from __future__ import annotations

from pytoon import DELIMITERS, EncodeOptions, encode


def main() -> None:
    payload = {
        "user": {
            "id": 123,
            "name": "Ada",
            "tags": ["reading", "gaming"],
            "active": True,
            "prefs": [],
        },
        "history": [
            {"sku": "A1", "qty": 2, "price": 9.99},
            {"sku": "B2", "qty": 1, "price": 14.5},
        ],
    }

    print("Default encoding:\n")
    print(encode(payload))
    print("\nCustom delimiter, length marker:\n")
    print(
        encode(
            payload["history"],
            EncodeOptions(
                indent=4,
                delimiter=DELIMITERS["pipe"],
                length_marker="#",
            ),
        )
    )


if __name__ == "__main__":
    main()
