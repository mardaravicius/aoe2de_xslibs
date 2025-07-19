from xs_converter.converter import PythonToXsConverter
from xs_converter.functions import xs_array_create_int, xs_array_set_int, xs_array_resize_int, xs_array_get_int, \
    xs_array_get_size, xs_chat_data
from xs_converter.symbols import XsExternConst, XsExtern

c_int_list_success = 0
c_int_list_generic_error = -1
c_int_list_index_out_of_range_error = -2
c_int_list_resize_failed_error = -3
c_int_list_max_capacity_error = -4
c_int_list_max_capacity = 999999999
c_int_list_empty_param = -999999999
_int_list_last_operation_status = c_int_list_success


def constants() -> None:
    c_int_list_success: XsExternConst[int] = 0
    c_int_list_generic_error: XsExternConst[int] = -1
    c_int_list_index_out_of_range_error: XsExternConst[int] = -2
    c_int_list_resize_failed_error: XsExternConst[int] = -3
    c_int_list_max_capacity_error: XsExternConst[int] = -4
    c_int_list_max_capacity: XsExternConst[int] = 999999999
    c_int_list_empty_param: XsExternConst[int] = -999999999
    _int_list_last_operation_status: XsExtern[int] = c_int_list_success


def xs_int_list_create(capacity: int = 7) -> int:
    """
    Creates empty list for int values. List is a dynamic array that grows and shrinks as values are added and removed.
    :param capacity: initial list capacity
    :return: created list id, or error if negative
    """
    if capacity < 0 or capacity >= c_int_list_max_capacity:
        return c_int_list_generic_error
    lst: int = xs_array_create_int(capacity + 1)
    if lst < 0:
        return c_int_list_generic_error
    xs_array_set_int(lst, 0, 0)
    return lst


def xs_int_list(
        v0: int = c_int_list_empty_param,
        v1: int = c_int_list_empty_param,
        v2: int = c_int_list_empty_param,
        v3: int = c_int_list_empty_param,
        v4: int = c_int_list_empty_param,
        v5: int = c_int_list_empty_param,
        v6: int = c_int_list_empty_param,
        v7: int = c_int_list_empty_param,
        v8: int = c_int_list_empty_param,
        v9: int = c_int_list_empty_param,
        v10: int = c_int_list_empty_param,
        v11: int = c_int_list_empty_param,
) -> int:
    """
    Creates a list with provided values. The first value that equals `cIntListEmptyParam` will stop further insertion.
    This Function can create a list with 12 values at the maximum, but further values can be added with other functions.
    :param v1 through v11: value at a given index of a list
    :return: created list id, or error if negative
    """
    lst: int = xs_array_create_int(13)
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


def xs_int_list_from_range(start: int = 0, stop: int = 0, step: int = 1) -> int:
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
    distance: int = int(abs(stop - start))
    stepa: int = int(abs(step))
    size: int = distance // stepa
    if size >= c_int_list_max_capacity:
        return c_int_list_generic_error
    remain: int = distance % stepa
    if remain > 0:
        size += 1
    lst: int = xs_array_create_int(size + 1)
    if lst < 0:
        return c_int_list_generic_error
    i: int = 1
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


def xs_int_list_repeat(value: int = 0, times: int = 0) -> int:
    if times < 0 or times >= c_int_list_max_capacity:
        return c_int_list_generic_error
    lst: int = xs_array_create_int(times + 1, value)
    if lst < 0:
        return c_int_list_generic_error
    xs_array_set_int(lst, 0, times)
    return lst


def xs_int_list_from_array(arr: int = -1) -> int:
    arr_size: int = xs_array_get_size(arr)
    lst = xs_int_list_create(arr_size)
    if lst < 0:
        return lst
    for i in range(0, arr_size):
        xs_array_set_int(lst, i + 1, xs_array_get_int(arr, i))
    xs_array_set_int(lst, 0, arr_size)
    return lst


def xs_int_list_get(lst: int = -1, idx: int = -1) -> int:
    global _int_list_last_operation_status
    size: int = xs_array_get_int(lst, 0)
    if idx < 0 or idx >= size:
        _int_list_last_operation_status = c_int_list_index_out_of_range_error
        return c_int_list_generic_error
    _int_list_last_operation_status = c_int_list_success
    return xs_array_get_int(lst, idx + 1)


def xs_int_list_set(lst: int = -1, idx: int = -1, value: int = 0) -> int:
    size: int = xs_array_get_int(lst, 0)
    if idx < 0 or idx >= size:
        return c_int_list_index_out_of_range_error
    xs_array_set_int(lst, idx + 1, value)
    return c_int_list_success


def xs_int_list_size(lst: int = -1) -> int:
    return xs_array_get_int(lst, 0)


def _xs_int_list_extend_int_array(lst: int = -1, capacity: int = 0) -> int:
    if capacity == c_int_list_max_capacity:
        return c_int_list_max_capacity_error
    new_capacity: int = capacity * 2
    if new_capacity > c_int_list_max_capacity:
        new_capacity = c_int_list_max_capacity
    r: int = xs_array_resize_int(lst, new_capacity)
    if r != 1:
        return c_int_list_resize_failed_error
    return c_int_list_success


def _xs_int_list_shrink_int_array(lst: int = -1, size: int = 0, capacity: int = 0) -> int:
    if size <= (capacity // 2):
        r: int = xs_array_resize_int(lst, size)
        if r != 1:
            return c_int_list_resize_failed_error
    return c_int_list_success


def xs_int_list_append(lst: int = -1, value: int = 0) -> int:
    capacity: int = xs_array_get_size(lst)
    size: int = xs_array_get_int(lst, 0)
    next_idx: int = size + 1
    if capacity == next_idx:
        r: int = _xs_int_list_extend_int_array(lst, capacity)
        if r != c_int_list_success:
            return r
    xs_array_set_int(lst, next_idx, value)
    xs_array_set_int(lst, 0, next_idx)
    return c_int_list_success


# def xs_int_list_pop(lst: int = -1) -> int:
#     global _int_array_list_last_operation_status
#     capacity: int = xs_array_get_size(lst)
#     size: int = xs_array_get_int(lst, 0)
#     if size == 0:
#         _int_array_list_last_operation_status = c_int_list_index_out_of_range_error
#         return c_int_list_generic_error
#     removed_elem: int = xs_array_get_int(lst, size)
#     r: int = _shrink_int_array(lst, size, capacity)
#     if r != c_int_list_success:
#         _int_array_list_last_operation_status = r
#         return c_int_list_generic_error
#     xs_array_set_int(lst, 0, size - 1)
#     _int_array_list_last_operation_status = c_int_list_success
#     return removed_elem


def xs_int_list_insert(lst: int = -1, idx: int = -1, value: int = 0) -> int:
    capacity: int = xs_array_get_size(lst)
    size: int = xs_array_get_int(lst, 0)
    if idx < 0 or idx > size:
        return c_int_list_index_out_of_range_error
    new_size: int = size + 1
    if capacity == new_size:
        r: int = _xs_int_list_extend_int_array(lst, capacity)
        if r != c_int_list_success:
            return r
    for i in range(size, idx + 2, -1):
        xs_array_set_int(lst, i + 1, xs_array_get_int(lst, i))
    xs_array_set_int(lst, idx + 1, value)
    xs_array_set_int(lst, 0, new_size)

    return c_int_list_success


def xs_int_list_pop(lst: int = -1, idx: int = c_int_list_max_capacity) -> int:
    global _int_list_last_operation_status
    capacity: int = xs_array_get_size(lst)
    size: int = xs_array_get_int(lst, 0)
    if idx == c_int_list_max_capacity:
        idx = size - 1
    elif idx < 0 or idx >= size:
        _int_list_last_operation_status = c_int_list_index_out_of_range_error
        return c_int_list_generic_error
    removed_elem: int = xs_array_get_int(lst, idx + 1)
    for i in range(idx + 2, size + 1):
        xs_array_set_int(lst, i - 1, xs_array_get_int(lst, i))
    r: int = _xs_int_list_shrink_int_array(lst, size, capacity)
    if r != c_int_list_success:
        _int_list_last_operation_status = r
        return c_int_list_generic_error
    xs_array_set_int(lst, 0, size - 1)
    _int_list_last_operation_status = c_int_list_success
    return removed_elem


def xs_int_list_remove(lst: int = -1, value: int = -1) -> int:
    capacity: int = xs_array_get_size(lst)
    size: int = xs_array_get_int(lst, 0)
    found_idx: int = -1
    i: int = 1
    while i <= size and found_idx == -1:
        c_val: int = xs_array_get_int(lst, i)
        if c_val == value:
            found_idx = i
        i += 1
    if found_idx == -1:
        return c_int_list_generic_error
    for j in range(found_idx + 1, size + 1):
        xs_array_set_int(lst, j - 1, xs_array_get_int(lst, j))
    r: int = _xs_int_list_shrink_int_array(lst, size, capacity)
    if r != c_int_list_success:
        return r
    xs_array_set_int(lst, 0, size - 1)
    return found_idx - 1


def xs_int_list_index(lst: int = -1, value: int = -1) -> int:
    size: int = xs_array_get_int(lst, 0)
    found_idx: int = -1
    i: int = 1
    while i <= size and found_idx == -1:
        c_val: int = xs_array_get_int(lst, i)
        if c_val == value:
            found_idx = i
        i += 1
    if found_idx == -1:
        return c_int_list_generic_error
    return found_idx - 1


def _xs_int_list_compare_elem(a: int = -1, b: int = -1, reverse: bool = False) -> bool:
    if reverse:
        return a > b
    return a < b


def _xs_int_list_sift_down(lst: int = -1, start: int = -1, end: int = -1, reverse: bool = False) -> None:
    root: int = start
    while True:
        child: int = 2 * root
        if child > end:
            return
        child_val: int = xs_array_get_int(lst, child)
        child_val1: int = xs_array_get_int(lst, child + 1)
        if child + 1 <= end and _xs_int_list_compare_elem(child_val, child_val1, reverse):
            child += 1
            child_val = child_val1
        root_val: int = xs_array_get_int(lst, root)
        if _xs_int_list_compare_elem(root_val, child_val, reverse):
            xs_array_set_int(lst, root, child_val)
            xs_array_set_int(lst, child, root_val)
            root = child
        else:
            return


def xs_int_list_sort(lst: int = -1, reverse: bool = False) -> None:
    global _int_list_last_operation_status
    size: int = xs_array_get_int(lst, 0)
    for start in range(size // 2, 0, -1):
        _xs_int_list_sift_down(lst, start, size, reverse)

    for end in range(size, 1, -1):
        temp: int = xs_array_get_int(lst, 1)
        xs_array_set_int(lst, 1, xs_array_get_int(lst, end))
        xs_array_set_int(lst, end, temp)
        _xs_int_list_sift_down(lst, 1, end - 1, reverse)


def xs_int_list_to_string(lst: int = -1) -> str:
    size: int = xs_array_get_int(lst, 0)
    s: str = "["
    for i in range(1, size + 1):
        s += str(xs_array_get_int(lst, i))
        if i < size:
            s += ", "
    s += "]"
    return s


def xs_int_list_copy(lst: int = -1, start: int = 0, end: int = c_int_list_max_capacity) -> int:
    size: int = xs_array_get_int(lst, 0)
    fr: int = 0
    if start < 0:
        fr = size + start
    else:
        fr = start
    to: int = 0
    if end < 0:
        to = size + end
    else:
        to = end
    if fr < 0:
        fr = 0
    if to > size:
        to = size
    new_size: int = to - fr
    if new_size < 0:
        new_size = 0
    new_lst: int = xs_array_create_int(new_size + 1)
    if new_lst < 0:
        return c_int_list_generic_error
    for i in range(fr, to + 1):
        xs_array_set_int(new_lst, i - fr, xs_array_get_int(lst, i))
    xs_array_set_int(new_lst, 0, new_size)
    return new_lst


def xs_int_list_extend(source: int = -1, lst: int = -1) -> int:
    source_size: int = xs_array_get_int(source, 0)
    to_add: int = xs_array_get_int(lst, 0)
    capacity: int = xs_array_get_size(source)
    new_size: int = source_size + to_add
    if new_size > capacity:
        if new_size >= c_int_list_max_capacity:
            return c_int_list_max_capacity_error
        r: int = xs_array_resize_int(source, new_size + 1)
        if r != 1:
            return c_int_list_resize_failed_error
    for i in range(1, to_add + 1):
        xs_array_set_int(source, i + source_size, xs_array_get_int(lst, i))
    xs_array_set_int(source, 0, new_size)
    return c_int_list_success


def xs_int_list_extend_with_array(source: int = -1, arr: int = -1) -> int:
    source_size: int = xs_array_get_int(source, 0)
    to_add: int = xs_array_get_size(arr)
    capacity: int = xs_array_get_size(source)
    new_size: int = source_size + to_add
    if new_size > capacity:
        if new_size >= c_int_list_max_capacity or new_size < 0:
            return c_int_list_max_capacity_error
        r: int = xs_array_resize_int(source, new_size + 1)
        if r != 1:
            return c_int_list_resize_failed_error
    for i in range(0, to_add):
        xs_array_set_int(source, i + source_size + 1, xs_array_get_int(arr, i))
    xs_array_set_int(source, 0, new_size)
    return c_int_list_success


def xs_int_list_clear(lst: int = -1) -> int:
    capacity: int = xs_array_get_int(lst, 0)
    if capacity > 8:
        r: int = xs_array_resize_int(lst, 8)
        if r != 1:
            return c_int_list_resize_failed_error
    xs_array_set_int(lst, 0, 0)
    return c_int_list_success


def xs_int_list_compare(lst1: int = -1, lst2: int = -1) -> int:
    size1: int = xs_array_get_int(lst1, 0)
    size2: int = xs_array_get_int(lst2, 0)
    i: int = 1
    while i <= size1 and i <= size2:
        v1: int = xs_array_get_int(lst1, i)
        v2: int = xs_array_get_int(lst2, i)
        if v1 < v2:
            return -1
        if v1 > v2:
            return 1
        i += 1
    if size1 < size2:
        return -1
    if size1 > size2:
        return 1
    return 0


def xs_int_list_reverse(lst: int = -1) -> None:
    size: int = xs_array_get_int(lst, 0)
    mid: int = (size + 2) // 2
    for i in range(1, mid):
        temp: int = xs_array_get_int(lst, i)
        back_i: int = size - i + 1
        xs_array_set_int(lst, i, xs_array_get_int(lst, back_i))
        xs_array_set_int(lst, back_i, temp)


def xs_int_list_last_error() -> int:
    return _int_list_last_operation_status


def test() -> None:
    arr: int = xs_array_create_int(20)
    xs_chat_data("arr: " + str(arr))
    xs_int_list_append(arr, 1)
    xs_int_list_append(arr, 2)
    xs_int_list_append(arr, 3)
    xs_chat_data(xs_int_list_to_string(arr))
    xs_chat_data("pop 1: " + str(xs_int_list_pop(arr)))
    xs_chat_data("pop 2: " + str(xs_int_list_pop(arr)))
    xs_chat_data(xs_int_list_to_string(arr))
    xs_chat_data("pop 3: " + str(xs_int_list_pop(arr)))
    xs_chat_data("pop 4: " + str(xs_int_list_pop(arr)))
    xs_int_list_insert(arr, 0, 1)
    xs_int_list_insert(arr, 0, 2)
    xs_int_list_insert(arr, 0, 3)
    xs_int_list_insert(arr, 1, 4)
    xs_int_list_insert(arr, 1, 5)
    xs_int_list_insert(arr, 5, 6)
    xs_int_list_insert(arr, 7, 7)
    xs_chat_data(xs_int_list_to_string(arr))
    xs_int_list_sort(arr, True)
    xs_chat_data(xs_int_list_to_string(arr))


def int_list(include_test: bool) -> (str, str):
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
        xs_int_list_repeat,
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
        _xs_int_list_compare_elem,
        _xs_int_list_sift_down,
        xs_int_list_sort,
        xs_int_list_clear,
        xs_int_list_copy,
        xs_int_list_extend,
        xs_int_list_extend_with_array,
        xs_int_list_compare,
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
