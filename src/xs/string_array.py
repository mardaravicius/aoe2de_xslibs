from numpy import int32

from xs_converter.functions import xs_array_create_string, xs_array_set_string, xs_array_resize_string, \
    xs_array_get_string, xs_array_get_size, \
    str_char_at, str_index_of, str_len, str_remove, str_substring, str_trim
from xs_converter.symbols import XsExternConst, i32range

c_string_array_success: XsExternConst[int32] = int32(0)
c_string_array_generic_error: XsExternConst[int32] = int32(-1)
c_string_array_index_out_of_range_error: XsExternConst[int32] = int32(-2)
c_string_array_resize_failed_error: XsExternConst[int32] = int32(-3)
c_string_array_max_capacity_error: XsExternConst[int32] = int32(-4)
c_string_array_max_capacity: XsExternConst[int32] = int32(999999999)
c_string_array_empty_int_param: XsExternConst[int32] = int32(-999999999)
_string_array_last_operation_status: int32 = c_string_array_success


def xs_string_array(
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
    Creates an array with provided values. The first value that equals the default sentinel will stop further insertion.
    This Function can create an array with 12 values at the maximum.
    :param v0 through v11: value at a given index of an array
    :return: created array id, or `c_string_array_generic_error` on error
    """
    size: int32 = int32(12)
    if v0 == "!<[empty":
        size = int32(0)
    elif v1 == "!<[empty":
        size = int32(1)
    elif v2 == "!<[empty":
        size = int32(2)
    elif v3 == "!<[empty":
        size = int32(3)
    elif v4 == "!<[empty":
        size = int32(4)
    elif v5 == "!<[empty":
        size = int32(5)
    elif v6 == "!<[empty":
        size = int32(6)
    elif v7 == "!<[empty":
        size = int32(7)
    elif v8 == "!<[empty":
        size = int32(8)
    elif v9 == "!<[empty":
        size = int32(9)
    elif v10 == "!<[empty":
        size = int32(10)
    elif v11 == "!<[empty":
        size = int32(11)
    arr: int32 = xs_array_create_string(size)
    if arr < 0:
        return c_string_array_generic_error
    if size == 0:
        return arr
    xs_array_set_string(arr, 0, v0)
    if size == 1:
        return arr
    xs_array_set_string(arr, 1, v1)
    if size == 2:
        return arr
    xs_array_set_string(arr, 2, v2)
    if size == 3:
        return arr
    xs_array_set_string(arr, 3, v3)
    if size == 4:
        return arr
    xs_array_set_string(arr, 4, v4)
    if size == 5:
        return arr
    xs_array_set_string(arr, 5, v5)
    if size == 6:
        return arr
    xs_array_set_string(arr, 6, v6)
    if size == 7:
        return arr
    xs_array_set_string(arr, 7, v7)
    if size == 8:
        return arr
    xs_array_set_string(arr, 8, v8)
    if size == 9:
        return arr
    xs_array_set_string(arr, 9, v9)
    if size == 10:
        return arr
    xs_array_set_string(arr, 10, v10)
    if size == 11:
        return arr
    xs_array_set_string(arr, 11, v11)
    return arr


def xs_string_array_from_repeated_val(value: str = "", times: int32 = int32(0)) -> int32:
    """
    Creates an array by repeating a single value.
    :param value: value to repeat
    :param times: number of times to repeat the value
    :return: created array id, or `c_string_array_generic_error` on error
    """
    if times < 0 or times >= c_string_array_max_capacity:
        return c_string_array_generic_error
    arr: int32 = xs_array_create_string(times, value)
    if arr < 0:
        return c_string_array_generic_error
    return arr


def xs_string_array_from_repeated_array(arr: int32 = int32(-1), times: int32 = int32(0)) -> int32:
    """
    Creates a new array by repeating all elements of the given array.
    :param arr: source array id
    :param times: number of times to repeat the array contents
    :return: created array id, `c_string_array_max_capacity_error` if the result is too large, or `c_string_array_generic_error` on other errors
    """
    if times < 0:
        return c_string_array_generic_error
    size: int32 = xs_array_get_size(arr)
    if times > 0 and size > (c_string_array_max_capacity // times):
        return c_string_array_max_capacity_error
    new_size: int32 = size * times
    if new_size >= c_string_array_max_capacity:
        return c_string_array_max_capacity_error
    new_arr: int32 = xs_array_create_string(new_size)
    if new_arr < 0:
        return c_string_array_generic_error
    for i in i32range(0, size):
        val: str = xs_array_get_string(arr, i)
        j: int32 = i
        while j < new_size:
            xs_array_set_string(new_arr, j, val)
            j += size
    return new_arr


def xs_string_array_index(arr: int32 = int32(-1), value: str = "", start: int32 = int32(0), stop: int32 = c_string_array_empty_int_param) -> int32:
    """
    Returns the index of the first occurrence of the value within the optional [start, stop) range. Negative start/stop are relative to the end.
    :param arr: array id
    :param value: value to search for
    :param start: start of search range (inclusive)
    :param stop: end of search range (exclusive), defaults to array size
    :return: index of the value, or `c_string_array_generic_error` if not found
    """
    size: int32 = xs_array_get_size(arr)

    if stop == c_string_array_empty_int_param or stop > size:
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
        if xs_array_get_string(arr, i) == value:
            return i
    return c_string_array_generic_error


def xs_string_array_contains(arr: int32 = int32(-1), value: str = "") -> bool:
    """
    Checks whether the array contains the given value.
    :param arr: array id
    :param value: value to search for
    :return: true if the value is found, false otherwise
    """
    return xs_string_array_index(arr, value) > -1


def _xs_string_array_compare_elem(a: str = "", b: str = "", reverse: bool = False) -> bool:
    if reverse:
        return a > b
    return a < b


def _xs_string_array_sift_down(arr: int32 = int32(-1), start: int32 = int32(-1), end: int32 = int32(-1), reverse: bool = False) -> None:
    root: int32 = start
    while True:
        child: int32 = 2 * root + 1
        if child > end:
            return
        child_val: str = xs_array_get_string(arr, child)
        if child + 1 <= end:
            child_val1: str = xs_array_get_string(arr, child + 1)
            if _xs_string_array_compare_elem(child_val, child_val1, reverse):
                child += 1
                child_val = child_val1
        root_val: str = xs_array_get_string(arr, root)
        if _xs_string_array_compare_elem(root_val, child_val, reverse):
            xs_array_set_string(arr, root, child_val)
            xs_array_set_string(arr, child, root_val)
            root = child
        else:
            return


def xs_string_array_sort(arr: int32 = int32(-1), reverse: bool = False) -> None:
    """
    Sorts the array in-place using heapsort.
    :param arr: array id
    :param reverse: if true, sorts in descending order
    """
    size: int32 = xs_array_get_size(arr)
    for start in i32range(size // 2 - 1, -1, -1):
        _xs_string_array_sift_down(arr, start, size - 1, reverse)

    for end in i32range(size - 1, 0, -1):
        temp: str = xs_array_get_string(arr, 0)
        xs_array_set_string(arr, 0, xs_array_get_string(arr, end))
        xs_array_set_string(arr, end, temp)
        _xs_string_array_sift_down(arr, int32(0), end - 1, reverse)


def xs_string_array_to_string(arr: int32 = int32(-1)) -> str:
    """
    Returns a string representation of the array in the format `["v0", "v1", ...]`.
    :param arr: array id
    :return: string representation of the array
    """
    size: int32 = xs_array_get_size(arr)
    if size <= 0:
        return "[]"
    s: str = '["'
    for i in i32range(0, size):
        s += xs_array_get_string(arr, i)
        if i < size - 1:
            s += "\", \""
        else:
            s += "\""
    s += "]"
    return s


def xs_string_array_copy(arr: int32 = int32(-1), start: int32 = int32(0), end: int32 = c_string_array_max_capacity) -> int32:
    """
    Returns a copy of the array, optionally sliced by [start, end). Negative start/end are relative to the end.
    :param arr: array id
    :param start: start of slice (inclusive)
    :param end: end of slice (exclusive), defaults to array size
    :return: new array id, or `c_string_array_generic_error` on error
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
    new_arr: int32 = xs_array_create_string(new_size)
    if new_arr < 0:
        return c_string_array_generic_error
    for i in i32range(fr, to):
        xs_array_set_string(new_arr, i - fr, xs_array_get_string(arr, i))
    return new_arr


def xs_string_array_delete(arr: int32 = int32(-1)) -> int32:
    """
    Resizes the array to 0 to free its memory. XS can't fully delete arrays,
    so the array id stays allocated and must not be used afterwards.
    :param arr: array id
    :return: `c_string_array_success` on success, or `c_string_array_resize_failed_error` if the resize fails
    """
    r: int32 = xs_array_resize_string(arr, 0)
    if r != 1:
        return c_string_array_resize_failed_error
    return c_string_array_success


def xs_string_array_compare(arr1: int32 = int32(-1), arr2: int32 = int32(-1)) -> int32:
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
        v1: str = xs_array_get_string(arr1, i)
        v2: str = xs_array_get_string(arr2, i)
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


def xs_string_array_reverse(arr: int32 = int32(-1)) -> None:
    """
    Reverses the array in-place.
    :param arr: array id
    """
    size: int32 = xs_array_get_size(arr)
    mid: int32 = size // 2
    for i in i32range(0, mid):
        temp: str = xs_array_get_string(arr, i)
        back_i: int32 = size - i - 1
        xs_array_set_string(arr, i, xs_array_get_string(arr, back_i))
        xs_array_set_string(arr, back_i, temp)


def xs_string_array_count(arr: int32 = int32(-1), value: str = "") -> int32:
    """
    Counts the number of occurrences of a value in the array.
    :param arr: array id
    :param value: value to count
    :return: number of occurrences
    """
    count: int32 = int32(0)
    size: int32 = xs_array_get_size(arr)
    for i in i32range(0, size):
        if xs_array_get_string(arr, i) == value:
            count += 1
    return count


def xs_string_array_min(arr: int32 = int32(-1)) -> str:
    """
    Returns the minimum value in the array (lexicographic). Sets last error on failure.
    :param arr: array id
    :return: minimum value, or "-1" on error
    """
    global _string_array_last_operation_status
    size: int32 = xs_array_get_size(arr)
    if size <= 0:
        _string_array_last_operation_status = c_string_array_index_out_of_range_error
        return "-1"
    m: str = xs_array_get_string(arr, 0)
    for i in i32range(1, size):
        v: str = xs_array_get_string(arr, i)
        if v < m:
            m = v
    _string_array_last_operation_status = c_string_array_success
    return m


def xs_string_array_max(arr: int32 = int32(-1)) -> str:
    """
    Returns the maximum value in the array (lexicographic). Sets last error on failure.
    :param arr: array id
    :return: maximum value, or "-1" on error
    """
    global _string_array_last_operation_status
    size: int32 = xs_array_get_size(arr)
    if size <= 0:
        _string_array_last_operation_status = c_string_array_index_out_of_range_error
        return "-1"
    m: str = xs_array_get_string(arr, 0)
    for i in i32range(1, size):
        v: str = xs_array_get_string(arr, i)
        if v > m:
            m = v
    _string_array_last_operation_status = c_string_array_success
    return m


def xs_string_array_last_error() -> int32:
    """
    Returns the status code of the last operation that sets it (min, max).
    :return: `c_string_array_success` if the last such operation succeeded, or a negative error code
    """
    return _string_array_last_operation_status


def _xs_string_array_find_separator(text: str = "", separator: str = ",", start: int32 = int32(0)) -> int32:
    n: int32 = str_len(text)
    in_quotes: bool = False
    for i in i32range(start, n):
        ch: str = str_char_at(text, i)
        if ch == "'":
            in_quotes = not in_quotes
        elif ch == separator and not in_quotes:
            return i
    return int32(-1)


def _xs_string_array_split_items(items: str = "") -> int32:
    num_parts: int32 = int32(1)
    sep: int32 = _xs_string_array_find_separator(items, ",", 0)
    while sep >= 0:
        num_parts += 1
        sep = _xs_string_array_find_separator(items, ",", sep + 1)
    parts: int32 = xs_array_create_string(num_parts)
    start: int32 = int32(0)
    for i in i32range(0, num_parts):
        end: int32 = _xs_string_array_find_separator(items, ",", start)
        if end < 0:
            xs_array_set_string(parts, i, str_remove(items, 0, start))
        else:
            xs_array_set_string(parts, i, str_substring(items, start, end))
        start = end + 1
    return parts


def _xs_string_array_is_quoted(text: str = "") -> bool:
    n: int32 = str_len(text)
    if n < 2:
        return False
    if str_char_at(text, 0) != "'" or str_char_at(text, n - 1) != "'":
        return False
    return str_index_of(str_substring(text, 1, n - 1), "'") == -1


def xs_string_array_from_string(items: str = "") -> int32:
    """
    Creates an array from a comma separated string, e.g. `"'a','b c'"`. Strings must be wrapped in `'` and cannot contain `'`.
    Items are trimmed, and items that cannot be parsed are skipped.
    :param items: comma separated values
    :return: created array id, or `c_string_array_generic_error` on error
    """
    if str_trim(items) == "":
        return xs_array_create_string(0)
    parts: int32 = _xs_string_array_split_items(items)
    num_parts: int32 = xs_array_get_size(parts)
    arr: int32 = xs_array_create_string(num_parts)
    if arr < 0:
        xs_array_resize_string(parts, 0)
        return c_string_array_generic_error
    size: int32 = int32(0)
    for i in i32range(0, num_parts):
        item: str = str_trim(xs_array_get_string(parts, i))
        if _xs_string_array_is_quoted(item):
            xs_array_set_string(arr, size, str_substring(item, 1, str_len(item) - 1))
            size += 1
    xs_array_resize_string(parts, 0)
    if size < num_parts:
        r: int32 = xs_array_resize_string(arr, size)
        if r != 1:
            return c_string_array_resize_failed_error
    return arr
