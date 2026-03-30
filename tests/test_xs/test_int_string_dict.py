import importlib.util
import sys
import types
import unittest
from pathlib import Path

import numpy as np
from numpy import int32

import xs.int_string_dict as _isd
from xs_converter.functions import xs_array_create_int, xs_array_get_int, xs_array_get_size, xs_array_get_string, \
    xs_array_set_int
from xs_converter.symbols import i32range

np.seterr(over="ignore")


def _encode_value(value: int | int32) -> str:
    return str(int(int32(value)))


def _decode_value(value: str) -> int32:
    return int32(int(value))


def _build_compat_module() -> types.ModuleType:
    compat = types.ModuleType("xs.int_int_dict3")

    def _sync_constants() -> None:
        logical_slots: int32 = (compat.c_int_int_dict_max_capacity - 1) // 2
        _isd.c_int_string_dict_max_capacity = logical_slots + 2

    def xs_int_int_dict_create() -> int32:
        _sync_constants()
        return _isd.xs_int_string_dict_create()

    def xs_int_int_dict_put(dct: int32 = int32(-1), key: int32 = int32(-1), val: int32 = int32(0)) -> int32:
        _sync_constants()
        result = _isd.xs_int_string_dict_put(dct, key, _encode_value(val))
        if _isd.xs_int_string_dict_last_error() == _isd.c_int_string_dict_success:
            return _decode_value(result)
        return compat.c_int_int_dict_generic_error

    def xs_int_int_dict(*args) -> int32:
        _sync_constants()
        converted = []
        for i, arg in enumerate(args):
            if i % 2 == 1:
                converted.append(_encode_value(arg))
            else:
                converted.append(arg)
        return _isd.xs_int_string_dict(*converted)

    def xs_int_int_dict_get(dct: int32 = int32(-1), key: int32 = int32(-1), dft: int32 = int32(-1)) -> int32:
        result = _isd.xs_int_string_dict_get(dct, key, _encode_value(dft))
        return _decode_value(result)

    def xs_int_int_dict_remove(dct: int32 = int32(-1), key: int32 = int32(-1)) -> int32:
        result = _isd.xs_int_string_dict_remove(dct, key)
        if _isd.xs_int_string_dict_last_error() == _isd.c_int_string_dict_success:
            return _decode_value(result)
        return compat.c_int_int_dict_generic_error

    def xs_int_int_dict_contains(dct: int32 = int32(-1), key: int32 = int32(-1)) -> bool:
        return _isd.xs_int_string_dict_contains(dct, key)

    def xs_int_int_dict_size(dct: int32 = int32(-1)) -> int32:
        return _isd.xs_int_string_dict_size(dct)

    def xs_int_int_dict_clear(dct: int32 = int32(-1)) -> int32:
        return _isd.xs_int_string_dict_clear(dct)

    def xs_int_int_dict_copy(dct: int32 = int32(-1)) -> int32:
        return _isd.xs_int_string_dict_copy(dct)

    def xs_int_int_dict_to_string(dct: int32 = int32(-1)) -> str:
        capacity: int32 = xs_array_get_size(dct)
        values_arr: int32 = xs_array_get_int(dct, 1)
        s: str = "{"
        first: bool = True
        for i in i32range(2, capacity):
            key: int32 = xs_array_get_int(dct, i)
            if key != _isd.c_int_string_dict_empty_key:
                if first:
                    first = False
                else:
                    s += ", "
                s += f"{key}: {_decode_value(xs_array_get_string(values_arr, i - 2))}"
        s += "}"
        return s

    def xs_int_int_dict_last_error() -> int32:
        return _isd.xs_int_string_dict_last_error()

    def xs_int_int_dict_next_key(dct: int32 = int32(-1), is_first: bool = True,
                                  prev_key: int32 = int32(-1)) -> int32:
        return _isd.xs_int_string_dict_next_key(dct, is_first, prev_key)

    def xs_int_int_dict_has_next(dct: int32 = int32(-1), is_first: bool = True,
                                  prev_key: int32 = int32(-1)) -> bool:
        return _isd.xs_int_string_dict_has_next(dct, is_first, prev_key)

    def xs_int_int_dict_update(source: int32 = int32(-1), dct: int32 = int32(-1)) -> int32:
        _sync_constants()
        return _isd.xs_int_string_dict_update(source, dct)

    def xs_int_int_dict_put_if_absent(dct: int32 = int32(-1), key: int32 = int32(-1),
                                       val: int32 = int32(0)) -> int32:
        _sync_constants()
        result = _isd.xs_int_string_dict_put_if_absent(dct, key, _encode_value(val))
        if _isd.xs_int_string_dict_last_error() == _isd.c_int_string_dict_success:
            return _decode_value(result)
        return compat.c_int_int_dict_generic_error

    def xs_int_int_dict_keys(dct: int32 = int32(-1)) -> int32:
        return _isd.xs_int_string_dict_keys(dct)

    def xs_int_int_dict_values(dct: int32 = int32(-1)) -> int32:
        str_arr: int32 = _isd.xs_int_string_dict_values(dct)
        if str_arr < 0:
            return str_arr
        size: int32 = xs_array_get_size(str_arr)
        arr: int32 = xs_array_create_int(size, int32(0))
        if arr < 0:
            return arr
        for i in i32range(0, size):
            xs_array_set_int(arr, i, _decode_value(xs_array_get_string(str_arr, i)))
        return arr

    def xs_int_int_dict_equals(a: int32 = int32(-1), b: int32 = int32(-1)) -> bool:
        return _isd.xs_int_string_dict_equals(a, b)

    xs_int_int_dict_put.__module__ = "xs.int_int_dict3"
    xs_int_int_dict_put_if_absent.__module__ = "xs.int_int_dict3"

    compat.int32 = int32
    compat.float32 = _isd.float32
    compat.i32range = i32range
    compat.xs_array_create_int = xs_array_create_int
    compat.xs_array_get_int = xs_array_get_int
    compat.xs_array_get_size = xs_array_get_size
    compat.c_int_int_dict_success = _isd.c_int_string_dict_success
    compat.c_int_int_dict_generic_error = _isd.c_int_string_dict_generic_error
    compat.c_int_int_dict_no_key_error = _isd.c_int_string_dict_no_key_error
    compat.c_int_int_dict_resize_failed_error = _isd.c_int_string_dict_resize_failed_error
    compat.c_int_int_dict_max_capacity_error = _isd.c_int_string_dict_max_capacity_error
    compat.c_int_int_dict_max_capacity = int32(((_isd.c_int_string_dict_max_capacity - 2) * 2) + 1)
    compat.c_int_int_dict_max_load_factor = _isd.c_int_string_dict_max_load_factor
    compat.c_int_int_dict_empty_key = _isd.c_int_string_dict_empty_key
    compat.c_int_int_dict_initial_capacity = int32(((_isd.c_int_string_dict_initial_capacity - 2) * 2) + 1)
    compat.c_int_int_dict_hash_constant = _isd.c_int_string_dict_hash_constant
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
    spec = importlib.util.spec_from_file_location("_int_string_dict_base_tests", module_path)
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


class IntStringDictCompatibilityTest(_BASE_TESTS.IntIntDictTest):
    def test_rehash_past_max_capacity_reports_max_capacity_error(self):
        orig = _isd.c_int_string_dict_max_capacity
        _isd.c_int_string_dict_max_capacity = int32(18)
        try:
            xs_dct = _isd.xs_int_string_dict_create()
            expected = {}
            for key in range(12):
                _isd.xs_int_string_dict_put(xs_dct, int32(key), _encode_value(int32(key)))
                expected[key] = key
                self.assertEqual(_isd.c_int_string_dict_no_key_error, _isd.xs_int_string_dict_last_error())
            self.assertEqual(
                "-1",
                _isd.xs_int_string_dict_put(xs_dct, int32(12), _encode_value(int32(12))),
            )
            self.assertEqual(_isd.c_int_string_dict_max_capacity_error, _isd.xs_int_string_dict_last_error())
            self._assert_dicts_equal(xs_dct, expected)
        finally:
            _isd.c_int_string_dict_max_capacity = orig

    def test_put_if_absent_past_max_capacity_preserves_existing_entries(self):
        orig = _isd.c_int_string_dict_max_capacity
        _isd.c_int_string_dict_max_capacity = int32(18)
        try:
            xs_dct = _isd.xs_int_string_dict_create()
            expected = {}
            for key in range(12):
                _isd.xs_int_string_dict_put_if_absent(xs_dct, int32(key), _encode_value(int32(key)))
                expected[key] = key
                self.assertEqual(_isd.c_int_string_dict_no_key_error, _isd.xs_int_string_dict_last_error())
            self.assertEqual(
                "-1",
                _isd.xs_int_string_dict_put_if_absent(xs_dct, int32(12), _encode_value(int32(12))),
            )
            self.assertEqual(_isd.c_int_string_dict_max_capacity_error, _isd.xs_int_string_dict_last_error())
            self._assert_dicts_equal(xs_dct, expected)
        finally:
            _isd.c_int_string_dict_max_capacity = orig

    def test_copy_of_cleared_dict_does_not_leak_ghost_bucket_arrays(self):
        xs_dct = _isd.xs_int_string_dict_create()
        for k in range(50):
            _isd.xs_int_string_dict_put(xs_dct, int32(k), _encode_value(int32(k * 10)))
        _isd.xs_int_string_dict_clear(xs_dct)
        xs_dct_copy = _isd.xs_int_string_dict_copy(xs_dct)
        id_after = xs_array_create_int(int32(1))
        self.assertEqual(xs_dct_copy + 2, id_after)


class IntStringDictNativeTest(unittest.TestCase):

    def test_values_returns_string_array(self):
        xs_dct = _isd.xs_int_string_dict_create()
        _isd.xs_int_string_dict_put(xs_dct, int32(1), "one")
        _isd.xs_int_string_dict_put(xs_dct, int32(2), "two")

        arr = _isd.xs_int_string_dict_values(xs_dct)
        self.assertEqual(2, xs_array_get_size(arr))
        values = [xs_array_get_string(arr, int32(i)) for i in range(xs_array_get_size(arr))]
        self.assertEqual(["one", "two"], values)

    def test_to_string_mentions_quoted_string_value(self):
        xs_dct = _isd.xs_int_string_dict_create()
        _isd.xs_int_string_dict_put(xs_dct, int32(5), "value")
        s = _isd.xs_int_string_dict_to_string(xs_dct)
        self.assertIn('5: "value"', s)

    def test_empty_string_round_trips(self):
        xs_dct = _isd.xs_int_string_dict_create()
        _isd.xs_int_string_dict_put(xs_dct, int32(7), "")
        self.assertEqual(_isd.c_int_string_dict_no_key_error, _isd.xs_int_string_dict_last_error())
        self.assertTrue(_isd.xs_int_string_dict_contains(xs_dct, int32(7)))
        self.assertEqual("", _isd.xs_int_string_dict_get(xs_dct, int32(7)))
        self.assertEqual(_isd.c_int_string_dict_success, _isd.xs_int_string_dict_last_error())

    def test_error_string_can_be_stored(self):
        xs_dct = _isd.xs_int_string_dict_create()
        _isd.xs_int_string_dict_put(xs_dct, int32(9), "-1")
        self.assertEqual("-1", _isd.xs_int_string_dict_get(xs_dct, int32(9)))
        self.assertEqual(_isd.c_int_string_dict_success, _isd.xs_int_string_dict_last_error())


class IntStringDictAllocationCleanupTest(unittest.TestCase):
    def setUp(self):
        self.orig_create_int = _isd.xs_array_create_int
        self.orig_create_string = _isd.xs_array_create_string
        self.orig_resize_int = _isd.xs_array_resize_int
        self.orig_resize_string = _isd.xs_array_resize_string

    def tearDown(self):
        _isd.xs_array_create_int = self.orig_create_int
        _isd.xs_array_create_string = self.orig_create_string
        _isd.xs_array_resize_int = self.orig_resize_int
        _isd.xs_array_resize_string = self.orig_resize_string

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

        _isd.xs_array_create_int = _create_int
        _isd.xs_array_create_string = _create_string
        _isd.xs_array_resize_int = _resize_int

        self.assertEqual(_isd.c_int_string_dict_generic_error, _isd.xs_int_string_dict_create())
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

        _isd.xs_array_create_int = _create_int
        _isd.xs_array_create_string = _create_string
        _isd.xs_array_resize_string = _resize_string

        self.assertEqual(_isd.c_int_string_dict_generic_error, _isd.xs_int_string_dict_create())
        self.assertEqual(0, calls["create_string"])
        self.assertEqual(0, calls["resize_string"])

    def test_copy_shrinks_int_array_when_string_array_allocation_fails(self):
        created: dict[str, int32] = {}
        xs_dct = _isd.xs_int_string_dict_create()
        _isd.xs_int_string_dict_put(xs_dct, int32(1), "one")

        def _create_int(*args, **kwargs):
            arr = self.orig_create_int(*args, **kwargs)
            created["arr"] = arr
            return arr

        def _create_string(*args, **kwargs):
            return int32(-1)

        def _resize_int(arr_id, new_size):
            self.orig_resize_int(arr_id, new_size)
            return int32(0)

        _isd.xs_array_create_int = _create_int
        _isd.xs_array_create_string = _create_string
        _isd.xs_array_resize_int = _resize_int

        self.assertEqual(_isd.c_int_string_dict_resize_failed_error, _isd.xs_int_string_dict_copy(xs_dct))
        self.assertEqual(0, xs_array_get_size(created["arr"]))

    def test_copy_returns_without_allocating_string_array_when_int_array_allocation_fails(self):
        calls: dict[str, int32] = {"create_string": int32(0), "resize_string": int32(0)}
        xs_dct = _isd.xs_int_string_dict_create()
        _isd.xs_int_string_dict_put(xs_dct, int32(1), "one")

        def _create_int(*args, **kwargs):
            return int32(-1)

        def _create_string(*args, **kwargs):
            calls["create_string"] += 1
            return self.orig_create_string(*args, **kwargs)

        def _resize_string(arr_id, new_size):
            calls["resize_string"] += 1
            return int32(0)

        _isd.xs_array_create_int = _create_int
        _isd.xs_array_create_string = _create_string
        _isd.xs_array_resize_string = _resize_string

        self.assertEqual(_isd.c_int_string_dict_resize_failed_error, _isd.xs_int_string_dict_copy(xs_dct))
        self.assertEqual(0, calls["create_string"])
        self.assertEqual(0, calls["resize_string"])
