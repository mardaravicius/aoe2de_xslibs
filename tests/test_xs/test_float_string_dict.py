import random
import unittest

import numpy as np
from numpy import float32, int32

import xs.float_string_dict as _fsd
from xs.float_string_dict import *
from xs_converter.functions import bit_cast_to_float, bit_cast_to_int, xs_array_get_float, xs_array_get_size, xs_array_get_string

np.seterr(over="ignore")


def _bits_to_float(bits: int | int32) -> float32:
    return bit_cast_to_float(int32(bits))


def _canonical_nan_bits() -> int32:
    return c_float_string_dict_canonical_nan_bits


def _canonical_bits(value: float | float32) -> int:
    key: float32 = float32(value)
    if key != key:
        return int(_canonical_nan_bits())
    if key == float32(0.0):
        return 0
    return int(bit_cast_to_int(key))


def _value_for_bits(bits: int) -> float32:
    return bit_cast_to_float(int32(bits))


class FloatStringDictTest(unittest.TestCase):
    def _iter_dict(self, xs_dct: int32):
        result: dict[int, str] = {}
        first: bool = True
        key: float32 = c_float_string_dict_empty_key
        while xs_float_string_dict_has_next(xs_dct, first, key):
            key = xs_float_string_dict_next_key(xs_dct, first, key)
            first = False
            result[_canonical_bits(key)] = xs_float_string_dict_get(xs_dct, key)
        return result

    def _assert_dict_matches(self, xs_dct: int32, expected: dict[int, str]):
        self.assertEqual(len(expected), xs_float_string_dict_size(xs_dct))
        for bits, val in expected.items():
            key = _value_for_bits(bits)
            self.assertTrue(xs_float_string_dict_contains(xs_dct, key))
            self.assertEqual(val, xs_float_string_dict_get(xs_dct, key))
            self.assertEqual(c_float_string_dict_success, xs_float_string_dict_last_error())

    def test_put_get_remove_with_finite_keys(self):
        xs_dct = xs_float_string_dict_create()
        expected: dict[int, str] = {}
        for i in range(-15, 16):
            key = float32(i) + float32(0.25)
            val = f"v{i}"
            prev = xs_float_string_dict_put(xs_dct, key, val)
            self.assertEqual(c_float_string_dict_no_key_error, xs_float_string_dict_last_error())
            self.assertEqual("-1", prev)
            expected[_canonical_bits(key)] = val
        self._assert_dict_matches(xs_dct, expected)

        for i in range(-5, 6):
            key = float32(i) + float32(0.25)
            prev = xs_float_string_dict_put(xs_dct, key, f"new{i}")
            self.assertEqual(c_float_string_dict_success, xs_float_string_dict_last_error())
            self.assertEqual(f"v{i}", prev)
            expected[_canonical_bits(key)] = f"new{i}"
        self._assert_dict_matches(xs_dct, expected)

        for i in range(-3, 4):
            key = float32(i) + float32(0.25)
            removed = xs_float_string_dict_remove(xs_dct, key)
            self.assertEqual(c_float_string_dict_success, xs_float_string_dict_last_error())
            self.assertEqual(expected.pop(_canonical_bits(key)), removed)
        self._assert_dict_matches(xs_dct, expected)

    def test_zero_keys_are_canonicalized(self):
        xs_dct = xs_float_string_dict_create()
        pos_zero = _bits_to_float(0)
        neg_zero = _bits_to_float(-2147483648)
        self.assertEqual("-1", xs_float_string_dict_put(xs_dct, pos_zero, "zero"))
        self.assertEqual(c_float_string_dict_no_key_error, xs_float_string_dict_last_error())
        self.assertEqual("zero", xs_float_string_dict_get(xs_dct, neg_zero))
        prev = xs_float_string_dict_put(xs_dct, neg_zero, "other")
        self.assertEqual(c_float_string_dict_success, xs_float_string_dict_last_error())
        self.assertEqual("zero", prev)
        self.assertEqual(1, xs_float_string_dict_size(xs_dct))
        self.assertEqual("other", xs_float_string_dict_get(xs_dct, pos_zero))

    def test_nan_keys_are_canonicalized(self):
        xs_dct = xs_float_string_dict_create()
        nan1 = _bits_to_float(int32(214328934) * 10 + 5)
        nan2 = _bits_to_float(int32(214328934) * 10 + 6)
        self.assertEqual("-1", xs_float_string_dict_put(xs_dct, nan1, "n1"))
        self.assertEqual(c_float_string_dict_no_key_error, xs_float_string_dict_last_error())
        self.assertTrue(xs_float_string_dict_contains(xs_dct, nan2))
        self.assertEqual("n1", xs_float_string_dict_get(xs_dct, nan2))
        prev = xs_float_string_dict_put(xs_dct, nan2, "n2")
        self.assertEqual(c_float_string_dict_success, xs_float_string_dict_last_error())
        self.assertEqual("n1", prev)
        self.assertEqual(1, xs_float_string_dict_size(xs_dct))
        self.assertEqual("n2", xs_float_string_dict_get(xs_dct, nan1))

    def test_keys_and_values_arrays_match(self):
        xs_dct = xs_float_string_dict_create()
        expected: dict[int, str] = {}
        items = [
            (float32(1.5), "a"),
            (_bits_to_float(-2147483648), "b"),
            (_bits_to_float(int32(214328934) * 10 + 5), "c"),
            (float32(-3.75), ""),
        ]
        for key, val in items:
            xs_float_string_dict_put(xs_dct, key, val)
            expected[_canonical_bits(key)] = val
        keys_arr = xs_float_string_dict_keys(xs_dct)
        vals_arr = xs_float_string_dict_values(xs_dct)
        self.assertEqual(xs_array_get_size(keys_arr), xs_array_get_size(vals_arr))
        reconstructed = {}
        for i in range(xs_array_get_size(keys_arr)):
            reconstructed[_canonical_bits(xs_array_get_float(keys_arr, int32(i)))] = xs_array_get_string(vals_arr, int32(i))
        self.assertEqual(expected, reconstructed)

    def test_keys_array_uses_canonical_zero_and_nan(self):
        xs_dct = xs_float_string_dict_create()
        xs_float_string_dict_put(xs_dct, _bits_to_float(-2147483648), "zero")
        xs_float_string_dict_put(xs_dct, _bits_to_float(int32(214328934) * 10 + 9), "nan")
        keys_arr = xs_float_string_dict_keys(xs_dct)
        bits = {int(bit_cast_to_int(xs_array_get_float(keys_arr, int32(i)))) for i in range(xs_array_get_size(keys_arr))}
        self.assertEqual({0, int(_canonical_nan_bits())}, bits)

    def test_put_if_absent_uses_normalized_keys(self):
        xs_dct = xs_float_string_dict_create()
        self.assertEqual("-1", xs_float_string_dict_put_if_absent(xs_dct, _bits_to_float(-2147483648), "zero"))
        self.assertEqual(c_float_string_dict_no_key_error, xs_float_string_dict_last_error())
        self.assertEqual("zero", xs_float_string_dict_put_if_absent(xs_dct, float32(0.0), "other"))
        self.assertEqual(c_float_string_dict_success, xs_float_string_dict_last_error())
        self.assertEqual("zero", xs_float_string_dict_get(xs_dct, float32(0.0)))

        nan = _bits_to_float(int32(214328934) * 10 + 5)
        self.assertEqual("-1", xs_float_string_dict_put_if_absent(xs_dct, nan, "nan"))
        self.assertEqual(c_float_string_dict_no_key_error, xs_float_string_dict_last_error())
        self.assertEqual("nan", xs_float_string_dict_put_if_absent(xs_dct, _bits_to_float(int32(214328934) * 10 + 6), "other-nan"))
        self.assertEqual(c_float_string_dict_success, xs_float_string_dict_last_error())

    def test_copy_update_and_equals(self):
        xs_dct = xs_float_string_dict_create()
        xs_float_string_dict_put(xs_dct, float32(2.5), "a")
        xs_float_string_dict_put(xs_dct, _bits_to_float(-2147483648), "b")
        xs_float_string_dict_put(xs_dct, _bits_to_float(int32(214328934) * 10 + 5), "c")

        copied = xs_float_string_dict_copy(xs_dct)
        self.assertTrue(xs_float_string_dict_equals(xs_dct, copied))

        target = xs_float_string_dict_create()
        self.assertEqual(c_float_string_dict_success, xs_float_string_dict_update(target, xs_dct))
        self.assertTrue(xs_float_string_dict_equals(xs_dct, target))

        xs_float_string_dict_put(copied, float32(7.25), "d")
        self.assertFalse(xs_float_string_dict_equals(xs_dct, copied))

    def test_sentinel_key_is_rejected(self):
        xs_dct = xs_float_string_dict_create()
        self.assertEqual("-1", xs_float_string_dict_put(xs_dct, c_float_string_dict_empty_key, "x"))
        self.assertEqual(c_float_string_dict_generic_error, xs_float_string_dict_last_error())
        self.assertEqual(0, xs_float_string_dict_size(xs_dct))
        self.assertFalse(xs_float_string_dict_contains(xs_dct, c_float_string_dict_empty_key))

    def test_clear_reuse_and_constructor(self):
        xs_dct = xs_float_string_dict(float32(1.5), "a", c_float_string_dict_empty_key, "b")
        self.assertEqual(1, xs_float_string_dict_size(xs_dct))
        self.assertEqual("a", xs_float_string_dict_get(xs_dct, float32(1.5)))
        self.assertEqual(c_float_string_dict_success, xs_float_string_dict_clear(xs_dct))
        self.assertEqual(0, xs_float_string_dict_size(xs_dct))
        xs_float_string_dict_put(xs_dct, _bits_to_float(int32(214328934) * 10 + 5), "")
        self.assertEqual("", xs_float_string_dict_get(xs_dct, _bits_to_float(int32(214328934) * 10 + 6)))

    def test_rehash_preserves_special_keys(self):
        xs_dct = xs_float_string_dict_create()
        expected: dict[int, str] = {
            0: "zero",
            int(_canonical_nan_bits()): "nan",
        }
        xs_float_string_dict_put(xs_dct, _bits_to_float(-2147483648), "zero")
        xs_float_string_dict_put(xs_dct, _bits_to_float(int32(214328934) * 10 + 5), "nan")
        for i in range(120):
            key = float32(i) + float32(0.5)
            val = f"v{i}"
            xs_float_string_dict_put(xs_dct, key, val)
            expected[_canonical_bits(key)] = val
        self._assert_dict_matches(xs_dct, expected)
        self.assertEqual(expected, self._iter_dict(xs_dct))

    def test_rehash_past_max_capacity_reports_max_capacity_error(self):
        orig = _fsd.c_float_string_dict_max_capacity
        _fsd.c_float_string_dict_max_capacity = int32(18)
        try:
            xs_dct = xs_float_string_dict_create()
            expected: dict[int, str] = {}
            for key in range(12):
                float_key = float32(key) + float32(0.5)
                xs_float_string_dict_put(xs_dct, float_key, f"v{key}")
                expected[_canonical_bits(float_key)] = f"v{key}"
                self.assertEqual(c_float_string_dict_no_key_error, xs_float_string_dict_last_error())
            self.assertEqual(
                "-1",
                xs_float_string_dict_put(xs_dct, float32(12.5), "v12"),
            )
            self.assertEqual(c_float_string_dict_max_capacity_error, xs_float_string_dict_last_error())
            self._assert_dict_matches(xs_dct, expected)
        finally:
            _fsd.c_float_string_dict_max_capacity = orig

    def test_put_if_absent_past_max_capacity_preserves_existing_entries(self):
        orig = _fsd.c_float_string_dict_max_capacity
        _fsd.c_float_string_dict_max_capacity = int32(18)
        try:
            xs_dct = xs_float_string_dict_create()
            expected: dict[int, str] = {}
            for key in range(12):
                float_key = float32(key) + float32(0.5)
                xs_float_string_dict_put_if_absent(xs_dct, float_key, f"v{key}")
                expected[_canonical_bits(float_key)] = f"v{key}"
                self.assertEqual(c_float_string_dict_no_key_error, xs_float_string_dict_last_error())
            self.assertEqual(
                "-1",
                xs_float_string_dict_put_if_absent(xs_dct, float32(12.5), "v12"),
            )
            self.assertEqual(c_float_string_dict_max_capacity_error, xs_float_string_dict_last_error())
            self._assert_dict_matches(xs_dct, expected)
        finally:
            _fsd.c_float_string_dict_max_capacity = orig

    def test_copy_of_cleared_dict_does_not_leak_ghost_bucket_arrays(self):
        xs_dct = xs_float_string_dict_create()
        for k in range(50):
            xs_float_string_dict_put(xs_dct, float32(k) + float32(0.25), f"v{k}")
        xs_float_string_dict_clear(xs_dct)
        xs_dct_copy = xs_float_string_dict_copy(xs_dct)
        id_after = _fsd.xs_array_create_int(int32(1))
        self.assertEqual(xs_dct_copy + 2, id_after)

    def test_randomized_put_remove_cycle(self):
        xs_dct = xs_float_string_dict_create()
        expected: dict[int, str] = {}
        specials = [
            float32(0.0),
            _bits_to_float(-2147483648),
            _bits_to_float(int32(214328934) * 10 + 5),
            _bits_to_float(int32(214328934) * 10 + 6),
        ]
        for _ in range(250):
            key = random.choice(specials) if random.randint(0, 3) == 0 else float32(random.randint(-50, 50)) + float32(0.125)
            bits = _canonical_bits(key)
            if random.randint(0, 2) <= 1:
                val = f"s{random.randint(-100, 100)}"
                xs_float_string_dict_put(xs_dct, key, val)
                expected[bits] = val
            else:
                xs_float_string_dict_remove(xs_dct, key)
                if xs_float_string_dict_last_error() == c_float_string_dict_success:
                    expected.pop(bits, None)
        self._assert_dict_matches(xs_dct, expected)


class FloatStringDictAllocationCleanupTest(unittest.TestCase):
    def setUp(self):
        self.orig_create_int = _fsd.xs_array_create_int
        self.orig_create_string = _fsd.xs_array_create_string
        self.orig_resize_int = _fsd.xs_array_resize_int
        self.orig_resize_string = _fsd.xs_array_resize_string

    def tearDown(self):
        _fsd.xs_array_create_int = self.orig_create_int
        _fsd.xs_array_create_string = self.orig_create_string
        _fsd.xs_array_resize_int = self.orig_resize_int
        _fsd.xs_array_resize_string = self.orig_resize_string

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

        _fsd.xs_array_create_int = _create_int
        _fsd.xs_array_create_string = _create_string
        _fsd.xs_array_resize_int = _resize_int

        self.assertEqual(_fsd.c_float_string_dict_generic_error, _fsd.xs_float_string_dict_create())
        self.assertEqual(0, _fsd.xs_array_get_size(created["arr"]))

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

        _fsd.xs_array_create_int = _create_int
        _fsd.xs_array_create_string = _create_string
        _fsd.xs_array_resize_string = _resize_string

        self.assertEqual(_fsd.c_float_string_dict_generic_error, _fsd.xs_float_string_dict_create())
        self.assertEqual(0, calls["create_string"])
        self.assertEqual(0, calls["resize_string"])

    def test_copy_shrinks_int_array_when_string_array_allocation_fails(self):
        created: dict[str, int32] = {}
        xs_dct = _fsd.xs_float_string_dict_create()
        _fsd.xs_float_string_dict_put(xs_dct, float32(1.5), "one")

        def _create_int(*args, **kwargs):
            arr = self.orig_create_int(*args, **kwargs)
            created["arr"] = arr
            return arr

        def _create_string(*args, **kwargs):
            return int32(-1)

        def _resize_int(arr_id, new_size):
            self.orig_resize_int(arr_id, new_size)
            return int32(0)

        _fsd.xs_array_create_int = _create_int
        _fsd.xs_array_create_string = _create_string
        _fsd.xs_array_resize_int = _resize_int

        self.assertEqual(_fsd.c_float_string_dict_resize_failed_error, _fsd.xs_float_string_dict_copy(xs_dct))
        self.assertEqual(0, _fsd.xs_array_get_size(created["arr"]))

    def test_copy_returns_without_allocating_string_array_when_int_array_allocation_fails(self):
        calls: dict[str, int32] = {"create_string": int32(0), "resize_string": int32(0)}
        xs_dct = _fsd.xs_float_string_dict_create()
        _fsd.xs_float_string_dict_put(xs_dct, float32(1.5), "one")

        def _create_int(*args, **kwargs):
            return int32(-1)

        def _create_string(*args, **kwargs):
            calls["create_string"] += 1
            return self.orig_create_string(*args, **kwargs)

        def _resize_string(arr_id, new_size):
            calls["resize_string"] += 1
            return int32(0)

        _fsd.xs_array_create_int = _create_int
        _fsd.xs_array_create_string = _create_string
        _fsd.xs_array_resize_string = _resize_string

        self.assertEqual(_fsd.c_float_string_dict_resize_failed_error, _fsd.xs_float_string_dict_copy(xs_dct))
        self.assertEqual(0, calls["create_string"])
        self.assertEqual(0, calls["resize_string"])
