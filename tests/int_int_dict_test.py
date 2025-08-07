import random
import unittest

from xs.int_int_dict2 import *

class IntIntDictTest(unittest.TestCase):

    def test_xs_int_int_dict_put(self):
        arr = xs_int_int_dict_create()
        dct = {}
        for _ in range(100):
            k = random.randint(-100, 100)
            v = k * -1
            arr_prev = xs_int_int_dict_put(arr, k, v)
            if xs_int_int_dict_last_error() == c_int_int_dict_no_key_error:
                arr_prev = None
            d_prev = dct.get(k)
            dct[k] = v
            self.assertEqual(d_prev, arr_prev)
            self.assertEqual(dct[k], xs_int_int_dict_get(arr, k))
            self.assertEqual(len(dct), xs_int_int_dict_size(arr))

    def test_xs_int_int_dict(self):
        test_data = [
            tuple(range(0, 0)),
            tuple(range(0, 2)),
            tuple(range(0, 4)),
            tuple(range(0, 6)),
            tuple(range(0, 8)),
            tuple(range(0, 10)),
            tuple(range(0, 12)),
        ]

        for data in test_data:
            arr = xs_int_int_dict(*data)
            for i in range(0, len(data), 2):
                self.assertEqual(data[i + 1], xs_int_int_dict_get(arr, data[i]))
            self.assertEqual(len(data) // 2, xs_int_int_dict_size(arr))

    def test_xs_int_int_dict_remove(self):
        arr = xs_int_int_dict_create()
        dct = {}
        for i in range(-100, 101):
            xs_int_int_dict_put(arr, i, i * -1)
            dct[i] = i * -1
        for i in range(0, 100):
            k = random.randint(-110, 111)
            arr_prev = xs_int_int_dict_remove(arr, k)
            if xs_int_int_dict_last_error() == c_int_int_dict_no_key_error:
                arr_prev = None
            if k in dct:
                d_prev = dct.pop(k)
            else:
                d_prev = None
            self.assertEqual(d_prev, arr_prev)
            for k in dct.keys():
                self.assertEqual(dct[k], xs_int_int_dict_get(arr, k))
                self.assertEqual(len(dct), xs_int_int_dict_size(arr))

    def test_xs_int_int_dict_contains(self):
        arr = xs_int_int_dict_create()
        dct = {}
        for i in range(-100, 101):
            xs_int_int_dict_put(arr, i, i * -1)
            dct[i] = i * -1
        for i in range(-120, 121):
            self.assertEqual(i in dct, xs_int_int_dict_contains(arr, i))

    def test_xs_int_int_dict_clear(self):
        arr = xs_int_int_dict_create()
        dct = {}
        for _ in range(100):
            k = random.randint(-100, 100)
            v = k * -1
            xs_int_int_dict_put(arr, k, v)
            dct[k] = v

        xs_int_int_dict_clear(arr)
        dct.clear()
        self.assertEqual(len(dct), xs_int_int_dict_size(arr))

        for _ in range(100):
            k = random.randint(-100, 100)
            v = k * -1
            xs_int_int_dict_put(arr, k, v)
            dct[k] = v
            self.assertEqual(dct[k], xs_int_int_dict_get(arr, k))
            self.assertEqual(len(dct), xs_int_int_dict_size(arr))

    def test_xs_int_int_dict_copy(self):
        arr = xs_int_int_dict_create()
        for _ in range(100):
            k = random.randint(-100, 100)
            v = k * -1
            xs_int_int_dict_put(arr, k, v)

        arr_copy = xs_int_int_dict_copy(arr)
        self.assertEqual(xs_int_int_dict_to_string(arr), xs_int_int_dict_to_string(arr_copy))
        self.assertEqual(xs_int_int_dict_size(arr), xs_int_int_dict_size(arr_copy))

        xs_int_int_dict_put(arr, 1001, -1001)
        self.assertGreater(xs_int_int_dict_size(arr), xs_int_int_dict_size(arr_copy))


    def test_xs_int_int_next_key(self):
        arr = xs_int_int_dict_create()
        dct = {}
        for i in range(100):
            v = random.randint(-100, 100)
            dct[v] = v * -1
            xs_int_int_dict_put(arr, v, v * -1)

        res = {}
        first = True
        key = -1
        while xs_int_int_dict_has_next(arr, first, key):
            key = xs_int_int_dict_next_key(arr, first, key)
            first = False
            val = xs_int_int_dict_get(arr, key)
            res[key] = val

        self.assertEqual(dct, res)


    def test_xs_int_int_dict_update(self):
        arr1 = xs_int_int_dict_create()
        arr2 = xs_int_int_dict_create()
        dct = {}
        for i in range(100):
            v = random.randint(-100, 100)
            dct[v] = v * -1
            xs_int_int_dict_put(arr1, v, v * -1)
        for i in range(100):
            v = random.randint(-100, 100)
            dct[v] = v * -1
            xs_int_int_dict_put(arr2, v, v * -1)

        self.assertEqual(c_int_int_dict_success, xs_int_int_dict_update(arr1, arr2))

        self.assertEqual(len(dct), xs_int_int_dict_size(arr1))
        for key in dct.keys():
            self.assertEqual(dct[key], xs_int_int_dict_get(arr1, key))
