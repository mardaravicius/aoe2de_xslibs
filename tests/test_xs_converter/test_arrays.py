import unittest

from numpy import int32, float32
from typing import List, cast
from xs_converter.functions import vector, xs_set_player_attribute, xs_chat_data, xs_array_get_int
from xs_converter.symbols import XsVector

from tests.test_xs_converter.helpers import _convert


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

    def test_empty_annotated_list(self):
        def f() -> None:
            arr: list[int] = []

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

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

    def test_2d_array_init(self):
        def f() -> None:
            arr: list[list[float]] = [[0.0] * 5] * 3

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(3);\n"
            "    for (temp00000000 = 0; < 3) {\n"
            "        xsArraySetInt(arr, temp00000000, xsArrayCreateFloat(5));\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_3d_array_init(self):
        def f() -> None:
            arr: list[list[list[float]]] = [[[0.0] * 4] * 5] * 3

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(3);\n"
            "    for (temp00000000 = 0; < 3) {\n"
            "        int temp00000001 = xsArrayCreateInt(5);\n"
            "        xsArraySetInt(arr, temp00000000, temp00000001);\n"
            "        for (temp00000002 = 0; < 5) {\n"
            "            xsArraySetInt(temp00000001, temp00000002, xsArrayCreateFloat(4));\n"
            "        }\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestArrayAssignment(unittest.TestCase):

    def test_set_int(self):
        def f() -> None:
            a: list[int] = [0] * 10
            a[0] = 1

        expected = (
            "void f() {\n"
            "    int a = xsArrayCreateInt(10);\n"
            "    xsArraySetInt(a, 0, 1);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_set_negative_int(self):
        def f() -> None:
            a: list[int] = [0] * 10
            a[0] = -5

        expected = (
            "void f() {\n"
            "    int a = xsArrayCreateInt(10);\n"
            "    xsArraySetInt(a, 0, -5);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_set_float(self):
        def f() -> None:
            a: list[float] = [0.0] * 10
            a[0] = 1.5

        expected = (
            "void f() {\n"
            "    int a = xsArrayCreateFloat(10);\n"
            "    xsArraySetFloat(a, 0, 1.5);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_set_bool_true(self):
        def f() -> None:
            a: list[bool] = [False] * 10
            a[0] = True

        expected = (
            "void f() {\n"
            "    int a = xsArrayCreateBool(10);\n"
            "    xsArraySetBool(a, 0, true);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_set_bool_false(self):
        def f() -> None:
            a: list[bool] = [False] * 10
            a[0] = False

        expected = (
            "void f() {\n"
            "    int a = xsArrayCreateBool(10);\n"
            "    xsArraySetBool(a, 0, false);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_set_string(self):
        def f() -> None:
            a: list[str] = [""] * 10
            a[0] = "hello"

        expected = (
            "void f() {\n"
            "    int a = xsArrayCreateString(10);\n"
            '    xsArraySetString(a, 0, "hello");\n'
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_set_empty_string(self):
        def f() -> None:
            a: list[str] = [""] * 10
            a[0] = ""

        expected = (
            "void f() {\n"
            "    int a = xsArrayCreateString(10);\n"
            '    xsArraySetString(a, 0, "");\n'
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_set_int32_cast(self):
        def f() -> None:
            a: list[int] = [0] * 10
            a[0] = int32(-1)

        expected = (
            "void f() {\n"
            "    int a = xsArrayCreateInt(10);\n"
            "    xsArraySetInt(a, 0, -1);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_set_float32_cast(self):
        def f() -> None:
            a: list[float] = [0.0] * 10
            a[0] = float32(1.5)

        expected = (
            "void f() {\n"
            "    int a = xsArrayCreateFloat(10);\n"
            "    xsArraySetFloat(a, 0, 1.5);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_set_vector(self):
        def f() -> None:
            a: list[XsVector] = [vector(0.0, 0.0, 0.0)] * 10
            a[0] = vector(1.1, 1.1, 1.1)

        expected = (
            "void f() {\n"
            "    int a = xsArrayCreateVector(10);\n"
            "    xsArraySetVector(a, 0, vector(1.1, 1.1, 1.1));\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_variable_index(self):
        def f() -> None:
            a: list[int] = [0] * 10
            i: int = 0
            a[i] = 1

        expected = (
            "void f() {\n"
            "    int a = xsArrayCreateInt(10);\n"
            "    int i = 0;\n"
            "    xsArraySetInt(a, i, 1);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_expression_index(self):
        def f() -> None:
            a: list[int] = [0] * 10
            i: int = 0
            a[i + 1] = 1

        expected = (
            "void f() {\n"
            "    int a = xsArrayCreateInt(10);\n"
            "    int i = 0;\n"
            "    xsArraySetInt(a, i + 1, 1);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_non_constant_value_raises(self):
        def f() -> None:
            a: list[int] = [0] * 10
            x: int = 5
            a[0] = x

        with self.assertRaises(ValueError):
            _convert(f)

    def test_no_indent(self):
        def f() -> None:
            a: list[int] = [0] * 10
            a[0] = 1

        self.assertEqual(
            "void f(){int a=xsArrayCreateInt(10);xsArraySetInt(a,0,1);}",
            _convert(f, indent=False),
        )

    def test_camel_case_array_name(self):
        def f() -> None:
            my_arr: list[int] = [0] * 10
            my_arr[0] = 1

        expected = (
            "void f() {\n"
            "    int myArr = xsArrayCreateInt(10);\n"
            "    xsArraySetInt(myArr, 0, 1);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_set_2d_array_float(self):
        def f() -> None:
            arr: list[list[float]] = [[0.0] * 3] * 2
            arr[0][1] = 2.2

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(2);\n"
            "    for (temp00000000 = 0; < 2) {\n"
            "        xsArraySetInt(arr, temp00000000, xsArrayCreateFloat(3));\n"
            "    }\n"
            "    xsArraySetFloat(xsArrayGetInt(arr, 0), 1, 2.2);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_set_2d_array_int(self):
        def f() -> None:
            arr: list[list[int]] = [[0] * 4] * 3
            arr[1][2] = 42

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(3);\n"
            "    for (temp00000000 = 0; < 3) {\n"
            "        xsArraySetInt(arr, temp00000000, xsArrayCreateInt(4));\n"
            "    }\n"
            "    xsArraySetInt(xsArrayGetInt(arr, 1), 2, 42);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_set_3d_array(self):
        def f() -> None:
            arr: list[list[list[float]]] = [[[0.0] * 4] * 5] * 3
            arr[0][1][2] = 9.9

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(3);\n"
            "    for (temp00000000 = 0; < 3) {\n"
            "        int temp00000001 = xsArrayCreateInt(5);\n"
            "        xsArraySetInt(arr, temp00000000, temp00000001);\n"
            "        for (temp00000002 = 0; < 5) {\n"
            "            xsArraySetInt(temp00000001, temp00000002, xsArrayCreateFloat(4));\n"
            "        }\n"
            "    }\n"
            "    xsArraySetFloat(xsArrayGetInt(xsArrayGetInt(arr, 0), 1), 2, 9.9);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_set_2d_array_with_variable_index(self):
        def f() -> None:
            arr: list[list[int]] = [[0] * 4] * 3
            i: int = 1
            j: int = 2
            arr[i][j] = 10

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(3);\n"
            "    for (temp00000000 = 0; < 3) {\n"
            "        xsArraySetInt(arr, temp00000000, xsArrayCreateInt(4));\n"
            "    }\n"
            "    int i = 1;\n"
            "    int j = 2;\n"
            "    xsArraySetInt(xsArrayGetInt(arr, i), j, 10);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_set_2d_array_with_cast(self):
        def f() -> None:
            arr: list[list[float]] = [[0.0] * 3] * 2
            x: float = 5.5
            arr[0][1] = cast(float, x)

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(2);\n"
            "    for (temp00000000 = 0; < 2) {\n"
            "        xsArraySetInt(arr, temp00000000, xsArrayCreateFloat(3));\n"
            "    }\n"
            "    float x = 5.5;\n"
            "    xsArraySetFloat(xsArrayGetInt(arr, 0), 1, x);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestArrayGet(unittest.TestCase):

    def test_get_int(self):
        def f() -> None:
            arr: list[int] = [0] * 10
            v: int = arr[0]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(10);\n"
            "    int v = xsArrayGetInt(arr, 0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_get_float(self):
        def f() -> None:
            arr: list[float] = [0.0] * 10
            v: float = arr[0]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateFloat(10);\n"
            "    float v = xsArrayGetFloat(arr, 0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_get_bool(self):
        def f() -> None:
            arr: list[bool] = [False] * 10
            v: bool = arr[0]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateBool(10);\n"
            "    bool v = xsArrayGetBool(arr, 0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_get_string(self):
        def f() -> None:
            arr: list[str] = [""] * 10
            v: str = arr[0]

        expected = (
            "void f() {\n"
            '    int arr = xsArrayCreateString(10);\n'
            "    string v = xsArrayGetString(arr, 0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_get_vector(self):
        def f() -> None:
            arr: list[XsVector] = [vector(0.0, 0.0, 0.0)] * 10
            v: XsVector = arr[0]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateVector(10);\n"
            "    vector v = xsArrayGetVector(arr, 0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_get_int32(self):
        def f() -> None:
            arr: list[int32] = [0] * 10
            v: int32 = arr[0]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(10);\n"
            "    int v = xsArrayGetInt(arr, 0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_get_float32(self):
        def f() -> None:
            arr: list[float32] = [0.0] * 10
            v: float32 = arr[0]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateFloat(10);\n"
            "    float v = xsArrayGetFloat(arr, 0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_get_variable_index(self):
        def f() -> None:
            arr: list[int] = [0] * 10
            i: int = 3
            v: int = arr[i]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(10);\n"
            "    int i = 3;\n"
            "    int v = xsArrayGetInt(arr, i);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_get_expression_index(self):
        def f() -> None:
            arr: list[int] = [0] * 10
            i: int = 0
            v: int = arr[i + 1]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(10);\n"
            "    int i = 0;\n"
            "    int v = xsArrayGetInt(arr, i + 1);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_get_camel_case(self):
        def f() -> None:
            my_arr: list[int] = [0] * 10
            my_val: int = my_arr[0]

        expected = (
            "void f() {\n"
            "    int myArr = xsArrayCreateInt(10);\n"
            "    int myVal = xsArrayGetInt(myArr, 0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_get_no_indent(self):
        def f() -> None:
            arr: list[int] = [0] * 10
            v: int = arr[0]

        self.assertEqual(
            "void f(){int arr=xsArrayCreateInt(10);int v=xsArrayGetInt(arr,0);}",
            _convert(f, indent=False),
        )

    def test_get_2d_array_access(self):
        def f() -> None:
            arr: list[int] = [0] * 10
            v: int = arr[0][1]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(10);\n"
            "    int v = xsArrayGetInt(xsArrayGetInt(arr, 0), 1);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_get_3d_array_access(self):
        def f() -> None:
            arr: list[list[list[float]]] = [[[0.0] * 4] * 5] * 3
            v: float = arr[0][1][2]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(3);\n"
            "    for (temp00000000 = 0; < 3) {\n"
            "        int temp00000001 = xsArrayCreateInt(5);\n"
            "        xsArraySetInt(arr, temp00000000, temp00000001);\n"
            "        for (temp00000002 = 0; < 5) {\n"
            "            xsArraySetInt(temp00000001, temp00000002, xsArrayCreateFloat(4));\n"
            "        }\n"
            "    }\n"
            "    float v = xsArrayGetFloat(xsArrayGetInt(xsArrayGetInt(arr, 0), 1), 2);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_get_2d_array_access_float_result(self):
        def f() -> None:
            arr: list[list[float]] = [[0.0] * 5] * 3
            v: float = arr[0][1]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(3);\n"
            "    for (temp00000000 = 0; < 3) {\n"
            "        xsArraySetInt(arr, temp00000000, xsArrayCreateFloat(5));\n"
            "    }\n"
            "    float v = xsArrayGetFloat(xsArrayGetInt(arr, 0), 1);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_array_get_in_function_call(self):
        def f() -> None:
            arr: list[str] = [""] * 5
            xs_chat_data(cast(str, arr[0]))

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateString(5);\n"
            '    xsChatData(xsArrayGetString(arr, 0));\n'
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_array_get_in_arithmetic(self):
        def f() -> None:
            arr: list[int] = [0] * 5
            x: int = cast(int, arr[0]) + 1

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(5);\n"
            "    int x = xsArrayGetInt(arr, 0) + 1;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_array_get_in_condition(self):
        def f() -> None:
            arr: list[int] = [0] * 5
            if cast(int, arr[0]) > 3:
                pass

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(5);\n"
            "    if (xsArrayGetInt(arr, 0) > 3) {\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_2d_array_get_in_expression(self):
        def f() -> None:
            arr: list[list[float]] = [[0.0] * 5] * 3
            x: float = cast(float, arr[0][1]) + 1.0

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(3);\n"
            "    for (temp00000000 = 0; < 3) {\n"
            "        xsArraySetInt(arr, temp00000000, xsArrayCreateFloat(5));\n"
            "    }\n"
            "    float x = xsArrayGetFloat(xsArrayGetInt(arr, 0), 1) + 1.0;\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_array_get_as_array_set_value(self):
        def f() -> None:
            a: list[int] = [0] * 5
            b: list[int] = [0] * 5
            a[0] = cast(int, b[1])

        expected = (
            "void f() {\n"
            "    int a = xsArrayCreateInt(5);\n"
            "    int b = xsArrayCreateInt(5);\n"
            "    xsArraySetInt(a, 0, xsArrayGetInt(b, 1));\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_get_subarray_handle(self):
        def f() -> None:
            arr: list[list[int]] = [[0] * 4] * 3
            sub: list[int] = arr[0]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(3);\n"
            "    for (temp00000000 = 0; < 3) {\n"
            "        xsArraySetInt(arr, temp00000000, xsArrayCreateInt(4));\n"
            "    }\n"
            "    int sub = xsArrayGetInt(arr, 0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


class TestListLiterals(unittest.TestCase):

    def test_int_list(self):
        def f() -> None:
            arr = [1, 2, 3]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(3);\n"
            "    xsArraySetInt(arr, 0, 1);\n"
            "    xsArraySetInt(arr, 1, 2);\n"
            "    xsArraySetInt(arr, 2, 3);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_float_list(self):
        def f() -> None:
            arr = [1.0, 2.5]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateFloat(2);\n"
            "    xsArraySetFloat(arr, 0, 1.0);\n"
            "    xsArraySetFloat(arr, 1, 2.5);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_bool_list(self):
        def f() -> None:
            arr = [True, False, True]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateBool(3);\n"
            "    xsArraySetBool(arr, 0, true);\n"
            "    xsArraySetBool(arr, 1, false);\n"
            "    xsArraySetBool(arr, 2, true);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_string_list(self):
        def f() -> None:
            arr = ["hello", "world"]

        expected = (
            "void f() {\n"
            '    int arr = xsArrayCreateString(2);\n'
            '    xsArraySetString(arr, 0, "hello");\n'
            '    xsArraySetString(arr, 1, "world");\n'
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_vector_list(self):
        def f() -> None:
            arr = [vector(1.0, 2.0, 3.0), vector(4.0, 5.0, 6.0)]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateVector(2);\n"
            "    xsArraySetVector(arr, 0, vector(1.0, 2.0, 3.0));\n"
            "    xsArraySetVector(arr, 1, vector(4.0, 5.0, 6.0));\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_variables_with_constant_type_hint(self):
        def f() -> None:
            a: int = 10
            b: int = 20
            arr = [a, b, 3]

        expected = (
            "void f() {\n"
            "    int a = 10;\n"
            "    int b = 20;\n"
            "    int arr = xsArrayCreateInt(3);\n"
            "    xsArraySetInt(arr, 0, a);\n"
            "    xsArraySetInt(arr, 1, b);\n"
            "    xsArraySetInt(arr, 2, 3);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_int32_cast_infers_type(self):
        def f() -> None:
            x: int = 5
            arr = [int32(1), x]

        expected = (
            "void f() {\n"
            "    int x = 5;\n"
            "    int arr = xsArrayCreateInt(2);\n"
            "    xsArraySetInt(arr, 0, 1);\n"
            "    xsArraySetInt(arr, 1, x);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_float32_cast_infers_type(self):
        def f() -> None:
            x: float = 5.0
            arr = [float32(1.0), x]

        expected = (
            "void f() {\n"
            "    float x = 5.0;\n"
            "    int arr = xsArrayCreateFloat(2);\n"
            "    xsArraySetFloat(arr, 0, 1.0);\n"
            "    xsArraySetFloat(arr, 1, x);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_single_element(self):
        def f() -> None:
            arr = [42]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(1);\n"
            "    xsArraySetInt(arr, 0, 42);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_negative_constants(self):
        def f() -> None:
            arr = [-1, -2, -3]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(3);\n"
            "    xsArraySetInt(arr, 0, -1);\n"
            "    xsArraySetInt(arr, 1, -2);\n"
            "    xsArraySetInt(arr, 2, -3);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_camel_case_name(self):
        def f() -> None:
            my_arr = [1, 2]

        expected = (
            "void f() {\n"
            "    int myArr = xsArrayCreateInt(2);\n"
            "    xsArraySetInt(myArr, 0, 1);\n"
            "    xsArraySetInt(myArr, 1, 2);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_annotated_list(self):
        def f() -> None:
            arr: list[int] = [1, 2, 3]

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(3);\n"
            "    xsArraySetInt(arr, 0, 1);\n"
            "    xsArraySetInt(arr, 1, 2);\n"
            "    xsArraySetInt(arr, 2, 3);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_all_variables_raises_without_annotation(self):
        def f() -> None:
            a: int = 1
            b: int = 2
            arr = [a, b]

        with self.assertRaises(ValueError):
            _convert(f)

    def test_all_variables_with_annotation(self):
        def f() -> None:
            a: int = 1
            b: int = 2
            c: int = 3
            arr: list[int] = [a, b, c]

        expected = (
            "void f() {\n"
            "    int a = 1;\n"
            "    int b = 2;\n"
            "    int c = 3;\n"
            "    int arr = xsArrayCreateInt(3);\n"
            "    xsArraySetInt(arr, 0, a);\n"
            "    xsArraySetInt(arr, 1, b);\n"
            "    xsArraySetInt(arr, 2, c);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_empty_annotated_int_list(self):
        def f() -> None:
            arr: list[int] = []

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_empty_annotated_float_list(self):
        def f() -> None:
            arr: list[float] = []

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateFloat(0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_empty_annotated_string_list(self):
        def f() -> None:
            arr: list[str] = []

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateString(0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_empty_annotated_bool_list(self):
        def f() -> None:
            arr: list[bool] = []

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateBool(0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_empty_annotated_uppercase_list(self):
        def f() -> None:
            arr: List[int] = []

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_annotated_variables_float(self):
        def f() -> None:
            a: float = 1.0
            arr: list[float] = [a]

        expected = (
            "void f() {\n"
            "    float a = 1.0;\n"
            "    int arr = xsArrayCreateFloat(1);\n"
            "    xsArraySetFloat(arr, 0, a);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_mixed_constant_types_raises(self):
        def f() -> None:
            arr = [1, 2.0]

        with self.assertRaises(ValueError):
            _convert(f)

    def test_mixed_int_bool_raises(self):
        def f() -> None:
            arr = [1, True]

        with self.assertRaises(ValueError):
            _convert(f)

    def test_empty_list_raises(self):
        def f() -> None:
            arr = []

        with self.assertRaises(ValueError):
            _convert(f)

    def test_no_indent(self):
        def f() -> None:
            arr = [1, 2, 3]

        self.assertEqual(
            "void f(){int arr=xsArrayCreateInt(3);xsArraySetInt(arr,0,1);xsArraySetInt(arr,1,2);xsArraySetInt(arr,2,3);}",
            _convert(f, indent=False),
        )

    def test_inside_if_block(self):
        def f() -> None:
            if True:
                arr = [1, 2]

        expected = (
            "void f() {\n"
            "    if (true) {\n"
            "        int arr = xsArrayCreateInt(2);\n"
            "        xsArraySetInt(arr, 0, 1);\n"
            "        xsArraySetInt(arr, 1, 2);\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_list_in_function_call(self):
        def f() -> None:
            xs_array_get_int([1, 2, 3], 0)

        expected = (
            "void f() {\n"
            "    int temp00000000 = xsArrayCreateInt(3);\n"
            "    xsArraySetInt(temp00000000, 0, 1);\n"
            "    xsArraySetInt(temp00000000, 1, 2);\n"
            "    xsArraySetInt(temp00000000, 2, 3);\n"
            "    xsArrayGetInt(temp00000000, 0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_two_lists_in_call(self):
        def f() -> None:
            xs_set_player_attribute([1, 2], [3, 4])

        expected = (
            "void f() {\n"
            "    int temp00000000 = xsArrayCreateInt(2);\n"
            "    xsArraySetInt(temp00000000, 0, 1);\n"
            "    xsArraySetInt(temp00000000, 1, 2);\n"
            "    int temp00000001 = xsArrayCreateInt(2);\n"
            "    xsArraySetInt(temp00000001, 0, 3);\n"
            "    xsArraySetInt(temp00000001, 1, 4);\n"
            "    xsSetPlayerAttribute(temp00000000, temp00000001);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_list_in_expression_no_indent(self):
        def f() -> None:
            xs_array_get_int([1, 2], 0)

        self.assertEqual(
            "void f(){int temp00000000=xsArrayCreateInt(2);xsArraySetInt(temp00000000,0,1);xsArraySetInt(temp00000000,1,2);xsArrayGetInt(temp00000000,0);}",
            _convert(f, indent=False),
        )

    def test_list_in_expression_inside_if(self):
        def f() -> None:
            if True:
                xs_array_get_int([10, 20], 0)

        expected = (
            "void f() {\n"
            "    if (true) {\n"
            "        int temp00000000 = xsArrayCreateInt(2);\n"
            "        xsArraySetInt(temp00000000, 0, 10);\n"
            "        xsArraySetInt(temp00000000, 1, 20);\n"
            "        xsArrayGetInt(temp00000000, 0);\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_float_list_in_expression(self):
        def f() -> None:
            xs_chat_data([1.5, 2.5])

        expected = (
            "void f() {\n"
            "    int temp00000000 = xsArrayCreateFloat(2);\n"
            "    xsArraySetFloat(temp00000000, 0, 1.5);\n"
            "    xsArraySetFloat(temp00000000, 1, 2.5);\n"
            "    xsChatData(temp00000000);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_empty_list_in_expression_raises(self):
        def f() -> None:
            xs_chat_data([])

        with self.assertRaises(ValueError):
            _convert(f)


class TestCastInArrays(unittest.TestCase):

    def test_cast_int_in_repeat_array(self):
        def f() -> None:
            a: int = 5
            arr: list[int] = [cast(int, a)] * 10

        expected = (
            "void f() {\n"
            "    int a = 5;\n"
            "    int arr = xsArrayCreateInt(10, a);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_float_in_repeat_array(self):
        def f() -> None:
            a: float = 1.5
            arr: list[float] = [cast(float, a)] * 5

        expected = (
            "void f() {\n"
            "    float a = 1.5;\n"
            "    int arr = xsArrayCreateFloat(5, a);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_bool_in_repeat_array(self):
        def f() -> None:
            a: bool = True
            arr: list[bool] = [cast(bool, a)] * 3

        expected = (
            "void f() {\n"
            "    bool a = true;\n"
            "    int arr = xsArrayCreateBool(3, a);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_str_in_repeat_array(self):
        def f() -> None:
            a: str = "hi"
            arr: list[str] = [cast(str, a)] * 4

        expected = (
            "void f() {\n"
            '    string a = "hi";\n'
            "    int arr = xsArrayCreateString(4, a);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_int_in_array_set(self):
        def f() -> None:
            arr: list[int] = [0] * 10
            x: int = 42
            arr[0] = cast(int, x)

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(10);\n"
            "    int x = 42;\n"
            "    xsArraySetInt(arr, 0, x);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_float_in_array_set(self):
        def f() -> None:
            arr: list[float] = [0.0] * 10
            x: float = 1.5
            arr[0] = cast(float, x)

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateFloat(10);\n"
            "    float x = 1.5;\n"
            "    xsArraySetFloat(arr, 0, x);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_bool_in_array_set(self):
        def f() -> None:
            arr: list[bool] = [False] * 10
            x: bool = True
            arr[0] = cast(bool, x)

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateBool(10);\n"
            "    bool x = true;\n"
            "    xsArraySetBool(arr, 0, x);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_str_in_array_set(self):
        def f() -> None:
            arr: list[str] = [""] * 10
            x: str = "hello"
            arr[0] = cast(str, x)

        expected = (
            "void f() {\n"
            '    int arr = xsArrayCreateString(10);\n'
            '    string x = "hello";\n'
            "    xsArraySetString(arr, 0, x);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_int_in_list_literal(self):
        def f() -> None:
            a: int = 10
            b: int = 20
            arr = [cast(int, a), cast(int, b)]

        expected = (
            "void f() {\n"
            "    int a = 10;\n"
            "    int b = 20;\n"
            "    int arr = xsArrayCreateInt(2);\n"
            "    xsArraySetInt(arr, 0, a);\n"
            "    xsArraySetInt(arr, 1, b);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_float_in_list_literal(self):
        def f() -> None:
            a: float = 1.0
            b: float = 2.5
            arr = [cast(float, a), cast(float, b)]

        expected = (
            "void f() {\n"
            "    float a = 1.0;\n"
            "    float b = 2.5;\n"
            "    int arr = xsArrayCreateFloat(2);\n"
            "    xsArraySetFloat(arr, 0, a);\n"
            "    xsArraySetFloat(arr, 1, b);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_mixed_with_constants_in_list(self):
        def f() -> None:
            a: int = 10
            arr = [cast(int, a), 20, 30]

        expected = (
            "void f() {\n"
            "    int a = 10;\n"
            "    int arr = xsArrayCreateInt(3);\n"
            "    xsArraySetInt(arr, 0, a);\n"
            "    xsArraySetInt(arr, 1, 20);\n"
            "    xsArraySetInt(arr, 2, 30);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_constant_zero_default_omitted(self):
        def f() -> None:
            arr: list[int] = [cast(int, 0)] * 10

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(10);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_constant_nonzero_default(self):
        def f() -> None:
            arr: list[int] = [cast(int, 5)] * 10

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(10, 5);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_in_annotated_list_literal(self):
        def f() -> None:
            a: float = 1.0
            b: float = 2.0
            arr: list[float] = [cast(float, a), cast(float, b)]

        expected = (
            "void f() {\n"
            "    float a = 1.0;\n"
            "    float b = 2.0;\n"
            "    int arr = xsArrayCreateFloat(2);\n"
            "    xsArraySetFloat(arr, 0, a);\n"
            "    xsArraySetFloat(arr, 1, b);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_no_indent(self):
        def f() -> None:
            x: int = 5
            arr: list[int] = [cast(int, x)] * 3

        self.assertEqual(
            "void f(){int x=5;int arr=xsArrayCreateInt(3,x);}",
            _convert(f, indent=False),
        )

    def test_cast_expression_in_array_set(self):
        def f() -> None:
            arr: list[int] = [0] * 10
            x: int = 5
            arr[0] = cast(int, x + 1)

        expected = (
            "void f() {\n"
            "    int arr = xsArrayCreateInt(10);\n"
            "    int x = 5;\n"
            "    xsArraySetInt(arr, 0, x + 1);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_in_list_literal_with_expression(self):
        def f() -> None:
            a: int = 10
            arr = [cast(int, a + 1), cast(int, a + 2)]

        expected = (
            "void f() {\n"
            "    int a = 10;\n"
            "    int arr = xsArrayCreateInt(2);\n"
            "    xsArraySetInt(arr, 0, a + 1);\n"
            "    xsArraySetInt(arr, 1, a + 2);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_int32_in_list_literal(self):
        def f() -> None:
            a: int = 10
            arr = [cast(int32, a), 20]

        expected = (
            "void f() {\n"
            "    int a = 10;\n"
            "    int arr = xsArrayCreateInt(2);\n"
            "    xsArraySetInt(arr, 0, a);\n"
            "    xsArraySetInt(arr, 1, 20);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))

    def test_cast_float32_in_list_literal(self):
        def f() -> None:
            a: float = 1.0
            arr = [cast(float32, a), 2.0]

        expected = (
            "void f() {\n"
            "    float a = 1.0;\n"
            "    int arr = xsArrayCreateFloat(2);\n"
            "    xsArraySetFloat(arr, 0, a);\n"
            "    xsArraySetFloat(arr, 1, 2.0);\n"
            "}\n"
        )
        self.assertEqual(expected, _convert(f))


if __name__ == "__main__":
    unittest.main()
