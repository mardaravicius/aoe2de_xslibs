import unittest

from xs_converter.functions import (
    xs_set_player_attribute,
    xs_player_attribute,
    xs_get_game_time,
    xs_chat_data,
    xs_array_get_int,
)

from tests.test_xs_converter.helpers import convert


class TestFunctionCalls(unittest.TestCase):

    def test_simple_call(self):
        def f() -> None:
            xs_get_game_time()

        expected = (
            "void f() {\n"
            "    xsGetGameTime();\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_call_with_args(self):
        def f() -> None:
            xs_set_player_attribute(1, 20, 33.3)

        expected = (
            "void f() {\n"
            "    xsSetPlayerAttribute(1, 20, 33.3);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_nested_calls(self):
        def f() -> None:
            xs_set_player_attribute(1, 100, xs_player_attribute(1, 100) + 1.0)

        expected = (
            "void f() {\n"
            "    xsSetPlayerAttribute(1, 100, xsPlayerAttribute(1, 100) + 1.0);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_str_conversion(self):
        def f() -> None:
            x: int = 42
            s: str = str(x)

        expected = (
            "void f() {\n"
            "    int x = 42;\n"
            '    string s = "" + x;\n'
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_float_conversion_from_var(self):
        def f() -> None:
            x: int = 5
            y: float = float(x)

        expected = (
            "void f() {\n"
            "    int x = 5;\n"
            "    float y = 0.0 + x;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_float_conversion_from_constant(self):
        def f() -> None:
            y: float = float(5)

        expected = (
            "void f() {\n"
            "    float y = 5;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_int_conversion_from_var(self):
        def f() -> None:
            x: float = 5.5
            y: int = int(x)

        expected = (
            "void f() {\n"
            "    float x = 5.5;\n"
            "    int y = 0 + x;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_int_conversion_from_constant(self):
        def f() -> None:
            y: int = int(5)

        expected = (
            "void f() {\n"
            "    int y = 5;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_float_conversion_from_neg_constant(self):
        def f() -> None:
            y: float = float(-5)

        expected = (
            "void f() {\n"
            "    float y = -5;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_int_conversion_from_neg_constant(self):
        def f() -> None:
            y: int = int(-5)

        expected = (
            "void f() {\n"
            "    int y = -5;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_len_call(self):
        def f() -> None:
            arr: list[int] = [0] * 10
            n: int = len(arr)

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(10);\n"
            "    int n = xsArrayGetSize(arr);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_len_in_expression(self):
        def f() -> None:
            arr: list[int] = [0] * 10
            n: int = len(arr) - 1

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(10);\n"
            "    int n = xsArrayGetSize(arr) - 1;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_len_in_condition(self):
        def f() -> None:
            arr: list[int] = [0] * 5
            i: int = 0
            if i < len(arr):
                pass

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(5);\n"
            "    int i = 0;\n"
            "    if (i < xsArrayGetSize(arr)) {\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_len_no_indent(self):
        def f() -> None:
            arr: list[int] = [0] * 10
            n: int = len(arr)

        self.assertEqual(
            "void f(){int arr=xsArrayCreateInt(10);int n=xsArrayGetSize(arr);}",
            convert(f, indent=False),
        )


if __name__ == "__main__":
    unittest.main()
