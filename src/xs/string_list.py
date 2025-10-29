from numpy import int32, float32

from xs_converter.converter import PythonToXsConverter
from xs_converter.functions import xs_array_get_size, xs_chat_data, xs_array_get_int, xs_array_create_string, \
    xs_array_create_int, xs_array_set_string, xs_array_set_int, xs_array_get_string, xs_array_resize_string
from xs_converter.symbols import XsExternConst, i32range

c_string_list_success = int32(0)
c_string_list_generic_error = int32(-1)
c_string_list_index_out_of_range_error = int32(-2)
c_string_list_resize_failed_error = int32(-3)
c_string_list_max_capacity_error = int32(-4)
c_string_list_max_capacity = int32(999999999)
c_string_list_empty_param = ""
_int_list_last_operation_status = c_string_list_success


def constants() -> None:
    c_string_list_success: XsExternConst[int32] = int32(0)
    c_string_list_generic_error: XsExternConst[int32] = int32(-1)
    c_string_list_index_out_of_range_error: XsExternConst[int32] = int32(-2)
    c_string_list_resize_failed_error: XsExternConst[int32] = int32(-3)
    c_string_list_max_capacity_error: XsExternConst[int32] = int32(-4)
    c_string_list_max_capacity: XsExternConst[int32] = int32(999999999)
    c_string_list_empty_param: XsExternConst[str] = ""
    _int_list_last_operation_status: int32 = c_string_list_success


def xs_string_list_size(lst: int32 = int32(-1)) -> int32:
    return xs_array_get_int(lst, 0)
#
#
# def _xs_string_list_set_size(lst: int32 = int32(-1), size: int32 = int32(0)) -> None:
#     xs_array_set_float(lst, 0, bit_cast_to_float(size))


def xs_string_list_create(capacity: int32 = int32(7)) -> int32:
    """
    Creates empty list for float values. List is a dynamic array that grows and shrinks as values are added and removed.
    :param capacity: initial list capacity
    :return: created list id, or error if negative
    """
    if capacity < 0 or capacity >= c_string_list_max_capacity:
        return c_string_list_generic_error
    lst: int32 = xs_array_create_int(2, 0)
    str_lst: int32 = xs_array_create_string(capacity)
    if lst < 0 or str_lst < 0:
        return c_string_list_generic_error
    xs_array_set_int(lst, 1, str_lst)
    return lst


def xs_string_list(
        v0: str = c_string_list_empty_param,
        v1: str = c_string_list_empty_param,
        v2: str = c_string_list_empty_param,
        v3: str = c_string_list_empty_param,
        v4: str = c_string_list_empty_param,
        v5: str = c_string_list_empty_param,
        v6: str = c_string_list_empty_param,
        v7: str = c_string_list_empty_param,
        v8: str = c_string_list_empty_param,
        v9: str = c_string_list_empty_param,
        v10: str = c_string_list_empty_param,
        v11: str = c_string_list_empty_param,
) -> int32:
    """
    Creates a list with provided values. The first value that equals `cIntListEmptyParam` will stop further insertion.
    This Function can create a list with 12 values at the maximum, but further values can be added with other functions.
    :param v1 through v11: value at a given index of a list
    :return: created list id, or error if negative
    """
    str_lst: int32 = xs_array_create_string(12)
    lst: int32 = xs_array_create_int(2, str_lst)
    if str_lst < 0 or lst < 0:
        return c_string_list_generic_error
    if v0 == c_string_list_empty_param:
        xs_array_set_int(lst, 0, int32(0))
        return str_lst
    xs_array_set_string(str_lst, 0, v0)
    if v1 == c_string_list_empty_param:
        xs_array_set_int(lst, 0, int32(1))
        return str_lst
    xs_array_set_string(str_lst, 1, v1)
    if v2 == c_string_list_empty_param:
        xs_array_set_int(lst, 0, int32(2))
        return str_lst
    xs_array_set_string(str_lst, 2, v2)
    if v3 == c_string_list_empty_param:
        xs_array_set_int(lst, 0, int32(3))
        return str_lst
    xs_array_set_string(str_lst, 3, v3)
    if v4 == c_string_list_empty_param:
        xs_array_set_int(lst, 0, int32(4))
        return str_lst
    xs_array_set_string(str_lst, 4, v4)
    if v5 == c_string_list_empty_param:
        xs_array_set_int(lst, 0, int32(5))
        return str_lst
    xs_array_set_string(str_lst, 5, v5)
    if v6 == c_string_list_empty_param:
        xs_array_set_int(lst, 0, int32(6))
        return str_lst
    xs_array_set_string(str_lst, 6, v6)
    if v7 == c_string_list_empty_param:
        xs_array_set_int(lst, 0, int32(7))
        return str_lst
    xs_array_set_string(str_lst, 7, v7)
    if v8 == c_string_list_empty_param:
        xs_array_set_int(lst, 0, int32(8))
        return str_lst
    xs_array_set_string(str_lst, 8, v8)
    if v9 == c_string_list_empty_param:
        xs_array_set_int(lst, 0, int32(9))
        return str_lst
    xs_array_set_string(str_lst, 9, v9)
    if v10 == c_string_list_empty_param:
        xs_array_set_int(lst, 0, int32(10))
        return str_lst
    xs_array_set_string(str_lst, 10, v10)
    if v11 == c_string_list_empty_param:
        xs_array_set_int(lst, 0, int32(11))
        return str_lst
    xs_array_set_string(str_lst, 11, v11)
    xs_array_set_int(lst, 0, int32(12))
    return lst


def xs_string_list_from_repeated_val(value: str = "", times: int32 = int32(0)) -> int32:
    if times < 0 or times >= c_string_list_max_capacity:
        return c_string_list_generic_error
    lst: int32 = xs_array_create_int(2, times)
    str_lst: int32 = xs_array_create_string(times, value)
    if str_lst < 0 or lst < 0:
        return c_string_list_generic_error
    xs_array_set_int(lst, 1, str_lst)
    return lst


def xs_string_list_from_repeated_list(lst: int32 = int32(-1), times: int32 = int32(0)) -> int32:
    size: int32 = xs_string_list_size(lst)
    new_capacity: int32 = (size * times)
    if new_capacity > c_string_list_max_capacity:
        return c_string_list_generic_error
    new_str_lst: int32 = xs_array_create_string(new_capacity)
    new_lst: int32 = xs_array_create_int(2, new_capacity)
    if new_str_lst < 0 or new_lst < 0:
        return c_string_list_generic_error
    lst: int32 = xs_array_get_int(lst, 1)
    for i in i32range(0, size):
        val: str = xs_array_get_string(lst, i)
        j: int32 = i
        while j < new_capacity:
            xs_array_set_string(new_str_lst, j, val)
            j += size
    xs_array_set_int(new_lst, 1, new_str_lst)
    return new_lst


def xs_string_list_from_array(arr: int32 = int32(-1)) -> int32:
    arr_size: int32 = xs_array_get_size(arr)
    new_str_lst: int32 = xs_array_create_string(2)
    lst: int32 = xs_array_create_int(2, arr_size)
    if lst < 0 or new_str_lst < 0:
        return c_string_list_generic_error
    for i in i32range(0, arr_size):
        xs_array_set_string(new_str_lst, i, xs_array_get_string(arr, i))
    xs_array_set_int(lst, 1, new_str_lst)
    return lst


def xs_string_list_use_array_as_source(arr: int32 = int32(-1)) -> int32:
    arr_size: int32 = xs_array_get_size(arr)
    if arr_size > c_string_list_max_capacity:
        return c_string_list_max_capacity_error
    lst: int32 = xs_array_create_int(2, arr_size)
    if lst < 0:
        return c_string_list_generic_error
    xs_array_set_int(lst, 1, arr)
    return lst


def xs_string_list_get(lst: int32 = int32(-1), idx: int32 = int32(-1)) -> str:
    global _int_list_last_operation_status
    size: int32 = xs_string_list_size(lst)
    if idx < 0 or idx >= size:
        _int_list_last_operation_status = c_string_list_index_out_of_range_error
        return str(c_string_list_generic_error)
    _int_list_last_operation_status = c_string_list_success
    return xs_array_get_string(xs_array_get_int(lst, 1), idx)


def xs_string_list_set(lst: int32 = int32(-1), idx: int32 = int32(-1), value: str = "") -> int32:
    size: int32 = xs_string_list_size(lst)
    if idx < 0 or idx >= size:
        return c_string_list_index_out_of_range_error
    xs_array_set_string(xs_array_get_int(lst, 1), idx, value)
    return c_string_list_success


def _xs_string_list_extend_string_array(lst: int32 = int32(-1), capacity: int32 = int32(0)) -> int32:
    if capacity == c_string_list_max_capacity:
        return c_string_list_max_capacity_error
    new_capacity: int32 = capacity * 2
    if new_capacity > c_string_list_max_capacity:
        new_capacity = c_string_list_max_capacity
    r: int32 = xs_array_resize_string(lst, new_capacity)
    if r != 1:
        return c_string_list_resize_failed_error
    return c_string_list_success


def _xs_string_list_shrink_int_array(lst: int32 = int32(-1), size: int32 = int32(0), capacity: int32 = int32(0)) -> int32:
    if size <= (capacity // 2):
        r: int32 = xs_array_resize_string(lst, size)
        if r != 1:
            return c_string_list_resize_failed_error
    return c_string_list_success


def xs_string_list_append(lst: int32 = int32(-1), value: str = "") -> int32:
    str_lst: int32 = xs_array_get_int(lst, 1)
    capacity: int32 = xs_array_get_size(str_lst)
    size: int32 = xs_string_list_size(lst)
    if capacity == size:
        r: int32 = _xs_string_list_extend_string_array(lst, capacity)
        if r != c_string_list_success:
            return r
    xs_array_set_string(str_lst, size, value)
    xs_array_set_int(lst, 0, size + 1)
    return c_string_list_success


def xs_string_list_insert(lst: int32 = int32(-1), idx: int32 = int32(-1), value: str = "") -> int32:
    str_lst: int32 = xs_array_get_int(lst, 1)
    capacity: int32 = xs_array_get_size(str_lst)
    size: int32 = xs_string_list_size(lst)
    if idx < 0 or idx > size:
        return c_string_list_index_out_of_range_error
    new_size: int32 = size + 1
    if capacity == new_size:
        r: int32 = _xs_string_list_extend_string_array(lst, capacity)
        if r != c_string_list_success:
            return r
    for i in i32range(size, idx, -1):
        xs_array_set_float(lst, i + 1, xs_array_get_float(lst, i))
    xs_array_set_float(lst, idx + 1, value)
    _xs_string_list_set_size(lst, new_size)

    return c_string_list_success


def xs_string_list_pop(lst: int32 = int32(-1), idx: int32 = c_string_list_max_capacity) -> float32:
    global _int_list_last_operation_status
    capacity: int32 = xs_array_get_size(lst)
    size: int32 = xs_string_list_size(lst)
    if idx == c_string_list_max_capacity:
        idx = size - 1
    elif idx < 0 or idx >= size:
        _int_list_last_operation_status = c_string_list_index_out_of_range_error
        return float32(c_string_list_generic_error)
    removed_elem: float32 = xs_array_get_float(lst, idx + 1)
    for i in i32range(idx + 2, size + 1):
        xs_array_set_float(lst, i - 1, xs_array_get_float(lst, i))
    r: int32 = _xs_string_list_shrink_int_array(lst, size, capacity)
    if r != c_string_list_success:
        _int_list_last_operation_status = r
        return float32(c_string_list_generic_error)
    _xs_string_list_set_size(lst, size - 1)
    _int_list_last_operation_status = c_string_list_success
    return removed_elem


def xs_string_list_remove(lst: int32 = int32(-1), value: float32 = float32(-1)) -> int32:
    capacity: int32 = xs_array_get_size(lst)
    size: int32 = xs_string_list_size(lst)
    found_idx: int32 = int32(-1)
    i: int32 = int32(1)
    while i <= size and found_idx == -1:
        c_val: float32 = xs_array_get_float(lst, i)
        if c_val == value:
            found_idx = i
        i += 1
    if found_idx == -1:
        return c_string_list_generic_error
    for j in i32range(found_idx + 1, size + 1):
        xs_array_set_float(lst, j - 1, xs_array_get_float(lst, j))
    r: int32 = _xs_string_list_shrink_int_array(lst, size, capacity)
    if r != c_string_list_success:
        return r
    _xs_string_list_set_size(lst, size - 1)
    return found_idx - 1


def xs_string_list_index(lst: int32 = int32(-1), value: float32 = float32(-1.0), start: int32 = int32(0), stop: int32 = c_string_list_empty_param) -> int32:
    size: int32 = xs_string_list_size(lst)

    if stop == c_string_list_empty_param or stop > size:
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
        if xs_array_get_float(lst, i + 1) == value:
            return i
    return c_string_list_generic_error


def xs_string_list_contains(lst: int32 = int32(-1), value: float32 = float32(-1.0)) -> bool:
    return xs_string_list_index(lst, value) > -1


def _xs_string_list_compare_elem(a: float32 = float32(-1.0), b: float32 = float32(-1.0), reverse: bool = False) -> bool:
    if reverse:
        return a > b
    return a < b


def _xs_string_list_sift_down(lst: int32 = int32(-1), start: int32 = int32(-1), end: int32 = int32(-1), reverse: bool = False) -> None:
    root: int32 = start
    while True:
        child: int32 = 2 * root
        if child > end:
            return
        child_val: float32 = xs_array_get_float(lst, child)
        child_val1: float32 = xs_array_get_float(lst, child + 1)
        if child + 1 <= end and _xs_string_list_compare_elem(child_val, child_val1, reverse):
            child += 1
            child_val = child_val1
        root_val: float32 = xs_array_get_float(lst, root)
        if _xs_string_list_compare_elem(root_val, child_val, reverse):
            xs_array_set_float(lst, root, child_val)
            xs_array_set_float(lst, child, root_val)
            root = child
        else:
            return


def xs_string_list_sort(lst: int32 = int32(-1), reverse: bool = False) -> None:
    global _int_list_last_operation_status
    size: int32 = xs_string_list_size(lst)
    for start in i32range(size // 2, 0, -1):
        _xs_string_list_sift_down(lst, start, size, reverse)

    for end in i32range(size, 1, -1):
        temp: float32 = xs_array_get_float(lst, 1)
        xs_array_set_float(lst, 1, xs_array_get_float(lst, end))
        xs_array_set_float(lst, end, temp)
        _xs_string_list_sift_down(lst, int32(1), end - 1, reverse)


def xs_string_list_to_string(lst: int32 = int32(-1)) -> str:
    size: int32 = xs_string_list_size(lst)
    s: str = "["
    for i in i32range(1, size + 1):
        s += str(xs_array_get_float(lst, i))
        if i < size:
            s += ", "
    s += "]"
    return s


def xs_string_list_copy(lst: int32 = int32(-1), start: int32 = int32(0), end: int32 = c_string_list_max_capacity) -> int32:
    size: int32 = xs_string_list_size(lst)
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
    new_lst: int32 = xs_array_create_float(new_size + 1)
    if new_lst < 0:
        return c_string_list_generic_error
    for i in i32range(fr, to + 1):
        xs_array_set_float(new_lst, i - fr, xs_array_get_float(lst, i))
    _xs_string_list_set_size(new_lst, new_size)
    return new_lst


def xs_string_list_extend(source: int32 = int32(-1), lst: int32 = int32(-1)) -> int32:
    source_size: int32 = xs_string_list_size(source)
    to_add: int32 = xs_string_list_size(lst)
    capacity: int32 = xs_array_get_size(source)
    new_size: int32 = source_size + to_add
    if new_size > capacity:
        if new_size >= c_string_list_max_capacity:
            return c_string_list_max_capacity_error
        r: int32 = xs_array_resize_float(source, new_size + 1)
        if r != 1:
            return c_string_list_resize_failed_error
    for i in i32range(1, to_add + 1):
        xs_array_set_float(source, i + source_size, xs_array_get_float(lst, i))
    _xs_string_list_set_size(source, new_size)
    return c_string_list_success


def xs_string_list_extend_with_array(source: int32 = int32(-1), arr: int32 = int32(-1)) -> int32:
    source_size: int32 = xs_string_list_size(source)
    to_add: int32 = xs_array_get_size(arr)
    capacity: int32 = xs_array_get_size(source)
    new_size: int32 = source_size + to_add
    if new_size > capacity:
        if new_size >= c_string_list_max_capacity or new_size < 0:
            return c_string_list_max_capacity_error
        r: int32 = xs_array_resize_float(source, new_size + 1)
        if r != 1:
            return c_string_list_resize_failed_error
    for i in i32range(0, to_add):
        xs_array_set_float(source, i + source_size + 1, xs_array_get_float(arr, i))
    _xs_string_list_set_size(source, new_size)
    return c_string_list_success


def xs_string_list_clear(lst: int32 = int32(-1)) -> int32:
    capacity: int32 = xs_string_list_size(lst)
    if capacity > 8:
        r: int32 = xs_array_resize_float(lst, 8)
        if r != 1:
            return c_string_list_resize_failed_error
    _xs_string_list_set_size(lst, float32(0.0))
    return c_string_list_success


def xs_string_list_compare(lst1: int32 = int32(-1), lst2: int32 = int32(-1)) -> int32:
    size1: int32 = xs_string_list_size(lst1)
    size2: int32 = xs_string_list_size(lst2)
    i: int32 = int32(1)
    while i <= size1 and i <= size2:
        v1: float32 = xs_array_get_float(lst1, i)
        v2: float32 = xs_array_get_float(lst2, i)
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
    size: int32 = xs_string_list_size(lst)
    mid: int32 = (size + 2) // 2
    for i in i32range(1, mid):
        temp: float32 = xs_array_get_float(lst, i)
        back_i: int32 = size - i + 1
        xs_array_set_float(lst, i, xs_array_get_float(lst, back_i))
        xs_array_set_float(lst, back_i, temp)


def xs_string_list_count(lst: int32 = int32(-1), value: float32 = float32(-1.0)) -> int32:
    count: int32 = int32(0)
    size: int32 = xs_string_list_size(lst)
    for i in i32range(1, size + 1):
        if xs_array_get_float(lst, i) == value:
            count += 1
    return count


def xs_string_list_sum(lst: int32 = int32(-1)) -> float32:
    s: float32 = float32(0.0)
    size: int32 = xs_string_list_size(lst)
    for i in i32range(1, size + 1):
        s += xs_array_get_float(lst, i)
    return s


def xs_string_list_min(lst: int32 = int32(-1)) -> float32:
    global _int_list_last_operation_status
    size: int32 = xs_string_list_size(lst)
    if size == 0:
        _int_list_last_operation_status = c_string_list_index_out_of_range_error
        return float32(c_string_list_generic_error)
    m: float32 = xs_array_get_float(lst, 1)
    if size == 1:
        _int_list_last_operation_status = c_string_list_success
        return m
    for i in i32range(2, size + 1):
        v: float32 = xs_array_get_float(lst, i)
        if v < m:
            m = v
    _int_list_last_operation_status = c_string_list_success
    return m


def xs_string_list_max(lst: int32 = int32(-1)) -> float32:
    global _int_list_last_operation_status
    size: int32 = xs_string_list_size(lst)
    if size == 0:
        _int_list_last_operation_status = c_string_list_index_out_of_range_error
        return float32(c_string_list_generic_error)
    m: float32 = xs_array_get_float(lst, 1)
    if size == 1:
        _int_list_last_operation_status = c_string_list_success
        return m
    for i in i32range(2, size + 1):
        v: float32 = xs_array_get_float(lst, i)
        if v > m:
            m = v
    _int_list_last_operation_status = c_string_list_success
    return m


def xs_string_list_last_error() -> int32:
    return _int_list_last_operation_status


def test() -> None:
    lst: int32 = xs_string_list_create(int32(20))
    xs_chat_data("arr: " + str(lst))
    xs_string_list_append(lst, float32(1))
    xs_string_list_append(lst, float32(2))
    xs_string_list_append(lst, float32(3))
    xs_chat_data(xs_string_list_to_string(lst))
    xs_chat_data("pop 1: " + str(xs_string_list_pop(lst)))
    xs_chat_data("pop 2: " + str(xs_string_list_pop(lst)))
    xs_chat_data(xs_string_list_to_string(lst))
    xs_chat_data("pop 3: " + str(xs_string_list_pop(lst)))
    xs_chat_data("pop 4: " + str(xs_string_list_pop(lst)))
    xs_string_list_insert(lst, int32(0), float32(1))
    xs_string_list_insert(lst, int32(0), float32(2))
    xs_string_list_insert(lst, int32(0), float32(3))
    xs_string_list_insert(lst, int32(1), float32(4))
    xs_string_list_insert(lst, int32(1), float32(5))
    xs_string_list_insert(lst, int32(5), float32(6))
    xs_string_list_insert(lst, int32(7), float32(7))
    xs_chat_data(xs_string_list_to_string(lst))
    xs_string_list_sort(lst, True)
    xs_chat_data(xs_string_list_to_string(lst))


def float_list(include_test: bool) -> tuple[str, str]:
    constants_function_xs = PythonToXsConverter.to_xs_script(
        constants,
        indent=True,
    )
    constants_xs = (constants_function_xs[constants_function_xs.find("extern"):constants_function_xs.rfind("}")]
                    .strip()
                    .replace("    ", "")
                    ) + "\n\n"
    xs = constants_xs + PythonToXsConverter.to_xs_script(
        xs_string_list_size,
        _xs_string_list_set_size,
        xs_string_list,
        xs_string_list_create,
        xs_string_list_from_repeated_val,
        xs_string_list_from_repeated_list,
        xs_string_list_from_array,
        xs_string_list_use_array_as_source,
        xs_string_list_get,
        xs_string_list_set,
        _xs_string_list_extend_string_array,
        _xs_string_list_shrink_int_array,
        xs_string_list_to_string,
        xs_string_list_append,
        xs_string_list_pop,
        xs_string_list_insert,
        xs_string_list_remove,
        xs_string_list_index,
        xs_string_list_contains,
        _xs_string_list_compare_elem,
        _xs_string_list_sift_down,
        xs_string_list_sort,
        xs_string_list_clear,
        xs_string_list_copy,
        xs_string_list_extend,
        xs_string_list_extend_with_array,
        xs_string_list_compare,
        xs_string_list_count,
        xs_string_list_sum,
        xs_string_list_min,
        xs_string_list_max,
        xs_string_list_last_error,
        indent=True,
    )
    if include_test:
        xs += constants_xs + PythonToXsConverter.to_xs_script(
            test,
            indent=True,
        )
    print(xs)
    return (xs, "floatList")


if __name__ == "__main__":
    int_list(True)
