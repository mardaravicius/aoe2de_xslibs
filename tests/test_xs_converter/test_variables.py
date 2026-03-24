import unittest

from numpy import int32, float32
from xs_converter.symbols import XsConst, XsStatic, XsExtern, XsExternConst, XsVector
from xs_converter.functions import vector

from tests.test_xs_converter.helpers import convert


class TestVariableDefinitions(unittest.TestCase):

    def test_int_var(self):
        def f() -> None:
            x: int = 42

        expected = (
            "void f() {\n"
            "    int x = 42;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_float_var(self):
        def f() -> None:
            x: float = 3.14

        expected = (
            "void f() {\n"
            "    float x = 3.14;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_bool_var(self):
        def f() -> None:
            flag: bool = True

        expected = (
            "void f() {\n"
            "    bool flag = true;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_string_var(self):
        def f() -> None:
            msg: str = "hello"

        expected = (
            "void f() {\n"
            '    string msg = "hello";\n'
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_vector_var(self):
        def f() -> None:
            v: XsVector = vector(1.0, 2.0, 3.0)

        expected = (
            "void f() {\n"
            "    vector v = vector(1.0, 2.0, 3.0);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_const_modifier(self):
        def f() -> None:
            x: XsConst[int] = 99

        expected = (
            "void f() {\n"
            "    const int x = 99;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_static_modifier(self):
        def f() -> None:
            x: XsStatic[int] = 0

        expected = (
            "void f() {\n"
            "    static int x = 0;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_extern_modifier(self):
        def f() -> None:
            x: XsExtern[int] = 0

        expected = (
            "void f() {\n"
            "    extern int x = 0;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_extern_const_modifier(self):
        def f() -> None:
            x: XsExternConst[int] = 0

        expected = (
            "void f() {\n"
            "    extern const int x = 0;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))


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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))


class TestInt32Float32(unittest.TestCase):

    def test_int32_variable(self):
        def f() -> None:
            x: int32 = 7

        expected = (
            "void f() {\n"
            "    int x = 7;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_float32_variable(self):
        def f() -> None:
            x: float32 = 1.5

        expected = (
            "void f() {\n"
            "    float x = 1.5;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_int32_return_type(self):
        def f() -> int32:
            return 0

        expected = (
            "int f() {\n"
            "    return (0);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_float32_return_type(self):
        def f() -> float32:
            return 0.0

        expected = (
            "float f() {\n"
            "    return (0.0);\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

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
        self.assertEqual(expected, convert(f))

    def test_int32_cast_from_constant(self):
        def f() -> None:
            y: int = int32(42)

        expected = (
            "void f() {\n"
            "    int y = 42;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))

    def test_float32_cast_from_constant(self):
        def f() -> None:
            y: float = float32(3.14)

        expected = (
            "void f() {\n"
            "    float y = 3.14;\n"
            "}\n"
        )
        self.assertEqual(expected, convert(f))


if __name__ == "__main__":
    unittest.main()
