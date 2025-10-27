from __future__ import annotations

import math
import unittest
from dataclasses import dataclass
from typing import Any, Dict, Optional

from pytoon import DELIMITERS, encode
from pytoon.normalize import normalize_value


class EncodeTestCase(unittest.TestCase):
    def assertEncoding(
        self,
        value: Any,
        expected: str,
        options: Optional[Dict[str, Any]] = None,
        msg: Optional[str] = None,
    ) -> None:
        self.assertEqual(encode(value, options), expected, msg)


class EncodePrimitivesTest(EncodeTestCase):
    def test_unquoted_strings(self) -> None:
        cases = [
            ("hello", "hello"),
            ("Ada_99", "Ada_99"),
            ("emoji 🚀", "emoji 🚀"),
        ]
        for source, expected in cases:
            with self.subTest(value=source):
                self.assertEncoding(source, expected)

    def test_strings_requiring_quotes(self) -> None:
        cases = {
            "": '""',
            "true": '"true"',
            " line ": '" line "',
            'say "hi"': '"say \\"hi\\""',
            "x,y": '"x,y"',
            "[array]": '"[array]"',
            "- item": '"- item"',
        }
        for source, expected in cases.items():
            with self.subTest(value=source):
                self.assertEncoding(source, expected)

    def test_numbers_booleans_and_null(self) -> None:
        self.assertEncoding(42, "42")
        self.assertEncoding(-0.0, "0")
        self.assertEncoding(1e-6, "0.000001")
        self.assertEncoding(1e20, "100000000000000000000")
        self.assertEncoding(True, "true")
        self.assertEncoding(False, "false")
        self.assertEncoding(None, "null")

    def test_special_float_values_encode_as_null(self) -> None:
        for value in (math.nan, math.inf, -math.inf):
            with self.subTest(value=value):
                self.assertEncoding(value, "null")


class EncodeObjectsTest(EncodeTestCase):
    def test_preserves_key_order(self) -> None:
        payload = {"id": 123, "name": "Ada", "active": True}
        self.assertEncoding(payload, "id: 123\nname: Ada\nactive: true")

    def test_nested_objects_and_empty_children(self) -> None:
        payload = {"user": {"profile": {"name": "Ada"}, "prefs": {}}}
        self.assertEncoding(
            payload,
            "user:\n  profile:\n    name: Ada\n  prefs:",
        )

    def test_numeric_keys_are_quoted(self) -> None:
        payload = {1: "Ada", 2: "Bob"}
        self.assertEncoding(
            payload,
            '"1": Ada\n"2": Bob',
        )

    def test_dataclass_normalisation(self) -> None:
        @dataclass
        class User:
            id: int
            name: str

        self.assertEncoding(User(1, "Ada"), "id: 1\nname: Ada")


class EncodeArraysTest(EncodeTestCase):
    def test_inline_primitive_array(self) -> None:
        payload = {"tags": ["reading", "gaming"]}
        self.assertEncoding(payload, "tags[2]: reading,gaming")

    def test_array_of_arrays(self) -> None:
        payload = {"pairs": [["a", "b"], ["c", "d"]]}
        self.assertEncoding(
            payload,
            "pairs[2]:\n  - [2]: a,b\n  - [2]: c,d",
        )

    def test_tabular_array_of_objects(self) -> None:
        payload = {"items": [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Bob"}]}
        self.assertEncoding(
            payload,
            "items[2]{id,name}:\n  1,Ada\n  2,Bob",
        )

    def test_non_tabular_array_of_objects_falls_back_to_list(self) -> None:
        payload = {"items": [{"id": 1, "name": "Ada"}, {"id": 2, "extra": True}]}
        self.assertEncoding(
            payload,
            "items[2]:\n  - id: 1\n    name: Ada\n  - id: 2\n    extra: true",
        )

    def test_root_array_encoding(self) -> None:
        self.assertEncoding(
            ["x", "true", True],
            '[3]: x,"true",true',
        )


class EncodeOptionsTest(EncodeTestCase):
    def test_custom_delimiters_quote_when_necessary(self) -> None:
        cases = [
            (DELIMITERS["pipe"], {"items": ["a", "b|c", "d"]}, 'items[3|]: a|"b|c"|d'),
            (DELIMITERS["tab"], {"items": ["a", "b\tc", "d"]}, "items[3\t]: a\t\"b\\tc\"\td"),
        ]
        for delimiter, payload, expected in cases:
            with self.subTest(delimiter=repr(delimiter)):
                self.assertEncoding(payload, expected, {"delimiter": delimiter})

    def test_delimiter_preserves_commas_with_tabular_rows(self) -> None:
        payload = {"items": [{"id": 1, "note": "a,b"}, {"id": 2, "note": "c,d"}]}
        self.assertEncoding(
            payload,
            'items[2]{id,note}:\n  1,"a,b"\n  2,"c,d"',
            {"delimiter": DELIMITERS["comma"]},
        )
        self.assertEncoding(
            payload,
            "items[2\t]{id\tnote}:\n  1\ta,b\n  2\tc,d",
            {"delimiter": DELIMITERS["tab"]},
        )

    def test_length_marker_applies_to_nested_arrays(self) -> None:
        payload = {"groups": [["a"], ["b", "c"]]}
        self.assertEncoding(
            payload,
            "groups[#2]:\n  - [#1]: a\n  - [#2]: b,c",
            {"length_marker": "#"},
        )


class NormalizationTest(unittest.TestCase):
    def test_set_normalises_to_list(self) -> None:
        result = normalize_value({"items": {1, 2}})
        self.assertIsInstance(result, dict)
        items = result["items"]
        self.assertCountEqual(items, [1, 2])

    def test_mapping_with_non_string_keys(self) -> None:
        result = normalize_value({1: True, 2.5: False})
        self.assertEqual(result, {"1": True, "2.5": False})

    def test_sequence_types_coerce_to_lists(self) -> None:
        result = normalize_value({"coords": tuple([1, 2, 3])})
        self.assertEqual(result, {"coords": [1, 2, 3]})


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, pattern: str) -> unittest.TestSuite:  # noqa: D401 - required signature
    suite = unittest.TestSuite()
    for test_case in (
        EncodePrimitivesTest,
        EncodeObjectsTest,
        EncodeArraysTest,
        EncodeOptionsTest,
        NormalizationTest,
    ):
        suite.addTests(loader.loadTestsFromTestCase(test_case))
    return suite


if __name__ == "__main__":
    unittest.main()
