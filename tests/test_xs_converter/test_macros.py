import unittest

from xs_converter.functions import xs_set_player_attribute
from xs_converter.macro import macro_pass_value, macro_repeat_with_iterable

from tests.test_xs_converter.helpers import convert


class TestMacros(unittest.TestCase):

    def test_macro_replaces_variable(self):
        def f() -> None:
            x: int = macro_pass_value("my_val", int)

        expected = (
            "void f() {\n"
            "    int x = 42;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f, my_val=42))

    def test_macro_with_string_value(self):
        def f() -> None:
            x: str = macro_pass_value("msg", str)

        expected = (
            "void f() {\n"
            '    string x = "hello";\n'
            "}\n"
        )
        self.assertEqual(expected, convert(f, msg="hello"))

    def test_repeat_with_iterable(self):
        def f() -> None:
            with macro_repeat_with_iterable("players", tuple[int, int]) as (player_number, res):
                xs_set_player_attribute(player_number, 100, res)

        expected = (
            "void f() {\n"
            "    xsSetPlayerAttribute(1, 100, 10.0);\n"
            "    xsSetPlayerAttribute(2, 100, 20.0);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f, players=[(1, 10.0), (2, 20.0)]))


if __name__ == "__main__":
    unittest.main()
