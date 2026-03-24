import unittest

from xs_converter.constants import XsConstants
from xs_converter.functions import xs_effect_amount

from tests.test_xs_converter.helpers import convert


class TestConstants(unittest.TestCase):

    def test_large_int(self):
        def f() -> None:
            x: int = 1_500_000_021

        expected = (
            "void f() {\n"
            "    int x = 150000002 * 10 + 1;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_large_negative_int(self):
        def f() -> None:
            x: int = -1_500_000_021

        expected = (
            "void f() {\n"
            "    int x = -150000002 * 10 - 1;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_max_int(self):
        def f() -> None:
            x: int = 2_147_483_647

        expected = (
            "void f() {\n"
            "    int x = 214748364 * 10 + 7;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_min_int(self):
        def f() -> None:
            x: int = -2_147_483_648

        expected = (
            "void f() {\n"
            "    int x = -214748364 * 10 - 8;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_int_overflow_raises(self):
        def f() -> None:
            x: int = 2_147_483_648

        with self.assertRaises(ValueError):
            convert(f)

    def test_int_underflow_raises(self):
        def f() -> None:
            x: int = -2_147_483_649

        with self.assertRaises(ValueError):
            convert(f)

    def test_string_with_quotes(self):
        def f() -> None:
            x: str = 'he said "hi"'

        expected = (
            "void f() {\n"
            '    string x = "he said \\"hi\\"";\n'
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_false_constant(self):
        def f() -> None:
            x: bool = False

        expected = (
            "void f() {\n"
            "    bool x = false;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_xs_constant_in_call(self):
        def f() -> None:
            xs_effect_amount(XsConstants.c_set_attribute, 101, XsConstants.c_attack, 10.0, 1)

        expected = (
            "void f() {\n"
            "    xsEffectAmount(cSetAttribute, 101, cAttack, 10.0, 1);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))


class TestBinaryExpressions(unittest.TestCase):

    def test_addition(self):
        def f() -> int:
            return 1 + 2

        expected = (
            "int f() {\n"
            "    return (1 + 2);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_subtraction(self):
        def f() -> int:
            return 5 - 3

        expected = (
            "int f() {\n"
            "    return (5 - 3);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_multiplication(self):
        def f() -> int:
            return 2 * 3

        expected = (
            "int f() {\n"
            "    return (2 * 3);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_division(self):
        def f() -> float:
            return 10.0 / 3.0

        expected = (
            "float f() {\n"
            "    return (10.0 / 3.0);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_floor_division(self):
        def f() -> int:
            return 10 // 3

        expected = (
            "int f() {\n"
            "    return (10 / 3);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_modulo(self):
        def f() -> int:
            return 10 % 3

        expected = (
            "int f() {\n"
            "    return (10 % 3);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_nested_binary_ops(self):
        def f() -> None:
            x: float = 2.2 * 12.45 + 1.1

        expected = (
            "void f() {\n"
            "    float x = (2.2 * 12.45) + 1.1;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))


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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))


class TestUnaryExpressions(unittest.TestCase):

    def test_negative_constant(self):
        def f() -> None:
            x: int = -5

        expected = (
            "void f() {\n"
            "    int x = -5;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))


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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))


if __name__ == "__main__":
    unittest.main()
