import unittest
from random import randint

from xs.int_array import *


class IntArrayTest(unittest.TestCase):
    def test_xs_int_array(self):
        for i in i32range(0, 13):
            params = tuple(i32range(i))
            arr = xs_int_array(*params)
            self.assertEqual(i, xs_array_get_size(arr))
            self.assertEqual(istr(list(range(i))), xs_int_array_to_string(arr))

    def test_xs_int_array_stop_at_magic_number(self):
        arr = xs_int_array(int32(1), c_int_array_empty_param, int32(2))
        self.assertEqual(istr([1]), xs_int_array_to_string(arr))

    def test_xs_int_array_range(self):
        test_data = [
            (0, 0, 1), (0, 1, 1), (0, 10, 1), (0, 10, 3), (10, 0, -1), (10, 0, -3),
            (-4, 4, 1), (5, -5, -2), (-8, -22, -3),
        ]
        for data in test_data:
            arr = xs_int_array_from_range(*data)
            self.assertEqual(istr(list(i32range(*data))), xs_int_array_to_string(arr))

    def test_xs_int_array_range_fail(self):
        for data in [(0, 5, 0), (10, 1, 1), (1, 10, -1)]:
            self.assertEqual(c_int_array_generic_error, xs_int_array_from_range(*data))

    def test_xs_int_array_repeated(self):
        self.assertEqual(c_int_array_generic_error, xs_int_array_from_repeated_val(int32(4), int32(-1)))
        self.assertEqual("[4, 4, 4]", xs_int_array_to_string(xs_int_array_from_repeated_val(int32(4), int32(3))))
        arr = xs_int_array(int32(1), int32(2))
        self.assertEqual("[1, 2, 1, 2, 1, 2]", xs_int_array_to_string(xs_int_array_from_repeated_array(arr, int32(3))))
        self.assertEqual("[]", xs_int_array_to_string(xs_int_array_from_repeated_array(arr, int32(0))))

    def test_xs_int_array_from_string(self):
        self.assertEqual("[1, 2, 3]", xs_int_array_to_string(xs_int_array_from_string(" 1, x,2 ,3")))
        self.assertEqual("[]", xs_int_array_to_string(xs_int_array_from_string("  ")))

    def test_xs_int_array_index(self):
        arr = xs_int_array(int32(1), int32(2), int32(3), int32(2))
        self.assertEqual(1, xs_int_array_index(arr, int32(2)))
        self.assertEqual(3, xs_int_array_index(arr, int32(2), int32(2)))
        self.assertEqual(3, xs_int_array_index(arr, int32(2), int32(-1)))
        self.assertEqual(c_int_array_generic_error, xs_int_array_index(arr, int32(2), int32(0), int32(-3)))
        self.assertTrue(xs_int_array_contains(arr, int32(3)))
        self.assertFalse(xs_int_array_contains(arr, int32(4)))
        self.assertEqual(2, xs_int_array_count(arr, int32(2)))

    def test_xs_int_array_sort(self):
        for size in [0, 1, 2, 5, 50]:
            for reverse in [False, True]:
                data = [randint(-100, 100) for _ in range(size)]
                arr = xs_array_create_int(int32(size))
                for i, v in enumerate(data):
                    xs_array_set_int(arr, int32(i), int32(v))
                xs_int_array_sort(arr, reverse)
                self.assertEqual(istr(sorted(data, reverse=reverse)), xs_int_array_to_string(arr))

    def test_xs_int_array_reverse(self):
        for i in range(0, 6):
            arr = xs_int_array_from_range(int32(0), int32(i))
            xs_int_array_reverse(arr)
            self.assertEqual(istr(list(reversed(range(i)))), xs_int_array_to_string(arr))

    def test_xs_int_array_copy(self):
        data = list(range(6))
        arr = xs_int_array_from_range(int32(0), int32(6))
        for start, end in [(0, 6), (2, 4), (-3, 6), (1, -1), (4, 2), (-10, 100)]:
            self.assertEqual(istr(data[start:end]), xs_int_array_to_string(xs_int_array_copy(arr, int32(start), int32(end))))
        self.assertEqual(istr(data), xs_int_array_to_string(xs_int_array_copy(arr)))

    def test_xs_int_array_compare(self):
        a = xs_int_array(int32(1), int32(2))
        self.assertEqual(0, xs_int_array_compare(a, xs_int_array(int32(1), int32(2))))
        self.assertEqual(-1, xs_int_array_compare(a, xs_int_array(int32(1), int32(3))))
        self.assertEqual(1, xs_int_array_compare(a, xs_int_array(int32(1))))
        self.assertEqual(-1, xs_int_array_compare(a, xs_int_array(int32(1), int32(2), int32(0))))

    def test_xs_int_array_aggregates(self):
        arr = xs_int_array(int32(3), int32(-2), int32(8))
        self.assertEqual(9, xs_int_array_sum(arr))
        self.assertEqual(-2, xs_int_array_min(arr))
        self.assertEqual(8, xs_int_array_max(arr))
        self.assertEqual(c_int_array_success, xs_int_array_last_error())
        empty = xs_int_array()
        self.assertEqual(0, xs_int_array_sum(empty))
        self.assertEqual(c_int_array_generic_error, xs_int_array_min(empty))
        self.assertEqual(c_int_array_index_out_of_range_error, xs_int_array_last_error())
        self.assertEqual(c_int_array_generic_error, xs_int_array_max(empty))

    def test_xs_int_array_range_near_int_limits(self):
        for data in [(2147483640, 2147483647, 3), (-2147483647, -2147483643, 1), (-2147483640, -2147483648, -4)]:
            arr = xs_int_array_from_range(*[int32(v) for v in data])
            self.assertEqual(istr(list(range(*data))), xs_int_array_to_string(arr))
        for data in [(-2147483648, 2147483647, 1), (2147483647, -2, -1), (0, 10, -2147483648)]:
            self.assertEqual(c_int_array_generic_error, xs_int_array_from_range(*[int32(v) for v in data]))

    def test_xs_int_array_repeated_array_edge_cases(self):
        empty = xs_int_array()
        self.assertEqual("[]", xs_int_array_to_string(xs_int_array_from_repeated_array(empty, int32(5))))
        arr = xs_int_array(int32(1), int32(2))
        self.assertEqual(c_int_array_generic_error, xs_int_array_from_repeated_array(arr, int32(-1)))
        self.assertEqual(c_int_array_max_capacity_error,
                         xs_int_array_from_repeated_array(arr, c_int_array_max_capacity // 2 + 1))

    def test_xs_int_array_index_edge_cases(self):
        arr = xs_int_array(int32(1), int32(2), int32(3))
        self.assertEqual(c_int_array_generic_error, xs_int_array_index(arr, int32(1), int32(2), int32(1)))
        self.assertEqual(c_int_array_generic_error, xs_int_array_index(arr, int32(1), int32(5)))
        self.assertEqual(0, xs_int_array_index(arr, int32(1), int32(-10)))
        self.assertEqual(2, xs_int_array_index(arr, int32(3), int32(0), int32(100)))

    def test_xs_int_array_empty_array_operations(self):
        empty = xs_int_array()
        self.assertEqual(c_int_array_generic_error, xs_int_array_index(empty, int32(0)))
        self.assertFalse(xs_int_array_contains(empty, int32(0)))
        self.assertEqual(0, xs_int_array_count(empty, int32(0)))
        self.assertEqual(0, xs_int_array_compare(empty, xs_int_array()))
        self.assertEqual(-1, xs_int_array_compare(empty, xs_int_array(int32(0))))
        self.assertEqual(1, xs_int_array_compare(xs_int_array(int32(0)), empty))
        xs_int_array_reverse(empty)
        self.assertEqual("[]", xs_int_array_to_string(empty))
        self.assertEqual("[]", xs_int_array_to_string(xs_int_array_copy(empty)))

    def test_xs_int_array_copy_start_past_end(self):
        arr = xs_int_array(int32(1), int32(2), int32(3))
        self.assertEqual("[]", xs_int_array_to_string(xs_int_array_copy(arr, int32(5))))
        self.assertEqual("[]", xs_int_array_to_string(xs_int_array_copy(arr, int32(3), int32(10))))

    def test_xs_int_array_copy_is_independent(self):
        arr = xs_int_array(int32(1), int32(2))
        copy = xs_int_array_copy(arr)
        xs_array_set_int(copy, int32(0), int32(9))
        self.assertEqual("[1, 2]", xs_int_array_to_string(arr))

    def test_xs_int_array_delete(self):
        arr = xs_int_array(int32(1), int32(2))
        self.assertEqual(c_int_array_success, xs_int_array_delete(arr))
        self.assertEqual(0, xs_array_get_size(arr))


def istr(lst: list[int | int32]) -> str:
    return str([int(x) for x in lst])


if __name__ == "__main__":
    unittest.main()
