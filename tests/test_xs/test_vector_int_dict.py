import importlib.util
import sys
import types
import unittest
from pathlib import Path

import numpy as np
from numpy import int32

import xs.vector_int_dict as _vid
from xs_converter.functions import vector, xs_array_create_int, xs_array_get_int, xs_array_get_size, \
    xs_array_get_vector, xs_array_set_int
from xs_converter.symbols import i32range

np.seterr(over="ignore")


def _encode_key(value: int | int32):
    if int32(value) == int32(-999999999):
        return _vid.c_vector_int_dict_empty_key
    unsigned: int = int(int32(value)) & 0xFFFFFFFF
    return vector(float(unsigned & 0xFFFF), float((unsigned >> 16) & 0xFFFF), 0.0)


def _decode_key(value) -> int32:
    low: int = int(value.x)
    high: int = int(value.y)
    unsigned: int = (high << 16) | low
    if unsigned >= 0x80000000:
        unsigned -= 0x100000000
    return int32(unsigned)


def _build_compat_module() -> types.ModuleType:
    compat = types.ModuleType("xs.int_int_dict3")

    def _sync_constants() -> None:
        logical_slots: int32 = (compat.c_int_int_dict_max_capacity - 1) // 2
        _vid.c_vector_int_dict_max_capacity = (logical_slots * 4) + 1

    def xs_int_int_dict_create() -> int32:
        _sync_constants()
        return _vid.xs_vector_int_dict_create()

    def xs_int_int_dict_put(dct: int32 = int32(-1), key: int32 = int32(-1), val: int32 = int32(0)) -> int32:
        _sync_constants()
        return _vid.xs_vector_int_dict_put(dct, _encode_key(key), val)

    def xs_int_int_dict(*args) -> int32:
        _sync_constants()
        converted = []
        for i, arg in enumerate(args):
            if i % 2 == 0:
                converted.append(_encode_key(arg))
            else:
                converted.append(arg)
        return _vid.xs_vector_int_dict(*converted)

    def xs_int_int_dict_get(dct: int32 = int32(-1), key: int32 = int32(-1), dft: int32 = int32(-1)) -> int32:
        return _vid.xs_vector_int_dict_get(dct, _encode_key(key), dft)

    def xs_int_int_dict_remove(dct: int32 = int32(-1), key: int32 = int32(-1)) -> int32:
        return _vid.xs_vector_int_dict_remove(dct, _encode_key(key))

    def xs_int_int_dict_contains(dct: int32 = int32(-1), key: int32 = int32(-1)) -> bool:
        return _vid.xs_vector_int_dict_contains(dct, _encode_key(key))

    def xs_int_int_dict_size(dct: int32 = int32(-1)) -> int32:
        return _vid.xs_vector_int_dict_size(dct)

    def xs_int_int_dict_clear(dct: int32 = int32(-1)) -> int32:
        return _vid.xs_vector_int_dict_clear(dct)

    def xs_int_int_dict_copy(dct: int32 = int32(-1)) -> int32:
        return _vid.xs_vector_int_dict_copy(dct)

    def xs_int_int_dict_to_string(dct: int32 = int32(-1)) -> str:
        capacity: int32 = xs_array_get_size(dct)
        s: str = "{"
        first: bool = True
        for i in i32range(1, capacity, 4):
            key = _vid._xs_vector_int_dict_get_stored_key(dct, i)
            if key != _vid.c_vector_int_dict_empty_key:
                if first:
                    first = False
                else:
                    s += ", "
                s += f"{_decode_key(key)}: {_vid._xs_vector_int_dict_get_stored_value(dct, i)}"
        s += "}"
        return s

    def xs_int_int_dict_last_error() -> int32:
        return _vid.xs_vector_int_dict_last_error()

    def xs_int_int_dict_next_key(dct: int32 = int32(-1), is_first: bool = True, prev_key: int32 = int32(-1)) -> int32:
        key = _vid.xs_vector_int_dict_next_key(dct, is_first, _encode_key(prev_key))
        if _vid.xs_vector_int_dict_last_error() == _vid.c_vector_int_dict_success:
            return _decode_key(key)
        return compat.c_int_int_dict_generic_error

    def xs_int_int_dict_has_next(dct: int32 = int32(-1), is_first: bool = True, prev_key: int32 = int32(-1)) -> bool:
        return _vid.xs_vector_int_dict_has_next(dct, is_first, _encode_key(prev_key))

    def xs_int_int_dict_update(source: int32 = int32(-1), dct: int32 = int32(-1)) -> int32:
        _sync_constants()
        return _vid.xs_vector_int_dict_update(source, dct)

    def xs_int_int_dict_put_if_absent(dct: int32 = int32(-1), key: int32 = int32(-1), val: int32 = int32(0)) -> int32:
        _sync_constants()
        return _vid.xs_vector_int_dict_put_if_absent(dct, _encode_key(key), val)

    def xs_int_int_dict_keys(dct: int32 = int32(-1)) -> int32:
        vec_arr: int32 = _vid.xs_vector_int_dict_keys(dct)
        if vec_arr < 0:
            return vec_arr
        size: int32 = xs_array_get_size(vec_arr)
        arr: int32 = xs_array_create_int(size, int32(0))
        if arr < 0:
            return arr
        for i in i32range(0, size):
            xs_array_set_int(arr, i, _decode_key(xs_array_get_vector(vec_arr, i)))
        return arr

    def xs_int_int_dict_values(dct: int32 = int32(-1)) -> int32:
        return _vid.xs_vector_int_dict_values(dct)

    def xs_int_int_dict_equals(a: int32 = int32(-1), b: int32 = int32(-1)) -> bool:
        return _vid.xs_vector_int_dict_equals(a, b)

    compat.int32 = int32
    compat.float32 = _vid.float32
    compat.i32range = i32range
    compat.xs_array_create_int = xs_array_create_int
    compat.xs_array_get_int = xs_array_get_int
    compat.xs_array_get_size = xs_array_get_size
    compat.c_int_int_dict_success = _vid.c_vector_int_dict_success
    compat.c_int_int_dict_generic_error = _vid.c_vector_int_dict_generic_error
    compat.c_int_int_dict_no_key_error = _vid.c_vector_int_dict_no_key_error
    compat.c_int_int_dict_resize_failed_error = _vid.c_vector_int_dict_resize_failed_error
    compat.c_int_int_dict_max_capacity_error = _vid.c_vector_int_dict_max_capacity_error
    compat.c_int_int_dict_max_capacity = int32(((_vid.c_vector_int_dict_max_capacity - 1) // 2) + 1)
    compat.c_int_int_dict_max_load_factor = _vid.c_vector_int_dict_max_load_factor
    compat.c_int_int_dict_empty_key = int32(-999999999)
    compat.c_int_int_dict_initial_capacity = int32(((_vid.c_vector_int_dict_initial_capacity - 1) // 2) + 1)
    compat.c_int_int_dict_hash_constant = _vid.c_vector_int_dict_hash_constant
    compat.xs_int_int_dict_create = xs_int_int_dict_create
    compat.xs_int_int_dict_put = xs_int_int_dict_put
    compat.xs_int_int_dict = xs_int_int_dict
    compat.xs_int_int_dict_get = xs_int_int_dict_get
    compat.xs_int_int_dict_remove = xs_int_int_dict_remove
    compat.xs_int_int_dict_contains = xs_int_int_dict_contains
    compat.xs_int_int_dict_size = xs_int_int_dict_size
    compat.xs_int_int_dict_clear = xs_int_int_dict_clear
    compat.xs_int_int_dict_copy = xs_int_int_dict_copy
    compat.xs_int_int_dict_to_string = xs_int_int_dict_to_string
    compat.xs_int_int_dict_last_error = xs_int_int_dict_last_error
    compat.xs_int_int_dict_next_key = xs_int_int_dict_next_key
    compat.xs_int_int_dict_has_next = xs_int_int_dict_has_next
    compat.xs_int_int_dict_update = xs_int_int_dict_update
    compat.xs_int_int_dict_put_if_absent = xs_int_int_dict_put_if_absent
    compat.xs_int_int_dict_keys = xs_int_int_dict_keys
    compat.xs_int_int_dict_values = xs_int_int_dict_values
    compat.xs_int_int_dict_equals = xs_int_int_dict_equals
    return compat


def _load_base_test_module():
    module_path = Path(__file__).with_name("test_int_int_dict3.py")
    spec = importlib.util.spec_from_file_location("_vector_int_dict_base_tests", module_path)
    module = importlib.util.module_from_spec(spec)
    previous = sys.modules.get("xs.int_int_dict3")
    sys.modules["xs.int_int_dict3"] = _build_compat_module()
    try:
        spec.loader.exec_module(module)
    finally:
        if previous is None:
            del sys.modules["xs.int_int_dict3"]
        else:
            sys.modules["xs.int_int_dict3"] = previous
    return module


_BASE_TESTS = _load_base_test_module()


class VectorIntDictCompatibilityTest(_BASE_TESTS.IntIntDictTest):
    def test_rehash_past_max_capacity_reports_max_capacity_error(self):
        orig = _vid.c_vector_int_dict_max_capacity
        _vid.c_vector_int_dict_max_capacity = int32(65)
        try:
            xs_dct = _vid.xs_vector_int_dict_create()
            expected = {}
            for key in range(12):
                _vid.xs_vector_int_dict_put(xs_dct, _encode_key(int32(key)), int32(key))
                expected[key] = key
                self.assertEqual(_vid.c_vector_int_dict_no_key_error, _vid.xs_vector_int_dict_last_error())
            self.assertEqual(
                _vid.c_vector_int_dict_generic_error,
                _vid.xs_vector_int_dict_put(xs_dct, _encode_key(int32(12)), int32(12)),
            )
            self.assertEqual(_vid.c_vector_int_dict_max_capacity_error, _vid.xs_vector_int_dict_last_error())
            self._assert_dicts_equal(xs_dct, expected)
        finally:
            _vid.c_vector_int_dict_max_capacity = orig

    def test_put_if_absent_past_max_capacity_preserves_existing_entries(self):
        orig = _vid.c_vector_int_dict_max_capacity
        _vid.c_vector_int_dict_max_capacity = int32(65)
        try:
            xs_dct = _vid.xs_vector_int_dict_create()
            expected = {}
            for key in range(12):
                _vid.xs_vector_int_dict_put_if_absent(xs_dct, _encode_key(int32(key)), int32(key))
                expected[key] = key
                self.assertEqual(_vid.c_vector_int_dict_no_key_error, _vid.xs_vector_int_dict_last_error())
            self.assertEqual(
                _vid.c_vector_int_dict_generic_error,
                _vid.xs_vector_int_dict_put_if_absent(xs_dct, _encode_key(int32(12)), int32(12)),
            )
            self.assertEqual(_vid.c_vector_int_dict_max_capacity_error, _vid.xs_vector_int_dict_last_error())
            self._assert_dicts_equal(xs_dct, expected)
        finally:
            _vid.c_vector_int_dict_max_capacity = orig


class VectorIntDictNativeTest(unittest.TestCase):

    def test_keys_returns_vector_array(self):
        xs_dct = _vid.xs_vector_int_dict_create()
        k1 = vector(1.0, 2.0, 3.0)
        k2 = vector(4.0, 5.0, 6.0)
        _vid.xs_vector_int_dict_put(xs_dct, k1, int32(10))
        _vid.xs_vector_int_dict_put(xs_dct, k2, int32(20))

        arr = _vid.xs_vector_int_dict_keys(xs_dct)
        self.assertEqual(2, xs_array_get_size(arr))
        keys = [xs_array_get_vector(arr, int32(i)) for i in range(xs_array_get_size(arr))]
        self.assertEqual([k1, k2], keys)

    def test_to_string_mentions_vector_key(self):
        xs_dct = _vid.xs_vector_int_dict_create()
        key = vector(1.5, 2.5, 3.5)
        _vid.xs_vector_int_dict_put(xs_dct, key, int32(7))
        s = _vid.xs_vector_int_dict_to_string(xs_dct)
        self.assertIn("(1.5, 2.5, 3.5)", s)
        self.assertIn("7", s)
