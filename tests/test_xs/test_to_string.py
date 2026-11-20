import importlib
import unittest

import numpy as np

from xs_converter.functions import vector

np.seterr(over="ignore")


def _module(name: str):
    return importlib.import_module(f"xs.{name}")


def _to_string(name: str, items: str, *args) -> str:
    m = _module(name)
    handle = getattr(m, f"xs_{name}_from_string")(items)
    return getattr(m, f"xs_{name}_to_string")(handle, *args)


V1 = str(vector(1.0, 2.0, 3.0))
V2 = str(vector(4.0, 5.0, 6.0))

SEQUENCES = {
    "int": ("1,2", "1; 2"),
    "float": ("1.5,2.5", "1.5; 2.5"),
    "bool": ("true,false", "true; false"),
    "vector": ("v(1.0,2.0,3.0),v(4.0,5.0,6.0)", f"{V1}; {V2}"),
}

DICTS = {
    "int_int": ("1:2", "1=2"),
    "float_int": ("1.5:2", "1.5=2"),
    "int_vector": ("1:v(1.0,2.0,3.0)", f"1={V1}"),
    "float_vector": ("1.5:v(1.0,2.0,3.0)", f"1.5={V1}"),
    "vector_int": ("v(1.0,2.0,3.0):2", f"{V1}=2"),
    "vector_vector": ("v(1.0,2.0,3.0):v(4.0,5.0,6.0)", f"{V1}={V2}"),
}

STRING_DICTS = {
    "int_string": ("1:'a'", "1='a'"),
    "float_string": ("1.5:'a'", "1.5='a'"),
    "vector_string": ("v(1.0,2.0,3.0):'a'", f"{V1}='a'"),
    "string_int": ("'a':2", "'a'=2"),
    "string_vector": ("'a':v(1.0,2.0,3.0)", f"'a'={V1}"),
    "string_string": ("'a':'b'", "'a'='b'"),
}

SAMPLE = {
    "int": ("1", "2"),
    "float": ("1.5", "2.5"),
    "string": ("'a'", "'b'"),
    "vector": ("v(1.0,2.0,3.0)", "v(4.0,5.0,6.0)"),
}


class TestToString(unittest.TestCase):
    def test_sequences_custom_delimiters(self):
        for kind in ("list", "array"):
            for t, (items, inner) in SEQUENCES.items():
                with self.subTest(t=f"{t}_{kind}"):
                    self.assertEqual(_to_string(f"{t}_{kind}", items, "<", "; ", ">"), f"<{inner}>")
            with self.subTest(t=f"string_{kind}"):
                self.assertEqual(_to_string(f"string_{kind}", "'a','b'", "<", "; ", ">", "'"), "<'a'; 'b'>")

    def test_sequences_empty_custom_delimiters(self):
        for kind in ("list", "array"):
            for t in (*SEQUENCES, "string"):
                with self.subTest(t=f"{t}_{kind}"):
                    self.assertEqual(_to_string(f"{t}_{kind}", "", "<", "; ", ">"), "<>")

    def test_dicts_custom_delimiters(self):
        for t, (items, inner) in DICTS.items():
            with self.subTest(t=t):
                self.assertEqual(_to_string(f"{t}_dict", items, "<", "; ", ">", "="), f"<{inner}>")
        for t, (items, inner) in STRING_DICTS.items():
            with self.subTest(t=t):
                self.assertEqual(_to_string(f"{t}_dict", items, "<", "; ", ">", "=", "'"), f"<{inner}>")

    def test_dict_sep_between_items(self):
        for t in (*DICTS, *STRING_DICTS):
            k, v = t.split("_")
            pairs = [f"{SAMPLE[k][i]}:{SAMPLE[v][i]}" for i in range(2)]
            with self.subTest(t=t):
                s = _to_string(f"{t}_dict", ",".join(pairs), "", "|", "")
                self.assertEqual(sorted(s.split("|")),
                                 sorted(_to_string(f"{t}_dict", p, "", "|", "") for p in pairs))

    def test_bool_custom_words(self):
        for kind in ("list", "array"):
            with self.subTest(kind=kind):
                self.assertEqual(_to_string(f"bool_{kind}", "true,false", "[", ", ", "]", "1", "0"), "[1, 0]")

    def test_empty_quote(self):
        self.assertEqual(_to_string("string_list", "'a','b'", "[", ", ", "]", ""), "[a, b]")
        self.assertEqual(_to_string("string_array", "'a','b'", "[", ", ", "]", ""), "[a, b]")
        self.assertEqual(_to_string("string_string_dict", "'a':'b'", "{", ", ", "}", ": ", ""), "{a: b}")
        self.assertEqual(_to_string("int_string_dict", "1:'b'", "{", ", ", "}", ": ", ""), "{1: b}")
        self.assertEqual(_to_string("string_int_dict", "'a':2", "{", ", ", "}", ": ", ""), "{a: 2}")

    def test_dicts_empty_custom_delimiters(self):
        for t in (*DICTS, *STRING_DICTS):
            with self.subTest(t=t):
                self.assertEqual(_to_string(f"{t}_dict", "", "<", "; ", ">"), "<>")

    def test_defaults_unchanged(self):
        self.assertEqual(_to_string("string_list", "'a','b'"), '["a", "b"]')
        self.assertEqual(_to_string("string_array", ""), "[]")
        self.assertEqual(_to_string("string_string_dict", "'a':'b'"), '{"a": "b"}')
        self.assertEqual(_to_string("int_int_dict", "1:2"), "{1: 2}")


if __name__ == "__main__":
    unittest.main()
