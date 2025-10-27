from __future__ import annotations

import unittest

from pytoon import encode


class EncodePrimitivesTest(unittest.TestCase):
    def test_safe_string_unquoted(self) -> None:
        self.assertEqual(encode("hello"), "hello")
        self.assertEqual(encode("Ada_99"), "Ada_99")

    def test_quotes_and_escapes_strings(self) -> None:
        self.assertEqual(encode(""), '""')
        self.assertEqual(encode("true"), '"true"')
        self.assertEqual(encode("line1\nline2"), '"line1\\nline2"')

    def test_numbers_and_booleans(self) -> None:
        self.assertEqual(encode(42), "42")
        self.assertEqual(encode(-0.0), "0")
        self.assertEqual(encode(1e-6), "0.000001")
        self.assertEqual(encode(True), "true")
        self.assertEqual(encode(False), "false")


class EncodeObjectsTest(unittest.TestCase):
    def test_simple_object(self) -> None:
        payload = {"id": 123, "name": "Ada", "active": True}
        self.assertEqual(encode(payload), "id: 123\nname: Ada\nactive: true")

    def test_nested_object(self) -> None:
        payload = {"user": {"id": 1, "prefs": []}}
        self.assertEqual(encode(payload), "user:\n  id: 1\n  prefs[0]:")


class EncodeArraysTest(unittest.TestCase):
    def test_inline_primitive_array(self) -> None:
        payload = {"tags": ["reading", "gaming"]}
        self.assertEqual(encode(payload), "tags[2]: reading,gaming")

    def test_tabular_object_array(self) -> None:
        payload = {"items": [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Bob"}]}
        self.assertEqual(
            encode(payload),
            "items[2]{id,name}:\n  1,Ada\n  2,Bob",
        )

    def test_list_object_array(self) -> None:
        payload = {
            "items": [
                {"id": 1, "name": "Ada"},
                {"id": 2, "name": "Bob", "extra": True},
            ]
        }
        self.assertEqual(
            encode(payload),
            "items[2]:\n"
            "  - id: 1\n"
            "    name: Ada\n"
            "  - id: 2\n"
            "    name: Bob\n"
            "    extra: true",
        )

    def test_array_of_arrays(self) -> None:
        payload = {"pairs": [["a", "b"], ["c", "d"]]}
        self.assertEqual(
            encode(payload),
            "pairs[2]:\n  - [2]: a,b\n  - [2]: c,d",
        )


class EncodeOptionsTest(unittest.TestCase):
    def test_custom_delimiter(self) -> None:
        payload = {"items": ["a", "b|c", "d"]}
        self.assertEqual(
            encode(payload, {"delimiter": "|"}),
            'items[3|]: a|"b|c"|d',
        )

    def test_length_marker(self) -> None:
        payload = {"tags": ["reading", "gaming", "coding"]}
        self.assertEqual(
            encode(payload, {"length_marker": "#"}),
            "tags[#3]: reading,gaming,coding",
        )


if __name__ == "__main__":
    unittest.main()
