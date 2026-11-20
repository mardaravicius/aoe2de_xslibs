from numpy import int32, float32

from xs_converter.functions import xs_array_create_vector, xs_array_set_vector, \
    xs_array_get_vector, xs_array_get_size, vector, xs_vector_set, \
    str_char_at, str_len, str_remove, str_split, str_substring, str_to_float, str_trim, xs_array_create_string, \
    xs_array_get_string, xs_array_resize_string, xs_array_set_string
from xs_converter.symbols import XsExternConst, i32range, XsVector, XsConst

c_vector_array_generic_error: XsExternConst[int32] = int32(-1)
c_vector_array_max_capacity_error: XsExternConst[int32] = int32(-4)
c_vector_array_max_capacity: XsExternConst[int32] = int32(999999999)
c_vector_array_empty_param: XsExternConst[XsVector] = vector(-9999999.0, -9999999.0, -9999999.0)
c_vector_array_empty_int_param: XsExternConst[int32] = int32(-999999999)
_c_vector_array_empty_float: XsConst[float32] = float32(-9999999.0)


def xs_vector_array(
        v0: XsVector = c_vector_array_empty_param,
        v1: XsVector = c_vector_array_empty_param,
        v2: XsVector = c_vector_array_empty_param,
        v3: XsVector = c_vector_array_empty_param,
        v4: XsVector = c_vector_array_empty_param,
        v5: XsVector = c_vector_array_empty_param,
        v6: XsVector = c_vector_array_empty_param,
        v7: XsVector = c_vector_array_empty_param,
        v8: XsVector = c_vector_array_empty_param,
        v9: XsVector = c_vector_array_empty_param,
        v10: XsVector = c_vector_array_empty_param,
        v11: XsVector = c_vector_array_empty_param,
) -> int32:
    """
    Creates an array with provided values. The first value that equals `c_vector_array_empty_param` will stop further insertion.
    This Function can create an array with 12 values at the maximum.
    :param v0 through v11: value at a given index of an array
    :return: created array id, or `c_vector_array_generic_error` on error
    """
    size: int32 = int32(12)
    if v0 == c_vector_array_empty_param:
        size = int32(0)
    elif v1 == c_vector_array_empty_param:
        size = int32(1)
    elif v2 == c_vector_array_empty_param:
        size = int32(2)
    elif v3 == c_vector_array_empty_param:
        size = int32(3)
    elif v4 == c_vector_array_empty_param:
        size = int32(4)
    elif v5 == c_vector_array_empty_param:
        size = int32(5)
    elif v6 == c_vector_array_empty_param:
        size = int32(6)
    elif v7 == c_vector_array_empty_param:
        size = int32(7)
    elif v8 == c_vector_array_empty_param:
        size = int32(8)
    elif v9 == c_vector_array_empty_param:
        size = int32(9)
    elif v10 == c_vector_array_empty_param:
        size = int32(10)
    elif v11 == c_vector_array_empty_param:
        size = int32(11)
    arr: int32 = xs_array_create_vector(size)
    if arr < 0:
        return c_vector_array_generic_error
    if size == 0:
        return arr
    xs_array_set_vector(arr, 0, v0)
    if size == 1:
        return arr
    xs_array_set_vector(arr, 1, v1)
    if size == 2:
        return arr
    xs_array_set_vector(arr, 2, v2)
    if size == 3:
        return arr
    xs_array_set_vector(arr, 3, v3)
    if size == 4:
        return arr
    xs_array_set_vector(arr, 4, v4)
    if size == 5:
        return arr
    xs_array_set_vector(arr, 5, v5)
    if size == 6:
        return arr
    xs_array_set_vector(arr, 6, v6)
    if size == 7:
        return arr
    xs_array_set_vector(arr, 7, v7)
    if size == 8:
        return arr
    xs_array_set_vector(arr, 8, v8)
    if size == 9:
        return arr
    xs_array_set_vector(arr, 9, v9)
    if size == 10:
        return arr
    xs_array_set_vector(arr, 10, v10)
    if size == 11:
        return arr
    xs_array_set_vector(arr, 11, v11)
    return arr


def xs_vector_array_from_repeated_val(value: XsVector = vector(0.0, 0.0, 0.0), times: int32 = int32(0)) -> int32:
    """
    Creates an array by repeating a single value.
    :param value: value to repeat
    :param times: number of times to repeat the value
    :return: created array id, or `c_vector_array_generic_error` on error
    """
    if times < 0 or times >= c_vector_array_max_capacity:
        return c_vector_array_generic_error
    arr: int32 = xs_array_create_vector(times, value)
    if arr < 0:
        return c_vector_array_generic_error
    return arr


def xs_vector_array_from_repeated_array(arr: int32 = int32(-1), times: int32 = int32(0)) -> int32:
    """
    Creates a new array by repeating all elements of the given array.
    :param arr: source array id
    :param times: number of times to repeat the array contents
    :return: created array id, `c_vector_array_max_capacity_error` if the result is too large, or `c_vector_array_generic_error` on other errors
    """
    if times < 0:
        return c_vector_array_generic_error
    size: int32 = xs_array_get_size(arr)
    if times > 0 and size > (c_vector_array_max_capacity // times):
        return c_vector_array_max_capacity_error
    new_size: int32 = size * times
    if new_size >= c_vector_array_max_capacity:
        return c_vector_array_max_capacity_error
    new_arr: int32 = xs_array_create_vector(new_size)
    if new_arr < 0:
        return c_vector_array_generic_error
    for i in i32range(0, size):
        val: XsVector = xs_array_get_vector(arr, i)
        j: int32 = i
        while j < new_size:
            xs_array_set_vector(new_arr, j, val)
            j += size
    return new_arr


def xs_vector_array_index(arr: int32 = int32(-1), value: XsVector = vector(-1.0, -1.0, -1.0), start: int32 = int32(0), stop: int32 = c_vector_array_empty_int_param) -> int32:
    """
    Returns the index of the first occurrence of the value within the optional [start, stop) range. Negative start/stop are relative to the end.
    :param arr: array id
    :param value: value to search for
    :param start: start of search range (inclusive)
    :param stop: end of search range (exclusive), defaults to array size
    :return: index of the value, or `c_vector_array_generic_error` if not found
    """
    size: int32 = xs_array_get_size(arr)

    if stop == c_vector_array_empty_int_param or stop > size:
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
        if xs_array_get_vector(arr, i) == value:
            return i
    return c_vector_array_generic_error


def xs_vector_array_contains(arr: int32 = int32(-1), value: XsVector = vector(-1.0, -1.0, -1.0)) -> bool:
    """
    Checks whether the array contains the given value.
    :param arr: array id
    :param value: value to search for
    :return: true if the value is found, false otherwise
    """
    return xs_vector_array_index(arr, value) > -1


def xs_vector_array_to_string(arr: int32 = int32(-1)) -> str:
    """
    Returns a string representation of the array in the format `[v0, v1, ...]`.
    :param arr: array id
    :return: string representation of the array
    """
    size: int32 = xs_array_get_size(arr)
    s: str = "["
    for i in i32range(0, size):
        s += str(xs_array_get_vector(arr, i))
        if i < size - 1:
            s += ", "
    s += "]"
    return s


def xs_vector_array_copy(arr: int32 = int32(-1), start: int32 = int32(0), end: int32 = c_vector_array_max_capacity) -> int32:
    """
    Returns a copy of the array, optionally sliced by [start, end). Negative start/end are relative to the end.
    :param arr: array id
    :param start: start of slice (inclusive)
    :param end: end of slice (exclusive), defaults to array size
    :return: new array id, or `c_vector_array_generic_error` on error
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
    new_arr: int32 = xs_array_create_vector(new_size)
    if new_arr < 0:
        return c_vector_array_generic_error
    for i in i32range(fr, to):
        xs_array_set_vector(new_arr, i - fr, xs_array_get_vector(arr, i))
    return new_arr


def xs_vector_array_reverse(arr: int32 = int32(-1)) -> None:
    """
    Reverses the array in-place.
    :param arr: array id
    """
    size: int32 = xs_array_get_size(arr)
    mid: int32 = size // 2
    for i in i32range(0, mid):
        temp: XsVector = xs_array_get_vector(arr, i)
        back_i: int32 = size - i - 1
        xs_array_set_vector(arr, i, xs_array_get_vector(arr, back_i))
        xs_array_set_vector(arr, back_i, temp)


def xs_vector_array_count(arr: int32 = int32(-1), value: XsVector = vector(-1.0, -1.0, -1.0)) -> int32:
    """
    Counts the number of occurrences of a value in the array.
    :param arr: array id
    :param value: value to count
    :return: number of occurrences
    """
    count: int32 = int32(0)
    size: int32 = xs_array_get_size(arr)
    for i in i32range(0, size):
        if xs_array_get_vector(arr, i) == value:
            count += 1
    return count


def _xs_vector_array_find_separator(text: str = "", separator: str = ",", start: int32 = int32(0)) -> int32:
    n: int32 = str_len(text)
    in_quotes: bool = False
    in_parens: bool = False
    for i in i32range(start, n):
        ch: str = str_char_at(text, i)
        if ch == "'":
            in_quotes = not in_quotes
        elif not in_quotes:
            if ch == "(":
                in_parens = True
            elif ch == ")":
                in_parens = False
            elif ch == separator and not in_parens:
                return i
    return int32(-1)


def _xs_vector_array_split_items(items: str = "") -> int32:
    num_parts: int32 = int32(1)
    sep: int32 = _xs_vector_array_find_separator(items, ",", 0)
    while sep >= 0:
        num_parts += 1
        sep = _xs_vector_array_find_separator(items, ",", sep + 1)
    parts: int32 = xs_array_create_string(num_parts)
    start: int32 = int32(0)
    for i in i32range(0, num_parts):
        end: int32 = _xs_vector_array_find_separator(items, ",", start)
        if end < 0:
            xs_array_set_string(parts, i, str_remove(items, 0, start))
        else:
            xs_array_set_string(parts, i, str_substring(items, start, end))
        start = end + 1
    return parts


def _xs_vector_array_parse_vector(text: str = "") -> XsVector:
    n: int32 = str_len(text)
    if n < 3:
        return c_vector_array_empty_param
    if str_substring(text, 0, 2) != "v(" or str_char_at(text, n - 1) != ")":
        return c_vector_array_empty_param
    coords: int32 = str_split(str_substring(text, 2, n - 1), ",")
    if xs_array_get_size(coords) != 3:
        xs_array_resize_string(coords, 0)
        return c_vector_array_empty_param
    x: float32 = str_to_float(str_trim(xs_array_get_string(coords, 0)), _c_vector_array_empty_float)
    y: float32 = str_to_float(str_trim(xs_array_get_string(coords, 1)), _c_vector_array_empty_float)
    z: float32 = str_to_float(str_trim(xs_array_get_string(coords, 2)), _c_vector_array_empty_float)
    xs_array_resize_string(coords, 0)
    if x == _c_vector_array_empty_float or y == _c_vector_array_empty_float or z == _c_vector_array_empty_float:
        return c_vector_array_empty_param
    return xs_vector_set(x, y, z)


def xs_vector_array_from_string(items: str = "") -> int32:
    """
    Creates an array from a comma separated string, e.g. `"v(1.0,2.0,3.0),v(1.5,0.0,-2.0)"`.
    Items are trimmed, and items that cannot be parsed are skipped. Items are parsed twice because
    vector arrays can't be resized, so the array is created at its final size.
    :param items: comma separated values
    :return: created array id, or `c_vector_array_generic_error` on error
    """
    if str_trim(items) == "":
        return xs_array_create_vector(0)
    parts: int32 = _xs_vector_array_split_items(items)
    num_parts: int32 = xs_array_get_size(parts)
    size: int32 = int32(0)
    for i in i32range(0, num_parts):
        if _xs_vector_array_parse_vector(str_trim(xs_array_get_string(parts, i))) != c_vector_array_empty_param:
            size += 1
    arr: int32 = xs_array_create_vector(size)
    if arr < 0:
        xs_array_resize_string(parts, 0)
        return c_vector_array_generic_error
    j: int32 = int32(0)
    for i in i32range(0, num_parts):
        value: XsVector = _xs_vector_array_parse_vector(str_trim(xs_array_get_string(parts, i)))
        if value != c_vector_array_empty_param:
            xs_array_set_vector(arr, j, value)
            j += 1
    xs_array_resize_string(parts, 0)
    return arr
