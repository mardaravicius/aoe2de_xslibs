from numpy import int32

from xs_converter.converter import PythonToXsConverter
from xs_converter.functions import xs_array_create_int, xs_array_set_int, xs_array_resize_int, xs_array_get_int, \
    xs_array_get_size, xs_chat_data, abs
from xs_converter.symbols import XsExternConst, i32range

c_int_list_success = int32(0)
c_int_list_generic_error = int32(-1)
c_int_list_index_out_of_range_error = int32(-2)
c_int_list_resize_failed_error = int32(-3)
c_int_list_max_capacity_error = int32(-4)
c_int_list_max_capacity = int32(999999999)
c_int_list_empty_param = -int32(999999999)
_int_list_last_operation_status = c_int_list_success


def constants() -> None:
    c_int_list_success: XsExternConst[int32] = int32(0)
    c_int_list_generic_error: XsExternConst[int32] = int32(-1)
    c_int_list_index_out_of_range_error: XsExternConst[int32] = int32(-2)
    c_int_list_resize_failed_error: XsExternConst[int32] = int32(-3)
    c_int_list_max_capacity_error: XsExternConst[int32] = int32(-4)
    c_int_list_max_capacity: XsExternConst[int32] = int32(999999999)
    c_int_list_empty_param: XsExternConst[int32] = int32(-999999999)
    _int_list_last_operation_status: int32 = c_int_list_success


def xs_int_list_create(capacity: int32 = int32(7)) -> int32:
    """
    Creates empty list for int values. List is a dynamic array that grows and shrinks as values are added and removed.
    :param capacity: initial list capacity
    :return: created list id, or error if negative
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
    Creates a list with provided values. The first value that equals `cIntListEmptyParam` will stop further insertion.
    This Function can create a list with 12 values at the maximum, but further values can be added with other functions.
    :param v1 through v11: value at a given index of a list
    :return: created list id, or error if negative
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


def xs_int_list_from_range(start: int32 = int32(0), stop: int32 = int32(0), step: int32 = int32(1)) -> int32:
    """
    Creates a list from a given range.
    :param start: Start
    :param stop:
    :param step:
    :return: created list id, or error if negative
    """
    if step == 0:
        return c_int_list_generic_error
    if step > 0 and start > stop:
        return c_int_list_generic_error
    if step < 0 and start < stop:
        return c_int_list_generic_error
    distance: int32 = int32(abs(stop - start))
    stepa: int32 = int32(abs(step))
    size: int32 = distance // stepa
    if size >= c_int_list_max_capacity:
        return c_int_list_generic_error
    remain: int32 = distance % stepa
    if remain > 0:
        size += 1
    lst: int32 = xs_array_create_int(size + 1)
    if lst < 0:
        return c_int_list_generic_error
    i: int32 = int32(1)
    if step > 0:
        while start < stop:
            xs_array_set_int(lst, i, start)
            start += step
            i += 1
    else:
        while start > stop:
            xs_array_set_int(lst, i, start)
            start += step
            i += 1
    xs_array_set_int(lst, 0, size)
    return lst


def xs_int_list_from_repeated_val(value: int32 = int32(0), times: int32 = int32(0)) -> int32:
    if times < 0 or times >= c_int_list_max_capacity:
        return c_int_list_generic_error
    lst: int32 = xs_array_create_int(times + 1, value)
    if lst < 0:
        return c_int_list_generic_error
    xs_array_set_int(lst, 0, times)
    return lst


def xs_int_list_from_repeated_list(lst: int32 = int32(-1), times: int32 = int32(0)) -> int32:
    size: int32 = xs_array_get_int(lst, 0)
    new_capacity: int32 = (size * times) + 1
    if new_capacity > c_int_list_max_capacity:
        return c_int_list_generic_error
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
    arr_size: int32 = xs_array_get_size(arr)
    lst: int32 = xs_int_list_create(arr_size)
    if lst < 0:
        return lst
    for i in i32range(0, arr_size):
        xs_array_set_int(lst, i + 1, xs_array_get_int(arr, i))
    xs_array_set_int(lst, 0, arr_size)
    return lst


def xs_int_list_use_array_as_source(arr: int32 = int32(-1)) -> int32:
    arr_size: int32 = xs_array_get_size(arr)
    if arr_size + 1 > c_int_list_max_capacity:
        return c_int_list_max_capacity_error
    r: int32 = xs_array_resize_int(arr, arr_size + 1)
    if r < 0:
        return c_int_list_resize_failed_error
    for i in i32range(arr_size - 1, -1, -1):
        xs_array_set_int(arr, i + 1, xs_array_get_int(arr, i))
    xs_array_set_int(arr, 0, arr_size)
    return c_int_list_success


def xs_int_list_get(lst: int32 = int32(-1), idx: int32 = int32(-1)) -> int32:
    global _int_list_last_operation_status
    size: int32 = xs_array_get_int(lst, 0)
    if idx < 0 or idx >= size:
        _int_list_last_operation_status = c_int_list_index_out_of_range_error
        return c_int_list_generic_error
    _int_list_last_operation_status = c_int_list_success
    return xs_array_get_int(lst, idx + 1)


def xs_int_list_set(lst: int32 = int32(-1), idx: int32 = int32(-1), value: int32 = int32(0)) -> int32:
    size: int32 = xs_array_get_int(lst, 0)
    if idx < 0 or idx >= size:
        return c_int_list_index_out_of_range_error
    xs_array_set_int(lst, idx + 1, value)
    return c_int_list_success


def xs_int_list_size(lst: int32 = int32(-1)) -> int32:
    return xs_array_get_int(lst, 0)


def _xs_int_list_extend_int_array(lst: int32 = int32(-1), capacity: int32 = int32(0)) -> int32:
    if capacity == c_int_list_max_capacity:
        return c_int_list_max_capacity_error
    new_capacity: int32 = capacity * 2
    if new_capacity > c_int_list_max_capacity:
        new_capacity = c_int_list_max_capacity
    r: int32 = xs_array_resize_int(lst, new_capacity)
    if r != 1:
        return c_int_list_resize_failed_error
    return c_int_list_success


def _xs_int_list_shrink_int_array(lst: int32 = int32(-1), size: int32 = int32(0), capacity: int32 = int32(0)) -> int32:
    if size <= (capacity // 2):
        r: int32 = xs_array_resize_int(lst, size)
        if r != 1:
            return c_int_list_resize_failed_error
    return c_int_list_success


def xs_int_list_append(lst: int32 = int32(-1), value: int32 = int32(0)) -> int32:
    capacity: int32 = xs_array_get_size(lst)
    size: int32 = xs_array_get_int(lst, 0)
    next_idx: int32 = size + 1
    if capacity == next_idx:
        r: int32 = _xs_int_list_extend_int_array(lst, capacity)
        if r != c_int_list_success:
            return r
    xs_array_set_int(lst, next_idx, value)
    xs_array_set_int(lst, 0, next_idx)
    return c_int_list_success


# def xs_int_list_pop(lst: int32 = int32(-1)) -> int32:
#     global _int_array_list_last_operation_status
#     capacity: int32 = xs_array_get_size(lst)
#     size: int32 = xs_array_get_int(lst, 0)
#     if size == 0:
#         _int_array_list_last_operation_status = c_int_list_index_out_of_range_error
#         return c_int_list_generic_error
#     removed_elem: int32 = xs_array_get_int(lst, size)
#     r: int32 = _shrink_int_array(lst, size, capacity)
#     if r != c_int_list_success:
#         _int_array_list_last_operation_status = r
#         return c_int_list_generic_error
#     xs_array_set_int(lst, 0, size - 1)
#     _int_array_list_last_operation_status = c_int_list_success
#     return removed_elem


def xs_int_list_insert(lst: int32 = int32(-1), idx: int32 = int32(-1), value: int32 = int32(0)) -> int32:
    capacity: int32 = xs_array_get_size(lst)
    size: int32 = xs_array_get_int(lst, 0)
    if idx < 0 or idx > size:
        return c_int_list_index_out_of_range_error
    new_size: int32 = size + 1
    if capacity == new_size:
        r: int32 = _xs_int_list_extend_int_array(lst, capacity)
        if r != c_int_list_success:
            return r
    for i in i32range(size, idx, -1):
        xs_array_set_int(lst, i + 1, xs_array_get_int(lst, i))
    xs_array_set_int(lst, idx + 1, value)
    xs_array_set_int(lst, 0, new_size)

    return c_int_list_success


def xs_int_list_pop(lst: int32 = int32(-1), idx: int32 = c_int_list_max_capacity) -> int32:
    global _int_list_last_operation_status
    capacity: int32 = xs_array_get_size(lst)
    size: int32 = xs_array_get_int(lst, 0)
    if idx == c_int_list_max_capacity:
        idx = size - 1
    elif idx < 0 or idx >= size:
        _int_list_last_operation_status = c_int_list_index_out_of_range_error
        return c_int_list_generic_error
    removed_elem: int32 = xs_array_get_int(lst, idx + 1)
    for i in i32range(idx + 2, size + 1):
        xs_array_set_int(lst, i - 1, xs_array_get_int(lst, i))
    r: int32 = _xs_int_list_shrink_int_array(lst, size, capacity)
    if r != c_int_list_success:
        _int_list_last_operation_status = r
        return c_int_list_generic_error
    xs_array_set_int(lst, 0, size - 1)
    _int_list_last_operation_status = c_int_list_success
    return removed_elem


def xs_int_list_remove(lst: int32 = int32(-1), value: int32 = int32(-1)) -> int32:
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
    r: int32 = _xs_int_list_shrink_int_array(lst, size, capacity)
    if r != c_int_list_success:
        return r
    xs_array_set_int(lst, 0, size - 1)
    return found_idx - 1


def xs_int_list_index(lst: int32 = int32(-1), value: int32 = int32(-1), start: int32 = int32(0), stop: int32 = c_int_list_empty_param) -> int32:
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
        child_val1: int32 = xs_array_get_int(lst, child + 1)
        if child + 1 <= end and _xs_int_list_compare_elem(child_val, child_val1, reverse):
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
    global _int_list_last_operation_status
    size: int32 = xs_array_get_int(lst, 0)
    for start in i32range(size // 2, 0, -1):
        _xs_int_list_sift_down(lst, start, size, reverse)

    for end in i32range(size, 1, -1):
        temp: int32 = xs_array_get_int(lst, 1)
        xs_array_set_int(lst, 1, xs_array_get_int(lst, end))
        xs_array_set_int(lst, end, temp)
        _xs_int_list_sift_down(lst, 1, end - 1, reverse)


def xs_int_list_to_string(lst: int32 = int32(-1)) -> str:
    size: int32 = xs_array_get_int(lst, 0)
    s: str = "["
    for i in i32range(1, size + 1):
        s += str(xs_array_get_int(lst, i))
        if i < size:
            s += ", "
    s += "]"
    return s


def xs_int_list_copy(lst: int32 = int32(-1), start: int32 = int32(0), end: int32 = c_int_list_max_capacity) -> int32:
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
    for i in i32range(fr, to + 1):
        xs_array_set_int(new_lst, i - fr, xs_array_get_int(lst, i))
    xs_array_set_int(new_lst, 0, new_size)
    return new_lst


def xs_int_list_extend(source: int32 = int32(-1), lst: int32 = int32(-1)) -> int32:
    source_size: int32 = xs_array_get_int(source, 0)
    to_add: int32 = xs_array_get_int(lst, 0)
    capacity: int32 = xs_array_get_size(source)
    new_size: int32 = source_size + to_add
    if new_size > capacity:
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
    source_size: int32 = xs_array_get_int(source, 0)
    to_add: int32 = xs_array_get_size(arr)
    capacity: int32 = xs_array_get_size(source)
    new_size: int32 = source_size + to_add
    if new_size > capacity:
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
    capacity: int32 = xs_array_get_int(lst, 0)
    if capacity > 8:
        r: int32 = xs_array_resize_int(lst, 8)
        if r != 1:
            return c_int_list_resize_failed_error
    xs_array_set_int(lst, 0, 0)
    return c_int_list_success


def xs_int_list_compare(lst1: int32 = int32(-1), lst2: int32 = int32(-1)) -> int32:
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
    size: int32 = xs_array_get_int(lst, 0)
    mid: int32 = (size + 2) // 2
    for i in i32range(1, mid):
        temp: int32 = xs_array_get_int(lst, i)
        back_i: int32 = size - i + 1
        xs_array_set_int(lst, i, xs_array_get_int(lst, back_i))
        xs_array_set_int(lst, back_i, temp)


def xs_int_list_count(arr: int32 = int32(-1), value: int32 = int32(-1)) -> int32:
    count: int32 = int32(0)
    size: int32 = xs_array_get_int(arr, 0)
    for i in i32range(1, size + 1):
        if xs_array_get_int(arr, i) == value:
            count += 1
    return count


def xs_int_list_sum(arr: int32 = int32(-1)) -> int32:
    s: int32 = int32(0)
    size: int32 = xs_array_get_int(arr, 0)
    for i in i32range(1, size + 1):
        s += xs_array_get_int(arr, i)
    return s


def xs_int_list_min(arr: int32 = int32(-1)) -> int32:
    global _int_list_last_operation_status
    size: int32 = xs_array_get_int(arr, 0)
    if size == 0:
        _int_list_last_operation_status = c_int_list_index_out_of_range_error
        return c_int_list_generic_error
    m: int32 = xs_array_get_int(arr, 1)
    if size == 1:
        _int_list_last_operation_status = c_int_list_success
        return m
    for i in i32range(2, size + 1):
        v: int32 = xs_array_get_int(arr, i)
        if v < m:
            m = v
    _int_list_last_operation_status = c_int_list_success
    return m


def xs_int_list_max(arr: int32 = int32(-1)) -> int32:
    global _int_list_last_operation_status
    size: int32 = xs_array_get_int(arr, 0)
    if size == 0:
        _int_list_last_operation_status = c_int_list_index_out_of_range_error
        return c_int_list_generic_error
    m: int32 = xs_array_get_int(arr, 1)
    if size == 1:
        _int_list_last_operation_status = c_int_list_success
        return m
    for i in i32range(2, size + 1):
        v: int32 = xs_array_get_int(arr, i)
        if v > m:
            m = v
    _int_list_last_operation_status = c_int_list_success
    return m


def xs_int_list_last_error() -> int32:
    return _int_list_last_operation_status


def test() -> None:
    arr: int32 = xs_array_create_int(20)
    xs_chat_data("arr: " + str(arr))
    xs_int_list_append(arr, int32(1))
    xs_int_list_append(arr, int32(2))
    xs_int_list_append(arr, int32(3))
    xs_chat_data(xs_int_list_to_string(arr))
    xs_chat_data("pop 1: " + str(xs_int_list_pop(arr)))
    xs_chat_data("pop 2: " + str(xs_int_list_pop(arr)))
    xs_chat_data(xs_int_list_to_string(arr))
    xs_chat_data("pop 3: " + str(xs_int_list_pop(arr)))
    xs_chat_data("pop 4: " + str(xs_int_list_pop(arr)))
    xs_int_list_insert(arr, int32(0), int32(1))
    xs_int_list_insert(arr, int32(0), int32(2))
    xs_int_list_insert(arr, int32(0), int32(3))
    xs_int_list_insert(arr, int32(1), int32(4))
    xs_int_list_insert(arr, int32(1), int32(5))
    xs_int_list_insert(arr, int32(5), int32(6))
    xs_int_list_insert(arr, int32(7), int32(7))
    xs_chat_data(xs_int_list_to_string(arr))
    xs_int_list_sort(arr, True)
    xs_chat_data(xs_int_list_to_string(arr))


def int_list(include_test: bool) -> tuple[str, str]:
    constants_function_xs = PythonToXsConverter.to_xs_script(
        constants,
        indent=True,
    )
    constants_xs = (constants_function_xs[constants_function_xs.find("extern"):constants_function_xs.rfind("}")]
                    .strip()
                    .replace("    ", "")
                    ) + "\n\n"
    xs = constants_xs + PythonToXsConverter.to_xs_script(
        xs_int_list,
        xs_int_list_create,
        xs_int_list_from_range,
        xs_int_list_from_repeated_val,
        xs_int_list_from_repeated_list,
        xs_int_list_from_array,
        xs_int_list_use_array_as_source,
        xs_int_list_get,
        xs_int_list_set,
        xs_int_list_size,
        _xs_int_list_extend_int_array,
        _xs_int_list_shrink_int_array,
        xs_int_list_to_string,
        xs_int_list_append,
        xs_int_list_pop,
        xs_int_list_insert,
        xs_int_list_remove,
        xs_int_list_index,
        xs_int_list_contains,
        _xs_int_list_compare_elem,
        _xs_int_list_sift_down,
        xs_int_list_sort,
        xs_int_list_clear,
        xs_int_list_copy,
        xs_int_list_extend,
        xs_int_list_extend_with_array,
        xs_int_list_compare,
        xs_int_list_count,
        xs_int_list_sum,
        xs_int_list_min,
        xs_int_list_max,
        xs_int_list_last_error,
        indent=True,
    )
    if include_test:
        xs += constants_xs + PythonToXsConverter.to_xs_script(
            test,
            indent=True,
        )
    print(xs)
    return (xs, "intList")


if __name__ == '__main__':
    int_list(True)
