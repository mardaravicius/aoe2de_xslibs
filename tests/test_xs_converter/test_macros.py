import unittest

from xs_converter.functions import xs_set_player_attribute
from xs_converter.macro import macro_bindings, macro_pass_value, macro_repeat

from tests.test_xs_converter.helpers import convert


class TestMacros(unittest.TestCase):

    def test_macro_replaces_variable(self):
        def f() -> None:
            x: int = macro_pass_value("my_val")

        expected = (
            "void f() {\n"
            "    int x = 42;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f, my_val=42))

    def test_macro_with_string_value(self):
        def f() -> None:
            x: str = macro_pass_value("msg")

        expected = (
            "void f() {\n"
            '    string x = "hello";\n'
            "}\n"
        )
        self.assertEqual(expected, convert(f, msg="hello"))

    def test_repeat_macro_unrolls_for_loop(self):
        def f() -> None:
            for player_number, res in macro_repeat("players"):
                xs_set_player_attribute(player_number, 100, res)

        expected = (
            "void f() {\n"
            "    xsSetPlayerAttribute(1, 100, 10.0);\n"
            "    xsSetPlayerAttribute(2, 100, 20.0);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f, players=[(1, 10.0), (2, 20.0)]))

    def test_runtime_macro_pass_value_uses_bound_value(self):
        with macro_bindings(my_val=42):
            self.assertEqual(42, macro_pass_value("my_val"))

    def test_runtime_macro_bindings_accept_mapping(self):
        with macro_bindings({"my_val": 42}):
            self.assertEqual(42, macro_pass_value("my_val"))

    def test_runtime_macro_repeat_uses_bound_iterable(self):
        with macro_bindings(players=[(1, 10.0), (2, 20.0)]):
            self.assertEqual([(1, 10.0), (2, 20.0)], list(macro_repeat("players")))

    def test_runtime_macro_bindings_nest(self):
        with macro_bindings(my_val=1):
            self.assertEqual(1, macro_pass_value("my_val"))
            with macro_bindings(my_val=2):
                self.assertEqual(2, macro_pass_value("my_val"))
            self.assertEqual(1, macro_pass_value("my_val"))

    def test_runtime_macro_pass_value_requires_bound_name(self):
        with macro_bindings(other=42):
            with self.assertRaisesRegex(KeyError, "not bound"):
                macro_pass_value("my_val")

    def test_runtime_macro_repeat_requires_iterable(self):
        with macro_bindings(players=1):
            with self.assertRaisesRegex(TypeError, "expected an iterable"):
                list(macro_repeat("players"))

if __name__ == "__main__":
    unittest.main()
