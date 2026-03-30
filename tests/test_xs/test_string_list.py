import random
import unittest
from random import randint

import xs.string_list as _sl
from xs.string_list import *
from xs_converter.functions import xs_array_create_string, xs_array_set_string, xs_array_get_string, xs_array_get_int


class StringListTest(unittest.TestCase):
    def test_xs_string_list(self):
        for i in i32range(0, 13):
            params = to_str_lst(range(i))
            xs_lst = xs_string_list(*params)
            self.assertEqual(i, xs_string_list_size(xs_lst))
            self.assertEqual(to_str(params), xs_string_list_to_string(xs_lst))

    def test_xs_string_list_stop_at_magic_number(self):
        xs_lst = xs_string_list("aa", "!<[empty", "bb")
        self.assertEqual(to_str(["aa"]), xs_string_list_to_string(xs_lst))

    def test_xs_string_list_create_empty(self):
        xs_lst = xs_string_list_create(int32(16))
        self.assertEqual(0, xs_string_list_size(xs_lst))

    def test_xs_string_list_create_fail_at_negative_capacity(self):
        xs_lst = xs_string_list_create(int32(-1))
        self.assertEqual(c_string_list_generic_error, xs_lst)

    def test_xs_string_list_create_fail_over_max_capacity(self):
        xs_lst = xs_string_list_create(c_string_list_max_capacity)
        self.assertEqual(c_string_list_generic_error, xs_lst)
        xs_string_list_clear(xs_lst)

    def test_xs_string_list_from_repeated_val(self):
        xs_lst = xs_string_list_from_repeated_val("aa", int32(7))
        self.assertEqual(7, xs_string_list_size(xs_lst))
        self.assertEqual('["aa", "aa", "aa", "aa", "aa", "aa", "aa"]', xs_string_list_to_string(xs_lst))

    def test_xs_string_list_from_repeated_val_fail_with_negative_repeat(self):
        xs_lst = xs_string_list_from_repeated_val("aa", int32(-2))
        self.assertEqual(c_string_list_generic_error, xs_lst)

    def test_xs_string_list_from_repeated_val_fail_over_max_capacity(self):
        xs_lst = xs_string_list_from_repeated_val("aa", c_string_list_max_capacity + 1)
        self.assertEqual(c_string_list_generic_error, xs_lst)
        xs_string_list_clear(xs_lst)

    def test_xs_string_list_from_repeated_list(self):
        lst1 = ["aa", "bb", "cc", "dd"]
        lst2 = lst1 * 7
        xs_lst1 = xs_string_list(*lst1)
        xs_lst2 = xs_string_list_from_repeated_list(xs_lst1, int32(7))
        self.assertEqual(to_str(lst2), xs_string_list_to_string(xs_lst2))
        self.assertEqual(len(lst2), xs_string_list_size(xs_lst2))

    def test_xs_string_list_from_repeated_list_negative_times(self):
        xs_lst = xs_string_list("aa", "bb", "cc")
        result = xs_string_list_from_repeated_list(xs_lst, int32(-1))
        self.assertEqual(c_string_list_generic_error, result)

    def test_xs_string_list_from_repeated_list_zero_times(self):
        xs_lst = xs_string_list("aa", "bb", "cc")
        result = xs_string_list_from_repeated_list(xs_lst, int32(0))
        self.assertGreaterEqual(result, 0)
        self.assertEqual(0, xs_string_list_size(result))

    def test_xs_string_list_from_repeated_list_overflow(self):
        xs_lst = xs_string_list("aa", "bb", "cc")
        result = xs_string_list_from_repeated_list(xs_lst, c_string_list_max_capacity)
        self.assertEqual(c_string_list_max_capacity_error, result)

    def test_xs_string_list_from_array(self):
        xs_arr = xs_array_create_string(10, "aaa")
        xs_lst = xs_string_list_from_array(xs_arr)
        lst = ["aaa"] * 10
        self.assertEqual(to_str(lst), xs_string_list_to_string(xs_lst))
        self.assertEqual(xs_array_get_size(xs_arr), xs_string_list_size(xs_lst))
        self.assertEqual(len(lst), xs_string_list_size(xs_lst))

    def test_xs_string_list_from_array_fail_over_max_capacity(self):
        orig = _sl.c_string_list_max_capacity
        _sl.c_string_list_max_capacity = int32(1000)
        xs_arr = xs_array_create_string(_sl.c_string_list_max_capacity + 1, "aaa")
        self.assertEqual(c_string_list_max_capacity_error, xs_string_list_from_array(xs_arr))
        xs_array_resize_string(xs_arr, 0)
        _sl.c_string_list_max_capacity = orig

    def test_xs_string_list_use_array_as_source(self):
        xs_arr = xs_array_create_string(10, "bbb")
        lst = ["bbb"] * 10
        xs_lst = xs_string_list_use_array_as_source(xs_arr)
        self.assertEqual(to_str(lst), xs_string_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_string_list_size(xs_lst))
        xs_array_set_string(xs_arr, 0, "abc")
        self.assertEqual(xs_array_get_string(xs_arr, 0), xs_string_list_get(xs_lst, int32(0)))

    def test_xs_string_list_get(self):
        lst = to_str_lst(range(-1, 100))
        xs_lst = xs_string_list_create(int32(101))
        for v in range(-1, 100):
            xs_string_list_append(xs_lst, str(v))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            self.assertEqual(lst[i], xs_string_list_get(xs_lst, int32(i)))
            self.assertEqual(c_string_list_success, xs_string_list_last_error())

    def test_xs_string_list_get_fail_with_incorrect_idx(self):
        xs_lst = xs_string_list("aa", "bb", "cc", "dd")
        self.assertEqual(str(c_string_list_generic_error), xs_string_list_get(xs_lst, int32(4)))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_last_error())
        self.assertEqual(str(c_string_list_generic_error), xs_string_list_get(xs_lst, int32(-1)))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_last_error())

    def test_xs_string_list_set(self):
        lst = to_str_lst(range(-1, 100))
        xs_lst = xs_string_list_create(int32(101))
        for v in range(-1, 100):
            xs_string_list_append(xs_lst, str(v))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            v = random.random()
            self.assertEqual(c_string_list_success, xs_string_list_set(xs_lst, int32(i), str(v)))
            lst[i] = str(v)
        self.assertEqual(to_str(lst), xs_string_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_string_list_size(xs_lst))

    def test_xs_string_list_set_fail_with_incorrect_idx(self):
        xs_lst = xs_string_list("aa", "bb", "cc", "dd")
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_set(xs_lst, int32(4), "ff"))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_set(xs_lst, int32(-1), "ff"))

    def test_xs_string_list_append(self):
        xs_lst = xs_string_list_create()
        lst = []
        for i in range(11, 22):
            xs_string_list_append(xs_lst, str(i))
            lst.append(str(i))
        self.assertEqual(len(lst), xs_string_list_size(xs_lst))
        self.assertEqual(to_str(lst), xs_string_list_to_string(xs_lst))

    def test_xs_string_list_append_fail_over_max_capacity(self):
        orig = _sl.c_string_list_max_capacity
        _sl.c_string_list_max_capacity = int32(1000)
        xs_lst = xs_string_list_from_repeated_val("aaa", _sl.c_string_list_max_capacity)
        self.assertEqual(c_string_list_max_capacity_error, xs_string_list_append(xs_lst, "bbb"))
        xs_string_list_clear(xs_lst)
        _sl.c_string_list_max_capacity = orig

    def test_xs_string_list_insert(self):
        lst = ["aa", "bb", "cc", "dd", "ee", "ff"]
        xs_lst = xs_string_list(*lst)
        for v in range(0, 100):
            i = randint(0, len(lst))
            lst.insert(i, str(v))
            self.assertEqual(c_string_list_success, xs_string_list_insert(xs_lst, int32(i), str(v)))
        self.assertEqual(to_str(lst), xs_string_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_string_list_size(xs_lst))

    def test_xs_string_list_insert_fail_with_incorrect_idx(self):
        xs_lst = xs_string_list("aa", "bb", "cc")
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_insert(xs_lst, int32(-1), "dd"))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_insert(xs_lst, int32(4), "ee"))

    def test_xs_string_list_insert_fail_over_max_capacity(self):
        orig = _sl.c_string_list_max_capacity
        _sl.c_string_list_max_capacity = int32(1000)
        xs_lst = xs_string_list_from_repeated_val("aa", _sl.c_string_list_max_capacity)
        self.assertEqual(c_string_list_max_capacity_error, xs_string_list_insert(xs_lst, int32(100), "bb"))
        xs_string_list_clear(xs_lst)
        _sl.c_string_list_max_capacity = orig

    def test_xs_string_list_pop(self):
        lst = ["aa", "bb", "cc", "dd", "ee", "ff"]
        xs_lst = xs_string_list(*lst)
        for _ in range(len(lst)):
            self.assertEqual(lst.pop(), xs_string_list_pop(xs_lst))
            self.assertEqual(c_string_list_success, xs_string_list_last_error())
        self.assertEqual(len(lst), xs_string_list_size(xs_lst))
        self.assertEqual(str(lst), xs_string_list_to_string(xs_lst))

    def test_xs_string_list_pop_at_index(self):
        xs_lst = xs_string_list_create(int32(201))
        for v in range(-1, 200):
            xs_string_list_append(xs_lst, str(v))
        lst = list(range(-1, 200))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            self.assertEqual(str(lst[i]), xs_string_list_pop(xs_lst, int32(i)))
            lst.pop(i)
            self.assertEqual(c_string_list_success, xs_string_list_last_error())
        self.assertEqual(to_str(lst), xs_string_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_string_list_size(xs_lst))

    def test_xs_string_list_pop_at_max(self):
        orig = _sl.c_string_list_max_capacity
        _sl.c_string_list_max_capacity = int32(1000)
        xs_lst = xs_string_list_from_repeated_val("aa", _sl.c_string_list_max_capacity)
        self.assertEqual("aa", xs_string_list_pop(xs_lst, _sl.c_string_list_max_capacity))
        self.assertEqual(_sl.c_string_list_max_capacity - 1, xs_string_list_size(xs_lst))
        xs_string_list_clear(xs_lst)
        _sl.c_string_list_max_capacity = orig

    def test_xs_string_list_pop_fail_with_incorrect_idx(self):
        xs_lst = xs_string_list("aa", "bb", "cc", "dd")
        self.assertEqual(str(c_string_list_generic_error), xs_string_list_pop(xs_lst, int32(4)))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_last_error())
        self.assertEqual(str(c_string_list_generic_error), xs_string_list_pop(xs_lst, int32(-1)))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_last_error())

    def test_xs_string_list_pop_empty_list(self):
        xs_lst = xs_string_list_create()
        self.assertEqual(0, xs_string_list_size(xs_lst))
        result = xs_string_list_pop(xs_lst)
        self.assertEqual(str(c_string_list_generic_error), str(result))

    def test_xs_string_list_pop_until_empty_then_pop_again(self):
        xs_lst = xs_string_list("aa", "bb")
        self.assertEqual("bb", xs_string_list_pop(xs_lst))
        self.assertEqual("aa", xs_string_list_pop(xs_lst))
        self.assertEqual(0, xs_string_list_size(xs_lst))
        result = xs_string_list_pop(xs_lst)
        self.assertEqual(str(c_string_list_generic_error), str(result))

    def test_xs_string_list_pop_append_cycle(self):
        xs_lst = xs_string_list_create(int32(4))
        lst = []
        for i in range(20):
            xs_string_list_append(xs_lst, str(i))
            lst.append(str(i))
        for _ in range(15):
            lst.pop()
            xs_string_list_pop(xs_lst)
        for i in range(100, 120):
            xs_string_list_append(xs_lst, str(i))
            lst.append(str(i))
        self.assertEqual(to_str(lst), xs_string_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_string_list_size(xs_lst))

    def test_xs_string_list_shrink_after_pop_then_append(self):
        xs_lst = xs_string_list_create(int32(0))
        for i in range(50):
            xs_string_list_append(xs_lst, str(i))
        for _ in range(40):
            xs_string_list_pop(xs_lst)
        remaining = [str(i) for i in range(10)]
        self.assertEqual(to_str(remaining), xs_string_list_to_string(xs_lst))
        self.assertEqual(10, xs_string_list_size(xs_lst))
        xs_string_list_append(xs_lst, "99")
        remaining.append("99")
        self.assertEqual(to_str(remaining), xs_string_list_to_string(xs_lst))
        self.assertEqual(11, xs_string_list_size(xs_lst))

    def test_xs_string_list_remove(self):
        xs_lst = xs_string_list_create(int32(201))
        for v in range(-1, 200):
            xs_string_list_append(xs_lst, str(v))
        lst = to_str_lst(range(-1, 200, 1))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            val = lst[i]
            self.assertEqual(i, xs_string_list_remove(xs_lst, val))
            lst.remove(val)

        self.assertEqual(to_str(lst), xs_string_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_string_list_size(xs_lst))

    def test_xs_string_list_remove_fail_with_incorrect_idx(self):
        xs_lst = xs_string_list("aa", "bb", "cc", "dd")
        self.assertEqual(c_string_list_generic_error, xs_string_list_remove(xs_lst, "ff"))

    def test_xs_string_list_index(self):
        xs_lst = xs_string_list_create(int32(201))
        for v in range(-1, 200):
            xs_string_list_append(xs_lst, str(v))
        lst = to_str_lst(range(-1, 200))
        for _ in range(100):
            val = lst[randint(0, len(lst) - 1)]
            self.assertEqual(lst.index(val), xs_string_list_index(xs_lst, val))

    def test_xs_string_list_index_with_ranges(self):
        xs_lst = xs_string_list()
        lst = []
        for _ in range(500):
            val = str(random.randint(-100, 100))
            xs_string_list_append(xs_lst, val)
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
                    r = c_string_list_generic_error
                self.assertEqual(r, xs_string_list_index(*params_xs))

    def test_xs_string_list_index_fail_with_incorrect_idx(self):
        xs_lst = xs_string_list("aa", "bb", "cc")
        self.assertEqual(c_string_list_generic_error, xs_string_list_index(xs_lst, "dd"))

    def test_xs_string_list_contains(self):
        xs_lst = xs_string_list("aa", "bb")
        self.assertTrue(xs_string_list_contains(xs_lst, "aa"))
        self.assertTrue(xs_string_list_contains(xs_lst, "bb"))
        self.assertFalse(xs_string_list_contains(xs_lst, "cc"))

    def test_xs_string_list_sort(self):
        for _ in range(100):
            size = randint(0, 100)
            xs_lst = xs_string_list_create(int32(0))
            lst = []
            for _ in range(size):
                val = str(random.randint(-100, 100))
                xs_string_list_append(xs_lst, val)
                lst.append(val)
            lst.sort()
            xs_string_list_sort(xs_lst)
            self.assertEqual(to_str(lst), xs_string_list_to_string(xs_lst))
            self.assertEqual(len(lst), xs_string_list_size(xs_lst))

    def test_xs_string_list_sort_reverse(self):
        for _ in range(100):
            size = randint(0, 100)
            xs_lst = xs_string_list_create(int32(size))
            lst = []
            for _ in range(size):
                val = str(random.randint(-100, 100))
                xs_string_list_append(xs_lst, val)
                lst.append(val)
            lst.sort(reverse=True)
            xs_string_list_sort(xs_lst, True)
            self.assertEqual(to_str(lst), xs_string_list_to_string(xs_lst))
            self.assertEqual(len(lst), xs_string_list_size(xs_lst))

    def test_xs_string_list_sort_single_element(self):
        xs_lst = xs_string_list("aa")
        xs_string_list_sort(xs_lst)
        self.assertEqual(to_str(["aa"]), xs_string_list_to_string(xs_lst))

    def test_xs_string_list_sort_two_elements(self):
        xs_lst = xs_string_list("zz", "aa")
        xs_string_list_sort(xs_lst)
        self.assertEqual(to_str(["aa", "zz"]), xs_string_list_to_string(xs_lst))
        xs_lst2 = xs_string_list("aa", "zz")
        xs_string_list_sort(xs_lst2, True)
        self.assertEqual(to_str(["zz", "aa"]), xs_string_list_to_string(xs_lst2))

    def test_xs_string_list_sort_empty(self):
        xs_lst = xs_string_list()
        xs_string_list_sort(xs_lst)
        self.assertEqual("[]", xs_string_list_to_string(xs_lst))

    def test_xs_string_list_to_string_test(self):
        xs_lst = xs_string_list("aa", "bb", "cc", "dd", "ee")
        self.assertEqual('["aa", "bb", "cc", "dd", "ee"]', xs_string_list_to_string(xs_lst))
        xs_lst_empty = xs_string_list()
        self.assertEqual("[]", xs_string_list_to_string(xs_lst_empty))

    def test_xs_string_list_reverse_even(self):
        lst = ["aa", "bb", "cc", "dd", "ee", "ff"]
        xs_lst = xs_string_list(*lst)

        xs_string_list_reverse(xs_lst)
        lst.reverse()

        self.assertEqual(to_str(lst), xs_string_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_string_list_size(xs_lst))

    def test_xs_string_list_reverse_odd(self):
        lst = ["aa", "bb", "cc", "dd", "ee", "ff", "gg"]
        xs_lst = xs_string_list(*lst)

        xs_string_list_reverse(xs_lst)
        lst.reverse()

        self.assertEqual(to_str(lst), xs_string_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_string_list_size(xs_lst))

    def test_xs_string_list_reverse_empty(self):
        lst = []
        xs_lst = xs_string_list(*lst)

        xs_string_list_reverse(xs_lst)
        lst.reverse()

        self.assertEqual(to_str(lst), xs_string_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_string_list_size(xs_lst))

    def test_xs_string_list_copy(self):
        lst = ["aa", "bb", "cc", "dd", "ee", "ff"]
        xs_lst = xs_string_list(*lst)
        xs_copy = xs_string_list_copy(xs_lst)
        self.assertEqual(xs_string_list_to_string(xs_lst), xs_string_list_to_string(xs_copy))
        self.assertEqual(xs_string_list_size(xs_lst), xs_string_list_size(xs_copy))

        xs_string_list_set(xs_lst, int32(0), "zz")
        self.assertEqual(to_str(lst), xs_string_list_to_string(xs_copy))
        self.assertEqual(len(lst), xs_string_list_size(xs_copy))

    def test_xs_string_list_copy_slices(self):
        lst = ["aa", "bb", "cc", "dd", "ee", "ff"]
        xs_lst = xs_string_list(*lst)

        for i in i32range(len(lst) * -1, len(lst) + 1):
            for j in i32range(len(lst) * -1, len(lst) + 1):
                xs_copy = xs_string_list_copy(xs_lst, i, j)
                copy_lst = lst[i:j]
                self.assertEqual(to_str(copy_lst), xs_string_list_to_string(xs_copy))
                self.assertEqual(len(copy_lst), xs_string_list_size(xs_copy))

    def test_xs_string_list_copy_empty(self):
        xs_lst = xs_string_list()
        xs_copy = xs_string_list_copy(xs_lst)
        self.assertEqual(0, xs_string_list_size(xs_copy))
        self.assertEqual("[]", xs_string_list_to_string(xs_copy))

    def test_xs_string_list_copy_single_element(self):
        xs_lst = xs_string_list("aa")
        xs_copy = xs_string_list_copy(xs_lst)
        self.assertEqual(1, xs_string_list_size(xs_copy))
        self.assertEqual(to_str(["aa"]), xs_string_list_to_string(xs_copy))

    def test_xs_string_list_extend(self):
        lst1 = ["aa", "bb", "cc", "dd", "ee", "ff"]
        lst2 = ["aa", "bb", "cc", "dd", "ee", "ff", "gg", "hh", "ii", "jj"]

        xs_lst1 = xs_string_list(*lst1)
        xs_lst2 = xs_string_list(*lst2)
        self.assertEqual(c_string_list_success, xs_string_list_extend(xs_lst1, xs_lst2))
        lst1.extend(lst2)

        self.assertEqual(to_str(lst1), xs_string_list_to_string(xs_lst1))
        self.assertEqual(len(lst1), xs_string_list_size(xs_lst1))

    def test_xs_string_list_extend_at_exact_capacity_boundary(self):
        lst1 = [str(i) for i in range(12)]
        xs_lst1 = xs_string_list(*lst1)
        self.assertEqual(12, xs_array_get_size(xs_array_get_int(xs_lst1, 1)))
        xs_lst2 = xs_string_list("99")
        self.assertEqual(c_string_list_success, xs_string_list_extend(xs_lst1, xs_lst2))
        lst1.append("99")
        self.assertEqual(13, xs_string_list_size(xs_lst1))
        self.assertEqual(to_str(lst1), xs_string_list_to_string(xs_lst1))

    def test_xs_string_list_extend_fills_exactly(self):
        lst1 = [str(i) for i in range(7)]
        lst2 = [str(i) for i in range(10, 16)]
        xs_lst1 = xs_string_list(*lst1)
        xs_lst2 = xs_string_list(*lst2)
        self.assertEqual(c_string_list_success, xs_string_list_extend(xs_lst1, xs_lst2))
        lst1.extend(lst2)
        self.assertEqual(to_str(lst1), xs_string_list_to_string(xs_lst1))
        self.assertEqual(len(lst1), xs_string_list_size(xs_lst1))

    def test_xs_string_list_extend_with_array(self):
        lst1 = ["aa", "bb", "cc", "dd", "ee", "ff"]
        lst2 = ["zz"] * 10

        xs_lst = xs_string_list(*lst1)
        xs_arr = xs_array_create_string(10, "zz")
        self.assertEqual(c_string_list_success, xs_string_list_extend_with_array(xs_lst, xs_arr))
        lst1.extend(lst2)

        self.assertEqual(to_str(lst1), xs_string_list_to_string(xs_lst))
        self.assertEqual(len(lst1), xs_string_list_size(xs_lst))

    def test_xs_string_list_extend_with_array_copies_raw_array_values_in_order(self):
        lst1 = ["aa", "bb"]
        arr_values = ["one", "two", "three"]
        xs_lst = xs_string_list(*lst1)
        xs_arr = xs_array_create_string(len(arr_values))
        for i, value in enumerate(arr_values):
            xs_array_set_string(xs_arr, i, value)
        self.assertEqual(c_string_list_success, xs_string_list_extend_with_array(xs_lst, xs_arr))
        lst1.extend(arr_values)
        self.assertEqual(to_str(lst1), xs_string_list_to_string(xs_lst))
        self.assertEqual(len(lst1), xs_string_list_size(xs_lst))

    def test_xs_string_list_extend_with_array_at_exact_capacity_boundary(self):
        lst1 = [str(i) for i in range(12)]
        xs_lst = xs_string_list(*lst1)
        self.assertEqual(12, xs_array_get_size(xs_array_get_int(xs_lst, 1)))
        xs_arr = xs_array_create_string(1, "99")
        self.assertEqual(c_string_list_success, xs_string_list_extend_with_array(xs_lst, xs_arr))
        lst1.append("99")
        self.assertEqual(13, xs_string_list_size(xs_lst))
        self.assertEqual(to_str(lst1), xs_string_list_to_string(xs_lst))

    def test_xs_string_list_clear(self):
        xs_lst = xs_string_list("aa", "bb", "cc", "dd", "ee", "ff")

        self.assertEqual(c_string_list_success, xs_string_list_clear(xs_lst))
        self.assertEqual("[]", xs_string_list_to_string(xs_lst))
        self.assertEqual(0, xs_string_list_size(xs_lst))

    def test_xs_string_list_clear_shrinks_large_capacity(self):
        xs_lst = xs_string_list_create(int32(100))
        xs_string_list_append(xs_lst, "aa")
        xs_string_list_append(xs_lst, "bb")
        xs_string_list_append(xs_lst, "cc")
        self.assertEqual(3, xs_string_list_size(xs_lst))
        str_lst = xs_array_get_int(xs_lst, 1)
        capacity_before = xs_array_get_size(str_lst)
        self.assertGreater(capacity_before, 8)
        self.assertEqual(c_string_list_success, xs_string_list_clear(xs_lst))
        self.assertEqual(0, xs_string_list_size(xs_lst))
        str_lst = xs_array_get_int(xs_lst, 1)
        capacity_after = xs_array_get_size(str_lst)
        self.assertLessEqual(capacity_after, 8)

    def test_xs_string_list_clear_small_list(self):
        xs_lst = xs_string_list("aa", "bb")
        self.assertEqual(c_string_list_success, xs_string_list_clear(xs_lst))
        self.assertEqual(0, xs_string_list_size(xs_lst))

    def test_xs_string_list_compare(self):
        xs_lst1 = xs_string_list("aa", "bb", "dd")
        xs_lst2 = xs_string_list("aa", "bb", "cc")

        self.assertEqual(1, xs_string_list_compare(xs_lst1, xs_lst2))
        self.assertEqual(-1, xs_string_list_compare(xs_lst2, xs_lst1))
        self.assertEqual(0, xs_string_list_compare(xs_lst1, xs_lst1))

    def test_xs_string_list_compare_same_prefix(self):
        xs_lst1 = xs_string_list("aa", "bb", "cc")
        xs_lst2 = xs_string_list("aa", "bb", "cc", "dd")

        self.assertEqual(-1, xs_string_list_compare(xs_lst1, xs_lst2))
        self.assertEqual(1, xs_string_list_compare(xs_lst2, xs_lst1))

    def test_xs_string_list_compare_empty(self):
        xs_lst1 = xs_string_list()
        xs_lst2 = xs_string_list()

        self.assertEqual(0, xs_string_list_compare(xs_lst1, xs_lst2))

    def test_xs_string_list_count_min_max(self):
        xs_lst = xs_string_list()
        lst = []
        for _ in range(100):
            v = str(random.randint(-100, 100))
            xs_string_list_append(xs_lst, v)
            lst.append(v)

        self.assertEqual(lst.count(lst[0]), xs_string_list_count(xs_lst, lst[0]))
        self.assertEqual(min(lst), xs_string_list_min(xs_lst))
        self.assertEqual(max(lst), xs_string_list_max(xs_lst))

    def test_xs_string_list_count_min_max_on_empty(self):
        xs_lst = xs_string_list()
        lst = []

        self.assertEqual(lst.count(float32(1.0)), xs_string_list_count(xs_lst, float32(1.0)))
        self.assertEqual(str(c_string_list_generic_error), xs_string_list_min(xs_lst))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_last_error())
        self.assertEqual(str(c_string_list_generic_error), xs_string_list_max(xs_lst))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_last_error())


class StringListAllocationCleanupTest(unittest.TestCase):
    def setUp(self):
        self.orig_create_int = _sl.xs_array_create_int
        self.orig_create_string = _sl.xs_array_create_string
        self.orig_resize_int = _sl.xs_array_resize_int
        self.orig_resize_string = _sl.xs_array_resize_string

    def tearDown(self):
        _sl.xs_array_create_int = self.orig_create_int
        _sl.xs_array_create_string = self.orig_create_string
        _sl.xs_array_resize_int = self.orig_resize_int
        _sl.xs_array_resize_string = self.orig_resize_string

    def test_create_shrinks_int_array_when_string_array_allocation_fails(self):
        created: dict[str, int32] = {}

        def _create_int(*args, **kwargs):
            arr = self.orig_create_int(*args, **kwargs)
            created["arr"] = arr
            return arr

        def _create_string(*args, **kwargs):
            return int32(-1)

        def _resize_int(arr_id, new_size):
            self.orig_resize_int(arr_id, new_size)
            return int32(0)

        _sl.xs_array_create_int = _create_int
        _sl.xs_array_create_string = _create_string
        _sl.xs_array_resize_int = _resize_int

        self.assertEqual(c_string_list_generic_error, xs_string_list_create())
        self.assertEqual(0, xs_array_get_size(created["arr"]))

    def test_create_returns_without_allocating_string_array_when_int_array_allocation_fails(self):
        calls: dict[str, int32] = {"create_string": int32(0), "resize_string": int32(0)}

        def _create_int(*args, **kwargs):
            return int32(-1)

        def _create_string(*args, **kwargs):
            calls["create_string"] += 1
            return self.orig_create_string(*args, **kwargs)

        def _resize_string(arr_id, new_size):
            calls["resize_string"] += 1
            return int32(0)

        _sl.xs_array_create_int = _create_int
        _sl.xs_array_create_string = _create_string
        _sl.xs_array_resize_string = _resize_string

        self.assertEqual(c_string_list_generic_error, xs_string_list_create())
        self.assertEqual(0, calls["create_string"])
        self.assertEqual(0, calls["resize_string"])

    def test_constructor_shrinks_string_array_when_int_array_allocation_fails(self):
        created: dict[str, int32] = {}

        def _create_int(*args, **kwargs):
            return int32(-1)

        def _create_string(*args, **kwargs):
            arr = self.orig_create_string(*args, **kwargs)
            created["arr"] = arr
            return arr

        def _resize_string(arr_id, new_size):
            self.orig_resize_string(arr_id, new_size)
            return int32(0)

        _sl.xs_array_create_int = _create_int
        _sl.xs_array_create_string = _create_string
        _sl.xs_array_resize_string = _resize_string

        self.assertEqual(c_string_list_generic_error, xs_string_list("aa"))
        self.assertEqual(0, xs_array_get_size(created["arr"]))

    def test_copy_shrinks_int_array_when_string_array_allocation_fails(self):
        created: dict[str, int32] = {}
        xs_lst = xs_string_list("aa", "bb")

        def _create_int(*args, **kwargs):
            arr = self.orig_create_int(*args, **kwargs)
            created["arr"] = arr
            return arr

        def _create_string(*args, **kwargs):
            return int32(-1)

        def _resize_int(arr_id, new_size):
            self.orig_resize_int(arr_id, new_size)
            return int32(0)

        _sl.xs_array_create_int = _create_int
        _sl.xs_array_create_string = _create_string
        _sl.xs_array_resize_int = _resize_int

        self.assertEqual(c_string_list_generic_error, xs_string_list_copy(xs_lst))
        self.assertEqual(0, xs_array_get_size(created["arr"]))

    def test_from_repeated_list_shrinks_string_array_when_int_array_allocation_fails(self):
        created: dict[str, int32] = {}
        xs_lst = xs_string_list("aa", "bb")

        def _create_int(*args, **kwargs):
            return int32(-1)

        def _create_string(*args, **kwargs):
            arr = self.orig_create_string(*args, **kwargs)
            created["arr"] = arr
            return arr

        def _resize_string(arr_id, new_size):
            self.orig_resize_string(arr_id, new_size)
            return int32(0)

        _sl.xs_array_create_int = _create_int
        _sl.xs_array_create_string = _create_string
        _sl.xs_array_resize_string = _resize_string

        self.assertEqual(c_string_list_generic_error, xs_string_list_from_repeated_list(xs_lst, int32(2)))
        self.assertEqual(0, xs_array_get_size(created["arr"]))


def to_str_lst(lst) -> list[str]:
    return [str(x) for x in lst]


def to_str(lst) -> str:
    r = "["
    for i, x in enumerate(lst):
        r += '"' + str(x) + '"'
        if i < len(lst) - 1:
            r += ", "
    r += "]"
    return r
