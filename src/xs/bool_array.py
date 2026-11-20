from numpy import int32

from xs_converter.functions import xs_array_create_bool, xs_array_set_bool, xs_array_resize_bool, xs_array_get_bool, \
    xs_array_get_size, \
    str_split, str_trim, xs_array_get_string, xs_array_resize_string
from xs_converter.symbols import XsExternConst, i32range

c_bool_array_success: XsExternConst[int32] = int32(0)
c_bool_array_generic_error: XsExternConst[int32] = int32(-1)
c_bool_array_resize_failed_error: XsExternConst[int32] = int32(-3)
c_bool_array_max_capacity_error: XsExternConst[int32] = int32(-4)
c_bool_array_max_capacity: XsExternConst[int32] = int32(999999999)
c_bool_array_empty_int_param: XsExternConst[int32] = int32(-999999999)


def xs_bool_array_from_repeated_val(value: bool = False, times: int32 = int32(0)) -> int32:
    """
    Creates an array by repeating a single value.
    :param value: value to repeat
    :param times: number of times to repeat the value
    :return: created array id, or `c_bool_array_generic_error` on error
    """
    if times < 0 or times >= c_bool_array_max_capacity:
        return c_bool_array_generic_error
    arr: int32 = xs_array_create_bool(times, value)
    if arr < 0:
        return c_bool_array_generic_error
    return arr


def xs_bool_array_from_repeated_array(arr: int32 = int32(-1), times: int32 = int32(0)) -> int32:
    """
    Creates a new array by repeating all elements of the given array.
    :param arr: source array id
    :param times: number of times to repeat the array contents
    :return: created array id, `c_bool_array_max_capacity_error` if the result is too large, or `c_bool_array_generic_error` on other errors
    """
    if times < 0:
        return c_bool_array_generic_error
    size: int32 = xs_array_get_size(arr)
    if times > 0 and size > (c_bool_array_max_capacity // times):
        return c_bool_array_max_capacity_error
    new_size: int32 = size * times
    if new_size >= c_bool_array_max_capacity:
        return c_bool_array_max_capacity_error
    new_arr: int32 = xs_array_create_bool(new_size)
    if new_arr < 0:
        return c_bool_array_generic_error
    for i in i32range(0, size):
        val: bool = xs_array_get_bool(arr, i)
        j: int32 = i
        while j < new_size:
            xs_array_set_bool(new_arr, j, val)
            j += size
    return new_arr


def xs_bool_array_index(arr: int32 = int32(-1), value: bool = False, start: int32 = int32(0), stop: int32 = c_bool_array_empty_int_param) -> int32:
    """
    Returns the index of the first occurrence of the value within the optional [start, stop) range. Negative start/stop are relative to the end.
    :param arr: array id
    :param value: value to search for
    :param start: start of search range (inclusive)
    :param stop: end of search range (exclusive), defaults to array size
    :return: index of the value, or `c_bool_array_generic_error` if not found
    """
    size: int32 = xs_array_get_size(arr)

    if stop == c_bool_array_empty_int_param or stop > size:
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
        if xs_array_get_bool(arr, i) == value:
            return i
    return c_bool_array_generic_error


def xs_bool_array_contains(arr: int32 = int32(-1), value: bool = False) -> bool:
    """
    Checks whether the array contains the given value.
    :param arr: array id
    :param value: value to search for
    :return: true if the value is found, false otherwise
    """
    return xs_bool_array_index(arr, value) > -1


def _xs_bool_array_compare_elem(a: bool = False, b: bool = False, reverse: bool = False) -> bool:
    if reverse:
        return a and (not b)
    return (not a) and b


def _xs_bool_array_sift_down(arr: int32 = int32(-1), start: int32 = int32(-1), end: int32 = int32(-1), reverse: bool = False) -> None:
    root: int32 = start
    while True:
        child: int32 = 2 * root + 1
        if child > end:
            return
        child_val: bool = xs_array_get_bool(arr, child)
        if child + 1 <= end:
            child_val1: bool = xs_array_get_bool(arr, child + 1)
            if _xs_bool_array_compare_elem(child_val, child_val1, reverse):
                child += 1
                child_val = child_val1
        root_val: bool = xs_array_get_bool(arr, root)
        if _xs_bool_array_compare_elem(root_val, child_val, reverse):
            xs_array_set_bool(arr, root, child_val)
            xs_array_set_bool(arr, child, root_val)
            root = child
        else:
            return


def xs_bool_array_sort(arr: int32 = int32(-1), reverse: bool = False) -> None:
    """
    Sorts the array in-place using heapsort.
    :param arr: array id
    :param reverse: if true, sorts in descending order
    """
    size: int32 = xs_array_get_size(arr)
    for start in i32range(size // 2 - 1, -1, -1):
        _xs_bool_array_sift_down(arr, start, size - 1, reverse)

    for end in i32range(size - 1, 0, -1):
        temp: bool = xs_array_get_bool(arr, 0)
        xs_array_set_bool(arr, 0, xs_array_get_bool(arr, end))
        xs_array_set_bool(arr, end, temp)
        _xs_bool_array_sift_down(arr, int32(0), end - 1, reverse)


def xs_bool_array_to_string(arr: int32 = int32(-1), start: str = "[", sep: str = ", ", end: str = "]", str_true: str = "true",
                            str_false: str = "false") -> str:
    """
    Returns a string representation of the array, by default in the format `[true, false, ...]`.
    :param arr: array id
    :param start: string prepended to the output
    :param sep: separator between elements
    :param end: string appended to the output
    :param str_true: string used for true values
    :param str_false: string used for false values
    :return: string representation of the array
    """
    size: int32 = xs_array_get_size(arr)
    s: str = start
    for i in i32range(0, size):
        if xs_array_get_bool(arr, i):
            s += str_true
        else:
            s += str_false
        if i < size - 1:
            s += sep
    s += end
    return s


def xs_bool_array_copy(arr: int32 = int32(-1), start: int32 = int32(0), end: int32 = c_bool_array_max_capacity) -> int32:
    """
    Returns a copy of the array, optionally sliced by [start, end). Negative start/end are relative to the end.
    :param arr: array id
    :param start: start of slice (inclusive)
    :param end: end of slice (exclusive), defaults to array size
    :return: new array id, or `c_bool_array_generic_error` on error
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
    new_arr: int32 = xs_array_create_bool(new_size)
    if new_arr < 0:
        return c_bool_array_generic_error
    for i in i32range(fr, to):
        xs_array_set_bool(new_arr, i - fr, xs_array_get_bool(arr, i))
    return new_arr


def xs_bool_array_delete(arr: int32 = int32(-1)) -> int32:
    """
    Resizes the array to 0 to free its memory. XS can't fully delete arrays,
    so the array id stays allocated and must not be used afterwards.
    :param arr: array id
    :return: `c_bool_array_success` on success, or `c_bool_array_resize_failed_error` if the resize fails
    """
    r: int32 = xs_array_resize_bool(arr, 0)
    if r != 1:
        return c_bool_array_resize_failed_error
    return c_bool_array_success


def xs_bool_array_compare(arr1: int32 = int32(-1), arr2: int32 = int32(-1)) -> int32:
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
        v1: bool = xs_array_get_bool(arr1, i)
        v2: bool = xs_array_get_bool(arr2, i)
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


def xs_bool_array_reverse(arr: int32 = int32(-1)) -> None:
    """
    Reverses the array in-place.
    :param arr: array id
    """
    size: int32 = xs_array_get_size(arr)
    mid: int32 = size // 2
    for i in i32range(0, mid):
        temp: bool = xs_array_get_bool(arr, i)
        back_i: int32 = size - i - 1
        xs_array_set_bool(arr, i, xs_array_get_bool(arr, back_i))
        xs_array_set_bool(arr, back_i, temp)


def xs_bool_array_count(arr: int32 = int32(-1), value: bool = False) -> int32:
    """
    Counts the number of occurrences of a value in the array.
    :param arr: array id
    :param value: value to count
    :return: number of occurrences
    """
    count: int32 = int32(0)
    size: int32 = xs_array_get_size(arr)
    for i in i32range(0, size):
        if xs_array_get_bool(arr, i) == value:
            count += 1
    return count


def xs_bool_array_from_string(items: str = "") -> int32:
    """
    Creates an array from a comma separated string, e.g. `"true,false"`.
    Items are trimmed, and items that cannot be parsed are skipped.
    :param items: comma separated values
    :return: created array id, or `c_bool_array_generic_error` on error
    """
    if str_trim(items) == "":
        return xs_array_create_bool(0)
    parts: int32 = str_split(items, ",")
    num_parts: int32 = xs_array_get_size(parts)
    arr: int32 = xs_array_create_bool(num_parts)
    if arr < 0:
        xs_array_resize_string(parts, 0)
        return c_bool_array_generic_error
    size: int32 = int32(0)
    for i in i32range(0, num_parts):
        item: str = str_trim(xs_array_get_string(parts, i))
        value: bool = item == "true"
        if value or item == "false":
            xs_array_set_bool(arr, size, value)
            size += 1
    xs_array_resize_string(parts, 0)
    if size < num_parts:
        r: int32 = xs_array_resize_bool(arr, size)
        if r != 1:
            return c_bool_array_resize_failed_error
    return arr
