from numpy import int32

from xs_converter.functions import xs_array_get_size, xs_array_get_int, xs_array_create_bool, \
    xs_array_create_int, xs_array_set_bool, xs_array_set_int, xs_array_get_bool, xs_array_resize_bool
from xs_converter.symbols import XsExternConst, i32range

c_bool_list_success: XsExternConst[int32] = int32(0)
c_bool_list_generic_error: XsExternConst[int32] = int32(-1)
c_bool_list_index_out_of_range_error: XsExternConst[int32] = int32(-2)
c_bool_list_resize_failed_error: XsExternConst[int32] = int32(-3)
c_bool_list_max_capacity_error: XsExternConst[int32] = int32(-4)
c_bool_list_max_capacity: XsExternConst[int32] = int32(999999999)
c_bool_list_empty_int_param: XsExternConst[int32] = int32(-999999999)
_bool_list_last_operation_status: int32 = c_bool_list_success


def _xs_bool_list_bool_to_string(value: bool = False) -> str:
    if value:
        return "true"
    return "false"


def xs_bool_list_size(lst: int32 = int32(-1)) -> int32:
    """
    Returns the number of elements in the list.
    :param lst: list id
    :return: list size
    """
    return xs_array_get_int(lst, 0)


def xs_bool_list_create(capacity: int32 = int32(7)) -> int32:
    """
    Creates empty list for bool values. List is a dynamic array that grows and shrinks as values are added and removed.
    :param capacity: initial list capacity
    :return: created list id, or `c_bool_list_generic_error` on error
    """
    if capacity < 0 or capacity >= c_bool_list_max_capacity:
        return c_bool_list_generic_error
    lst: int32 = xs_array_create_int(2, 0)
    bool_lst: int32 = xs_array_create_bool(capacity)
    if lst < 0 or bool_lst < 0:
        return c_bool_list_generic_error
    xs_array_set_int(lst, 1, bool_lst)
    return lst


def xs_bool_list_from_repeated_val(value: bool = False, times: int32 = int32(0)) -> int32:
    """
    Creates a list by repeating a single value.
    :param value: value to repeat
    :param times: number of times to repeat the value
    :return: created list id, or `c_bool_list_generic_error` on error
    """
    if times < 0 or times > c_bool_list_max_capacity:
        return c_bool_list_generic_error
    lst: int32 = xs_array_create_int(2, times)
    bool_lst: int32 = xs_array_create_bool(times, value)
    if bool_lst < 0 or lst < 0:
        return c_bool_list_generic_error
    xs_array_set_int(lst, 1, bool_lst)
    return lst


def xs_bool_list_from_repeated_list(lst: int32 = int32(-1), times: int32 = int32(0)) -> int32:
    """
    Creates a new list by repeating all elements of the given list.
    :param lst: source list id
    :param times: number of times to repeat the list contents
    :return: created list id, or `c_bool_list_generic_error` on error
    """
    if times < 0:
        return c_bool_list_generic_error
    size: int32 = xs_array_get_int(lst, 0)
    if times > 0 and size > (c_bool_list_max_capacity // times):
        return c_bool_list_max_capacity_error
    new_capacity: int32 = size * times
    if new_capacity > c_bool_list_max_capacity:
        return c_bool_list_max_capacity_error
    new_bool_lst: int32 = xs_array_create_bool(new_capacity)
    new_lst: int32 = xs_array_create_int(2, new_capacity)
    if new_bool_lst < 0 or new_lst < 0:
        return c_bool_list_generic_error
    bool_lst: int32 = xs_array_get_int(lst, 1)
    for i in i32range(0, size):
        val: bool = xs_array_get_bool(bool_lst, i)
        j: int32 = i
        while j < new_capacity:
            xs_array_set_bool(new_bool_lst, j, val)
            j += size
    xs_array_set_int(new_lst, 1, new_bool_lst)
    return new_lst


def xs_bool_list_from_array(arr: int32 = int32(-1)) -> int32:
    """
    Creates a new list by copying elements from an XS array.
    :param arr: source XS array id
    :return: created list id, or `c_bool_list_generic_error` on error
    """
    arr_size: int32 = xs_array_get_size(arr)
    if arr_size > c_bool_list_max_capacity:
        return c_bool_list_max_capacity_error
    new_bool_lst: int32 = xs_array_create_bool(arr_size)
    lst: int32 = xs_array_create_int(2, arr_size)
    if lst < 0 or new_bool_lst < 0:
        return c_bool_list_generic_error
    for i in i32range(0, arr_size):
        xs_array_set_bool(new_bool_lst, i, xs_array_get_bool(arr, i))
    xs_array_set_int(lst, 1, new_bool_lst)
    return lst


def xs_bool_list_use_array_as_source(arr: int32 = int32(-1)) -> int32:
    """
    Wraps an existing XS bool array as a list without copying elements.
    :param arr: XS bool array id to use as backing storage
    :return: list id, or `c_bool_list_max_capacity_error`/`c_bool_list_generic_error` on error
    """
    arr_size: int32 = xs_array_get_size(arr)
    if arr_size > c_bool_list_max_capacity:
        return c_bool_list_max_capacity_error
    lst: int32 = xs_array_create_int(2, arr_size)
    if lst < 0:
        return c_bool_list_generic_error
    xs_array_set_int(lst, 1, arr)
    return lst


def xs_bool_list_get(lst: int32 = int32(-1), idx: int32 = int32(-1)) -> bool:
    """
    Returns the element at the given index. Sets last error on failure.
    :param lst: list id
    :param idx: zero-based index
    :return: value at index, or `false` on error
    """
    global _bool_list_last_operation_status
    size: int32 = xs_bool_list_size(lst)
    if idx < 0 or idx >= size:
        _bool_list_last_operation_status = c_bool_list_index_out_of_range_error
        return False
    _bool_list_last_operation_status = c_bool_list_success
    return xs_array_get_bool(xs_array_get_int(lst, 1), idx)


def xs_bool_list_set(lst: int32 = int32(-1), idx: int32 = int32(-1), value: bool = False) -> int32:
    """
    Sets the element at the given index to a new value.
    :param lst: list id
    :param idx: zero-based index
    :param value: new value to set
    :return: `c_bool_list_success` on success, or error if negative
    """
    size: int32 = xs_array_get_int(lst, 0)
    if idx < 0 or idx >= size:
        return c_bool_list_index_out_of_range_error
    xs_array_set_bool(xs_array_get_int(lst, 1), idx, value)
    return c_bool_list_success


def _xs_bool_list_extend_bool_array(lst: int32 = int32(-1), capacity: int32 = int32(0)) -> int32:
    if capacity >= c_bool_list_max_capacity:
        return c_bool_list_max_capacity_error
    new_capacity: int32 = int32(0)
    if capacity > c_bool_list_max_capacity // 2:
        new_capacity = c_bool_list_max_capacity
    else:
        new_capacity = capacity * 2
    if new_capacity > c_bool_list_max_capacity:
        new_capacity = c_bool_list_max_capacity
    elif new_capacity == 0:
        new_capacity = int32(8)
    r: int32 = xs_array_resize_bool(lst, new_capacity)
    if r != 1:
        return c_bool_list_resize_failed_error
    return c_bool_list_success


def _xs_bool_list_shrink_bool_array(lst: int32 = int32(-1), size: int32 = int32(0),
                                    capacity: int32 = int32(0)) -> int32:
    if size <= (capacity // 2):
        r: int32 = xs_array_resize_bool(lst, capacity // 2)
        if r != 1:
            return c_bool_list_resize_failed_error
    return c_bool_list_success


def xs_bool_list_append(lst: int32 = int32(-1), value: bool = False) -> int32:
    """
    Appends a value to the end of the list, growing the backing array if needed.
    :param lst: list id
    :param value: value to append
    :return: `c_bool_list_success` on success, or error if negative
    """
    bool_lst: int32 = xs_array_get_int(lst, 1)
    capacity: int32 = xs_array_get_size(bool_lst)
    size: int32 = xs_array_get_int(lst, 0)
    if capacity <= size:
        r: int32 = _xs_bool_list_extend_bool_array(bool_lst, capacity)
        if r != c_bool_list_success:
            return r
    xs_array_set_bool(bool_lst, size, value)
    xs_array_set_int(lst, 0, size + 1)
    return c_bool_list_success


def xs_bool_list_insert(lst: int32 = int32(-1), idx: int32 = int32(-1), value: bool = False) -> int32:
    """
    Inserts a value at the given index, shifting subsequent elements to the right.
    :param lst: list id
    :param idx: zero-based index at which to insert
    :param value: value to insert
    :return: `c_bool_list_success` on success, or error if negative
    """
    size: int32 = xs_array_get_int(lst, 0)
    if idx < 0 or idx > size:
        return c_bool_list_index_out_of_range_error
    new_size: int32 = size + 1
    bool_lst: int32 = xs_array_get_int(lst, 1)
    capacity: int32 = xs_array_get_size(bool_lst)
    if capacity < new_size:
        r: int32 = _xs_bool_list_extend_bool_array(bool_lst, capacity)
        if r != c_bool_list_success:
            return r
    for i in i32range(size, idx, -1):
        xs_array_set_bool(bool_lst, i, xs_array_get_bool(bool_lst, i - 1))
    xs_array_set_bool(bool_lst, idx, value)
    xs_array_set_int(lst, 0, new_size)
    return c_bool_list_success


def xs_bool_list_pop(lst: int32 = int32(-1), idx: int32 = c_bool_list_max_capacity) -> bool:
    """
    Removes and returns the element at the given index, shifting subsequent elements to the left.
    Defaults to the last element. Sets last error on failure.
    :param lst: list id
    :param idx: zero-based index of element to remove (defaults to last)
    :return: removed value, or `false` on error
    """
    global _bool_list_last_operation_status
    bool_lst: int32 = xs_array_get_int(lst, 1)
    capacity: int32 = xs_array_get_size(bool_lst)
    size: int32 = xs_array_get_int(lst, 0)
    if idx == c_bool_list_max_capacity:
        idx = size - 1
    if idx < 0 or idx >= size:
        _bool_list_last_operation_status = c_bool_list_index_out_of_range_error
        return False
    removed_elem: bool = xs_array_get_bool(bool_lst, idx)
    for i in i32range(idx, size - 1):
        xs_array_set_bool(bool_lst, i, xs_array_get_bool(bool_lst, i + 1))
    xs_array_set_int(lst, 0, size - 1)
    r: int32 = _xs_bool_list_shrink_bool_array(bool_lst, size, capacity)
    if r != c_bool_list_success:
        _bool_list_last_operation_status = r
        return False
    _bool_list_last_operation_status = c_bool_list_success
    return removed_elem


def xs_bool_list_remove(lst: int32 = int32(-1), value: bool = False) -> int32:
    """
    Removes the first occurrence of the given value from the list.
    :param lst: list id
    :param value: value to remove
    :return: index of the removed element, or `c_bool_list_generic_error` if not found
    """
    bool_lst: int32 = xs_array_get_int(lst, 1)
    size: int32 = xs_array_get_int(lst, 0)
    found_idx: int32 = int32(-1)
    i: int32 = int32(0)
    while i < size and found_idx == -1:
        c_val: bool = xs_array_get_bool(bool_lst, i)
        if c_val == value:
            found_idx = i
        i += 1
    if found_idx == -1:
        return c_bool_list_generic_error
    new_size: int32 = size - 1
    for j in i32range(found_idx, new_size):
        xs_array_set_bool(bool_lst, j, xs_array_get_bool(bool_lst, j + 1))
    xs_array_set_int(lst, 0, new_size)
    capacity: int32 = xs_array_get_size(bool_lst)
    r: int32 = _xs_bool_list_shrink_bool_array(bool_lst, size, capacity)
    if r != c_bool_list_success:
        return r
    return found_idx


def xs_bool_list_index(lst: int32 = int32(-1), value: bool = False, start: int32 = int32(0),
                       stop: int32 = c_bool_list_empty_int_param) -> int32:
    """
    Returns the index of the first occurrence of the value within the optional [start, stop) range. Negative start/stop are relative to the end.
    :param lst: list id
    :param value: value to search for
    :param start: start of search range (inclusive)
    :param stop: end of search range (exclusive), defaults to list size
    :return: index of the value, or `c_bool_list_generic_error` if not found
    """
    size: int32 = xs_array_get_int(lst, 0)
    bool_lst: int32 = xs_array_get_int(lst, 1)

    if stop == c_bool_list_empty_int_param or stop > size:
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
        if xs_array_get_bool(bool_lst, i) == value:
            return i
    return c_bool_list_generic_error


def xs_bool_list_contains(lst: int32 = int32(-1), value: bool = False) -> bool:
    """
    Checks whether the list contains the given value.
    :param lst: list id
    :param value: value to search for
    :return: true if the value is found, false otherwise
    """
    return xs_bool_list_index(lst, value) > -1


def _xs_bool_list_compare_elem(a: bool = False, b: bool = False, reverse: bool = False) -> bool:
    if reverse:
        return a and (not b)
    return (not a) and b


def _xs_bool_list_sift_down(lst: int32 = int32(-1), start: int32 = int32(-1), end: int32 = int32(-1),
                            reverse: bool = False) -> None:
    root: int32 = start
    while True:
        child: int32 = 2 * root + 1
        if child > end:
            return
        child_val: bool = xs_array_get_bool(lst, child)
        if child + 1 <= end:
            child_val1: bool = xs_array_get_bool(lst, child + 1)
            if _xs_bool_list_compare_elem(child_val, child_val1, reverse):
                child += 1
                child_val = child_val1
        root_val: bool = xs_array_get_bool(lst, root)
        if _xs_bool_list_compare_elem(root_val, child_val, reverse):
            xs_array_set_bool(lst, root, child_val)
            xs_array_set_bool(lst, child, root_val)
            root = child
        else:
            return


def xs_bool_list_sort(lst: int32 = int32(-1), reverse: bool = False) -> None:
    """
    Sorts the list in-place using heapsort.
    :param lst: list id
    :param reverse: if true, sorts in descending order
    """
    size: int32 = xs_array_get_int(lst, 0)
    bool_lst: int32 = xs_array_get_int(lst, 1)
    for start in i32range(size // 2 - 1, -1, -1):
        _xs_bool_list_sift_down(bool_lst, start, size - 1, reverse)

    for end in i32range(size - 1, 0, -1):
        temp: bool = xs_array_get_bool(bool_lst, 0)
        xs_array_set_bool(bool_lst, 0, xs_array_get_bool(bool_lst, end))
        xs_array_set_bool(bool_lst, end, temp)
        _xs_bool_list_sift_down(bool_lst, int32(0), end - 1, reverse)


def xs_bool_list_to_string(lst: int32 = int32(-1)) -> str:
    """
    Returns a string representation of the list in the format `[true, false, ...]`.
    :param lst: list id
    :return: string representation of the list
    """
    size: int32 = xs_array_get_int(lst, 0)
    bool_lst: int32 = xs_array_get_int(lst, 1)
    if size == 0:
        return "[]"
    s: str = "["
    for i in i32range(0, size):
        s += _xs_bool_list_bool_to_string(xs_array_get_bool(bool_lst, i))
        if i < size - 1:
            s += ", "
    s += "]"
    return s


def xs_bool_list_copy(lst: int32 = int32(-1), start: int32 = int32(0),
                      end: int32 = c_bool_list_max_capacity) -> int32:
    """
    Returns a copy of the list, optionally sliced by [start, end). Negative start/end are relative to the end.
    :param lst: list id
    :param start: start of slice (inclusive)
    :param end: end of slice (exclusive), defaults to list size
    :return: new list id, or `c_bool_list_generic_error` on error
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
    new_bool_lst: int32 = xs_array_create_bool(new_size)
    if new_lst < 0 or new_bool_lst < 0:
        return c_bool_list_generic_error
    xs_array_set_int(new_lst, 1, new_bool_lst)
    bool_lst: int32 = xs_array_get_int(lst, 1)
    for i in i32range(fr, to):
        xs_array_set_bool(new_bool_lst, i - fr, xs_array_get_bool(bool_lst, i))

    return new_lst


def xs_bool_list_extend(source: int32 = int32(-1), lst: int32 = int32(-1)) -> int32:
    """
    Appends all elements from another list to the source list.
    :param source: list id to extend
    :param lst: list id whose elements are appended
    :return: `c_bool_list_success` on success, or error if negative
    """
    source_size: int32 = xs_array_get_int(source, 0)
    to_add: int32 = xs_array_get_int(lst, 0)
    bool_source: int32 = xs_array_get_int(source, 1)
    capacity: int32 = xs_array_get_size(bool_source)
    new_size: int32 = source_size + to_add
    if new_size > capacity:
        if new_size > c_bool_list_max_capacity:
            return c_bool_list_max_capacity_error
        r: int32 = xs_array_resize_bool(bool_source, new_size)
        if r != 1:
            return c_bool_list_resize_failed_error
    bool_list: int32 = xs_array_get_int(lst, 1)
    for i in i32range(0, to_add):
        xs_array_set_bool(bool_source, i + source_size, xs_array_get_bool(bool_list, i))
    xs_array_set_int(source, 0, new_size)
    return c_bool_list_success


def xs_bool_list_extend_with_array(source: int32 = int32(-1), arr: int32 = int32(-1)) -> int32:
    """
    Appends all elements from a raw XS bool array to the source list.
    :param source: list id to extend
    :param arr: raw XS bool array id whose elements are appended
    :return: `c_bool_list_success` on success, or error if negative
    """
    source_size: int32 = xs_array_get_int(source, 0)
    to_add: int32 = xs_array_get_size(arr)
    bool_source: int32 = xs_array_get_int(source, 1)
    capacity: int32 = xs_array_get_size(bool_source)
    new_size: int32 = source_size + to_add
    if new_size > capacity:
        if new_size > c_bool_list_max_capacity or new_size < 0:
            return c_bool_list_max_capacity_error
        r: int32 = xs_array_resize_bool(bool_source, new_size)
        if r != 1:
            return c_bool_list_resize_failed_error
    for i in i32range(0, to_add):
        xs_array_set_bool(bool_source, i + source_size, xs_array_get_bool(arr, i))
    xs_array_set_int(source, 0, new_size)
    return c_bool_list_success


def xs_bool_list_clear(lst: int32 = int32(-1)) -> int32:
    """
    Removes all elements from the list and shrinks the backing array.
    :param lst: list id
    :return: `c_bool_list_success` on success, or error if negative
    """
    bool_list: int32 = xs_array_get_int(lst, 1)
    capacity: int32 = xs_array_get_size(bool_list)
    if capacity > 8:
        r: int32 = xs_array_resize_bool(bool_list, 8)
        if r != 1:
            return c_bool_list_resize_failed_error
    xs_array_set_int(lst, 0, 0)
    return c_bool_list_success


def xs_bool_list_compare(lst1: int32 = int32(-1), lst2: int32 = int32(-1)) -> int32:
    """
    Performs lexicographic comparison of two lists.
    :param lst1: first list id
    :param lst2: second list id
    :return: -1 if lst1 < lst2, 1 if lst1 > lst2, 0 if equal
    """
    size1: int32 = xs_array_get_int(lst1, 0)
    size2: int32 = xs_array_get_int(lst2, 0)
    bool_list1: int32 = xs_array_get_int(lst1, 1)
    bool_list2: int32 = xs_array_get_int(lst2, 1)
    i: int32 = int32(0)
    while i < size1 and i < size2:
        v1: bool = xs_array_get_bool(bool_list1, i)
        v2: bool = xs_array_get_bool(bool_list2, i)
        if (not v1) and v2:
            return int32(-1)
        if v1 and (not v2):
            return int32(1)
        i += 1
    if size1 < size2:
        return int32(-1)
    if size1 > size2:
        return int32(1)
    return int32(0)


def xs_bool_list_reverse(lst: int32 = int32(-1)) -> None:
    """
    Reverses the list in-place.
    :param lst: list id
    """
    size: int32 = xs_array_get_int(lst, 0)
    bool_list: int32 = xs_array_get_int(lst, 1)
    mid: int32 = size // 2
    for i in i32range(0, mid):
        temp: bool = xs_array_get_bool(bool_list, i)
        back_i: int32 = size - i - 1
        xs_array_set_bool(bool_list, i, xs_array_get_bool(bool_list, back_i))
        xs_array_set_bool(bool_list, back_i, temp)


def xs_bool_list_count(lst: int32 = int32(-1), value: bool = False) -> int32:
    """
    Counts the number of occurrences of a value in the list.
    :param lst: list id
    :param value: value to count
    :return: number of occurrences
    """
    count: int32 = int32(0)
    size: int32 = xs_array_get_int(lst, 0)
    bool_list: int32 = xs_array_get_int(lst, 1)
    for i in i32range(0, size):
        if xs_array_get_bool(bool_list, i) == value:
            count += 1
    return count


def xs_bool_list_last_error() -> int32:
    """
    Returns the status code of the last operation that sets it (get, pop).
    :return: `c_bool_list_success` if the last such operation succeeded, or a negative error code
    """
    return _bool_list_last_operation_status
