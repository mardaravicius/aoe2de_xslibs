import random
import unittest

import numpy as np
from numpy import float32, int32

import xs.float_int_dict as _fid
from xs.float_int_dict import *
from xs_converter.functions import bit_cast_to_float, bit_cast_to_int, xs_array_get_float, xs_array_get_int, xs_array_get_size

np.seterr(over="ignore")


def _bits_to_float(bits: int | int32) -> float32:
    return bit_cast_to_float(int32(bits))


def _canonical_nan_bits() -> int32:
    return int32(-8388607)


def _canonical_bits(value: float | float32) -> int:
    key: float32 = float32(value)
    if key != key:
        return int(_canonical_nan_bits())
    if key == float32(0.0):
        return 0
    return int(bit_cast_to_int(key))


def _value_for_bits(bits: int) -> float32:
    return bit_cast_to_float(int32(bits))


class FloatIntDictTest(unittest.TestCase):
    def _iter_dict(self, xs_dct: int32):
        result: dict[int, int] = {}
        first: bool = True
        key: float32 = c_float_int_dict_empty_key
        while xs_float_int_dict_has_next(xs_dct, first, key):
            key = xs_float_int_dict_next_key(xs_dct, first, key)
            first = False
            val = xs_float_int_dict_get(xs_dct, key)
            result[_canonical_bits(key)] = int(val)
        return result

    def _assert_dict_matches(self, xs_dct: int32, expected: dict[int, int]):
        self.assertEqual(len(expected), xs_float_int_dict_size(xs_dct))
        for bits, val in expected.items():
            key = _value_for_bits(bits)
            self.assertTrue(xs_float_int_dict_contains(xs_dct, key))
            self.assertEqual(val, xs_float_int_dict_get(xs_dct, key))
            self.assertEqual(c_float_int_dict_success, xs_float_int_dict_last_error())

    def test_empty_dict(self):
        xs_dct = xs_float_int_dict_create()
        self.assertEqual(0, xs_float_int_dict_size(xs_dct))
        self.assertFalse(xs_float_int_dict_contains(xs_dct, float32(5.5)))
        self.assertEqual(77, xs_float_int_dict_get(xs_dct, float32(5.5), int32(77)))
        self.assertEqual(c_float_int_dict_no_key_error, xs_float_int_dict_last_error())
        self.assertFalse(xs_float_int_dict_has_next(xs_dct, True, c_float_int_dict_empty_key))
        self.assertEqual("{}", xs_float_int_dict_to_string(xs_dct))

    def test_put_get_remove_with_finite_keys(self):
        xs_dct = xs_float_int_dict_create()
        expected: dict[int, int] = {}
        for i in range(-20, 21):
            key = float32(i) + float32(0.5)
            val = int32(i * 7)
            previous = xs_float_int_dict_put(xs_dct, key, val)
            self.assertEqual(c_float_int_dict_no_key_error, xs_float_int_dict_last_error())
            self.assertEqual(c_float_int_dict_generic_error, previous)
            expected[_canonical_bits(key)] = int(val)
        self._assert_dict_matches(xs_dct, expected)

        for i in range(-10, 11):
            key = float32(i) + float32(0.5)
            old_val = xs_float_int_dict_put(xs_dct, key, int32(i))
            self.assertEqual(c_float_int_dict_success, xs_float_int_dict_last_error())
            self.assertEqual(i * 7, int(old_val))
            expected[_canonical_bits(key)] = i
        self._assert_dict_matches(xs_dct, expected)

        for i in range(-5, 6):
            key = float32(i) + float32(0.5)
            removed = xs_float_int_dict_remove(xs_dct, key)
            self.assertEqual(c_float_int_dict_success, xs_float_int_dict_last_error())
            self.assertEqual(expected.pop(_canonical_bits(key)), int(removed))
        self._assert_dict_matches(xs_dct, expected)

    def test_zero_keys_are_canonicalized(self):
        xs_dct = xs_float_int_dict_create()
        pos_zero = _bits_to_float(0)
        neg_zero = _bits_to_float(-2147483648)

        self.assertEqual(c_float_int_dict_generic_error, xs_float_int_dict_put(xs_dct, pos_zero, int32(11)))
        self.assertEqual(c_float_int_dict_no_key_error, xs_float_int_dict_last_error())
        self.assertTrue(xs_float_int_dict_contains(xs_dct, neg_zero))
        self.assertEqual(11, xs_float_int_dict_get(xs_dct, neg_zero))

        previous = xs_float_int_dict_put(xs_dct, neg_zero, int32(22))
        self.assertEqual(c_float_int_dict_success, xs_float_int_dict_last_error())
        self.assertEqual(11, int(previous))
        self.assertEqual(22, xs_float_int_dict_get(xs_dct, pos_zero))
        self.assertEqual(1, xs_float_int_dict_size(xs_dct))

        removed = xs_float_int_dict_remove(xs_dct, neg_zero)
        self.assertEqual(c_float_int_dict_success, xs_float_int_dict_last_error())
        self.assertEqual(22, int(removed))
        self.assertFalse(xs_float_int_dict_contains(xs_dct, pos_zero))

    def test_nan_keys_are_canonicalized(self):
        xs_dct = xs_float_int_dict_create()
        nan1 = _bits_to_float(int32(214328934) * 10 + 5)
        nan2 = _bits_to_float(int32(214328934) * 10 + 6)

        self.assertEqual(c_float_int_dict_generic_error, xs_float_int_dict_put(xs_dct, nan1, int32(13)))
        self.assertEqual(c_float_int_dict_no_key_error, xs_float_int_dict_last_error())
        self.assertTrue(xs_float_int_dict_contains(xs_dct, nan2))
        self.assertEqual(13, xs_float_int_dict_get(xs_dct, nan2))

        previous = xs_float_int_dict_put(xs_dct, nan2, int32(17))
        self.assertEqual(c_float_int_dict_success, xs_float_int_dict_last_error())
        self.assertEqual(13, int(previous))
        self.assertEqual(17, xs_float_int_dict_get(xs_dct, nan1))
        self.assertEqual(1, xs_float_int_dict_size(xs_dct))

        removed = xs_float_int_dict_remove(xs_dct, nan1)
        self.assertEqual(c_float_int_dict_success, xs_float_int_dict_last_error())
        self.assertEqual(17, int(removed))
        self.assertFalse(xs_float_int_dict_contains(xs_dct, nan2))

    def test_keys_array_returns_canonical_zero_and_nan(self):
        xs_dct = xs_float_int_dict_create()
        neg_zero = _bits_to_float(-2147483648)
        nan = _bits_to_float(int32(214328934) * 10 + 9)
        xs_float_int_dict_put(xs_dct, neg_zero, int32(1))
        xs_float_int_dict_put(xs_dct, nan, int32(2))

        arr = xs_float_int_dict_keys(xs_dct)
        self.assertEqual(2, xs_array_get_size(arr))
        bits = {int(bit_cast_to_int(xs_array_get_float(arr, int32(i)))) for i in range(xs_array_get_size(arr))}
        self.assertEqual({0, int(_canonical_nan_bits())}, bits)

    def test_values_array_matches_keys_order(self):
        xs_dct = xs_float_int_dict_create()
        expected: dict[int, int] = {}
        keys = [float32(-3.5), float32(2.25), _bits_to_float(-2147483648), _bits_to_float(int32(214328934) * 10 + 8)]
        for idx, key in enumerate(keys):
            val = idx * 100
            xs_float_int_dict_put(xs_dct, key, int32(val))
            expected[_canonical_bits(key)] = val

        keys_arr = xs_float_int_dict_keys(xs_dct)
        vals_arr = xs_float_int_dict_values(xs_dct)
        self.assertEqual(xs_array_get_size(keys_arr), xs_array_get_size(vals_arr))
        reconstructed = {}
        for i in range(xs_array_get_size(keys_arr)):
            reconstructed[_canonical_bits(xs_array_get_float(keys_arr, int32(i)))] = int(xs_array_get_int(vals_arr, int32(i)))
        self.assertEqual(expected, reconstructed)

    def test_iteration_handles_canonical_keys(self):
        xs_dct = xs_float_int_dict_create()
        expected = {
            _canonical_bits(float32(1.5)): 10,
            _canonical_bits(_bits_to_float(-2147483648)): 20,
            _canonical_bits(_bits_to_float(int32(214328934) * 10 + 7)): 30,
            _canonical_bits(float32(-2.75)): 40,
        }
        for bits, val in list(expected.items()):
            xs_float_int_dict_put(xs_dct, _value_for_bits(bits), int32(val))
        self.assertEqual(expected, self._iter_dict(xs_dct))

    def test_rehash_preserves_zero_nan_and_finite_keys(self):
        xs_dct = xs_float_int_dict_create()
        expected: dict[int, int] = {}
        xs_float_int_dict_put(xs_dct, _bits_to_float(-2147483648), int32(100))
        expected[0] = 100
        xs_float_int_dict_put(xs_dct, _bits_to_float(int32(214328934) * 10 + 5), int32(200))
        expected[int(_canonical_nan_bits())] = 200
        for i in range(150):
            key = float32(i) + float32(0.125)
            val = i * 3
            xs_float_int_dict_put(xs_dct, key, int32(val))
            expected[_canonical_bits(key)] = val
        self._assert_dict_matches(xs_dct, expected)
        self.assertEqual(expected, self._iter_dict(xs_dct))

    def test_sentinel_key_is_rejected(self):
        xs_dct = xs_float_int_dict_create()
        result = xs_float_int_dict_put(xs_dct, c_float_int_dict_empty_key, int32(42))
        self.assertEqual(c_float_int_dict_generic_error, result)
        self.assertEqual(c_float_int_dict_generic_error, xs_float_int_dict_last_error())
        self.assertEqual(0, xs_float_int_dict_size(xs_dct))
        self.assertFalse(xs_float_int_dict_contains(xs_dct, c_float_int_dict_empty_key))
        self.assertEqual(77, xs_float_int_dict_get(xs_dct, c_float_int_dict_empty_key, int32(77)))
        self.assertEqual(c_float_int_dict_no_key_error, xs_float_int_dict_last_error())

    def test_copy_update_and_equals_with_special_keys(self):
        xs_dct = xs_float_int_dict_create()
        xs_float_int_dict_put(xs_dct, _bits_to_float(-2147483648), int32(1))
        xs_float_int_dict_put(xs_dct, _bits_to_float(int32(214328934) * 10 + 5), int32(2))
        xs_float_int_dict_put(xs_dct, float32(3.5), int32(3))

        copied = xs_float_int_dict_copy(xs_dct)
        self.assertTrue(xs_float_int_dict_equals(xs_dct, copied))

        target = xs_float_int_dict_create()
        self.assertEqual(c_float_int_dict_success, xs_float_int_dict_update(target, xs_dct))
        self.assertTrue(xs_float_int_dict_equals(xs_dct, target))

        xs_float_int_dict_put(copied, float32(7.25), int32(9))
        self.assertFalse(xs_float_int_dict_equals(xs_dct, copied))

    def test_put_if_absent_uses_normalized_keys(self):
        xs_dct = xs_float_int_dict_create()
        neg_zero = _bits_to_float(-2147483648)
        nan = _bits_to_float(int32(214328934) * 10 + 5)

        self.assertEqual(c_float_int_dict_generic_error, xs_float_int_dict_put_if_absent(xs_dct, neg_zero, int32(10)))
        self.assertEqual(c_float_int_dict_no_key_error, xs_float_int_dict_last_error())
        self.assertEqual(10, xs_float_int_dict_put_if_absent(xs_dct, float32(0.0), int32(11)))
        self.assertEqual(c_float_int_dict_success, xs_float_int_dict_last_error())
        self.assertEqual(10, xs_float_int_dict_get(xs_dct, float32(0.0)))

        self.assertEqual(c_float_int_dict_generic_error, xs_float_int_dict_put_if_absent(xs_dct, nan, int32(20)))
        self.assertEqual(c_float_int_dict_no_key_error, xs_float_int_dict_last_error())
        self.assertEqual(20, xs_float_int_dict_put_if_absent(xs_dct, _bits_to_float(int32(214328934) * 10 + 6), int32(21)))
        self.assertEqual(c_float_int_dict_success, xs_float_int_dict_last_error())
        self.assertEqual(20, xs_float_int_dict_get(xs_dct, nan))

    def test_constructor_stops_at_sentinel_key(self):
        xs_dct = xs_float_int_dict(float32(1.5), int32(10), c_float_int_dict_empty_key, int32(20))
        self.assertEqual(1, xs_float_int_dict_size(xs_dct))
        self.assertEqual(10, xs_float_int_dict_get(xs_dct, float32(1.5)))

    def test_clear_then_reuse(self):
        xs_dct = xs_float_int_dict_create()
        for i in range(50):
            xs_float_int_dict_put(xs_dct, float32(i) + float32(0.25), int32(i))
        self.assertEqual(c_float_int_dict_success, xs_float_int_dict_clear(xs_dct))
        self.assertEqual(0, xs_float_int_dict_size(xs_dct))

        xs_float_int_dict_put(xs_dct, _bits_to_float(-2147483648), int32(33))
        xs_float_int_dict_put(xs_dct, _bits_to_float(int32(214328934) * 10 + 5), int32(44))
        self.assertEqual(33, xs_float_int_dict_get(xs_dct, float32(0.0)))
        self.assertEqual(44, xs_float_int_dict_get(xs_dct, _bits_to_float(int32(214328934) * 10 + 6)))

    def test_rehash_past_max_capacity_reports_max_capacity_error(self):
        orig = _fid.c_float_int_dict_max_capacity
        _fid.c_float_int_dict_max_capacity = int32(33)
        try:
            xs_dct = xs_float_int_dict_create()
            expected: dict[int, int] = {}
            for key in range(12):
                xs_float_int_dict_put(xs_dct, float32(key) + float32(0.5), int32(key))
                expected[_canonical_bits(float32(key) + float32(0.5))] = key
                self.assertEqual(c_float_int_dict_no_key_error, xs_float_int_dict_last_error())
            self.assertEqual(
                c_float_int_dict_generic_error,
                xs_float_int_dict_put(xs_dct, float32(12.5), int32(12)),
            )
            self.assertEqual(c_float_int_dict_max_capacity_error, xs_float_int_dict_last_error())
            self._assert_dict_matches(xs_dct, expected)
        finally:
            _fid.c_float_int_dict_max_capacity = orig

    def test_put_if_absent_past_max_capacity_preserves_existing_entries(self):
        orig = _fid.c_float_int_dict_max_capacity
        _fid.c_float_int_dict_max_capacity = int32(33)
        try:
            xs_dct = xs_float_int_dict_create()
            expected: dict[int, int] = {}
            for key in range(12):
                xs_float_int_dict_put_if_absent(xs_dct, float32(key) + float32(0.5), int32(key))
                expected[_canonical_bits(float32(key) + float32(0.5))] = key
                self.assertEqual(c_float_int_dict_no_key_error, xs_float_int_dict_last_error())
            self.assertEqual(
                c_float_int_dict_generic_error,
                xs_float_int_dict_put_if_absent(xs_dct, float32(12.5), int32(12)),
            )
            self.assertEqual(c_float_int_dict_max_capacity_error, xs_float_int_dict_last_error())
            self._assert_dict_matches(xs_dct, expected)
        finally:
            _fid.c_float_int_dict_max_capacity = orig

    def test_randomized_put_remove_cycle(self):
        xs_dct = xs_float_int_dict_create()
        expected: dict[int, int] = {}
        special_keys = [
            float32(0.0),
            _bits_to_float(-2147483648),
            _bits_to_float(int32(214328934) * 10 + 5),
            _bits_to_float(int32(214328934) * 10 + 6),
        ]
        for _ in range(300):
            choice = random.randint(0, 3)
            if choice == 0:
                key = random.choice(special_keys)
            else:
                key = float32(random.randint(-50, 50)) + float32(0.25)
            bits = _canonical_bits(key)
            if random.randint(0, 2) <= 1:
                val = random.randint(-200, 200)
                xs_float_int_dict_put(xs_dct, key, int32(val))
                expected[bits] = val
            else:
                xs_float_int_dict_remove(xs_dct, key)
                if xs_float_int_dict_last_error() == c_float_int_dict_success:
                    expected.pop(bits, None)
        self._assert_dict_matches(xs_dct, expected)
        self.assertEqual(expected, self._iter_dict(xs_dct))
