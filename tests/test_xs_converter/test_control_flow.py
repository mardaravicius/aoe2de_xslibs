import unittest

from xs_converter.constants import XsConstants
from xs_converter.functions import (
    xs_set_player_attribute,
    xs_player_attribute,
    xs_get_game_time,
    xs_effect_amount,
    xs_get_player_civilization,
    xs_chat_data,
)

from tests.test_xs_converter.helpers import convert


class TestReturn(unittest.TestCase):

    def test_return_void(self):
        def f() -> None:
            return

        expected = (
            "void f() {\n"
            "    return;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_return_value(self):
        def f() -> int:
            return 42

        expected = (
            "int f() {\n"
            "    return (42);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_return_expression(self):
        def f(x: int = 0) -> int:
            return x + 1

        expected = (
            "int f(int x = 0) {\n"
            "    return (x + 1);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))


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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))


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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
            "    int temp00000000 = e + f;\n"
            "    if (temp00000000 > 0) {\n"
            "        while (i < (c + d)) {\n"
            '            xsChatData("hi");\n'
            "            i = i + temp00000000;\n"
            "        }\n"
            "    } else if (temp00000000 < 0) {\n"
            "        while (i > (c + d)) {\n"
            '            xsChatData("hi");\n'
            "            i = i + temp00000000;\n"
            "        }\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_range_step_variable_negative_dispatches_by_sign(self):
        def f() -> None:
            step: int = -2
            for i in range(9, 0, step):
                xs_chat_data("hi")

        expected = (
            "void f() {\n"
            "    int step = -2;\n"
            "    int i = 9;\n"
            "    if (step > 0) {\n"
            "        while (i < 0) {\n"
            '            xsChatData("hi");\n'
            "            i = i + step;\n"
            "        }\n"
            "    } else if (step < 0) {\n"
            "        while (i > 0) {\n"
            '            xsChatData("hi");\n'
            "            i = i + step;\n"
            "        }\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_range_bound_sub_not_commutative(self):
        """Subtraction is not commutative: `1 - n` should NOT be rewritten as `>= n`."""
        def f() -> None:
            n: int = 10
            for i in range(9, 1 - n, -1):
                xs_chat_data("hi")

        expected = (
            "void f() {\n"
            "    int n = 10;\n"
            "    for (i = 9; > 1 - n) {\n"
            '        xsChatData("hi");\n'
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_range_bound_sub_minus_one_optimizes(self):
        """n - 1 with negative step still optimizes to >= n."""
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
        self.assertEqual(expected, convert(f))

    def test_range_bound_add_one_plus_n_optimizes(self):
        """1 + n with positive step still optimizes to <= n."""
        def f() -> None:
            n: int = 5
            for i in range(0, 1 + n):
                xs_chat_data("hi")

        expected = (
            "void f() {\n"
            "    int n = 5;\n"
            "    for (i = 0; <= n) {\n"
            '        xsChatData("hi");\n'
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))


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
        self.assertEqual(expected, convert(f))


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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))


if __name__ == "__main__":
    unittest.main()
