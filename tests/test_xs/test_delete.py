import importlib
import unittest
from unittest import mock

import numpy as np
from numpy import int32

from xs_converter.functions import xs_array_get_int, xs_array_get_size

np.seterr(over="ignore")

# module name -> (main array resize function, [(child array getter, child resize function)])
def _at(idx: int):
    return lambda module, handle: xs_array_get_int(handle, int32(idx))


COLLECTIONS = {
    "int_list": ("xs_array_resize_int", []),
    "float_list": ("xs_array_resize_float", []),
    "vector_list": ("xs_array_resize_float", []),
    "bool_list": ("xs_array_resize_int", [(_at(1), "xs_array_resize_bool")]),
    "string_list": ("xs_array_resize_int", [(_at(1), "xs_array_resize_string")]),
    "int_int_dict": ("xs_array_resize_int", []),
    "float_int_dict": ("xs_array_resize_int", []),
    "int_vector_dict": ("xs_array_resize_float", []),
    "float_vector_dict": ("xs_array_resize_float", []),
    "vector_int_dict": ("xs_array_resize_float", []),
    "vector_vector_dict": ("xs_array_resize_float", []),
    "int_string_dict": ("xs_array_resize_int", [(_at(1), "xs_array_resize_string")]),
    "float_string_dict": ("xs_array_resize_int", [(_at(1), "xs_array_resize_string")]),
    "string_int_dict": ("xs_array_resize_int", [(_at(1), "xs_array_resize_string")]),
    "string_string_dict": ("xs_array_resize_int", [(_at(1), "xs_array_resize_string")]),
    "string_vector_dict": ("xs_array_resize_int", [(_at(1), "xs_array_resize_string"), (_at(2), "xs_array_resize_float")]),
    "vector_string_dict": ("xs_array_resize_float", [
        (lambda m, h: m._xs_vector_string_dict_get_values_array(h), "xs_array_resize_string"),
    ]),
}


class DeleteTest(unittest.TestCase):
    def _create(self, name: str):
        module = importlib.import_module(f"xs.{name}")
        handle = getattr(module, f"xs_{name}_create")()
        self.assertGreaterEqual(handle, 0)
        return module, handle

    def _child_arrays(self, module, name: str, handle: int32) -> list[int32]:
        return [getter(module, handle) for getter, _ in COLLECTIONS[name][1]]

    def test_delete_resizes_all_arrays_to_zero(self):
        for name in COLLECTIONS:
            with self.subTest(name):
                module, handle = self._create(name)
                children = self._child_arrays(module, name, handle)

                result = getattr(module, f"xs_{name}_delete")(handle)

                self.assertEqual(result, getattr(module, f"c_{name}_success"))
                self.assertEqual(xs_array_get_size(handle), 0)
                for child in children:
                    self.assertEqual(xs_array_get_size(child), 0)

    def test_delete_returns_error_when_any_resize_fails(self):
        for name, (main_resize, children) in COLLECTIONS.items():
            resize_fns = [main_resize] + [fn for _, fn in children]
            for fail_at in range(len(resize_fns)):
                with self.subTest(name, fail_at=fail_at):
                    module, handle = self._create(name)
                    calls = {"n": 0}

                    def _patched(orig):
                        def _resize(arr, size):
                            calls["n"] += 1
                            if calls["n"] == fail_at + 1:
                                return int32(-1)
                            return orig(arr, size)
                        return _resize

                    patches = [mock.patch.object(module, fn, _patched(getattr(module, fn))) for fn in set(resize_fns)]
                    for p in patches:
                        p.start()
                    try:
                        result = getattr(module, f"xs_{name}_delete")(handle)
                    finally:
                        for p in patches:
                            p.stop()

                    self.assertEqual(result, getattr(module, f"c_{name}_resize_failed_error"))


if __name__ == "__main__":
    unittest.main()
