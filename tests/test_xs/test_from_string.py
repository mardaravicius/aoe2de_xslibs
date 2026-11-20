import importlib
import unittest

import numpy as np
from numpy import int32, float32

from xs_converter.functions import vector

np.seterr(over="ignore")


def _module(name: str):
    return importlib.import_module(f"xs.{name}")


def _list_values(name: str, lst: int32) -> list:
    m = _module(name)
    size = getattr(m, f"xs_{name}_size")(lst)
    return [getattr(m, f"xs_{name}_get")(lst, int32(i)) for i in range(size)]


V1 = vector(1.0, 1.1, -3.3)
V2 = vector(1.0, 2.0, 3.0)

SAMPLES = {
    "int": ("1, -2 ,30", [int32(1), int32(-2), int32(30)]),
    "float": ("1.0,1.1, -2.5", [float32(1.0), float32(1.1), float32(-2.5)]),
    "string": ("'a', ' b, c:(' ,''", ["a", " b, c:(", ""]),
    "vector": ("v(1.0,1.1,-3.3), v( 1.0 , 2.0 , 3.0 )", [V1, V2]),
}


class TestListFromString(unittest.TestCase):
    def _from(self, name: str, items: str) -> list:
        lst = getattr(_module(name), f"xs_{name}_from_string")(items)
        self.assertGreaterEqual(lst, 0)
        return _list_values(name, lst)

    def test_parses_values(self):
        for t, (items, expected) in SAMPLES.items():
            with self.subTest(t=t):
                self.assertEqual(self._from(f"{t}_list", items), expected)
        self.assertEqual(self._from("bool_list", "true, false,true"), [True, False, True])

    def test_empty_string_creates_empty_list(self):
        for t in ("int", "float", "bool", "string", "vector"):
            with self.subTest(t=t):
                self.assertEqual(self._from(f"{t}_list", ""), [])
                self.assertEqual(self._from(f"{t}_list", "   "), [])

    def test_skips_invalid_items(self):
        self.assertEqual(self._from("int_list", "1,x,,2"), [int32(1), int32(2)])
        self.assertEqual(self._from("float_list", "1.0,x,,2.5,1"), [float32(1.0), float32(2.5)])
        self.assertEqual(self._from("bool_list", "true,yes,1,false"), [True, False])
        self.assertEqual(
            self._from("vector_list", "v(1.0,2.0,3.0),v(1.0,2.0),(1.0,2.0,3.0),v(1.0,a,3.0),v(),,v(1,2,3),v(1.0,2.0,3.0"),
            [V2],
        )

    def test_int_list_keeps_leading_digits(self):
        self.assertEqual(self._from("int_list", "1.5,1x,+3"), [int32(1), int32(1), int32(3)])

    def test_string_list_requires_quotes(self):
        self.assertEqual(self._from("string_list", "'a',b,'',,'e''f','d'"), ["a", "", "d"])

    def test_string_list_ignores_brackets(self):
        self.assertEqual(self._from("string_list", "'a',(,'b'"), ["a", "b"])

    def test_unclosed_quote_consumes_rest_of_input(self):
        self.assertEqual(self._from("string_list", "'a','b,'c'"), ["a"])

    def test_unbalanced_brackets_do_not_swallow_following_items(self):
        self.assertEqual(self._from("vector_list", "v(1.0,2.0,3.0)),v(1.0,1.1,-3.3)"), [V1])
        self.assertEqual(self._from("vector_list", "v(1.0,2.0,3.0,v(1.0,1.1,-3.3),v(1.0,2.0,3.0)"), [V2])

    def test_sentinel_values_are_invalid(self):
        self.assertEqual(self._from("int_list", "-999999999,1"), [int32(1)])
        self.assertEqual(self._from("float_list", "-9999999.0,1.0"), [float32(1.0)])
        self.assertEqual(self._from("vector_list", "v(-9999999.0,-9999999.0,-9999999.0),v(1.0,2.0,3.0)"), [V2])

    def test_list_is_growable(self):
        lst = _module("int_list").xs_int_list_from_string("1,2")
        _module("int_list").xs_int_list_append(lst, int32(3))
        self.assertEqual(_list_values("int_list", lst), [int32(1), int32(2), int32(3)])


DICT_SAMPLES = {
    "int": ("1", int32(1), "-2", int32(-2)),
    "float": ("1.5", float32(1.5), "-2.0", float32(-2.0)),
    "string": ("'a'", "a", "' b,c:('", " b,c:("),
    "vector": ("v(1.0,1.1,-3.3)", V1, "v(1.0,2.0,3.0)", V2),
}

DICT_DEFAULTS = {"int": int32(-12345), "string": "<none>", "vector": vector(-5.0, -5.0, -5.0)}


class TestDictFromString(unittest.TestCase):
    def _check(self, k: str, v: str):
        name = f"{k}_{v}_dict"
        m = _module(name)
        k1s, k1, k2s, k2 = DICT_SAMPLES[k]
        v1s, v1, v2s, v2 = DICT_SAMPLES[v]
        dct = getattr(m, f"xs_{name}_from_string")(f" {k1s} : {v1s} ,{k2s}:{v2s}")
        self.assertGreaterEqual(dct, 0)
        size = getattr(m, f"xs_{name}_size")
        get = getattr(m, f"xs_{name}_get")
        self.assertEqual(size(dct), 2)
        self.assertEqual(get(dct, k1, DICT_DEFAULTS[v]), v1)
        self.assertEqual(get(dct, k2, DICT_DEFAULTS[v]), v2)

        empty = getattr(m, f"xs_{name}_from_string")("")
        self.assertGreaterEqual(empty, 0)
        self.assertEqual(size(empty), 0)

    def test_all_dicts(self):
        for k in ("int", "float", "string", "vector"):
            for v in ("int", "string", "vector"):
                with self.subTest(k=k, v=v):
                    self._check(k, v)

    def test_skips_invalid_pairs(self):
        m = _module("int_string_dict")
        dct = m.xs_int_string_dict_from_string("1:'a',2,x:'b',3:'',4:'d:e',5:f,6:'g")
        self.assertEqual(m.xs_int_string_dict_size(dct), 3)
        self.assertEqual(m.xs_int_string_dict_get(dct, int32(1), "?"), "a")
        self.assertEqual(m.xs_int_string_dict_get(dct, int32(3), "?"), "")
        self.assertEqual(m.xs_int_string_dict_get(dct, int32(4), "?"), "d:e")

        m = _module("string_string_dict")
        dct = m.xs_string_string_dict_from_string("'abc':'',':':'a,b',x:'y','k':v,'':'empty'")
        self.assertEqual(m.xs_string_string_dict_size(dct), 3)
        self.assertEqual(m.xs_string_string_dict_get(dct, "abc", "?"), "")
        self.assertEqual(m.xs_string_string_dict_get(dct, ":", "?"), "a,b")
        self.assertEqual(m.xs_string_string_dict_get(dct, "", "?"), "empty")

        m = _module("float_int_dict")
        dct = m.xs_float_int_dict_from_string("1.5:1,x:2,2.5:y,3.5:3")
        self.assertEqual(m.xs_float_int_dict_size(dct), 2)
        self.assertEqual(m.xs_float_int_dict_get(dct, float32(3.5), int32(-1)), int32(3))

        m = _module("vector_string_dict")
        dct = m.xs_vector_string_dict_from_string("v(1.0,2.0,3.0):'smile :)',v(4.0,5.0,6.0):'b'")
        self.assertEqual(m.xs_vector_string_dict_size(dct), 2)
        self.assertEqual(m.xs_vector_string_dict_get(dct, V2, "?"), "smile :)")

        m = _module("vector_int_dict")
        dct = m.xs_vector_int_dict_from_string("v(1.0,2.0,3.0):1,v(1.0,2.0):2,v(4.0,5.0,6.0):x,v(7.0,8.0,9.0):3")
        self.assertEqual(m.xs_vector_int_dict_size(dct), 2)
        self.assertEqual(m.xs_vector_int_dict_get(dct, vector(7.0, 8.0, 9.0), int32(-1)), int32(3))

    def test_later_duplicate_key_wins(self):
        m = _module("string_int_dict")
        dct = m.xs_string_int_dict_from_string("'a':1,'a':2")
        self.assertEqual(m.xs_string_int_dict_size(dct), 1)
        self.assertEqual(m.xs_string_int_dict_get(dct, "a", int32(-1)), int32(2))


if __name__ == "__main__":
    unittest.main()
