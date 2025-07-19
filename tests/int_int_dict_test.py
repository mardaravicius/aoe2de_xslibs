import random
import unittest

from xs.int_int_dict import *


class IntIntDictTest(unittest.TestCase):

    def test_xs_int_int_dict_put(self):
        arr = xs_int_int_dict_create()
        dct = {}
        for i in range(0, 40):
            if i >= 20:
                v = i - 20
            else:
                v = i * -1
            arr_prev = xs_int_int_dict_put(arr, i, v)
            if xs_int_int_dict_last_error() == c_int_int_dict_no_key:
                arr_prev = None
            d_prev = dct.get(i)
            dct[i] = v
            self.assertEqual(d_prev, arr_prev)
            self.assertEqual(dct[i], xs_int_int_dict_get(arr, i))
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
            if xs_int_int_dict_last_error() == c_int_int_dict_no_key:
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
