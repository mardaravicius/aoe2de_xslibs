import unittest

from xs.vector_array import *

V1 = vector(1.0, 1.1, -3.3)
V2 = vector(1.0, 2.0, 3.0)


def v(i: int) -> XsVector:
    return vector(float(i), float(i) + 0.5, -float(i))


class VectorArrayTest(unittest.TestCase):
    def test_xs_vector_array(self):
        for i in range(0, 13):
            data = [v(j) for j in range(i)]
            arr = xs_vector_array(*data)
            self.assertEqual(i, xs_array_get_size(arr))
            self.assertEqual(vstr(data), xs_vector_array_to_string(arr))

    def test_xs_vector_array_stop_at_magic_number(self):
        arr = xs_vector_array(V1, c_vector_array_empty_param, V2)
        self.assertEqual(vstr([V1]), xs_vector_array_to_string(arr))

    def test_xs_vector_array_repeated(self):
        self.assertEqual(c_vector_array_generic_error, xs_vector_array_from_repeated_val(V1, int32(-1)))
        self.assertEqual(vstr([V1, V1, V1]), xs_vector_array_to_string(xs_vector_array_from_repeated_val(V1, int32(3))))
        arr = xs_vector_array(V1, V2)
        self.assertEqual(vstr([V1, V2, V1, V2, V1, V2]),
                         xs_vector_array_to_string(xs_vector_array_from_repeated_array(arr, int32(3))))
        self.assertEqual("[]", xs_vector_array_to_string(xs_vector_array_from_repeated_array(arr, int32(0))))

    def test_xs_vector_array_repeated_array_edge_cases(self):
        empty = xs_vector_array()
        self.assertEqual("[]", xs_vector_array_to_string(xs_vector_array_from_repeated_array(empty, int32(5))))
        arr = xs_vector_array(V1, V2)
        self.assertEqual(c_vector_array_generic_error, xs_vector_array_from_repeated_array(arr, int32(-1)))
        self.assertEqual(c_vector_array_max_capacity_error,
                         xs_vector_array_from_repeated_array(arr, c_vector_array_max_capacity // 2 + 1))

    def test_xs_vector_array_from_string(self):
        self.assertEqual(vstr([V1, V2]),
                         xs_vector_array_to_string(xs_vector_array_from_string("v(1.0,1.1,-3.3), v( 1.0 , 2.0 , 3.0 )")))
        self.assertEqual(vstr([V2]), xs_vector_array_to_string(xs_vector_array_from_string(
            "v(1.0,2.0,3.0),v(1.0,2.0),(1.0,2.0,3.0),v(1.0,a,3.0),v(),,v(1,2,3),v(1.0,2.0,3.0")))
        self.assertEqual("[]", xs_vector_array_to_string(xs_vector_array_from_string("  ")))
        self.assertEqual("[]", xs_vector_array_to_string(xs_vector_array_from_string("x,v(1.0)")))
        self.assertEqual(vstr([V2]), xs_vector_array_to_string(xs_vector_array_from_string("v(1.0,2.0,3.0)")))

    def test_xs_vector_array_index(self):
        arr = xs_vector_array(V1, V2, v(3), V2)
        self.assertEqual(1, xs_vector_array_index(arr, V2))
        self.assertEqual(3, xs_vector_array_index(arr, V2, int32(2)))
        self.assertEqual(3, xs_vector_array_index(arr, V2, int32(-1)))
        self.assertEqual(c_vector_array_generic_error, xs_vector_array_index(arr, V2, int32(0), int32(-3)))
        self.assertTrue(xs_vector_array_contains(arr, v(3)))
        self.assertFalse(xs_vector_array_contains(arr, v(4)))
        self.assertEqual(2, xs_vector_array_count(arr, V2))

    def test_xs_vector_array_index_edge_cases(self):
        arr = xs_vector_array(V1, V2, v(3))
        self.assertEqual(c_vector_array_generic_error, xs_vector_array_index(arr, V1, int32(2), int32(1)))
        self.assertEqual(c_vector_array_generic_error, xs_vector_array_index(arr, V1, int32(5)))
        self.assertEqual(0, xs_vector_array_index(arr, V1, int32(-10)))
        self.assertEqual(2, xs_vector_array_index(arr, v(3), int32(0), int32(100)))

    def test_xs_vector_array_reverse(self):
        for i in range(0, 6):
            data = [v(j) for j in range(i)]
            arr = xs_vector_array(*data)
            xs_vector_array_reverse(arr)
            self.assertEqual(vstr(list(reversed(data))), xs_vector_array_to_string(arr))

    def test_xs_vector_array_copy(self):
        data = [v(j) for j in range(6)]
        arr = xs_vector_array(*data)
        for start, end in [(0, 6), (2, 4), (-3, 6), (1, -1), (4, 2), (-10, 100)]:
            self.assertEqual(vstr(data[start:end]),
                             xs_vector_array_to_string(xs_vector_array_copy(arr, int32(start), int32(end))))
        self.assertEqual(vstr(data), xs_vector_array_to_string(xs_vector_array_copy(arr)))

    def test_xs_vector_array_copy_start_past_end(self):
        arr = xs_vector_array(V1, V2, v(3))
        self.assertEqual("[]", xs_vector_array_to_string(xs_vector_array_copy(arr, int32(5))))
        self.assertEqual("[]", xs_vector_array_to_string(xs_vector_array_copy(arr, int32(3), int32(10))))

    def test_xs_vector_array_copy_is_independent(self):
        arr = xs_vector_array(V1, V2)
        copy = xs_vector_array_copy(arr)
        xs_array_set_vector(copy, int32(0), v(9))
        self.assertEqual(vstr([V1, V2]), xs_vector_array_to_string(arr))

    def test_xs_vector_array_empty_array_operations(self):
        empty = xs_vector_array()
        self.assertEqual(c_vector_array_generic_error, xs_vector_array_index(empty, V1))
        self.assertFalse(xs_vector_array_contains(empty, V1))
        self.assertEqual(0, xs_vector_array_count(empty, V1))
        xs_vector_array_reverse(empty)
        self.assertEqual("[]", xs_vector_array_to_string(empty))
        self.assertEqual("[]", xs_vector_array_to_string(xs_vector_array_copy(empty)))


def vstr(lst: list) -> str:
    if not lst:
        return "[]"
    return "[" + ", ".join(str(x) for x in lst) + "]"


if __name__ == "__main__":
    unittest.main()
