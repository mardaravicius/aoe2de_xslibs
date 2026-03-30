import unittest
from random import randint

import xs.bool_list as _bl
from xs.bool_list import *
from xs_converter.functions import xs_array_get_size, xs_array_get_int
from xs_converter.impl import xs_functions_impl as _impl


def _create_bool_array_impl(size: int | int32, default_value: bool = False, unique_name: str = "") -> int32:
    size = int(size)
    if size < 0:
        return int32(-1)
    if unique_name != "" and unique_name in _impl.ARRAY_NAMES:
        return int32(-1)
    _impl.ARRAYS.append(_impl.XsArray(bool, [bool(default_value)] * size))
    if unique_name != "":
        _impl.ARRAY_NAMES.add(unique_name)
    return int32(len(_impl.ARRAYS) - 1)


def _set_bool_array_impl(array_id: int | int32, index: int | int32, value: bool) -> bool:
    array_id = int(array_id)
    index = int(index)
    if array_id < 0 or array_id >= len(_impl.ARRAYS):
        return False
    xs_array = _impl.ARRAYS[array_id]
    if xs_array.arr_type != bool or index < 0 or index >= len(xs_array.array):
        return False
    xs_array.array[index] = bool(value)
    return True


def _get_bool_array_impl(array_id: int | int32, index: int | int32) -> bool:
    array_id = int(array_id)
    index = int(index)
    if array_id < 0 or array_id >= len(_impl.ARRAYS):
        return False
    xs_array = _impl.ARRAYS[array_id]
    if xs_array.arr_type != bool or index < 0 or index >= len(xs_array.array):
        return False
    return bool(xs_array.array[index])


def _resize_bool_array_impl(array_id: int | int32, new_size: int | int32) -> bool:
    array_id = int(array_id)
    new_size = int(new_size)
    if array_id < 0 or array_id >= len(_impl.ARRAYS) or new_size < 0:
        return False
    xs_array = _impl.ARRAYS[array_id]
    if xs_array.arr_type != bool:
        return False
    size = len(xs_array.array)
    if new_size > size:
        xs_array.array.extend([False] * (new_size - size))
    else:
        del xs_array.array[new_size:size]
    return True


class BoolListTest(unittest.TestCase):
    def setUp(self):
        _impl.ARRAYS.clear()
        _impl.ARRAY_NAMES.clear()
        self.orig_create_int = _bl.xs_array_create_int
        self.orig_create_bool = _bl.xs_array_create_bool
        self.orig_set_bool = _bl.xs_array_set_bool
        self.orig_get_bool = _bl.xs_array_get_bool
        self.orig_resize_int = _bl.xs_array_resize_int
        self.orig_resize_bool = _bl.xs_array_resize_bool
        _bl.xs_array_create_bool = _create_bool_array_impl
        _bl.xs_array_set_bool = _set_bool_array_impl
        _bl.xs_array_get_bool = _get_bool_array_impl
        _bl.xs_array_resize_bool = _resize_bool_array_impl

    def tearDown(self):
        _bl.xs_array_create_int = self.orig_create_int
        _bl.xs_array_create_bool = self.orig_create_bool
        _bl.xs_array_set_bool = self.orig_set_bool
        _bl.xs_array_get_bool = self.orig_get_bool
        _bl.xs_array_resize_int = self.orig_resize_int
        _bl.xs_array_resize_bool = self.orig_resize_bool

    def _create_bool_array(self, values: list[bool]) -> int32:
        arr = _create_bool_array_impl(len(values))
        for i, value in enumerate(values):
            _set_bool_array_impl(arr, i, value)
        return arr

    def _create_bool_list(self, values: list[bool], capacity: int | None = None) -> int32:
        if capacity is None:
            capacity = len(values)
        xs_lst = xs_bool_list_create(int32(capacity))
        for value in values:
            xs_bool_list_append(xs_lst, value)
        return xs_lst

    def test_xs_bool_list_create_and_append(self):
        for i in i32range(0, 13):
            values = [bool(j % 2) for j in range(i)]
            xs_lst = self._create_bool_list(values)
            self.assertEqual(i, xs_bool_list_size(xs_lst))
            self.assertEqual(bstr(values), xs_bool_list_to_string(xs_lst))

    def test_xs_bool_list_create_empty(self):
        xs_lst = xs_bool_list_create(int32(16))
        self.assertEqual(0, xs_bool_list_size(xs_lst))

    def test_xs_bool_list_create_fail_at_negative_capacity(self):
        xs_lst = xs_bool_list_create(int32(-1))
        self.assertEqual(c_bool_list_generic_error, xs_lst)

    def test_xs_bool_list_create_fail_over_max_capacity(self):
        xs_lst = xs_bool_list_create(c_bool_list_max_capacity)
        self.assertEqual(c_bool_list_generic_error, xs_lst)

    def test_xs_bool_list_from_repeated_val(self):
        xs_lst = xs_bool_list_from_repeated_val(True, int32(7))
        self.assertEqual(7, xs_bool_list_size(xs_lst))
        self.assertEqual("[true, true, true, true, true, true, true]", xs_bool_list_to_string(xs_lst))

    def test_xs_bool_list_from_repeated_val_fail_with_negative_repeat(self):
        xs_lst = xs_bool_list_from_repeated_val(True, int32(-2))
        self.assertEqual(c_bool_list_generic_error, xs_lst)

    def test_xs_bool_list_from_repeated_val_fail_over_max_capacity(self):
        xs_lst = xs_bool_list_from_repeated_val(True, c_bool_list_max_capacity + 1)
        self.assertEqual(c_bool_list_generic_error, xs_lst)

    def test_xs_bool_list_from_repeated_list(self):
        lst1 = [True, False, True, False]
        lst2 = lst1 * 7
        xs_lst1 = self._create_bool_list(lst1)
        xs_lst2 = xs_bool_list_from_repeated_list(xs_lst1, int32(7))
        self.assertEqual(bstr(lst2), xs_bool_list_to_string(xs_lst2))
        self.assertEqual(len(lst2), xs_bool_list_size(xs_lst2))

    def test_xs_bool_list_from_repeated_list_negative_times(self):
        xs_lst = self._create_bool_list([True, False, True])
        result = xs_bool_list_from_repeated_list(xs_lst, int32(-1))
        self.assertEqual(c_bool_list_generic_error, result)

    def test_xs_bool_list_from_repeated_list_zero_times(self):
        xs_lst = self._create_bool_list([True, False, True])
        result = xs_bool_list_from_repeated_list(xs_lst, int32(0))
        self.assertGreaterEqual(result, 0)
        self.assertEqual(0, xs_bool_list_size(result))

    def test_xs_bool_list_from_repeated_list_overflow(self):
        xs_lst = self._create_bool_list([True, False, True])
        result = xs_bool_list_from_repeated_list(xs_lst, c_bool_list_max_capacity)
        self.assertEqual(c_bool_list_max_capacity_error, result)

    def test_xs_bool_list_from_array(self):
        xs_arr = self._create_bool_array([True] * 10)
        xs_lst = xs_bool_list_from_array(xs_arr)
        lst = [True] * 10
        self.assertEqual(bstr(lst), xs_bool_list_to_string(xs_lst))
        self.assertEqual(xs_array_get_size(xs_arr), xs_bool_list_size(xs_lst))
        self.assertEqual(len(lst), xs_bool_list_size(xs_lst))

    def test_xs_bool_list_from_array_fail_over_max_capacity(self):
        orig = _bl.c_bool_list_max_capacity
        _bl.c_bool_list_max_capacity = int32(1000)
        xs_arr = _create_bool_array_impl(_bl.c_bool_list_max_capacity + 1, True)
        self.assertEqual(c_bool_list_max_capacity_error, xs_bool_list_from_array(xs_arr))
        _bl.c_bool_list_max_capacity = orig

    def test_xs_bool_list_use_array_as_source(self):
        xs_arr = self._create_bool_array([False] * 10)
        lst = [False] * 10
        xs_lst = xs_bool_list_use_array_as_source(xs_arr)
        self.assertEqual(bstr(lst), xs_bool_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_bool_list_size(xs_lst))
        _set_bool_array_impl(xs_arr, 0, True)
        self.assertEqual(_get_bool_array_impl(xs_arr, 0), xs_bool_list_get(xs_lst, int32(0)))

    def test_xs_bool_list_get(self):
        lst = [bool(i % 2) for i in range(101)]
        xs_lst = xs_bool_list_create(int32(101))
        for value in lst:
            xs_bool_list_append(xs_lst, value)
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            self.assertEqual(lst[i], xs_bool_list_get(xs_lst, int32(i)))
            self.assertEqual(c_bool_list_success, xs_bool_list_last_error())

    def test_xs_bool_list_get_fail_with_incorrect_idx(self):
        xs_lst = self._create_bool_list([True, False, True, False])
        self.assertFalse(xs_bool_list_get(xs_lst, int32(4)))
        self.assertEqual(c_bool_list_index_out_of_range_error, xs_bool_list_last_error())
        self.assertFalse(xs_bool_list_get(xs_lst, int32(-1)))
        self.assertEqual(c_bool_list_index_out_of_range_error, xs_bool_list_last_error())

    def test_xs_bool_list_set(self):
        lst = [bool(i % 2) for i in range(101)]
        xs_lst = xs_bool_list_create(int32(101))
        for value in lst:
            xs_bool_list_append(xs_lst, value)
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            value = bool(randint(0, 1))
            self.assertEqual(c_bool_list_success, xs_bool_list_set(xs_lst, int32(i), value))
            lst[i] = value
        self.assertEqual(bstr(lst), xs_bool_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_bool_list_size(xs_lst))

    def test_xs_bool_list_set_fail_with_incorrect_idx(self):
        xs_lst = self._create_bool_list([True, False, True, False])
        self.assertEqual(c_bool_list_index_out_of_range_error, xs_bool_list_set(xs_lst, int32(4), True))
        self.assertEqual(c_bool_list_index_out_of_range_error, xs_bool_list_set(xs_lst, int32(-1), True))

    def test_xs_bool_list_append(self):
        xs_lst = xs_bool_list_create()
        lst = []
        for i in range(11, 22):
            value = bool(i % 2)
            xs_bool_list_append(xs_lst, value)
            lst.append(value)
        self.assertEqual(len(lst), xs_bool_list_size(xs_lst))
        self.assertEqual(bstr(lst), xs_bool_list_to_string(xs_lst))

    def test_xs_bool_list_append_fail_over_max_capacity(self):
        orig = _bl.c_bool_list_max_capacity
        _bl.c_bool_list_max_capacity = int32(1000)
        xs_lst = xs_bool_list_from_repeated_val(True, _bl.c_bool_list_max_capacity)
        self.assertEqual(c_bool_list_max_capacity_error, xs_bool_list_append(xs_lst, False))
        _bl.c_bool_list_max_capacity = orig

    def test_xs_bool_list_insert(self):
        lst = [True, False, True, False, True, False]
        xs_lst = self._create_bool_list(lst)
        for i in range(100):
            idx = randint(0, len(lst))
            value = bool(i % 2)
            lst.insert(idx, value)
            self.assertEqual(c_bool_list_success, xs_bool_list_insert(xs_lst, int32(idx), value))
        self.assertEqual(bstr(lst), xs_bool_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_bool_list_size(xs_lst))

    def test_xs_bool_list_insert_fail_with_incorrect_idx(self):
        xs_lst = self._create_bool_list([True, False, True])
        self.assertEqual(c_bool_list_index_out_of_range_error, xs_bool_list_insert(xs_lst, int32(-1), False))
        self.assertEqual(c_bool_list_index_out_of_range_error, xs_bool_list_insert(xs_lst, int32(4), False))

    def test_xs_bool_list_insert_fail_over_max_capacity(self):
        orig = _bl.c_bool_list_max_capacity
        _bl.c_bool_list_max_capacity = int32(1000)
        xs_lst = xs_bool_list_from_repeated_val(True, _bl.c_bool_list_max_capacity)
        self.assertEqual(c_bool_list_max_capacity_error, xs_bool_list_insert(xs_lst, int32(100), False))
        _bl.c_bool_list_max_capacity = orig

    def test_xs_bool_list_pop(self):
        lst = [True, False, True, False, True, False]
        xs_lst = self._create_bool_list(lst)
        for _ in range(len(lst)):
            self.assertEqual(lst.pop(), xs_bool_list_pop(xs_lst))
            self.assertEqual(c_bool_list_success, xs_bool_list_last_error())
        self.assertEqual(len(lst), xs_bool_list_size(xs_lst))
        self.assertEqual("[]", xs_bool_list_to_string(xs_lst))

    def test_xs_bool_list_pop_at_index(self):
        xs_lst = xs_bool_list_create(int32(201))
        lst = []
        for i in range(201):
            value = bool(i % 2)
            xs_bool_list_append(xs_lst, value)
            lst.append(value)
        for _ in range(100):
            i = randint(0, len(lst) - 1)
            self.assertEqual(lst[i], xs_bool_list_pop(xs_lst, int32(i)))
            lst.pop(i)
            self.assertEqual(c_bool_list_success, xs_bool_list_last_error())
        self.assertEqual(bstr(lst), xs_bool_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_bool_list_size(xs_lst))

    def test_xs_bool_list_pop_at_max(self):
        orig = _bl.c_bool_list_max_capacity
        _bl.c_bool_list_max_capacity = int32(1000)
        xs_lst = xs_bool_list_from_repeated_val(True, _bl.c_bool_list_max_capacity)
        self.assertTrue(xs_bool_list_pop(xs_lst, _bl.c_bool_list_max_capacity))
        self.assertEqual(_bl.c_bool_list_max_capacity - 1, xs_bool_list_size(xs_lst))
        _bl.c_bool_list_max_capacity = orig

    def test_xs_bool_list_pop_fail_with_incorrect_idx(self):
        xs_lst = self._create_bool_list([True, False, True, False])
        self.assertFalse(xs_bool_list_pop(xs_lst, int32(4)))
        self.assertEqual(c_bool_list_index_out_of_range_error, xs_bool_list_last_error())
        self.assertFalse(xs_bool_list_pop(xs_lst, int32(-1)))
        self.assertEqual(c_bool_list_index_out_of_range_error, xs_bool_list_last_error())

    def test_xs_bool_list_pop_empty_list(self):
        xs_lst = xs_bool_list_create()
        self.assertEqual(0, xs_bool_list_size(xs_lst))
        self.assertFalse(xs_bool_list_pop(xs_lst))
        self.assertEqual(c_bool_list_index_out_of_range_error, xs_bool_list_last_error())

    def test_xs_bool_list_shrink_after_pop_then_append(self):
        xs_lst = xs_bool_list_create(int32(0))
        for i in range(50):
            xs_bool_list_append(xs_lst, bool(i % 2))
        for _ in range(40):
            xs_bool_list_pop(xs_lst)
        remaining = [bool(i % 2) for i in range(10)]
        self.assertEqual(bstr(remaining), xs_bool_list_to_string(xs_lst))
        self.assertEqual(10, xs_bool_list_size(xs_lst))
        xs_bool_list_append(xs_lst, True)
        remaining.append(True)
        self.assertEqual(bstr(remaining), xs_bool_list_to_string(xs_lst))
        self.assertEqual(11, xs_bool_list_size(xs_lst))

    def test_xs_bool_list_remove(self):
        xs_lst = self._create_bool_list([False, True, False, True, False, True])
        self.assertEqual(0, xs_bool_list_remove(xs_lst, False))
        self.assertEqual("[true, false, true, false, true]", xs_bool_list_to_string(xs_lst))
        self.assertEqual(1, xs_bool_list_remove(xs_lst, False))
        self.assertEqual("[true, true, false, true]", xs_bool_list_to_string(xs_lst))

    def test_xs_bool_list_remove_fail_when_value_missing(self):
        xs_lst = self._create_bool_list([True, True, True, True])
        self.assertEqual(c_bool_list_generic_error, xs_bool_list_remove(xs_lst, False))

    def test_xs_bool_list_index(self):
        xs_lst = xs_bool_list_create(int32(201))
        lst = []
        for _ in range(201):
            value = bool(randint(0, 1))
            xs_bool_list_append(xs_lst, value)
            lst.append(value)
        for _ in range(100):
            value = bool(randint(0, 1))
            if value in lst:
                self.assertEqual(lst.index(value), xs_bool_list_index(xs_lst, value))
            else:
                self.assertEqual(c_bool_list_generic_error, xs_bool_list_index(xs_lst, value))

    def test_xs_bool_list_index_with_ranges(self):
        xs_lst = xs_bool_list_create()
        lst = []
        for _ in range(500):
            value = bool(randint(0, 1))
            xs_bool_list_append(xs_lst, value)
            lst.append(value)
        test_data = [
            (0, 0),
            (0, 1),
            (0, 10),
            (10, 0),
            (-4, 4),
            (5, -5),
            (-17, -13),
            (-8, -22),
        ]
        for _ in range(100):
            for data in test_data:
                value = bool(randint(0, 1))
                params_xs = (xs_lst, value) + data
                params = (value,) + data
                try:
                    r = lst.index(params[0], params[1], params[2])
                except ValueError:
                    r = c_bool_list_generic_error
                self.assertEqual(r, xs_bool_list_index(*params_xs))

    def test_xs_bool_list_index_fail_when_missing(self):
        xs_lst = self._create_bool_list([True, True, True])
        self.assertEqual(c_bool_list_generic_error, xs_bool_list_index(xs_lst, False))

    def test_xs_bool_list_contains(self):
        xs_lst = self._create_bool_list([True, False])
        self.assertTrue(xs_bool_list_contains(xs_lst, True))
        self.assertTrue(xs_bool_list_contains(xs_lst, False))

    def test_xs_bool_list_sort(self):
        for _ in range(100):
            size = randint(0, 100)
            xs_lst = xs_bool_list_create(int32(0))
            lst = []
            for _ in range(size):
                value = bool(randint(0, 1))
                xs_bool_list_append(xs_lst, value)
                lst.append(value)
            lst.sort()
            xs_bool_list_sort(xs_lst)
            self.assertEqual(bstr(lst), xs_bool_list_to_string(xs_lst))
            self.assertEqual(len(lst), xs_bool_list_size(xs_lst))

    def test_xs_bool_list_sort_reverse(self):
        for _ in range(100):
            size = randint(0, 100)
            xs_lst = xs_bool_list_create(int32(size))
            lst = []
            for _ in range(size):
                value = bool(randint(0, 1))
                xs_bool_list_append(xs_lst, value)
                lst.append(value)
            lst.sort(reverse=True)
            xs_bool_list_sort(xs_lst, True)
            self.assertEqual(bstr(lst), xs_bool_list_to_string(xs_lst))
            self.assertEqual(len(lst), xs_bool_list_size(xs_lst))

    def test_xs_bool_list_to_string_test(self):
        xs_lst = self._create_bool_list([True, False, True, False, True])
        self.assertEqual("[true, false, true, false, true]", xs_bool_list_to_string(xs_lst))
        xs_lst_empty = xs_bool_list_create()
        self.assertEqual("[]", xs_bool_list_to_string(xs_lst_empty))

    def test_xs_bool_list_reverse_even(self):
        lst = [True, False, True, False, True, False]
        xs_lst = self._create_bool_list(lst)
        xs_bool_list_reverse(xs_lst)
        lst.reverse()
        self.assertEqual(bstr(lst), xs_bool_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_bool_list_size(xs_lst))

    def test_xs_bool_list_reverse_odd(self):
        lst = [True, False, True, False, True, False, True]
        xs_lst = self._create_bool_list(lst)
        xs_bool_list_reverse(xs_lst)
        lst.reverse()
        self.assertEqual(bstr(lst), xs_bool_list_to_string(xs_lst))
        self.assertEqual(len(lst), xs_bool_list_size(xs_lst))

    def test_xs_bool_list_reverse_empty(self):
        xs_lst = xs_bool_list_create()
        xs_bool_list_reverse(xs_lst)
        self.assertEqual("[]", xs_bool_list_to_string(xs_lst))
        self.assertEqual(0, xs_bool_list_size(xs_lst))

    def test_xs_bool_list_copy(self):
        lst = [True, False, True, False, True, False]
        xs_lst = self._create_bool_list(lst)
        xs_copy = xs_bool_list_copy(xs_lst)
        self.assertEqual(xs_bool_list_to_string(xs_lst), xs_bool_list_to_string(xs_copy))
        self.assertEqual(xs_bool_list_size(xs_lst), xs_bool_list_size(xs_copy))
        xs_bool_list_set(xs_lst, int32(0), False)
        self.assertEqual(bstr(lst), xs_bool_list_to_string(xs_copy))
        self.assertEqual(len(lst), xs_bool_list_size(xs_copy))

    def test_xs_bool_list_copy_slices(self):
        lst = [True, False, True, False, True, False]
        xs_lst = self._create_bool_list(lst)
        for i in i32range(len(lst) * -1, len(lst) + 1):
            for j in i32range(len(lst) * -1, len(lst) + 1):
                xs_copy = xs_bool_list_copy(xs_lst, i, j)
                copy_lst = lst[i:j]
                self.assertEqual(bstr(copy_lst), xs_bool_list_to_string(xs_copy))
                self.assertEqual(len(copy_lst), xs_bool_list_size(xs_copy))

    def test_xs_bool_list_extend(self):
        lst1 = [True, False, True, False]
        lst2 = [False, False, True, True, False]
        xs_lst1 = self._create_bool_list(lst1)
        xs_lst2 = self._create_bool_list(lst2)
        self.assertEqual(c_bool_list_success, xs_bool_list_extend(xs_lst1, xs_lst2))
        lst1.extend(lst2)
        self.assertEqual(bstr(lst1), xs_bool_list_to_string(xs_lst1))
        self.assertEqual(len(lst1), xs_bool_list_size(xs_lst1))

    def test_xs_bool_list_extend_with_array(self):
        lst1 = [True, False, True, False]
        bool_arr_values = [False] * 10
        xs_lst = self._create_bool_list(lst1)
        bool_arr = self._create_bool_array(bool_arr_values)
        self.assertEqual(c_bool_list_success, xs_bool_list_extend_with_array(xs_lst, bool_arr))
        lst1.extend(bool_arr_values)
        self.assertEqual(bstr(lst1), xs_bool_list_to_string(xs_lst))
        self.assertEqual(len(lst1), xs_bool_list_size(xs_lst))

    def test_xs_bool_list_extend_with_array_copies_raw_array_values_in_order(self):
        lst1 = [True, True]
        bool_arr_values = [False, True, False]
        xs_lst = self._create_bool_list(lst1)
        bool_arr = self._create_bool_array(bool_arr_values)
        self.assertEqual(c_bool_list_success, xs_bool_list_extend_with_array(xs_lst, bool_arr))
        lst1.extend(bool_arr_values)
        self.assertEqual(bstr(lst1), xs_bool_list_to_string(xs_lst))
        self.assertEqual(len(lst1), xs_bool_list_size(xs_lst))

    def test_xs_bool_list_clear(self):
        xs_lst = self._create_bool_list([True, False, True, False, True, False])
        self.assertEqual(c_bool_list_success, xs_bool_list_clear(xs_lst))
        self.assertEqual("[]", xs_bool_list_to_string(xs_lst))
        self.assertEqual(0, xs_bool_list_size(xs_lst))

    def test_xs_bool_list_clear_shrinks_large_capacity(self):
        xs_lst = xs_bool_list_create(int32(100))
        xs_bool_list_append(xs_lst, True)
        xs_bool_list_append(xs_lst, False)
        xs_bool_list_append(xs_lst, True)
        self.assertEqual(3, xs_bool_list_size(xs_lst))
        bool_lst = xs_array_get_int(xs_lst, 1)
        capacity_before = xs_array_get_size(bool_lst)
        self.assertGreater(capacity_before, 8)
        self.assertEqual(c_bool_list_success, xs_bool_list_clear(xs_lst))
        self.assertEqual(0, xs_bool_list_size(xs_lst))
        bool_lst = xs_array_get_int(xs_lst, 1)
        capacity_after = xs_array_get_size(bool_lst)
        self.assertLessEqual(capacity_after, 8)

    def test_xs_bool_list_compare(self):
        xs_lst1 = self._create_bool_list([True, True, False])
        xs_lst2 = self._create_bool_list([True, False, True])
        self.assertEqual(1, xs_bool_list_compare(xs_lst1, xs_lst2))
        self.assertEqual(-1, xs_bool_list_compare(xs_lst2, xs_lst1))
        self.assertEqual(0, xs_bool_list_compare(xs_lst1, xs_lst1))

    def test_xs_bool_list_compare_same_prefix(self):
        xs_lst1 = self._create_bool_list([True, False, True])
        xs_lst2 = self._create_bool_list([True, False, True, False])
        self.assertEqual(-1, xs_bool_list_compare(xs_lst1, xs_lst2))
        self.assertEqual(1, xs_bool_list_compare(xs_lst2, xs_lst1))

    def test_xs_bool_list_compare_empty(self):
        xs_lst1 = xs_bool_list_create()
        xs_lst2 = xs_bool_list_create()
        self.assertEqual(0, xs_bool_list_compare(xs_lst1, xs_lst2))

    def test_xs_bool_list_count(self):
        xs_lst = xs_bool_list_create()
        lst = []
        for _ in range(100):
            value = bool(randint(0, 1))
            xs_bool_list_append(xs_lst, value)
            lst.append(value)
        self.assertEqual(lst.count(lst[0]), xs_bool_list_count(xs_lst, lst[0]))

    def test_xs_bool_list_count_on_empty(self):
        xs_lst = xs_bool_list_create()
        self.assertEqual(0, xs_bool_list_count(xs_lst, True))

    def test_create_shrinks_int_array_when_bool_array_allocation_fails(self):
        created: dict[str, int32] = {}

        def _create_int(*args, **kwargs):
            arr = self.orig_create_int(*args, **kwargs)
            created["arr"] = arr
            return arr

        def _create_bool(*args, **kwargs):
            return int32(-1)

        def _resize_int(arr_id, new_size):
            self.orig_resize_int(arr_id, new_size)
            return int32(0)

        _bl.xs_array_create_int = _create_int
        _bl.xs_array_create_bool = _create_bool
        _bl.xs_array_resize_int = _resize_int

        self.assertEqual(c_bool_list_generic_error, xs_bool_list_create())
        self.assertEqual(0, xs_array_get_size(created["arr"]))

    def test_create_returns_without_allocating_bool_array_when_int_array_allocation_fails(self):
        calls: dict[str, int32] = {"create_bool": int32(0), "resize_bool": int32(0)}

        def _create_int(*args, **kwargs):
            return int32(-1)

        def _create_bool(*args, **kwargs):
            calls["create_bool"] += 1
            return _create_bool_array_impl(*args, **kwargs)

        def _resize_bool(arr_id, new_size):
            calls["resize_bool"] += 1
            return int32(0)

        _bl.xs_array_create_int = _create_int
        _bl.xs_array_create_bool = _create_bool
        _bl.xs_array_resize_bool = _resize_bool

        self.assertEqual(c_bool_list_generic_error, xs_bool_list_create())
        self.assertEqual(0, calls["create_bool"])
        self.assertEqual(0, calls["resize_bool"])

    def test_from_repeated_list_shrinks_bool_array_when_int_array_allocation_fails(self):
        created: dict[str, int32] = {}
        xs_lst = self._create_bool_list([True, False])

        def _create_int(*args, **kwargs):
            return int32(-1)

        def _create_bool(*args, **kwargs):
            arr = _create_bool_array_impl(*args, **kwargs)
            created["arr"] = arr
            return arr

        def _resize_bool(arr_id, new_size):
            _resize_bool_array_impl(arr_id, new_size)
            return int32(0)

        _bl.xs_array_create_int = _create_int
        _bl.xs_array_create_bool = _create_bool
        _bl.xs_array_resize_bool = _resize_bool

        self.assertEqual(c_bool_list_generic_error, xs_bool_list_from_repeated_list(xs_lst, int32(2)))
        self.assertEqual(0, xs_array_get_size(created["arr"]))

    def test_copy_shrinks_int_array_when_bool_array_allocation_fails(self):
        created: dict[str, int32] = {}
        xs_lst = self._create_bool_list([True, False])

        def _create_int(*args, **kwargs):
            arr = self.orig_create_int(*args, **kwargs)
            created["arr"] = arr
            return arr

        def _create_bool(*args, **kwargs):
            return int32(-1)

        def _resize_int(arr_id, new_size):
            self.orig_resize_int(arr_id, new_size)
            return int32(0)

        _bl.xs_array_create_int = _create_int
        _bl.xs_array_create_bool = _create_bool
        _bl.xs_array_resize_int = _resize_int

        self.assertEqual(c_bool_list_generic_error, xs_bool_list_copy(xs_lst))
        self.assertEqual(0, xs_array_get_size(created["arr"]))

    def test_from_array_shrinks_bool_array_when_int_array_allocation_fails(self):
        created: dict[str, int32] = {}
        xs_arr = self._create_bool_array([True, False])

        def _create_int(*args, **kwargs):
            return int32(-1)

        def _create_bool(*args, **kwargs):
            arr = _create_bool_array_impl(*args, **kwargs)
            created["arr"] = arr
            return arr

        def _resize_bool(arr_id, new_size):
            _resize_bool_array_impl(arr_id, new_size)
            return int32(0)

        _bl.xs_array_create_int = _create_int
        _bl.xs_array_create_bool = _create_bool
        _bl.xs_array_resize_bool = _resize_bool

        self.assertEqual(c_bool_list_generic_error, xs_bool_list_from_array(xs_arr))
        self.assertEqual(0, xs_array_get_size(created["arr"]))


def bstr(lst: list[bool]) -> str:
    r = "["
    for i, value in enumerate(lst):
        r += "true" if value else "false"
        if i < len(lst) - 1:
            r += ", "
    r += "]"
    return r
