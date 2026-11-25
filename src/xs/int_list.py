from numpy import int32

from xs_converter.functions import xs_array_create_int, xs_array_set_int, xs_array_resize_int, xs_array_get_int, \
    xs_array_get_size, \
    str_split, str_to_int, str_trim, xs_array_get_string, xs_array_resize_string
from xs_converter.symbols import XsExternConst, i32range

c_int_list_success: XsExternConst[int32] = int32(0)
c_int_list_generic_error: XsExternConst[int32] = int32(-1)
c_int_list_index_out_of_range_error: XsExternConst[int32] = int32(-2)
c_int_list_resize_failed_error: XsExternConst[int32] = int32(-3)
c_int_list_max_capacity_error: XsExternConst[int32] = int32(-4)
c_int_list_max_capacity: XsExternConst[int32] = int32(999999999)
c_int_list_empty_param: XsExternConst[int32] = int32(-999999999)
_c_int_list_int_max: int32 = int32(-1)
_c_int_list_int_min: int32 = int32(-1)
_int_list_last_operation_status: int32 = c_int_list_success
_int_list_sort_keys: int32 = int32(-1)
_int_list_sort_values: int32 = int32(-1)


def xs_int_list_create(capacity: int32 = int32(7)) -> int32:
    """
    Creates empty list for int values. List is a dynamic array that grows and shrinks as values are added and removed.
    :param capacity: initial list capacity
    :return: created list id, or `c_int_list_generic_error` on error
    """
    if capacity < 0 or capacity >= c_int_list_max_capacity:
        return c_int_list_generic_error
    lst: int32 = xs_array_create_int(capacity + 1)
    if lst < 0:
        return c_int_list_generic_error
    xs_array_set_int(lst, 0, 0)
    return lst


def xs_int_list(
        v0: int32 = c_int_list_empty_param,
        v1: int32 = c_int_list_empty_param,
        v2: int32 = c_int_list_empty_param,
        v3: int32 = c_int_list_empty_param,
        v4: int32 = c_int_list_empty_param,
        v5: int32 = c_int_list_empty_param,
        v6: int32 = c_int_list_empty_param,
        v7: int32 = c_int_list_empty_param,
        v8: int32 = c_int_list_empty_param,
        v9: int32 = c_int_list_empty_param,
        v10: int32 = c_int_list_empty_param,
        v11: int32 = c_int_list_empty_param,
) -> int32:
    """
    Creates a list with provided values. The first value that equals `c_int_list_empty_param` will stop further insertion.
    This Function can create a list with 12 values at the maximum, but further values can be added with other functions.
    :param v0 through v11: value at a given index of a list
    :return: created list id, or `c_int_list_generic_error` on error
    """
    lst: int32 = xs_array_create_int(13)
    if lst < 0:
        return c_int_list_generic_error
    if v0 == c_int_list_empty_param:
        xs_array_set_int(lst, 0, 0)
        return lst
    xs_array_set_int(lst, 1, v0)
    if v1 == c_int_list_empty_param:
        xs_array_set_int(lst, 0, 1)
        return lst
    xs_array_set_int(lst, 2, v1)
    if v2 == c_int_list_empty_param:
        xs_array_set_int(lst, 0, 2)
        return lst
    xs_array_set_int(lst, 3, v2)
    if v3 == c_int_list_empty_param:
        xs_array_set_int(lst, 0, 3)
        return lst
    xs_array_set_int(lst, 4, v3)
    if v4 == c_int_list_empty_param:
        xs_array_set_int(lst, 0, 4)
        return lst
    xs_array_set_int(lst, 5, v4)
    if v5 == c_int_list_empty_param:
        xs_array_set_int(lst, 0, 5)
        return lst
    xs_array_set_int(lst, 6, v5)
    if v6 == c_int_list_empty_param:
        xs_array_set_int(lst, 0, 6)
        return lst
    xs_array_set_int(lst, 7, v6)
    if v7 == c_int_list_empty_param:
        xs_array_set_int(lst, 0, 7)
        return lst
    xs_array_set_int(lst, 8, v7)
    if v8 == c_int_list_empty_param:
        xs_array_set_int(lst, 0, 8)
        return lst
    xs_array_set_int(lst, 9, v8)
    if v9 == c_int_list_empty_param:
        xs_array_set_int(lst, 0, 9)
        return lst
    xs_array_set_int(lst, 10, v9)
    if v10 == c_int_list_empty_param:
        xs_array_set_int(lst, 0, 10)
        return lst
    xs_array_set_int(lst, 11, v10)
    if v11 == c_int_list_empty_param:
        xs_array_set_int(lst, 0, 11)
        return lst
    xs_array_set_int(lst, 12, v11)
    xs_array_set_int(lst, 0, 12)
    return lst


def _xs_int_list_int_abs(n: int32 = int32(0)) -> int32:
    if n < int32(0):
        return n * int32(-1)
    return n


def xs_int_list_from_range(start: int32 = int32(0), stop: int32 = int32(0), step: int32 = int32(1)) -> int32:
    """
    Creates a list from a given range.
    :param start: start of range (inclusive)
    :param stop: end of range (exclusive)
    :param step: increment between values (positive or negative, must not be zero)
    :return: created list id, or `c_int_list_generic_error` on error
    """
    global _c_int_list_int_min, _c_int_list_int_max
    if _c_int_list_int_min == int32(-1):
        _c_int_list_int_min = -2147483648
        _c_int_list_int_max = 2147483647
    if step == 0 or step == _c_int_list_int_min:
        return c_int_list_generic_error
    distance: int32 = int32(0)
    if step > 0:
        if start > stop:
            return c_int_list_generic_error
        if start < 0 and stop >= 0 and stop > _c_int_list_int_max + start:
            return c_int_list_generic_error
        distance = stop - start
    else:
        if start < stop:
            return c_int_list_generic_error
        if start >= 0 and stop < 0 and start > _c_int_list_int_max + stop:
            return c_int_list_generic_error
        distance = start - stop
    step_a: int32 = _xs_int_list_int_abs(step)
    size: int32 = distance // step_a
    if size >= c_int_list_max_capacity:
        return c_int_list_generic_error
    if distance % step_a > 0:
        size += int32(1)
    lst: int32 = xs_array_create_int(size + 1)
    if lst < 0:
        return c_int_list_generic_error
    i: int32 = int32(1)
    current: int32 = start
    while i <= size:
        xs_array_set_int(lst, i, current)
        if i < size:
            current += step
        i += 1
    xs_array_set_int(lst, 0, size)
    return lst


def xs_int_list_from_repeated_val(value: int32 = int32(0), times: int32 = int32(0)) -> int32:
    """
    Creates a list by repeating a single value.
    :param value: value to repeat
    :param times: number of times to repeat the value
    :return: created list id, or `c_int_list_generic_error` on error
    """
    if times < 0 or times >= c_int_list_max_capacity:
        return c_int_list_generic_error
    lst: int32 = xs_array_create_int(times + 1, value)
    if lst < 0:
        return c_int_list_generic_error
    xs_array_set_int(lst, 0, times)
    return lst


def xs_int_list_from_repeated_list(lst: int32 = int32(-1), times: int32 = int32(0)) -> int32:
    """
    Creates a new list by repeating all elements of the given list.
    :param lst: source list id
    :param times: number of times to repeat the list contents
    :return: created list id, or `c_int_list_generic_error` on error
    """
    if times < 0:
        return c_int_list_generic_error
    size: int32 = xs_array_get_int(lst, 0)
    if times > 0 and size > (c_int_list_max_capacity // times):
        return c_int_list_max_capacity_error
    new_capacity: int32 = (size * times) + 1
    if new_capacity > c_int_list_max_capacity:
        return c_int_list_max_capacity_error
    new_lst: int32 = xs_array_create_int(new_capacity)
    if new_lst < 0:
        return c_int_list_generic_error
    for i in i32range(1, size + 1):
        val: int32 = xs_array_get_int(lst, i)
        j: int32 = i
        while j < new_capacity:
            xs_array_set_int(new_lst, j, val)
            j += size
    xs_array_set_int(new_lst, 0, new_capacity - 1)
    return new_lst


def xs_int_list_from_array(arr: int32 = int32(-1)) -> int32:
    """
    Creates a new list by copying elements from an XS array.
    :param arr: source XS array id
    :return: created list id, or `c_int_list_generic_error` on error
    """
    arr_size: int32 = xs_array_get_size(arr)
    lst: int32 = xs_int_list_create(arr_size)
    if lst < 0:
        return lst
    for i in i32range(0, arr_size):
        xs_array_set_int(lst, i + 1, xs_array_get_int(arr, i))
    xs_array_set_int(lst, 0, arr_size)
    return lst


def xs_int_list_use_array_as_source(arr: int32 = int32(-1)) -> int32:
    """
    Converts an existing XS array into a list in-place by shifting elements and storing the size.
    :param arr: XS array id to convert
    :return: list id (same as arr), or `c_int_list_max_capacity_error`/`c_int_list_resize_failed_error` on error
    """
    arr_size: int32 = xs_array_get_size(arr)
    if arr_size + 1 > c_int_list_max_capacity:
        return c_int_list_max_capacity_error
    r: int32 = xs_array_resize_int(arr, arr_size + 1)
    if r < 0:
        return c_int_list_resize_failed_error
    for i in i32range(arr_size - 1, -1, -1):
        xs_array_set_int(arr, i + 1, xs_array_get_int(arr, i))
    xs_array_set_int(arr, 0, arr_size)
    return arr


def xs_int_list_get(lst: int32 = int32(-1), idx: int32 = int32(-1)) -> int32:
    """
    Returns the element at the given index. Sets last error on failure.
    :param lst: list id
    :param idx: zero-based index
    :return: value at index, or `c_int_list_generic_error` on error
    """
    global _int_list_last_operation_status
    size: int32 = xs_array_get_int(lst, 0)
    if idx < 0 or idx >= size:
        _int_list_last_operation_status = c_int_list_index_out_of_range_error
        return c_int_list_generic_error
    _int_list_last_operation_status = c_int_list_success
    return xs_array_get_int(lst, idx + 1)


def xs_int_list_set(lst: int32 = int32(-1), idx: int32 = int32(-1), value: int32 = int32(0)) -> int32:
    """
    Sets the element at the given index to a new value.
    :param lst: list id
    :param idx: zero-based index
    :param value: new value to set
    :return: `c_int_list_success` on success, or error if negative
    """
    size: int32 = xs_array_get_int(lst, 0)
    if idx < 0 or idx >= size:
        return c_int_list_index_out_of_range_error
    xs_array_set_int(lst, idx + 1, value)
    return c_int_list_success


def xs_int_list_size(lst: int32 = int32(-1)) -> int32:
    """
    Returns the number of elements in the list.
    :param lst: list id
    :return: list size
    """
    return xs_array_get_int(lst, 0)


def _xs_int_list_extend_int_array(lst: int32 = int32(-1), capacity: int32 = int32(0)) -> int32:
    if capacity >= c_int_list_max_capacity:
        return c_int_list_max_capacity_error
    new_capacity: int32 = int32(0)
    if capacity > c_int_list_max_capacity // 2:
        new_capacity = c_int_list_max_capacity
    else:
        new_capacity = capacity * 2
    if new_capacity > c_int_list_max_capacity:
        new_capacity = c_int_list_max_capacity
    elif new_capacity == 0:
        new_capacity = int32(8)
    r: int32 = xs_array_resize_int(lst, new_capacity)
    if r != 1:
        return c_int_list_resize_failed_error
    return c_int_list_success


def _xs_int_list_shrink_int_array(lst: int32 = int32(-1), size: int32 = int32(0), capacity: int32 = int32(0)) -> int32:
    if size <= (capacity // 2):
        r: int32 = xs_array_resize_int(lst, capacity // 2)
        if r != 1:
            return c_int_list_resize_failed_error
    return c_int_list_success


def xs_int_list_append(lst: int32 = int32(-1), value: int32 = int32(0)) -> int32:
    """
    Appends a value to the end of the list, growing the backing array if needed.
    :param lst: list id
    :param value: value to append
    :return: `c_int_list_success` on success, or error if negative
    """
    capacity: int32 = xs_array_get_size(lst)
    size: int32 = xs_array_get_int(lst, 0)
    next_idx: int32 = size + 1
    if capacity <= next_idx:
        r: int32 = _xs_int_list_extend_int_array(lst, capacity)
        if r != c_int_list_success:
            return r
    xs_array_set_int(lst, next_idx, value)
    xs_array_set_int(lst, 0, next_idx)
    return c_int_list_success


def xs_int_list_insert(lst: int32 = int32(-1), idx: int32 = int32(-1), value: int32 = int32(0)) -> int32:
    """
    Inserts a value at the given index, shifting subsequent elements to the right.
    :param lst: list id
    :param idx: zero-based index at which to insert
    :param value: value to insert
    :return: `c_int_list_success` on success, or error if negative
    """
    capacity: int32 = xs_array_get_size(lst)
    size: int32 = xs_array_get_int(lst, 0)
    if idx < 0 or idx > size:
        return c_int_list_index_out_of_range_error
    new_size: int32 = size + 1
    if capacity <= new_size:
        r: int32 = _xs_int_list_extend_int_array(lst, capacity)
        if r != c_int_list_success:
            return r
    for i in i32range(size, idx, -1):
        xs_array_set_int(lst, i + 1, xs_array_get_int(lst, i))
    xs_array_set_int(lst, idx + 1, value)
    xs_array_set_int(lst, 0, new_size)

    return c_int_list_success


def xs_int_list_pop(lst: int32 = int32(-1), idx: int32 = c_int_list_max_capacity) -> int32:
    """
    Removes and returns the element at the given index, shifting subsequent elements to the left.
    Defaults to the last element. Sets last error on failure.
    :param lst: list id
    :param idx: zero-based index of element to remove (defaults to last)
    :return: removed value, or `c_int_list_generic_error` on error
    """
    global _int_list_last_operation_status
    capacity: int32 = xs_array_get_size(lst)
    size: int32 = xs_array_get_int(lst, 0)
    if idx == c_int_list_max_capacity:
        idx = size - 1
    if idx < 0 or idx >= size:
        _int_list_last_operation_status = c_int_list_index_out_of_range_error
        return c_int_list_generic_error
    removed_elem: int32 = xs_array_get_int(lst, idx + 1)
    for i in i32range(idx + 2, size + 1):
        xs_array_set_int(lst, i - 1, xs_array_get_int(lst, i))
    xs_array_set_int(lst, 0, size - 1)
    r: int32 = _xs_int_list_shrink_int_array(lst, size, capacity)
    if r != c_int_list_success:
        _int_list_last_operation_status = r
        return c_int_list_generic_error
    _int_list_last_operation_status = c_int_list_success
    return removed_elem


def xs_int_list_remove(lst: int32 = int32(-1), value: int32 = int32(-1)) -> int32:
    """
    Removes the first occurrence of the given value from the list.
    :param lst: list id
    :param value: value to remove
    :return: index of the removed element, or `c_int_list_generic_error` if not found
    """
    capacity: int32 = xs_array_get_size(lst)
    size: int32 = xs_array_get_int(lst, 0)
    found_idx: int32 = int32(-1)
    i: int32 = int32(1)
    while i <= size and found_idx == -1:
        c_val: int32 = xs_array_get_int(lst, i)
        if c_val == value:
            found_idx = i
        i += 1
    if found_idx == -1:
        return c_int_list_generic_error
    for j in i32range(found_idx + 1, size + 1):
        xs_array_set_int(lst, j - 1, xs_array_get_int(lst, j))
    xs_array_set_int(lst, 0, size - 1)
    r: int32 = _xs_int_list_shrink_int_array(lst, size, capacity)
    if r != c_int_list_success:
        return r
    return found_idx - 1


def xs_int_list_index(lst: int32 = int32(-1), value: int32 = int32(-1), start: int32 = int32(0), stop: int32 = c_int_list_empty_param) -> int32:
    """
    Returns the index of the first occurrence of the value within the optional [start, stop) range. Negative start/stop are relative to the end.
    :param lst: list id
    :param value: value to search for
    :param start: start of search range (inclusive)
    :param stop: end of search range (exclusive), defaults to list size
    :return: index of the value, or `c_int_list_generic_error` if not found
    """
    size: int32 = xs_array_get_int(lst, 0)

    if stop == c_int_list_empty_param or stop > size:
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
        if xs_array_get_int(lst, i + 1) == value:
            return i
    return c_int_list_generic_error


def xs_int_list_contains(lst: int32 = int32(-1), value: int32 = int32(-1)) -> bool:
    """
    Checks whether the list contains the given value.
    :param lst: list id
    :param value: value to search for
    :return: true if the value is found, false otherwise
    """
    return xs_int_list_index(lst, value) > -1


def _xs_int_list_compare_elem(a: int32 = int32(-1), b: int32 = int32(-1), reverse: bool = False) -> bool:
    if reverse:
        return a > b
    return a < b


def _xs_int_list_sift_down(lst: int32 = int32(-1), start: int32 = int32(-1), end: int32 = int32(-1), reverse: bool = False) -> None:
    root: int32 = start
    while True:
        child: int32 = 2 * root
        if child > end:
            return
        child_val: int32 = xs_array_get_int(lst, child)
        if child + 1 <= end:
            child_val1: int32 = xs_array_get_int(lst, child + 1)
            if _xs_int_list_compare_elem(child_val, child_val1, reverse):
                child += 1
                child_val = child_val1
        root_val: int32 = xs_array_get_int(lst, root)
        if _xs_int_list_compare_elem(root_val, child_val, reverse):
            xs_array_set_int(lst, root, child_val)
            xs_array_set_int(lst, child, root_val)
            root = child
        else:
            return


def xs_int_list_sort(lst: int32 = int32(-1), reverse: bool = False) -> None:
    """
    Sorts the list in-place using heapsort.
    :param lst: list id
    :param reverse: if true, sorts in descending order
    """
    size: int32 = xs_array_get_int(lst, 0)
    for start in i32range(size // 2, 0, -1):
        _xs_int_list_sift_down(lst, start, size, reverse)

    for end in i32range(size, 1, -1):
        temp: int32 = xs_array_get_int(lst, 1)
        xs_array_set_int(lst, 1, xs_array_get_int(lst, end))
        xs_array_set_int(lst, end, temp)
        _xs_int_list_sift_down(lst, int32(1), end - 1, reverse)


def _xs_int_list_ensure_sort_buffers(keys_size: int32 = int32(0), values_size: int32 = int32(0)) -> int32:
    global _int_list_sort_keys, _int_list_sort_values
    if _int_list_sort_keys < 0:
        _int_list_sort_keys = xs_array_create_int(keys_size)
        if _int_list_sort_keys < 0:
            return c_int_list_generic_error
    if _int_list_sort_values < 0:
        _int_list_sort_values = xs_array_create_int(values_size)
        if _int_list_sort_values < 0:
            return c_int_list_generic_error
    r: int32 = int32(1)
    if xs_array_get_size(_int_list_sort_keys) < keys_size:
        r = xs_array_resize_int(_int_list_sort_keys, keys_size)
        if r != 1:
            return c_int_list_resize_failed_error
    if xs_array_get_size(_int_list_sort_values) < values_size:
        r = xs_array_resize_int(_int_list_sort_values, values_size)
        if r != 1:
            return c_int_list_resize_failed_error
    return c_int_list_success


def _xs_int_list_release_sort_buffers(release_buffers: bool = True) -> None:
    if not release_buffers:
        return
    if _int_list_sort_keys >= 0:
        xs_array_resize_int(_int_list_sort_keys, 0)
    if _int_list_sort_values >= 0:
        xs_array_resize_int(_int_list_sort_values, 0)


def _xs_int_list_insertion_sort_with(data: int32 = int32(-1), other: int32 = int32(-1), lo: int32 = int32(0),
                                     hi: int32 = int32(0), voff: int32 = int32(0), reverse: bool = False) -> None:
    for i in i32range(lo + 1, hi):
        key: int32 = xs_array_get_int(data, i)
        value: int32 = xs_array_get_int(other, i + voff)
        j: int32 = i - 1
        shifting: bool = True
        while shifting and j >= lo:
            prev: int32 = xs_array_get_int(data, j)
            if _xs_int_list_compare_elem(key, prev, reverse):
                xs_array_set_int(data, j + 1, prev)
                xs_array_set_int(other, j + 1 + voff, xs_array_get_int(other, j + voff))
                j -= 1
            else:
                shifting = False
        xs_array_set_int(data, j + 1, key)
        xs_array_set_int(other, j + 1 + voff, value)


def _xs_int_list_merge_with(src: int32 = int32(-1), src_other: int32 = int32(-1), dst: int32 = int32(-1),
                            dst_other: int32 = int32(-1), lo: int32 = int32(0), mid: int32 = int32(0),
                            hi: int32 = int32(0), voff: int32 = int32(0), reverse: bool = False) -> None:
    i: int32 = lo
    j: int32 = mid
    k: int32 = lo
    if i < mid and j < hi:
        left: int32 = xs_array_get_int(src, i)
        right: int32 = xs_array_get_int(src, j)
        while i < mid and j < hi:
            if _xs_int_list_compare_elem(right, left, reverse):
                xs_array_set_int(dst, k, right)
                xs_array_set_int(dst_other, k + voff, xs_array_get_int(src_other, j + voff))
                j += 1
                if j < hi:
                    right = xs_array_get_int(src, j)
            else:
                xs_array_set_int(dst, k, left)
                xs_array_set_int(dst_other, k + voff, xs_array_get_int(src_other, i + voff))
                i += 1
                if i < mid:
                    left = xs_array_get_int(src, i)
            k += 1
    while i < mid:
        xs_array_set_int(dst, k, xs_array_get_int(src, i))
        xs_array_set_int(dst_other, k + voff, xs_array_get_int(src_other, i + voff))
        i += 1
        k += 1
    while j < hi:
        xs_array_set_int(dst, k, xs_array_get_int(src, j))
        xs_array_set_int(dst_other, k + voff, xs_array_get_int(src_other, j + voff))
        j += 1
        k += 1


def xs_int_list_sort_with(lst: int32 = int32(-1), other: int32 = int32(-1), reverse: bool = False, release_buffers: bool = True) -> int32:
    """
    Sorts the list in-place using a stable merge sort, and moves the elements of `other` the same way,
    so `other[i]` stays paired with `lst[i]`. Equal elements keep their original order.
    Inputs larger than 16 elements use two internal buffer arrays shared by all calls.
    :param lst: list id
    :param other: int list id of the same size as `lst`
    :param reverse: if true, sorts in descending order
    :param release_buffers: if true, resizes the internal buffers to 0 after sorting to free their memory;
        the same buffers are grown again on the next call
    :return: `c_int_list_success` on success, `c_int_list_generic_error` if the sizes differ or buffers
        can't be created, or `c_int_list_resize_failed_error` if the buffers can't grow
    """
    size: int32 = xs_array_get_int(lst, 0)
    data: int32 = lst
    start: int32 = int32(1)
    end: int32 = size + 1
    voff: int32 = int32(0)
    if xs_array_get_int(other, 0) != size:
        return c_int_list_generic_error
    run: int32 = int32(16)
    if size > run:
        r: int32 = _xs_int_list_ensure_sort_buffers(end, end + voff)
        if r != c_int_list_success:
            _xs_int_list_release_sort_buffers(release_buffers)
            return r
    run_start: int32 = start
    while run_start < end:
        run_end: int32 = run_start + run
        if run_end > end:
            run_end = end
        _xs_int_list_insertion_sort_with(data, other, run_start, run_end, voff, reverse)
        run_start = run_end
    if size <= run:
        return c_int_list_success
    src: int32 = data
    src_other: int32 = other
    dst: int32 = _int_list_sort_keys
    dst_other: int32 = _int_list_sort_values
    in_buffers: bool = False
    width: int32 = run
    while width < size:
        lo: int32 = start
        while lo < end:
            mid: int32 = lo + width
            if mid > end:
                mid = end
            hi: int32 = mid + width
            if hi > end:
                hi = end
            _xs_int_list_merge_with(src, src_other, dst, dst_other, lo, mid, hi, voff, reverse)
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
            xs_array_set_int(data, i, xs_array_get_int(src, i))
            xs_array_set_int(other, i + voff, xs_array_get_int(src_other, i + voff))
    _xs_int_list_release_sort_buffers(release_buffers)
    return c_int_list_success


def xs_int_list_to_string(lst: int32 = int32(-1), start: str = "[", sep: str = ", ", end: str = "]") -> str:
    """
    Returns a string representation of the list, by default in the format `[v0, v1, ...]`.
    :param lst: list id
    :param start: string prepended to the output
    :param sep: separator between elements
    :param end: string appended to the output
    :return: string representation of the list
    """
    size: int32 = xs_array_get_int(lst, 0)
    s: str = start
    for i in i32range(1, size + 1):
        s += str(xs_array_get_int(lst, i))
        if i < size:
            s += sep
    s += end
    return s


def xs_int_list_copy(lst: int32 = int32(-1), start: int32 = int32(0), end: int32 = c_int_list_max_capacity) -> int32:
    """
    Returns a copy of the list, optionally sliced by [start, end). Negative start/end are relative to the end.
    :param lst: list id
    :param start: start of slice (inclusive)
    :param end: end of slice (exclusive), defaults to list size
    :return: new list id, or `c_int_list_generic_error` on error
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
    new_lst: int32 = xs_array_create_int(new_size + 1)
    if new_lst < 0:
        return c_int_list_generic_error
    for i in i32range(fr, to):
        xs_array_set_int(new_lst, i - fr + 1, xs_array_get_int(lst, i + 1))
    xs_array_set_int(new_lst, 0, new_size)
    return new_lst


def xs_int_list_extend(source: int32 = int32(-1), lst: int32 = int32(-1)) -> int32:
    """
    Appends all elements from another list to the source list.
    :param source: list id to extend
    :param lst: list id whose elements are appended
    :return: `c_int_list_success` on success, or error if negative
    """
    source_size: int32 = xs_array_get_int(source, 0)
    to_add: int32 = xs_array_get_int(lst, 0)
    capacity: int32 = xs_array_get_size(source)
    new_size: int32 = source_size + to_add
    if new_size + 1 > capacity:
        if new_size >= c_int_list_max_capacity:
            return c_int_list_max_capacity_error
        r: int32 = xs_array_resize_int(source, new_size + 1)
        if r != 1:
            return c_int_list_resize_failed_error
    for i in i32range(1, to_add + 1):
        xs_array_set_int(source, i + source_size, xs_array_get_int(lst, i))
    xs_array_set_int(source, 0, new_size)
    return c_int_list_success


def xs_int_list_extend_with_array(source: int32 = int32(-1), arr: int32 = int32(-1)) -> int32:
    """
    Appends all elements from an XS array to the source list.
    :param source: list id to extend
    :param arr: XS array id whose elements are appended
    :return: `c_int_list_success` on success, or error if negative
    """
    source_size: int32 = xs_array_get_int(source, 0)
    to_add: int32 = xs_array_get_size(arr)
    capacity: int32 = xs_array_get_size(source)
    new_size: int32 = source_size + to_add
    if new_size + 1 > capacity:
        if new_size >= c_int_list_max_capacity or new_size < 0:
            return c_int_list_max_capacity_error
        r: int32 = xs_array_resize_int(source, new_size + 1)
        if r != 1:
            return c_int_list_resize_failed_error
    for i in i32range(0, to_add):
        xs_array_set_int(source, i + source_size + 1, xs_array_get_int(arr, i))
    xs_array_set_int(source, 0, new_size)
    return c_int_list_success


def xs_int_list_clear(lst: int32 = int32(-1)) -> int32:
    """
    Removes all elements from the list and shrinks the backing array.
    :param lst: list id
    :return: `c_int_list_success` on success, or error if negative
    """
    capacity: int32 = xs_array_get_size(lst)
    if capacity > 8:
        r: int32 = xs_array_resize_int(lst, 8)
        if r != 1:
            return c_int_list_resize_failed_error
    xs_array_set_int(lst, 0, 0)
    return c_int_list_success


def xs_int_list_delete(lst: int32 = int32(-1)) -> int32:
    """
    Resizes all arrays of the list to 0 to free their memory. XS can't fully delete arrays,
    so the list id stays allocated and must not be used afterwards.
    :param lst: list id
    :return: `c_int_list_success` on success, or `c_int_list_resize_failed_error` if any resize fails
    """
    r: int32 = xs_array_resize_int(lst, 0)
    if r != 1:
        return c_int_list_resize_failed_error
    return c_int_list_success


def xs_int_list_compare(lst1: int32 = int32(-1), lst2: int32 = int32(-1)) -> int32:
    """
    Performs lexicographic comparison of two lists.
    :param lst1: first list id
    :param lst2: second list id
    :return: -1 if lst1 < lst2, 1 if lst1 > lst2, 0 if equal
    """
    size1: int32 = xs_array_get_int(lst1, 0)
    size2: int32 = xs_array_get_int(lst2, 0)
    i: int32 = int32(1)
    while i <= size1 and i <= size2:
        v1: int32 = xs_array_get_int(lst1, i)
        v2: int32 = xs_array_get_int(lst2, i)
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


def xs_int_list_reverse(lst: int32 = int32(-1)) -> None:
    """
    Reverses the list in-place.
    :param lst: list id
    """
    size: int32 = xs_array_get_int(lst, 0)
    mid: int32 = (size + 2) // 2
    for i in i32range(1, mid):
        temp: int32 = xs_array_get_int(lst, i)
        back_i: int32 = size - i + 1
        xs_array_set_int(lst, i, xs_array_get_int(lst, back_i))
        xs_array_set_int(lst, back_i, temp)


def xs_int_list_count(lst: int32 = int32(-1), value: int32 = int32(-1)) -> int32:
    """
    Counts the number of occurrences of a value in the list.
    :param lst: list id
    :param value: value to count
    :return: number of occurrences
    """
    count: int32 = int32(0)
    size: int32 = xs_array_get_int(lst, 0)
    for i in i32range(1, size + 1):
        if xs_array_get_int(lst, i) == value:
            count += 1
    return count


def xs_int_list_sum(lst: int32 = int32(-1)) -> int32:
    """
    Returns the sum of all elements in the list.
    :param lst: list id
    :return: sum of elements
    """
    s: int32 = int32(0)
    size: int32 = xs_array_get_int(lst, 0)
    for i in i32range(1, size + 1):
        s += xs_array_get_int(lst, i)
    return s


def xs_int_list_min(lst: int32 = int32(-1)) -> int32:
    """
    Returns the minimum value in the list. Sets last error on failure.
    :param lst: list id
    :return: minimum value, or `c_int_list_generic_error` on error
    """
    global _int_list_last_operation_status
    size: int32 = xs_array_get_int(lst, 0)
    if size == 0:
        _int_list_last_operation_status = c_int_list_index_out_of_range_error
        return c_int_list_generic_error
    m: int32 = xs_array_get_int(lst, 1)
    if size == 1:
        _int_list_last_operation_status = c_int_list_success
        return m
    for i in i32range(2, size + 1):
        v: int32 = xs_array_get_int(lst, i)
        if v < m:
            m = v
    _int_list_last_operation_status = c_int_list_success
    return m


def xs_int_list_max(lst: int32 = int32(-1)) -> int32:
    """
    Returns the maximum value in the list. Sets last error on failure.
    :param lst: list id
    :return: maximum value, or `c_int_list_generic_error` on error
    """
    global _int_list_last_operation_status
    size: int32 = xs_array_get_int(lst, 0)
    if size == 0:
        _int_list_last_operation_status = c_int_list_index_out_of_range_error
        return c_int_list_generic_error
    m: int32 = xs_array_get_int(lst, 1)
    if size == 1:
        _int_list_last_operation_status = c_int_list_success
        return m
    for i in i32range(2, size + 1):
        v: int32 = xs_array_get_int(lst, i)
        if v > m:
            m = v
    _int_list_last_operation_status = c_int_list_success
    return m


def xs_int_list_last_error() -> int32:
    """
    Returns the status code of the last operation that sets it (get, pop, min, max).
    :return: `c_int_list_success` if the last such operation succeeded, or a negative error code
    """
    return _int_list_last_operation_status


def xs_int_list_from_string(items: str = "") -> int32:
    """
    Creates a list from a comma separated string, e.g. `"1,2,3"`.
    Items are trimmed, and items that cannot be parsed are skipped.
    :param items: comma separated values
    :return: created list id, or `c_int_list_generic_error` on error
    """
    if str_trim(items) == "":
        return xs_int_list_create()
    parts: int32 = str_split(items, ",")
    num_parts: int32 = xs_array_get_size(parts)
    lst: int32 = xs_int_list_create(num_parts)
    if lst < 0:
        xs_array_resize_string(parts, 0)
        return c_int_list_generic_error
    for i in i32range(0, num_parts):
        item: str = str_trim(xs_array_get_string(parts, i))
        value: int32 = str_to_int(item, 10, c_int_list_empty_param)
        if value != c_int_list_empty_param:
            xs_int_list_append(lst, value)
    xs_array_resize_string(parts, 0)
    return lst
