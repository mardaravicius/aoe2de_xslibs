import unittest
from random import randint

from xs.int_list import *


class IntListTest(unittest.TestCase):
    def test_xs_int_list(self):
        for i in i32range(0, 13):
            params = tuple(i32range(i))
            arr = xs_int_list(*params)
            self.assertEqual(i, xs_int_list_size(arr))
            self.assertEqual(istr(list(range(i))), xs_int_list_to_string(arr))

    def test_xs_int_list_stop_at_magic_number(self):
        arr = xs_int_list(int32(1), c_int_list_empty_param, int32(2))
        self.assertEqual(istr([1]), xs_int_list_to_string(arr))

    def test_xs_int_list_create_empty(self):
        arr = xs_int_list_create(int32(16))
        self.assertEqual(0, xs_int_list_size(arr))

    def test_xs_int_list_create_fail_at_negative_capacity(self):
        arr = xs_int_list_create(int32(-1))
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
            lst = list(i32range(*data))
            self.assertEqual(len(lst), xs_int_list_size(arr))
            self.assertEqual(istr(lst), xs_int_list_to_string(arr))

    def test_xs_int_list_range_fail_with_incorrect_ranges(self):
        test_data = [
            (0, 5, 0),
            (10, 1, 1),
            (1, 10, -1),
        ]

        for data in test_data:
            arr = xs_int_list_from_range(*data)
            self.assertEqual(c_int_list_generic_error, arr)

    def test_xs_int_list_range_fail_over_max_capacity(self):
        arr = xs_int_list_from_range(int32(0), c_int_list_max_capacity, int32(1))
        self.assertEqual(c_int_list_generic_error, arr)
        xs_array_resize_int(arr, 0)

    def test_xs_int_list_from_repeated_val(self):
        arr = xs_int_list_from_repeated_val(int32(5), int32(7))
        self.assertEqual(7, xs_int_list_size(arr), 7)
        self.assertEqual("[5, 5, 5, 5, 5, 5, 5]", xs_int_list_to_string(arr))

    def test_xs_int_list_from_repeated_val_fail_with_negative_repeat(self):
        arr = xs_int_list_from_repeated_val(int32(5), int32(-2))
        self.assertEqual(c_int_list_generic_error, arr)

    def test_xs_int_list_from_repeated_val_fail_over_max_capacity(self):
        arr = xs_int_list_from_repeated_val(int32(5), c_int_list_max_capacity)
        self.assertEqual(arr, c_int_list_generic_error)
        xs_array_resize_int(0, arr)

    def test_xs_int_list_from_repeated_list(self):
        lst1 = [1, 2, 3, 4]
        lst2 = lst1 * 7
        arr1 = xs_int_list(*tuple(lst1))
        arr2 = xs_int_list_from_repeated_list(arr1, int32(7))
        self.assertEqual(istr(lst2), xs_int_list_to_string(arr2))
        self.assertEqual(len(lst2), xs_int_list_size(arr2))

    def test_xs_int_list_from_array(self):
        arr = xs_array_create_int(10, 5)
        lst = [5] * 10
        arr_lst = xs_int_list_from_array(arr)
        self.assertEqual(istr(lst), xs_int_list_to_string(arr_lst))
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
        self.assertEqual(istr(lst), xs_int_list_to_string(arr))
        self.assertEqual(len(lst), xs_int_list_size(arr))
        xs_array_set_int(arr, 1, 2000)
        self.assertEqual(xs_array_get_int(arr, 1), xs_int_list_get(arr, int32(0)))

    def test_xs_int_list_get(self):
        lst = list(i32range(-1, 100))
        arr = xs_int_list_from_range(int32(-1), int32(100))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            self.assertEqual(lst[i], xs_int_list_get(arr, int32(i)))
            self.assertEqual(c_int_list_success, xs_int_list_last_error())

    def test_xs_int_list_get_fail_with_incorrect_idx(self):
        arr = xs_int_list(int32(-1), int32(0), int32(1), int32(2))
        self.assertEqual(c_int_list_generic_error, xs_int_list_get(arr, int32(4)))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())
        self.assertEqual(c_int_list_generic_error, xs_int_list_get(arr, int32(-1)))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())

    def test_xs_int_list_set(self):
        lst = list(i32range(-1, 100))
        arr = xs_int_list_from_range(int32(-1), int32(100))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            v = randint(-100, 100)
            self.assertEqual(c_int_list_success, xs_int_list_set(arr, int32(i), int32(v)))
            lst[i] = v
        self.assertEqual(istr(lst), xs_int_list_to_string(arr))
        self.assertEqual(len(lst), xs_int_list_size(arr))

    def test_xs_int_list_set_fail_with_incorrect_idx(self):
        arr = xs_int_list(int32(-1), int32(0), int32(1), int32(2))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_set(arr, int32(4), int32(5)))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_set(arr, int32(-1), int32(5)))

    def test_xs_int_list_append(self):
        arr = xs_int_list_create()
        lst = []
        for i in i32range(11, 22):
            xs_int_list_append(arr, i)
            lst.append(i)
        self.assertEqual(len(lst), xs_int_list_size(arr))
        self.assertEqual(istr(lst), xs_int_list_to_string(arr))

    def test_xs_int_list_append_fail_over_max_capacity(self):
        arr = xs_int_list_from_repeated_val(int32(1), c_int_list_max_capacity - 1)
        self.assertLessEqual(0, arr)
        self.assertEqual(c_int_list_max_capacity_error, xs_int_list_append(arr, int32(10)))
        xs_array_resize_int(arr, 0)

    def test_xs_int_list_insert(self):
        lst = [-1, 0, 1, 2, 3, 4]
        arr = xs_int_list(*tuple(lst))
        for v in i32range(100):
            i = randint(0, len(lst))
            self.assertEqual(c_int_list_success, xs_int_list_insert(arr, int32(i), v))
            lst.insert(i, v)
        self.assertEqual(istr(lst), xs_int_list_to_string(arr))
        self.assertEqual(len(lst), xs_int_list_size(arr))

    def test_xs_int_list_insert_fail_with_incorrect_idx(self):
        arr = xs_int_list(int32(1), int32(2), int32(3))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_insert(arr, int32(-1)))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_insert(arr, int32(4)))

    def test_xs_int_list_insert_fail_over_max_capacity(self):
        arr = xs_int_list_from_repeated_val(int32(1), c_int_list_max_capacity - 1)
        self.assertEqual(c_int_list_max_capacity_error, xs_int_list_insert(arr, int32(100)))
        xs_array_resize_int(arr, 0)

    def test_xs_int_list_pop(self):
        lst = [-1, 0, 1, 2, 3, 4]
        arr = xs_int_list(*tuple(lst))
        for _ in range(len(lst)):
            self.assertEqual(lst.pop(), xs_int_list_pop(arr))
            self.assertEqual(c_int_list_success, xs_int_list_last_error())
        self.assertEqual(len(lst), xs_int_list_size(arr))
        self.assertEqual(istr(lst), xs_int_list_to_string(arr))

    def test_xs_int_list_pop_at_index(self):
        arr = xs_int_list_from_range(int32(-1), int32(200))
        lst = list(i32range(-1, 200))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            val = lst[i]
            self.assertEqual(val, xs_int_list_pop(arr, int32(i)))
            lst.pop(i)
            self.assertEqual(c_int_list_success, xs_int_list_last_error())
        self.assertEqual(istr(lst), xs_int_list_to_string(arr))
        self.assertEqual(len(lst), xs_int_list_size(arr))

    def test_xs_int_list_pop_fail_with_incorrect_idx(self):
        arr = xs_int_list(int32(-1), int32(0), int32(1), int32(2))
        self.assertEqual(c_int_list_generic_error, xs_int_list_pop(arr, int32(4)))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())
        self.assertEqual(c_int_list_generic_error, xs_int_list_pop(arr, int32(-1)))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())

    def test_xs_int_list_remove(self):
        arr = xs_int_list_from_range(int32(-1), int32(200))
        lst = list(i32range(-1, 200))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            val = lst[i]
            self.assertEqual(i, xs_int_list_remove(arr, val))
            lst.remove(val)

        self.assertEqual(istr(lst), xs_int_list_to_string(arr))
        self.assertEqual(len(lst), xs_int_list_size(arr))

    def test_xs_int_list_remove_fail_with_incorrect_idx(self):
        arr = xs_int_list(int32(-1), int32(0), int32(1), int32(2))
        self.assertEqual(c_int_list_generic_error, xs_int_list_remove(arr, int32(4)))

    def test_xs_int_list_index(self):
        arr = xs_int_list_from_range(int32(-1), int32(200))
        lst = list(i32range(-1, 200))
        for _ in range(100):
            val = lst[randint(0, len(lst) - 1)]
            self.assertEqual(lst.index(val), xs_int_list_index(arr, val))

    def test_xs_int_list_index_with_ranges(self):
        arr = xs_int_list()
        lst = []
        for _ in range(500):
            val = randint(-100, 101)
            xs_int_list_append(arr, int32(val))
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
        arr = xs_int_list(int32(1), int32(2), int32(3))
        self.assertEqual(c_int_list_generic_error, xs_int_list_index(arr, int32(4)))

    def test_xs_int_list_contains(self):
        arr = xs_int_list(int32(1), int32(2))
        self.assertTrue(xs_int_list_contains(arr, int32(1)))
        self.assertTrue(xs_int_list_contains(arr, int32(2)))
        self.assertFalse(xs_int_list_contains(arr, int32(3)))

    def test_xs_int_list_sort(self):
        for _ in range(100):
            size = randint(1, 100)
            arr = xs_int_list_create(int32(size))
            lst = []
            for _ in range(size):
                val = randint(-100, 100)
                xs_int_list_append(arr, int32(val))
                lst.append(val)
            lst.sort()
            xs_int_list_sort(arr)
            self.assertEqual(istr(lst), xs_int_list_to_string(arr))
            self.assertEqual(len(lst), xs_int_list_size(arr))

    def test_xs_int_list_sort_reverse(self):
        for _ in range(100):
            size = randint(0, 100)
            arr = xs_int_list_create(int32(size))
            lst = []
            for _ in range(size):
                val = randint(-100, 100)
                xs_int_list_append(arr, int32(val))
                lst.append(val)
            lst.sort(reverse=True)
            xs_int_list_sort(arr, True)
            self.assertEqual(istr(lst), xs_int_list_to_string(arr))
            self.assertEqual(len(lst), xs_int_list_size(arr))

    def test_xs_int_list_to_string_test(self):
        arr = xs_int_list(int32(-1), int32(0), int32(1), int32(2), int32(3))
        self.assertEqual("[-1, 0, 1, 2, 3]", xs_int_list_to_string(arr))
        arr_empty = xs_int_list()
        self.assertEqual("[]", xs_int_list_to_string(arr_empty))

    def test_xs_int_list_reverse_even(self):
        lst = [-1, 0, 1, 2, 3, 4]
        arr = xs_int_list(*tuple(lst))

        xs_int_list_reverse(arr)
        lst.reverse()

        self.assertEqual(istr(lst), xs_int_list_to_string(arr))
        self.assertEqual(len(lst), xs_int_list_size(arr))

    def test_xs_int_list_reverse_odd(self):
        lst = [-1, 0, 1, 2, 3, 4, 5]
        arr = xs_int_list(*tuple(lst))

        xs_int_list_reverse(arr)
        lst.reverse()

        self.assertEqual(istr(lst), xs_int_list_to_string(arr))
        self.assertEqual(len(lst), xs_int_list_size(arr))

    def test_xs_int_list_reverse_empty(self):
        lst = []
        arr = xs_int_list(*tuple(lst))

        xs_int_list_reverse(arr)
        lst.reverse()

        self.assertEqual(istr(lst), xs_int_list_to_string(arr))
        self.assertEqual(len(lst), xs_int_list_size(arr))

    def test_xs_int_list_copy(self):
        lst = [-1, 0, 1, 2, 3, 4]
        arr = xs_int_list(*tuple(lst))
        copy = xs_int_list_copy(arr)
        self.assertEqual(xs_int_list_to_string(arr), xs_int_list_to_string(copy))
        self.assertEqual(xs_int_list_size(arr), xs_int_list_size(copy))

        xs_int_list_set(arr, int32(0), int32(100))
        self.assertEqual(istr(lst), xs_int_list_to_string(copy))
        self.assertEqual(len(lst), xs_int_list_size(copy))

    def test_xs_int_list_copy_slices(self):
        lst = [-1, 0, 1, 2, 3, 4]
        arr = xs_int_list(*tuple(lst))

        for i in i32range(len(lst) * -1, len(lst) + 1):
            for j in i32range(len(lst) * -1, len(lst) + 1):
                copy_arr = xs_int_list_copy(arr, i, j)
                copy_lst = lst[i:j]
                self.assertEqual(istr(copy_lst), xs_int_list_to_string(copy_arr))
                self.assertEqual(len(copy_lst), xs_int_list_size(copy_arr))

    def test_xs_int_list_extend(self):
        lst1 = [-1, 0, 1, 2, 3, 4]
        lst2 = [0, -10, 20, -30, 40, -50, 60, -70, 80, -90]

        arr1 = xs_int_list(*tuple(lst1))
        arr2 = xs_int_list(*tuple(lst2))
        self.assertEqual(c_int_list_success, xs_int_list_extend(arr1, arr2))
        lst1.extend(lst2)

        self.assertEqual(istr(lst1), xs_int_list_to_string(arr1))
        self.assertEqual(len(lst1), xs_int_list_size(arr1))

    def test_xs_int_list_extend_with_array(self):
        lst1 = [-1, 0, 1, 2, 3, 4]
        lst2 = [5] * 10

        arr1 = xs_int_list(*tuple(lst1))
        arr2 = xs_array_create_int(10, 5)
        self.assertEqual(c_int_list_success, xs_int_list_extend_with_array(arr1, arr2))
        lst1.extend(lst2)

        self.assertEqual(istr(lst1), xs_int_list_to_string(arr1))
        self.assertEqual(len(lst1), xs_int_list_size(arr1))

    def test_xs_int_list_clear(self):
        arr = xs_int_list(int32(-1), int32(0), int32(1), int32(2), int32(3), int32(4))

        self.assertEqual(c_int_list_success, xs_int_list_clear(arr))
        self.assertEqual("[]", xs_int_list_to_string(arr))
        self.assertEqual(0, xs_int_list_size(arr))

    def test_xs_int_list_compare(self):
        arr1 = xs_int_list(int32(-1), int32(0), int32(2))
        arr2 = xs_int_list(int32(-1), int32(0), int32(1))

        self.assertEqual(1, xs_int_list_compare(arr1, arr2))
        self.assertEqual(-1, xs_int_list_compare(arr2, arr1))
        self.assertEqual(0, xs_int_list_compare(arr1, arr1))

    def test_xs_int_list_compare_same_prefix(self):
        arr1 = xs_int_list(int32(-1), int32(0), int32(1))
        arr2 = xs_int_list(int32(-1), int32(0), int32(1), int32(2), int32(3), int32(4))

        self.assertEqual(-1, xs_int_list_compare(arr1, arr2))
        self.assertEqual(1, xs_int_list_compare(arr2, arr1))

    def test_xs_int_list_compare_empty(self):
        arr1 = xs_int_list()
        arr2 = xs_int_list()

        self.assertEqual(0, xs_int_list_compare(arr1, arr2))

    def test_xs_int_list_sum_count_min_max(self):
        arr = xs_int_list()
        lst = []
        for _ in range(100):
            v = randint(-20, 21)
            xs_int_list_append(arr, int32(v))
            lst.append(v)

        self.assertEqual(sum(lst), xs_int_list_sum(arr))
        self.assertEqual(lst.count(1), xs_int_list_count(arr, int32(1)))
        self.assertEqual(min(lst), xs_int_list_min(arr))
        self.assertEqual(max(lst), xs_int_list_max(arr))

    def test_xs_int_list_sum_count_min_max_on_empty(self):
        arr = xs_int_list()
        lst = []

        self.assertEqual(sum(lst), xs_int_list_sum(arr))
        self.assertEqual(lst.count(1), xs_int_list_count(arr, int32(1)))
        self.assertEqual(c_int_list_generic_error, xs_int_list_min(arr))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())
        self.assertEqual(c_int_list_generic_error, xs_int_list_max(arr))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())


def istr(lst: list[int | int32]) -> str:
    return str([int(x) for x in lst])
