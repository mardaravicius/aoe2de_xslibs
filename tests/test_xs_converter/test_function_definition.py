import unittest

from xs_converter.symbols import xs_rule, xs_ignore
from xs_converter.functions import xs_set_player_attribute, xs_chat_data

from tests.test_xs_converter.helpers import convert


class TestEmptyFunction(unittest.TestCase):

    def test_void_no_args(self):
        def my_func() -> None:
            pass

        expected = (
            "void myFunc() {\n"
            "}\n"
        )
        self.assertEqual(expected, convert(my_func))

    def test_void_no_args_no_indent(self):
        def my_func() -> None:
            pass

        self.assertEqual("void myFunc(){}", convert(my_func, indent=False))


class TestReturnTypes(unittest.TestCase):

    def test_int_return(self):
        def get_value() -> int:
            return 42

        expected = (
            "int getValue() {\n"
            "    return (42);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(get_value))

    def test_float_return(self):
        def get_value() -> float:
            return 1.5

        expected = (
            "float getValue() {\n"
            "    return (1.5);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(get_value))

    def test_bool_return(self):
        def is_ready() -> bool:
            return True

        expected = (
            "bool isReady() {\n"
            "    return (true);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(is_ready))

    def test_str_return(self):
        def get_name() -> str:
            return "hello"

        expected = (
            "string getName() {\n"
            '    return ("hello");\n'
            "}\n"
        )
        self.assertEqual(expected, convert(get_name))


class TestFunctionArguments(unittest.TestCase):

    def test_single_arg(self):
        def add_one(x: int = 0) -> int:
            return x + 1

        expected = (
            "int addOne(int x = 0) {\n"
            "    return (x + 1);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(add_one))

    def test_multiple_args(self):
        def compute(a: int = 0, b: float = 0.0) -> float:
            pass

        expected = (
            "float compute(int a = 0, float b = 0.0) {\n"
            "}\n"
        )
        self.assertEqual(expected, convert(compute))

    def test_bool_default(self):
        def toggle(flag: bool = False) -> None:
            pass

        expected = (
            "void toggle(bool flag = false) {\n"
            "}\n"
        )
        self.assertEqual(expected, convert(toggle))

    def test_string_default(self):
        def greet(name: str = "world") -> None:
            pass

        expected = (
            'void greet(string name = "world") {\n'
            "}\n"
        )
        self.assertEqual(expected, convert(greet))


class TestCamelCaseConversion(unittest.TestCase):

    def test_single_underscore(self):
        def my_func() -> None:
            pass

        expected = (
            "void myFunc() {\n"
            "}\n"
        )
        self.assertEqual(expected, convert(my_func))

    def test_multiple_underscores(self):
        def my_long_function_name() -> None:
            pass

        expected = (
            "void myLongFunctionName() {\n"
            "}\n"
        )
        self.assertEqual(expected, convert(my_long_function_name))

    def test_leading_underscore_preserved(self):
        def _private_func() -> None:
            pass

        expected = (
            "void _privateFunc() {\n"
            "}\n"
        )
        self.assertEqual(expected, convert(_private_func))

    def test_variable_name_camel_case(self):
        def f() -> None:
            my_var: int = 10

        expected = (
            "void f() {\n"
            "    int myVar = 10;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))


class TestMultipleFunctions(unittest.TestCase):

    def test_two_functions(self):
        def first_func() -> None:
            pass

        def second_func() -> None:
            pass

        expected = (
            "void firstFunc() {\n"
            "}\n"
            "\n"
            "void secondFunc() {\n"
            "}\n"
        )
        self.assertEqual(expected, convert(first_func, second_func))

    def test_function_with_rule(self):
        def main_func() -> None:
            xs_chat_data("init")

        @xs_rule(active=True, run_immediately=True)
        def tick() -> None:
            xs_chat_data("tick")

        expected = (
            "void mainFunc() {\n"
            '    xsChatData("init");\n'
            "}\n"
            "\n"
            "rule tick active runImmediately {\n"
            '    xsChatData("tick");\n'
            "}\n"
        )
        self.assertEqual(expected, convert(main_func, tick))


class TestDocstring(unittest.TestCase):

    def test_docstring_is_excluded_from_body(self):
        def f() -> None:
            """This is a docstring."""
            x: int = 1

        expected = (
            "/*\n"
            "    This is a docstring.\n"
            "*/\n"
            "void f() {\n"
            "    int x = 1;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_docstring_as_comment_in_indented_mode(self):
        def f() -> None:
            """My doc."""
            pass

        expected = (
            "/*\n"
            "    My doc.\n"
            "*/\n"
            "void f() {\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))


class TestNoIndentMode(unittest.TestCase):

    def test_if_no_indent(self):
        def f() -> None:
            x: int = 1
            if x > 0:
                xs_chat_data("yes")

        self.assertEqual(
            'void f(){int x=1;if(x>0){xsChatData("yes");}}',
            convert(f, indent=False),
        )

    def test_for_no_indent(self):
        def f() -> None:
            for i in range(5):
                xs_chat_data("hi")

        self.assertEqual(
            'void f(){for(i=0;<5){xsChatData("hi");}}',
            convert(f, indent=False),
        )


class TestXsRule(unittest.TestCase):

    def test_active_rule_with_priority(self):
        @xs_rule(active=True, high_frequency=False, priority=21, min_interval=1, max_interval=2)
        def my_rule() -> None:
            xs_set_player_attribute(1, 20, 33.3)

        expected = (
            "rule myRule active minInterval 1 maxInterval 2 priority 21 {\n"
            "    xsSetPlayerAttribute(1, 20, 33.3);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(my_rule, root_flags=[False]))

    def test_inactive_rule(self):
        @xs_rule()
        def idle_rule() -> None:
            pass

        expected = (
            "rule idleRule inactive {\n"
            "}\n"
        )
        self.assertEqual(expected, convert(idle_rule, root_flags=[False]))

    def test_high_frequency_rule(self):
        @xs_rule(active=True, high_frequency=True)
        def fast_rule() -> None:
            pass

        expected = (
            "rule fastRule active highFrequency {\n"
            "}\n"
        )
        self.assertEqual(expected, convert(fast_rule, root_flags=[False]))

    def test_run_immediately_rule(self):
        @xs_rule(active=True, run_immediately=True)
        def init_rule() -> None:
            pass

        expected = (
            "rule initRule active runImmediately {\n"
            "}\n"
        )
        self.assertEqual(expected, convert(init_rule, root_flags=[False]))

    def test_rule_with_group(self):
        @xs_rule(group="myGroup", active=True)
        def grouped_rule() -> None:
            pass

        expected = (
            "rule groupedRule group myGroup active {\n"
            "}\n"
        )
        self.assertEqual(expected, convert(grouped_rule, root_flags=[False]))


class TestXsIgnore(unittest.TestCase):

    def test_xs_ignore_single_function(self):
        @xs_ignore
        def skipped() -> None:
            pass

        self.assertEqual("", convert(skipped))

    def test_xs_ignore_in_multiple_functions(self):
        def kept() -> None:
            pass

        @xs_ignore
        def skipped() -> None:
            pass

        def also_kept() -> int:
            return 1

        expected = (
            "void kept() {\n"
            "}\n"
            "\n"
            "int alsoKept() {\n"
            "    return (1);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(kept, skipped, also_kept))


if __name__ == "__main__":
    unittest.main()
