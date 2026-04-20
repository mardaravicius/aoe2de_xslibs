import random
import unittest

import numpy as np
from numpy import float32, int32

import xs.float_vector_dict as _fvd
from xs.float_vector_dict import *
from xs_converter.functions import bit_cast_to_float, bit_cast_to_int, vector, xs_array_get_float, xs_array_get_size, xs_array_get_vector

np.seterr(over="ignore")


def _bits_to_float(bits: int | int32) -> float32:
    return bit_cast_to_float(int32(bits))


def _canonical_nan_bits() -> int32:
    return c_float_vector_dict_canonical_nan_bits


def _canonical_bits(value: float | float32) -> int:
    key: float32 = float32(value)
    if key != key:
        return int(_canonical_nan_bits())
    if key == float32(0.0):
        return 0
    return int(bit_cast_to_int(key))


def _vec(n: int) -> XsVector:
    return vector(float32(n), float32(n + 1), float32(n + 2))


class FloatVectorDictTest(unittest.TestCase):
    def _iter_dict(self, xs_dct: int32):
        result: dict[int, XsVector] = {}
        first: bool = True
        key: float32 = c_float_vector_dict_empty_key
        while xs_float_vector_dict_has_next(xs_dct, first, key):
            key = xs_float_vector_dict_next_key(xs_dct, first, key)
            first = False
            result[_canonical_bits(key)] = xs_float_vector_dict_get(xs_dct, key)
        return result

    def _assert_dict_matches(self, xs_dct: int32, expected: dict[int, XsVector]):
        self.assertEqual(len(expected), xs_float_vector_dict_size(xs_dct))
        for bits, val in expected.items():
            key = bit_cast_to_float(int32(bits))
            self.assertTrue(xs_float_vector_dict_contains(xs_dct, key))
            self.assertEqual(val, xs_float_vector_dict_get(xs_dct, key))
            self.assertEqual(c_float_vector_dict_success, xs_float_vector_dict_last_error())

    def test_put_get_remove_with_finite_keys(self):
        xs_dct = xs_float_vector_dict_create()
        expected: dict[int, XsVector] = {}
        for i in range(-12, 13):
            key = float32(i) + float32(0.75)
            val = _vec(i)
            prev = xs_float_vector_dict_put(xs_dct, key, val)
            self.assertEqual(c_float_vector_dict_no_key_error, xs_float_vector_dict_last_error())
            self.assertEqual(c_float_vector_dict_generic_error_vector, prev)
            expected[_canonical_bits(key)] = val
        self._assert_dict_matches(xs_dct, expected)

        for i in range(-4, 5):
            key = float32(i) + float32(0.75)
            prev = xs_float_vector_dict_put(xs_dct, key, _vec(i + 50))
            self.assertEqual(c_float_vector_dict_success, xs_float_vector_dict_last_error())
            self.assertEqual(_vec(i), prev)
            expected[_canonical_bits(key)] = _vec(i + 50)
        self._assert_dict_matches(xs_dct, expected)

        for i in range(-2, 3):
            key = float32(i) + float32(0.75)
            removed = xs_float_vector_dict_remove(xs_dct, key)
            self.assertEqual(c_float_vector_dict_success, xs_float_vector_dict_last_error())
            self.assertEqual(expected.pop(_canonical_bits(key)), removed)
        self._assert_dict_matches(xs_dct, expected)

    def test_zero_keys_are_canonicalized(self):
        xs_dct = xs_float_vector_dict_create()
        pos_zero = _bits_to_float(0)
        neg_zero = _bits_to_float(-2147483648)
        self.assertEqual(c_float_vector_dict_generic_error_vector, xs_float_vector_dict_put(xs_dct, pos_zero, _vec(1)))
        self.assertEqual(c_float_vector_dict_no_key_error, xs_float_vector_dict_last_error())
        self.assertEqual(_vec(1), xs_float_vector_dict_get(xs_dct, neg_zero))
        prev = xs_float_vector_dict_put(xs_dct, neg_zero, _vec(2))
        self.assertEqual(c_float_vector_dict_success, xs_float_vector_dict_last_error())
        self.assertEqual(_vec(1), prev)
        self.assertEqual(1, xs_float_vector_dict_size(xs_dct))
        self.assertEqual(_vec(2), xs_float_vector_dict_get(xs_dct, pos_zero))

    def test_nan_keys_are_canonicalized(self):
        xs_dct = xs_float_vector_dict_create()
        nan1 = _bits_to_float(int32(214328934) * 10 + 5)
        nan2 = _bits_to_float(int32(214328934) * 10 + 6)
        self.assertEqual(c_float_vector_dict_generic_error_vector, xs_float_vector_dict_put(xs_dct, nan1, _vec(3)))
        self.assertEqual(c_float_vector_dict_no_key_error, xs_float_vector_dict_last_error())
        self.assertTrue(xs_float_vector_dict_contains(xs_dct, nan2))
        self.assertEqual(_vec(3), xs_float_vector_dict_get(xs_dct, nan2))
        prev = xs_float_vector_dict_put(xs_dct, nan2, _vec(4))
        self.assertEqual(c_float_vector_dict_success, xs_float_vector_dict_last_error())
        self.assertEqual(_vec(3), prev)
        self.assertEqual(1, xs_float_vector_dict_size(xs_dct))
        self.assertEqual(_vec(4), xs_float_vector_dict_get(xs_dct, nan1))

    def test_keys_and_values_arrays_match(self):
        xs_dct = xs_float_vector_dict_create()
        expected: dict[int, XsVector] = {}
        items = [
            (float32(1.5), _vec(1)),
            (_bits_to_float(-2147483648), _vec(2)),
            (_bits_to_float(int32(214328934) * 10 + 5), _vec(3)),
            (float32(-7.25), _vec(4)),
        ]
        for key, val in items:
            xs_float_vector_dict_put(xs_dct, key, val)
            expected[_canonical_bits(key)] = val
        keys_arr = xs_float_vector_dict_keys(xs_dct)
        vals_arr = xs_float_vector_dict_values(xs_dct)
        self.assertEqual(xs_array_get_size(keys_arr), xs_array_get_size(vals_arr))
        reconstructed = {}
        for i in range(xs_array_get_size(keys_arr)):
            reconstructed[_canonical_bits(xs_array_get_float(keys_arr, int32(i)))] = xs_array_get_vector(vals_arr, int32(i))
        self.assertEqual(expected, reconstructed)

    def test_keys_array_uses_canonical_zero_and_nan(self):
        xs_dct = xs_float_vector_dict_create()
        xs_float_vector_dict_put(xs_dct, _bits_to_float(-2147483648), _vec(1))
        xs_float_vector_dict_put(xs_dct, _bits_to_float(int32(214328934) * 10 + 9), _vec(2))
        keys_arr = xs_float_vector_dict_keys(xs_dct)
        bits = {int(bit_cast_to_int(xs_array_get_float(keys_arr, int32(i)))) for i in range(xs_array_get_size(keys_arr))}
        self.assertEqual({0, int(_canonical_nan_bits())}, bits)

    def test_put_if_absent_uses_normalized_keys(self):
        xs_dct = xs_float_vector_dict_create()
        self.assertEqual(c_float_vector_dict_generic_error_vector, xs_float_vector_dict_put_if_absent(xs_dct, _bits_to_float(-2147483648), _vec(10)))
        self.assertEqual(c_float_vector_dict_no_key_error, xs_float_vector_dict_last_error())
        self.assertEqual(_vec(10), xs_float_vector_dict_put_if_absent(xs_dct, float32(0.0), _vec(11)))
        self.assertEqual(c_float_vector_dict_success, xs_float_vector_dict_last_error())

        nan = _bits_to_float(int32(214328934) * 10 + 5)
        self.assertEqual(c_float_vector_dict_generic_error_vector, xs_float_vector_dict_put_if_absent(xs_dct, nan, _vec(20)))
        self.assertEqual(c_float_vector_dict_no_key_error, xs_float_vector_dict_last_error())
        self.assertEqual(_vec(20), xs_float_vector_dict_put_if_absent(xs_dct, _bits_to_float(int32(214328934) * 10 + 6), _vec(21)))
        self.assertEqual(c_float_vector_dict_success, xs_float_vector_dict_last_error())

    def test_copy_update_and_equals(self):
        xs_dct = xs_float_vector_dict_create()
        xs_float_vector_dict_put(xs_dct, float32(2.5), _vec(1))
        xs_float_vector_dict_put(xs_dct, _bits_to_float(-2147483648), _vec(2))
        xs_float_vector_dict_put(xs_dct, _bits_to_float(int32(214328934) * 10 + 5), _vec(3))

        copied = xs_float_vector_dict_copy(xs_dct)
        self.assertTrue(xs_float_vector_dict_equals(xs_dct, copied))

        target = xs_float_vector_dict_create()
        self.assertEqual(c_float_vector_dict_success, xs_float_vector_dict_update(target, xs_dct))
        self.assertTrue(xs_float_vector_dict_equals(xs_dct, target))

        xs_float_vector_dict_put(copied, float32(9.5), _vec(4))
        self.assertFalse(xs_float_vector_dict_equals(xs_dct, copied))

    def test_sentinel_key_is_rejected(self):
        xs_dct = xs_float_vector_dict_create()
        self.assertEqual(c_float_vector_dict_generic_error_vector, xs_float_vector_dict_put(xs_dct, c_float_vector_dict_empty_key, _vec(1)))
        self.assertEqual(c_float_vector_dict_generic_error, xs_float_vector_dict_last_error())
        self.assertEqual(0, xs_float_vector_dict_size(xs_dct))
        self.assertFalse(xs_float_vector_dict_contains(xs_dct, c_float_vector_dict_empty_key))

    def test_clear_reuse_and_constructor(self):
        xs_dct = xs_float_vector_dict(float32(1.5), _vec(1), c_float_vector_dict_empty_key, _vec(2))
        self.assertEqual(1, xs_float_vector_dict_size(xs_dct))
        self.assertEqual(_vec(1), xs_float_vector_dict_get(xs_dct, float32(1.5)))
        self.assertEqual(c_float_vector_dict_success, xs_float_vector_dict_clear(xs_dct))
        self.assertEqual(0, xs_float_vector_dict_size(xs_dct))
        xs_float_vector_dict_put(xs_dct, _bits_to_float(int32(214328934) * 10 + 5), _vec(5))
        self.assertEqual(_vec(5), xs_float_vector_dict_get(xs_dct, _bits_to_float(int32(214328934) * 10 + 6)))

    def test_rehash_preserves_special_keys(self):
        xs_dct = xs_float_vector_dict_create()
        expected: dict[int, XsVector] = {
            0: _vec(100),
            int(_canonical_nan_bits()): _vec(200),
        }
        xs_float_vector_dict_put(xs_dct, _bits_to_float(-2147483648), _vec(100))
        xs_float_vector_dict_put(xs_dct, _bits_to_float(int32(214328934) * 10 + 5), _vec(200))
        for i in range(120):
            key = float32(i) + float32(0.125)
            val = _vec(i)
            xs_float_vector_dict_put(xs_dct, key, val)
            expected[_canonical_bits(key)] = val
        self._assert_dict_matches(xs_dct, expected)
        self.assertEqual(expected, self._iter_dict(xs_dct))

    def test_rehash_past_max_capacity_reports_max_capacity_error(self):
        orig = _fvd.c_float_vector_dict_max_capacity
        _fvd.c_float_vector_dict_max_capacity = int32(65)
        try:
            xs_dct = xs_float_vector_dict_create()
            expected: dict[int, XsVector] = {}
            for key in range(12):
                float_key = float32(key) + float32(0.5)
                xs_float_vector_dict_put(xs_dct, float_key, _vec(key))
                expected[_canonical_bits(float_key)] = _vec(key)
                self.assertEqual(c_float_vector_dict_no_key_error, xs_float_vector_dict_last_error())
            self.assertEqual(
                c_float_vector_dict_generic_error_vector,
                xs_float_vector_dict_put(xs_dct, float32(12.5), _vec(12)),
            )
            self.assertEqual(c_float_vector_dict_max_capacity_error, xs_float_vector_dict_last_error())
            self._assert_dict_matches(xs_dct, expected)
        finally:
            _fvd.c_float_vector_dict_max_capacity = orig

    def test_put_if_absent_past_max_capacity_preserves_existing_entries(self):
        orig = _fvd.c_float_vector_dict_max_capacity
        _fvd.c_float_vector_dict_max_capacity = int32(65)
        try:
            xs_dct = xs_float_vector_dict_create()
            expected: dict[int, XsVector] = {}
            for key in range(12):
                float_key = float32(key) + float32(0.5)
                xs_float_vector_dict_put_if_absent(xs_dct, float_key, _vec(key))
                expected[_canonical_bits(float_key)] = _vec(key)
                self.assertEqual(c_float_vector_dict_no_key_error, xs_float_vector_dict_last_error())
            self.assertEqual(
                c_float_vector_dict_generic_error_vector,
                xs_float_vector_dict_put_if_absent(xs_dct, float32(12.5), _vec(12)),
            )
            self.assertEqual(c_float_vector_dict_max_capacity_error, xs_float_vector_dict_last_error())
            self._assert_dict_matches(xs_dct, expected)
        finally:
            _fvd.c_float_vector_dict_max_capacity = orig

    def test_randomized_put_remove_cycle(self):
        xs_dct = xs_float_vector_dict_create()
        expected: dict[int, XsVector] = {}
        specials = [
            float32(0.0),
            _bits_to_float(-2147483648),
            _bits_to_float(int32(214328934) * 10 + 5),
            _bits_to_float(int32(214328934) * 10 + 6),
        ]
        for _ in range(250):
            key = random.choice(specials) if random.randint(0, 3) == 0 else float32(random.randint(-50, 50)) + float32(0.375)
            bits = _canonical_bits(key)
            if random.randint(0, 2) <= 1:
                val = _vec(random.randint(-20, 20))
                xs_float_vector_dict_put(xs_dct, key, val)
                expected[bits] = val
            else:
                xs_float_vector_dict_remove(xs_dct, key)
                if xs_float_vector_dict_last_error() == c_float_vector_dict_success:
                    expected.pop(bits, None)
        self._assert_dict_matches(xs_dct, expected)
