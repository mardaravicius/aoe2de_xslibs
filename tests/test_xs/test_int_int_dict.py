import random
import unittest

from xs.int_int_dict2 import *


class IntIntDictTest(unittest.TestCase):

    def _iter_dict(self, xs_dct: int32):
        result = {}
        first = True
        key = int32(-1)
        while xs_int_int_dict_has_next(xs_dct, first, key):
            key = xs_int_int_dict_next_key(xs_dct, first, key)
            first = False
            val = xs_int_int_dict_get(xs_dct, key)
            result[int(key)] = int(val)
        return result

    def _assert_dicts_equal(self, xs_dct: int32, dct: dict[int | int32, int | int32]):
        self.assertEqual(len(dct), xs_int_int_dict_size(xs_dct))
        for k, v in dct.items():
            self.assertTrue(xs_int_int_dict_contains(xs_dct, int32(k)))
            self.assertEqual(v, xs_int_int_dict_get(xs_dct, int32(k)))

    def test_xs_int_int_dict_put(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for _ in i32range(100):
            k = random.randint(-100, 100)
            v = k * -1
            xs_prev = xs_int_int_dict_put(xs_dct, int32(k), int32(v))
            if xs_int_int_dict_last_error() == c_int_int_dict_no_key_error:
                xs_prev = None
            prev = dct.get(k)
            dct[k] = v
            self.assertEqual(prev, xs_prev)
            self.assertEqual(dct[k], xs_int_int_dict_get(xs_dct, int32(k)))
            self.assertEqual(len(dct), xs_int_int_dict_size(xs_dct))

    def test_xs_int_int_dict(self):
        test_data = [
            tuple(i32range(0, 0)),
            tuple(i32range(0, 2)),
            tuple(i32range(0, 4)),
            tuple(i32range(0, 6)),
            tuple(i32range(0, 8)),
            tuple(i32range(0, 10)),
            tuple(i32range(0, 12)),
        ]

        for data in test_data:
            xs_dct = xs_int_int_dict(*data)
            for i in i32range(0, len(data), 2):
                self.assertEqual(data[i + 1], xs_int_int_dict_get(xs_dct, data[i]))
            self.assertEqual(len(data) // 2, xs_int_int_dict_size(xs_dct))

    def test_xs_int_int_dict_remove(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for i in i32range(-100, 101):
            xs_int_int_dict_put(xs_dct, i, i * -1)
            dct[i] = i * -1
        for _ in i32range(0, 100):
            k = random.randint(-110, 111)
            xs_prev = xs_int_int_dict_remove(xs_dct, int32(k))
            if xs_int_int_dict_last_error() == c_int_int_dict_no_key_error:
                xs_prev = None
            if k in dct:
                prev = dct.pop(k)
            else:
                prev = None
            self.assertEqual(prev, xs_prev)
            self._assert_dicts_equal(xs_dct, dct)

    def test_xs_int_int_dict_contains(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for i in i32range(-100, 101):
            xs_int_int_dict_put(xs_dct, i, i * -1)
            dct[i] = i * -1
        for i in i32range(-120, 121):
            self.assertEqual(i in dct, xs_int_int_dict_contains(xs_dct, i))

    def test_xs_int_int_dict_clear(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for _ in i32range(100):
            k = random.randint(-100, 100)
            v = k * -1
            xs_int_int_dict_put(xs_dct, int32(k), int32(v))
            dct[k] = v

        xs_int_int_dict_clear(xs_dct)
        self._assert_dicts_equal(xs_dct, {})

        dct = {}
        for _ in i32range(100):
            k = random.randint(-100, 100)
            v = k * -1
            xs_int_int_dict_put(xs_dct, int32(k), int32(v))
            dct[k] = v
        self._assert_dicts_equal(xs_dct, dct)

    def test_xs_int_int_dict_copy(self):
        xs_dct = xs_int_int_dict_create()
        for _ in i32range(100):
            k = random.randint(-100, 100)
            v = k * -1
            xs_int_int_dict_put(xs_dct, int32(k), int32(v))

        xs_dct_copy = xs_int_int_dict_copy(xs_dct)
        self.assertEqual(xs_int_int_dict_to_string(xs_dct), xs_int_int_dict_to_string(xs_dct_copy))
        self.assertEqual(xs_int_int_dict_size(xs_dct), xs_int_int_dict_size(xs_dct_copy))

        xs_int_int_dict_put(xs_dct, int32(1001), int32(-1001))
        self.assertGreater(xs_int_int_dict_size(xs_dct), xs_int_int_dict_size(xs_dct_copy))

    def test_xs_int_int_next_key(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for _ in i32range(100):
            v = random.randint(-100, 100)
            dct[v] = v * -1
            xs_int_int_dict_put(xs_dct, int32(v), int32(v * -1))

        self.assertEqual(dct, self._iter_dict(xs_dct))

    def test_xs_int_int_dict_update(self):
        xs_dct1 = xs_int_int_dict_create()
        xs_dct2 = xs_int_int_dict_create()
        dct = {}
        for _ in i32range(100):
            v = random.randint(-100, 100)
            dct[v] = v * -1
            xs_int_int_dict_put(xs_dct1, int32(v), int32(v * -1))
        for _ in i32range(100):
            v = random.randint(-100, 100)
            dct[v] = v * -1
            xs_int_int_dict_put(xs_dct2, int32(v), int32(v * -1))

        self.assertEqual(c_int_int_dict_success, xs_int_int_dict_update(xs_dct1, xs_dct2))
        self._assert_dicts_equal(xs_dct1, dct)

    def test_empty_dict_size(self):
        xs_dct = xs_int_int_dict_create()
        self.assertEqual(0, xs_int_int_dict_size(xs_dct))

    def test_empty_dict_get_returns_default(self):
        xs_dct = xs_int_int_dict_create()
        k = random.randint(-100, 100)
        dft = random.randint(1, 100)
        self.assertEqual(-1, xs_int_int_dict_get(xs_dct, int32(k)))
        self.assertEqual(c_int_int_dict_no_key_error, xs_int_int_dict_last_error())
        self.assertEqual(dft, xs_int_int_dict_get(xs_dct, int32(k), int32(dft)))
        self.assertEqual(c_int_int_dict_no_key_error, xs_int_int_dict_last_error())

    def test_empty_dict_contains(self):
        xs_dct = xs_int_int_dict_create()
        for _ in range(5):
            self.assertFalse(xs_int_int_dict_contains(xs_dct, int32(random.randint(-100, 100))))

    def test_empty_dict_remove(self):
        xs_dct = xs_int_int_dict_create()
        xs_int_int_dict_remove(xs_dct, int32(random.randint(-100, 100)))
        self.assertEqual(c_int_int_dict_no_key_error, xs_int_int_dict_last_error())
        self.assertEqual(0, xs_int_int_dict_size(xs_dct))

    def test_empty_dict_iterate(self):
        xs_dct = xs_int_int_dict_create()
        self.assertFalse(xs_int_int_dict_has_next(xs_dct, True, int32(-1)))
        self.assertEqual({}, self._iter_dict(xs_dct))

    def test_empty_dict_to_string(self):
        xs_dct = xs_int_int_dict_create()
        self.assertEqual("{}", xs_int_int_dict_to_string(xs_dct))

    def test_empty_dict_clear(self):
        xs_dct = xs_int_int_dict_create()
        self.assertEqual(c_int_int_dict_success, xs_int_int_dict_clear(xs_dct))
        self.assertEqual(0, xs_int_int_dict_size(xs_dct))

    def test_empty_dict_copy(self):
        xs_dct = xs_int_int_dict_create()
        xs_dct_copy = xs_int_int_dict_copy(xs_dct)
        self.assertTrue(xs_dct_copy >= 0)
        self.assertEqual(0, xs_int_int_dict_size(xs_dct_copy))
        self.assertEqual("{}", xs_int_int_dict_to_string(xs_dct_copy))

    def test_single_element(self):
        xs_dct = xs_int_int_dict_create()
        k = random.randint(-100, 100)
        v = random.randint(-100, 100)
        xs_int_int_dict_put(xs_dct, int32(k), int32(v))
        self.assertEqual(1, xs_int_int_dict_size(xs_dct))
        self.assertEqual(v, xs_int_int_dict_get(xs_dct, int32(k)))
        self.assertTrue(xs_int_int_dict_contains(xs_dct, int32(k)))
        self.assertEqual({k: v}, self._iter_dict(xs_dct))

    def test_single_element_remove(self):
        xs_dct = xs_int_int_dict_create()
        k = random.randint(-100, 100)
        v = random.randint(-100, 100)
        xs_int_int_dict_put(xs_dct, int32(k), int32(v))
        prev = xs_int_int_dict_remove(xs_dct, int32(k))
        self.assertEqual(c_int_int_dict_success, xs_int_int_dict_last_error())
        self.assertEqual(v, prev)
        self.assertEqual(0, xs_int_int_dict_size(xs_dct))
        self.assertFalse(xs_int_int_dict_contains(xs_dct, int32(k)))

    def test_key_zero(self):
        xs_dct = xs_int_int_dict_create()
        xs_int_int_dict_put(xs_dct, int32(0), int32(42))
        self.assertEqual(1, xs_int_int_dict_size(xs_dct))
        self.assertEqual(42, xs_int_int_dict_get(xs_dct, int32(0)))
        self.assertTrue(xs_int_int_dict_contains(xs_dct, int32(0)))

    def test_value_zero(self):
        xs_dct = xs_int_int_dict_create()
        xs_int_int_dict_put(xs_dct, int32(7), int32(0))
        self.assertEqual(0, xs_int_int_dict_get(xs_dct, int32(7)))
        self.assertEqual(c_int_int_dict_success, xs_int_int_dict_last_error())

    def test_negative_keys(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for k in range(-50, 0):
            v = k * 3
            xs_int_int_dict_put(xs_dct, int32(k), int32(v))
            dct[k] = v
        self._assert_dicts_equal(xs_dct, dct)

    def test_overwrite_same_key_repeatedly(self):
        xs_dct = xs_int_int_dict_create()
        k = random.randint(-100, 100)
        for v in range(100):
            prev = xs_int_int_dict_put(xs_dct, int32(k), int32(v))
            if v > 0:
                self.assertEqual(c_int_int_dict_success, xs_int_int_dict_last_error())
                self.assertEqual(v - 1, prev)
        self.assertEqual(1, xs_int_int_dict_size(xs_dct))
        self.assertEqual(99, xs_int_int_dict_get(xs_dct, int32(k)))

    def test_get_custom_default(self):
        xs_dct = xs_int_int_dict_create()
        k = random.randint(-100, 100)
        v = random.randint(-100, 100)
        dft = random.randint(101, 200)
        xs_int_int_dict_put(xs_dct, int32(k), int32(v))
        self.assertEqual(v, xs_int_int_dict_get(xs_dct, int32(k), int32(dft)))
        self.assertEqual(dft, xs_int_int_dict_get(xs_dct, int32(k + 1000), int32(dft)))

    def test_remove_all_elements_one_by_one(self):
        xs_dct = xs_int_int_dict_create()
        keys = list(range(50))
        for k in keys:
            xs_int_int_dict_put(xs_dct, int32(k), int32(k * 10))
        random.shuffle(keys)
        for i, k in enumerate(keys):
            prev = xs_int_int_dict_remove(xs_dct, int32(k))
            self.assertEqual(c_int_int_dict_success, xs_int_int_dict_last_error())
            self.assertEqual(k * 10, prev)
            self.assertEqual(len(keys) - i - 1, xs_int_int_dict_size(xs_dct))
            self.assertFalse(xs_int_int_dict_contains(xs_dct, int32(k)))
        self.assertEqual(0, xs_int_int_dict_size(xs_dct))

    def test_remove_nonexistent_key(self):
        xs_dct = xs_int_int_dict_create()
        k = random.randint(-100, 100)
        v = random.randint(-100, 100)
        xs_int_int_dict_put(xs_dct, int32(k), int32(v))
        xs_int_int_dict_remove(xs_dct, int32(k + 1000))
        self.assertEqual(c_int_int_dict_no_key_error, xs_int_int_dict_last_error())
        self.assertEqual(1, xs_int_int_dict_size(xs_dct))
        self.assertEqual(v, xs_int_int_dict_get(xs_dct, int32(k)))

    def test_contains_after_remove(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for _ in range(20):
            k = random.randint(-100, 100)
            dct[k] = k
            xs_int_int_dict_put(xs_dct, int32(k), int32(k))
        removed_key = random.choice(list(dct.keys()))
        del dct[removed_key]
        xs_int_int_dict_remove(xs_dct, int32(removed_key))
        for k in dct:
            self.assertTrue(xs_int_int_dict_contains(xs_dct, int32(k)))
        self.assertFalse(xs_int_int_dict_contains(xs_dct, int32(removed_key)))

    def test_put_after_remove_same_key(self):
        xs_dct = xs_int_int_dict_create()
        k = random.randint(-100, 100)
        v1 = random.randint(-100, 100)
        v2 = random.randint(-100, 100)
        xs_int_int_dict_put(xs_dct, int32(k), int32(v1))
        xs_int_int_dict_remove(xs_dct, int32(k))
        self.assertFalse(xs_int_int_dict_contains(xs_dct, int32(k)))
        xs_int_int_dict_put(xs_dct, int32(k), int32(v2))
        self.assertEqual(v2, xs_int_int_dict_get(xs_dct, int32(k)))
        self.assertEqual(1, xs_int_int_dict_size(xs_dct))

    def test_many_inserts_triggers_rehash(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for _ in range(200):
            k = random.randint(-500, 500)
            v = random.randint(-500, 500)
            xs_int_int_dict_put(xs_dct, int32(k), int32(v))
            dct[k] = v
        self._assert_dicts_equal(xs_dct, dct)

    def test_rehash_preserves_all_entries(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for _ in range(200):
            k = random.randint(-500, 500)
            v = random.randint(-500, 500)
            xs_int_int_dict_put(xs_dct, int32(k), int32(v))
            dct[k] = v
        self._assert_dicts_equal(xs_dct, dct)
        self.assertEqual(dct, self._iter_dict(xs_dct))

    def test_copy_deep_independence(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for _ in range(20):
            k = random.randint(-100, 100)
            v = random.randint(-100, 100)
            xs_int_int_dict_put(xs_dct, int32(k), int32(v))
            dct[k] = v
        xs_dct_copy = xs_int_int_dict_copy(xs_dct)

        new_k1 = random.randint(500, 600)
        xs_int_int_dict_put(xs_dct, int32(new_k1), int32(1))
        self.assertFalse(xs_int_int_dict_contains(xs_dct_copy, int32(new_k1)))

        new_k2 = random.randint(700, 800)
        xs_int_int_dict_put(xs_dct_copy, int32(new_k2), int32(2))
        self.assertFalse(xs_int_int_dict_contains(xs_dct, int32(new_k2)))

        existing_k = random.choice(list(dct.keys()))
        new_v = random.randint(900, 999)
        xs_int_int_dict_put(xs_dct, int32(existing_k), int32(new_v))
        self.assertEqual(dct[existing_k], xs_int_int_dict_get(xs_dct_copy, int32(existing_k)))

    def test_copy_preserves_all_entries(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for _ in range(100):
            k = random.randint(-100, 100)
            v = random.randint(-100, 100)
            xs_int_int_dict_put(xs_dct, int32(k), int32(v))
            dct[k] = v
        xs_dct_copy = xs_int_int_dict_copy(xs_dct)
        self._assert_dicts_equal(xs_dct_copy, dct)

    def test_clear_then_reuse_heavily(self):
        xs_dct = xs_int_int_dict_create()
        for _ in range(3):
            dct = {}
            for _ in range(80):
                k = random.randint(-100, 100)
                v = random.randint(-100, 100)
                xs_int_int_dict_put(xs_dct, int32(k), int32(v))
                dct[k] = v
            self._assert_dicts_equal(xs_dct, dct)
            xs_int_int_dict_clear(xs_dct)
            self.assertEqual(0, xs_int_int_dict_size(xs_dct))

    def test_clear_all_contains_false(self):
        xs_dct = xs_int_int_dict_create()
        keys = set()
        for _ in range(50):
            k = random.randint(-100, 100)
            keys.add(k)
            xs_int_int_dict_put(xs_dct, int32(k), int32(random.randint(-100, 100)))
        xs_int_int_dict_clear(xs_dct)
        for k in keys:
            self.assertFalse(xs_int_int_dict_contains(xs_dct, int32(k)))

    def test_update_empty_into_nonempty(self):
        xs_dct1 = xs_int_int_dict_create()
        dct = {}
        for _ in range(20):
            k = random.randint(-100, 100)
            v = random.randint(-100, 100)
            xs_int_int_dict_put(xs_dct1, int32(k), int32(v))
            dct[k] = v
        xs_dct2 = xs_int_int_dict_create()
        self.assertEqual(c_int_int_dict_success, xs_int_int_dict_update(xs_dct1, xs_dct2))
        self._assert_dicts_equal(xs_dct1, dct)

    def test_update_nonempty_into_empty(self):
        xs_dct1 = xs_int_int_dict_create()
        xs_dct2 = xs_int_int_dict_create()
        dct = {}
        for _ in range(20):
            k = random.randint(-100, 100)
            v = random.randint(-100, 100)
            xs_int_int_dict_put(xs_dct2, int32(k), int32(v))
            dct[k] = v
        self.assertEqual(c_int_int_dict_success, xs_int_int_dict_update(xs_dct1, xs_dct2))
        self._assert_dicts_equal(xs_dct1, dct)

    def test_update_overlapping_keys(self):
        xs_dct1 = xs_int_int_dict_create()
        xs_dct2 = xs_int_int_dict_create()
        for k in range(10):
            xs_int_int_dict_put(xs_dct1, int32(k), int32(100))
        for k in range(5, 15):
            xs_int_int_dict_put(xs_dct2, int32(k), int32(200))
        self.assertEqual(c_int_int_dict_success, xs_int_int_dict_update(xs_dct1, xs_dct2))
        expected = {k: 100 for k in range(5)}
        expected.update({k: 200 for k in range(5, 15)})
        self._assert_dicts_equal(xs_dct1, expected)

    def test_iterate_single_element(self):
        xs_dct = xs_int_int_dict_create()
        k = random.randint(-100, 100)
        v = random.randint(-100, 100)
        xs_int_int_dict_put(xs_dct, int32(k), int32(v))
        self.assertEqual({k: v}, self._iter_dict(xs_dct))

    def test_iterate_after_removals(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for _ in range(50):
            k = random.randint(-100, 100)
            v = random.randint(-100, 100)
            xs_int_int_dict_put(xs_dct, int32(k), int32(v))
            dct[k] = v
        keys_to_remove = random.sample(list(dct.keys()), len(dct) // 3)
        for k in keys_to_remove:
            xs_int_int_dict_remove(xs_dct, int32(k))
            del dct[k]
        self.assertEqual(dct, self._iter_dict(xs_dct))

    def test_large_values(self):
        xs_dct = xs_int_int_dict_create()
        large_pos = int32(2147483647)
        large_neg = int32(-2147483648)
        xs_int_int_dict_put(xs_dct, int32(1), large_pos)
        xs_int_int_dict_put(xs_dct, int32(2), large_neg)
        xs_int_int_dict_put(xs_dct, large_pos, int32(1))
        xs_int_int_dict_put(xs_dct, large_neg, int32(2))
        self.assertEqual(large_pos, xs_int_int_dict_get(xs_dct, int32(1)))
        self.assertEqual(large_neg, xs_int_int_dict_get(xs_dct, int32(2)))
        self.assertEqual(1, xs_int_int_dict_get(xs_dct, large_pos))
        self.assertEqual(2, xs_int_int_dict_get(xs_dct, large_neg))

    def test_to_string_single(self):
        xs_dct = xs_int_int_dict_create()
        k = random.randint(-100, 100)
        v = random.randint(-100, 100)
        xs_int_int_dict_put(xs_dct, int32(k), int32(v))
        s = xs_int_int_dict_to_string(xs_dct)
        self.assertEqual(f"{{{k}: {v}}}", s)

    def test_to_string_multiple(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for _ in range(10):
            k = random.randint(-100, 100)
            v = random.randint(-100, 100)
            xs_int_int_dict_put(xs_dct, int32(k), int32(v))
            dct[k] = v
        s = xs_int_int_dict_to_string(xs_dct)
        for k, v in dct.items():
            self.assertIn(f"{k}: {v}", s)

    def test_last_error_after_successful_get(self):
        xs_dct = xs_int_int_dict_create()
        k = random.randint(-100, 100)
        xs_int_int_dict_put(xs_dct, int32(k), int32(random.randint(-100, 100)))
        xs_int_int_dict_get(xs_dct, int32(k))
        self.assertEqual(c_int_int_dict_success, xs_int_int_dict_last_error())

    def test_last_error_after_failed_get(self):
        xs_dct = xs_int_int_dict_create()
        xs_int_int_dict_get(xs_dct, int32(random.randint(-100, 100)))
        self.assertEqual(c_int_int_dict_no_key_error, xs_int_int_dict_last_error())

    def test_last_error_after_new_put(self):
        xs_dct = xs_int_int_dict_create()
        xs_int_int_dict_put(xs_dct, int32(random.randint(-100, 100)), int32(random.randint(-100, 100)))
        self.assertEqual(c_int_int_dict_no_key_error, xs_int_int_dict_last_error())

    def test_last_error_after_overwrite_put(self):
        xs_dct = xs_int_int_dict_create()
        k = random.randint(-100, 100)
        xs_int_int_dict_put(xs_dct, int32(k), int32(random.randint(-100, 100)))
        xs_int_int_dict_put(xs_dct, int32(k), int32(random.randint(-100, 100)))
        self.assertEqual(c_int_int_dict_success, xs_int_int_dict_last_error())

    def test_stress_put_remove_cycle(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for _ in range(500):
            op = random.randint(0, 2)
            k = random.randint(-50, 50)
            if op <= 1:
                v = random.randint(-1000, 1000)
                xs_int_int_dict_put(xs_dct, int32(k), int32(v))
                dct[k] = v
            else:
                xs_int_int_dict_remove(xs_dct, int32(k))
                dct.pop(k, None)
        self._assert_dicts_equal(xs_dct, dct)
        self.assertEqual(dct, self._iter_dict(xs_dct))

    def _arr_to_list(self, arr: int32) -> list[int]:
        return [int(xs_array_get_int(arr, int32(i))) for i in range(xs_array_get_size(arr))]

    def test_keys_empty_dict(self):
        xs_dct = xs_int_int_dict_create()
        arr = xs_int_int_dict_keys(xs_dct)
        self.assertTrue(arr >= 0)
        self.assertEqual(0, xs_array_get_size(arr))

    def test_values_empty_dict(self):
        xs_dct = xs_int_int_dict_create()
        arr = xs_int_int_dict_values(xs_dct)
        self.assertTrue(arr >= 0)
        self.assertEqual(0, xs_array_get_size(arr))

    def test_keys_single_element(self):
        xs_dct = xs_int_int_dict_create()
        xs_int_int_dict_put(xs_dct, int32(42), int32(99))
        arr = xs_int_int_dict_keys(xs_dct)
        self.assertEqual([42], self._arr_to_list(arr))

    def test_values_single_element(self):
        xs_dct = xs_int_int_dict_create()
        xs_int_int_dict_put(xs_dct, int32(42), int32(99))
        arr = xs_int_int_dict_values(xs_dct)
        self.assertEqual([99], self._arr_to_list(arr))

    def test_keys_multiple_elements(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for _ in range(50):
            k = random.randint(-100, 100)
            v = random.randint(-100, 100)
            xs_int_int_dict_put(xs_dct, int32(k), int32(v))
            dct[k] = v
        arr = xs_int_int_dict_keys(xs_dct)
        self.assertEqual(len(dct), xs_array_get_size(arr))
        self.assertEqual(set(dct.keys()), set(self._arr_to_list(arr)))

    def test_values_multiple_elements(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for _ in range(50):
            k = random.randint(-100, 100)
            v = random.randint(-100, 100)
            xs_int_int_dict_put(xs_dct, int32(k), int32(v))
            dct[k] = v
        keys_arr = xs_int_int_dict_keys(xs_dct)
        vals_arr = xs_int_int_dict_values(xs_dct)
        self.assertEqual(xs_array_get_size(keys_arr), xs_array_get_size(vals_arr))
        for i in range(xs_array_get_size(keys_arr)):
            k = int(xs_array_get_int(keys_arr, int32(i)))
            v = int(xs_array_get_int(vals_arr, int32(i)))
            self.assertEqual(dct[k], v)

    def test_keys_values_order_matches(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for k in range(-20, 21):
            v = k * 3
            xs_int_int_dict_put(xs_dct, int32(k), int32(v))
            dct[k] = v
        keys_arr = xs_int_int_dict_keys(xs_dct)
        vals_arr = xs_int_int_dict_values(xs_dct)
        keys_list = self._arr_to_list(keys_arr)
        vals_list = self._arr_to_list(vals_arr)
        reconstructed = dict(zip(keys_list, vals_list))
        self.assertEqual(dct, reconstructed)

    def test_keys_after_removals(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for k in range(30):
            xs_int_int_dict_put(xs_dct, int32(k), int32(k * 10))
            dct[k] = k * 10
        for k in random.sample(list(dct.keys()), 10):
            xs_int_int_dict_remove(xs_dct, int32(k))
            del dct[k]
        arr = xs_int_int_dict_keys(xs_dct)
        self.assertEqual(len(dct), xs_array_get_size(arr))
        self.assertEqual(set(dct.keys()), set(self._arr_to_list(arr)))

    def test_keys_after_rehash(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for k in range(200):
            xs_int_int_dict_put(xs_dct, int32(k), int32(k))
            dct[k] = k
        arr = xs_int_int_dict_keys(xs_dct)
        self.assertEqual(len(dct), xs_array_get_size(arr))
        self.assertEqual(set(dct.keys()), set(self._arr_to_list(arr)))

    def test_values_after_overwrite(self):
        xs_dct = xs_int_int_dict_create()
        for k in range(10):
            xs_int_int_dict_put(xs_dct, int32(k), int32(0))
        for k in range(10):
            xs_int_int_dict_put(xs_dct, int32(k), int32(k * 100))
        vals_arr = xs_int_int_dict_values(xs_dct)
        self.assertEqual(10, xs_array_get_size(vals_arr))
        self.assertEqual(set(range(0, 1000, 100)), set(self._arr_to_list(vals_arr)))

    def test_equals_both_empty(self):
        a = xs_int_int_dict_create()
        b = xs_int_int_dict_create()
        self.assertTrue(xs_int_int_dict_equals(a, b))

    def test_equals_same_contents(self):
        a = xs_int_int_dict_create()
        b = xs_int_int_dict_create()
        for k in range(50):
            xs_int_int_dict_put(a, int32(k), int32(k * 10))
            xs_int_int_dict_put(b, int32(k), int32(k * 10))
        self.assertTrue(xs_int_int_dict_equals(a, b))

    def test_equals_different_insertion_order(self):
        a = xs_int_int_dict_create()
        b = xs_int_int_dict_create()
        keys = list(range(40))
        for k in keys:
            xs_int_int_dict_put(a, int32(k), int32(k))
        random.shuffle(keys)
        for k in keys:
            xs_int_int_dict_put(b, int32(k), int32(k))
        self.assertTrue(xs_int_int_dict_equals(a, b))

    def test_equals_different_sizes(self):
        a = xs_int_int_dict_create()
        b = xs_int_int_dict_create()
        xs_int_int_dict_put(a, int32(1), int32(1))
        xs_int_int_dict_put(b, int32(1), int32(1))
        xs_int_int_dict_put(b, int32(2), int32(2))
        self.assertFalse(xs_int_int_dict_equals(a, b))
        self.assertFalse(xs_int_int_dict_equals(b, a))

    def test_equals_same_keys_different_values(self):
        a = xs_int_int_dict_create()
        b = xs_int_int_dict_create()
        for k in range(20):
            xs_int_int_dict_put(a, int32(k), int32(k))
            xs_int_int_dict_put(b, int32(k), int32(k + 1))
        self.assertFalse(xs_int_int_dict_equals(a, b))

    def test_equals_one_empty(self):
        a = xs_int_int_dict_create()
        b = xs_int_int_dict_create()
        xs_int_int_dict_put(a, int32(1), int32(1))
        self.assertFalse(xs_int_int_dict_equals(a, b))
        self.assertFalse(xs_int_int_dict_equals(b, a))

    def test_equals_after_copy(self):
        a = xs_int_int_dict_create()
        for _ in range(100):
            k = random.randint(-100, 100)
            v = random.randint(-100, 100)
            xs_int_int_dict_put(a, int32(k), int32(v))
        b = xs_int_int_dict_copy(a)
        self.assertTrue(xs_int_int_dict_equals(a, b))

    def test_equals_after_remove_diverges(self):
        a = xs_int_int_dict_create()
        b = xs_int_int_dict_create()
        for k in range(10):
            xs_int_int_dict_put(a, int32(k), int32(k))
            xs_int_int_dict_put(b, int32(k), int32(k))
        xs_int_int_dict_remove(a, int32(5))
        self.assertFalse(xs_int_int_dict_equals(a, b))

    def test_put_if_absent_inserts_new_key(self):
        xs_dct = xs_int_int_dict_create()
        result = xs_int_int_dict_put_if_absent(xs_dct, int32(10), int32(42))
        self.assertEqual(c_int_int_dict_no_key_error, xs_int_int_dict_last_error())
        self.assertEqual(1, xs_int_int_dict_size(xs_dct))
        self.assertEqual(42, xs_int_int_dict_get(xs_dct, int32(10)))

    def test_put_if_absent_does_not_overwrite(self):
        xs_dct = xs_int_int_dict_create()
        xs_int_int_dict_put(xs_dct, int32(10), int32(42))
        result = xs_int_int_dict_put_if_absent(xs_dct, int32(10), int32(99))
        self.assertEqual(c_int_int_dict_success, xs_int_int_dict_last_error())
        self.assertEqual(42, result)
        self.assertEqual(42, xs_int_int_dict_get(xs_dct, int32(10)))
        self.assertEqual(1, xs_int_int_dict_size(xs_dct))

    def test_put_if_absent_multiple_keys(self):
        xs_dct = xs_int_int_dict_create()
        for k in range(20):
            xs_int_int_dict_put_if_absent(xs_dct, int32(k), int32(k * 10))
        for k in range(20):
            result = xs_int_int_dict_put_if_absent(xs_dct, int32(k), int32(999))
            self.assertEqual(c_int_int_dict_success, xs_int_int_dict_last_error())
            self.assertEqual(k * 10, result)
        self.assertEqual(20, xs_int_int_dict_size(xs_dct))

    def test_put_if_absent_on_empty_dict(self):
        xs_dct = xs_int_int_dict_create()
        xs_int_int_dict_put_if_absent(xs_dct, int32(0), int32(0))
        self.assertEqual(c_int_int_dict_no_key_error, xs_int_int_dict_last_error())
        self.assertEqual(1, xs_int_int_dict_size(xs_dct))
        self.assertEqual(0, xs_int_int_dict_get(xs_dct, int32(0)))

    def test_put_if_absent_stress(self):
        xs_dct = xs_int_int_dict_create()
        dct = {}
        for _ in range(200):
            k = random.randint(-50, 50)
            v = random.randint(-100, 100)
            if k not in dct:
                dct[k] = v
            xs_int_int_dict_put_if_absent(xs_dct, int32(k), int32(v))
        self._assert_dicts_equal(xs_dct, dct)
