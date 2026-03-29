import random
import unittest
from random import randint

from xs.vector_list import *
from xs.vector_list import xs_vector_list_capacity
import xs.vector_list as _vl


class VectorListTest(unittest.TestCase):
    def test_xs_vector_list(self):
        for i in i32range(0, 13):
            params = tuple(vector(float(j), float(j) + 0.1, float(j) + 0.2) for j in range(i))
            xs_lst = xs_vector_list(*params)
            self.assertEqual(i, xs_vector_list_size(xs_lst))
            self.assertEqual(vstr(list(params)), xs_vector_list_to_string(xs_lst))

    def test_xs_vector_list_stop_at_magic_number(self):
        xs_lst = xs_vector_list(vector(1.1, 2.2, 3.3), c_vector_list_empty_param, vector(4.4, 5.5, 6.6))
        self.assertEqual(vstr([vector(1.1, 2.2, 3.3)]), xs_vector_list_to_string(xs_lst))

    def test_xs_vector_list_create_empty(self):
        xs_lst = xs_vector_list_create(int32(16))
        self.assertEqual(0, xs_vector_list_size(xs_lst))

    def test_xs_vector_list_create_fail_at_negative_capacity(self):
        xs_lst = xs_vector_list_create(int32(-1))
        self.assertEqual(c_vector_list_generic_error, xs_lst)

    def test_xs_vector_list_create_fail_over_max_capacity(self):
        xs_lst = xs_vector_list_create(c_vector_list_max_capacity)
        self.assertEqual(c_vector_list_generic_error, xs_lst)
        xs_vector_list_clear(xs_lst)

    def test_xs_vector_list_from_repeated_val(self):
        v = vector(5.5, 6.6, 7.7)
        xs_lst = xs_vector_list_from_repeated_val(v, int32(7))
        self.assertEqual(7, xs_vector_list_size(xs_lst))
        self.assertEqual(vstr([v] * 7), xs_vector_list_to_string(xs_lst))

    def test_xs_vector_list_from_repeated_val_fail_with_negative_repeat(self):
        xs_lst = xs_vector_list_from_repeated_val(vector(5.0, 5.0, 5.0), int32(-2))
        self.assertEqual(c_vector_list_generic_error, xs_lst)

    def test_xs_vector_list_from_repeated_val_fail_over_max_capacity(self):
        xs_lst = xs_vector_list_from_repeated_val(vector(5.5, 6.6, 7.7), c_vector_list_max_capacity)
        self.assertEqual(c_vector_list_generic_error, xs_lst)
        xs_vector_list_clear(xs_lst)

    def test_xs_vector_list_from_repeated_list(self):
        lst1 = [vector(1.1, 2.2, 3.3), vector(4.4, 5.5, 6.6), vector(7.7, 8.8, 9.9), vector(10.1, 11.2, 12.3)]
        lst2 = lst1 * 7
        xs_lst1 = xs_vector_list(*tuple(lst1))
        xs_lst2 = xs_vector_list_from_repeated_list(xs_lst1, int32(7))
        self.assertEqual(vstr(lst2), xs_vector_list_to_string(xs_lst2))
        self.assertEqual(len(lst2), xs_vector_list_size(xs_lst2))

    def test_xs_vector_list_from_repeated_list_negative_times(self):
        xs_lst = xs_vector_list(vector(1.1, 2.2, 3.3), vector(4.4, 5.5, 6.6), vector(7.7, 8.8, 9.9))
        result = xs_vector_list_from_repeated_list(xs_lst, int32(-1))
        self.assertEqual(c_vector_list_generic_error, result)

    def test_xs_vector_list_from_repeated_list_zero_times(self):
        xs_lst = xs_vector_list(vector(1.1, 2.2, 3.3), vector(4.4, 5.5, 6.6), vector(7.7, 8.8, 9.9))
        result = xs_vector_list_from_repeated_list(xs_lst, int32(0))
        self.assertGreaterEqual(result, 0)
        self.assertEqual(0, xs_vector_list_size(result))

    def test_xs_vector_list_from_repeated_list_overflow(self):
        xs_lst = xs_vector_list(vector(1.1, 2.2, 3.3), vector(4.4, 5.5, 6.6), vector(7.7, 8.8, 9.9))
        result = xs_vector_list_from_repeated_list(xs_lst, c_vector_list_max_capacity)
        self.assertEqual(c_vector_list_max_capacity_error, result)

    def test_xs_vector_list_from_repeated_list_overflow_exact_boundary(self):
        orig = _vl.c_vector_list_max_capacity
        _vl.c_vector_list_max_capacity = int32(9)
        xs_lst = xs_vector_list(vector(1.0, 0.0, 0.0), vector(0.0, 1.0, 0.0), vector(0.0, 0.0, 1.0))
        result = xs_vector_list_from_repeated_list(xs_lst, int32(3))
        _vl.c_vector_list_max_capacity = orig
        self.assertEqual(c_vector_list_max_capacity_error, result)

    def test_xs_vector_list_from_array(self):
        v = vector(5.5, 6.6, 7.7)
        xs_arr = xs_array_create_vector(10, v)
        xs_lst = xs_vector_list_from_array(xs_arr)
        lst = [v] * 10
        self.assertEqual(vstr(lst), xs_vector_list_to_string(xs_lst))
        self.assertEqual(xs_array_get_size(xs_arr), xs_vector_list_size(xs_lst))
        self.assertEqual(len(lst), xs_vector_list_size(xs_lst))

    def test_xs_vector_list_from_array_fail_over_max_capacity(self):
        orig = _vl.c_vector_list_max_capacity
        _vl.c_vector_list_max_capacity = int32(1000)
        xs_arr = xs_array_create_vector(_vl.c_vector_list_max_capacity, vector(5.5, 6.6, 7.7))
        self.assertEqual(c_vector_list_generic_error, xs_vector_list_from_array(xs_arr))
        xs_array_resize_vector(xs_arr, 0)
        _vl.c_vector_list_max_capacity = orig

    # def test_xs_vector_list_use_array_as_source(self):
    #     v = vector(5.5, 6.6, 7.7)
    #     xs_arr = xs_array_create_vector(10, v)
    #     lst = [v] * 10
    #     xs_lst = xs_vector_list_use_array_as_source(xs_arr)
    #     self.assertEqual(vstr(lst), xs_vector_list_to_string(xs_lst))
    #     self.assertEqual(len(lst), xs_vector_list_size(xs_lst))
    #     xs_array_set_vector(xs_arr, 1, vector(2000.2, 3000.3, 4000.4))
    #     self.assertEqual(xs_array_get_vector(xs_arr, 1), xs_vector_list_get(xs_lst, int32(0)))

    def test_xs_vector_list_get(self):
        lst = [vector(float(i), float(i) + 0.1, float(i) + 0.2) for i in range(-1, 100)]
        xs_lst = xs_vector_list_create(int32(101))
        for v in lst:
            xs_vector_list_append(xs_lst, v)
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            self.assertEqual(lst[i], xs_vector_list_get(xs_lst, int32(i)))
            self.assertEqual(c_vector_list_success, xs_vector_list_last_error())

    def test_xs_vector_list_get_fail_with_incorrect_idx(self):
        xs_lst = xs_vector_list(vector(-1.1, 0.0, 1.1), vector(0.0, 1.1, 2.2),
                                vector(1.1, 2.2, 3.3), vector(2.2, 3.3, 4.4))
        self.assertEqual(c_vector_list_generic_error_vector, xs_vector_list_get(xs_lst, int32(4)))
        self.assertEqual(c_vector_list_index_out_of_range_error, xs_vector_list_last_error())
        self.assertEqual(c_vector_list_generic_error_vector, xs_vector_list_get(xs_lst, int32(-1)))
        self.assertEqual(c_vector_list_index_out_of_range_error, xs_vector_list_last_error())

    def test_xs_vector_list_set(self):
        lst = [vector(float(i), float(i) + 0.1, float(i) + 0.2) for i in range(-1, 100)]
        xs_lst = xs_vector_list_create(int32(101))
        for v in lst:
            xs_vector_list_append(xs_lst, v)
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            v = vector(random.random(), random.random(), random.random())
            self.assertEqual(c_vector_list_success, xs_vector_list_set(xs_lst, int32(i), v))
            lst[i] = v
        self.assertEqual(vstr(lst), xs_vector_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_vector_list_size(xs_lst))

    def test_xs_vector_list_set_fail_with_incorrect_idx(self):
        xs_lst = xs_vector_list(vector(-1.1, 0.0, 1.1), vector(0.0, 1.1, 2.2),
                                vector(1.1, 2.2, 3.3), vector(2.2, 3.3, 4.4))
        v = vector(5.5, 6.6, 7.7)
        self.assertEqual(c_vector_list_index_out_of_range_error, xs_vector_list_set(xs_lst, int32(4), v))
        self.assertEqual(c_vector_list_index_out_of_range_error, xs_vector_list_set(xs_lst, int32(-1), v))

    def test_xs_vector_list_append(self):
        xs_lst = xs_vector_list_create()
        lst = []
        for i in range(11):
            v = vector(float(i) + 11.0, float(i) + 11.1, float(i) + 11.2)
            xs_vector_list_append(xs_lst, v)
            lst.append(v)
        self.assertEqual(len(lst), xs_vector_list_size(xs_lst))
        self.assertEqual(vstr(lst), xs_vector_list_to_string(xs_lst))

    def test_xs_vector_list_append_fail_over_max_capacity(self):
        orig = _vl.c_vector_list_max_capacity
        _vl.c_vector_list_max_capacity = int32(1000)
        xs_lst = xs_vector_list_from_repeated_val(vector(1.0, 1.0, 1.0), _vl.c_vector_list_max_capacity - 1)
        self.assertLessEqual(0, xs_lst)
        self.assertEqual(c_vector_list_max_capacity_error, xs_vector_list_append(xs_lst, vector(10.0, 10.0, 10.0)))
        xs_vector_list_clear(xs_lst)
        _vl.c_vector_list_max_capacity = orig

    def test_xs_vector_list_insert(self):
        lst = [vector(-1.1, 0.0, 1.1), vector(0.0, 1.1, 2.2), vector(1.1, 2.2, 3.3),
               vector(2.2, 3.3, 4.4), vector(3.3, 4.4, 5.5), vector(4.4, 5.5, 6.6)]
        xs_lst = xs_vector_list(*tuple(lst))
        for _ in range(100):
            v = vector(random.random(), random.random(), random.random())
            i = randint(0, len(lst))
            self.assertEqual(c_vector_list_success, xs_vector_list_insert(xs_lst, int32(i), v))
            lst.insert(i, v)
        self.assertEqual(vstr(lst), xs_vector_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_vector_list_size(xs_lst))

    def test_xs_vector_list_insert_fail_with_incorrect_idx(self):
        xs_lst = xs_vector_list(vector(1.1, 2.2, 3.3), vector(4.4, 5.5, 6.6), vector(7.7, 8.8, 9.9))
        v = vector(1.0, 1.0, 1.0)
        self.assertEqual(c_vector_list_index_out_of_range_error, xs_vector_list_insert(xs_lst, int32(-1), v))
        self.assertEqual(c_vector_list_index_out_of_range_error, xs_vector_list_insert(xs_lst, int32(4), v))

    def test_xs_vector_list_insert_fail_over_max_capacity(self):
        orig = _vl.c_vector_list_max_capacity
        _vl.c_vector_list_max_capacity = int32(1000)
        xs_lst = xs_vector_list_from_repeated_val(vector(1.1, 2.2, 3.3), _vl.c_vector_list_max_capacity - 1)
        self.assertEqual(c_vector_list_max_capacity_error,
                         xs_vector_list_insert(xs_lst, int32(100), vector(1.0, 1.0, 1.0)))
        xs_vector_list_clear(xs_lst)
        _vl.c_vector_list_max_capacity = orig

    def test_xs_vector_list_pop(self):
        lst = [vector(-1.1, 0.0, 1.1), vector(0.0, 1.1, 2.2), vector(1.1, 2.2, 3.3),
               vector(2.2, 3.3, 4.4), vector(3.3, 4.4, 5.5), vector(4.4, 5.5, 6.6)]
        xs_lst = xs_vector_list(*tuple(lst))
        for _ in range(len(lst)):
            self.assertEqual(xs_vector_list_pop(xs_lst), lst.pop())
            self.assertEqual(xs_vector_list_last_error(), c_vector_list_success)
        self.assertEqual(xs_vector_list_size(xs_lst), len(lst))
        self.assertEqual(xs_vector_list_to_string(xs_lst), "[]")

    def test_xs_vector_list_pop_at_index(self):
        lst = [vector(float(i), float(i) + 0.1, float(i) + 0.2) for i in range(200)]
        xs_lst = xs_vector_list_create(int32(201))
        for v in lst:
            xs_vector_list_append(xs_lst, v)
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            val = lst[i]
            self.assertEqual(val, xs_vector_list_pop(xs_lst, int32(i)))
            lst.pop(i)
            self.assertEqual(c_vector_list_success, xs_vector_list_last_error())
        self.assertEqual(vstr(lst), xs_vector_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_vector_list_size(xs_lst))

    def test_xs_vector_list_pop_fail_with_incorrect_idx(self):
        xs_lst = xs_vector_list(vector(-1.1, 0.0, 1.1), vector(0.0, 1.1, 2.2),
                                vector(1.1, 2.2, 3.3), vector(2.2, 3.3, 4.4))
        self.assertEqual(c_vector_list_generic_error_vector, xs_vector_list_pop(xs_lst, int32(4)))
        self.assertEqual(c_vector_list_index_out_of_range_error, xs_vector_list_last_error())
        self.assertEqual(c_vector_list_generic_error_vector, xs_vector_list_pop(xs_lst, int32(-1)))
        self.assertEqual(c_vector_list_index_out_of_range_error, xs_vector_list_last_error())

    def test_xs_vector_list_pop_empty_list(self):
        xs_lst = xs_vector_list_create()
        self.assertEqual(0, xs_vector_list_size(xs_lst))
        result = xs_vector_list_pop(xs_lst)
        self.assertEqual(c_vector_list_generic_error_vector, result)
        self.assertEqual(c_vector_list_index_out_of_range_error, xs_vector_list_last_error())
        self.assertEqual(0, xs_vector_list_size(xs_lst))

    def test_xs_vector_list_pop_until_empty_then_pop_again(self):
        v1 = vector(1.1, 2.2, 3.3)
        v2 = vector(4.4, 5.5, 6.6)
        xs_lst = xs_vector_list(v1, v2)
        self.assertEqual(v2, xs_vector_list_pop(xs_lst))
        self.assertEqual(v1, xs_vector_list_pop(xs_lst))
        self.assertEqual(0, xs_vector_list_size(xs_lst))
        result = xs_vector_list_pop(xs_lst)
        self.assertEqual(c_vector_list_generic_error_vector, result)
        self.assertEqual(c_vector_list_index_out_of_range_error, xs_vector_list_last_error())
        self.assertEqual(0, xs_vector_list_size(xs_lst))
        self.assertEqual("[]", xs_vector_list_to_string(xs_lst))

    def test_xs_vector_list_pop_append_cycle(self):
        xs_lst = xs_vector_list_create(int32(4))
        lst = []
        for i in range(20):
            v = vector(float(i), 0.0, 0.0)
            xs_vector_list_append(xs_lst, v)
            lst.append(v)
        for _ in range(15):
            lst.pop()
            xs_vector_list_pop(xs_lst)
        for i in range(100, 120):
            v = vector(float(i), 0.0, 0.0)
            xs_vector_list_append(xs_lst, v)
            lst.append(v)
        self.assertEqual(vstr(lst), xs_vector_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_vector_list_size(xs_lst))

    def test_xs_vector_list_shrink_after_pop_then_append(self):
        xs_lst = xs_vector_list_create(int32(0))
        for i in range(50):
            xs_vector_list_append(xs_lst, vector(float(i), 0.0, 0.0))
        for _ in range(40):
            xs_vector_list_pop(xs_lst)
        remaining = [vector(float(i), 0.0, 0.0) for i in range(10)]
        self.assertEqual(vstr(remaining), xs_vector_list_to_string(xs_lst))
        self.assertEqual(10, xs_vector_list_size(xs_lst))
        xs_vector_list_append(xs_lst, vector(99.0, 0.0, 0.0))
        remaining.append(vector(99.0, 0.0, 0.0))
        self.assertEqual(vstr(remaining), xs_vector_list_to_string(xs_lst))
        self.assertEqual(11, xs_vector_list_size(xs_lst))

    def test_xs_vector_list_remove(self):
        lst = [vector(float(i), float(i) + 0.1, float(i) + 0.2) for i in range(200)]
        xs_lst = xs_vector_list_create(int32(201))
        for v in lst:
            xs_vector_list_append(xs_lst, v)
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            val = lst[i]
            self.assertEqual(i, xs_vector_list_remove(xs_lst, val))
            lst.remove(val)
        self.assertEqual(vstr(lst), xs_vector_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_vector_list_size(xs_lst))

    def test_xs_vector_list_remove_fail_with_incorrect_idx(self):
        xs_lst = xs_vector_list(vector(-1.1, 0.0, 1.1), vector(0.0, 1.1, 2.2),
                                vector(1.1, 2.2, 3.3), vector(2.2, 3.3, 4.4))
        self.assertEqual(c_vector_list_generic_error, xs_vector_list_remove(xs_lst, vector(99.0, 99.0, 99.0)))

    def test_xs_vector_list_index(self):
        lst = [vector(float(i), float(i) + 0.1, float(i) + 0.2) for i in range(200)]
        xs_lst = xs_vector_list_create(int32(201))
        for v in lst:
            xs_vector_list_append(xs_lst, v)
        for _ in range(100):
            val = lst[randint(0, len(lst) - 1)]
            self.assertEqual(lst.index(val), xs_vector_list_index(xs_lst, val))

    def test_xs_vector_list_index_with_ranges(self):
        xs_lst = xs_vector_list()
        lst = []
        for _ in range(500):
            val = vector(random.random(), random.random(), random.random())
            xs_vector_list_append(xs_lst, val)
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
                    r = c_vector_list_generic_error
                self.assertEqual(r, xs_vector_list_index(*params_xs))

    def test_xs_vector_list_index_fail_with_incorrect_idx(self):
        xs_lst = xs_vector_list(vector(1.1, 2.2, 3.3), vector(4.4, 5.5, 6.6), vector(7.7, 8.8, 9.9))
        self.assertEqual(c_vector_list_generic_error, xs_vector_list_index(xs_lst, vector(99.0, 99.0, 99.0)))

    def test_xs_vector_list_contains(self):
        xs_lst = xs_vector_list(vector(1.1, 2.2, 3.3), vector(4.4, 5.5, 6.6))
        self.assertTrue(xs_vector_list_contains(xs_lst, vector(1.1, 2.2, 3.3)))
        self.assertTrue(xs_vector_list_contains(xs_lst, vector(4.4, 5.5, 6.6)))
        self.assertFalse(xs_vector_list_contains(xs_lst, vector(7.7, 8.8, 9.9)))

    def test_xs_vector_list_to_string_test(self):
        xs_lst = xs_vector_list(vector(-1.1, 0.0, 1.1), vector(0.0, 1.1, 2.2),
                                vector(1.1, 2.2, 3.3), vector(2.2, 3.3, 4.4), vector(3.3, 4.4, 5.5))
        expected = vstr([vector(-1.1, 0.0, 1.1), vector(0.0, 1.1, 2.2),
                         vector(1.1, 2.2, 3.3), vector(2.2, 3.3, 4.4), vector(3.3, 4.4, 5.5)])
        self.assertEqual(expected, xs_vector_list_to_string(xs_lst))
        xs_lst_empty = xs_vector_list()
        self.assertEqual("[]", xs_vector_list_to_string(xs_lst_empty))

    def test_xs_vector_list_reverse_even(self):
        lst = [vector(-1.1, 0.0, 1.1), vector(0.0, 1.1, 2.2), vector(1.1, 2.2, 3.3),
               vector(2.2, 3.3, 4.4), vector(3.3, 4.4, 5.5), vector(4.4, 5.5, 6.6)]
        xs_lst = xs_vector_list(*tuple(lst))
        xs_vector_list_reverse(xs_lst)
        lst.reverse()
        self.assertEqual(vstr(lst), xs_vector_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_vector_list_size(xs_lst))

    def test_xs_vector_list_reverse_odd(self):
        lst = [vector(-1.1, 0.0, 1.1), vector(0.0, 1.1, 2.2), vector(1.1, 2.2, 3.3),
               vector(2.2, 3.3, 4.4), vector(3.3, 4.4, 5.5), vector(4.4, 5.5, 6.6), vector(5.5, 6.6, 7.7)]
        xs_lst = xs_vector_list(*tuple(lst))
        xs_vector_list_reverse(xs_lst)
        lst.reverse()
        self.assertEqual(vstr(lst), xs_vector_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_vector_list_size(xs_lst))

    def test_xs_vector_list_reverse_empty(self):
        lst = []
        xs_lst = xs_vector_list()
        xs_vector_list_reverse(xs_lst)
        lst.reverse()
        self.assertEqual(vstr(lst), xs_vector_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_vector_list_size(xs_lst))

    def test_xs_vector_list_copy(self):
        lst = [vector(-1.1, 0.0, 1.1), vector(0.0, 1.1, 2.2), vector(1.1, 2.2, 3.3),
               vector(2.2, 3.3, 4.4), vector(3.3, 4.4, 5.5), vector(4.4, 5.5, 6.6)]
        xs_lst = xs_vector_list(*tuple(lst))
        xs_copy = xs_vector_list_copy(xs_lst)
        self.assertEqual(xs_vector_list_to_string(xs_lst), xs_vector_list_to_string(xs_copy))
        self.assertEqual(xs_vector_list_size(xs_lst), xs_vector_list_size(xs_copy))

        xs_vector_list_set(xs_lst, int32(0), vector(100.1, 200.2, 300.3))
        self.assertEqual(vstr(lst), xs_vector_list_to_string(xs_copy))
        self.assertEqual(len(lst), xs_vector_list_size(xs_copy))

    def test_xs_vector_list_copy_slices(self):
        lst = [vector(-1.1, 0.0, 1.1), vector(0.0, 1.1, 2.2), vector(1.1, 2.2, 3.3),
               vector(2.2, 3.3, 4.4), vector(3.3, 4.4, 5.5), vector(4.4, 5.5, 6.6)]
        xs_lst = xs_vector_list(*tuple(lst))

        for i in i32range(len(lst) * -1, len(lst) + 1):
            for j in i32range(len(lst) * -1, len(lst) + 1):
                xs_copy = xs_vector_list_copy(xs_lst, i, j)
                copy_lst = lst[i:j]
                self.assertEqual(vstr(copy_lst), xs_vector_list_to_string(xs_copy))
                self.assertEqual(len(copy_lst), xs_vector_list_size(xs_copy))

    def test_xs_vector_list_copy_empty(self):
        xs_lst = xs_vector_list()
        xs_copy = xs_vector_list_copy(xs_lst)
        self.assertEqual(0, xs_vector_list_size(xs_copy))
        self.assertEqual("[]", xs_vector_list_to_string(xs_copy))

    def test_xs_vector_list_copy_single_element(self):
        xs_lst = xs_vector_list(vector(4.2, 5.3, 6.4))
        xs_copy = xs_vector_list_copy(xs_lst)
        self.assertEqual(1, xs_vector_list_size(xs_copy))
        self.assertEqual(vstr([vector(4.2, 5.3, 6.4)]), xs_vector_list_to_string(xs_copy))

    def test_xs_vector_list_extend(self):
        lst1 = [vector(-1.1, 0.0, 1.1), vector(0.0, 1.1, 2.2), vector(1.1, 2.2, 3.3),
                vector(2.2, 3.3, 4.4), vector(3.3, 4.4, 5.5), vector(4.4, 5.5, 6.6)]
        lst2 = [vector(0.0, -10.1, 20.2), vector(-30.3, 40.4, -50.5), vector(60.6, -70.7, 80.8),
                vector(-90.9, 100.1, -110.1), vector(120.1, -130.1, 140.1), vector(-150.1, 160.1, -170.1),
                vector(180.1, -190.1, 200.2), vector(-210.2, 220.2, -230.2), vector(240.2, -250.2, 260.3),
                vector(-270.3, 280.3, -290.3)]

        xs_lst1 = xs_vector_list(*tuple(lst1))
        xs_lst2 = xs_vector_list(*tuple(lst2))
        self.assertEqual(c_vector_list_success, xs_vector_list_extend(xs_lst1, xs_lst2))
        lst1.extend(lst2)

        self.assertEqual(vstr(lst1), xs_vector_list_to_string(xs_lst1))
        self.assertEqual(len(lst1), xs_vector_list_size(xs_lst1))

    def test_xs_vector_list_extend_at_exact_capacity_boundary(self):
        lst1 = [vector(float(i), 0.0, 0.0) for i in range(12)]
        xs_lst1 = xs_vector_list(*lst1)
        self.assertEqual(13, xs_vector_list_capacity(xs_lst1))
        xs_lst2 = xs_vector_list(vector(99.0, 0.0, 0.0))
        self.assertEqual(c_vector_list_success, xs_vector_list_extend(xs_lst1, xs_lst2))
        lst1.append(vector(99.0, 0.0, 0.0))
        self.assertEqual(13, xs_vector_list_size(xs_lst1))
        self.assertEqual(vstr(lst1), xs_vector_list_to_string(xs_lst1))

    def test_xs_vector_list_extend_fills_exactly(self):
        lst1 = [vector(float(i), 0.0, 0.0) for i in range(7)]
        lst2 = [vector(float(i), 0.0, 0.0) for i in range(10, 16)]
        xs_lst1 = xs_vector_list(*lst1)
        xs_lst2 = xs_vector_list(*lst2)
        self.assertEqual(c_vector_list_success, xs_vector_list_extend(xs_lst1, xs_lst2))
        lst1.extend(lst2)
        self.assertEqual(vstr(lst1), xs_vector_list_to_string(xs_lst1))
        self.assertEqual(len(lst1), xs_vector_list_size(xs_lst1))

    def test_xs_vector_list_extend_with_array(self):
        lst1 = [vector(-1.1, 0.0, 1.1), vector(0.0, 1.1, 2.2), vector(1.1, 2.2, 3.3),
                vector(2.2, 3.3, 4.4), vector(3.3, 4.4, 5.5), vector(4.4, 5.5, 6.6)]
        v = vector(5.5, 6.6, 7.7)
        lst2 = [v] * 10

        xs_lst = xs_vector_list(*tuple(lst1))
        xs_arr = xs_array_create_vector(10, v)
        self.assertEqual(c_vector_list_success, xs_vector_list_extend_with_array(xs_lst, xs_arr))
        lst1.extend(lst2)

        self.assertEqual(vstr(lst1), xs_vector_list_to_string(xs_lst))
        self.assertEqual(len(lst1), xs_vector_list_size(xs_lst))

    def test_xs_vector_list_extend_with_array_copies_raw_array_values_in_order(self):
        lst1 = [vector(1.0, 0.0, 0.0), vector(2.0, 0.0, 0.0)]
        arr_values = [
            vector(3.0, 3.0, 3.0),
            vector(4.0, 4.0, 4.0),
            vector(5.0, 5.0, 5.0),
        ]
        xs_lst = xs_vector_list(*tuple(lst1))
        xs_arr = xs_array_create_vector(len(arr_values))
        for i, value in enumerate(arr_values):
            xs_array_set_vector(xs_arr, i, value)
        self.assertEqual(c_vector_list_success, xs_vector_list_extend_with_array(xs_lst, xs_arr))
        lst1.extend(arr_values)
        self.assertEqual(vstr(lst1), xs_vector_list_to_string(xs_lst))
        self.assertEqual(len(lst1), xs_vector_list_size(xs_lst))

    def test_xs_vector_list_extend_with_array_at_exact_capacity_boundary(self):
        lst1 = [vector(float(i), 0.0, 0.0) for i in range(12)]
        xs_lst = xs_vector_list(*lst1)
        self.assertEqual(13, xs_vector_list_capacity(xs_lst))
        xs_arr = xs_array_create_vector(1, vector(99.0, 0.0, 0.0))
        self.assertEqual(c_vector_list_success, xs_vector_list_extend_with_array(xs_lst, xs_arr))
        lst1.append(vector(99.0, 0.0, 0.0))
        self.assertEqual(13, xs_vector_list_size(xs_lst))
        self.assertEqual(vstr(lst1), xs_vector_list_to_string(xs_lst))

    def test_xs_vector_list_clear(self):
        xs_lst = xs_vector_list(vector(-1.1, 0.0, 1.1), vector(0.0, 1.1, 2.2), vector(1.1, 2.2, 3.3),
                                vector(2.2, 3.3, 4.4), vector(3.3, 4.4, 5.5), vector(4.4, 5.5, 6.6))
        self.assertEqual(c_vector_list_success, xs_vector_list_clear(xs_lst))
        self.assertEqual("[]", xs_vector_list_to_string(xs_lst))
        self.assertEqual(0, xs_vector_list_size(xs_lst))

    def test_xs_vector_list_clear_shrinks_large_capacity(self):
        xs_lst = xs_vector_list_create(int32(100))
        xs_vector_list_append(xs_lst, vector(1.0, 0.0, 0.0))
        xs_vector_list_append(xs_lst, vector(2.0, 0.0, 0.0))
        xs_vector_list_append(xs_lst, vector(3.0, 0.0, 0.0))
        self.assertEqual(3, xs_vector_list_size(xs_lst))
        capacity_before = xs_vector_list_capacity(xs_lst)
        self.assertGreater(capacity_before, 8)
        self.assertEqual(c_vector_list_success, xs_vector_list_clear(xs_lst))
        self.assertEqual(0, xs_vector_list_size(xs_lst))
        capacity_after = xs_vector_list_capacity(xs_lst)
        self.assertLessEqual(capacity_after, 8)

    def test_xs_vector_list_clear_small_list(self):
        xs_lst = xs_vector_list(vector(1.1, 2.2, 3.3), vector(4.4, 5.5, 6.6))
        self.assertEqual(c_vector_list_success, xs_vector_list_clear(xs_lst))
        self.assertEqual(0, xs_vector_list_size(xs_lst))

    def test_xs_vector_list_count(self):
        v1 = vector(1.1, 2.2, 3.3)
        v2 = vector(4.4, 5.5, 6.6)
        xs_lst = xs_vector_list()
        lst = []
        for _ in range(50):
            xs_vector_list_append(xs_lst, v1)
            lst.append(v1)
        for _ in range(50):
            xs_vector_list_append(xs_lst, v2)
            lst.append(v2)

        self.assertEqual(lst.count(v1), xs_vector_list_count(xs_lst, v1))
        self.assertEqual(lst.count(v2), xs_vector_list_count(xs_lst, v2))
        self.assertEqual(0, xs_vector_list_count(xs_lst, vector(9.9, 9.9, 9.9)))

    def test_xs_vector_list_count_on_empty(self):
        xs_lst = xs_vector_list()
        self.assertEqual(0, xs_vector_list_count(xs_lst, vector(1.0, 2.0, 3.0)))


def vstr(lst: list) -> str:
    if not lst:
        return "[]"
    return "[" + ", ".join(str(v) for v in lst) + "]"
