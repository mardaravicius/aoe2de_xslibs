import random
import unittest
from random import randint

from xs.float_list import *
from xs_converter.symbols import f32range


class FloatListTest(unittest.TestCase):
    def test_xs_float_list(self):
        for i in i32range(0, 13):
            params = tuple(f32range(i))
            arr = xs_float_list(*params)
            self.assertEqual(i, xs_float_list_size(arr))
            self.assertEqual(fstr(list(f32range(i))), xs_float_list_to_string(arr))

    def test_xs_float_list_stop_at_magic_number(self):
        arr = xs_float_list(float32(1.1), c_float_list_empty_param, float32(2.2))
        self.assertEqual(fstr([1.1]), xs_float_list_to_string(arr))

    def test_xs_float_list_create_empty(self):
        arr = xs_float_list_create(int32(16))
        self.assertEqual(0, xs_float_list_size(arr))

    def test_xs_float_list_create_fail_at_negative_capacity(self):
        arr = xs_float_list_create(int32(-1))
        self.assertEqual(c_float_list_generic_error, arr)

    def test_xs_float_list_create_fail_over_max_capacity(self):
        arr = xs_float_list_create(c_float_list_max_capacity)
        self.assertEqual(c_float_list_generic_error, arr)
        xs_array_resize_float(arr, 0)

    def test_xs_float_list_from_repeated_val(self):
        arr = xs_float_list_from_repeated_val(float32(5.5), int32(7))
        self.assertEqual(7, xs_float_list_size(arr))
        self.assertEqual("[5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5]", xs_float_list_to_string(arr))

    def test_xs_float_list_from_repeated_val_fail_with_negative_repeat(self):
        arr = xs_float_list_from_repeated_val(float32(5), int32(-2))
        self.assertEqual(c_float_list_generic_error, arr)

    def test_xs_float_list_from_repeated_val_fail_over_max_capacity(self):
        arr = xs_float_list_from_repeated_val(float32(5.5), c_float_list_max_capacity)
        self.assertEqual(c_float_list_generic_error, arr)
        xs_array_resize_float(arr, 0)

    def test_xs_float_list_from_repeated_list(self):
        lst1 = [float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        lst2 = lst1 * 7
        arr1 = xs_float_list(*tuple(lst1))
        arr2 = xs_float_list_from_repeated_list(arr1, int32(7))
        self.assertEqual(fstr(lst2), xs_float_list_to_string(arr2))
        self.assertEqual(len(lst2), xs_float_list_size(arr2))

    def test_xs_float_list_from_array(self):
        arr = xs_array_create_float(10, 5.5)
        arr_lst = xs_float_list_from_array(arr)
        lst = [float32(5.5)] * 10
        self.assertEqual(fstr(lst), xs_float_list_to_string(arr_lst))
        self.assertEqual(xs_array_get_size(arr), xs_float_list_size(arr_lst))
        self.assertEqual(len(lst), xs_float_list_size(arr_lst))

    def test_xs_float_list_from_array_fail_over_max_capacity(self):
        arr = xs_array_create_float(c_float_list_max_capacity, 5.5)
        self.assertEqual(c_float_list_generic_error, xs_float_list_from_array(arr))
        xs_array_resize_float(arr, 0)

    def test_xs_float_list_use_array_as_source(self):
        arr = xs_array_create_float(10, 5.5)
        lst = [float32(5.5)] * 10
        self.assertEqual(c_float_list_success, xs_float_list_use_array_as_source(arr))
        self.assertEqual(fstr(lst), xs_float_list_to_string(arr))
        self.assertEqual(len(lst), xs_float_list_size(arr))
        xs_array_set_float(arr, 1, 2000.2222)
        self.assertEqual(xs_array_get_float(arr, 1), xs_float_list_get(arr, int32(0)))

    def test_xs_float_list_get(self):
        lst = list(f32range(-1.0, 100.0, 1.1))
        arr = xs_float_list_create(int32(101))
        for v in f32range(-1.0, 100.0, 1.1):
            xs_float_list_append(arr, v)
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            self.assertEqual(lst[i], xs_float_list_get(arr, int32(i)))
            self.assertEqual(c_float_list_success, xs_float_list_last_error())

    def test_xs_float_list_get_fail_with_incorrect_idx(self):
        arr = xs_float_list(float32(-1.1), float32(0.0), float32(1.1), float32(2.2))
        self.assertEqual(c_float_list_generic_error, xs_float_list_get(arr, int32(4)))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_last_error())
        self.assertEqual(c_float_list_generic_error, xs_float_list_get(arr, int32(-1)))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_last_error())

    def test_xs_float_list_set(self):
        lst = list(f32range(-1.0, 100.0, 1.1))
        arr = xs_float_list_create(int32(101))
        for v in f32range(-1.0, 100.0, 1.1):
            xs_float_list_append(arr, v)
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            v = random.random()
            self.assertEqual(c_float_list_success, xs_float_list_set(arr, int32(i), float32(v)))
            lst[i] = v
        self.assertEqual(fstr(lst), xs_float_list_to_string(arr))
        self.assertEqual(len(lst), xs_float_list_size(arr))

    def test_xs_float_list_set_fail_with_incorrect_idx(self):
        arr = xs_float_list(float32(-1.1), float32(0.0), float32(1.1), float32(2.2))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_set(arr, int32(4), float32(5.5)))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_set(arr, int32(-1), float32(5.5)))

    def test_xs_float_list_append(self):
        arr = xs_float_list_create()
        lst = []
        for i in f32range(11.0, 22.2, 1.1):
            xs_float_list_append(arr, i)
            lst.append(i)
        self.assertEqual(len(lst), xs_float_list_size(arr))
        self.assertEqual(fstr(lst), xs_float_list_to_string(arr))

    def test_xs_float_list_append_fail_over_max_capacity(self):
        arr = xs_float_list_from_repeated_val(int32(1), c_float_list_max_capacity - 1)
        self.assertLessEqual(0, arr)
        self.assertEqual(c_float_list_max_capacity_error, xs_float_list_append(arr, int32(10)))
        xs_array_resize_float(arr, 0)

    def test_xs_float_list_insert(self):
        lst = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        arr = xs_float_list(*tuple(lst))
        for v in f32range(0.0, 100.0, 1.1):
            i = randint(0, len(lst))
            self.assertEqual(c_float_list_success, xs_float_list_insert(arr, int32(i), v))
            lst.insert(i, v)
        self.assertEqual(fstr(lst), xs_float_list_to_string(arr))
        self.assertEqual(len(lst), xs_float_list_size(arr))

    def test_xs_float_list_insert_fail_with_incorrect_idx(self):
        arr = xs_float_list(float32(1.1), float32(2.2), float32(3.3))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_insert(arr, int32(-1), float32(1.1)))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_insert(arr, int32(4), float32(1.1)))

    def test_xs_float_list_insert_fail_over_max_capacity(self):
        arr = xs_float_list_from_repeated_val(float32(1.1), c_float_list_max_capacity - 1)
        self.assertEqual(c_float_list_max_capacity_error, xs_float_list_insert(arr, int32(100), float32(1.1)))
        xs_array_resize_float(arr, 0)

    def test_xs_float_list_pop(self):
        lst = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        arr = xs_float_list(*tuple(lst))
        for _ in range(len(lst)):
            self.assertEqual(xs_float_list_pop(arr), lst.pop())
            self.assertEqual(xs_float_list_last_error(), c_float_list_success)
        self.assertEqual(xs_float_list_size(arr), len(lst))
        self.assertEqual(xs_float_list_to_string(arr), str(lst))

    def test_xs_float_list_pop_at_index(self):
        arr = xs_float_list_create(int32(201))
        for v in f32range(-1.0, 200.0, 1.1):
            xs_float_list_append(arr, v)
        lst = list(f32range(-1.0, 200.0, 1.1))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            val = lst[i]
            self.assertEqual(val, xs_float_list_pop(arr, int32(i)))
            lst.pop(i)
            self.assertEqual(c_float_list_success, xs_float_list_last_error())
        self.assertEqual(fstr(lst), xs_float_list_to_string(arr))
        self.assertEqual(len(lst), xs_float_list_size(arr))

    def test_xs_float_list_pop_fail_with_incorrect_idx(self):
        arr = xs_float_list(float32(-1.1), float32(0.0), float32(1.1), float32(2.2))
        self.assertEqual(c_float_list_generic_error, xs_float_list_pop(arr, int32(4)))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_last_error())
        self.assertEqual(c_float_list_generic_error, xs_float_list_pop(arr, int32(-1)))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_last_error())

    def test_xs_float_list_remove(self):
        arr = xs_float_list_create(int32(201))
        for v in f32range(-1.1, 200.0, 1.1):
            xs_float_list_append(arr, v)
        lst = list(f32range(-1.1, 200.0, 1.1))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            val = lst[i]
            self.assertEqual(i, xs_float_list_remove(arr, val))
            lst.remove(val)

        self.assertEqual(fstr(lst), xs_float_list_to_string(arr))
        self.assertEqual(len(lst), xs_float_list_size(arr))

    def test_xs_float_list_remove_fail_with_incorrect_idx(self):
        arr = xs_float_list(float32(-1.1), float32(0.0), float32(1.1), float32(2.2))
        self.assertEqual(c_float_list_generic_error, xs_float_list_remove(arr, float32(4.4)))

    def test_xs_float_list_index(self):
        arr = xs_float_list_create(int32(201))
        for v in f32range(-1.1, 200.0, 1.1):
            xs_float_list_append(arr, v)
        lst = list(f32range(-1.1, 200.0, 1.1))
        for _ in range(100):
            val = lst[randint(0, len(lst) - 1)]
            self.assertEqual(lst.index(val), xs_float_list_index(arr, val))

    def test_xs_float_list_index_with_ranges(self):
        arr = xs_float_list()
        lst = []
        for _ in range(500):
            val = float32(random.random())
            xs_float_list_append(arr, val)
            lst.append(val)
        test_data = [
            (0, 0),
            (0, 1),
            (0, 10),
            (0, 10),
            (0, 10),
            (10, 0),
            (10, 0),
            (10, 0),
            (-4, 4),
            (5, -5),
            (-17, -13),
            (-8, -22),
        ]
        for _ in range(100):
            for data in test_data:
                i = randint(0, len(lst) - 1)
                val = lst[i]
                params_xs = (arr, val) + data
                params = (val,) + data
                try:
                    r = lst.index(params[0], params[1], params[2])
                except ValueError:
                    r = c_float_list_generic_error
                self.assertEqual(r, xs_float_list_index(*params_xs))

    def test_xs_float_list_index_fail_with_incorrect_idx(self):
        arr = xs_float_list(float32(1.1), float32(2.2), float32(3.3))
        self.assertEqual(c_float_list_generic_error, xs_float_list_index(arr, float32(4.4)))

    def test_xs_float_list_contains(self):
        arr = xs_float_list(float32(1.1), float32(2.2))
        self.assertTrue(xs_float_list_contains(arr, float32(1.1)))
        self.assertTrue(xs_float_list_contains(arr, float32(2.2)))
        self.assertFalse(xs_float_list_contains(arr, float32(3.3)))

    def test_xs_float_list_sort(self):
        for _ in range(100):
            size = randint(0, 100)
            arr = xs_float_list_create(int32(size))
            lst = []
            for _ in range(size):
                val = float32(random.random())
                xs_float_list_append(arr, val)
                lst.append(val)
            lst.sort()
            xs_float_list_sort(arr)
            self.assertEqual(fstr(lst), xs_float_list_to_string(arr))
            self.assertEqual(len(lst), xs_float_list_size(arr))

    def test_xs_float_list_sort_reverse(self):
        for _ in range(100):
            size = randint(0, 100)
            arr = xs_float_list_create(int32(size))
            lst = []
            for _ in range(size):
                val = float32(random.random())
                xs_float_list_append(arr, val)
                lst.append(val)
            lst.sort(reverse=True)
            xs_float_list_sort(arr, True)
            self.assertEqual(fstr(lst), xs_float_list_to_string(arr))
            self.assertEqual(len(lst), xs_float_list_size(arr))

    def test_xs_float_list_to_string_test(self):
        arr = xs_float_list(float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3))
        self.assertEqual(xs_float_list_to_string(arr), "[-1.1, 0.0, 1.1, 2.2, 3.3]")
        arr_empty = xs_float_list()
        self.assertEqual("[]", xs_float_list_to_string(arr_empty))

    def test_xs_float_list_reverse_even(self):
        lst = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        arr = xs_float_list(*tuple(lst))

        xs_float_list_reverse(arr)
        lst.reverse()

        self.assertEqual(fstr(lst), xs_float_list_to_string(arr))
        self.assertEqual(len(lst), xs_float_list_size(arr))

    def test_xs_float_list_reverse_odd(self):
        lst = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4), float32(5.5)]
        arr = xs_float_list(*tuple(lst))

        xs_float_list_reverse(arr)
        lst.reverse()

        self.assertEqual(fstr(lst), xs_float_list_to_string(arr))
        self.assertEqual(len(lst), xs_float_list_size(arr))

    def test_xs_float_list_reverse_empty(self):
        lst = []
        arr = xs_float_list(*tuple(lst))

        xs_float_list_reverse(arr)
        lst.reverse()

        self.assertEqual(fstr(lst), xs_float_list_to_string(arr))
        self.assertEqual(len(lst), xs_float_list_size(arr))

    def test_xs_float_list_copy(self):
        lst = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        arr = xs_float_list(*tuple(lst))
        copy = xs_float_list_copy(arr)
        self.assertEqual(xs_float_list_to_string(arr), xs_float_list_to_string(copy))
        self.assertEqual(xs_float_list_size(arr), xs_float_list_size(copy))

        xs_float_list_set(arr, int32(0), float32(100.111))
        self.assertEqual(fstr(lst), xs_float_list_to_string(copy))
        self.assertEqual(len(lst), xs_float_list_size(copy))

    def test_xs_float_list_copy_slices(self):
        lst = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        arr = xs_float_list(*tuple(lst))

        for i in i32range(len(lst) * -1, len(lst) + 1):
            for j in i32range(len(lst) * -1, len(lst) + 1):
                copy_arr = xs_float_list_copy(arr, i, j)
                copy_lst = lst[i:j]
                self.assertEqual(fstr(copy_lst), xs_float_list_to_string(copy_arr))
                self.assertEqual(len(copy_lst), xs_float_list_size(copy_arr))

    def test_xs_float_list_extend(self):
        lst1 = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        lst2 = [float32(0.0), float32(-10.11), float32(20.22), float32(-30.33), float32(40.44), float32(-50.55),
                float32(60.66), float32(-70.77), float32(80.88), float32(-90.99)]

        arr1 = xs_float_list(*tuple(lst1))
        arr2 = xs_float_list(*tuple(lst2))
        self.assertEqual(c_float_list_success, xs_float_list_extend(arr1, arr2))
        lst1.extend(lst2)

        self.assertEqual(fstr(lst1), xs_float_list_to_string(arr1))
        self.assertEqual(len(lst1), xs_float_list_size(arr1))

    def test_xs_float_list_extend_with_array(self):
        lst1 = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        lst2 = [float32(5.5)] * 10

        arr1 = xs_float_list(*tuple(lst1))
        arr2 = xs_array_create_float(10, float32(5.5))
        self.assertEqual(c_float_list_success, xs_float_list_extend_with_array(arr1, arr2))
        lst1.extend(lst2)

        self.assertEqual(fstr(lst1), xs_float_list_to_string(arr1))
        self.assertEqual(len(lst1), xs_float_list_size(arr1))

    def test_xs_float_list_clear(self):
        arr = xs_float_list(float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4))

        self.assertEqual(c_float_list_success, xs_float_list_clear(arr))
        self.assertEqual("[]", xs_float_list_to_string(arr))
        self.assertEqual(0, xs_float_list_size(arr))

    def test_xs_float_list_compare(self):
        arr1 = xs_float_list(float32(-1.1), float32(0.0), float32(2.2))
        arr2 = xs_float_list(float32(-1.1), float32(0.0), float32(1.1))

        self.assertEqual(1, xs_float_list_compare(arr1, arr2))
        self.assertEqual(-1, xs_float_list_compare(arr2, arr1))
        self.assertEqual(0, xs_float_list_compare(arr1, arr1))

    def test_xs_float_list_compare_same_prefix(self):
        arr1 = xs_float_list(float32(-1.1), float32(0.0), float32(1.1))
        arr2 = xs_float_list(float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4))

        self.assertEqual(-1, xs_float_list_compare(arr1, arr2))
        self.assertEqual(1, xs_float_list_compare(arr2, arr1))

    def test_xs_float_list_compare_empty(self):
        arr1 = xs_float_list()
        arr2 = xs_float_list()

        self.assertEqual(0, xs_float_list_compare(arr1, arr2))

    def test_xs_float_list_sum_count_min_max(self):
        arr = xs_float_list()
        lst = []
        for _ in range(100):
            v = float32(random.random())
            xs_float_list_append(arr, v)
            lst.append(v)

        self.assertEqual(sum(lst), xs_float_list_sum(arr))
        self.assertEqual(lst.count(lst[0]), xs_float_list_count(arr, lst[0]))
        self.assertEqual(min(lst), xs_float_list_min(arr))
        self.assertEqual(max(lst), xs_float_list_max(arr))

    def test_xs_float_list_sum_count_min_max_on_empty(self):
        arr = xs_float_list()
        lst = []

        self.assertEqual(sum(lst), xs_float_list_sum(arr))
        self.assertEqual(lst.count(float32(1.0)), xs_float_list_count(arr, float32(1.0)))
        self.assertEqual(c_float_list_generic_error, xs_float_list_min(arr))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_last_error())
        self.assertEqual(c_float_list_generic_error, xs_float_list_max(arr))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_last_error())


def fstr(lst: list[float | float32]) -> str:
    return str([str(float32(x)) for x in lst]).replace("'", "")
