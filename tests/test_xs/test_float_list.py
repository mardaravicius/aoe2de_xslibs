import random
import unittest
from random import randint

import xs.float_list as _fl
from xs.float_list import *
from xs_converter.symbols import f32range


class FloatListTest(unittest.TestCase):
    def test_xs_float_list(self):
        for i in i32range(0, 13):
            params = tuple(f32range(i))
            xs_lst = xs_float_list(*params)
            self.assertEqual(i, xs_float_list_size(xs_lst))
            self.assertEqual(fstr(list(f32range(i))), xs_float_list_to_string(xs_lst))

    def test_xs_float_list_stop_at_magic_number(self):
        xs_lst = xs_float_list(float32(1.1), c_float_list_empty_param, float32(2.2))
        self.assertEqual(fstr([1.1]), xs_float_list_to_string(xs_lst))

    def test_xs_float_list_create_empty(self):
        xs_lst = xs_float_list_create(int32(16))
        self.assertEqual(0, xs_float_list_size(xs_lst))

    def test_xs_float_list_create_fail_at_negative_capacity(self):
        xs_lst = xs_float_list_create(int32(-1))
        self.assertEqual(c_float_list_generic_error, xs_lst)

    def test_xs_float_list_create_fail_over_max_capacity(self):
        xs_lst = xs_float_list_create(c_float_list_max_capacity)
        self.assertEqual(c_float_list_generic_error, xs_lst)
        xs_float_list_clear(xs_lst)

    def test_xs_float_list_from_repeated_val(self):
        xs_lst = xs_float_list_from_repeated_val(float32(5.5), int32(7))
        self.assertEqual(7, xs_float_list_size(xs_lst))
        self.assertEqual("[5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5]", xs_float_list_to_string(xs_lst))

    def test_xs_float_list_from_repeated_val_fail_with_negative_repeat(self):
        xs_lst = xs_float_list_from_repeated_val(float32(5), int32(-2))
        self.assertEqual(c_float_list_generic_error, xs_lst)

    def test_xs_float_list_from_repeated_val_fail_over_max_capacity(self):
        xs_lst = xs_float_list_from_repeated_val(float32(5.5), c_float_list_max_capacity)
        self.assertEqual(c_float_list_generic_error, xs_lst)
        xs_float_list_clear(xs_lst)

    def test_xs_float_list_from_repeated_list(self):
        lst1 = [float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        lst2 = lst1 * 7
        xs_lst1 = xs_float_list(*tuple(lst1))
        xs_lst2 = xs_float_list_from_repeated_list(xs_lst1, int32(7))
        self.assertEqual(fstr(lst2), xs_float_list_to_string(xs_lst2))
        self.assertEqual(len(lst2), xs_float_list_size(xs_lst2))

    def test_xs_float_list_from_repeated_list_negative_times(self):
        xs_lst = xs_float_list(float32(1.1), float32(2.2), float32(3.3))
        result = xs_float_list_from_repeated_list(xs_lst, int32(-1))
        self.assertEqual(c_float_list_generic_error, result)

    def test_xs_float_list_from_repeated_list_zero_times(self):
        xs_lst = xs_float_list(float32(1.1), float32(2.2), float32(3.3))
        result = xs_float_list_from_repeated_list(xs_lst, int32(0))
        self.assertGreaterEqual(result, 0)
        self.assertEqual(0, xs_float_list_size(result))

    def test_xs_float_list_from_repeated_list_overflow(self):
        xs_lst = xs_float_list(float32(1.1), float32(2.2), float32(3.3))
        result = xs_float_list_from_repeated_list(xs_lst, c_float_list_max_capacity)
        self.assertEqual(c_float_list_max_capacity_error, result)

    def test_xs_float_list_from_repeated_list_overflow_exact_boundary(self):
        orig = _fl.c_float_list_max_capacity
        _fl.c_float_list_max_capacity = int32(9)
        xs_lst = xs_float_list(float32(1.0), float32(2.0), float32(3.0))
        result = xs_float_list_from_repeated_list(xs_lst, int32(3))
        _fl.c_float_list_max_capacity = orig
        self.assertEqual(c_float_list_max_capacity_error, result)

    def test_xs_float_list_from_array(self):
        xs_arr = xs_array_create_float(10, 5.5)
        xs_lst = xs_float_list_from_array(xs_arr)
        lst = [float32(5.5)] * 10
        self.assertEqual(fstr(lst), xs_float_list_to_string(xs_lst))
        self.assertEqual(xs_array_get_size(xs_arr), xs_float_list_size(xs_lst))
        self.assertEqual(len(lst), xs_float_list_size(xs_lst))

    def test_xs_float_list_from_array_fail_over_max_capacity(self):
        orig = _fl.c_float_list_max_capacity
        _fl.c_float_list_max_capacity = int32(1000)
        xs_arr = xs_array_create_float(_fl.c_float_list_max_capacity, 5.5)
        self.assertEqual(c_float_list_generic_error, xs_float_list_from_array(xs_arr))
        xs_array_resize_float(xs_arr, 0)
        _fl.c_float_list_max_capacity = orig

    def test_xs_float_list_use_array_as_source(self):
        xs_arr = xs_array_create_float(10, 5.5)
        lst = [float32(5.5)] * 10
        xs_lst = xs_float_list_use_array_as_source(xs_arr)
        self.assertEqual(fstr(lst), xs_float_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_float_list_size(xs_lst))
        xs_array_set_float(xs_arr, 1, 2000.2222)
        self.assertEqual(xs_array_get_float(xs_arr, 1), xs_float_list_get(xs_lst, int32(0)))

    def test_xs_float_list_get(self):
        lst = list(f32range(-1.0, 100.0, 1.1))
        xs_lst = xs_float_list_create(int32(101))
        for v in f32range(-1.0, 100.0, 1.1):
            xs_float_list_append(xs_lst, v)
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            self.assertEqual(lst[i], xs_float_list_get(xs_lst, int32(i)))
            self.assertEqual(c_float_list_success, xs_float_list_last_error())

    def test_xs_float_list_get_fail_with_incorrect_idx(self):
        xs_lst = xs_float_list(float32(-1.1), float32(0.0), float32(1.1), float32(2.2))
        self.assertEqual(c_float_list_generic_error, xs_float_list_get(xs_lst, int32(4)))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_last_error())
        self.assertEqual(c_float_list_generic_error, xs_float_list_get(xs_lst, int32(-1)))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_last_error())

    def test_xs_float_list_set(self):
        lst = list(f32range(-1.0, 100.0, 1.1))
        xs_lst = xs_float_list_create(int32(101))
        for v in f32range(-1.0, 100.0, 1.1):
            xs_float_list_append(xs_lst, v)
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            v = random.random()
            self.assertEqual(c_float_list_success, xs_float_list_set(xs_lst, int32(i), float32(v)))
            lst[i] = v
        self.assertEqual(fstr(lst), xs_float_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_float_list_size(xs_lst))

    def test_xs_float_list_set_fail_with_incorrect_idx(self):
        xs_lst = xs_float_list(float32(-1.1), float32(0.0), float32(1.1), float32(2.2))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_set(xs_lst, int32(4), float32(5.5)))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_set(xs_lst, int32(-1), float32(5.5)))

    def test_xs_float_list_append(self):
        xs_lst = xs_float_list_create()
        lst = []
        for i in f32range(11.0, 22.2, 1.1):
            xs_float_list_append(xs_lst, i)
            lst.append(i)
        self.assertEqual(len(lst), xs_float_list_size(xs_lst))
        self.assertEqual(fstr(lst), xs_float_list_to_string(xs_lst))

    def test_xs_float_list_append_fail_over_max_capacity(self):
        orig = _fl.c_float_list_max_capacity
        _fl.c_float_list_max_capacity = int32(1000)
        xs_lst = xs_float_list_from_repeated_val(float32(1.0), _fl.c_float_list_max_capacity - 1)
        self.assertLessEqual(0, xs_lst)
        self.assertEqual(c_float_list_max_capacity_error, xs_float_list_append(xs_lst, float32(10.0)))
        xs_float_list_clear(xs_lst)
        _fl.c_float_list_max_capacity = orig

    def test_xs_float_list_insert(self):
        lst = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        xs_lst = xs_float_list(*tuple(lst))
        for v in f32range(0.0, 100.0, 1.1):
            i = randint(0, len(lst))
            self.assertEqual(c_float_list_success, xs_float_list_insert(xs_lst, int32(i), v))
            lst.insert(i, v)
        self.assertEqual(fstr(lst), xs_float_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_float_list_size(xs_lst))

    def test_xs_float_list_insert_fail_with_incorrect_idx(self):
        xs_lst = xs_float_list(float32(1.1), float32(2.2), float32(3.3))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_insert(xs_lst, int32(-1), float32(1.1)))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_insert(xs_lst, int32(4), float32(1.1)))

    def test_xs_float_list_insert_fail_over_max_capacity(self):
        orig = _fl.c_float_list_max_capacity
        _fl.c_float_list_max_capacity = int32(1000)
        xs_lst = xs_float_list_from_repeated_val(float32(1.1), _fl.c_float_list_max_capacity - 1)
        self.assertEqual(c_float_list_max_capacity_error, xs_float_list_insert(xs_lst, int32(100), float32(1.1)))
        xs_float_list_clear(xs_lst)
        _fl.c_float_list_max_capacity = orig

    def test_xs_float_list_pop(self):
        lst = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        xs_lst = xs_float_list(*tuple(lst))
        for _ in range(len(lst)):
            self.assertEqual(xs_float_list_pop(xs_lst), lst.pop())
            self.assertEqual(xs_float_list_last_error(), c_float_list_success)
        self.assertEqual(xs_float_list_size(xs_lst), len(lst))
        self.assertEqual(xs_float_list_to_string(xs_lst), str(lst))

    def test_xs_float_list_pop_at_index(self):
        xs_lst = xs_float_list_create(int32(201))
        for v in f32range(-1.0, 200.0, 1.1):
            xs_float_list_append(xs_lst, v)
        lst = list(f32range(-1.0, 200.0, 1.1))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            val = lst[i]
            self.assertEqual(val, xs_float_list_pop(xs_lst, int32(i)))
            lst.pop(i)
            self.assertEqual(c_float_list_success, xs_float_list_last_error())
        self.assertEqual(fstr(lst), xs_float_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_float_list_size(xs_lst))

    def test_xs_float_list_pop_fail_with_incorrect_idx(self):
        xs_lst = xs_float_list(float32(-1.1), float32(0.0), float32(1.1), float32(2.2))
        self.assertEqual(c_float_list_generic_error, xs_float_list_pop(xs_lst, int32(4)))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_last_error())
        self.assertEqual(c_float_list_generic_error, xs_float_list_pop(xs_lst, int32(-1)))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_last_error())

    def test_xs_float_list_pop_empty_list(self):
        xs_lst = xs_float_list_create()
        self.assertEqual(0, xs_float_list_size(xs_lst))
        result = xs_float_list_pop(xs_lst)
        self.assertEqual(c_float_list_generic_error_float, result)
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_last_error())
        self.assertEqual(0, xs_float_list_size(xs_lst))

    def test_xs_float_list_pop_until_empty_then_pop_again(self):
        xs_lst = xs_float_list(float32(1.1), float32(2.2))
        self.assertEqual(float32(2.2), xs_float_list_pop(xs_lst))
        self.assertEqual(float32(1.1), xs_float_list_pop(xs_lst))
        self.assertEqual(0, xs_float_list_size(xs_lst))
        result = xs_float_list_pop(xs_lst)
        self.assertEqual(c_float_list_generic_error_float, result)
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_last_error())
        self.assertEqual(0, xs_float_list_size(xs_lst))
        self.assertEqual("[]", xs_float_list_to_string(xs_lst))

    def test_xs_float_list_pop_append_cycle(self):
        xs_lst = xs_float_list_create(int32(4))
        lst = []
        for i in range(20):
            xs_float_list_append(xs_lst, float32(i))
            lst.append(float32(i))
        for _ in range(15):
            lst.pop()
            xs_float_list_pop(xs_lst)
        for i in range(100, 120):
            xs_float_list_append(xs_lst, float32(i))
            lst.append(float32(i))
        self.assertEqual(fstr(lst), xs_float_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_float_list_size(xs_lst))

    def test_xs_float_list_shrink_after_pop_then_append(self):
        xs_lst = xs_float_list_create(int32(0))
        for i in range(50):
            xs_float_list_append(xs_lst, float32(i))
        for _ in range(40):
            xs_float_list_pop(xs_lst)
        remaining = [float32(i) for i in range(10)]
        self.assertEqual(fstr(remaining), xs_float_list_to_string(xs_lst))
        self.assertEqual(10, xs_float_list_size(xs_lst))
        xs_float_list_append(xs_lst, float32(99.0))
        remaining.append(float32(99.0))
        self.assertEqual(fstr(remaining), xs_float_list_to_string(xs_lst))
        self.assertEqual(11, xs_float_list_size(xs_lst))

    def test_xs_float_list_remove(self):
        xs_lst = xs_float_list_create(int32(201))
        for v in f32range(-1.1, 200.0, 1.1):
            xs_float_list_append(xs_lst, v)
        lst = list(f32range(-1.1, 200.0, 1.1))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            val = lst[i]
            self.assertEqual(i, xs_float_list_remove(xs_lst, val))
            lst.remove(val)

        self.assertEqual(fstr(lst), xs_float_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_float_list_size(xs_lst))

    def test_xs_float_list_remove_fail_with_incorrect_idx(self):
        xs_lst = xs_float_list(float32(-1.1), float32(0.0), float32(1.1), float32(2.2))
        self.assertEqual(c_float_list_generic_error, xs_float_list_remove(xs_lst, float32(4.4)))

    def test_xs_float_list_index(self):
        xs_lst = xs_float_list_create(int32(201))
        for v in f32range(-1.1, 200.0, 1.1):
            xs_float_list_append(xs_lst, v)
        lst = list(f32range(-1.1, 200.0, 1.1))
        for _ in range(100):
            val = lst[randint(0, len(lst) - 1)]
            self.assertEqual(lst.index(val), xs_float_list_index(xs_lst, val))

    def test_xs_float_list_index_with_ranges(self):
        xs_lst = xs_float_list()
        lst = []
        for _ in range(500):
            val = float32(random.random())
            xs_float_list_append(xs_lst, val)
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
                params_xs = (xs_lst, val) + data
                params = (val,) + data
                try:
                    r = lst.index(params[0], params[1], params[2])
                except ValueError:
                    r = c_float_list_generic_error
                self.assertEqual(r, xs_float_list_index(*params_xs))

    def test_xs_float_list_index_fail_with_incorrect_idx(self):
        xs_lst = xs_float_list(float32(1.1), float32(2.2), float32(3.3))
        self.assertEqual(c_float_list_generic_error, xs_float_list_index(xs_lst, float32(4.4)))

    def test_xs_float_list_contains(self):
        xs_lst = xs_float_list(float32(1.1), float32(2.2))
        self.assertTrue(xs_float_list_contains(xs_lst, float32(1.1)))
        self.assertTrue(xs_float_list_contains(xs_lst, float32(2.2)))
        self.assertFalse(xs_float_list_contains(xs_lst, float32(3.3)))

    def test_xs_float_list_sort(self):
        for _ in range(100):
            size = randint(0, 100)
            xs_lst = xs_float_list_create(int32(0))
            lst = []
            for _ in range(size):
                val = float32(random.random())
                xs_float_list_append(xs_lst, val)
                lst.append(val)
            lst.sort()
            xs_float_list_sort(xs_lst)
            self.assertEqual(fstr(lst), xs_float_list_to_string(xs_lst))
            self.assertEqual(len(lst), xs_float_list_size(xs_lst))

    def test_xs_float_list_sort_reverse(self):
        for _ in range(100):
            size = randint(0, 100)
            xs_lst = xs_float_list_create(int32(size))
            lst = []
            for _ in range(size):
                val = float32(random.random())
                xs_float_list_append(xs_lst, val)
                lst.append(val)
            lst.sort(reverse=True)
            xs_float_list_sort(xs_lst, True)
            self.assertEqual(fstr(lst), xs_float_list_to_string(xs_lst))
            self.assertEqual(len(lst), xs_float_list_size(xs_lst))

    def test_xs_float_list_sort_single_element(self):
        xs_lst = xs_float_list(float32(4.2))
        xs_float_list_sort(xs_lst)
        self.assertEqual(fstr([4.2]), xs_float_list_to_string(xs_lst))

    def test_xs_float_list_sort_two_elements(self):
        xs_lst = xs_float_list(float32(5.5), float32(3.3))
        xs_float_list_sort(xs_lst)
        self.assertEqual(fstr([3.3, 5.5]), xs_float_list_to_string(xs_lst))
        xs_lst2 = xs_float_list(float32(5.5), float32(3.3))
        xs_float_list_sort(xs_lst2, True)
        self.assertEqual(fstr([5.5, 3.3]), xs_float_list_to_string(xs_lst2))

    def test_xs_float_list_sort_empty(self):
        xs_lst = xs_float_list()
        xs_float_list_sort(xs_lst)
        self.assertEqual("[]", xs_float_list_to_string(xs_lst))

    def test_xs_float_list_to_string_test(self):
        xs_lst = xs_float_list(float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3))
        self.assertEqual("[-1.1, 0.0, 1.1, 2.2, 3.3]", xs_float_list_to_string(xs_lst))
        xs_lst_empty = xs_float_list()
        self.assertEqual("[]", xs_float_list_to_string(xs_lst_empty))

    def test_xs_float_list_reverse_even(self):
        lst = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        xs_lst = xs_float_list(*tuple(lst))

        xs_float_list_reverse(xs_lst)
        lst.reverse()

        self.assertEqual(fstr(lst), xs_float_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_float_list_size(xs_lst))

    def test_xs_float_list_reverse_odd(self):
        lst = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4), float32(5.5)]
        xs_lst = xs_float_list(*tuple(lst))

        xs_float_list_reverse(xs_lst)
        lst.reverse()

        self.assertEqual(fstr(lst), xs_float_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_float_list_size(xs_lst))

    def test_xs_float_list_reverse_empty(self):
        lst = []
        xs_lst = xs_float_list(*tuple(lst))

        xs_float_list_reverse(xs_lst)
        lst.reverse()

        self.assertEqual(fstr(lst), xs_float_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_float_list_size(xs_lst))

    def test_xs_float_list_copy(self):
        lst = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        xs_lst = xs_float_list(*tuple(lst))
        xs_copy = xs_float_list_copy(xs_lst)
        self.assertEqual(xs_float_list_to_string(xs_lst), xs_float_list_to_string(xs_copy))
        self.assertEqual(xs_float_list_size(xs_lst), xs_float_list_size(xs_copy))

        xs_float_list_set(xs_lst, int32(0), float32(100.111))
        self.assertEqual(fstr(lst), xs_float_list_to_string(xs_copy))
        self.assertEqual(len(lst), xs_float_list_size(xs_copy))

    def test_xs_float_list_copy_slices(self):
        lst = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        xs_lst = xs_float_list(*tuple(lst))

        for i in i32range(len(lst) * -1, len(lst) + 1):
            for j in i32range(len(lst) * -1, len(lst) + 1):
                xs_copy = xs_float_list_copy(xs_lst, i, j)
                copy_lst = lst[i:j]
                self.assertEqual(fstr(copy_lst), xs_float_list_to_string(xs_copy))
                self.assertEqual(len(copy_lst), xs_float_list_size(xs_copy))

    def test_xs_float_list_copy_empty(self):
        xs_lst = xs_float_list()
        xs_copy = xs_float_list_copy(xs_lst)
        self.assertEqual(0, xs_float_list_size(xs_copy))
        self.assertEqual("[]", xs_float_list_to_string(xs_copy))

    def test_xs_float_list_copy_single_element(self):
        xs_lst = xs_float_list(float32(4.2))
        xs_copy = xs_float_list_copy(xs_lst)
        self.assertEqual(1, xs_float_list_size(xs_copy))
        self.assertEqual(fstr([4.2]), xs_float_list_to_string(xs_copy))

    def test_xs_float_list_extend(self):
        lst1 = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        lst2 = [float32(0.0), float32(-10.11), float32(20.22), float32(-30.33), float32(40.44), float32(-50.55),
                float32(60.66), float32(-70.77), float32(80.88), float32(-90.99)]

        xs_lst1 = xs_float_list(*tuple(lst1))
        xs_lst2 = xs_float_list(*tuple(lst2))
        self.assertEqual(c_float_list_success, xs_float_list_extend(xs_lst1, xs_lst2))
        lst1.extend(lst2)

        self.assertEqual(fstr(lst1), xs_float_list_to_string(xs_lst1))
        self.assertEqual(len(lst1), xs_float_list_size(xs_lst1))

    def test_xs_float_list_extend_at_exact_capacity_boundary(self):
        lst1 = [float32(i) for i in range(12)]
        xs_lst1 = xs_float_list(*lst1)
        self.assertEqual(13, xs_array_get_size(xs_lst1))
        xs_lst2 = xs_float_list(float32(99.0))
        self.assertEqual(c_float_list_success, xs_float_list_extend(xs_lst1, xs_lst2))
        lst1.append(float32(99.0))
        self.assertEqual(13, xs_float_list_size(xs_lst1))
        self.assertEqual(fstr(lst1), xs_float_list_to_string(xs_lst1))

    def test_xs_float_list_extend_fills_exactly(self):
        lst1 = [float32(i) for i in range(7)]
        lst2 = [float32(i) for i in range(10, 16)]
        xs_lst1 = xs_float_list(*lst1)
        xs_lst2 = xs_float_list(*lst2)
        self.assertEqual(c_float_list_success, xs_float_list_extend(xs_lst1, xs_lst2))
        lst1.extend(lst2)
        self.assertEqual(fstr(lst1), xs_float_list_to_string(xs_lst1))
        self.assertEqual(len(lst1), xs_float_list_size(xs_lst1))

    def test_xs_float_list_extend_with_array(self):
        lst1 = [float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4)]
        lst2 = [float32(5.5)] * 10

        xs_lst = xs_float_list(*tuple(lst1))
        xs_arr = xs_array_create_float(10, float32(5.5))
        self.assertEqual(c_float_list_success, xs_float_list_extend_with_array(xs_lst, xs_arr))
        lst1.extend(lst2)

        self.assertEqual(fstr(lst1), xs_float_list_to_string(xs_lst))
        self.assertEqual(len(lst1), xs_float_list_size(xs_lst))

    def test_xs_float_list_extend_with_array_at_exact_capacity_boundary(self):
        lst1 = [float32(i) for i in range(12)]
        xs_lst = xs_float_list(*lst1)
        self.assertEqual(13, xs_array_get_size(xs_lst))
        xs_arr = xs_array_create_float(1, float32(99.0))
        self.assertEqual(c_float_list_success, xs_float_list_extend_with_array(xs_lst, xs_arr))
        lst1.append(float32(99.0))
        self.assertEqual(13, xs_float_list_size(xs_lst))
        self.assertEqual(fstr(lst1), xs_float_list_to_string(xs_lst))

    def test_xs_float_list_clear(self):
        xs_lst = xs_float_list(float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4))

        self.assertEqual(c_float_list_success, xs_float_list_clear(xs_lst))
        self.assertEqual("[]", xs_float_list_to_string(xs_lst))
        self.assertEqual(0, xs_float_list_size(xs_lst))

    def test_xs_float_list_clear_shrinks_large_capacity(self):
        xs_lst = xs_float_list_create(int32(100))
        xs_float_list_append(xs_lst, float32(1.0))
        xs_float_list_append(xs_lst, float32(2.0))
        xs_float_list_append(xs_lst, float32(3.0))
        self.assertEqual(3, xs_float_list_size(xs_lst))
        capacity_before = xs_array_get_size(xs_lst)
        self.assertGreater(capacity_before, 8)
        self.assertEqual(c_float_list_success, xs_float_list_clear(xs_lst))
        self.assertEqual(0, xs_float_list_size(xs_lst))
        capacity_after = xs_array_get_size(xs_lst)
        self.assertLessEqual(capacity_after, 8)

    def test_xs_float_list_clear_small_list(self):
        xs_lst = xs_float_list(float32(1.1), float32(2.2))
        self.assertEqual(c_float_list_success, xs_float_list_clear(xs_lst))
        self.assertEqual(0, xs_float_list_size(xs_lst))

    def test_xs_float_list_compare(self):
        xs_lst1 = xs_float_list(float32(-1.1), float32(0.0), float32(2.2))
        xs_lst2 = xs_float_list(float32(-1.1), float32(0.0), float32(1.1))

        self.assertEqual(1, xs_float_list_compare(xs_lst1, xs_lst2))
        self.assertEqual(-1, xs_float_list_compare(xs_lst2, xs_lst1))
        self.assertEqual(0, xs_float_list_compare(xs_lst1, xs_lst1))

    def test_xs_float_list_compare_same_prefix(self):
        xs_lst1 = xs_float_list(float32(-1.1), float32(0.0), float32(1.1))
        xs_lst2 = xs_float_list(float32(-1.1), float32(0.0), float32(1.1), float32(2.2), float32(3.3), float32(4.4))

        self.assertEqual(-1, xs_float_list_compare(xs_lst1, xs_lst2))
        self.assertEqual(1, xs_float_list_compare(xs_lst2, xs_lst1))

    def test_xs_float_list_compare_empty(self):
        xs_lst1 = xs_float_list()
        xs_lst2 = xs_float_list()

        self.assertEqual(0, xs_float_list_compare(xs_lst1, xs_lst2))

    def test_xs_float_list_sum_count_min_max(self):
        xs_lst = xs_float_list()
        lst = []
        for _ in range(100):
            v = float32(random.random())
            xs_float_list_append(xs_lst, v)
            lst.append(v)

        self.assertEqual(sum(lst), xs_float_list_sum(xs_lst))
        self.assertEqual(lst.count(lst[0]), xs_float_list_count(xs_lst, lst[0]))
        self.assertEqual(min(lst), xs_float_list_min(xs_lst))
        self.assertEqual(max(lst), xs_float_list_max(xs_lst))

    def test_xs_float_list_sum_count_min_max_on_empty(self):
        xs_lst = xs_float_list()
        lst = []

        self.assertEqual(sum(lst), xs_float_list_sum(xs_lst))
        self.assertEqual(lst.count(float32(1.0)), xs_float_list_count(xs_lst, float32(1.0)))
        self.assertEqual(c_float_list_generic_error, xs_float_list_min(xs_lst))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_last_error())
        self.assertEqual(c_float_list_generic_error, xs_float_list_max(xs_lst))
        self.assertEqual(c_float_list_index_out_of_range_error, xs_float_list_last_error())


def fstr(lst: list[float | float32]) -> str:
    return str([str(float32(x)) for x in lst]).replace("'", "")
