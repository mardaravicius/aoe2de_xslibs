import unittest
from random import uniform

from xs.float_array import *


class FloatArrayTest(unittest.TestCase):
    def test_xs_float_array(self):
        for i in range(0, 13):
            data = [float32(v + 0.5) for v in range(i)]
            arr = xs_float_array(*data)
            self.assertEqual(i, xs_array_get_size(arr))
            self.assertEqual(fstr(data), xs_float_array_to_string(arr))

    def test_xs_float_array_stop_at_magic_number(self):
        arr = xs_float_array(float32(1.5), c_float_array_empty_param, float32(2.5))
        self.assertEqual(fstr([1.5]), xs_float_array_to_string(arr))

    def test_xs_float_array_repeated(self):
        self.assertEqual(c_float_array_generic_error, xs_float_array_from_repeated_val(float32(4.5), int32(-1)))
        self.assertEqual(fstr([4.5, 4.5, 4.5]),
                         xs_float_array_to_string(xs_float_array_from_repeated_val(float32(4.5), int32(3))))
        arr = xs_float_array(float32(1.5), float32(2.5))
        self.assertEqual(fstr([1.5, 2.5, 1.5, 2.5, 1.5, 2.5]),
                         xs_float_array_to_string(xs_float_array_from_repeated_array(arr, int32(3))))
        self.assertEqual("[]", xs_float_array_to_string(xs_float_array_from_repeated_array(arr, int32(0))))

    def test_xs_float_array_repeated_array_edge_cases(self):
        empty = xs_float_array()
        self.assertEqual("[]", xs_float_array_to_string(xs_float_array_from_repeated_array(empty, int32(5))))
        arr = xs_float_array(float32(1.5), float32(2.5))
        self.assertEqual(c_float_array_generic_error, xs_float_array_from_repeated_array(arr, int32(-1)))
        self.assertEqual(c_float_array_max_capacity_error,
                         xs_float_array_from_repeated_array(arr, c_float_array_max_capacity // 2 + 1))

    def test_xs_float_array_from_string(self):
        self.assertEqual(fstr([1.0, 1.5, -2.25]),
                         xs_float_array_to_string(xs_float_array_from_string(" 1.0, x,1.5 ,-2.25")))
        self.assertEqual("[]", xs_float_array_to_string(xs_float_array_from_string("  ")))

    def test_xs_float_array_index(self):
        arr = xs_float_array(float32(1.5), float32(2.5), float32(3.5), float32(2.5))
        self.assertEqual(1, xs_float_array_index(arr, float32(2.5)))
        self.assertEqual(3, xs_float_array_index(arr, float32(2.5), int32(2)))
        self.assertEqual(3, xs_float_array_index(arr, float32(2.5), int32(-1)))
        self.assertEqual(c_float_array_generic_error, xs_float_array_index(arr, float32(2.5), int32(0), int32(-3)))
        self.assertTrue(xs_float_array_contains(arr, float32(3.5)))
        self.assertFalse(xs_float_array_contains(arr, float32(4.5)))
        self.assertEqual(2, xs_float_array_count(arr, float32(2.5)))

    def test_xs_float_array_index_edge_cases(self):
        arr = xs_float_array(float32(1.5), float32(2.5), float32(3.5))
        self.assertEqual(c_float_array_generic_error, xs_float_array_index(arr, float32(1.5), int32(2), int32(1)))
        self.assertEqual(c_float_array_generic_error, xs_float_array_index(arr, float32(1.5), int32(5)))
        self.assertEqual(0, xs_float_array_index(arr, float32(1.5), int32(-10)))
        self.assertEqual(2, xs_float_array_index(arr, float32(3.5), int32(0), int32(100)))

    def test_xs_float_array_sort(self):
        for size in [0, 1, 2, 5, 50]:
            for reverse in [False, True]:
                data = [float32(uniform(-100, 100)) for _ in range(size)]
                arr = xs_array_create_float(int32(size))
                for i, v in enumerate(data):
                    xs_array_set_float(arr, int32(i), v)
                xs_float_array_sort(arr, reverse)
                self.assertEqual(fstr(sorted(data, reverse=reverse)), xs_float_array_to_string(arr))

    def test_xs_float_array_reverse(self):
        for i in range(0, 6):
            data = [float32(v + 0.5) for v in range(i)]
            arr = xs_float_array(*data)
            xs_float_array_reverse(arr)
            self.assertEqual(fstr(list(reversed(data))), xs_float_array_to_string(arr))

    def test_xs_float_array_copy(self):
        data = [float32(v + 0.5) for v in range(6)]
        arr = xs_float_array(*data)
        for start, end in [(0, 6), (2, 4), (-3, 6), (1, -1), (4, 2), (-10, 100)]:
            self.assertEqual(fstr(data[start:end]),
                             xs_float_array_to_string(xs_float_array_copy(arr, int32(start), int32(end))))
        self.assertEqual(fstr(data), xs_float_array_to_string(xs_float_array_copy(arr)))

    def test_xs_float_array_copy_start_past_end(self):
        arr = xs_float_array(float32(1.5), float32(2.5), float32(3.5))
        self.assertEqual("[]", xs_float_array_to_string(xs_float_array_copy(arr, int32(5))))
        self.assertEqual("[]", xs_float_array_to_string(xs_float_array_copy(arr, int32(3), int32(10))))

    def test_xs_float_array_copy_is_independent(self):
        arr = xs_float_array(float32(1.5), float32(2.5))
        copy = xs_float_array_copy(arr)
        xs_array_set_float(copy, int32(0), float32(9.5))
        self.assertEqual(fstr([1.5, 2.5]), xs_float_array_to_string(arr))

    def test_xs_float_array_compare(self):
        a = xs_float_array(float32(1.5), float32(2.5))
        self.assertEqual(0, xs_float_array_compare(a, xs_float_array(float32(1.5), float32(2.5))))
        self.assertEqual(-1, xs_float_array_compare(a, xs_float_array(float32(1.5), float32(3.5))))
        self.assertEqual(1, xs_float_array_compare(a, xs_float_array(float32(1.5))))
        self.assertEqual(-1, xs_float_array_compare(a, xs_float_array(float32(1.5), float32(2.5), float32(0.0))))

    def test_xs_float_array_aggregates(self):
        arr = xs_float_array(float32(3.5), float32(-2.25), float32(8.0))
        self.assertAlmostEqual(9.25, xs_float_array_sum(arr), places=5)
        self.assertEqual(float32(-2.25), xs_float_array_min(arr))
        self.assertEqual(float32(8.0), xs_float_array_max(arr))
        self.assertEqual(c_float_array_success, xs_float_array_last_error())
        empty = xs_float_array()
        self.assertEqual(0.0, xs_float_array_sum(empty))
        self.assertEqual(c_float_array_generic_error_float, xs_float_array_min(empty))
        self.assertEqual(c_float_array_index_out_of_range_error, xs_float_array_last_error())
        self.assertEqual(c_float_array_generic_error_float, xs_float_array_max(empty))

    def test_xs_float_array_empty_array_operations(self):
        empty = xs_float_array()
        self.assertEqual(c_float_array_generic_error, xs_float_array_index(empty, float32(0.0)))
        self.assertFalse(xs_float_array_contains(empty, float32(0.0)))
        self.assertEqual(0, xs_float_array_count(empty, float32(0.0)))
        self.assertEqual(0, xs_float_array_compare(empty, xs_float_array()))
        self.assertEqual(-1, xs_float_array_compare(empty, xs_float_array(float32(0.0))))
        self.assertEqual(1, xs_float_array_compare(xs_float_array(float32(0.0)), empty))
        xs_float_array_reverse(empty)
        self.assertEqual("[]", xs_float_array_to_string(empty))
        self.assertEqual("[]", xs_float_array_to_string(xs_float_array_copy(empty)))

    def test_xs_float_array_delete(self):
        arr = xs_float_array(float32(1.5), float32(2.5))
        self.assertEqual(c_float_array_success, xs_float_array_delete(arr))
        self.assertEqual(0, xs_array_get_size(arr))

    def test_xs_float_array_sort_with(self):
        from random import Random
        _r = Random(1)
        for size in [0, 1, 2, 15, 16, 17, 31, 33, 64, 100, 257, 17]:
            for reverse in [False, True]:
                keys = [float32(_r.choice([-1.5, 0.0, 0.25, 2.0])) for _ in range(size)]
                arr = xs_array_create_float(int32(size))
                other = xs_array_create_int(int32(size))
                for i, v in enumerate(keys):
                    xs_array_set_float(arr, int32(i), v)
                    xs_array_set_int(other, int32(i), int32(i))
                self.assertEqual(c_float_array_success, xs_float_array_sort_with(arr, other, reverse))
                expected = sorted(range(size), key=lambda i: keys[i], reverse=reverse)
                self.assertEqual([keys[i] for i in expected], [xs_array_get_float(arr, int32(i)) for i in range(size)])
                self.assertEqual(expected, [int(xs_array_get_int(other, int32(i))) for i in range(size)])

    def test_xs_float_array_sort_with_size_mismatch(self):
        arr = xs_array_create_float(int32(3))
        other = xs_array_create_int(int32(2))
        self.assertEqual(c_float_array_generic_error, xs_float_array_sort_with(arr, other))
        self.assertEqual(c_float_array_generic_error, xs_float_array_sort_with(arr, xs_array_create_int(int32(4))))

    def test_xs_float_array_sort_with_release_buffers(self):
        import xs.float_array as module
        for release, expected_empty in [(True, True), (False, False)]:
            size = 40
            arr = xs_array_create_float(int32(size))
            other = xs_array_create_int(int32(size))
            for i in range(size):
                xs_array_set_float(arr, int32(i), float32(i % 3))
            self.assertEqual(c_float_array_success, xs_float_array_sort_with(arr, other, False, release))
            keys_size = xs_array_get_size(module._float_array_sort_keys)
            values_size = xs_array_get_size(module._float_array_sort_values)
            self.assertEqual(expected_empty, keys_size == 0 and values_size == 0)

    def test_xs_float_array_sort_with_buffer_failure_leaves_input_unchanged(self):
        import xs.float_array as module
        size = 40
        arr = xs_array_create_float(int32(size))
        other = xs_array_create_int(int32(size))
        for i in range(size):
            xs_array_set_float(arr, int32(i), float32(size - i))
            xs_array_set_int(other, int32(i), int32(i))
        before = ([xs_array_get_float(arr, int32(i)) for i in range(size)], [xs_array_get_int(other, int32(i)) for i in range(size)])
        orig_create_int = module.xs_array_create_int
        orig_keys, orig_values = module._float_array_sort_keys, module._float_array_sort_values
        module._float_array_sort_keys = int32(-1)
        module._float_array_sort_values = int32(-1)
        module.xs_array_create_int = lambda *args, **kwargs: int32(-1)
        try:
            self.assertEqual(c_float_array_generic_error, xs_float_array_sort_with(arr, other))
        finally:
            module.xs_array_create_int = orig_create_int
            module._float_array_sort_keys, module._float_array_sort_values = orig_keys, orig_values
        self.assertEqual(before, ([xs_array_get_float(arr, int32(i)) for i in range(size)], [xs_array_get_int(other, int32(i)) for i in range(size)]))





def fstr(lst: list[float | float32]) -> str:
    return str([str(float32(x)) for x in lst]).replace("'", "")


if __name__ == "__main__":
    unittest.main()
