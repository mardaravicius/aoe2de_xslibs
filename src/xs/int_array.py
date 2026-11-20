from numpy import int32

from xs_converter.functions import xs_array_create_int, xs_array_set_int, xs_array_resize_int, xs_array_get_int, \
    xs_array_get_size, \
    str_split, str_to_int, str_trim, xs_array_get_string, xs_array_resize_string
from xs_converter.symbols import XsExternConst, i32range

c_int_array_success: XsExternConst[int32] = int32(0)
c_int_array_generic_error: XsExternConst[int32] = int32(-1)
c_int_array_index_out_of_range_error: XsExternConst[int32] = int32(-2)
c_int_array_resize_failed_error: XsExternConst[int32] = int32(-3)
c_int_array_max_capacity_error: XsExternConst[int32] = int32(-4)
c_int_array_max_capacity: XsExternConst[int32] = int32(999999999)
c_int_array_empty_param: XsExternConst[int32] = int32(-999999999)
_c_int_array_int_max: int32 = int32(-1)
_c_int_array_int_min: int32 = int32(-1)
_int_array_last_operation_status: int32 = c_int_array_success


def xs_int_array(
        v0: int32 = c_int_array_empty_param,
        v1: int32 = c_int_array_empty_param,
        v2: int32 = c_int_array_empty_param,
        v3: int32 = c_int_array_empty_param,
        v4: int32 = c_int_array_empty_param,
        v5: int32 = c_int_array_empty_param,
        v6: int32 = c_int_array_empty_param,
        v7: int32 = c_int_array_empty_param,
        v8: int32 = c_int_array_empty_param,
        v9: int32 = c_int_array_empty_param,
        v10: int32 = c_int_array_empty_param,
        v11: int32 = c_int_array_empty_param,
) -> int32:
    """
    Creates an array with provided values. The first value that equals `c_int_array_empty_param` will stop further insertion.
    This Function can create an array with 12 values at the maximum.
    :param v0 through v11: value at a given index of an array
    :return: created array id, or `c_int_array_generic_error` on error
    """
    size: int32 = int32(12)
    if v0 == c_int_array_empty_param:
        size = int32(0)
    elif v1 == c_int_array_empty_param:
        size = int32(1)
    elif v2 == c_int_array_empty_param:
        size = int32(2)
    elif v3 == c_int_array_empty_param:
        size = int32(3)
    elif v4 == c_int_array_empty_param:
        size = int32(4)
    elif v5 == c_int_array_empty_param:
        size = int32(5)
    elif v6 == c_int_array_empty_param:
        size = int32(6)
    elif v7 == c_int_array_empty_param:
        size = int32(7)
    elif v8 == c_int_array_empty_param:
        size = int32(8)
    elif v9 == c_int_array_empty_param:
        size = int32(9)
    elif v10 == c_int_array_empty_param:
        size = int32(10)
    elif v11 == c_int_array_empty_param:
        size = int32(11)
    arr: int32 = xs_array_create_int(size)
    if arr < 0:
        return c_int_array_generic_error
    if size == 0:
        return arr
    xs_array_set_int(arr, 0, v0)
    if size == 1:
        return arr
    xs_array_set_int(arr, 1, v1)
    if size == 2:
        return arr
    xs_array_set_int(arr, 2, v2)
    if size == 3:
        return arr
    xs_array_set_int(arr, 3, v3)
    if size == 4:
        return arr
    xs_array_set_int(arr, 4, v4)
    if size == 5:
        return arr
    xs_array_set_int(arr, 5, v5)
    if size == 6:
        return arr
    xs_array_set_int(arr, 6, v6)
    if size == 7:
        return arr
    xs_array_set_int(arr, 7, v7)
    if size == 8:
        return arr
    xs_array_set_int(arr, 8, v8)
    if size == 9:
        return arr
    xs_array_set_int(arr, 9, v9)
    if size == 10:
        return arr
    xs_array_set_int(arr, 10, v10)
    if size == 11:
        return arr
    xs_array_set_int(arr, 11, v11)
    return arr


def _xs_int_array_int_abs(n: int32 = int32(0)) -> int32:
    if n < int32(0):
        return n * int32(-1)
    return n


def xs_int_array_from_range(start: int32 = int32(0), stop: int32 = int32(0), step: int32 = int32(1)) -> int32:
    """
    Creates an array from a given range.
    :param start: start of range (inclusive)
    :param stop: end of range (exclusive)
    :param step: increment between values (positive or negative, must not be zero)
    :return: created array id, or `c_int_array_generic_error` on error
    """
    global _c_int_array_int_min, _c_int_array_int_max
    if _c_int_array_int_min == int32(-1):
        _c_int_array_int_min = -2147483648
        _c_int_array_int_max = 2147483647
    if step == 0 or step == _c_int_array_int_min:
        return c_int_array_generic_error
    distance: int32 = int32(0)
    if step > 0:
        if start > stop:
            return c_int_array_generic_error
        if start < 0 and stop >= 0 and stop > _c_int_array_int_max + start:
            return c_int_array_generic_error
        distance = stop - start
    else:
        if start < stop:
            return c_int_array_generic_error
        if start >= 0 and stop < 0 and start > _c_int_array_int_max + stop:
            return c_int_array_generic_error
        distance = start - stop
    step_a: int32 = _xs_int_array_int_abs(step)
    size: int32 = distance // step_a
    if size >= c_int_array_max_capacity:
        return c_int_array_generic_error
    if distance % step_a > 0:
        size += int32(1)
    arr: int32 = xs_array_create_int(size)
    if arr < 0:
        return c_int_array_generic_error
    i: int32 = int32(0)
    current: int32 = start
    while i < size:
        xs_array_set_int(arr, i, current)
        if i < size - 1:
            current += step
        i += 1
    return arr


def xs_int_array_from_repeated_val(value: int32 = int32(0), times: int32 = int32(0)) -> int32:
    """
    Creates an array by repeating a single value.
    :param value: value to repeat
    :param times: number of times to repeat the value
    :return: created array id, or `c_int_array_generic_error` on error
    """
    if times < 0 or times >= c_int_array_max_capacity:
        return c_int_array_generic_error
    arr: int32 = xs_array_create_int(times, value)
    if arr < 0:
        return c_int_array_generic_error
    return arr


def xs_int_array_from_repeated_array(arr: int32 = int32(-1), times: int32 = int32(0)) -> int32:
    """
    Creates a new array by repeating all elements of the given array.
    :param arr: source array id
    :param times: number of times to repeat the array contents
    :return: created array id, `c_int_array_max_capacity_error` if the result is too large, or `c_int_array_generic_error` on other errors
    """
    if times < 0:
        return c_int_array_generic_error
    size: int32 = xs_array_get_size(arr)
    if times > 0 and size > (c_int_array_max_capacity // times):
        return c_int_array_max_capacity_error
    new_size: int32 = size * times
    if new_size >= c_int_array_max_capacity:
        return c_int_array_max_capacity_error
    new_arr: int32 = xs_array_create_int(new_size)
    if new_arr < 0:
        return c_int_array_generic_error
    for i in i32range(0, size):
        val: int32 = xs_array_get_int(arr, i)
        j: int32 = i
        while j < new_size:
            xs_array_set_int(new_arr, j, val)
            j += size
    return new_arr


def xs_int_array_index(arr: int32 = int32(-1), value: int32 = int32(-1), start: int32 = int32(0), stop: int32 = c_int_array_empty_param) -> int32:
    """
    Returns the index of the first occurrence of the value within the optional [start, stop) range. Negative start/stop are relative to the end.
    :param arr: array id
    :param value: value to search for
    :param start: start of search range (inclusive)
    :param stop: end of search range (exclusive), defaults to array size
    :return: index of the value, or `c_int_array_generic_error` if not found
    """
    size: int32 = xs_array_get_size(arr)

    if stop == c_int_array_empty_param or stop > size:
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
        if xs_array_get_int(arr, i) == value:
            return i
    return c_int_array_generic_error


def xs_int_array_contains(arr: int32 = int32(-1), value: int32 = int32(-1)) -> bool:
    """
    Checks whether the array contains the given value.
    :param arr: array id
    :param value: value to search for
    :return: true if the value is found, false otherwise
    """
    return xs_int_array_index(arr, value) > -1


def _xs_int_array_compare_elem(a: int32 = int32(-1), b: int32 = int32(-1), reverse: bool = False) -> bool:
    if reverse:
        return a > b
    return a < b


def _xs_int_array_sift_down(arr: int32 = int32(-1), start: int32 = int32(-1), end: int32 = int32(-1), reverse: bool = False) -> None:
    root: int32 = start
    while True:
        child: int32 = 2 * root + 1
        if child > end:
            return
        child_val: int32 = xs_array_get_int(arr, child)
        if child + 1 <= end:
            child_val1: int32 = xs_array_get_int(arr, child + 1)
            if _xs_int_array_compare_elem(child_val, child_val1, reverse):
                child += 1
                child_val = child_val1
        root_val: int32 = xs_array_get_int(arr, root)
        if _xs_int_array_compare_elem(root_val, child_val, reverse):
            xs_array_set_int(arr, root, child_val)
            xs_array_set_int(arr, child, root_val)
            root = child
        else:
            return


def xs_int_array_sort(arr: int32 = int32(-1), reverse: bool = False) -> None:
    """
    Sorts the array in-place using heapsort.
    :param arr: array id
    :param reverse: if true, sorts in descending order
    """
    size: int32 = xs_array_get_size(arr)
    for start in i32range(size // 2 - 1, -1, -1):
        _xs_int_array_sift_down(arr, start, size - 1, reverse)

    for end in i32range(size - 1, 0, -1):
        temp: int32 = xs_array_get_int(arr, 0)
        xs_array_set_int(arr, 0, xs_array_get_int(arr, end))
        xs_array_set_int(arr, end, temp)
        _xs_int_array_sift_down(arr, int32(0), end - 1, reverse)


def xs_int_array_to_string(arr: int32 = int32(-1), start: str = "[", sep: str = ", ", end: str = "]") -> str:
    """
    Returns a string representation of the array, by default in the format `[v0, v1, ...]`.
    :param arr: array id
    :param start: string prepended to the output
    :param sep: separator between elements
    :param end: string appended to the output
    :return: string representation of the array
    """
    size: int32 = xs_array_get_size(arr)
    s: str = start
    for i in i32range(0, size):
        s += str(xs_array_get_int(arr, i))
        if i < size - 1:
            s += sep
    s += end
    return s


def xs_int_array_copy(arr: int32 = int32(-1), start: int32 = int32(0), end: int32 = c_int_array_max_capacity) -> int32:
    """
    Returns a copy of the array, optionally sliced by [start, end). Negative start/end are relative to the end.
    :param arr: array id
    :param start: start of slice (inclusive)
    :param end: end of slice (exclusive), defaults to array size
    :return: new array id, or `c_int_array_generic_error` on error
    """
    size: int32 = xs_array_get_size(arr)
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
    new_arr: int32 = xs_array_create_int(new_size)
    if new_arr < 0:
        return c_int_array_generic_error
    for i in i32range(fr, to):
        xs_array_set_int(new_arr, i - fr, xs_array_get_int(arr, i))
    return new_arr


def xs_int_array_delete(arr: int32 = int32(-1)) -> int32:
    """
    Resizes the array to 0 to free its memory. XS can't fully delete arrays,
    so the array id stays allocated and must not be used afterwards.
    :param arr: array id
    :return: `c_int_array_success` on success, or `c_int_array_resize_failed_error` if the resize fails
    """
    r: int32 = xs_array_resize_int(arr, 0)
    if r != 1:
        return c_int_array_resize_failed_error
    return c_int_array_success


def xs_int_array_compare(arr1: int32 = int32(-1), arr2: int32 = int32(-1)) -> int32:
    """
    Performs lexicographic comparison of two arrays.
    :param arr1: first array id
    :param arr2: second array id
    :return: -1 if arr1 < arr2, 1 if arr1 > arr2, 0 if equal
    """
    size1: int32 = xs_array_get_size(arr1)
    size2: int32 = xs_array_get_size(arr2)
    i: int32 = int32(0)
    while i < size1 and i < size2:
        v1: int32 = xs_array_get_int(arr1, i)
        v2: int32 = xs_array_get_int(arr2, i)
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


def xs_int_array_reverse(arr: int32 = int32(-1)) -> None:
    """
    Reverses the array in-place.
    :param arr: array id
    """
    size: int32 = xs_array_get_size(arr)
    mid: int32 = size // 2
    for i in i32range(0, mid):
        temp: int32 = xs_array_get_int(arr, i)
        back_i: int32 = size - i - 1
        xs_array_set_int(arr, i, xs_array_get_int(arr, back_i))
        xs_array_set_int(arr, back_i, temp)


def xs_int_array_count(arr: int32 = int32(-1), value: int32 = int32(-1)) -> int32:
    """
    Counts the number of occurrences of a value in the array.
    :param arr: array id
    :param value: value to count
    :return: number of occurrences
    """
    count: int32 = int32(0)
    size: int32 = xs_array_get_size(arr)
    for i in i32range(0, size):
        if xs_array_get_int(arr, i) == value:
            count += 1
    return count


def xs_int_array_sum(arr: int32 = int32(-1)) -> int32:
    """
    Returns the sum of all elements in the array.
    :param arr: array id
    :return: sum of elements
    """
    s: int32 = int32(0)
    size: int32 = xs_array_get_size(arr)
    for i in i32range(0, size):
        s += xs_array_get_int(arr, i)
    return s


def xs_int_array_min(arr: int32 = int32(-1)) -> int32:
    """
    Returns the minimum value in the array. Sets last error on failure.
    :param arr: array id
    :return: minimum value, or `c_int_array_generic_error` on error
    """
    global _int_array_last_operation_status
    size: int32 = xs_array_get_size(arr)
    if size <= 0:
        _int_array_last_operation_status = c_int_array_index_out_of_range_error
        return c_int_array_generic_error
    m: int32 = xs_array_get_int(arr, 0)
    for i in i32range(1, size):
        v: int32 = xs_array_get_int(arr, i)
        if v < m:
            m = v
    _int_array_last_operation_status = c_int_array_success
    return m


def xs_int_array_max(arr: int32 = int32(-1)) -> int32:
    """
    Returns the maximum value in the array. Sets last error on failure.
    :param arr: array id
    :return: maximum value, or `c_int_array_generic_error` on error
    """
    global _int_array_last_operation_status
    size: int32 = xs_array_get_size(arr)
    if size <= 0:
        _int_array_last_operation_status = c_int_array_index_out_of_range_error
        return c_int_array_generic_error
    m: int32 = xs_array_get_int(arr, 0)
    for i in i32range(1, size):
        v: int32 = xs_array_get_int(arr, i)
        if v > m:
            m = v
    _int_array_last_operation_status = c_int_array_success
    return m


def xs_int_array_last_error() -> int32:
    """
    Returns the status code of the last operation that sets it (min, max).
    :return: `c_int_array_success` if the last such operation succeeded, or a negative error code
    """
    return _int_array_last_operation_status


def xs_int_array_from_string(items: str = "") -> int32:
    """
    Creates an array from a comma separated string, e.g. `"1,2,3"`.
    Items are trimmed, and items that cannot be parsed are skipped.
    :param items: comma separated values
    :return: created array id, or `c_int_array_generic_error` on error
    """
    if str_trim(items) == "":
        return xs_array_create_int(0)
    parts: int32 = str_split(items, ",")
    num_parts: int32 = xs_array_get_size(parts)
    arr: int32 = xs_array_create_int(num_parts)
    if arr < 0:
        xs_array_resize_string(parts, 0)
        return c_int_array_generic_error
    size: int32 = int32(0)
    for i in i32range(0, num_parts):
        item: str = str_trim(xs_array_get_string(parts, i))
        value: int32 = str_to_int(item, 10, c_int_array_empty_param)
        if value != c_int_array_empty_param:
            xs_array_set_int(arr, size, value)
            size += 1
    xs_array_resize_string(parts, 0)
    if size < num_parts:
        r: int32 = xs_array_resize_int(arr, size)
        if r != 1:
            return c_int_array_resize_failed_error
    return arr
