import random
import unittest
from random import randint

from xs.string_list import *
from xs_converter.functions import xs_array_create_string, xs_array_set_string, xs_array_get_string


class StringListTest(unittest.TestCase):
    def test_xs_string_list(self):
        for i in i32range(0, 13):
            params = to_str_lst(range(i))
            arr = xs_string_list(*params)
            self.assertEqual(i, xs_string_list_size(arr))
            self.assertEqual(to_str(params), xs_string_list_to_string(arr))

    def test_xs_string_list_stop_at_magic_number(self):
        arr = xs_string_list("aa", c_string_list_empty_param, "bb")
        self.assertEqual(to_str(["aa"]), xs_string_list_to_string(arr))

    def test_xs_string_list_create_empty(self):
        arr = xs_string_list_create(int32(16))
        self.assertEqual(0, xs_string_list_size(arr))

    def test_xs_string_list_create_fail_at_negative_capacity(self):
        arr = xs_string_list_create(int32(-1))
        self.assertEqual(c_string_list_generic_error, arr)

    def test_xs_string_list_create_fail_over_max_capacity(self):
        arr = xs_string_list_create(c_string_list_max_capacity)
        self.assertEqual(c_string_list_generic_error, arr)

    def test_xs_string_list_from_repeated_val(self):
        arr = xs_string_list_from_repeated_val("aa", int32(7))
        self.assertEqual(7, xs_string_list_size(arr))
        self.assertEqual('["aa", "aa", "aa", "aa", "aa", "aa", "aa"]', xs_string_list_to_string(arr))

    def test_xs_string_list_from_repeated_val_fail_with_negative_repeat(self):
        arr = xs_string_list_from_repeated_val("aa", int32(-2))
        self.assertEqual(c_string_list_generic_error, arr)

    def test_xs_string_list_from_repeated_val_fail_over_max_capacity(self):
        arr = xs_string_list_from_repeated_val("aa", c_string_list_max_capacity + 1)
        self.assertEqual(c_string_list_generic_error, arr)

    def test_xs_string_list_from_repeated_list(self):
        lst1 = ["aa", "bb", "cc", "dd"]
        lst2 = lst1 * 7
        arr1 = xs_string_list(*lst1)
        arr2 = xs_string_list_from_repeated_list(arr1, int32(7))
        self.assertEqual(to_str(lst2), xs_string_list_to_string(arr2))
        self.assertEqual(len(lst2), xs_string_list_size(arr2))

    def test_xs_string_list_from_array(self):
        arr = xs_array_create_string(10, "aaa")
        arr_lst = xs_string_list_from_array(arr)
        lst = ["aaa"] * 10
        self.assertEqual(to_str(lst), xs_string_list_to_string(arr_lst))
        self.assertEqual(xs_array_get_size(arr), xs_string_list_size(arr_lst))
        self.assertEqual(len(lst), xs_string_list_size(arr_lst))

    def test_xs_string_list_from_array_fail_over_max_capacity(self):
        arr = xs_array_create_string(c_string_list_max_capacity + 1, "aaa")
        self.assertEqual(c_string_list_max_capacity_error, xs_string_list_from_array(arr))

    def test_xs_string_list_use_array_as_source(self):
        arr = xs_array_create_string(10, "bbb")
        lst = ["bbb"] * 10
        str_lst = xs_string_list_use_array_as_source(arr)
        self.assertEqual(to_str(lst), xs_string_list_to_string(str_lst))
        self.assertEqual(len(lst), xs_string_list_size(str_lst))
        xs_array_set_string(arr, 0, "abc")
        self.assertEqual(xs_array_get_string(arr, 0), xs_string_list_get(str_lst, int32(0)))

    def test_xs_string_list_get(self):
        lst = to_str_lst(range(-1, 100))
        arr = xs_string_list_create(int32(101))
        for v in range(-1, 100):
            xs_string_list_append(arr, str(v))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            self.assertEqual(lst[i], xs_string_list_get(arr, int32(i)))
            self.assertEqual(c_string_list_success, xs_string_list_last_error())

    def test_xs_string_list_get_fail_with_incorrect_idx(self):
        arr = xs_string_list("aa", "bb", "cc", "dd")
        self.assertEqual(str(c_string_list_generic_error), xs_string_list_get(arr, int32(4)))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_last_error())
        self.assertEqual(str(c_string_list_generic_error), xs_string_list_get(arr, int32(-1)))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_last_error())

    def test_xs_string_list_set(self):
        lst = to_str_lst(range(-1, 100))
        arr = xs_string_list_create(int32(101))
        for v in range(-1, 100):
            xs_string_list_append(arr, str(v))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            v = random.random()
            self.assertEqual(c_string_list_success, xs_string_list_set(arr, int32(i), str(v)))
            lst[i] = str(v)
        self.assertEqual(to_str(lst), xs_string_list_to_string(arr))
        self.assertEqual(len(lst), xs_string_list_size(arr))

    def test_xs_string_list_set_fail_with_incorrect_idx(self):
        arr = xs_string_list("aa", "bb", "cc", "dd")
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_set(arr, int32(4), "ff"))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_set(arr, int32(-1), "ff"))

    def test_xs_string_list_append(self):
        arr = xs_string_list_create()
        lst = []
        for i in range(11, 22):
            xs_string_list_append(arr, str(i))
            lst.append(str(i))
        self.assertEqual(len(lst), xs_string_list_size(arr))
        self.assertEqual(to_str(lst), xs_string_list_to_string(arr))

    def test_xs_string_list_append_fail_over_max_capacity(self):
        arr = xs_string_list_from_repeated_val("aaa", c_string_list_max_capacity)
        self.assertEqual(c_string_list_max_capacity_error, xs_string_list_append(arr, "bbb"))

    def test_xs_string_list_insert(self):
        lst = ["aa", "bb", "cc", "dd", "ee", "ff"]
        arr = xs_string_list(*lst)
        for v in range(0, 100):
            i = randint(0, len(lst))
            lst.insert(i, str(v))
            self.assertEqual(c_string_list_success, xs_string_list_insert(arr, int32(i), str(v)))
        self.assertEqual(to_str(lst), xs_string_list_to_string(arr))
        self.assertEqual(len(lst), xs_string_list_size(arr))

    def test_xs_string_list_insert_fail_with_incorrect_idx(self):
        arr = xs_string_list("aa", "bb", "cc")
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_insert(arr, int32(-1), "dd"))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_insert(arr, int32(4), "ee"))

    def test_xs_string_list_insert_fail_over_max_capacity(self):
        arr = xs_string_list_from_repeated_val("aa", c_string_list_max_capacity)
        self.assertEqual(c_string_list_max_capacity_error, xs_string_list_insert(arr, int32(100), "bb"))

    def test_xs_string_list_pop(self):
        lst = ["aa", "bb", "cc", "dd", "ee", "ff"]
        arr = xs_string_list(*lst)
        for _ in range(len(lst)):
            self.assertEqual(lst.pop(), xs_string_list_pop(arr))
            self.assertEqual(c_string_list_success, xs_string_list_last_error())
        self.assertEqual(len(lst), xs_string_list_size(arr))
        self.assertEqual(str(lst), xs_string_list_to_string(arr))

    def test_xs_string_list_pop_at_index(self):
        arr = xs_string_list_create(int32(201))
        for v in range(-1, 200):
            xs_string_list_append(arr, str(v))
        lst = list(range(-1, 200))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            self.assertEqual(str(lst[i]), xs_string_list_pop(arr, int32(i)))
            lst.pop(i)
            self.assertEqual(c_string_list_success, xs_string_list_last_error())
        self.assertEqual(to_str(lst), xs_string_list_to_string(arr))
        self.assertEqual(len(lst), xs_string_list_size(arr))

    def test_xs_string_list_pop_at_max(self):
        arr = xs_string_list_from_repeated_val("aa", c_string_list_max_capacity)
        self.assertEqual("aa", xs_string_list_pop(arr, c_string_list_max_capacity))
        self.assertEqual(c_string_list_max_capacity - 1, xs_string_list_size(arr))

    def test_xs_string_list_pop_fail_with_incorrect_idx(self):
        arr = xs_string_list("aa", "bb", "cc", "dd")
        self.assertEqual(str(c_string_list_generic_error), xs_string_list_pop(arr, int32(4)))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_last_error())
        self.assertEqual(str(c_string_list_generic_error), xs_string_list_pop(arr, int32(-1)))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_last_error())

    def test_xs_string_list_remove(self):
        arr = xs_string_list_create(int32(201))
        for v in range(-1, 200):
            xs_string_list_append(arr, str(v))
        lst = to_str_lst(range(-1, 200, 1))
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            val = lst[i]
            self.assertEqual(i, xs_string_list_remove(arr, val))
            lst.remove(val)

        self.assertEqual(to_str(lst), xs_string_list_to_string(arr))
        self.assertEqual(len(lst), xs_string_list_size(arr))

    def test_xs_string_list_remove_fail_with_incorrect_idx(self):
        arr = xs_string_list("aa", "bb", "cc", "dd")
        self.assertEqual(c_string_list_generic_error, xs_string_list_remove(arr, "ff"))

    def test_xs_string_list_index(self):
        arr = xs_string_list_create(int32(201))
        for v in range(-1, 200):
            xs_string_list_append(arr, str(v))
        lst = to_str_lst(range(-1, 200))
        for _ in range(100):
            val = lst[randint(0, len(lst) - 1)]
            self.assertEqual(lst.index(val), xs_string_list_index(arr, val))

    def test_xs_string_list_index_with_ranges(self):
        arr = xs_string_list()
        lst = []
        for _ in range(500):
            val = str(random.randint(-100, 100))
            xs_string_list_append(arr, val)
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
                    r = c_string_list_generic_error
                self.assertEqual(r, xs_string_list_index(*params_xs))

    def test_xs_string_list_index_fail_with_incorrect_idx(self):
        arr = xs_string_list("aa", "bb", "cc")
        self.assertEqual(c_string_list_generic_error, xs_string_list_index(arr, "dd"))

    def test_xs_string_list_contains(self):
        arr = xs_string_list("aa", "bb")
        self.assertTrue(xs_string_list_contains(arr, "aa"))
        self.assertTrue(xs_string_list_contains(arr, "bb"))
        self.assertFalse(xs_string_list_contains(arr, "cc"))

    def test_xs_string_list_sort(self):
        for _ in range(100):
            size = randint(0, 100)
            arr = xs_string_list_create(int32(0))
            lst = []
            for _ in range(size):
                val = str(random.randint(-100, 100))
                xs_string_list_append(arr, val)
                lst.append(val)
            lst.sort()
            xs_string_list_sort(arr)
            self.assertEqual(to_str(lst), xs_string_list_to_string(arr))
            self.assertEqual(len(lst), xs_string_list_size(arr))

    def test_xs_string_list_sort_reverse(self):
        for _ in range(100):
            size = randint(0, 100)
            arr = xs_string_list_create(int32(size))
            lst = []
            for _ in range(size):
                val = str(random.randint(-100, 100))
                xs_string_list_append(arr, val)
                lst.append(val)
            lst.sort(reverse=True)
            xs_string_list_sort(arr, True)
            self.assertEqual(to_str(lst), xs_string_list_to_string(arr))
            self.assertEqual(len(lst), xs_string_list_size(arr))

    def test_xs_string_list_to_string_test(self):
        arr = xs_string_list("aa", "bb", "cc", "dd", "ee")
        self.assertEqual('["aa", "bb", "cc", "dd", "ee"]', xs_string_list_to_string(arr))
        arr_empty = xs_string_list()
        self.assertEqual("[]", xs_string_list_to_string(arr_empty))

    def test_xs_string_list_reverse_even(self):
        lst = ["aa", "bb", "cc", "dd", "ee", "ff"]
        arr = xs_string_list(*lst)

        xs_string_list_reverse(arr)
        lst.reverse()

        self.assertEqual(to_str(lst), xs_string_list_to_string(arr))
        self.assertEqual(len(lst), xs_string_list_size(arr))

    def test_xs_string_list_reverse_odd(self):
        lst = ["aa", "bb", "cc", "dd", "ee", "ff", "gg"]
        arr = xs_string_list(*lst)

        xs_string_list_reverse(arr)
        lst.reverse()

        self.assertEqual(to_str(lst), xs_string_list_to_string(arr))
        self.assertEqual(len(lst), xs_string_list_size(arr))

    def test_xs_string_list_reverse_empty(self):
        lst = []
        arr = xs_string_list(*lst)

        xs_string_list_reverse(arr)
        lst.reverse()

        self.assertEqual(to_str(lst), xs_string_list_to_string(arr))
        self.assertEqual(len(lst), xs_string_list_size(arr))

    def test_xs_string_list_copy(self):
        lst = ["aa", "bb", "cc", "dd", "ee", "ff"]
        arr = xs_string_list(*lst)
        copy = xs_string_list_copy(arr)
        self.assertEqual(xs_string_list_to_string(arr), xs_string_list_to_string(copy))
        self.assertEqual(xs_string_list_size(arr), xs_string_list_size(copy))

        xs_string_list_set(arr, int32(0), "zz")
        self.assertEqual(to_str(lst), xs_string_list_to_string(copy))
        self.assertEqual(len(lst), xs_string_list_size(copy))

    def test_xs_string_list_copy_slices(self):
        lst = ["aa", "bb", "cc", "dd", "ee", "ff"]
        arr = xs_string_list(*lst)

        for i in i32range(len(lst) * -1, len(lst) + 1):
            for j in i32range(len(lst) * -1, len(lst) + 1):
                copy_arr = xs_string_list_copy(arr, i, j)
                copy_lst = lst[i:j]
                self.assertEqual(to_str(copy_lst), xs_string_list_to_string(copy_arr))
                self.assertEqual(len(copy_lst), xs_string_list_size(copy_arr))

    def test_xs_string_list_extend(self):
        lst1 = ["aa", "bb", "cc", "dd", "ee", "ff"]
        lst2 = ["aa", "bb", "cc", "dd", "ee", "ff", "gg", "hh", "ii", "jj"]

        arr1 = xs_string_list(*lst1)
        arr2 = xs_string_list(*lst2)
        self.assertEqual(c_string_list_success, xs_string_list_extend(arr1, arr2))
        lst1.extend(lst2)

        self.assertEqual(to_str(lst1), xs_string_list_to_string(arr1))
        self.assertEqual(len(lst1), xs_string_list_size(arr1))

    def test_xs_string_list_extend_with_array(self):
        lst1 = ["aa", "bb", "cc", "dd", "ee", "ff"]
        lst2 = ["zz"] * 10

        arr1 = xs_string_list(*lst1)
        arr2 = xs_array_create_string(10, "zz")
        self.assertEqual(c_string_list_success, xs_string_list_extend_with_array(arr1, arr2))
        lst1.extend(lst2)

        self.assertEqual(to_str(lst1), xs_string_list_to_string(arr1))
        self.assertEqual(len(lst1), xs_string_list_size(arr1))

    def test_xs_string_list_clear(self):
        arr = xs_string_list("aa", "bb", "cc", "dd", "ee", "ff")

        self.assertEqual(c_string_list_success, xs_string_list_clear(arr))
        self.assertEqual("[]", xs_string_list_to_string(arr))
        self.assertEqual(0, xs_string_list_size(arr))

    def test_xs_string_list_compare(self):
        arr1 = xs_string_list("aa", "bb", "dd")
        arr2 = xs_string_list("aa", "bb", "cc")

        self.assertEqual(1, xs_string_list_compare(arr1, arr2))
        self.assertEqual(-1, xs_string_list_compare(arr2, arr1))
        self.assertEqual(0, xs_string_list_compare(arr1, arr1))

    def test_xs_string_list_compare_same_prefix(self):
        arr1 = xs_string_list("aa", "bb", "cc")
        arr2 = xs_string_list("aa", "bb", "cc", "dd")

        self.assertEqual(-1, xs_string_list_compare(arr1, arr2))
        self.assertEqual(1, xs_string_list_compare(arr2, arr1))

    def test_xs_string_list_compare_empty(self):
        arr1 = xs_string_list()
        arr2 = xs_string_list()

        self.assertEqual(0, xs_string_list_compare(arr1, arr2))

    def test_xs_string_list_count_min_max(self):
        arr = xs_string_list()
        lst = []
        for _ in range(100):
            v = str(random.randint(-100, 100))
            xs_string_list_append(arr, v)
            lst.append(v)

        self.assertEqual(lst.count(lst[0]), xs_string_list_count(arr, lst[0]))
        self.assertEqual(min(lst), xs_string_list_min(arr))
        self.assertEqual(max(lst), xs_string_list_max(arr))

    def test_xs_string_list_count_min_max_on_empty(self):
        arr = xs_string_list()
        lst = []

        self.assertEqual(lst.count(float32(1.0)), xs_string_list_count(arr, float32(1.0)))
        self.assertEqual(str(c_string_list_generic_error), xs_string_list_min(arr))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_last_error())
        self.assertEqual(str(c_string_list_generic_error), xs_string_list_max(arr))
        self.assertEqual(c_string_list_index_out_of_range_error, xs_string_list_last_error())


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
