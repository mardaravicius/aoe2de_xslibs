from numpy import int32

from xs_converter.converter import PythonToXsConverter
from xs_converter.functions import xs_array_create_vector, xs_array_set_vector, xs_array_resize_vector, \
    xs_array_get_vector, xs_array_get_size, xs_chat_data, bit_cast_to_float, bit_cast_to_int, vector, xs_vector_get_x, \
    xs_vector_set
from xs_converter.symbols import XsExternConst, i32range, XsVector

c_vector_list_success = int32(0)
c_vector_list_generic_error = int32(-1)
c_vector_list_generic_error_vector = vector(-1.0, -1.0, -1.0)
c_vector_list_index_out_of_range_error = int32(-2)
c_vector_list_resize_failed_error = int32(-3)
c_vector_list_max_capacity_error = int32(-4)
c_vector_list_max_capacity = int32(999999999)
c_vector_list_empty_param = vector(-9999999.0, -9999999.0, -9999999.0)
c_vector_list_empty_int_param = -999999999
_vector_list_last_operation_status = c_vector_list_success


def constants() -> None:
    c_vector_list_success: XsExternConst[int32] = int32(0)
    c_vector_list_generic_error: XsExternConst[int32] = int32(-1)
    c_vector_list_generic_error_vector: XsExternConst[XsVector] = vector(-1.0, -1.0, -1.0)
    c_vector_list_index_out_of_range_error: XsExternConst[int32] = int32(-2)
    c_vector_list_resize_failed_error: XsExternConst[int32] = int32(-3)
    c_vector_list_max_capacity_error: XsExternConst[int32] = int32(-4)
    c_vector_list_max_capacity: XsExternConst[int32] = int32(999999999)
    c_vector_list_empty_param: XsExternConst[XsVector] = vector(-9999999.0, -9999999.0, -9999999.0)
    c_vector_list_empty_int_param: XsExternConst[int32] = -999999999
    _vector_list_last_operation_status: int32 = c_vector_list_success


def xs_vector_list_size(lst: int32 = int32(-1)) -> int32:
    return bit_cast_to_int(xs_vector_get_x(xs_array_get_vector(lst, 0)))


def _xs_vector_list_set_size(lst: int32 = int32(-1), size: int32 = int32(0)) -> None:
    xs_array_set_vector(lst, 0, xs_vector_set(bit_cast_to_float(size), 0.0, 0.0))


def xs_vector_list_create(capacity: int32 = int32(7)) -> int32:
    """
    Creates empty list for float values. List is a dynamic array that grows and shrinks as values are added and removed.
    :param capacity: initial list capacity
    :return: created list id, or error if negative
    """
    if capacity < 0 or capacity >= c_vector_list_max_capacity:
        return c_vector_list_generic_error
    lst: int32 = xs_array_create_vector(capacity + 1)
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
    Creates a list with provided values. The first value that equals `cFloatListEmptyParam` will stop further insertion.
    This Function can create a list with 12 values at the maximum, but further values can be added with other functions.
    :param v1 through v11: value at a given index of a list
    :return: created list id, or error if negative
    """
    lst: int32 = xs_array_create_vector(13)
    if lst < 0:
        return c_vector_list_generic_error
    if v0 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(0))
        return lst
    xs_array_set_vector(lst, 1, v0)
    if v1 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(1))
        return lst
    xs_array_set_vector(lst, 2, v1)
    if v2 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(2))
        return lst
    xs_array_set_vector(lst, 3, v2)
    if v3 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(3))
        return lst
    xs_array_set_vector(lst, 4, v3)
    if v4 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(4))
        return lst
    xs_array_set_vector(lst, 5, v4)
    if v5 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(5))
        return lst
    xs_array_set_vector(lst, 6, v5)
    if v6 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(6))
        return lst
    xs_array_set_vector(lst, 7, v6)
    if v7 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(7))
        return lst
    xs_array_set_vector(lst, 8, v7)
    if v8 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(8))
        return lst
    xs_array_set_vector(lst, 9, v8)
    if v9 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(9))
        return lst
    xs_array_set_vector(lst, 10, v9)
    if v10 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(10))
        return lst
    xs_array_set_vector(lst, 11, v10)
    if v11 == c_vector_list_empty_param:
        _xs_vector_list_set_size(lst, int32(11))
        return lst
    xs_array_set_vector(lst, 12, v11)
    _xs_vector_list_set_size(lst, int32(12))
    return lst


def xs_vector_list_from_repeated_val(value: XsVector = vector(0.0, 0.0, 0.0), times: int32 = int32(0)) -> int32:
    if times < 0 or times >= c_vector_list_max_capacity:
        return c_vector_list_generic_error
    lst: int32 = xs_array_create_vector(times + 1, value)
    if lst < 0:
        return c_vector_list_generic_error
    _xs_vector_list_set_size(lst, times)
    return lst


def xs_vector_list_from_repeated_list(lst: int32 = int32(-1), times: int32 = int32(0)) -> int32:
    size: int32 = xs_vector_list_size(lst)
    new_capacity: int32 = (size * times) + 1
    if new_capacity > c_vector_list_max_capacity:
        return c_vector_list_generic_error
    new_lst: int32 = xs_array_create_vector(new_capacity)
    if new_lst < 0:
        return c_vector_list_generic_error
    for i in i32range(1, size + 1):
        val: XsVector = xs_array_get_vector(lst, i)
        j: int32 = i
        while j < new_capacity:
            xs_array_set_vector(new_lst, j, val)
            j += size
    _xs_vector_list_set_size(new_lst, new_capacity - 1)
    return new_lst


def xs_vector_list_from_array(arr: int32 = int32(-1)) -> int32:
    arr_size: int32 = xs_array_get_size(arr)
    lst: int32 = xs_vector_list_create(arr_size)
    if lst < 0:
        return lst
    for i in i32range(0, arr_size):
        xs_array_set_vector(lst, i + 1, xs_array_get_vector(arr, i))
    _xs_vector_list_set_size(lst, arr_size)
    return lst


def xs_vector_list_use_array_as_source(arr: int32 = int32(-1)) -> int32:
    arr_size: int32 = xs_array_get_size(arr)
    if arr_size + 1 > c_vector_list_max_capacity:
        return c_vector_list_max_capacity_error
    r: int32 = xs_array_resize_vector(arr, arr_size + 1)
    if r < 0:
        return c_vector_list_resize_failed_error
    for i in i32range(arr_size - 1, -1, -1):
        xs_array_set_vector(arr, i + 1, xs_array_get_vector(arr, i))
    _xs_vector_list_set_size(arr, arr_size)
    return arr


def xs_vector_list_get(lst: int32 = int32(-1), idx: int32 = int32(-1)) -> XsVector:
    global _vector_list_last_operation_status
    size: int32 = xs_vector_list_size(lst)
    if idx < 0 or idx >= size:
        _vector_list_last_operation_status = c_vector_list_index_out_of_range_error
        return c_vector_list_generic_error_vector
    _vector_list_last_operation_status = c_vector_list_success
    return xs_array_get_vector(lst, idx + 1)


def xs_vector_list_set(lst: int32 = int32(-1), idx: int32 = int32(-1),
                       value: XsVector = vector(0.0, 0.0, 0.0)) -> int32:
    size: int32 = xs_vector_list_size(lst)
    if idx < 0 or idx >= size:
        return c_vector_list_index_out_of_range_error
    xs_array_set_vector(lst, idx + 1, value)
    return c_vector_list_success


def _xs_vector_list_extend_int_array(lst: int32 = int32(-1), capacity: int32 = int32(0)) -> int32:
    if capacity == c_vector_list_max_capacity:
        return c_vector_list_max_capacity_error
    new_capacity: int32 = capacity * 2
    if new_capacity > c_vector_list_max_capacity:
        new_capacity = c_vector_list_max_capacity
    r: int32 = xs_array_resize_vector(lst, new_capacity)
    if r != 1:
        return c_vector_list_resize_failed_error
    return c_vector_list_success


def _xs_vector_list_shrink_int_array(lst: int32 = int32(-1), size: int32 = int32(0),
                                     capacity: int32 = int32(0)) -> int32:
    if size <= (capacity // 2):
        r: int32 = xs_array_resize_vector(lst, size)
        if r != 1:
            return c_vector_list_resize_failed_error
    return c_vector_list_success


def xs_vector_list_append(lst: int32 = int32(-1), value: XsVector = vector(0.0, 0.0, 0.0)) -> int32:
    capacity: int32 = xs_array_get_size(lst)
    size: int32 = xs_vector_list_size(lst)
    next_idx: int32 = size + 1
    if capacity == next_idx:
        r: int32 = _xs_vector_list_extend_int_array(lst, capacity)
        if r != c_vector_list_success:
            return r
    xs_array_set_vector(lst, next_idx, value)
    _xs_vector_list_set_size(lst, next_idx)
    return c_vector_list_success


def xs_vector_list_insert(lst: int32 = int32(-1), idx: int32 = int32(-1),
                          value: XsVector = vector(0.0, 0.0, 0.0)) -> int32:
    capacity: int32 = xs_array_get_size(lst)
    size: int32 = xs_vector_list_size(lst)
    if idx < 0 or idx > size:
        return c_vector_list_index_out_of_range_error
    new_size: int32 = size + 1
    if capacity == new_size:
        r: int32 = _xs_vector_list_extend_int_array(lst, capacity)
        if r != c_vector_list_success:
            return r
    for i in i32range(size, idx, -1):
        xs_array_set_vector(lst, i + 1, xs_array_get_vector(lst, i))
    xs_array_set_vector(lst, idx + 1, value)
    _xs_vector_list_set_size(lst, new_size)

    return c_vector_list_success


def xs_vector_list_pop(lst: int32 = int32(-1), idx: int32 = c_vector_list_max_capacity) -> XsVector:
    global _vector_list_last_operation_status
    capacity: int32 = xs_array_get_size(lst)
    size: int32 = xs_vector_list_size(lst)
    if idx == c_vector_list_max_capacity:
        idx = size - 1
    elif idx < 0 or idx >= size:
        _vector_list_last_operation_status = c_vector_list_index_out_of_range_error
        return c_vector_list_generic_error_vector
    removed_elem: XsVector = xs_array_get_vector(lst, idx + 1)
    for i in i32range(idx + 2, size + 1):
        xs_array_set_vector(lst, i - 1, xs_array_get_vector(lst, i))
    r: int32 = _xs_vector_list_shrink_int_array(lst, size, capacity)
    if r != c_vector_list_success:
        _vector_list_last_operation_status = r
        return c_vector_list_generic_error_vector
    _xs_vector_list_set_size(lst, size - 1)
    _vector_list_last_operation_status = c_vector_list_success
    return removed_elem


def xs_vector_list_remove(lst: int32 = int32(-1), value: XsVector = vector(-1.0, -1.0, -1.0)) -> int32:
    capacity: int32 = xs_array_get_size(lst)
    size: int32 = xs_vector_list_size(lst)
    found_idx: int32 = int32(-1)
    i: int32 = int32(1)
    while i <= size and found_idx == -1:
        c_val: XsVector = xs_array_get_vector(lst, i)
        if c_val == value:
            found_idx = i
        i += 1
    if found_idx == -1:
        return c_vector_list_generic_error
    for j in i32range(found_idx + 1, size + 1):
        xs_array_set_vector(lst, j - 1, xs_array_get_vector(lst, j))
    r: int32 = _xs_vector_list_shrink_int_array(lst, size, capacity)
    if r != c_vector_list_success:
        return r
    _xs_vector_list_set_size(lst, size - 1)
    return found_idx - 1


def xs_vector_list_index(lst: int32 = int32(-1), value: XsVector = vector(-1.0, -1.0, -1.0), start: int32 = int32(0),
                         stop: int32 = c_vector_list_empty_int_param) -> int32:
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
        if xs_array_get_vector(lst, i + 1) == value:
            return i
    return c_vector_list_generic_error


def xs_vector_list_contains(lst: int32 = int32(-1), value: XsVector = vector(-1.0, -1.0, -1.0)) -> bool:
    return xs_vector_list_index(lst, value) > -1


def xs_vector_list_to_string(lst: int32 = int32(-1)) -> str:
    size: int32 = xs_vector_list_size(lst)
    s: str = "["
    for i in i32range(1, size + 1):
        s += str(xs_array_get_vector(lst, i))
        if i < size:
            s += ", "
    s += "]"
    return s


def xs_vector_list_copy(lst: int32 = int32(-1), start: int32 = int32(0),
                        end: int32 = c_vector_list_max_capacity) -> int32:
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
    new_lst: int32 = xs_array_create_vector(new_size + 1)
    if new_lst < 0:
        return c_vector_list_generic_error
    for i in i32range(fr, to + 1):
        xs_array_set_vector(new_lst, i - fr, xs_array_get_vector(lst, i))
    _xs_vector_list_set_size(new_lst, new_size)
    return new_lst


def xs_vector_list_extend(source: int32 = int32(-1), lst: int32 = int32(-1)) -> int32:
    source_size: int32 = xs_vector_list_size(source)
    to_add: int32 = xs_vector_list_size(lst)
    capacity: int32 = xs_array_get_size(source)
    new_size: int32 = source_size + to_add
    if new_size > capacity:
        if new_size >= c_vector_list_max_capacity:
            return c_vector_list_max_capacity_error
        r: int32 = xs_array_resize_vector(source, new_size + 1)
        if r != 1:
            return c_vector_list_resize_failed_error
    for i in i32range(1, to_add + 1):
        xs_array_set_vector(source, i + source_size, xs_array_get_vector(lst, i))
    _xs_vector_list_set_size(source, new_size)
    return c_vector_list_success


def xs_vector_list_extend_with_array(source: int32 = int32(-1), arr: int32 = int32(-1)) -> int32:
    source_size: int32 = xs_vector_list_size(source)
    to_add: int32 = xs_array_get_size(arr)
    capacity: int32 = xs_array_get_size(source)
    new_size: int32 = source_size + to_add
    if new_size > capacity:
        if new_size >= c_vector_list_max_capacity or new_size < 0:
            return c_vector_list_max_capacity_error
        r: int32 = xs_array_resize_vector(source, new_size + 1)
        if r != 1:
            return c_vector_list_resize_failed_error
    for i in i32range(0, to_add):
        xs_array_set_vector(source, i + source_size + 1, xs_array_get_vector(arr, i))
    _xs_vector_list_set_size(source, new_size)
    return c_vector_list_success


def xs_vector_list_clear(lst: int32 = int32(-1)) -> int32:
    capacity: int32 = xs_vector_list_size(lst)
    if capacity > 8:
        r: int32 = xs_array_resize_vector(lst, 8)
        if r != 1:
            return c_vector_list_resize_failed_error
    _xs_vector_list_set_size(lst, int32(0))
    return c_vector_list_success


def xs_vector_list_reverse(lst: int32 = int32(-1)) -> None:
    size: int32 = xs_vector_list_size(lst)
    mid: int32 = (size + 2) // 2
    for i in i32range(1, mid):
        temp: XsVector = xs_array_get_vector(lst, i)
        back_i: int32 = size - i + 1
        xs_array_set_vector(lst, i, xs_array_get_vector(lst, back_i))
        xs_array_set_vector(lst, back_i, temp)


def xs_vector_list_count(lst: int32 = int32(-1), value: XsVector = vector(-1.0, -1.0, -1.0)) -> int32:
    count: int32 = int32(0)
    size: int32 = xs_vector_list_size(lst)
    for i in i32range(1, size + 1):
        if xs_array_get_vector(lst, i) == value:
            count += 1
    return count


def xs_vector_list_last_error() -> int32:
    return _vector_list_last_operation_status


def test() -> None:
    lst: int32 = xs_vector_list_create(int32(20))
    xs_chat_data("arr: " + str(lst))
    xs_vector_list_append(lst, vector(1.1, 2.2, 3.3))
    xs_vector_list_append(lst, vector(11.11, 22.22, 33.33))
    xs_vector_list_append(lst, vector(111.111, 222.222, 333.333))
    xs_chat_data(xs_vector_list_to_string(lst))
    xs_chat_data("pop 1: " + str(xs_vector_list_pop(lst)))
    xs_chat_data("pop 2: " + str(xs_vector_list_pop(lst)))
    xs_chat_data(xs_vector_list_to_string(lst))
    xs_chat_data("pop 3: " + str(xs_vector_list_pop(lst)))
    xs_chat_data("pop 4: " + str(xs_vector_list_pop(lst)))
    xs_vector_list_insert(lst, int32(0), vector(1.0, 1.1, 1.2))
    xs_vector_list_insert(lst, int32(0), vector(2.0, 2.1, 2.2))
    xs_vector_list_insert(lst, int32(0), vector(3.0, 3.1, 3.2))
    xs_vector_list_insert(lst, int32(1), vector(4.0, 4.1, 4.2))
    xs_vector_list_insert(lst, int32(1), vector(5.0, 5.1, 5.2))
    xs_vector_list_insert(lst, int32(5), vector(6.0, 6.1, 6.2))
    xs_vector_list_insert(lst, int32(7), vector(7.0, 7.1, 7.2))
    xs_chat_data(xs_vector_list_to_string(lst))


def vector_list(include_test: bool) -> tuple[str, str]:
    constants_function_xs = PythonToXsConverter.to_xs_script(
        constants,
        indent=True,
    )
    constants_xs = (constants_function_xs[constants_function_xs.find("extern"):constants_function_xs.rfind("}")]
                    .strip()
                    .replace("    ", "")
                    ) + "\n\n"
    xs = constants_xs + PythonToXsConverter.to_xs_script(
        xs_vector_list_size,
        _xs_vector_list_set_size,
        xs_vector_list,
        xs_vector_list_create,
        xs_vector_list_from_repeated_val,
        xs_vector_list_from_repeated_list,
        xs_vector_list_from_array,
        xs_vector_list_use_array_as_source,
        xs_vector_list_get,
        xs_vector_list_set,
        _xs_vector_list_extend_int_array,
        _xs_vector_list_shrink_int_array,
        xs_vector_list_to_string,
        xs_vector_list_append,
        xs_vector_list_pop,
        xs_vector_list_insert,
        xs_vector_list_remove,
        xs_vector_list_index,
        xs_vector_list_contains,
        xs_vector_list_clear,
        xs_vector_list_copy,
        xs_vector_list_extend,
        xs_vector_list_extend_with_array,
        xs_vector_list_count,
        xs_vector_list_last_error,
        indent=True,
    )
    if include_test:
        xs += constants_xs + PythonToXsConverter.to_xs_script(
            test,
            indent=True,
        )
    print(xs)
    return xs, "vectorList"


if __name__ == "__main__":
    vector_list(True)
