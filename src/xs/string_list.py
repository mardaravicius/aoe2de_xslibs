from numpy import int32

from xs_converter.functions import xs_array_get_size, xs_array_get_int, xs_array_create_string, \
    xs_array_create_int, xs_array_set_string, xs_array_set_int, xs_array_get_string, xs_array_resize_int, \
    xs_array_resize_string, \
    str_char_at, str_index_of, str_len, str_remove, str_substring, str_trim
from xs_converter.symbols import XsConst, XsExternConst, i32range

c_string_list_success: XsExternConst[int32] = int32(0)
c_string_list_generic_error: XsExternConst[int32] = int32(-1)
c_string_list_index_out_of_range_error: XsExternConst[int32] = int32(-2)
c_string_list_resize_failed_error: XsExternConst[int32] = int32(-3)
c_string_list_max_capacity_error: XsExternConst[int32] = int32(-4)
c_string_list_max_capacity: XsExternConst[int32] = int32(999999999)
c_string_list_empty_int_param: XsExternConst[int32] = int32(-999999999)
_string_list_last_operation_status: int32 = c_string_list_success
_c_string_list_sort_run: XsConst[int32] = int32(16)
_string_list_sort_keys: int32 = int32(-1)
_string_list_sort_values: int32 = int32(-1)


def xs_string_list_size(lst: int32 = int32(-1)) -> int32:
    """
    Returns the number of elements in the list.
    :param lst: list id
    :return: list size
    """
    return xs_array_get_int(lst, 0)


def xs_string_list_create(capacity: int32 = int32(7)) -> int32:
    """
    Creates empty list for string values. List is a dynamic array that grows and shrinks as values are added and removed.
    :param capacity: initial list capacity
    :return: created list id, or `c_string_list_generic_error` on error
    """
    if capacity < 0 or capacity >= c_string_list_max_capacity:
        return c_string_list_generic_error
    lst: int32 = xs_array_create_int(2, 0)
    if lst < 0:
        return c_string_list_generic_error
    str_lst: int32 = xs_array_create_string(capacity)
    if str_lst < 0:
        xs_array_resize_int(lst, 0)
        return c_string_list_generic_error
    xs_array_set_int(lst, 1, str_lst)
    return lst


def xs_string_list(
        v0: str = "!<[empty",
        v1: str = "!<[empty",
        v2: str = "!<[empty",
        v3: str = "!<[empty",
        v4: str = "!<[empty",
        v5: str = "!<[empty",
        v6: str = "!<[empty",
        v7: str = "!<[empty",
        v8: str = "!<[empty",
        v9: str = "!<[empty",
        v10: str = "!<[empty",
        v11: str = "!<[empty",
) -> int32:
    """
    Creates a list with provided values. The first value that equals the default sentinel will stop further insertion.
    This Function can create a list with 12 values at the maximum, but further values can be added with other functions.
    :param v0 through v11: value at a given index of a list
    :return: created list id, or `c_string_list_generic_error` on error
    """
    str_lst: int32 = xs_array_create_string(12)
    if str_lst < 0:
        return c_string_list_generic_error
    lst: int32 = xs_array_create_int(2, str_lst)
    if lst < 0:
        xs_array_resize_string(str_lst, 0)
        return c_string_list_generic_error
    if v0 == "!<[empty":
        xs_array_set_int(lst, 0, int32(0))
        return lst
    xs_array_set_string(str_lst, 0, v0)
    if v1 == "!<[empty":
        xs_array_set_int(lst, 0, int32(1))
        return lst
    xs_array_set_string(str_lst, 1, v1)
    if v2 == "!<[empty":
        xs_array_set_int(lst, 0, int32(2))
        return lst
    xs_array_set_string(str_lst, 2, v2)
    if v3 == "!<[empty":
        xs_array_set_int(lst, 0, int32(3))
        return lst
    xs_array_set_string(str_lst, 3, v3)
    if v4 == "!<[empty":
        xs_array_set_int(lst, 0, int32(4))
        return lst
    xs_array_set_string(str_lst, 4, v4)
    if v5 == "!<[empty":
        xs_array_set_int(lst, 0, int32(5))
        return lst
    xs_array_set_string(str_lst, 5, v5)
    if v6 == "!<[empty":
        xs_array_set_int(lst, 0, int32(6))
        return lst
    xs_array_set_string(str_lst, 6, v6)
    if v7 == "!<[empty":
        xs_array_set_int(lst, 0, int32(7))
        return lst
    xs_array_set_string(str_lst, 7, v7)
    if v8 == "!<[empty":
        xs_array_set_int(lst, 0, int32(8))
        return lst
    xs_array_set_string(str_lst, 8, v8)
    if v9 == "!<[empty":
        xs_array_set_int(lst, 0, int32(9))
        return lst
    xs_array_set_string(str_lst, 9, v9)
    if v10 == "!<[empty":
        xs_array_set_int(lst, 0, int32(10))
        return lst
    xs_array_set_string(str_lst, 10, v10)
    if v11 == "!<[empty":
        xs_array_set_int(lst, 0, int32(11))
        return lst
    xs_array_set_string(str_lst, 11, v11)
    xs_array_set_int(lst, 0, int32(12))
    return lst


def xs_string_list_from_repeated_val(value: str = "", times: int32 = int32(0)) -> int32:
    """
    Creates a list by repeating a single value.
    :param value: value to repeat
    :param times: number of times to repeat the value
    :return: created list id, or `c_string_list_generic_error` on error
    """
    # Uses > (not >=) because the string array is 0-indexed and has no metadata slot,
    # so max_capacity elements fit exactly unlike int/float lists which reserve index 0.
    if times < 0 or times > c_string_list_max_capacity:
        return c_string_list_generic_error
    lst: int32 = xs_array_create_int(2, times)
    if lst < 0:
        return c_string_list_generic_error
    str_lst: int32 = xs_array_create_string(times, value)
    if str_lst < 0:
        xs_array_resize_int(lst, 0)
        return c_string_list_generic_error
    xs_array_set_int(lst, 1, str_lst)
    return lst


def xs_string_list_from_repeated_list(lst: int32 = int32(-1), times: int32 = int32(0)) -> int32:
    """
    Creates a new list by repeating all elements of the given list.
    :param lst: source list id
    :param times: number of times to repeat the list contents
    :return: created list id, or `c_string_list_generic_error` on error
    """
    if times < 0:
        return c_string_list_generic_error
    size: int32 = xs_array_get_int(lst, 0)
    if times > 0 and size > (c_string_list_max_capacity // times):
        return c_string_list_max_capacity_error
    new_capacity: int32 = (size * times)
    if new_capacity > c_string_list_max_capacity:
        return c_string_list_max_capacity_error
    new_str_lst: int32 = xs_array_create_string(new_capacity)
    if new_str_lst < 0:
        return c_string_list_generic_error
    new_lst: int32 = xs_array_create_int(2, new_capacity)
    if new_lst < 0:
        xs_array_resize_string(new_str_lst, 0)
        return c_string_list_generic_error
    str_lst: int32 = xs_array_get_int(lst, 1)
    for i in i32range(0, size):
        val: str = xs_array_get_string(str_lst, i)
        j: int32 = i
        while j < new_capacity:
            xs_array_set_string(new_str_lst, j, val)
            j += size
    xs_array_set_int(new_lst, 1, new_str_lst)
    return new_lst


def xs_string_list_from_array(arr: int32 = int32(-1)) -> int32:
    """
    Creates a new list by copying elements from an XS array.
    :param arr: source XS array id
    :return: created list id, or `c_string_list_generic_error` on error
    """
    arr_size: int32 = xs_array_get_size(arr)
    if arr_size > c_string_list_max_capacity:
        return c_string_list_max_capacity_error
    new_str_lst: int32 = xs_array_create_string(arr_size)
    if new_str_lst < 0:
        return c_string_list_generic_error
    lst: int32 = xs_array_create_int(2, arr_size)
    if lst < 0:
        xs_array_resize_string(new_str_lst, 0)
        return c_string_list_generic_error
    for i in i32range(0, arr_size):
        xs_array_set_string(new_str_lst, i, xs_array_get_string(arr, i))
    xs_array_set_int(lst, 1, new_str_lst)
    return lst


def xs_string_list_use_array_as_source(arr: int32 = int32(-1)) -> int32:
    """
    Wraps an existing XS string array as a list without copying elements.
    :param arr: XS string array id to use as backing storage
    :return: list id, or `c_string_list_max_capacity_error`/`c_string_list_generic_error` on error
    """
    arr_size: int32 = xs_array_get_size(arr)
    if arr_size > c_string_list_max_capacity:
        return c_string_list_max_capacity_error
    lst: int32 = xs_array_create_int(2, arr_size)
    if lst < 0:
        return c_string_list_generic_error
    xs_array_set_int(lst, 1, arr)
    return lst


def xs_string_list_get(lst: int32 = int32(-1), idx: int32 = int32(-1)) -> str:
    """
    Returns the element at the given index. Sets last error on failure.
    :param lst: list id
    :param idx: zero-based index
    :return: value at index, or "-1" on error
    """
    global _string_list_last_operation_status
    size: int32 = xs_string_list_size(lst)
    if idx < 0 or idx >= size:
        _string_list_last_operation_status = c_string_list_index_out_of_range_error
        return "-1"
    _string_list_last_operation_status = c_string_list_success
    return xs_array_get_string(xs_array_get_int(lst, 1), idx)


def xs_string_list_set(lst: int32 = int32(-1), idx: int32 = int32(-1), value: str = "") -> int32:
    """
    Sets the element at the given index to a new value.
    :param lst: list id
    :param idx: zero-based index
    :param value: new value to set
    :return: `c_string_list_success` on success, or error if negative
    """
    size: int32 = xs_array_get_int(lst, 0)
    if idx < 0 or idx >= size:
        return c_string_list_index_out_of_range_error
    xs_array_set_string(xs_array_get_int(lst, 1), idx, value)
    return c_string_list_success


def _xs_string_list_extend_string_array(lst: int32 = int32(-1), capacity: int32 = int32(0)) -> int32:
    if capacity >= c_string_list_max_capacity:
        return c_string_list_max_capacity_error
    new_capacity: int32 = int32(0)
    if capacity > c_string_list_max_capacity // 2:
        new_capacity = c_string_list_max_capacity
    else:
        new_capacity = capacity * 2
    if new_capacity > c_string_list_max_capacity:
        new_capacity = c_string_list_max_capacity
    elif new_capacity == 0:
        new_capacity = int32(8)
    r: int32 = xs_array_resize_string(lst, new_capacity)
    if r != 1:
        return c_string_list_resize_failed_error
    return c_string_list_success


def _xs_string_list_shrink_string_array(lst: int32 = int32(-1), size: int32 = int32(0),
                                        capacity: int32 = int32(0)) -> int32:
    if size <= (capacity // 2):
        r: int32 = xs_array_resize_string(lst, capacity // 2)
        if r != 1:
            return c_string_list_resize_failed_error
    return c_string_list_success


def xs_string_list_append(lst: int32 = int32(-1), value: str = "") -> int32:
    """
    Appends a value to the end of the list, growing the backing array if needed.
    :param lst: list id
    :param value: value to append
    :return: `c_string_list_success` on success, or error if negative
    """
    str_lst: int32 = xs_array_get_int(lst, 1)
    capacity: int32 = xs_array_get_size(str_lst)
    size: int32 = xs_array_get_int(lst, 0)
    if capacity <= size:
        r: int32 = _xs_string_list_extend_string_array(str_lst, capacity)
        if r != c_string_list_success:
            return r
    xs_array_set_string(str_lst, size, value)
    xs_array_set_int(lst, 0, size + 1)
    return c_string_list_success


def _xs_string_list_find_separator(text: str = "", separator: str = ",", start: int32 = int32(0)) -> int32:
    n: int32 = str_len(text)
    in_quotes: bool = False
    for i in i32range(start, n):
        ch: str = str_char_at(text, i)
        if ch == "'":
            in_quotes = not in_quotes
        elif ch == separator and not in_quotes:
            return i
    return int32(-1)


def _xs_string_list_split_items(items: str = "") -> int32:
    num_parts: int32 = int32(1)
    sep: int32 = _xs_string_list_find_separator(items, ",", 0)
    while sep >= 0:
        num_parts += 1
        sep = _xs_string_list_find_separator(items, ",", sep + 1)
    parts: int32 = xs_array_create_string(num_parts)
    start: int32 = int32(0)
    for i in i32range(0, num_parts):
        end: int32 = _xs_string_list_find_separator(items, ",", start)
        if end < 0:
            xs_array_set_string(parts, i, str_remove(items, 0, start))
        else:
            xs_array_set_string(parts, i, str_substring(items, start, end))
        start = end + 1
    return parts


def _xs_string_list_is_quoted(text: str = "") -> bool:
    n: int32 = str_len(text)
    if n < 2:
        return False
    if str_char_at(text, 0) != "'" or str_char_at(text, n - 1) != "'":
        return False
    return str_index_of(str_substring(text, 1, n - 1), "'") == -1


def xs_string_list_from_string(items: str = "") -> int32:
    """
    Creates a list from a comma separated string, e.g. `"'a','b c'"`. Strings must be wrapped in `'` and cannot contain `'`.
    Items are trimmed, and items that cannot be parsed are skipped.
    :param items: comma separated values
    :return: created list id, or `c_string_list_generic_error` on error
    """
    if str_trim(items) == "":
        return xs_string_list_create()
    parts: int32 = _xs_string_list_split_items(items)
    num_parts: int32 = xs_array_get_size(parts)
    lst: int32 = xs_string_list_create(num_parts)
    if lst < 0:
        xs_array_resize_string(parts, 0)
        return c_string_list_generic_error
    for i in i32range(0, num_parts):
        item: str = str_trim(xs_array_get_string(parts, i))
        if _xs_string_list_is_quoted(item):
            value: str = str_substring(item, 1, str_len(item) - 1)
            xs_string_list_append(lst, value)
    xs_array_resize_string(parts, 0)
    return lst


def xs_string_list_insert(lst: int32 = int32(-1), idx: int32 = int32(-1), value: str = "") -> int32:
    """
    Inserts a value at the given index, shifting subsequent elements to the right.
    :param lst: list id
    :param idx: zero-based index at which to insert
    :param value: value to insert
    :return: `c_string_list_success` on success, or error if negative
    """
    size: int32 = xs_array_get_int(lst, 0)
    if idx < 0 or idx > size:
        return c_string_list_index_out_of_range_error
    new_size: int32 = size + 1
    str_lst: int32 = xs_array_get_int(lst, 1)
    capacity: int32 = xs_array_get_size(str_lst)
    if capacity < new_size:
        r: int32 = _xs_string_list_extend_string_array(str_lst, capacity)
        if r != c_string_list_success:
            return r
    for i in i32range(size, idx, -1):
        xs_array_set_string(str_lst, i, xs_array_get_string(str_lst, i - 1))
    xs_array_set_string(str_lst, idx, value)
    xs_array_set_int(lst, 0, new_size)

    return c_string_list_success


def xs_string_list_pop(lst: int32 = int32(-1), idx: int32 = c_string_list_max_capacity) -> str:
    """
    Removes and returns the element at the given index, shifting subsequent elements to the left.
    Defaults to the last element. Sets last error on failure.
    :param lst: list id
    :param idx: zero-based index of element to remove (defaults to last)
    :return: removed value, or "-1" on error
    """
    global _string_list_last_operation_status
    str_lst: int32 = xs_array_get_int(lst, 1)
    capacity: int32 = xs_array_get_size(str_lst)
    size: int32 = xs_array_get_int(lst, 0)
    if idx == c_string_list_max_capacity:
        idx = size - 1
    if idx < 0 or idx >= size:
        _string_list_last_operation_status = c_string_list_index_out_of_range_error
        return "-1"
    removed_elem: str = xs_array_get_string(str_lst, idx)
    for i in i32range(idx, size - 1):
        xs_array_set_string(str_lst, i, xs_array_get_string(str_lst, i + 1))
    xs_array_set_int(lst, 0, size - 1)
    r: int32 = _xs_string_list_shrink_string_array(str_lst, size, capacity)
    if r != c_string_list_success:
        _string_list_last_operation_status = r
        return "-1"
    _string_list_last_operation_status = c_string_list_success
    return removed_elem


def xs_string_list_remove(lst: int32 = int32(-1), value: str = "") -> int32:
    """
    Removes the first occurrence of the given value from the list.
    :param lst: list id
    :param value: value to remove
    :return: index of the removed element, or `c_string_list_generic_error` if not found
    """
    str_lst: int32 = xs_array_get_int(lst, 1)
    size: int32 = xs_array_get_int(lst, 0)
    found_idx: int32 = int32(-1)
    i: int32 = int32(0)
    while i < size and found_idx == -1:
        c_val: str = xs_array_get_string(str_lst, i)
        if c_val == value:
            found_idx = i
        i += 1
    if found_idx == -1:
        return c_string_list_generic_error
    new_size: int32 = size - 1
    for j in i32range(found_idx, new_size):
        xs_array_set_string(str_lst, j, xs_array_get_string(str_lst, j + 1))
    xs_array_set_int(lst, 0, new_size)
    capacity: int32 = xs_array_get_size(str_lst)
    r: int32 = _xs_string_list_shrink_string_array(str_lst, size, capacity)
    if r != c_string_list_success:
        return r
    return found_idx


def xs_string_list_index(lst: int32 = int32(-1), value: str = "", start: int32 = int32(0),
                         stop: int32 = c_string_list_empty_int_param) -> int32:
    """
    Returns the index of the first occurrence of the value within the optional [start, stop) range. Negative start/stop are relative to the end.
    :param lst: list id
    :param value: value to search for
    :param start: start of search range (inclusive)
    :param stop: end of search range (exclusive), defaults to list size
    :return: index of the value, or `c_string_list_generic_error` if not found
    """
    size: int32 = xs_array_get_int(lst, 0)
    str_lst: int32 = xs_array_get_int(lst, 1)

    if stop == c_string_list_empty_int_param or stop > size:
        stop = size
    if start < 0:
        start += size
    if stop < 0:
        stop += size
    if start < 0:
        start = int32(0)
    if stop > size:
        stop = size

    for i in i32range(start, stop):
        if xs_array_get_string(str_lst, i) == value:
            return i
    return c_string_list_generic_error


def xs_string_list_contains(lst: int32 = int32(-1), value: str = "") -> bool:
    """
    Checks whether the list contains the given value.
    :param lst: list id
    :param value: value to search for
    :return: true if the value is found, false otherwise
    """
    return xs_string_list_index(lst, value) > -1


def _xs_string_list_compare_elem(a: str = "", b: str = "", reverse: bool = False) -> bool:
    if reverse:
        return a > b
    return a < b


def _xs_string_list_insertion_sort_with(data: int32 = int32(-1), other: int32 = int32(-1), lo: int32 = int32(0),
                                        hi: int32 = int32(0), voff: int32 = int32(0), reverse: bool = False) -> None:
    has_other: bool = other >= 0
    for i in i32range(lo + 1, hi):
        key: str = xs_array_get_string(data, i)
        value: int32 = int32(0)
        if has_other:
            value = xs_array_get_int(other, i + voff)
        j: int32 = i - 1
        shifting: bool = True
        while shifting and j >= lo:
            prev: str = xs_array_get_string(data, j)
            if _xs_string_list_compare_elem(key, prev, reverse):
                xs_array_set_string(data, j + 1, prev)
                if has_other:
                    xs_array_set_int(other, j + 1 + voff, xs_array_get_int(other, j + voff))
                j -= 1
            else:
                shifting = False
        xs_array_set_string(data, j + 1, key)
        if has_other:
            xs_array_set_int(other, j + 1 + voff, value)


def _xs_string_list_sift_down(lst: int32 = int32(-1), start: int32 = int32(-1), end: int32 = int32(-1),
                              reverse: bool = False) -> None:
    root: int32 = start
    val: str = xs_array_get_string(lst, root)
    sifting: bool = True
    while sifting:
        child: int32 = 2 * root + 1
        if child > end:
            sifting = False
        else:
            child_val: str = xs_array_get_string(lst, child)
            if child + 1 <= end:
                child_val1: str = xs_array_get_string(lst, child + 1)
                if _xs_string_list_compare_elem(child_val, child_val1, reverse):
                    child += 1
                    child_val = child_val1
            if _xs_string_list_compare_elem(val, child_val, reverse):
                xs_array_set_string(lst, root, child_val)
                root = child
            else:
                sifting = False
    xs_array_set_string(lst, root, val)


def xs_string_list_sort(lst: int32 = int32(-1), reverse: bool = False) -> None:
    """
    Sorts the list in-place.
    :param lst: list id
    :param reverse: if true, sorts in descending order
    """
    size: int32 = xs_array_get_int(lst, 0)
    str_lst: int32 = xs_array_get_int(lst, 1)
    if size <= _c_string_list_sort_run:
        _xs_string_list_insertion_sort_with(str_lst, int32(-1), int32(0), size, int32(0), reverse)
        return
    for start in i32range(size // 2 - 1, -1, -1):
        _xs_string_list_sift_down(str_lst, start, size - 1, reverse)

    for end in i32range(size - 1, 0, -1):
        temp: str = xs_array_get_string(str_lst, 0)
        xs_array_set_string(str_lst, 0, xs_array_get_string(str_lst, end))
        xs_array_set_string(str_lst, end, temp)
        _xs_string_list_sift_down(str_lst, int32(0), end - 1, reverse)


def _xs_string_list_ensure_sort_buffers(keys_size: int32 = int32(0), values_size: int32 = int32(0)) -> int32:
    global _string_list_sort_keys, _string_list_sort_values
    if _string_list_sort_keys < 0:
        _string_list_sort_keys = xs_array_create_string(keys_size)
        if _string_list_sort_keys < 0:
            return c_string_list_generic_error
    if _string_list_sort_values < 0:
        _string_list_sort_values = xs_array_create_int(values_size)
        if _string_list_sort_values < 0:
            return c_string_list_generic_error
    r: int32 = int32(1)
    if xs_array_get_size(_string_list_sort_keys) < keys_size:
        r = xs_array_resize_string(_string_list_sort_keys, keys_size)
        if r != 1:
            return c_string_list_resize_failed_error
    if xs_array_get_size(_string_list_sort_values) < values_size:
        r = xs_array_resize_int(_string_list_sort_values, values_size)
        if r != 1:
            return c_string_list_resize_failed_error
    return c_string_list_success


def _xs_string_list_release_sort_buffers(release_buffers: bool = True) -> None:
    if not release_buffers:
        return
    if _string_list_sort_keys >= 0:
        xs_array_resize_string(_string_list_sort_keys, 0)
    if _string_list_sort_values >= 0:
        xs_array_resize_int(_string_list_sort_values, 0)


def _xs_string_list_merge_with(src: int32 = int32(-1), src_other: int32 = int32(-1), dst: int32 = int32(-1),
                               dst_other: int32 = int32(-1), lo: int32 = int32(0), mid: int32 = int32(0),
                               hi: int32 = int32(0), voff: int32 = int32(0), reverse: bool = False) -> None:
    i: int32 = lo
    j: int32 = mid
    k: int32 = lo
    if i < mid and j < hi:
        left: str = xs_array_get_string(src, i)
        right: str = xs_array_get_string(src, j)
        while i < mid and j < hi:
            if _xs_string_list_compare_elem(right, left, reverse):
                xs_array_set_string(dst, k, right)
                xs_array_set_int(dst_other, k + voff, xs_array_get_int(src_other, j + voff))
                j += 1
                if j < hi:
                    right = xs_array_get_string(src, j)
            else:
                xs_array_set_string(dst, k, left)
                xs_array_set_int(dst_other, k + voff, xs_array_get_int(src_other, i + voff))
                i += 1
                if i < mid:
                    left = xs_array_get_string(src, i)
            k += 1
    while i < mid:
        xs_array_set_string(dst, k, xs_array_get_string(src, i))
        xs_array_set_int(dst_other, k + voff, xs_array_get_int(src_other, i + voff))
        i += 1
        k += 1
    while j < hi:
        xs_array_set_string(dst, k, xs_array_get_string(src, j))
        xs_array_set_int(dst_other, k + voff, xs_array_get_int(src_other, j + voff))
        j += 1
        k += 1


def xs_string_list_sort_with(lst: int32 = int32(-1), other: int32 = int32(-1), reverse: bool = False, release_buffers: bool = True) -> int32:
    """
    Sorts the list in-place with a stable sort, and moves the elements of `other` the same way,
    so `other[i]` stays paired with `lst[i]`. Equal elements keep their original order.
    Inputs larger than 16 elements use two internal buffer arrays shared by all calls.
    :param lst: list id
    :param other: int list id of the same size as `lst`
    :param reverse: if true, sorts in descending order
    :param release_buffers: if true, resizes the internal buffers to 0 after sorting to free their memory;
        the same buffers are grown again on the next call
    :return: `c_string_list_success` on success, `c_string_list_generic_error` if the sizes differ or buffers
        can't be created, or `c_string_list_resize_failed_error` if the buffers can't grow
    """
    size: int32 = xs_array_get_int(lst, 0)
    data: int32 = xs_array_get_int(lst, 1)
    start: int32 = int32(0)
    end: int32 = size
    voff: int32 = int32(1)
    if xs_array_get_int(other, 0) != size:
        return c_string_list_generic_error
    if size > _c_string_list_sort_run:
        r: int32 = _xs_string_list_ensure_sort_buffers(end, end + voff)
        if r != c_string_list_success:
            _xs_string_list_release_sort_buffers(release_buffers)
            return r
    run_start: int32 = start
    while run_start < end:
        run_end: int32 = run_start + _c_string_list_sort_run
        if run_end > end:
            run_end = end
        _xs_string_list_insertion_sort_with(data, other, run_start, run_end, voff, reverse)
        run_start = run_end
    if size <= _c_string_list_sort_run:
        return c_string_list_success
    src: int32 = data
    src_other: int32 = other
    dst: int32 = _string_list_sort_keys
    dst_other: int32 = _string_list_sort_values
    in_buffers: bool = False
    width: int32 = _c_string_list_sort_run
    while width < size:
        lo: int32 = start
        while lo < end:
            mid: int32 = lo + width
            if mid > end:
                mid = end
            hi: int32 = mid + width
            if hi > end:
                hi = end
            _xs_string_list_merge_with(src, src_other, dst, dst_other, lo, mid, hi, voff, reverse)
            lo = hi
        temp: int32 = src
        src = dst
        dst = temp
        temp = src_other
        src_other = dst_other
        dst_other = temp
        in_buffers = not in_buffers
        width *= 2
    if in_buffers:
        for i in i32range(start, end):
            xs_array_set_string(data, i, xs_array_get_string(src, i))
            xs_array_set_int(other, i + voff, xs_array_get_int(src_other, i + voff))
    _xs_string_list_release_sort_buffers(release_buffers)
    return c_string_list_success


def xs_string_list_to_string(lst: int32 = int32(-1), start: str = "[", sep: str = ", ", end: str = "]", quote: str = "\"") -> str:
    """
    Returns a string representation of the list, by default in the format `["v0", "v1", ...]`.
    :param lst: list id
    :param start: string prepended to the output
    :param sep: separator between elements
    :param end: string appended to the output
    :param quote: string wrapped around string elements
    :return: string representation of the list
    """
    size: int32 = xs_array_get_int(lst, 0)
    str_lst: int32 = xs_array_get_int(lst, 1)
    s: str = start
    for i in i32range(0, size):
        s += quote + xs_array_get_string(str_lst, i) + quote
        if i < size - 1:
            s += sep
    s += end
    return s


def xs_string_list_copy(lst: int32 = int32(-1), start: int32 = int32(0),
                        end: int32 = c_string_list_max_capacity) -> int32:
    """
    Returns a copy of the list, optionally sliced by [start, end). Negative start/end are relative to the end.
    :param lst: list id
    :param start: start of slice (inclusive)
    :param end: end of slice (exclusive), defaults to list size
    :return: new list id, or `c_string_list_generic_error` on error
    """
    size: int32 = xs_array_get_int(lst, 0)
    fr: int32 = int32(0)
    if start < 0:
        fr = size + start
    else:
        fr = start
    to: int32 = int32(0)
    if end < 0:
        to = size + end
    else:
        to = end
    if fr < 0:
        fr = int32(0)
    if to > size:
        to = size
    new_size: int32 = to - fr
    if new_size < 0:
        new_size = int32(0)
    new_lst: int32 = xs_array_create_int(2, new_size)
    if new_lst < 0:
        return c_string_list_generic_error
    new_str_lst: int32 = xs_array_create_string(new_size)
    if new_str_lst < 0:
        xs_array_resize_int(new_lst, 0)
        return c_string_list_generic_error
    xs_array_set_int(new_lst, 1, new_str_lst)
    str_lst: int32 = xs_array_get_int(lst, 1)
    for i in i32range(fr, to):
        xs_array_set_string(new_str_lst, i - fr, xs_array_get_string(str_lst, i))

    return new_lst


def xs_string_list_extend(source: int32 = int32(-1), lst: int32 = int32(-1)) -> int32:
    """
    Appends all elements from another list to the source list.
    :param source: list id to extend
    :param lst: list id whose elements are appended
    :return: `c_string_list_success` on success, or error if negative
    """
    source_size: int32 = xs_array_get_int(source, 0)
    to_add: int32 = xs_array_get_int(lst, 0)
    str_source: int32 = xs_array_get_int(source, 1)
    capacity: int32 = xs_array_get_size(str_source)
    new_size: int32 = source_size + to_add
    if new_size > capacity:
        if new_size > c_string_list_max_capacity:
            return c_string_list_max_capacity_error
        r: int32 = xs_array_resize_string(str_source, new_size)
        if r != 1:
            return c_string_list_resize_failed_error
    str_list: int32 = xs_array_get_int(lst, 1)
    for i in i32range(0, to_add):
        xs_array_set_string(str_source, i + source_size, xs_array_get_string(str_list, i))
    xs_array_set_int(source, 0, new_size)
    return c_string_list_success


def xs_string_list_extend_with_array(source: int32 = int32(-1), arr: int32 = int32(-1)) -> int32:
    """
    Appends all elements from an XS array to the source list.
    :param source: list id to extend
    :param arr: XS array id whose elements are appended
    :return: `c_string_list_success` on success, or error if negative
    """
    source_size: int32 = xs_array_get_int(source, 0)
    to_add: int32 = xs_array_get_size(arr)
    str_source: int32 = xs_array_get_int(source, 1)
    capacity: int32 = xs_array_get_size(str_source)
    new_size: int32 = source_size + to_add
    if new_size > capacity:
        if new_size > c_string_list_max_capacity or new_size < 0:
            return c_string_list_max_capacity_error
        r: int32 = xs_array_resize_string(str_source, new_size)
        if r != 1:
            return c_string_list_resize_failed_error
    for i in i32range(0, to_add):
        xs_array_set_string(str_source, i + source_size, xs_array_get_string(arr, i))
    xs_array_set_int(source, 0, new_size)
    return c_string_list_success


def xs_string_list_clear(lst: int32 = int32(-1)) -> int32:
    """
    Removes all elements from the list and shrinks the backing array.
    :param lst: list id
    :return: `c_string_list_success` on success, or error if negative
    """
    str_list: int32 = xs_array_get_int(lst, 1)
    capacity: int32 = xs_array_get_size(str_list)
    if capacity > 8:
        r: int32 = xs_array_resize_string(str_list, 8)
        if r != 1:
            return c_string_list_resize_failed_error
    xs_array_set_int(lst, 0, 0)
    return c_string_list_success


def xs_string_list_delete(lst: int32 = int32(-1)) -> int32:
    """
    Resizes all arrays of the list to 0 to free their memory. XS can't fully delete arrays,
    so the list id stays allocated and must not be used afterwards.
    :param lst: list id
    :return: `c_string_list_success` on success, or `c_string_list_resize_failed_error` if any resize fails
    """
    r: int32 = xs_array_resize_string(xs_array_get_int(lst, 1), 0)
    if r != 1:
        return c_string_list_resize_failed_error
    r = xs_array_resize_int(lst, 0)
    if r != 1:
        return c_string_list_resize_failed_error
    return c_string_list_success


def xs_string_list_compare(lst1: int32 = int32(-1), lst2: int32 = int32(-1)) -> int32:
    """
    Performs lexicographic comparison of two lists.
    :param lst1: first list id
    :param lst2: second list id
    :return: -1 if lst1 < lst2, 1 if lst1 > lst2, 0 if equal
    """
    size1: int32 = xs_array_get_int(lst1, 0)
    size2: int32 = xs_array_get_int(lst2, 0)
    str_list1: int32 = xs_array_get_int(lst1, 1)
    str_list2: int32 = xs_array_get_int(lst2, 1)
    i: int32 = int32(0)
    while i < size1 and i < size2:
        v1: str = xs_array_get_string(str_list1, i)
        v2: str = xs_array_get_string(str_list2, i)
        if v1 < v2:
            return int32(-1)
        if v1 > v2:
            return int32(1)
        i += 1
    if size1 < size2:
        return int32(-1)
    if size1 > size2:
        return int32(1)
    return int32(0)


def xs_string_list_reverse(lst: int32 = int32(-1)) -> None:
    """
    Reverses the list in-place.
    :param lst: list id
    """
    size: int32 = xs_array_get_int(lst, 0)
    str_list: int32 = xs_array_get_int(lst, 1)
    mid: int32 = size // 2
    for i in i32range(0, mid):
        temp: str = xs_array_get_string(str_list, i)
        back_i: int32 = size - i - 1
        xs_array_set_string(str_list, i, xs_array_get_string(str_list, back_i))
        xs_array_set_string(str_list, back_i, temp)


def xs_string_list_count(lst: int32 = int32(-1), value: str = "") -> int32:
    """
    Counts the number of occurrences of a value in the list.
    :param lst: list id
    :param value: value to count
    :return: number of occurrences
    """
    count: int32 = int32(0)
    size: int32 = xs_array_get_int(lst, 0)
    str_list: int32 = xs_array_get_int(lst, 1)
    for i in i32range(0, size):
        if xs_array_get_string(str_list, i) == value:
            count += 1
    return count


def xs_string_list_min(lst: int32 = int32(-1)) -> str:
    """
    Returns the minimum value in the list (lexicographic). Sets last error on failure.
    :param lst: list id
    :return: minimum value, or "-1" on error
    """
    global _string_list_last_operation_status
    size: int32 = xs_array_get_int(lst, 0)
    if size == 0:
        _string_list_last_operation_status = c_string_list_index_out_of_range_error
        return "-1"
    str_list: int32 = xs_array_get_int(lst, 1)
    m: str = xs_array_get_string(str_list, 0)
    if size == 1:
        _string_list_last_operation_status = c_string_list_success
        return m
    for i in i32range(1, size):
        v: str = xs_array_get_string(str_list, i)
        if v < m:
            m = v
    _string_list_last_operation_status = c_string_list_success
    return m


def xs_string_list_max(lst: int32 = int32(-1)) -> str:
    """
    Returns the maximum value in the list (lexicographic). Sets last error on failure.
    :param lst: list id
    :return: maximum value, or "-1" on error
    """
    global _string_list_last_operation_status
    size: int32 = xs_array_get_int(lst, 0)
    if size == 0:
        _string_list_last_operation_status = c_string_list_index_out_of_range_error
        return "-1"
    str_list: int32 = xs_array_get_int(lst, 1)
    m: str = xs_array_get_string(str_list, 0)
    if size == 1:
        _string_list_last_operation_status = c_string_list_success
        return m
    for i in i32range(1, size):
        v: str = xs_array_get_string(str_list, i)
        if v > m:
            m = v
    _string_list_last_operation_status = c_string_list_success
    return m


def xs_string_list_last_error() -> int32:
    """
    Returns the status code of the last operation that sets it (get, pop, min, max).
    :return: `c_string_list_success` if the last such operation succeeded, or a negative error code
    """
    return _string_list_last_operation_status
