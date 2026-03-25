from numpy import int32, float32

from xs_converter.functions import xs_array_create_vector, xs_array_set_vector, xs_array_resize_vector, \
    xs_array_get_vector, xs_array_get_size, bit_cast_to_float, bit_cast_to_int, vector, xs_vector_get_x, \
    xs_vector_set, xs_array_set_float, xs_vector_get_y, xs_vector_get_z, xs_array_get_float, xs_array_resize_float, \
    xs_array_create_float
from xs_converter.symbols import XsExternConst, i32range, XsVector

c_vector_list_success: XsExternConst[int32] = int32(0)
c_vector_list_generic_error: XsExternConst[int32] = int32(-1)
c_vector_list_generic_error_vector: XsExternConst[XsVector] = vector(-1.0, -1.0, -1.0)
c_vector_list_index_out_of_range_error: XsExternConst[int32] = int32(-2)
c_vector_list_resize_failed_error: XsExternConst[int32] = int32(-3)
c_vector_list_max_capacity_error: XsExternConst[int32] = int32(-4)
c_vector_list_max_capacity: XsExternConst[int32] = int32(333333333) # int32(999999999)
c_vector_list_empty_param: XsExternConst[XsVector] = vector(-9999999.0, -9999999.0, -9999999.0)
c_vector_list_empty_int_param: XsExternConst[int32] = int32(-999999999)
_vector_list_last_operation_status: int32 = c_vector_list_success


def _xs_vector_list_arr_create(size: int32 = int32(0), value: XsVector = vector(0.0, 0.0, 0.0)) -> int32:
    # return xs_array_create_vector(size, value)
    x: float32 = xs_vector_get_x(value)
    y: float32 = xs_vector_get_y(value)
    z: float32 = xs_vector_get_z(value)
    size *= 3
    arr: int32 = xs_array_create_float(size, x)
    if x == y and x == z:
        return arr

    for i in i32range(1, size, 3):
        xs_array_set_float(arr, i, y)
        xs_array_set_float(arr, i + 1, z)
    return arr


def _xs_vector_list_arr_set(arr: int32 = int32(-1), idx: int32 = int32(0), value: XsVector = vector(0.0, 0.0, 0.0)) -> None:
    # xs_array_set_vector(arr, idx, value)
    idx *= 3
    xs_array_set_float(arr, idx, xs_vector_get_x(value))
    xs_array_set_float(arr, idx + 1, xs_vector_get_y(value))
    xs_array_set_float(arr, idx + 2, xs_vector_get_z(value))


def _xs_vector_list_arr_get(arr: int32 = int32(-1), idx: int32 = int32(0)) -> XsVector:
    # return xs_array_get_vector(arr, idx)
    idx *= 3
    x: float32 = xs_array_get_float(arr, idx)
    y: float32 = xs_array_get_float(arr, idx + 1)
    z: float32 = xs_array_get_float(arr, idx + 2)
    return xs_vector_set(x, y, z)


def _xs_vector_list_arr_resize(arr: int32 = int32(-1), size: int32 = int32(0)) -> int32:
    # return xs_array_resize_vector(arr, size)
    return xs_array_resize_float(arr, size * 3)


def _xs_vector_list_set_size(lst: int32 = int32(-1), size: int32 = int32(0)) -> None:
    # xs_array_set_vector(lst, 0, xs_vector_set(bit_cast_to_float(size), 0.0, 0.0))
    xs_array_set_float(lst, 0, bit_cast_to_float(size))


def xs_vector_list_capacity(arr: int32 = int32(-1)) -> int32:
    # return xs_array_get_size(arr)
    return xs_array_get_size(arr) // int32(3)


def xs_vector_list_size(lst: int32 = int32(-1)) -> int32:
    """
    Returns the number of elements in the list.
    :param lst: list id
    :return: list size
    """
    # return bit_cast_to_int(xs_vector_get_x(xs_array_get_vector(lst, 0)))
    return bit_cast_to_int(xs_array_get_float(lst, 0))


def xs_vector_list_create(capacity: int32 = int32(7)) -> int32:
    """
    Creates empty list for vector values. List is a dynamic array that grows and shrinks as values are added and removed.
    :param capacity: initial list capacity
    :return: created list id, or `c_vector_list_generic_error` on error
    """
    if capacity < 0 or capacity >= c_vector_list_max_capacity:
        return c_vector_list_generic_error
    lst: int32 = _xs_vector_list_arr_create(capacity + 1)
    if lst < 0:
        return c_vector_list_generic_error
    _xs_vector_list_set_size(lst, int32(0))
    return lst


def xs_vector_list(
        v0: XsVector = c_vector_list_empty_param,
        v1: XsVector = c_vector_list_empty_param,
        v2: XsVector = c_vector_list_empty_param,
        v3: XsVector = c_vector_list_empty_param,
        v4: XsVector = c_vector_list_empty_param,
        v5: XsVector = c_vector_list_empty_param,
        v6: XsVector = c_vector_list_empty_param,
        v7: XsVector = c_vector_list_empty_param,
        v8: XsVector = c_vector_list_empty_param,
        v9: XsVector = c_vector_list_empty_param,
        v10: XsVector = c_vector_list_empty_param,
        v11: XsVector = c_vector_list_empty_param,
) -> int32:
    """
    Creates a list with provided values. The first value that equals `c_vector_list_empty_param` will stop further insertion.
    This Function can create a list with 12 values at the maximum, but further values can be added with other functions.
    :param v0 through v11: value at a given index of a list
    :return: created list id, or `c_vector_list_generic_error` on error
    """
    lst: int32 = _xs_vector_list_arr_create(13)
    if lst < 0:
        return c_vector_list_generic_error
    if v0 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(0))
        return lst
    _xs_vector_list_arr_set(lst, 1, v0)
    if v1 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(1))
        return lst
    _xs_vector_list_arr_set(lst, 2, v1)
    if v2 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(2))
        return lst
    _xs_vector_list_arr_set(lst, 3, v2)
    if v3 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(3))
        return lst
    _xs_vector_list_arr_set(lst, 4, v3)
    if v4 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(4))
        return lst
    _xs_vector_list_arr_set(lst, 5, v4)
    if v5 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(5))
        return lst
    _xs_vector_list_arr_set(lst, 6, v5)
    if v6 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(6))
        return lst
    _xs_vector_list_arr_set(lst, 7, v6)
    if v7 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(7))
        return lst
    _xs_vector_list_arr_set(lst, 8, v7)
    if v8 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(8))
        return lst
    _xs_vector_list_arr_set(lst, 9, v8)
    if v9 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(9))
        return lst
    _xs_vector_list_arr_set(lst, 10, v9)
    if v10 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(10))
        return lst
    _xs_vector_list_arr_set(lst, 11, v10)
    if v11 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(11))
        return lst
    _xs_vector_list_arr_set(lst, 12, v11)
    _xs_vector_list_set_size(lst, int32(12))
    return lst


def xs_vector_list_from_repeated_val(value: XsVector = vector(0.0, 0.0, 0.0), times: int32 = int32(0)) -> int32:
    """
    Creates a list by repeating a single value.
    :param value: value to repeat
    :param times: number of times to repeat the value
    :return: created list id, or `c_vector_list_generic_error` on error
    """
    if times < 0 or times >= c_vector_list_max_capacity:
        return c_vector_list_generic_error
    lst: int32 = _xs_vector_list_arr_create(times + 1, value)
    if lst < 0:
        return c_vector_list_generic_error
    _xs_vector_list_set_size(lst, times)
    return lst


def xs_vector_list_from_repeated_list(lst: int32 = int32(-1), times: int32 = int32(0)) -> int32:
    """
    Creates a new list by repeating all elements of the given list.
    :param lst: source list id
    :param times: number of times to repeat the list contents
    :return: created list id, or `c_vector_list_generic_error` on error
    """
    if times < 0:
        return c_vector_list_generic_error
    size: int32 = xs_vector_list_size(lst)
    if times > 0 and size > (c_vector_list_max_capacity // times):
        return c_vector_list_max_capacity_error
    new_capacity: int32 = (size * times) + 1
    if new_capacity > c_vector_list_max_capacity:
        return c_vector_list_max_capacity_error
    new_lst: int32 = _xs_vector_list_arr_create(new_capacity)
    if new_lst < 0:
        return c_vector_list_generic_error
    for i in i32range(1, size + 1):
        val: XsVector = _xs_vector_list_arr_get(lst, i)
        j: int32 = i
        while j < new_capacity:
            _xs_vector_list_arr_set(new_lst, j, val)
            j += size
    _xs_vector_list_set_size(new_lst, new_capacity - 1)
    return new_lst


def xs_vector_list_from_array(arr: int32 = int32(-1)) -> int32:
    """
    Creates a new list by copying elements from an XS array.
    :param arr: source XS array id
    :return: created list id, or `c_vector_list_generic_error` on error
    """
    arr_size: int32 = xs_array_get_size(arr)
    lst: int32 = xs_vector_list_create(arr_size)
    if lst < 0:
        return lst
    for i in i32range(0, arr_size):
        _xs_vector_list_arr_set(lst, i + 1, xs_array_get_vector(arr, i))
    _xs_vector_list_set_size(lst, arr_size)
    return lst


# def xs_vector_list_use_array_as_source(arr: int32 = int32(-1)) -> int32:
#     """
#     Converts an existing XS array into a list in-place by shifting elements and storing the size.
#     :param arr: XS array id to convert
#     :return: list id (same as arr), or `c_vector_list_max_capacity_error`/`c_vector_list_resize_failed_error` on error
#     """
#     arr_size: int32 = xs_array_get_size(arr)
#     if arr_size + 1 > c_vector_list_max_capacity:
#         return c_vector_list_max_capacity_error
#     r: int32 = xs_array_resize_vector(arr, arr_size + 1)
#     if r < 0:
#         return c_vector_list_resize_failed_error
#     for i in i32range(arr_size - 1, -1, -1):
#         _xs_vector_list_arr_set(arr, i + 1, xs_array_get_vector(arr, i))
#     _xs_vector_list_set_size(arr, arr_size)
#     return arr


def xs_vector_list_get(lst: int32 = int32(-1), idx: int32 = int32(-1)) -> XsVector:
    """
    Returns the element at the given index. Sets last error on failure.
    :param lst: list id
    :param idx: zero-based index
    :return: value at index, or `c_vector_list_generic_error_vector` on error
    """
    global _vector_list_last_operation_status
    size: int32 = xs_vector_list_size(lst)
    if idx < 0 or idx >= size:
        _vector_list_last_operation_status = c_vector_list_index_out_of_range_error
        return c_vector_list_generic_error_vector
    _vector_list_last_operation_status = c_vector_list_success
    return _xs_vector_list_arr_get(lst, idx + 1)


def xs_vector_list_set(lst: int32 = int32(-1), idx: int32 = int32(-1),
                       value: XsVector = vector(0.0, 0.0, 0.0)) -> int32:
    """
    Sets the element at the given index to a new value.
    :param lst: list id
    :param idx: zero-based index
    :param value: new value to set
    :return: `c_vector_list_success` on success, or error if negative
    """
    size: int32 = xs_vector_list_size(lst)
    if idx < 0 or idx >= size:
        return c_vector_list_index_out_of_range_error
    _xs_vector_list_arr_set(lst, idx + 1, value)
    return c_vector_list_success


def _xs_vector_list_extend_vector_array(lst: int32 = int32(-1), capacity: int32 = int32(0)) -> int32:
    if capacity >= c_vector_list_max_capacity:
        return c_vector_list_max_capacity_error
    new_capacity: int32 = int32(0)
    if capacity > c_vector_list_max_capacity // 2:
        new_capacity = c_vector_list_max_capacity
    else:
        new_capacity = capacity * 2
    if new_capacity > c_vector_list_max_capacity:
        new_capacity = c_vector_list_max_capacity
    elif new_capacity == 0:
        new_capacity = int32(8)
    r: int32 = _xs_vector_list_arr_resize(lst, new_capacity)
    if r != 1:
        return c_vector_list_resize_failed_error
    return c_vector_list_success


def _xs_vector_list_shrink_vector_array(lst: int32 = int32(-1), size: int32 = int32(0),
                                        capacity: int32 = int32(0)) -> int32:
    if size <= (capacity // 2):
        r: int32 = _xs_vector_list_arr_resize(lst, capacity // 2)
        if r != 1:
            return c_vector_list_resize_failed_error
    return c_vector_list_success


def xs_vector_list_append(lst: int32 = int32(-1), value: XsVector = vector(0.0, 0.0, 0.0)) -> int32:
    """
    Appends a value to the end of the list, growing the backing array if needed.
    :param lst: list id
    :param value: value to append
    :return: `c_vector_list_success` on success, or error if negative
    """
    capacity: int32 = xs_vector_list_capacity(lst)
    size: int32 = xs_vector_list_size(lst)
    next_idx: int32 = size + 1
    if capacity <= next_idx:
        r: int32 = _xs_vector_list_extend_vector_array(lst, capacity)
        if r != c_vector_list_success:
            return r
    _xs_vector_list_arr_set(lst, next_idx, value)
    _xs_vector_list_set_size(lst, next_idx)
    return c_vector_list_success


def xs_vector_list_insert(lst: int32 = int32(-1), idx: int32 = int32(-1),
                          value: XsVector = vector(0.0, 0.0, 0.0)) -> int32:
    """
    Inserts a value at the given index, shifting subsequent elements to the right.
    :param lst: list id
    :param idx: zero-based index at which to insert
    :param value: value to insert
    :return: `c_vector_list_success` on success, or error if negative
    """
    capacity: int32 = xs_vector_list_capacity(lst)
    size: int32 = xs_vector_list_size(lst)
    if idx < 0 or idx > size:
        return c_vector_list_index_out_of_range_error
    new_size: int32 = size + 1
    if capacity <= new_size:
        r: int32 = _xs_vector_list_extend_vector_array(lst, capacity)
        if r != c_vector_list_success:
            return r
    for i in i32range(size, idx, -1):
        _xs_vector_list_arr_set(lst, i + 1, _xs_vector_list_arr_get(lst, i))
    _xs_vector_list_arr_set(lst, idx + 1, value)
    _xs_vector_list_set_size(lst, new_size)

    return c_vector_list_success


def xs_vector_list_pop(lst: int32 = int32(-1), idx: int32 = c_vector_list_max_capacity) -> XsVector:
    """
    Removes and returns the element at the given index, shifting subsequent elements to the left.
    Defaults to the last element. Sets last error on failure.
    :param lst: list id
    :param idx: zero-based index of element to remove (defaults to last)
    :return: removed value, or `c_vector_list_generic_error_vector` on error
    """
    global _vector_list_last_operation_status
    capacity: int32 = xs_vector_list_capacity(lst)
    size: int32 = xs_vector_list_size(lst)
    if idx == c_vector_list_max_capacity:
        idx = size - 1
    if idx < 0 or idx >= size:
        _vector_list_last_operation_status = c_vector_list_index_out_of_range_error
        return c_vector_list_generic_error_vector
    removed_elem: XsVector = _xs_vector_list_arr_get(lst, idx + 1)
    for i in i32range(idx + 2, size + 1):
        _xs_vector_list_arr_set(lst, i - 1, _xs_vector_list_arr_get(lst, i))
    _xs_vector_list_set_size(lst, size - 1)
    r: int32 = _xs_vector_list_shrink_vector_array(lst, size, capacity)
    if r != c_vector_list_success:
        _vector_list_last_operation_status = r
        return c_vector_list_generic_error_vector
    _vector_list_last_operation_status = c_vector_list_success
    return removed_elem


def xs_vector_list_remove(lst: int32 = int32(-1), value: XsVector = vector(-1.0, -1.0, -1.0)) -> int32:
    """
    Removes the first occurrence of the given value from the list.
    :param lst: list id
    :param value: value to remove
    :return: index of the removed element, or `c_vector_list_generic_error` if not found
    """
    capacity: int32 = xs_vector_list_capacity(lst)
    size: int32 = xs_vector_list_size(lst)
    found_idx: int32 = int32(-1)
    i: int32 = int32(1)
    while i <= size and found_idx == -1:
        c_val: XsVector = _xs_vector_list_arr_get(lst, i)
        if c_val == value:
            found_idx = i
        i += 1
    if found_idx == -1:
        return c_vector_list_generic_error
    for j in i32range(found_idx + 1, size + 1):
        _xs_vector_list_arr_set(lst, j - 1, _xs_vector_list_arr_get(lst, j))
    _xs_vector_list_set_size(lst, size - 1)
    r: int32 = _xs_vector_list_shrink_vector_array(lst, size, capacity)
    if r != c_vector_list_success:
        return r
    return found_idx - 1


def xs_vector_list_index(lst: int32 = int32(-1), value: XsVector = vector(-1.0, -1.0, -1.0), start: int32 = int32(0),
                         stop: int32 = c_vector_list_empty_int_param) -> int32:
    """
    Returns the index of the first occurrence of the value within the optional [start, stop) range. Negative start/stop are relative to the end.
    :param lst: list id
    :param value: value to search for
    :param start: start of search range (inclusive)
    :param stop: end of search range (exclusive), defaults to list size
    :return: index of the value, or `c_vector_list_generic_error` if not found
    """
    size: int32 = xs_vector_list_size(lst)

    if stop == c_vector_list_empty_int_param or stop > size:
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
        if _xs_vector_list_arr_get(lst, i + 1) == value:
            return i
    return c_vector_list_generic_error


def xs_vector_list_contains(lst: int32 = int32(-1), value: XsVector = vector(-1.0, -1.0, -1.0)) -> bool:
    """
    Checks whether the list contains the given value.
    :param lst: list id
    :param value: value to search for
    :return: true if the value is found, false otherwise
    """
    return xs_vector_list_index(lst, value) > -1


def xs_vector_list_to_string(lst: int32 = int32(-1)) -> str:
    """
    Returns a string representation of the list in the format `[v0, v1, ...]`.
    :param lst: list id
    :return: string representation of the list
    """
    size: int32 = xs_vector_list_size(lst)
    s: str = "["
    for i in i32range(1, size + 1):
        s += str(_xs_vector_list_arr_get(lst, i))
        if i < size:
            s += ", "
    s += "]"
    return s


def xs_vector_list_copy(lst: int32 = int32(-1), start: int32 = int32(0),
                        end: int32 = c_vector_list_max_capacity) -> int32:
    """
    Returns a copy of the list, optionally sliced by [start, end). Negative start/end are relative to the end.
    :param lst: list id
    :param start: start of slice (inclusive)
    :param end: end of slice (exclusive), defaults to list size
    :return: new list id, or `c_vector_list_generic_error` on error
    """
    size: int32 = xs_vector_list_size(lst)
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
    new_lst: int32 = _xs_vector_list_arr_create(new_size + 1)
    if new_lst < 0:
        return c_vector_list_generic_error
    for i in i32range(fr, to):
        _xs_vector_list_arr_set(new_lst, i - fr + 1, _xs_vector_list_arr_get(lst, i + 1))
    _xs_vector_list_set_size(new_lst, new_size)
    return new_lst


def xs_vector_list_extend(source: int32 = int32(-1), lst: int32 = int32(-1)) -> int32:
    """
    Appends all elements from another list to the source list.
    :param source: list id to extend
    :param lst: list id whose elements are appended
    :return: `c_vector_list_success` on success, or error if negative
    """
    source_size: int32 = xs_vector_list_size(source)
    to_add: int32 = xs_vector_list_size(lst)
    capacity: int32 = xs_vector_list_capacity(source)
    new_size: int32 = source_size + to_add
    if new_size + 1 > capacity:
        if new_size >= c_vector_list_max_capacity:
            return c_vector_list_max_capacity_error
        r: int32 = _xs_vector_list_arr_resize(source, new_size + 1)
        if r != 1:
            return c_vector_list_resize_failed_error
    for i in i32range(1, to_add + 1):
        _xs_vector_list_arr_set(source, i + source_size, _xs_vector_list_arr_get(lst, i))
    _xs_vector_list_set_size(source, new_size)
    return c_vector_list_success


def xs_vector_list_extend_with_array(source: int32 = int32(-1), arr: int32 = int32(-1)) -> int32:
    """
    Appends all elements from an XS array to the source list.
    :param source: list id to extend
    :param arr: XS array id whose elements are appended
    :return: `c_vector_list_success` on success, or error if negative
    """
    source_size: int32 = xs_vector_list_size(source)
    to_add: int32 = xs_array_get_size(arr)
    capacity: int32 = xs_vector_list_capacity(source)
    new_size: int32 = source_size + to_add
    if new_size + 1 > capacity:
        if new_size >= c_vector_list_max_capacity or new_size < 0:
            return c_vector_list_max_capacity_error
        r: int32 = _xs_vector_list_arr_resize(source, new_size + 1)
        if r != 1:
            return c_vector_list_resize_failed_error
    for i in i32range(0, to_add):
        _xs_vector_list_arr_set(source, i + source_size + int32(1), xs_array_get_vector(arr, i))
    _xs_vector_list_set_size(source, new_size)
    return c_vector_list_success


def xs_vector_list_clear(lst: int32 = int32(-1)) -> int32:
    """
    Removes all elements from the list and shrinks the backing array.
    :param lst: list id
    :return: `c_vector_list_success` on success, or error if negative
    """
    capacity: int32 = xs_vector_list_capacity(lst)
    if capacity > 8:
        r: int32 = _xs_vector_list_arr_resize(lst, 8)
        if r != 1:
            return c_vector_list_resize_failed_error
    _xs_vector_list_set_size(lst, int32(0))
    return c_vector_list_success


def xs_vector_list_reverse(lst: int32 = int32(-1)) -> None:
    """
    Reverses the list in-place.
    :param lst: list id
    """
    size: int32 = xs_vector_list_size(lst)
    mid: int32 = (size + 2) // 2
    for i in i32range(1, mid):
        temp: XsVector = _xs_vector_list_arr_get(lst, i)
        back_i: int32 = size - i + 1
        _xs_vector_list_arr_set(lst, i, _xs_vector_list_arr_get(lst, back_i))
        _xs_vector_list_arr_set(lst, back_i, temp)


def xs_vector_list_count(lst: int32 = int32(-1), value: XsVector = vector(-1.0, -1.0, -1.0)) -> int32:
    """
    Counts the number of occurrences of a value in the list.
    :param lst: list id
    :param value: value to count
    :return: number of occurrences
    """
    count: int32 = int32(0)
    size: int32 = xs_vector_list_size(lst)
    for i in i32range(1, size + 1):
        if _xs_vector_list_arr_get(lst, i) == value:
            count += 1
    return count


def xs_vector_list_last_error() -> int32:
    """
    Returns the status code of the last operation that sets it (get, pop).
    :return: `c_vector_list_success` if the last such operation succeeded, or a negative error code
    """
    return _vector_list_last_operation_status
