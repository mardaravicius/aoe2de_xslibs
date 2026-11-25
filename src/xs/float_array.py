from numpy import int32, float32

from xs_converter.functions import xs_array_create_float, xs_array_set_float, xs_array_resize_float, xs_array_get_float, \
    xs_array_get_size, \
    str_split, str_to_float, str_trim, xs_array_get_string, xs_array_resize_string, \
    xs_array_create_int, xs_array_set_int, xs_array_get_int, xs_array_resize_int
from xs_converter.symbols import XsConst, XsExternConst, i32range

c_float_array_success: XsExternConst[int32] = int32(0)
c_float_array_generic_error: XsExternConst[int32] = int32(-1)
c_float_array_generic_error_float: XsExternConst[float32] = float32(-1.0)
c_float_array_index_out_of_range_error: XsExternConst[int32] = int32(-2)
c_float_array_resize_failed_error: XsExternConst[int32] = int32(-3)
c_float_array_max_capacity_error: XsExternConst[int32] = int32(-4)
c_float_array_max_capacity: XsExternConst[int32] = int32(999999999)
c_float_array_empty_param: XsExternConst[float32] = float32(-9999999.0)
c_float_array_empty_int_param: XsExternConst[int32] = int32(-999999999)
_float_array_last_operation_status: int32 = c_float_array_success
_c_float_array_sort_run: XsConst[int32] = int32(16)
_float_array_sort_keys: int32 = int32(-1)
_float_array_sort_values: int32 = int32(-1)


def xs_float_array(
        v0: float32 = c_float_array_empty_param,
        v1: float32 = c_float_array_empty_param,
        v2: float32 = c_float_array_empty_param,
        v3: float32 = c_float_array_empty_param,
        v4: float32 = c_float_array_empty_param,
        v5: float32 = c_float_array_empty_param,
        v6: float32 = c_float_array_empty_param,
        v7: float32 = c_float_array_empty_param,
        v8: float32 = c_float_array_empty_param,
        v9: float32 = c_float_array_empty_param,
        v10: float32 = c_float_array_empty_param,
        v11: float32 = c_float_array_empty_param,
) -> int32:
    """
    Creates an array with provided values. The first value that equals `c_float_array_empty_param` will stop further insertion.
    This Function can create an array with 12 values at the maximum.
    :param v0 through v11: value at a given index of an array
    :return: created array id, or `c_float_array_generic_error` on error
    """
    size: int32 = int32(12)
    if v0 == c_float_array_empty_param:
        size = int32(0)
    elif v1 == c_float_array_empty_param:
        size = int32(1)
    elif v2 == c_float_array_empty_param:
        size = int32(2)
    elif v3 == c_float_array_empty_param:
        size = int32(3)
    elif v4 == c_float_array_empty_param:
        size = int32(4)
    elif v5 == c_float_array_empty_param:
        size = int32(5)
    elif v6 == c_float_array_empty_param:
        size = int32(6)
    elif v7 == c_float_array_empty_param:
        size = int32(7)
    elif v8 == c_float_array_empty_param:
        size = int32(8)
    elif v9 == c_float_array_empty_param:
        size = int32(9)
    elif v10 == c_float_array_empty_param:
        size = int32(10)
    elif v11 == c_float_array_empty_param:
        size = int32(11)
    arr: int32 = xs_array_create_float(size)
    if arr < 0:
        return c_float_array_generic_error
    if size == 0:
        return arr
    xs_array_set_float(arr, 0, v0)
    if size == 1:
        return arr
    xs_array_set_float(arr, 1, v1)
    if size == 2:
        return arr
    xs_array_set_float(arr, 2, v2)
    if size == 3:
        return arr
    xs_array_set_float(arr, 3, v3)
    if size == 4:
        return arr
    xs_array_set_float(arr, 4, v4)
    if size == 5:
        return arr
    xs_array_set_float(arr, 5, v5)
    if size == 6:
        return arr
    xs_array_set_float(arr, 6, v6)
    if size == 7:
        return arr
    xs_array_set_float(arr, 7, v7)
    if size == 8:
        return arr
    xs_array_set_float(arr, 8, v8)
    if size == 9:
        return arr
    xs_array_set_float(arr, 9, v9)
    if size == 10:
        return arr
    xs_array_set_float(arr, 10, v10)
    if size == 11:
        return arr
    xs_array_set_float(arr, 11, v11)
    return arr


def xs_float_array_from_repeated_val(value: float32 = float32(0.0), times: int32 = int32(0)) -> int32:
    """
    Creates an array by repeating a single value.
    :param value: value to repeat
    :param times: number of times to repeat the value
    :return: created array id, or `c_float_array_generic_error` on error
    """
    if times < 0 or times >= c_float_array_max_capacity:
        return c_float_array_generic_error
    arr: int32 = xs_array_create_float(times, value)
    if arr < 0:
        return c_float_array_generic_error
    return arr


def xs_float_array_from_repeated_array(arr: int32 = int32(-1), times: int32 = int32(0)) -> int32:
    """
    Creates a new array by repeating all elements of the given array.
    :param arr: source array id
    :param times: number of times to repeat the array contents
    :return: created array id, `c_float_array_max_capacity_error` if the result is too large, or `c_float_array_generic_error` on other errors
    """
    if times < 0:
        return c_float_array_generic_error
    size: int32 = xs_array_get_size(arr)
    if times > 0 and size > (c_float_array_max_capacity // times):
        return c_float_array_max_capacity_error
    new_size: int32 = size * times
    if new_size >= c_float_array_max_capacity:
        return c_float_array_max_capacity_error
    new_arr: int32 = xs_array_create_float(new_size)
    if new_arr < 0:
        return c_float_array_generic_error
    for i in i32range(0, size):
        val: float32 = xs_array_get_float(arr, i)
        j: int32 = i
        while j < new_size:
            xs_array_set_float(new_arr, j, val)
            j += size
    return new_arr


def xs_float_array_index(arr: int32 = int32(-1), value: float32 = float32(-1.0), start: int32 = int32(0), stop: int32 = c_float_array_empty_int_param) -> int32:
    """
    Returns the index of the first occurrence of the value within the optional [start, stop) range. Negative start/stop are relative to the end.
    :param arr: array id
    :param value: value to search for
    :param start: start of search range (inclusive)
    :param stop: end of search range (exclusive), defaults to array size
    :return: index of the value, or `c_float_array_generic_error` if not found
    """
    size: int32 = xs_array_get_size(arr)

    if stop == c_float_array_empty_int_param or stop > size:
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
        if xs_array_get_float(arr, i) == value:
            return i
    return c_float_array_generic_error


def xs_float_array_contains(arr: int32 = int32(-1), value: float32 = float32(-1.0)) -> bool:
    """
    Checks whether the array contains the given value.
    :param arr: array id
    :param value: value to search for
    :return: true if the value is found, false otherwise
    """
    return xs_float_array_index(arr, value) > -1


def _xs_float_array_compare_elem(a: float32 = float32(-1.0), b: float32 = float32(-1.0), reverse: bool = False) -> bool:
    if reverse:
        return a > b
    return a < b


def _xs_float_array_insertion_sort_with(arr: int32 = int32(-1), other: int32 = int32(-1), lo: int32 = int32(0),
                                        hi: int32 = int32(0), reverse: bool = False) -> None:
    has_other: bool = other >= 0
    for i in i32range(lo + 1, hi):
        key: float32 = xs_array_get_float(arr, i)
        value: int32 = int32(0)
        if has_other:
            value = xs_array_get_int(other, i)
        j: int32 = i - 1
        shifting: bool = True
        while shifting and j >= lo:
            prev: float32 = xs_array_get_float(arr, j)
            if _xs_float_array_compare_elem(key, prev, reverse):
                xs_array_set_float(arr, j + 1, prev)
                if has_other:
                    xs_array_set_int(other, j + 1, xs_array_get_int(other, j))
                j -= 1
            else:
                shifting = False
        xs_array_set_float(arr, j + 1, key)
        if has_other:
            xs_array_set_int(other, j + 1, value)


def _xs_float_array_sift_down(arr: int32 = int32(-1), start: int32 = int32(-1), end: int32 = int32(-1), reverse: bool = False) -> None:
    root: int32 = start
    val: float32 = xs_array_get_float(arr, root)
    sifting: bool = True
    while sifting:
        child: int32 = 2 * root + 1
        if child > end:
            sifting = False
        else:
            child_val: float32 = xs_array_get_float(arr, child)
            if child + 1 <= end:
                child_val1: float32 = xs_array_get_float(arr, child + 1)
                if _xs_float_array_compare_elem(child_val, child_val1, reverse):
                    child += 1
                    child_val = child_val1
            if _xs_float_array_compare_elem(val, child_val, reverse):
                xs_array_set_float(arr, root, child_val)
                root = child
            else:
                sifting = False
    xs_array_set_float(arr, root, val)


def xs_float_array_sort(arr: int32 = int32(-1), reverse: bool = False) -> None:
    """
    Sorts the array in-place.
    :param arr: array id
    :param reverse: if true, sorts in descending order
    """
    size: int32 = xs_array_get_size(arr)
    if size <= _c_float_array_sort_run:
        _xs_float_array_insertion_sort_with(arr, int32(-1), int32(0), size, reverse)
        return
    for start in i32range(size // 2 - 1, -1, -1):
        _xs_float_array_sift_down(arr, start, size - 1, reverse)

    for end in i32range(size - 1, 0, -1):
        temp: float32 = xs_array_get_float(arr, 0)
        xs_array_set_float(arr, 0, xs_array_get_float(arr, end))
        xs_array_set_float(arr, end, temp)
        _xs_float_array_sift_down(arr, int32(0), end - 1, reverse)


def _xs_float_array_ensure_sort_buffers(size: int32 = int32(0)) -> int32:
    global _float_array_sort_keys, _float_array_sort_values
    if _float_array_sort_keys < 0:
        _float_array_sort_keys = xs_array_create_float(size)
        if _float_array_sort_keys < 0:
            return c_float_array_generic_error
    if _float_array_sort_values < 0:
        _float_array_sort_values = xs_array_create_int(size)
        if _float_array_sort_values < 0:
            return c_float_array_generic_error
    r: int32 = int32(1)
    if xs_array_get_size(_float_array_sort_keys) < size:
        r = xs_array_resize_float(_float_array_sort_keys, size)
        if r != 1:
            return c_float_array_resize_failed_error
    if xs_array_get_size(_float_array_sort_values) < size:
        r = xs_array_resize_int(_float_array_sort_values, size)
        if r != 1:
            return c_float_array_resize_failed_error
    return c_float_array_success


def _xs_float_array_release_sort_buffers(release_buffers: bool = True) -> None:
    if not release_buffers:
        return
    if _float_array_sort_keys >= 0:
        xs_array_resize_float(_float_array_sort_keys, 0)
    if _float_array_sort_values >= 0:
        xs_array_resize_int(_float_array_sort_values, 0)


def _xs_float_array_merge_with(src: int32 = int32(-1), src_other: int32 = int32(-1), dst: int32 = int32(-1),
                               dst_other: int32 = int32(-1), lo: int32 = int32(0), mid: int32 = int32(0),
                               hi: int32 = int32(0), reverse: bool = False) -> None:
    i: int32 = lo
    j: int32 = mid
    k: int32 = lo
    if i < mid and j < hi:
        left: float32 = xs_array_get_float(src, i)
        right: float32 = xs_array_get_float(src, j)
        while i < mid and j < hi:
            if _xs_float_array_compare_elem(right, left, reverse):
                xs_array_set_float(dst, k, right)
                xs_array_set_int(dst_other, k, xs_array_get_int(src_other, j))
                j += 1
                if j < hi:
                    right = xs_array_get_float(src, j)
            else:
                xs_array_set_float(dst, k, left)
                xs_array_set_int(dst_other, k, xs_array_get_int(src_other, i))
                i += 1
                if i < mid:
                    left = xs_array_get_float(src, i)
            k += 1
    while i < mid:
        xs_array_set_float(dst, k, xs_array_get_float(src, i))
        xs_array_set_int(dst_other, k, xs_array_get_int(src_other, i))
        i += 1
        k += 1
    while j < hi:
        xs_array_set_float(dst, k, xs_array_get_float(src, j))
        xs_array_set_int(dst_other, k, xs_array_get_int(src_other, j))
        j += 1
        k += 1


def xs_float_array_sort_with(arr: int32 = int32(-1), other: int32 = int32(-1), reverse: bool = False, release_buffers: bool = True) -> int32:
    """
    Sorts the array in-place with a stable sort, and moves the elements of `other` the same way,
    so `other[i]` stays paired with `arr[i]`. Equal elements keep their original order.
    Inputs larger than 16 elements use two internal buffer arrays shared by all calls.
    :param arr: array id
    :param other: int array id of the same size as `arr`
    :param reverse: if true, sorts in descending order
    :param release_buffers: if true, resizes the internal buffers to 0 after sorting to free their memory;
        the same buffers are grown again on the next call
    :return: `c_float_array_success` on success, `c_float_array_generic_error` if the sizes differ or buffers
        can't be created, or `c_float_array_resize_failed_error` if the buffers can't grow
    """
    size: int32 = xs_array_get_size(arr)
    if xs_array_get_size(other) != size:
        return c_float_array_generic_error
    if size > _c_float_array_sort_run:
        r: int32 = _xs_float_array_ensure_sort_buffers(size)
        if r != c_float_array_success:
            _xs_float_array_release_sort_buffers(release_buffers)
            return r
    run_start: int32 = int32(0)
    while run_start < size:
        run_end: int32 = run_start + _c_float_array_sort_run
        if run_end > size:
            run_end = size
        _xs_float_array_insertion_sort_with(arr, other, run_start, run_end, reverse)
        run_start = run_end
    if size <= _c_float_array_sort_run:
        return c_float_array_success
    src: int32 = arr
    src_other: int32 = other
    dst: int32 = _float_array_sort_keys
    dst_other: int32 = _float_array_sort_values
    in_buffers: bool = False
    width: int32 = _c_float_array_sort_run
    while width < size:
        lo: int32 = int32(0)
        while lo < size:
            mid: int32 = lo + width
            if mid > size:
                mid = size
            hi: int32 = mid + width
            if hi > size:
                hi = size
            _xs_float_array_merge_with(src, src_other, dst, dst_other, lo, mid, hi, reverse)
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
        for i in i32range(0, size):
            xs_array_set_float(arr, i, xs_array_get_float(src, i))
            xs_array_set_int(other, i, xs_array_get_int(src_other, i))
    _xs_float_array_release_sort_buffers(release_buffers)
    return c_float_array_success


def xs_float_array_to_string(arr: int32 = int32(-1), start: str = "[", sep: str = ", ", end: str = "]") -> str:
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
        s += str(xs_array_get_float(arr, i))
        if i < size - 1:
            s += sep
    s += end
    return s


def xs_float_array_copy(arr: int32 = int32(-1), start: int32 = int32(0), end: int32 = c_float_array_max_capacity) -> int32:
    """
    Returns a copy of the array, optionally sliced by [start, end). Negative start/end are relative to the end.
    :param arr: array id
    :param start: start of slice (inclusive)
    :param end: end of slice (exclusive), defaults to array size
    :return: new array id, or `c_float_array_generic_error` on error
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
    new_arr: int32 = xs_array_create_float(new_size)
    if new_arr < 0:
        return c_float_array_generic_error
    for i in i32range(fr, to):
        xs_array_set_float(new_arr, i - fr, xs_array_get_float(arr, i))
    return new_arr


def xs_float_array_delete(arr: int32 = int32(-1)) -> int32:
    """
    Resizes the array to 0 to free its memory. XS can't fully delete arrays,
    so the array id stays allocated and must not be used afterwards.
    :param arr: array id
    :return: `c_float_array_success` on success, or `c_float_array_resize_failed_error` if the resize fails
    """
    r: int32 = xs_array_resize_float(arr, 0)
    if r != 1:
        return c_float_array_resize_failed_error
    return c_float_array_success


def xs_float_array_compare(arr1: int32 = int32(-1), arr2: int32 = int32(-1)) -> int32:
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
        v1: float32 = xs_array_get_float(arr1, i)
        v2: float32 = xs_array_get_float(arr2, i)
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


def xs_float_array_reverse(arr: int32 = int32(-1)) -> None:
    """
    Reverses the array in-place.
    :param arr: array id
    """
    size: int32 = xs_array_get_size(arr)
    mid: int32 = size // 2
    for i in i32range(0, mid):
        temp: float32 = xs_array_get_float(arr, i)
        back_i: int32 = size - i - 1
        xs_array_set_float(arr, i, xs_array_get_float(arr, back_i))
        xs_array_set_float(arr, back_i, temp)


def xs_float_array_count(arr: int32 = int32(-1), value: float32 = float32(-1.0)) -> int32:
    """
    Counts the number of occurrences of a value in the array.
    :param arr: array id
    :param value: value to count
    :return: number of occurrences
    """
    count: int32 = int32(0)
    size: int32 = xs_array_get_size(arr)
    for i in i32range(0, size):
        if xs_array_get_float(arr, i) == value:
            count += 1
    return count


def xs_float_array_sum(arr: int32 = int32(-1)) -> float32:
    """
    Returns the sum of all elements in the array.
    :param arr: array id
    :return: sum of elements
    """
    s: float32 = float32(0.0)
    size: int32 = xs_array_get_size(arr)
    for i in i32range(0, size):
        s += xs_array_get_float(arr, i)
    return s


def xs_float_array_min(arr: int32 = int32(-1)) -> float32:
    """
    Returns the minimum value in the array. Sets last error on failure.
    :param arr: array id
    :return: minimum value, or `c_float_array_generic_error_float` on error
    """
    global _float_array_last_operation_status
    size: int32 = xs_array_get_size(arr)
    if size <= 0:
        _float_array_last_operation_status = c_float_array_index_out_of_range_error
        return c_float_array_generic_error_float
    m: float32 = xs_array_get_float(arr, 0)
    for i in i32range(1, size):
        v: float32 = xs_array_get_float(arr, i)
        if v < m:
            m = v
    _float_array_last_operation_status = c_float_array_success
    return m


def xs_float_array_max(arr: int32 = int32(-1)) -> float32:
    """
    Returns the maximum value in the array. Sets last error on failure.
    :param arr: array id
    :return: maximum value, or `c_float_array_generic_error_float` on error
    """
    global _float_array_last_operation_status
    size: int32 = xs_array_get_size(arr)
    if size <= 0:
        _float_array_last_operation_status = c_float_array_index_out_of_range_error
        return c_float_array_generic_error_float
    m: float32 = xs_array_get_float(arr, 0)
    for i in i32range(1, size):
        v: float32 = xs_array_get_float(arr, i)
        if v > m:
            m = v
    _float_array_last_operation_status = c_float_array_success
    return m


def xs_float_array_last_error() -> int32:
    """
    Returns the status code of the last operation that sets it (min, max).
    :return: `c_float_array_success` if the last such operation succeeded, or a negative error code
    """
    return _float_array_last_operation_status


def xs_float_array_from_string(items: str = "") -> int32:
    """
    Creates an array from a comma separated string, e.g. `"1.0,1.5,-2.25"`.
    Items are trimmed, and items that cannot be parsed are skipped.
    :param items: comma separated values
    :return: created array id, or `c_float_array_generic_error` on error
    """
    if str_trim(items) == "":
        return xs_array_create_float(0)
    parts: int32 = str_split(items, ",")
    num_parts: int32 = xs_array_get_size(parts)
    arr: int32 = xs_array_create_float(num_parts)
    if arr < 0:
        xs_array_resize_string(parts, 0)
        return c_float_array_generic_error
    size: int32 = int32(0)
    for i in i32range(0, num_parts):
        item: str = str_trim(xs_array_get_string(parts, i))
        value: float32 = str_to_float(item, c_float_array_empty_param)
        if value != c_float_array_empty_param:
            xs_array_set_float(arr, size, value)
            size += 1
    xs_array_resize_string(parts, 0)
    if size < num_parts:
        r: int32 = xs_array_resize_float(arr, size)
        if r != 1:
            return c_float_array_resize_failed_error
    return arr
