import dataclasses
import random
from typing import TypeVar

import numpy
from numpy import float32, int32

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


def xs_array_get_size_impl(array_id: int32) -> int32:
    if array_id < 0 or array_id >= len(ARRAYS):
        return int32(-1)
    return int32(len(ARRAYS[array_id].array))


def xs_array_create_int_impl(size: int32, default_value: int32, unique_name: str) -> int32:
    return xs_array_create_impl(size, default_value, unique_name, type(int32))


def xs_array_set_int_impl(array_id: int32, idx: int32, value: int32) -> int32:
    return xs_array_set_impl(array_id, idx, value, type(int32))


def xs_array_get_int_impl(array_id: int32, idx: int32) -> int32:
    return xs_array_get_impl(array_id, idx, type(int32))


def xs_array_resize_int_impl(array_id: int32, new_size: int32) -> int32:
    return xs_array_resize_impl(array_id, new_size, type(int32))


def xs_array_create_float_impl(size: int32, default_value: float32, unique_name: str) -> int32:
    return xs_array_create_impl(size, default_value, unique_name, type(float32))


def xs_array_set_float_impl(array_id: int32, idx: int32, value: float32) -> int32:
    return xs_array_set_impl(array_id, idx, value, type(float32))


def xs_array_get_float_impl(array_id: int32, idx: int32) -> float32:
    return xs_array_get_impl(array_id, idx, type(float32))


def xs_array_resize_float_impl(array_id: int32, new_size: int32) -> int32:
    return xs_array_resize_impl(array_id, new_size, type(float32))


def xs_array_create_string_impl(size: int32, default_value: str, unique_name: str) -> int32:
    return xs_array_create_impl(size, default_value, unique_name, type(str))


def xs_array_set_string_impl(array_id: int32, idx: int32, value: str) -> int32:
    return xs_array_set_impl(array_id, idx, value, type(str))


def xs_array_get_string_impl(array_id: int32, idx: int32) -> str:
    return xs_array_get_impl(array_id, idx, type(str))


def xs_array_resize_string_impl(array_id: int32, new_size: int32) -> int32:
    return xs_array_resize_impl(array_id, new_size, type(str))


def xs_array_create_impl(size: int32, default_value: T, unique_name: str, t: type[T]) -> int32:
    if size < 0:
        return int32(-1)
    arr = XsArray(t, [default_value] * size)
    ARRAYS.append(arr)
    if unique_name != "":
        if unique_name in ARRAY_NAMES:
            return int32(-1)
        else:
            ARRAY_NAMES.add(unique_name)
    return int32(len(ARRAYS) - 1)


def xs_array_set_impl(array_id: int32, idx: int32, value: T, t: type[T]) -> int32:
    if array_id < 0 or array_id >= len(ARRAYS):
        return int32(0)
    xs_array = ARRAYS[array_id]
    if xs_array.arr_type != t or idx < 0 or idx >= len(xs_array.array):
        return int32(0)
    xs_array.array[idx] = value
    return int32(1)


def xs_array_get_impl(array_id: int32, idx: int32, t: type[T]) -> T:
    if array_id < 0 or array_id >= len(ARRAYS):
        return int32(-1)
    xs_array = ARRAYS[array_id]
    if xs_array.arr_type != t or idx < 0 or idx >= len(xs_array.array):
        if t == type(int):
            return int32(-1)
        if t == type(float):
            return float32(-1.0)
        if t == type(str):
            return "-1"
        return None

    return xs_array.array[idx]


def xs_array_resize_impl(array_id: int32, new_size: int32, t: type[T]) -> int32:
    if array_id < 0 or array_id >= len(ARRAYS) or new_size < 0:
        return int32(0)
    xs_array = ARRAYS[array_id]
    if xs_array.arr_type != t:
        return int32(0)
    size = len(xs_array.array)
    if new_size == size:
        return int32(1)
    if new_size > size:
        if t == type(int):
            value = [int32(-1337)]
        elif t == type(float):
            value = [float32(-13.37)]
        elif t == type(str):
            value = ["<default string>"]
        else:
            value = [None]
        xs_array.array.extend(value * (new_size - size))
    else:
        xs_array.array = xs_array.array[:new_size - size]
    return int32(1)


def xs_chat_data_impl(msg: str, value: int32) -> None:
    if value != -1:
        msg = msg.replace("%d", str(value), 1)
    print(msg)


def bit_cast_to_float_impl(number: int32) -> float32:
    return float32(number.view(float32))


def bit_cast_to_int_impl(number: float32) -> int32:
    return int32(number.view(int32))


def xs_get_random_number_impl() -> int32:
    return int32(random.randint(0, 32766))