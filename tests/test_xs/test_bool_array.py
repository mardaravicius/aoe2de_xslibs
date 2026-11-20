import unittest
from random import choice

from xs.bool_array import *


class BoolArrayTest(unittest.TestCase):
    def test_xs_bool_array_repeated(self):
        self.assertEqual(c_bool_array_generic_error, xs_bool_array_from_repeated_val(True, int32(-1)))
        self.assertEqual("[true, true, true]", xs_bool_array_to_string(xs_bool_array_from_repeated_val(True, int32(3))))
        arr = xs_bool_array_from_string("true,false")
        self.assertEqual("[true, false, true, false, true, false]",
                         xs_bool_array_to_string(xs_bool_array_from_repeated_array(arr, int32(3))))
        self.assertEqual("[]", xs_bool_array_to_string(xs_bool_array_from_repeated_array(arr, int32(0))))

    def test_xs_bool_array_repeated_array_edge_cases(self):
        empty = xs_bool_array_from_string("")
        self.assertEqual("[]", xs_bool_array_to_string(xs_bool_array_from_repeated_array(empty, int32(5))))
        arr = xs_bool_array_from_string("true,false")
        self.assertEqual(c_bool_array_generic_error, xs_bool_array_from_repeated_array(arr, int32(-1)))
        self.assertEqual(c_bool_array_max_capacity_error,
                         xs_bool_array_from_repeated_array(arr, c_bool_array_max_capacity // 2 + 1))

    def test_xs_bool_array_from_string(self):
        self.assertEqual("[true, false, true]",
                         xs_bool_array_to_string(xs_bool_array_from_string(" true, x,false ,true, 1")))
        self.assertEqual("[]", xs_bool_array_to_string(xs_bool_array_from_string("  ")))

    def test_xs_bool_array_index(self):
        arr = bool_arr([True, False, True, False])
        self.assertEqual(1, xs_bool_array_index(arr, False))
        self.assertEqual(3, xs_bool_array_index(arr, False, int32(2)))
        self.assertEqual(3, xs_bool_array_index(arr, False, int32(-1)))
        self.assertEqual(c_bool_array_generic_error, xs_bool_array_index(arr, False, int32(0), int32(-3)))
        self.assertTrue(xs_bool_array_contains(arr, True))
        self.assertFalse(xs_bool_array_contains(bool_arr([True]), False))
        self.assertEqual(2, xs_bool_array_count(arr, False))

    def test_xs_bool_array_index_edge_cases(self):
        arr = bool_arr([True, False, False])
        self.assertEqual(c_bool_array_generic_error, xs_bool_array_index(arr, True, int32(2), int32(1)))
        self.assertEqual(c_bool_array_generic_error, xs_bool_array_index(arr, True, int32(5)))
        self.assertEqual(0, xs_bool_array_index(arr, True, int32(-10)))
        self.assertEqual(1, xs_bool_array_index(arr, False, int32(0), int32(100)))

    def test_xs_bool_array_sort(self):
        for size in [0, 1, 2, 5, 50]:
            for reverse in [False, True]:
                data = [choice([True, False]) for _ in range(size)]
                arr = bool_arr(data)
                xs_bool_array_sort(arr, reverse)
                self.assertEqual(bstr(sorted(data, reverse=reverse)), xs_bool_array_to_string(arr))

    def test_xs_bool_array_reverse(self):
        for i in range(0, 6):
            data = [v % 3 == 0 for v in range(i)]
            arr = bool_arr(data)
            xs_bool_array_reverse(arr)
            self.assertEqual(bstr(list(reversed(data))), xs_bool_array_to_string(arr))

    def test_xs_bool_array_copy(self):
        data = [True, False, False, True, True, False]
        arr = bool_arr(data)
        for start, end in [(0, 6), (2, 4), (-3, 6), (1, -1), (4, 2), (-10, 100)]:
            self.assertEqual(bstr(data[start:end]),
                             xs_bool_array_to_string(xs_bool_array_copy(arr, int32(start), int32(end))))
        self.assertEqual(bstr(data), xs_bool_array_to_string(xs_bool_array_copy(arr)))

    def test_xs_bool_array_copy_start_past_end(self):
        arr = bool_arr([True, False, True])
        self.assertEqual("[]", xs_bool_array_to_string(xs_bool_array_copy(arr, int32(5))))
        self.assertEqual("[]", xs_bool_array_to_string(xs_bool_array_copy(arr, int32(3), int32(10))))

    def test_xs_bool_array_copy_is_independent(self):
        arr = bool_arr([True, False])
        copy = xs_bool_array_copy(arr)
        xs_array_set_bool(copy, int32(0), False)
        self.assertEqual("[true, false]", xs_bool_array_to_string(arr))

    def test_xs_bool_array_compare(self):
        a = bool_arr([True, False])
        self.assertEqual(0, xs_bool_array_compare(a, bool_arr([True, False])))
        self.assertEqual(-1, xs_bool_array_compare(a, bool_arr([True, True])))
        self.assertEqual(1, xs_bool_array_compare(a, bool_arr([False, True])))
        self.assertEqual(1, xs_bool_array_compare(a, bool_arr([True])))
        self.assertEqual(-1, xs_bool_array_compare(a, bool_arr([True, False, False])))

    def test_xs_bool_array_empty_array_operations(self):
        empty = bool_arr([])
        self.assertEqual(c_bool_array_generic_error, xs_bool_array_index(empty, False))
        self.assertFalse(xs_bool_array_contains(empty, False))
        self.assertEqual(0, xs_bool_array_count(empty, False))
        self.assertEqual(0, xs_bool_array_compare(empty, bool_arr([])))
        self.assertEqual(-1, xs_bool_array_compare(empty, bool_arr([False])))
        self.assertEqual(1, xs_bool_array_compare(bool_arr([False]), empty))
        xs_bool_array_reverse(empty)
        self.assertEqual("[]", xs_bool_array_to_string(empty))
        self.assertEqual("[]", xs_bool_array_to_string(xs_bool_array_copy(empty)))

    def test_xs_bool_array_delete(self):
        arr = bool_arr([True, False])
        self.assertEqual(c_bool_array_success, xs_bool_array_delete(arr))
        self.assertEqual(0, xs_array_get_size(arr))


def bool_arr(data: list[bool]) -> int32:
    arr = xs_array_create_bool(int32(len(data)))
    for i, v in enumerate(data):
        xs_array_set_bool(arr, int32(i), v)
    return arr


def bstr(lst: list[bool]) -> str:
    return str(lst).replace("True", "true").replace("False", "false")


if __name__ == "__main__":
    unittest.main()
