import unittest
from random import randint

from xs.int_list import *


class IntListTest(unittest.TestCase):
    def test_xs_int_list(self):
        for i in i32range(0, 13):
            params = tuple(i32range(i))
            xs_lst = xs_int_list(*params)
            self.assertEqual(i, xs_int_list_size(xs_lst))
            self.assertEqual(istr(list(range(i))), xs_int_list_to_string(xs_lst))

    def test_xs_int_list_stop_at_magic_number(self):
        xs_lst = xs_int_list(int32(1), c_int_list_empty_param, int32(2))
        self.assertEqual(istr([1]), xs_int_list_to_string(xs_lst))

    def test_xs_int_list_create_empty(self):
        xs_lst = xs_int_list_create(int32(16))
        self.assertEqual(0, xs_int_list_size(xs_lst))

    def test_xs_int_list_create_fail_at_negative_capacity(self):
        xs_lst = xs_int_list_create(int32(-1))
        self.assertEqual(c_int_list_generic_error, xs_lst)

    def test_xs_int_list_create_fail_over_max_capacity(self):
        xs_lst = xs_int_list_create(c_int_list_max_capacity)
        self.assertEqual(c_int_list_generic_error, xs_lst)
        xs_int_list_clear(xs_lst)

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
            xs_lst = xs_int_list_from_range(*data)
            lst = list(i32range(*data))
            self.assertEqual(len(lst), xs_int_list_size(xs_lst))
            self.assertEqual(istr(lst), xs_int_list_to_string(xs_lst))

    def test_xs_int_list_range_fail_with_incorrect_ranges(self):
        test_data = [
            (0, 5, 0),
            (10, 1, 1),
            (1, 10, -1),
        ]

        for data in test_data:
            xs_lst = xs_int_list_from_range(*data)
            self.assertEqual(c_int_list_generic_error, xs_lst)

    def test_xs_int_list_range_fail_over_max_capacity(self):
        xs_lst = xs_int_list_from_range(int32(0), c_int_list_max_capacity, int32(1))
        self.assertEqual(c_int_list_generic_error, xs_lst)
        xs_int_list_clear(xs_lst)

    def test_xs_int_list_from_repeated_val(self):
        xs_lst = xs_int_list_from_repeated_val(int32(5), int32(7))
        self.assertEqual(7, xs_int_list_size(xs_lst), 7)
        self.assertEqual("[5, 5, 5, 5, 5, 5, 5]", xs_int_list_to_string(xs_lst))

    def test_xs_int_list_from_repeated_val_fail_with_negative_repeat(self):
        xs_lst = xs_int_list_from_repeated_val(int32(5), int32(-2))
        self.assertEqual(c_int_list_generic_error, xs_lst)

    def test_xs_int_list_from_repeated_val_fail_over_max_capacity(self):
        xs_lst = xs_int_list_from_repeated_val(int32(5), c_int_list_max_capacity)
        self.assertEqual(xs_lst, c_int_list_generic_error)
        xs_int_list_clear(xs_lst)

    def test_xs_int_list_from_repeated_list(self):
        lst1 = [1, 2, 3, 4]
        lst2 = lst1 * 7
        xs_lst1 = xs_int_list(*tuple(lst1))
        xs_lst2 = xs_int_list_from_repeated_list(xs_lst1, int32(7))
        self.assertEqual(istr(lst2), xs_int_list_to_string(xs_lst2))
        self.assertEqual(len(lst2), xs_int_list_size(xs_lst2))

    def test_xs_int_list_from_repeated_list_negative_times(self):
        xs_lst = xs_int_list(int32(1), int32(2), int32(3))
        result = xs_int_list_from_repeated_list(xs_lst, int32(-1))
        self.assertEqual(c_int_list_generic_error, result)

    def test_xs_int_list_from_repeated_list_zero_times(self):
        xs_lst = xs_int_list(int32(1), int32(2), int32(3))
        result = xs_int_list_from_repeated_list(xs_lst, int32(0))
        self.assertGreaterEqual(result, 0)
        self.assertEqual(0, xs_int_list_size(result))

    def test_xs_int_list_from_repeated_list_overflow(self):
        xs_lst = xs_int_list(int32(1), int32(2), int32(3))
        result = xs_int_list_from_repeated_list(xs_lst, c_int_list_max_capacity)
        self.assertEqual(c_int_list_max_capacity_error, result)

    def test_xs_int_list_from_array(self):
        xs_arr = xs_array_create_int(10, 5)
        lst = [5] * 10
        xs_lst = xs_int_list_from_array(xs_arr)
        self.assertEqual(istr(lst), xs_int_list_to_string(xs_lst))
        self.assertEqual(xs_array_get_size(xs_arr), xs_int_list_size(xs_lst))
        self.assertEqual(len(lst), xs_int_list_size(xs_lst))

    def test_xs_int_list_from_array_fail_over_max_capacity(self):
        xs_arr = xs_array_create_int(c_int_list_max_capacity, 5)
        self.assertEqual(c_int_list_generic_error, xs_int_list_from_array(xs_arr))
        xs_array_resize_int(xs_arr, 0)

    def test_xs_int_list_use_array_as_source(self):
        xs_arr = xs_array_create_int(10, 5)
        lst = [5] * 10
        xs_lst = xs_int_list_use_array_as_source(xs_arr)
        self.assertEqual(istr(lst), xs_int_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_int_list_size(xs_lst))
        xs_array_set_int(xs_arr, 1, 2000)
        self.assertEqual(xs_array_get_int(xs_arr, 1), xs_int_list_get(xs_lst, int32(0)))

    def test_xs_int_list_get(self):
        lst = list(i32range(-1, 100))
        xs_lst = xs_int_list_from_range(int32(-1), int32(100))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            self.assertEqual(lst[i], xs_int_list_get(xs_lst, int32(i)))
            self.assertEqual(c_int_list_success, xs_int_list_last_error())

    def test_xs_int_list_get_fail_with_incorrect_idx(self):
        xs_lst = xs_int_list(int32(-1), int32(0), int32(1), int32(2))
        self.assertEqual(c_int_list_generic_error, xs_int_list_get(xs_lst, int32(4)))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())
        self.assertEqual(c_int_list_generic_error, xs_int_list_get(xs_lst, int32(-1)))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())

    def test_xs_int_list_set(self):
        lst = list(i32range(-1, 100))
        xs_lst = xs_int_list_from_range(int32(-1), int32(100))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            v = randint(-100, 100)
            self.assertEqual(c_int_list_success, xs_int_list_set(xs_lst, int32(i), int32(v)))
            lst[i] = v
        self.assertEqual(istr(lst), xs_int_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_int_list_size(xs_lst))

    def test_xs_int_list_set_fail_with_incorrect_idx(self):
        xs_lst = xs_int_list(int32(-1), int32(0), int32(1), int32(2))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_set(xs_lst, int32(4), int32(5)))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_set(xs_lst, int32(-1), int32(5)))

    def test_xs_int_list_append(self):
        xs_lst = xs_int_list_create()
        lst = []
        for i in i32range(11, 22):
            xs_int_list_append(xs_lst, i)
            lst.append(i)
        self.assertEqual(len(lst), xs_int_list_size(xs_lst))
        self.assertEqual(istr(lst), xs_int_list_to_string(xs_lst))

    def test_xs_int_list_append_fail_over_max_capacity(self):
        xs_lst = xs_int_list_from_repeated_val(int32(1), c_int_list_max_capacity - 1)
        self.assertLessEqual(0, xs_lst)
        self.assertEqual(c_int_list_max_capacity_error, xs_int_list_append(xs_lst, int32(10)))
        xs_int_list_clear(xs_lst)

    def test_xs_int_list_insert(self):
        lst = [-1, 0, 1, 2, 3, 4]
        xs_lst = xs_int_list(*tuple(lst))
        for v in i32range(100):
            i = randint(0, len(lst))
            self.assertEqual(c_int_list_success, xs_int_list_insert(xs_lst, int32(i), v))
            lst.insert(i, v)
        self.assertEqual(istr(lst), xs_int_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_int_list_size(xs_lst))

    def test_xs_int_list_insert_fail_with_incorrect_idx(self):
        xs_lst = xs_int_list(int32(1), int32(2), int32(3))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_insert(xs_lst, int32(-1)))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_insert(xs_lst, int32(4)))

    def test_xs_int_list_insert_fail_over_max_capacity(self):
        xs_lst = xs_int_list_from_repeated_val(int32(1), c_int_list_max_capacity - 1)
        self.assertEqual(c_int_list_max_capacity_error, xs_int_list_insert(xs_lst, int32(100)))
        xs_int_list_clear(xs_lst)

    def test_xs_int_list_pop(self):
        lst = [-1, 0, 1, 2, 3, 4]
        xs_lst = xs_int_list(*tuple(lst))
        for _ in range(len(lst)):
            self.assertEqual(lst.pop(), xs_int_list_pop(xs_lst))
            self.assertEqual(c_int_list_success, xs_int_list_last_error())
        self.assertEqual(len(lst), xs_int_list_size(xs_lst))
        self.assertEqual(istr(lst), xs_int_list_to_string(xs_lst))

    def test_xs_int_list_pop_at_index(self):
        xs_lst = xs_int_list_from_range(int32(-1), int32(200))
        lst = list(i32range(-1, 200))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            val = lst[i]
            self.assertEqual(val, xs_int_list_pop(xs_lst, int32(i)))
            lst.pop(i)
            self.assertEqual(c_int_list_success, xs_int_list_last_error())
        self.assertEqual(istr(lst), xs_int_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_int_list_size(xs_lst))

    def test_xs_int_list_pop_fail_with_incorrect_idx(self):
        xs_lst = xs_int_list(int32(-1), int32(0), int32(1), int32(2))
        self.assertEqual(c_int_list_generic_error, xs_int_list_pop(xs_lst, int32(4)))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())
        self.assertEqual(c_int_list_generic_error, xs_int_list_pop(xs_lst, int32(-1)))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())

    def test_xs_int_list_pop_empty_list(self):
        xs_lst = xs_int_list_create()
        self.assertEqual(0, xs_int_list_size(xs_lst))
        result = xs_int_list_pop(xs_lst)
        self.assertEqual(c_int_list_generic_error, result)
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())
        self.assertEqual(0, xs_int_list_size(xs_lst))

    def test_xs_int_list_pop_until_empty_then_pop_again(self):
        xs_lst = xs_int_list(int32(10), int32(20))
        self.assertEqual(20, xs_int_list_pop(xs_lst))
        self.assertEqual(10, xs_int_list_pop(xs_lst))
        self.assertEqual(0, xs_int_list_size(xs_lst))
        result = xs_int_list_pop(xs_lst)
        self.assertEqual(c_int_list_generic_error, result)
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())
        self.assertEqual(0, xs_int_list_size(xs_lst))
        self.assertEqual("[]", xs_int_list_to_string(xs_lst))

    def test_xs_int_list_pop_append_cycle(self):
        xs_lst = xs_int_list_create(int32(4))
        lst = []
        for i in range(20):
            xs_int_list_append(xs_lst, int32(i))
            lst.append(i)
        for _ in range(15):
            lst.pop()
            xs_int_list_pop(xs_lst)
        for i in range(100, 120):
            xs_int_list_append(xs_lst, int32(i))
            lst.append(i)
        self.assertEqual(istr(lst), xs_int_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_int_list_size(xs_lst))

    def test_xs_int_list_shrink_after_pop_then_append(self):
        xs_lst = xs_int_list_create(int32(0))
        for i in i32range(0, 50):
            xs_int_list_append(xs_lst, i)
        for _ in range(40):
            xs_int_list_pop(xs_lst)
        remaining = list(range(10))
        self.assertEqual(istr(remaining), xs_int_list_to_string(xs_lst))
        self.assertEqual(10, xs_int_list_size(xs_lst))
        xs_int_list_append(xs_lst, int32(99))
        remaining.append(99)
        self.assertEqual(istr(remaining), xs_int_list_to_string(xs_lst))
        self.assertEqual(11, xs_int_list_size(xs_lst))

    def test_xs_int_list_remove(self):
        xs_lst = xs_int_list_from_range(int32(-1), int32(200))
        lst = list(i32range(-1, 200))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            val = lst[i]
            self.assertEqual(i, xs_int_list_remove(xs_lst, val))
            lst.remove(val)

        self.assertEqual(istr(lst), xs_int_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_int_list_size(xs_lst))

    def test_xs_int_list_remove_fail_with_incorrect_idx(self):
        xs_lst = xs_int_list(int32(-1), int32(0), int32(1), int32(2))
        self.assertEqual(c_int_list_generic_error, xs_int_list_remove(xs_lst, int32(4)))

    def test_xs_int_list_index(self):
        xs_lst = xs_int_list_from_range(int32(-1), int32(200))
        lst = list(i32range(-1, 200))
        for _ in range(100):
            val = lst[randint(0, len(lst) - 1)]
            self.assertEqual(lst.index(val), xs_int_list_index(xs_lst, val))

    def test_xs_int_list_index_with_ranges(self):
        xs_lst = xs_int_list()
        lst = []
        for _ in range(500):
            val = randint(-100, 101)
            xs_int_list_append(xs_lst, int32(val))
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
                params_xs = (xs_lst, val) + data
                params = (val,) + data
                try:
                    r = lst.index(params[0], params[1], params[2])
                except ValueError:
                    r = c_int_list_generic_error
                self.assertEqual(r, xs_int_list_index(*params_xs))

    def test_xs_int_list_index_fail_with_incorrect_idx(self):
        xs_lst = xs_int_list(int32(1), int32(2), int32(3))
        self.assertEqual(c_int_list_generic_error, xs_int_list_index(xs_lst, int32(4)))

    def test_xs_int_list_contains(self):
        xs_lst = xs_int_list(int32(1), int32(2))
        self.assertTrue(xs_int_list_contains(xs_lst, int32(1)))
        self.assertTrue(xs_int_list_contains(xs_lst, int32(2)))
        self.assertFalse(xs_int_list_contains(xs_lst, int32(3)))

    def test_xs_int_list_sort(self):
        for _ in range(100):
            size = randint(1, 100)
            xs_lst = xs_int_list_create(int32(0))
            lst = []
            for _ in range(size):
                val = randint(-100, 100)
                xs_int_list_append(xs_lst, int32(val))
                lst.append(val)
            lst.sort()
            xs_int_list_sort(xs_lst)
            self.assertEqual(istr(lst), xs_int_list_to_string(xs_lst))
            self.assertEqual(len(lst), xs_int_list_size(xs_lst))

    def test_xs_int_list_sort_reverse(self):
        for _ in range(100):
            size = randint(0, 100)
            xs_lst = xs_int_list_create(int32(size))
            lst = []
            for _ in range(size):
                val = randint(-100, 100)
                xs_int_list_append(xs_lst, int32(val))
                lst.append(val)
            lst.sort(reverse=True)
            xs_int_list_sort(xs_lst, True)
            self.assertEqual(istr(lst), xs_int_list_to_string(xs_lst))
            self.assertEqual(len(lst), xs_int_list_size(xs_lst))

    def test_xs_int_list_sort_single_element(self):
        xs_lst = xs_int_list(int32(42))
        xs_int_list_sort(xs_lst)
        self.assertEqual(istr([42]), xs_int_list_to_string(xs_lst))

    def test_xs_int_list_sort_two_elements(self):
        xs_lst = xs_int_list(int32(5), int32(3))
        xs_int_list_sort(xs_lst)
        self.assertEqual(istr([3, 5]), xs_int_list_to_string(xs_lst))
        xs_lst2 = xs_int_list(int32(5), int32(3))
        xs_int_list_sort(xs_lst2, True)
        self.assertEqual(istr([5, 3]), xs_int_list_to_string(xs_lst2))

    def test_xs_int_list_sort_empty(self):
        xs_lst = xs_int_list()
        xs_int_list_sort(xs_lst)
        self.assertEqual(istr([]), xs_int_list_to_string(xs_lst))

    def test_xs_int_list_to_string_test(self):
        xs_lst = xs_int_list(int32(-1), int32(0), int32(1), int32(2), int32(3))
        self.assertEqual("[-1, 0, 1, 2, 3]", xs_int_list_to_string(xs_lst))
        xs_lst_empty = xs_int_list()
        self.assertEqual("[]", xs_int_list_to_string(xs_lst_empty))

    def test_xs_int_list_reverse_even(self):
        lst = [-1, 0, 1, 2, 3, 4]
        xs_lst = xs_int_list(*tuple(lst))

        xs_int_list_reverse(xs_lst)
        lst.reverse()

        self.assertEqual(istr(lst), xs_int_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_int_list_size(xs_lst))

    def test_xs_int_list_reverse_odd(self):
        lst = [-1, 0, 1, 2, 3, 4, 5]
        xs_lst = xs_int_list(*tuple(lst))

        xs_int_list_reverse(xs_lst)
        lst.reverse()

        self.assertEqual(istr(lst), xs_int_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_int_list_size(xs_lst))

    def test_xs_int_list_reverse_empty(self):
        lst = []
        xs_lst = xs_int_list(*tuple(lst))

        xs_int_list_reverse(xs_lst)
        lst.reverse()

        self.assertEqual(istr(lst), xs_int_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_int_list_size(xs_lst))

    def test_xs_int_list_copy(self):
        lst = [-1, 0, 1, 2, 3, 4]
        xs_lst = xs_int_list(*tuple(lst))
        xs_copy = xs_int_list_copy(xs_lst)
        self.assertEqual(xs_int_list_to_string(xs_lst), xs_int_list_to_string(xs_copy))
        self.assertEqual(xs_int_list_size(xs_lst), xs_int_list_size(xs_copy))

        xs_int_list_set(xs_lst, int32(0), int32(100))
        self.assertEqual(istr(lst), xs_int_list_to_string(xs_copy))
        self.assertEqual(len(lst), xs_int_list_size(xs_copy))

    def test_xs_int_list_copy_slices(self):
        lst = [-1, 0, 1, 2, 3, 4]
        xs_lst = xs_int_list(*tuple(lst))

        for i in i32range(len(lst) * -1, len(lst) + 1):
            for j in i32range(len(lst) * -1, len(lst) + 1):
                xs_copy = xs_int_list_copy(xs_lst, i, j)
                copy_lst = lst[i:j]
                self.assertEqual(istr(copy_lst), xs_int_list_to_string(xs_copy))
                self.assertEqual(len(copy_lst), xs_int_list_size(xs_copy))

    def test_xs_int_list_copy_empty(self):
        xs_lst = xs_int_list()
        xs_copy = xs_int_list_copy(xs_lst)
        self.assertEqual(0, xs_int_list_size(xs_copy))
        self.assertEqual("[]", xs_int_list_to_string(xs_copy))

    def test_xs_int_list_copy_single_element(self):
        xs_lst = xs_int_list(int32(42))
        xs_copy = xs_int_list_copy(xs_lst)
        self.assertEqual(1, xs_int_list_size(xs_copy))
        self.assertEqual(istr([42]), xs_int_list_to_string(xs_copy))

    def test_xs_int_list_extend(self):
        lst1 = [-1, 0, 1, 2, 3, 4]
        lst2 = [0, -10, 20, -30, 40, -50, 60, -70, 80, -90]

        xs_lst1 = xs_int_list(*tuple(lst1))
        xs_lst2 = xs_int_list(*tuple(lst2))
        self.assertEqual(c_int_list_success, xs_int_list_extend(xs_lst1, xs_lst2))
        lst1.extend(lst2)

        self.assertEqual(istr(lst1), xs_int_list_to_string(xs_lst1))
        self.assertEqual(len(lst1), xs_int_list_size(xs_lst1))

    def test_xs_int_list_extend_at_exact_capacity_boundary(self):
        lst1 = list(range(12))
        xs_lst1 = xs_int_list(*[int32(x) for x in lst1])
        self.assertEqual(13, xs_array_get_size(xs_lst1))
        xs_lst2 = xs_int_list(int32(99))
        self.assertEqual(c_int_list_success, xs_int_list_extend(xs_lst1, xs_lst2))
        lst1.append(99)
        self.assertEqual(13, xs_int_list_size(xs_lst1))
        self.assertEqual(istr(lst1), xs_int_list_to_string(xs_lst1))

    def test_xs_int_list_extend_fills_exactly(self):
        lst1 = list(range(7))
        lst2 = list(range(10, 16))
        xs_lst1 = xs_int_list(*[int32(x) for x in lst1])
        xs_lst2 = xs_int_list(*[int32(x) for x in lst2])
        cap = xs_array_get_size(xs_lst1)
        needed = len(lst1) + len(lst2) + 1
        if needed > cap:
            pass
        self.assertEqual(c_int_list_success, xs_int_list_extend(xs_lst1, xs_lst2))
        lst1.extend(lst2)
        self.assertEqual(istr(lst1), xs_int_list_to_string(xs_lst1))
        self.assertEqual(len(lst1), xs_int_list_size(xs_lst1))

    def test_xs_int_list_extend_with_array(self):
        lst1 = [-1, 0, 1, 2, 3, 4]
        lst2 = [5] * 10

        xs_lst = xs_int_list(*tuple(lst1))
        xs_arr = xs_array_create_int(10, 5)
        self.assertEqual(c_int_list_success, xs_int_list_extend_with_array(xs_lst, xs_arr))
        lst1.extend(lst2)

        self.assertEqual(istr(lst1), xs_int_list_to_string(xs_lst))
        self.assertEqual(len(lst1), xs_int_list_size(xs_lst))

    def test_xs_int_list_extend_with_array_at_exact_capacity_boundary(self):
        lst1 = list(range(12))
        xs_lst = xs_int_list(*[int32(x) for x in lst1])
        self.assertEqual(13, xs_array_get_size(xs_lst))
        xs_arr = xs_array_create_int(1, 99)
        self.assertEqual(c_int_list_success, xs_int_list_extend_with_array(xs_lst, xs_arr))
        lst1.append(99)
        self.assertEqual(13, xs_int_list_size(xs_lst))
        self.assertEqual(istr(lst1), xs_int_list_to_string(xs_lst))

    def test_xs_int_list_clear(self):
        xs_lst = xs_int_list(int32(-1), int32(0), int32(1), int32(2), int32(3), int32(4))

        self.assertEqual(c_int_list_success, xs_int_list_clear(xs_lst))
        self.assertEqual("[]", xs_int_list_to_string(xs_lst))
        self.assertEqual(0, xs_int_list_size(xs_lst))

    def test_xs_int_list_clear_shrinks_large_capacity(self):
        xs_lst = xs_int_list_create(int32(100))
        xs_int_list_append(xs_lst, int32(1))
        xs_int_list_append(xs_lst, int32(2))
        xs_int_list_append(xs_lst, int32(3))
        self.assertEqual(3, xs_int_list_size(xs_lst))
        capacity_before = xs_array_get_size(xs_lst)
        self.assertGreater(capacity_before, 8)
        self.assertEqual(c_int_list_success, xs_int_list_clear(xs_lst))
        self.assertEqual(0, xs_int_list_size(xs_lst))
        capacity_after = xs_array_get_size(xs_lst)
        self.assertLessEqual(capacity_after, 8)

    def test_xs_int_list_clear_small_list(self):
        xs_lst = xs_int_list(int32(1), int32(2))
        self.assertEqual(c_int_list_success, xs_int_list_clear(xs_lst))
        self.assertEqual(0, xs_int_list_size(xs_lst))

    def test_xs_int_list_compare(self):
        xs_lst1 = xs_int_list(int32(-1), int32(0), int32(2))
        xs_lst2 = xs_int_list(int32(-1), int32(0), int32(1))

        self.assertEqual(1, xs_int_list_compare(xs_lst1, xs_lst2))
        self.assertEqual(-1, xs_int_list_compare(xs_lst2, xs_lst1))
        self.assertEqual(0, xs_int_list_compare(xs_lst1, xs_lst1))

    def test_xs_int_list_compare_same_prefix(self):
        xs_lst1 = xs_int_list(int32(-1), int32(0), int32(1))
        xs_lst2 = xs_int_list(int32(-1), int32(0), int32(1), int32(2), int32(3), int32(4))

        self.assertEqual(-1, xs_int_list_compare(xs_lst1, xs_lst2))
        self.assertEqual(1, xs_int_list_compare(xs_lst2, xs_lst1))

    def test_xs_int_list_compare_empty(self):
        xs_lst1 = xs_int_list()
        xs_lst2 = xs_int_list()

        self.assertEqual(0, xs_int_list_compare(xs_lst1, xs_lst2))

    def test_xs_int_list_sum_count_min_max(self):
        xs_lst = xs_int_list()
        lst = []
        for _ in range(100):
            v = randint(-20, 21)
            xs_int_list_append(xs_lst, int32(v))
            lst.append(v)

        self.assertEqual(sum(lst), xs_int_list_sum(xs_lst))
        self.assertEqual(lst.count(1), xs_int_list_count(xs_lst, int32(1)))
        self.assertEqual(min(lst), xs_int_list_min(xs_lst))
        self.assertEqual(max(lst), xs_int_list_max(xs_lst))

    def test_xs_int_list_sum_count_min_max_on_empty(self):
        xs_lst = xs_int_list()
        lst = []

        self.assertEqual(sum(lst), xs_int_list_sum(xs_lst))
        self.assertEqual(lst.count(1), xs_int_list_count(xs_lst, int32(1)))
        self.assertEqual(c_int_list_generic_error, xs_int_list_min(xs_lst))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())
        self.assertEqual(c_int_list_generic_error, xs_int_list_max(xs_lst))
        self.assertEqual(c_int_list_index_out_of_range_error, xs_int_list_last_error())


def istr(lst: list[int | int32]) -> str:
    return str([int(x) for x in lst])
