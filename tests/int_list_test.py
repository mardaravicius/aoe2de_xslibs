import unittest
from random import randint

from xs.int_list import *


class IntListTest(unittest.TestCase):

    def test_xs_int_list(self):
        for i in range(0, 13):
            params = tuple(range(i))
            arr = xs_int_list(*params)
            self.assertEqual(i, xs_int_list_size(arr))
            self.assertEqual(str(list(range(i))), xs_int_list_to_string(arr))

    def test_xs_int_list_stop_at_magic_number(self):
        arr = xs_int_list(1, c_int_list_empty_param, 2)
        self.assertEqual(str([1]), xs_int_list_to_string(arr))

    def test_xs_int_list_create_empty(self):
        arr = xs_int_list_create(16)
        self.assertEqual(0, xs_int_list_size(arr))

    def test_xs_int_list_create_fail_at_negative_capacity(self):
        arr = xs_int_list_create(-1)
        self.assertEqual(c_int_list_generic_error, arr)

    def test_xs_int_list_create_fail_over_max_capacity(self):
        arr = xs_int_list_create(c_int_list_max_capacity)
        self.assertEqual(c_int_list_generic_error, arr)
        xs_array_resize_int(arr, 0)

    def test_xs_int_list_range(self):
        test_data = [
            (0, 0, 1),
            (0, 1, 1),
            (0, 10, 1),
            (0, 10, 2),
            (0, 10, 3),
            (10, 0, -1),
            (10, 0, -2),
            (10, 0, -3),
            (-4, 4, 1),
            (5, -5, -2),
            (-17, -13, 1),
            (-8, -22, -3),
        ]

        for data in test_data:
            arr = xs_int_list_from_range(*data)
            lst = list(range(*data))
            self.assertEqual(len(lst), xs_int_list_size(arr))
            self.assertEqual(str(lst), xs_int_list_to_string(arr))

    def test_xs_int_list_range_fail_with_incorrect_ranges(self):
        test_data = [
            (0, 5, 0),
            (10, 1, 1),
            (1, 10, -1),
        ]

        for data in test_data:
            arr = xs_int_list_from_range(*data)
            self.assertEqual(arr, c_int_list_generic_error)

    def test_xs_int_list_range_fail_over_max_capacity(self):
        arr = xs_int_list_from_range(0, c_int_list_max_capacity, 1)
        self.assertEqual(arr, c_int_list_generic_error)
        xs_array_resize_int(arr, 0)

    def test_xs_int_list_from_repeated_val(self):
        arr = xs_int_list_from_repeated_val(5, 7)
        self.assertEqual(xs_int_list_size(arr), 7)
        self.assertEqual(xs_int_list_to_string(arr), "[5, 5, 5, 5, 5, 5, 5]")

    def test_xs_int_list_from_repeated_val_fail_with_negative_repeat(self):
        arr = xs_int_list_from_repeated_val(5, -2)
        self.assertEqual(arr, c_int_list_generic_error)

    def test_xs_int_list_from_repeated_val_fail_over_max_capacity(self):
        arr = xs_int_list_from_repeated_val(5, c_int_list_max_capacity)
        self.assertEqual(arr, c_int_list_generic_error)
        xs_array_resize_int(arr, 0)

    def test_xs_int_list_from_repeated_list(self):
        lst1 = [1, 2, 3, 4]
        lst2 = lst1 * 7
        arr1 = xs_int_list(*tuple(lst1))
        arr2 = xs_int_list_from_repeated_list(arr1, 7)
        self.assertEqual(str(lst2), xs_int_list_to_string(arr2))
        self.assertEqual(len(lst2), xs_int_list_size(arr2))

    def test_xs_int_list_from_array(self):
        arr = xs_array_create_int(10, 5)
        lst = [5] * 10
        arr_lst = xs_int_list_from_array(arr)
        self.assertEqual(str(lst), xs_int_list_to_string(arr_lst))
        self.assertEqual(xs_array_get_size(arr), xs_int_list_size(arr_lst))
        self.assertEqual(len(lst), xs_int_list_size(arr_lst))

    def test_xs_int_list_from_array_fail_over_max_capacity(self):
        arr = xs_array_create_int(c_int_list_max_capacity, 5)
        self.assertEqual(c_int_list_generic_error, xs_int_list_from_array(arr))
        xs_array_resize_int(arr, 0)

    def test_xs_int_list_use_array_as_source(self):
        arr = xs_array_create_int(10, 5)
        lst = [5] * 10
        self.assertEqual(c_int_list_success, xs_int_list_use_array_as_source(arr))
        self.assertEqual(str(lst), xs_int_list_to_string(arr))
        self.assertEqual(len(lst), xs_int_list_size(arr))
        xs_array_set_int(arr, 1, 2000)
        self.assertEqual(xs_array_get_int(arr, 1), xs_int_list_get(arr, 0))

    def test_xs_int_list_get(self):
        lst = list(range(-1, 100))
        arr = xs_int_list_from_range(-1, 100)
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            self.assertEqual(lst[i], xs_int_list_get(arr, i))
            self.assertEqual(c_int_list_success, xs_int_list_last_error())

    def test_xs_int_list_get_fail_with_incorrect_idx(self):
        arr = xs_int_list(-1, 0, 1, 2)
        self.assertEqual(xs_int_list_get(arr, 4), c_int_list_generic_error)
        self.assertEqual(xs_int_list_last_error(), c_int_list_index_out_of_range_error)
        self.assertEqual(xs_int_list_get(arr, -1), c_int_list_generic_error)
        self.assertEqual(xs_int_list_last_error(), c_int_list_index_out_of_range_error)

    def test_xs_int_list_set(self):
        lst = list(range(-1, 100))
        arr = xs_int_list_from_range(-1, 100)
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            v = randint(-100, 100)
            self.assertEqual(c_int_list_success, xs_int_list_set(arr, i, v))
            lst[i] = v
        self.assertEqual(str(lst), xs_int_list_to_string(arr))
        self.assertEqual(len(lst), xs_int_list_size(arr))

    def test_xs_int_list_set_fail_with_incorrect_idx(self):
        arr = xs_int_list(-1, 0, 1, 2)
        self.assertEqual(xs_int_list_set(arr, 4, 5), c_int_list_index_out_of_range_error)
        self.assertEqual(xs_int_list_set(arr, -1, 5), c_int_list_index_out_of_range_error)

    def test_xs_int_list_append(self):
        arr = xs_int_list_create()
        lst = []
        for i in range(11, 22):
            xs_int_list_append(arr, i)
            lst.append(i)
        self.assertEqual(xs_int_list_size(arr), len(lst))
        self.assertEqual(xs_int_list_to_string(arr), str(lst))

    def test_xs_int_list_append_fail_over_max_capacity(self):
        arr = xs_int_list_from_repeated_val(1, c_int_list_max_capacity - 1)
        self.assertGreaterEqual(arr, 0)
        self.assertEqual(xs_int_list_append(arr, 10), c_int_list_max_capacity_error)
        xs_array_resize_int(arr, 0)

    def test_xs_int_list_insert(self):
        lst = [-1, 0, 1, 2, 3, 4]
        arr = xs_int_list(*tuple(lst))
        for v in range(100):
            i = randint(0, len(lst))
            self.assertEqual(xs_int_list_insert(arr, i, v), c_int_list_success)
            lst.insert(i, v)
        self.assertEqual(xs_int_list_to_string(arr), str(lst))
        self.assertEqual(xs_int_list_size(arr), len(lst))

    def test_xs_int_list_insert_fail_with_incorrect_idx(self):
        arr = xs_int_list(1, 2, 3)
        self.assertEqual(xs_int_list_insert(arr, -1), c_int_list_index_out_of_range_error)
        self.assertEqual(xs_int_list_insert(arr, 4), c_int_list_index_out_of_range_error)

    def test_xs_int_list_insert_fail_over_max_capacity(self):
        arr = xs_int_list_from_repeated_val(1, c_int_list_max_capacity - 1)
        self.assertEqual(xs_int_list_insert(arr, 100), c_int_list_max_capacity_error)
        xs_array_resize_int(arr, 0)

    def test_xs_int_list_pop(self):
        lst = [-1, 0, 1, 2, 3, 4]
        arr = xs_int_list(*tuple(lst))
        for v in range(len(lst)):
            self.assertEqual(xs_int_list_pop(arr), lst.pop())
            self.assertEqual(xs_int_list_last_error(), c_int_list_success)
        self.assertEqual(xs_int_list_size(arr), len(lst))
        self.assertEqual(xs_int_list_to_string(arr), str(lst))

    def test_xs_int_list_pop_at_index(self):
        arr = xs_int_list_from_range(-1, 200)
        lst = list(range(-1, 200))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            val = lst[i]
            self.assertEqual(xs_int_list_pop(arr, i), val)
            lst.pop(i)
            self.assertEqual(xs_int_list_last_error(), c_int_list_success)
        self.assertEqual(xs_int_list_to_string(arr), str(lst))
        self.assertEqual(xs_int_list_size(arr), len(lst))

    def test_xs_int_list_pop_fail_with_incorrect_idx(self):
        arr = xs_int_list(-1, 0, 1, 2)
        self.assertEqual(xs_int_list_pop(arr, 4), c_int_list_generic_error)
        self.assertEqual(xs_int_list_last_error(), c_int_list_index_out_of_range_error)
        self.assertEqual(xs_int_list_pop(arr, -1), c_int_list_generic_error)
        self.assertEqual(xs_int_list_last_error(), c_int_list_index_out_of_range_error)

    def test_xs_int_list_remove(self):
        arr = xs_int_list_from_range(-1, 200)
        lst = list(range(-1, 200))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            val = lst[i]
            self.assertEqual(xs_int_list_remove(arr, val), i)
            lst.remove(val)

        self.assertEqual(xs_int_list_to_string(arr), str(lst))
        self.assertEqual(xs_int_list_size(arr), len(lst))

    def test_xs_int_list_remove_fail_with_incorrect_idx(self):
        arr = xs_int_list(-1, 0, 1, 2)
        self.assertEqual(xs_int_list_remove(arr, 4), c_int_list_generic_error)

    def test_xs_int_list_index(self):
        arr = xs_int_list_from_range(-1, 200)
        lst = list(range(-1, 200))
        for _ in range(100):
            val = lst[randint(0, len(lst) - 1)]
            self.assertEqual(xs_int_list_index(arr, val), lst.index(val))

    def test_xs_int_list_index_with_ranges(self):
        arr = xs_int_list()
        lst = []
        for _ in range(500):
            val = randint(-100, 101)
            xs_int_list_append(arr, val)
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
                val = randint(-110, 111)
                params_xs = (arr, val) + data
                params = (val,) + data
                try:
                    r = lst.index(params[0], params[1], params[2])
                except ValueError:
                    r = c_int_list_generic_error
                self.assertEqual(r, xs_int_list_index(*params_xs))

    def test_xs_int_list_index_fail_with_incorrect_idx(self):
        arr = xs_int_list(1, 2, 3)
        self.assertEqual(xs_int_list_index(arr, 4), c_int_list_generic_error)

    def test_xs_int_list_contains(self):
        arr = xs_int_list(1, 2)
        self.assertTrue(xs_int_list_contains(arr, 1))
        self.assertTrue(xs_int_list_contains(arr, 2))
        self.assertFalse(xs_int_list_contains(arr, 3))

    def test_xs_int_list_sort(self):
        for _ in range(100):
            size = randint(1, 100)
            arr = xs_int_list_create(size)
            lst = []
            for i in range(size):
                val = randint(-100, 100)
                xs_int_list_append(arr, val)
                lst.append(val)
            lst.sort()
            xs_int_list_sort(arr)
            self.assertEqual(xs_int_list_to_string(arr), str(lst))
            self.assertEqual(xs_int_list_size(arr), len(lst))

    def test_xs_int_list_sort_reverse(self):
        for _ in range(100):
            size = randint(0, 100)
            arr = xs_int_list_create(size)
            lst = []
            for i in range(size):
                val = randint(-100, 100)
                xs_int_list_append(arr, val)
                lst.append(val)
            lst.sort(reverse=True)
            xs_int_list_sort(arr, True)
            self.assertEqual(xs_int_list_to_string(arr), str(lst))
            self.assertEqual(xs_int_list_size(arr), len(lst))

    def test_xs_int_list_to_string_test(self):
        arr = xs_int_list(-1, 0, 1, 2, 3)
        self.assertEqual(xs_int_list_to_string(arr), "[-1, 0, 1, 2, 3]")
        arr_empty = xs_int_list()
        self.assertEqual(xs_int_list_to_string(arr_empty), "[]")

    def test_xs_int_list_reverse_even(self):
        lst = [-1, 0, 1, 2, 3, 4]
        arr = xs_int_list(*tuple(lst))

        xs_int_list_reverse(arr)
        lst.reverse()

        self.assertEqual(xs_int_list_to_string(arr), str(lst))
        self.assertEqual(xs_int_list_size(arr), len(lst))

    def test_xs_int_list_reverse_odd(self):
        lst = [-1, 0, 1, 2, 3, 4, 5]
        arr = xs_int_list(*tuple(lst))

        xs_int_list_reverse(arr)
        lst.reverse()

        self.assertEqual(xs_int_list_to_string(arr), str(lst))
        self.assertEqual(xs_int_list_size(arr), len(lst))

    def test_xs_int_list_reverse_empty(self):
        lst = []
        arr = xs_int_list(*tuple(lst))

        xs_int_list_reverse(arr)
        lst.reverse()

        self.assertEqual(xs_int_list_to_string(arr), str(lst))
        self.assertEqual(xs_int_list_size(arr), len(lst))

    def test_xs_int_list_copy(self):
        lst = [-1, 0, 1, 2, 3, 4]
        arr = xs_int_list(*tuple(lst))
        copy = xs_int_list_copy(arr)
        self.assertEqual(xs_int_list_to_string(copy), xs_int_list_to_string(arr))
        self.assertEqual(xs_int_list_size(copy), xs_int_list_size(arr))

        xs_int_list_set(arr, 0, 100)
        self.assertEqual(xs_int_list_to_string(copy), str(lst))
        self.assertEqual(xs_int_list_size(copy), len(lst))

    def test_xs_int_list_copy_slices(self):
        lst = [-1, 0, 1, 2, 3, 4]
        arr = xs_int_list(*tuple(lst))

        for i in range(len(lst) * -1, len(lst) + 1):
            for j in range(len(lst) * -1, len(lst) + 1):
                copy_arr = xs_int_list_copy(arr, i, j)
                copy_lst = lst[i:j]
                self.assertEqual(str(copy_lst), xs_int_list_to_string(copy_arr))
                self.assertEqual(len(copy_lst), xs_int_list_size(copy_arr))

    def test_xs_int_list_extend(self):
        lst1 = [-1, 0, 1, 2, 3, 4]
        lst2 = [0, -10, 20, -30, 40, -50, 60, -70, 80, -90]

        arr1 = xs_int_list(*tuple(lst1))
        arr2 = xs_int_list(*tuple(lst2))
        self.assertEqual(xs_int_list_extend(arr1, arr2), c_int_list_success)
        lst1.extend(lst2)

        self.assertEqual(xs_int_list_to_string(arr1), str(lst1))
        self.assertEqual(xs_int_list_size(arr1), len(lst1))

    def test_xs_int_list_extend_with_array(self):
        lst1 = [-1, 0, 1, 2, 3, 4]
        lst2 = [5] * 10

        arr1 = xs_int_list(*tuple(lst1))
        arr2 = xs_array_create_int(10, 5)
        self.assertEqual(xs_int_list_extend_with_array(arr1, arr2), c_int_list_success)
        lst1.extend(lst2)

        self.assertEqual(xs_int_list_to_string(arr1), str(lst1))
        self.assertEqual(xs_int_list_size(arr1), len(lst1))

    def test_xs_int_list_clear(self):
        arr = xs_int_list(-1, 0, 1, 2, 3, 4)

        self.assertEqual(xs_int_list_clear(arr), c_int_list_success)
        self.assertEqual(xs_int_list_to_string(arr), "[]")
        self.assertEqual(xs_int_list_size(arr), 0)

    def test_xs_int_list_compare(self):
        arr1 = xs_int_list(-1, 0, 2)
        arr2 = xs_int_list(-1, 0, 1)

        self.assertEqual(xs_int_list_compare(arr1, arr2), 1)
        self.assertEqual(xs_int_list_compare(arr2, arr1), -1)
        self.assertEqual(xs_int_list_compare(arr1, arr1), 0)

    def test_xs_int_list_compare_same_prefix(self):
        arr1 = xs_int_list(-1, 0, 1)
        arr2 = xs_int_list(-1, 0, 1, 2, 3, 4)

        self.assertEqual(xs_int_list_compare(arr1, arr2), -1)
        self.assertEqual(xs_int_list_compare(arr2, arr1), 1)

    def test_xs_int_list_compare_empty(self):
        arr1 = xs_int_list()
        arr2 = xs_int_list()

        self.assertEqual(xs_int_list_compare(arr1, arr2), 0)

    def test_xs_int_list_sum_count_min_max(self):
        arr = xs_int_list()
        lst = []
        for i in range(100):
            v = randint(-20, 21)
            xs_int_list_append(arr, v)
            lst.append(v)

        self.assertEqual(sum(lst), xs_int_list_sum(arr))
        self.assertEqual(lst.count(1), xs_int_list_count(arr, 1))
        self.assertEqual(min(lst), xs_int_list_min(arr))
        self.assertEqual(max(lst), xs_int_list_max(arr))

    def test_xs_int_list_sum_count_min_max_on_empty(self):
        arr = xs_int_list()
        lst = []

        self.assertEqual(sum(lst), xs_int_list_sum(arr))
        self.assertEqual(lst.count(1), xs_int_list_count(arr, 1))
        self.assertEqual(c_int_list_generic_error, xs_int_list_min(arr))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())
        self.assertEqual(c_int_list_generic_error, xs_int_list_max(arr))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())
