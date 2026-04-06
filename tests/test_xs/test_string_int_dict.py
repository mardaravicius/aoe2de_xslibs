import importlib.util
import sys
import types
import unittest
from pathlib import Path

import numpy as np
from numpy import float32, int32

import xs.string_int_dict as _sid
from xs_converter.functions import (
    xs_array_create_int,
    xs_array_get_int,
    xs_array_get_size,
    xs_array_get_string,
    xs_array_set_int,
)
from xs_converter.symbols import i32range

np.seterr(over="ignore")
EMPTY_KEY = "!<[empty"


def _encode_key(value: int | int32) -> str:
    encoded: int32 = int32(value)
    if encoded == int32(-999999999):
        return EMPTY_KEY
    return str(int(encoded))


def _decode_key(value: str) -> int32:
    if value == EMPTY_KEY:
        return int32(-999999999)
    return int32(int(value))


def _build_compat_module() -> types.ModuleType:
    compat = types.ModuleType("xs.int_int_dict3")

    def _sync_constants() -> None:
        _sid.c_string_int_dict_max_capacity = compat.c_int_int_dict_max_capacity

    def xs_int_int_dict_create() -> int32:
        _sync_constants()
        return _sid.xs_string_int_dict_create()

    def xs_int_int_dict_put(dct: int32 = int32(-1), key: int32 = int32(-1),
                            val: int32 = int32(0)) -> int32:
        _sync_constants()
        return _sid.xs_string_int_dict_put(dct, _encode_key(key), val)

    def xs_int_int_dict(*args) -> int32:
        _sync_constants()
        converted = []
        for i, arg in enumerate(args):
            if i % 2 == 0:
                converted.append(_encode_key(arg))
            else:
                converted.append(arg)
        return _sid.xs_string_int_dict(*converted)

    def xs_int_int_dict_get(dct: int32 = int32(-1), key: int32 = int32(-1),
                            dft: int32 = int32(-1)) -> int32:
        return _sid.xs_string_int_dict_get(dct, _encode_key(key), dft)

    def xs_int_int_dict_remove(dct: int32 = int32(-1), key: int32 = int32(-1)) -> int32:
        return _sid.xs_string_int_dict_remove(dct, _encode_key(key))

    def xs_int_int_dict_contains(dct: int32 = int32(-1), key: int32 = int32(-1)) -> bool:
        return _sid.xs_string_int_dict_contains(dct, _encode_key(key))

    def xs_int_int_dict_size(dct: int32 = int32(-1)) -> int32:
        return _sid.xs_string_int_dict_size(dct)

    def xs_int_int_dict_clear(dct: int32 = int32(-1)) -> int32:
        _sync_constants()
        return _sid.xs_string_int_dict_clear(dct)

    def xs_int_int_dict_copy(dct: int32 = int32(-1)) -> int32:
        return _sid.xs_string_int_dict_copy(dct)

    def xs_int_int_dict_to_string(dct: int32 = int32(-1)) -> str:
        keys_arr: int32 = _sid.xs_string_int_dict_keys(dct)
        vals_arr: int32 = _sid.xs_string_int_dict_values(dct)
        s: str = "{"
        first: bool = True
        for i in i32range(0, xs_array_get_size(keys_arr)):
            if first:
                first = False
            else:
                s += ", "
            s += f"{_decode_key(xs_array_get_string(keys_arr, i))}: {xs_array_get_int(vals_arr, i)}"
        s += "}"
        return s

    def xs_int_int_dict_last_error() -> int32:
        return _sid.xs_string_int_dict_last_error()

    def xs_int_int_dict_next_key(dct: int32 = int32(-1), is_first: bool = True,
                                 prev_key: int32 = int32(-1)) -> int32:
        result = _sid.xs_string_int_dict_next_key(dct, is_first, _encode_key(prev_key))
        if _sid.xs_string_int_dict_last_error() == _sid.c_string_int_dict_success:
            return _decode_key(result)
        return compat.c_int_int_dict_generic_error

    def xs_int_int_dict_has_next(dct: int32 = int32(-1), is_first: bool = True,
                                 prev_key: int32 = int32(-1)) -> bool:
        return _sid.xs_string_int_dict_has_next(dct, is_first, _encode_key(prev_key))

    def xs_int_int_dict_update(source: int32 = int32(-1), dct: int32 = int32(-1)) -> int32:
        _sync_constants()
        return _sid.xs_string_int_dict_update(source, dct)

    def xs_int_int_dict_put_if_absent(dct: int32 = int32(-1), key: int32 = int32(-1),
                                      val: int32 = int32(0)) -> int32:
        _sync_constants()
        return _sid.xs_string_int_dict_put_if_absent(dct, _encode_key(key), val)

    def xs_int_int_dict_keys(dct: int32 = int32(-1)) -> int32:
        str_arr: int32 = _sid.xs_string_int_dict_keys(dct)
        if str_arr < 0:
            return str_arr
        size: int32 = xs_array_get_size(str_arr)
        arr: int32 = xs_array_create_int(size, int32(0))
        if arr < 0:
            return arr
        for i in i32range(0, size):
            xs_array_set_int(arr, i, _decode_key(xs_array_get_string(str_arr, i)))
        return arr

    def xs_int_int_dict_values(dct: int32 = int32(-1)) -> int32:
        return _sid.xs_string_int_dict_values(dct)

    def xs_int_int_dict_equals(a: int32 = int32(-1), b: int32 = int32(-1)) -> bool:
        return _sid.xs_string_int_dict_equals(a, b)

    xs_int_int_dict_put.__module__ = "xs.int_int_dict3"
    xs_int_int_dict_put_if_absent.__module__ = "xs.int_int_dict3"

    compat.int32 = int32
    compat.float32 = float32
    compat.i32range = i32range
    compat.xs_array_create_int = xs_array_create_int
    compat.xs_array_get_int = xs_array_get_int
    compat.xs_array_get_size = xs_array_get_size
    compat.c_int_int_dict_success = _sid.c_string_int_dict_success
    compat.c_int_int_dict_generic_error = _sid.c_string_int_dict_generic_error
    compat.c_int_int_dict_no_key_error = _sid.c_string_int_dict_no_key_error
    compat.c_int_int_dict_resize_failed_error = _sid.c_string_int_dict_resize_failed_error
    compat.c_int_int_dict_max_capacity_error = _sid.c_string_int_dict_max_capacity_error
    compat.c_int_int_dict_max_capacity = _sid.c_string_int_dict_max_capacity
    compat.c_int_int_dict_max_load_factor = float32(1.0)
    compat.c_int_int_dict_empty_key = int32(-999999999)
    compat.c_int_int_dict_initial_capacity = _sid.c_string_int_dict_initial_capacity
    compat.c_int_int_dict_hash_constant = int32(0)
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
    spec = importlib.util.spec_from_file_location("_string_int_dict_base_tests", module_path)
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


class StringIntDictCompatibilityTest(_BASE_TESTS.IntIntDictTest):
    def test_rehash_past_max_capacity_reports_max_capacity_error(self):
        orig = _sid.c_string_int_dict_max_capacity
        _sid.c_string_int_dict_max_capacity = int32(12)
        try:
            xs_dct = _sid.xs_string_int_dict_create()
            expected = {}
            for key in range(12):
                _sid.xs_string_int_dict_put(xs_dct, _encode_key(int32(key)), int32(key))
                expected[key] = key
                self.assertEqual(_sid.c_string_int_dict_no_key_error, _sid.xs_string_int_dict_last_error())
            self.assertEqual(
                _sid.c_string_int_dict_generic_error,
                _sid.xs_string_int_dict_put(xs_dct, _encode_key(int32(12)), int32(12)),
            )
            self.assertEqual(_sid.c_string_int_dict_max_capacity_error, _sid.xs_string_int_dict_last_error())
            self._assert_dicts_equal(xs_dct, expected)
        finally:
            _sid.c_string_int_dict_max_capacity = orig

    def test_put_if_absent_past_max_capacity_preserves_existing_entries(self):
        orig = _sid.c_string_int_dict_max_capacity
        _sid.c_string_int_dict_max_capacity = int32(12)
        try:
            xs_dct = _sid.xs_string_int_dict_create()
            expected = {}
            for key in range(12):
                _sid.xs_string_int_dict_put_if_absent(xs_dct, _encode_key(int32(key)), int32(key))
                expected[key] = key
                self.assertEqual(_sid.c_string_int_dict_no_key_error, _sid.xs_string_int_dict_last_error())
            self.assertEqual(
                _sid.c_string_int_dict_generic_error,
                _sid.xs_string_int_dict_put_if_absent(xs_dct, _encode_key(int32(12)), int32(12)),
            )
            self.assertEqual(_sid.c_string_int_dict_max_capacity_error, _sid.xs_string_int_dict_last_error())
            self._assert_dicts_equal(xs_dct, expected)
        finally:
            _sid.c_string_int_dict_max_capacity = orig

    def test_copy_of_cleared_dict_does_not_leak_ghost_bucket_arrays(self):
        xs_dct = _sid.xs_string_int_dict_create()
        for k in range(50):
            _sid.xs_string_int_dict_put(xs_dct, _encode_key(int32(k)), int32(k * 10))
        _sid.xs_string_int_dict_clear(xs_dct)
        xs_dct_copy = _sid.xs_string_int_dict_copy(xs_dct)
        id_after = xs_array_create_int(int32(1))
        self.assertEqual(xs_dct_copy + 2, id_after)


class StringIntDictNativeTest(unittest.TestCase):
    def test_keys_returns_string_array(self):
        xs_dct = _sid.xs_string_int_dict_create()
        _sid.xs_string_int_dict_put(xs_dct, "one", int32(1))
        _sid.xs_string_int_dict_put(xs_dct, "two", int32(2))

        arr = _sid.xs_string_int_dict_keys(xs_dct)
        self.assertEqual(2, xs_array_get_size(arr))
        keys = [xs_array_get_string(arr, int32(i)) for i in range(xs_array_get_size(arr))]
        self.assertEqual(["one", "two"], keys)

    def test_to_string_mentions_quoted_string_key(self):
        xs_dct = _sid.xs_string_int_dict_create()
        _sid.xs_string_int_dict_put(xs_dct, "value", int32(5))
        s = _sid.xs_string_int_dict_to_string(xs_dct)
        self.assertIn('"value": 5', s)

    def test_empty_string_round_trips(self):
        xs_dct = _sid.xs_string_int_dict_create()
        _sid.xs_string_int_dict_put(xs_dct, "", int32(7))
        self.assertEqual(_sid.c_string_int_dict_no_key_error, _sid.xs_string_int_dict_last_error())
        self.assertTrue(_sid.xs_string_int_dict_contains(xs_dct, ""))
        self.assertEqual(7, _sid.xs_string_int_dict_get(xs_dct, ""))
        self.assertEqual(_sid.c_string_int_dict_success, _sid.xs_string_int_dict_last_error())

    def test_error_int_can_be_stored(self):
        xs_dct = _sid.xs_string_int_dict_create()
        _sid.xs_string_int_dict_put(xs_dct, "neg", int32(-1))
        self.assertEqual(-1, _sid.xs_string_int_dict_get(xs_dct, "neg"))
        self.assertEqual(_sid.c_string_int_dict_success, _sid.xs_string_int_dict_last_error())

    def test_equals_missing_key_with_default_like_value_false(self):
        a = _sid.xs_string_int_dict_create()
        b = _sid.xs_string_int_dict_create()
        _sid.xs_string_int_dict_put(a, "neg", int32(-1))
        self.assertFalse(_sid.xs_string_int_dict_equals(a, b))
        self.assertFalse(_sid.xs_string_int_dict_equals(b, a))

    def test_reserved_sentinel_key_cannot_be_stored(self):
        xs_dct = _sid.xs_string_int_dict_create()
        _sid.xs_string_int_dict_put(xs_dct, EMPTY_KEY, int32(42))
        self.assertFalse(_sid.xs_string_int_dict_contains(xs_dct, EMPTY_KEY))
        self.assertEqual(0, _sid.xs_string_int_dict_size(xs_dct))


class StringIntDictAllocationCleanupTest(unittest.TestCase):
    def setUp(self):
        self.orig_create_int = _sid.xs_array_create_int
        self.orig_create_string = _sid.xs_array_create_string
        self.orig_resize_int = _sid.xs_array_resize_int
        self.orig_resize_string = _sid.xs_array_resize_string

    def tearDown(self):
        _sid.xs_array_create_int = self.orig_create_int
        _sid.xs_array_create_string = self.orig_create_string
        _sid.xs_array_resize_int = self.orig_resize_int
        _sid.xs_array_resize_string = self.orig_resize_string

    def test_create_shrinks_int_array_when_string_array_allocation_fails(self):
        created: dict[str, int32] = {}

        def _create_int(*args, **kwargs):
            arr = self.orig_create_int(*args, **kwargs)
            created["arr"] = arr
            return arr

        def _create_string(*args, **kwargs):
            return int32(-1)

        def _resize_int(arr_id, new_size):
            self.orig_resize_int(arr_id, new_size)
            return int32(0)

        _sid.xs_array_create_int = _create_int
        _sid.xs_array_create_string = _create_string
        _sid.xs_array_resize_int = _resize_int

        self.assertEqual(_sid.c_string_int_dict_generic_error, _sid.xs_string_int_dict_create())
        self.assertEqual(0, xs_array_get_size(created["arr"]))

    def test_create_returns_without_allocating_string_array_when_int_array_allocation_fails(self):
        calls: dict[str, int32] = {"create_string": int32(0), "resize_string": int32(0)}

        def _create_int(*args, **kwargs):
            return int32(-1)

        def _create_string(*args, **kwargs):
            calls["create_string"] += 1
            return self.orig_create_string(*args, **kwargs)

        def _resize_string(arr_id, new_size):
            calls["resize_string"] += 1
            return int32(0)

        _sid.xs_array_create_int = _create_int
        _sid.xs_array_create_string = _create_string
        _sid.xs_array_resize_string = _resize_string

        self.assertEqual(_sid.c_string_int_dict_generic_error, _sid.xs_string_int_dict_create())
        self.assertEqual(0, calls["create_string"])
        self.assertEqual(0, calls["resize_string"])

    def test_copy_shrinks_int_array_when_string_array_allocation_fails(self):
        created: dict[str, int32] = {}
        xs_dct = _sid.xs_string_int_dict_create()
        _sid.xs_string_int_dict_put(xs_dct, "one", int32(1))

        def _create_int(*args, **kwargs):
            arr = self.orig_create_int(*args, **kwargs)
            created["arr"] = arr
            return arr

        def _create_string(*args, **kwargs):
            return int32(-1)

        def _resize_int(arr_id, new_size):
            self.orig_resize_int(arr_id, new_size)
            return int32(0)

        _sid.xs_array_create_int = _create_int
        _sid.xs_array_create_string = _create_string
        _sid.xs_array_resize_int = _resize_int

        self.assertEqual(_sid.c_string_int_dict_resize_failed_error, _sid.xs_string_int_dict_copy(xs_dct))
        self.assertEqual(0, xs_array_get_size(created["arr"]))

    def test_copy_returns_without_allocating_string_array_when_int_array_allocation_fails(self):
        calls: dict[str, int32] = {"create_string": int32(0), "resize_string": int32(0)}
        xs_dct = _sid.xs_string_int_dict_create()
        _sid.xs_string_int_dict_put(xs_dct, "one", int32(1))

        def _create_int(*args, **kwargs):
            return int32(-1)

        def _create_string(*args, **kwargs):
            calls["create_string"] += 1
            return self.orig_create_string(*args, **kwargs)

        def _resize_string(arr_id, new_size):
            calls["resize_string"] += 1
            return int32(0)

        _sid.xs_array_create_int = _create_int
        _sid.xs_array_create_string = _create_string
        _sid.xs_array_resize_string = _resize_string

        self.assertEqual(_sid.c_string_int_dict_resize_failed_error, _sid.xs_string_int_dict_copy(xs_dct))
        self.assertEqual(0, calls["create_string"])
        self.assertEqual(0, calls["resize_string"])

    def test_clear_rolls_back_key_array_when_int_resize_fails(self):
        xs_dct = _sid.xs_string_int_dict_create()
        for k in range(40):
            _sid.xs_string_int_dict_put(xs_dct, _encode_key(int32(k)), int32(k * 10))

        keys_arr = xs_array_get_int(xs_dct, int32(1))
        old_data_size = xs_array_get_size(xs_dct)
        old_keys_size = xs_array_get_size(keys_arr)
        old_size = _sid.xs_string_int_dict_size(xs_dct)

        def _resize_string(arr_id, new_size):
            return self.orig_resize_string(arr_id, new_size)

        def _resize_int(arr_id, new_size):
            return int32(0)

        _sid.xs_array_resize_string = _resize_string
        _sid.xs_array_resize_int = _resize_int

        self.assertEqual(_sid.c_string_int_dict_generic_error, _sid.xs_string_int_dict_clear(xs_dct))
        self.assertEqual(old_data_size, xs_array_get_size(xs_dct))
        self.assertEqual(old_keys_size, xs_array_get_size(keys_arr))
        self.assertEqual(old_size, _sid.xs_string_int_dict_size(xs_dct))
        self.assertEqual(int32(120), _sid.xs_string_int_dict_get(xs_dct, _encode_key(int32(12))))
        self.assertEqual(_sid.c_string_int_dict_success, _sid.xs_string_int_dict_last_error())
