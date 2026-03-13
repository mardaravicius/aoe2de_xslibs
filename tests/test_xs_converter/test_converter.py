import ast
import inspect
import textwrap
import unittest

from xs_converter.constants import XsConstants
from xs_converter.converter import PythonToXsConverter, XsContext
from xs_converter.functions import (
    vector,
    xs_set_player_attribute,
    xs_player_attribute,
    xs_get_game_time,
    xs_effect_amount,
    xs_get_player_civilization,
    xs_chat_data,
    xs_array_get_int,
)
from xs_converter.macro import macro_pass_value, macro_repeat_with_iterable
from xs_converter.symbols import XsConst, XsStatic, XsExtern, XsExternConst, XsVector, xs_rule
from numpy import int32, float32
from typing import List


def _parse_dedented(fn):
    source = textwrap.dedent(inspect.getsource(fn))
    module = ast.parse(source)
    assert len(module.body) == 1 and isinstance(module.body[0], ast.FunctionDef)
    return module.body[0]


def _convert(*functions, indent=True, root_flags=None, **kwargs) -> str:
    """Convert one or more Python functions to XS script.

    By default the first function is treated as root (matching to_xs_script
    behaviour).  Override per-function with ``root_flags``.
    """
    xs = ""
    for i, fn in enumerate(functions):
        root = (i == 0) if root_flags is None else root_flags[i]
        converter = PythonToXsConverter(indent, kwargs)
        fn_ast = _parse_dedented(fn)
        xs += converter.to_xs_function_definition(fn_ast, XsContext(), root)
        if i < len(functions) - 1:
            xs += converter.nl
    return xs


class TestEmptyFunction(unittest.TestCase):

    def test_void_no_args(self):
        def my_func() -> None:
            pass

        expected = (
            "void myFunc() {\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(my_func))

    def test_void_no_args_no_indent(self):
        def my_func() -> None:
            pass

        self.assertEqual("void myFunc(){}", _convert(my_func, indent=False))


class TestReturnTypes(unittest.TestCase):

    def test_int_return(self):
        def get_value() -> int:
            return 42

        expected = (
            "int getValue() {\n"
            "    return (42);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(get_value))

    def test_float_return(self):
        def get_value() -> float:
            return 1.5

        expected = (
            "float getValue() {\n"
            "    return (1.5);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(get_value))

    def test_bool_return(self):
        def is_ready() -> bool:
            return True

        expected = (
            "bool isReady() {\n"
            "    return (true);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(is_ready))

    def test_str_return(self):
        def get_name() -> str:
            return "hello"

        expected = (
            "string getName() {\n"
            '    return ("hello");\n'
            "}\n"
        )
        self.assertEqual(expected, _convert(get_name))


class TestFunctionArguments(unittest.TestCase):

    def test_single_arg(self):
        def add_one(x: int = 0) -> int:
            return x + 1

        expected = (
            "int addOne(int x = 0) {\n"
            "    return (x + 1);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(add_one))

    def test_multiple_args(self):
        def compute(a: int = 0, b: float = 0.0) -> float:
            pass

        expected = (
            "float compute(int a = 0, float b = 0.0) {\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(compute))

    def test_bool_default(self):
        def toggle(flag: bool = False) -> None:
            pass

        expected = (
            "void toggle(bool flag = false) {\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(toggle))

    def test_string_default(self):
        def greet(name: str = "world") -> None:
            pass

        expected = (
            'void greet(string name = "world") {\n'
            "}\n"
        )
        self.assertEqual(expected, _convert(greet))


class TestCamelCaseConversion(unittest.TestCase):

    def test_single_underscore(self):
        def my_func() -> None:
            pass

        expected = (
            "void myFunc() {\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(my_func))

    def test_multiple_underscores(self):
        def my_long_function_name() -> None:
            pass

        expected = (
            "void myLongFunctionName() {\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(my_long_function_name))

    def test_leading_underscore_preserved(self):
        def _private_func() -> None:
            pass

        expected = (
            "void _privateFunc() {\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(_private_func))

    def test_variable_name_camel_case(self):
        def f() -> None:
            my_var: int = 10

        expected = (
            "void f() {\n"
            "    int myVar = 10;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestVariableDefinitions(unittest.TestCase):

    def test_int_var(self):
        def f() -> None:
            x: int = 42

        expected = (
            "void f() {\n"
            "    int x = 42;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_float_var(self):
        def f() -> None:
            x: float = 3.14

        expected = (
            "void f() {\n"
            "    float x = 3.14;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_bool_var(self):
        def f() -> None:
            flag: bool = True

        expected = (
            "void f() {\n"
            "    bool flag = true;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_string_var(self):
        def f() -> None:
            msg: str = "hello"

        expected = (
            "void f() {\n"
            '    string msg = "hello";\n'
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_vector_var(self):
        def f() -> None:
            v: XsVector = vector(1.0, 2.0, 3.0)

        expected = (
            "void f() {\n"
            "    vector v = vector(1.0, 2.0, 3.0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_const_modifier(self):
        def f() -> None:
            x: XsConst[int] = 99

        expected = (
            "void f() {\n"
            "    const int x = 99;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_static_modifier(self):
        def f() -> None:
            x: XsStatic[int] = 0

        expected = (
            "void f() {\n"
            "    static int x = 0;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_extern_modifier(self):
        def f() -> None:
            x: XsExtern[int] = 0

        expected = (
            "void f() {\n"
            "    extern int x = 0;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_extern_const_modifier(self):
        def f() -> None:
            x: XsExternConst[int] = 0

        expected = (
            "void f() {\n"
            "    extern const int x = 0;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestVariableAssignment(unittest.TestCase):

    def test_reassignment(self):
        def f() -> None:
            x: int = 0
            x = 5

        expected = (
            "void f() {\n"
            "    int x = 0;\n"
            "    x = 5;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestAugmentedAssignment(unittest.TestCase):

    def test_increment_by_one(self):
        def f() -> None:
            x: int = 0
            x += 1

        expected = (
            "void f() {\n"
            "    int x = 0;\n"
            "    x++;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_decrement_by_one(self):
        def f() -> None:
            x: int = 5
            x -= 1

        expected = (
            "void f() {\n"
            "    int x = 5;\n"
            "    x--;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_add_more_than_one(self):
        def f() -> None:
            x: int = 0
            x += 10

        expected = (
            "void f() {\n"
            "    int x = 0;\n"
            "    x = x + 10;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_subtract_more_than_one(self):
        def f() -> None:
            x: int = 10
            x -= 3

        expected = (
            "void f() {\n"
            "    int x = 10;\n"
            "    x = x - 3;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_multiply_assign(self):
        def f() -> None:
            x: int = 2
            x *= 5

        expected = (
            "void f() {\n"
            "    int x = 2;\n"
            "    x = x * 5;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


    def test_div_assign(self):
        def f() -> None:
            x: int = 2
            x //= 5

        expected = (
            "void f() {\n"
            "    int x = 2;\n"
            "    x = x / 5;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestConstants(unittest.TestCase):

    def test_large_int(self):
        def f() -> None:
            x: int = 1_500_000_021

        expected = (
            "void f() {\n"
            "    int x = 150000002 * 10 + 1;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_large_negative_int(self):
        def f() -> None:
            x: int = -1_500_000_021

        expected = (
            "void f() {\n"
            "    int x = -150000002 * 10 - 1;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_max_int(self):
        def f() -> None:
            x: int = 2_147_483_647

        expected = (
            "void f() {\n"
            "    int x = 214748364 * 10 + 7;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_min_int(self):
        def f() -> None:
            x: int = -2_147_483_648

        expected = (
            "void f() {\n"
            "    int x = -214748364 * 10 - 8;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_int_overflow_raises(self):
        def f() -> None:
            x: int = 2_147_483_648

        with self.assertRaises(ValueError):
            _convert(f)

    def test_int_underflow_raises(self):
        def f() -> None:
            x: int = -2_147_483_649

        with self.assertRaises(ValueError):
            _convert(f)

    def test_string_with_quotes(self):
        def f() -> None:
            x: str = 'he said "hi"'

        expected = (
            "void f() {\n"
            '    string x = "he said \\"hi\\"";\n'
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_false_constant(self):
        def f() -> None:
            x: bool = False

        expected = (
            "void f() {\n"
            "    bool x = false;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestBinaryExpressions(unittest.TestCase):

    def test_addition(self):
        def f() -> int:
            return 1 + 2

        expected = (
            "int f() {\n"
            "    return (1 + 2);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_subtraction(self):
        def f() -> int:
            return 5 - 3

        expected = (
            "int f() {\n"
            "    return (5 - 3);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_multiplication(self):
        def f() -> int:
            return 2 * 3

        expected = (
            "int f() {\n"
            "    return (2 * 3);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_division(self):
        def f() -> float:
            return 10.0 / 3.0

        expected = (
            "float f() {\n"
            "    return (10.0 / 3.0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_floor_division(self):
        def f() -> int:
            return 10 // 3

        expected = (
            "int f() {\n"
            "    return (10 / 3);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_modulo(self):
        def f() -> int:
            return 10 % 3

        expected = (
            "int f() {\n"
            "    return (10 % 3);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_nested_binary_ops(self):
        def f() -> None:
            x: float = 2.2 * 12.45 + 1.1

        expected = (
            "void f() {\n"
            "    float x = (2.2 * 12.45) + 1.1;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestComparisonExpressions(unittest.TestCase):

    def test_equal(self):
        def f() -> None:
            x: int = 1
            if x == 2:
                pass

        expected = (
            "void f() {\n"
            "    int x = 1;\n"
            "    if (x == 2) {\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_not_equal(self):
        def f() -> None:
            x: int = 1
            if x != 2:
                pass

        expected = (
            "void f() {\n"
            "    int x = 1;\n"
            "    if (x != 2) {\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_greater_than(self):
        def f() -> None:
            x: int = 1
            if x > 0:
                pass

        expected = (
            "void f() {\n"
            "    int x = 1;\n"
            "    if (x > 0) {\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_greater_equal(self):
        def f() -> None:
            x: int = 1
            if x >= 0:
                pass

        expected = (
            "void f() {\n"
            "    int x = 1;\n"
            "    if (x >= 0) {\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_less_than(self):
        def f() -> None:
            x: int = 1
            if x < 10:
                pass

        expected = (
            "void f() {\n"
            "    int x = 1;\n"
            "    if (x < 10) {\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_less_equal(self):
        def f() -> None:
            x: int = 1
            if x <= 10:
                pass

        expected = (
            "void f() {\n"
            "    int x = 1;\n"
            "    if (x <= 10) {\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestUnaryExpressions(unittest.TestCase):

    def test_negative_constant(self):
        def f() -> None:
            x: int = -5

        expected = (
            "void f() {\n"
            "    int x = -5;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_not_operator(self):
        def f() -> None:
            x: bool = True
            if not x:
                pass

        expected = (
            "void f() {\n"
            "    bool x = true;\n"
            "    if (x == false) {\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestBoolOperations(unittest.TestCase):

    def test_or(self):
        def f() -> None:
            x: bool = True
            y: bool = False
            if x or y:
                pass

        expected = (
            "void f() {\n"
            "    bool x = true;\n"
            "    bool y = false;\n"
            "    if (x || y) {\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_and(self):
        def f() -> None:
            x: bool = True
            y: bool = False
            if x and y:
                pass

        expected = (
            "void f() {\n"
            "    bool x = true;\n"
            "    bool y = false;\n"
            "    if (x && y) {\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestFunctionCalls(unittest.TestCase):

    def test_simple_call(self):
        def f() -> None:
            xs_get_game_time()

        expected = (
            "void f() {\n"
            "    xsGetGameTime();\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_call_with_args(self):
        def f() -> None:
            xs_set_player_attribute(1, 20, 33.3)

        expected = (
            "void f() {\n"
            "    xsSetPlayerAttribute(1, 20, 33.3);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_nested_calls(self):
        def f() -> None:
            xs_set_player_attribute(1, 100, xs_player_attribute(1, 100) + 1.0)

        expected = (
            "void f() {\n"
            "    xsSetPlayerAttribute(1, 100, xsPlayerAttribute(1, 100) + 1.0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

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
        self.assertEqual(expected, _convert(f))

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
        self.assertEqual(expected, _convert(f))

    def test_float_conversion_from_constant(self):
        def f() -> None:
            y: float = float(5)

        expected = (
            "void f() {\n"
            "    float y = 5;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

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
        self.assertEqual(expected, _convert(f))

    def test_int_conversion_from_constant(self):
        def f() -> None:
            y: int = int(5)

        expected = (
            "void f() {\n"
            "    int y = 5;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_float_conversion_from_neg_constant(self):
        def f() -> None:
            y: float = float(-5)

        expected = (
            "void f() {\n"
            "    float y = -5;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_int_conversion_from_neg_constant(self):
        def f() -> None:
            y: int = int(-5)

        expected = (
            "void f() {\n"
            "    int y = -5;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestIfElse(unittest.TestCase):

    def test_simple_if(self):
        def f() -> None:
            x: int = 1
            if x > 0:
                xs_chat_data("positive")

        expected = (
            "void f() {\n"
            "    int x = 1;\n"
            "    if (x > 0) {\n"
            '        xsChatData("positive");\n'
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_if_else(self):
        def f() -> None:
            x: int = 1
            if x > 0:
                xs_chat_data("positive")
            else:
                xs_chat_data("non-positive")

        expected = (
            "void f() {\n"
            "    int x = 1;\n"
            "    if (x > 0) {\n"
            '        xsChatData("positive");\n'
            "    } else {\n"
            '        xsChatData("non-positive");\n'
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_if_elif_else(self):
        def f() -> None:
            x: int = 1
            if x > 0:
                xs_chat_data("positive")
            elif x == 0:
                xs_chat_data("zero")
            else:
                xs_chat_data("negative")

        expected = (
            "void f() {\n"
            "    int x = 1;\n"
            "    if (x > 0) {\n"
            '        xsChatData("positive");\n'
            "    } else if (x == 0) {\n"
            '        xsChatData("zero");\n'
            "    } else {\n"
            '        xsChatData("negative");\n'
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_if_with_pass_in_else(self):
        def f() -> None:
            x: int = 1
            if x > 0:
                xs_chat_data("yes")
            else:
                pass

        expected = (
            "void f() {\n"
            "    int x = 1;\n"
            "    if (x > 0) {\n"
            '        xsChatData("yes");\n'
            "    } else {\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestForLoops(unittest.TestCase):

    def test_range_one_arg(self):
        def f() -> None:
            for i in range(10):
                xs_chat_data("hi")

        expected = (
            "void f() {\n"
            "    for (i = 0; < 10) {\n"
            '        xsChatData("hi");\n'
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_range_two_args(self):
        def f() -> None:
            for p in range(3, 9):
                xs_effect_amount(0, 1, 2, 40.0, p)

        expected = (
            "void f() {\n"
            "    for (p = 3; < 9) {\n"
            "        xsEffectAmount(0, 1, 2, 40.0, p);\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_range_with_plus_one_bound(self):
        def f() -> None:
            n: int = 5
            for i in range(0, n + 1):
                xs_chat_data("hi")

        expected = (
            "void f() {\n"
            "    int n = 5;\n"
            "    for (i = 0; <= n) {\n"
            '        xsChatData("hi");\n'
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_range_step_minus_one(self):
        def f() -> None:
            for i in range(9, 3, -1):
                xs_chat_data("hi")

        expected = (
            "void f() {\n"
            "    for (i = 9; > 3) {\n"
            '        xsChatData("hi");\n'
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_range_step_minus_one_with_sub_bound(self):
        def f() -> None:
            to: int = 2
            for p2 in range(9, to - 1, -1):
                xs_chat_data("hi")

        expected = (
            "void f() {\n"
            "    int to = 2;\n"
            "    for (p2 = 9; >= to) {\n"
            '        xsChatData("hi");\n'
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_range_step_positive_not_one(self):
        def f() -> None:
            for i in range(0, 20, 5):
                xs_chat_data("hi")

        expected = (
            "void f() {\n"
            "    int i = 0;\n"
            "    while (i < 20) {\n"
            '        xsChatData("hi");\n'
            "        i = i + 5;\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_range_step_negative_not_one(self):
        def f() -> None:
            to: int = 2
            for p2 in range(9, to - 1, -2):
                xs_chat_data("hi")

        expected = (
            "void f() {\n"
            "    int to = 2;\n"
            "    int p2 = 9;\n"
            "    while (p2 >= to) {\n"
            '        xsChatData("hi");\n'
            "        p2 = p2 - 2;\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_range_for_only_expressions(self):
        def f() -> None:
            a: int = 1
            b: int = 2
            c: int = 3
            d: int = 4
            for i in range(a + b, c + d):
                xs_chat_data("hi")

        expected = (
            "void f() {\n"
            "    int a = 1;\n"
            "    int b = 2;\n"
            "    int c = 3;\n"
            "    int d = 4;\n"
            "    for (i = a + b; < c + d) {\n"
            '        xsChatData("hi");\n'
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_range_all_expressions(self):
        def f() -> None:
            a: int = 1
            b: int = 2
            c: int = 3
            d: int = 4
            e: int = 5
            f: int = 6
            for i in range(a + b, c + d, e + f):
                xs_chat_data("hi")

        expected = (
            "void f() {\n"
            "    int a = 1;\n"
            "    int b = 2;\n"
            "    int c = 3;\n"
            "    int d = 4;\n"
            "    int e = 5;\n"
            "    int f = 6;\n"
            "    int i = a + b;\n"
            "    while (i < (c + d)) {\n"
            '        xsChatData("hi");\n'
            "        i = i + (e + f);\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestWhileLoop(unittest.TestCase):

    def test_simple_while(self):
        def f() -> None:
            while xs_get_game_time() > 1000:
                xs_set_player_attribute(3, 422, xs_player_attribute(3, 422) + 10.0)

        expected = (
            "void f() {\n"
            "    while (xsGetGameTime() > 1000) {\n"
            "        xsSetPlayerAttribute(3, 422, xsPlayerAttribute(3, 422) + 10.0);\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestMatchCase(unittest.TestCase):

    def test_switch_with_default(self):
        def f() -> None:
            match xs_get_player_civilization(4):
                case 1:
                    return
                case _:
                    xs_chat_data("other")

        expected = (
            "void f() {\n"
            "    switch (xsGetPlayerCivilization(4)) {\n"
            "        case 1: {\n"
            "            return;\n"
            "        }\n"
            "        default: {\n"
            '            xsChatData("other");\n'
            "        }\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_switch_with_xs_constants(self):
        def f() -> None:
            match xs_get_player_civilization(4):
                case XsConstants.c_britons:
                    xs_effect_amount(XsConstants.c_set_attribute, 101, XsConstants.c_attack, 123.0, 4)

        expected = (
            "void f() {\n"
            "    switch (xsGetPlayerCivilization(4)) {\n"
            "        case cBritons: {\n"
            "            xsEffectAmount(cSetAttribute, 101, cAttack, 123.0, 4);\n"
            "        }\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestReturn(unittest.TestCase):

    def test_return_void(self):
        def f() -> None:
            return

        expected = (
            "void f() {\n"
            "    return;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_return_value(self):
        def f() -> int:
            return 42

        expected = (
            "int f() {\n"
            "    return (42);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_return_expression(self):
        def f(x: int = 0) -> int:
            return x + 1

        expected = (
            "int f(int x = 0) {\n"
            "    return (x + 1);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestFStrings(unittest.TestCase):

    def test_fstring_concatenation(self):
        def f() -> None:
            x: int = 10
            s: str = f"value={x}"

        expected = (
            "void f() {\n"
            "    int x = 10;\n"
            '    string s = ("value=" + x);\n'
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestXsConstants(unittest.TestCase):

    def test_xs_constant_in_call(self):
        def f() -> None:
            xs_effect_amount(XsConstants.c_set_attribute, 101, XsConstants.c_attack, 10.0, 1)

        expected = (
            "void f() {\n"
            "    xsEffectAmount(cSetAttribute, 101, cAttack, 10.0, 1);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


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
        self.assertEqual(expected, _convert(my_rule, root_flags=[False]))

    def test_inactive_rule(self):
        @xs_rule()
        def idle_rule() -> None:
            pass

        expected = (
            "rule idleRule inactive {\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(idle_rule, root_flags=[False]))

    def test_high_frequency_rule(self):
        @xs_rule(active=True, high_frequency=True)
        def fast_rule() -> None:
            pass

        # high_frequency=True always raises because the converter's rule_settings
        # dict always contains min_interval/max_interval keys (even when None).
        with self.assertRaises(ValueError):
            _convert(fast_rule, root_flags=[False])

    def test_run_immediately_rule(self):
        @xs_rule(active=True, run_immediately=True)
        def init_rule() -> None:
            pass

        expected = (
            "rule initRule active runImmediately {\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(init_rule, root_flags=[False]))

    def test_rule_with_group(self):
        @xs_rule(group="myGroup", active=True)
        def grouped_rule() -> None:
            pass

        expected = (
            "rule groupedRule group myGroup active {\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(grouped_rule, root_flags=[False]))


class TestMacroPassValue(unittest.TestCase):

    def test_macro_replaces_variable(self):
        def f() -> None:
            x: int = macro_pass_value("my_val", int)

        expected = (
            "void f() {\n"
            "    int x = 42;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f, my_val=42))

    def test_macro_with_string_value(self):
        def f() -> None:
            x: str = macro_pass_value("msg", str)

        expected = (
            "void f() {\n"
            '    string x = "hello";\n'
            "}\n"
        )
        self.assertEqual(expected, _convert(f, msg="hello"))


class TestMacroRepeat(unittest.TestCase):

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
        self.assertEqual(expected, _convert(f, players=[(1, 10.0), (2, 20.0)]))


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
        self.assertEqual(expected, _convert(first_func, second_func))

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
        self.assertEqual(expected, _convert(main_func, tick))


class TestNoIndentMode(unittest.TestCase):

    def test_if_no_indent(self):
        def f() -> None:
            x: int = 1
            if x > 0:
                xs_chat_data("yes")

        self.assertEqual(
            'void f(){int x=1;if(x>0){xsChatData("yes");}}',
            _convert(f, indent=False),
        )

    def test_for_no_indent(self):
        def f() -> None:
            for i in range(5):
                xs_chat_data("hi")

        self.assertEqual(
            'void f(){for(i=0;<5){xsChatData("hi");}}',
            _convert(f, indent=False),
        )


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
        self.assertEqual(expected, _convert(f))

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
        self.assertEqual(expected, _convert(f))


class IntegrationTest(unittest.TestCase):
    def test_full_function_converts(self):
        def xs_test_function() -> None:
            c_integer_var: XsConst[int] = 123
            static_integer_var: XsStatic[int] = 123
            float_var: float = 2.2 * 12.45 + 1.1
            ff: float = float_var
            string_var: str = "hello xs" + "asd"
            bool_var: bool = True
            vec: XsVector = vector(1.1, 2.2, 3.3)
            resource_1: int = macro_pass_value("resource1", int)
            resource_2: int = 411
            long_int: int = -2_147_483_648
            s: str = f"{long_int=}, {ff=}, {bool_var=}, {string_var=}, {vec=}"

            with macro_repeat_with_iterable("players", tuple[int, int]) as (player_number, res):
                xs_set_player_attribute(player_number, resource_2, res)

            xs_set_player_attribute(1, resource_1, xs_player_attribute(1, resource_1) + 1.0)

            if 0 < xs_get_game_time():
                return
            if xs_player_attribute(2, resource_2) > 10:
                xs_set_player_attribute(2, resource_2, 10.0)
            elif xs_player_attribute(2, resource_2) == 0:
                xs_set_player_attribute(2, resource_2, 1.0)
            else:
                pass

            for p in range(3, 9):
                xs_effect_amount(0, 1, 2, 40.0, p)

            to: int = 2
            for p2 in range(9, to - 1, -2):
                xs_effect_amount(0, 1, 2, 40.0, p2)

            while xs_get_game_time() > 1000:
                xs_set_player_attribute(3, 422, xs_player_attribute(3, 422) + 10.0)

            match xs_get_player_civilization(4):
                case 1:
                    return
                case XsConstants.c_britons:
                    xs_effect_amount(XsConstants.c_set_attribute, 101, XsConstants.c_attack, 123.0, 4)
                case _:
                    xs_effect_amount(XsConstants.c_set_attribute, 101, XsConstants.c_attack, 456.0, 4)

            so: int = 3

        expected = (
            "void xsTestFunction() {\n"
            "    const int cIntegerVar = 123;\n"
            "    static int staticIntegerVar = 123;\n"
            "    float floatVar = (2.2 * 12.45) + 1.1;\n"
            "    float ff = floatVar;\n"
            '    string stringVar = "hello xs" + "asd";\n'
            "    bool boolVar = true;\n"
            "    vector vec = vector(1.1, 2.2, 3.3);\n"
            "    int resource1 = 400;\n"
            "    int resource2 = 411;\n"
            "    int longInt = -214748364 * 10 - 8;\n"
            '    string s = ("long_int=" + longInt + ", ff=" + ff + ", bool_var=" + boolVar + ", string_var=" + stringVar + ", vec=" + vec);\n'
            "    xsSetPlayerAttribute(1, resource2, 40.0);\n"
            "    xsSetPlayerAttribute(2, resource2, 41.0);\n"
            "    xsSetPlayerAttribute(3, resource2, 42.0);\n"
            "    xsSetPlayerAttribute(5, resource2, 43.0);\n"
            "    xsSetPlayerAttribute(8, resource2, 44.0);\n"
            "    xsSetPlayerAttribute(1, resource1, xsPlayerAttribute(1, resource1) + 1.0);\n"
            "    if (0 < xsGetGameTime()) {\n"
            "        return;\n"
            "    }\n"
            "    if (xsPlayerAttribute(2, resource2) > 10) {\n"
            "        xsSetPlayerAttribute(2, resource2, 10.0);\n"
            "    } else if (xsPlayerAttribute(2, resource2) == 0) {\n"
            "        xsSetPlayerAttribute(2, resource2, 1.0);\n"
            "    } else {\n"
            "    }\n"
            "    for (p = 3; < 9) {\n"
            "        xsEffectAmount(0, 1, 2, 40.0, p);\n"
            "    }\n"
            "    int to = 2;\n"
            "    int p2 = 9;\n"
            "    while (p2 >= to) {\n"
            "        xsEffectAmount(0, 1, 2, 40.0, p2);\n"
            "        p2 = p2 - 2;\n"
            "    }\n"
            "    while (xsGetGameTime() > 1000) {\n"
            "        xsSetPlayerAttribute(3, 422, xsPlayerAttribute(3, 422) + 10.0);\n"
            "    }\n"
            "    switch (xsGetPlayerCivilization(4)) {\n"
            "        case 1: {\n"
            "            return;\n"
            "        }\n"
            "        case cBritons: {\n"
            "            xsEffectAmount(cSetAttribute, 101, cAttack, 123.0, 4);\n"
            "        }\n"
            "        default: {\n"
            "            xsEffectAmount(cSetAttribute, 101, cAttack, 456.0, 4);\n"
            "        }\n"
            "    }\n"
            "    int so = 3;\n"
            "}\n"
        )
        self.assertEqual(
            expected,
            _convert(
                xs_test_function,
                resource1=400,
                players=[(1, 40.0), (2, 41.0), (3, 42.0), (5, 43.0), (8, 44.0)],
            ),
        )


class TestInt32Float32(unittest.TestCase):

    def test_int32_variable(self):
        def f() -> None:
            x: int32 = 7

        expected = (
            "void f() {\n"
            "    int x = 7;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_float32_variable(self):
        def f() -> None:
            x: float32 = 1.5

        expected = (
            "void f() {\n"
            "    float x = 1.5;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_int32_return_type(self):
        def f() -> int32:
            return 0

        expected = (
            "int f() {\n"
            "    return (0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_float32_return_type(self):
        def f() -> float32:
            return 0.0

        expected = (
            "float f() {\n"
            "    return (0.0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_int32_cast_from_var(self):
        def f() -> None:
            x: float = 5.5
            y: int = int32(x)

        expected = (
            "void f() {\n"
            "    float x = 5.5;\n"
            "    int y = 0 + x;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_float32_cast_from_var(self):
        def f() -> None:
            x: int = 5
            y: float = float32(x)

        expected = (
            "void f() {\n"
            "    int x = 5;\n"
            "    float y = 0.0 + x;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_int32_cast_from_constant(self):
        def f() -> None:
            y: int = int32(42)

        expected = (
            "void f() {\n"
            "    int y = 42;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_float32_cast_from_constant(self):
        def f() -> None:
            y: float = float32(3.14)

        expected = (
            "void f() {\n"
            "    float y = 3.14;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestArrayDefinitions(unittest.TestCase):

    def test_int_array_nonzero_default(self):
        def f() -> None:
            arr: list[int] = [1] * 10

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(10, 1);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_int_array_zero_default_omitted(self):
        def f() -> None:
            arr: list[int] = [0] * 10

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(10);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_int_array_negative_default(self):
        def f() -> None:
            arr: list[int] = [-1] * 5

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(5, -1);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_int32_array(self):
        def f() -> None:
            arr: list[int32] = [5] * 20

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(20, 5);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_list_uppercase_int(self):
        def f() -> None:
            arr: List[int] = [1] * 10

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(10, 1);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_list_uppercase_int32(self):
        def f() -> None:
            arr: List[int32] = [3] * 5

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(5, 3);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_float_array_nonzero_default(self):
        def f() -> None:
            arr: list[float] = [1.5] * 10

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateFloat(10, 1.5);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_float_array_zero_default_omitted(self):
        def f() -> None:
            arr: list[float] = [0.0] * 10

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateFloat(10);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_float32_array(self):
        def f() -> None:
            arr: list[float32] = [2.5] * 8

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateFloat(8, 2.5);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_bool_array_true_default(self):
        def f() -> None:
            arr: list[bool] = [True] * 10

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateBool(10, true);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_bool_array_false_default_omitted(self):
        def f() -> None:
            arr: list[bool] = [False] * 10

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateBool(10);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_str_array_nonempty_default(self):
        def f() -> None:
            arr: list[str] = ["hello"] * 10

        expected = (
            "void f() {\n"
            '    int arr = xsArrayCreateString(10, "hello");\n'
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_str_array_empty_default_omitted(self):
        def f() -> None:
            arr: list[str] = [""] * 10

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateString(10);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_vector_array(self):
        def f() -> None:
            arr: list[XsVector] = [vector(1.0, 2.0, 3.0)] * 5

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateVector(5, vector(1.0, 2.0, 3.0));\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_vector_array_zero_default_omitted(self):
        def f() -> None:
            arr: list[XsVector] = [vector(0.0, 0.0, 0.0)] * 5

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateVector(5);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_array_with_variable_size(self):
        def f() -> None:
            n: int = 10
            arr: list[int] = [0] * n

        expected = (
            "void f() {\n"
            "    int n = 10;\n"
            "    int arr = xsArrayCreateInt(n);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_empty_list_raises(self):
        def f() -> None:
            arr: list[int] = []

        with self.assertRaises(ValueError):
            _convert(f)

    def test_array_creation_in_expression(self):
        def f() -> None:
            xs_array_get_int([10] * 10, 0)

        expected = (
            "void f() {\n"
            "    xsArrayGetInt(xsArrayCreateInt(10, 10), 0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_int32_cast_in_array(self):
        def f() -> None:
            arr: list[int] = [int32(10)] * int32(10)

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(10, 10);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_float32_cast_in_array(self):
        def f() -> None:
            arr: list[float] = [float32(1.5)] * 8

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateFloat(8, 1.5);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_variable_default_raises(self):
        def f() -> None:
            x: int = 5
            arr: list[int] = [x] * 10

        with self.assertRaises(ValueError):
            _convert(f)

    def test_size_is_variable(self):
        def f() -> None:
            x: int = 5
            arr: list[int] = [10] * x

        expected = (
            "void f() {\n"
            "    int x = 5;\n"
            "    int arr = xsArrayCreateInt(x, 10);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_no_indent_mode(self):
        def f() -> None:
            arr: list[int] = [1] * 10

        self.assertEqual(
            "void f(){int arr=xsArrayCreateInt(10,1);}",
            _convert(f, indent=False),
        )

    def test_no_indent_zero_default(self):
        def f() -> None:
            arr: list[int] = [0] * 10

        self.assertEqual(
            "void f(){int arr=xsArrayCreateInt(10);}",
            _convert(f, indent=False),
        )


if __name__ == "__main__":
    unittest.main()
