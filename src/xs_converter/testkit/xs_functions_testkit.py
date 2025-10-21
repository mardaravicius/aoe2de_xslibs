import dataclasses
from typing import TypeVar

import numpy
from numpy import float32

T = TypeVar('T')

ARRAYS = []
ARRAY_NAMES = set()


@dataclasses.dataclass
class XsArray:
    arr_type: type
    array: list


def abs_impl(x: float32) -> float32:
    return numpy.abs(x)


def pow_impl(x: float32, y: float32) -> float32:
    return numpy.pow(x, y)


def xs_array_get_size_impl(array_id: int) -> int:
    if array_id < 0 or array_id >= len(ARRAYS):
        return -1
    return len(ARRAYS[array_id].array)


def xs_array_create_int_impl(size: int, default_value: int, unique_name: str) -> int:
    return xs_array_create_impl(size, default_value, unique_name, type(int))


def xs_array_set_int_impl(array_id: int, idx: int, value: int) -> int:
    return xs_array_set_impl(array_id, idx, value, type(int))


def xs_array_get_int_impl(array_id: int, idx: int) -> int:
    return xs_array_get_impl(array_id, idx, type(int))


def xs_array_resize_int_impl(array_id: int, new_size: int) -> int:
    return xs_array_resize_impl(array_id, new_size, type(int))


def xs_array_create_float_impl(size: int, default_value: float, unique_name: str) -> int:
    return xs_array_create_impl(size, default_value, unique_name, type(float))


def xs_array_set_float_impl(array_id: int, idx: int, value: float) -> int:
    return xs_array_set_impl(array_id, idx, value, type(float))


def xs_array_get_float_impl(array_id: int, idx: int) -> float:
    return xs_array_get_impl(array_id, idx, type(float))


def xs_array_resize_float_impl(array_id: int, new_size: int) -> int:
    return xs_array_resize_impl(array_id, new_size, type(float))


def xs_array_create_impl(size: int, default_value: T, unique_name: str, t: type[T]) -> int:
    if size < 0:
        return -1
    arr = XsArray(t, [default_value] * size)
    ARRAYS.append(arr)
    if unique_name != "":
        if unique_name in ARRAY_NAMES:
            return -1
        else:
            ARRAY_NAMES.add(unique_name)
    return len(ARRAYS) - 1


def xs_array_set_impl(array_id: int, idx: int, value: T, t: type[T]) -> int:
    if array_id < 0 or array_id >= len(ARRAYS):
        return 0
    xs_array = ARRAYS[array_id]
    if xs_array.arr_type != t or idx < 0 or idx >= len(xs_array.array):
        return 0
    xs_array.array[idx] = value
    return 1


def xs_array_get_impl(array_id: int, idx: int, t: type[T]) -> T:
    if array_id < 0 or array_id >= len(ARRAYS):
        return -1
    xs_array = ARRAYS[array_id]
    if xs_array.arr_type != t or idx < 0 or idx >= len(xs_array.array):
        return -1
    return xs_array.array[idx]


def xs_array_resize_impl(array_id: int, new_size: int, t: type[T]) -> int:
    if array_id < 0 or array_id >= len(ARRAYS) or new_size < 0:
        return 0
    xs_array = ARRAYS[array_id]
    if xs_array.arr_type != t:
        return 0
    size = len(xs_array.array)
    if new_size == size:
        return 1
    if new_size > size:
        xs_array.array.extend([-1337] * (new_size - size))
    else:
        xs_array.array = xs_array.array[:new_size - size]
    return 1


def xs_chat_data_impl(msg: str, value: int) -> None:
    if value != -1:
        msg = msg.replace("%d", str(value), 1)
    print(msg)


def bit_cast_to_float_impl(number: int) -> float:
    i = numpy.int32(number)
    return float(i.view(numpy.float32))


def bit_cast_to_int_impl(number: float) -> int:
    f = numpy.float32(number)
    return int(f.view(numpy.int32))
