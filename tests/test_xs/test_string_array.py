import unittest
from random import choice, randint

from xs.string_array import *


class StringArrayTest(unittest.TestCase):
    def test_xs_string_array(self):
        for i in range(0, 13):
            data = [f"s{v}" for v in range(i)]
            arr = xs_string_array(*data)
            self.assertEqual(i, xs_array_get_size(arr))
            self.assertEqual(sstr(data), xs_string_array_to_string(arr))

    def test_xs_string_array_stop_at_magic_number(self):
        arr = xs_string_array("a", "!<[empty", "b")
        self.assertEqual(sstr(["a"]), xs_string_array_to_string(arr))

    def test_xs_string_array_repeated(self):
        self.assertEqual(c_string_array_generic_error, xs_string_array_from_repeated_val("x", int32(-1)))
        self.assertEqual(sstr(["x", "x", "x"]), xs_string_array_to_string(xs_string_array_from_repeated_val("x", int32(3))))
        arr = xs_string_array("a", "b")
        self.assertEqual(sstr(["a", "b", "a", "b", "a", "b"]),
                         xs_string_array_to_string(xs_string_array_from_repeated_array(arr, int32(3))))
        self.assertEqual("[]", xs_string_array_to_string(xs_string_array_from_repeated_array(arr, int32(0))))

    def test_xs_string_array_repeated_array_edge_cases(self):
        empty = xs_string_array()
        self.assertEqual("[]", xs_string_array_to_string(xs_string_array_from_repeated_array(empty, int32(5))))
        arr = xs_string_array("a", "b")
        self.assertEqual(c_string_array_generic_error, xs_string_array_from_repeated_array(arr, int32(-1)))
        self.assertEqual(c_string_array_max_capacity_error,
                         xs_string_array_from_repeated_array(arr, c_string_array_max_capacity // 2 + 1))

    def test_xs_string_array_from_string(self):
        self.assertEqual(sstr(["a", " b, c:(", ""]),
                         xs_string_array_to_string(xs_string_array_from_string("'a', ' b, c:(' ,''")))
        self.assertEqual(sstr(["a", "", "d"]),
                         xs_string_array_to_string(xs_string_array_from_string("'a',b,'',,'e''f','d'")))
        self.assertEqual(sstr(["a", "b"]), xs_string_array_to_string(xs_string_array_from_string("'a',(,'b'")))
        self.assertEqual(sstr(["a"]), xs_string_array_to_string(xs_string_array_from_string("'a','b,'c'")))
        self.assertEqual("[]", xs_string_array_to_string(xs_string_array_from_string("  ")))

    def test_xs_string_array_index(self):
        arr = xs_string_array("a", "b", "c", "b")
        self.assertEqual(1, xs_string_array_index(arr, "b"))
        self.assertEqual(3, xs_string_array_index(arr, "b", int32(2)))
        self.assertEqual(3, xs_string_array_index(arr, "b", int32(-1)))
        self.assertEqual(c_string_array_generic_error, xs_string_array_index(arr, "b", int32(0), int32(-3)))
        self.assertTrue(xs_string_array_contains(arr, "c"))
        self.assertFalse(xs_string_array_contains(arr, "d"))
        self.assertEqual(2, xs_string_array_count(arr, "b"))

    def test_xs_string_array_index_edge_cases(self):
        arr = xs_string_array("a", "b", "c")
        self.assertEqual(c_string_array_generic_error, xs_string_array_index(arr, "a", int32(2), int32(1)))
        self.assertEqual(c_string_array_generic_error, xs_string_array_index(arr, "a", int32(5)))
        self.assertEqual(0, xs_string_array_index(arr, "a", int32(-10)))
        self.assertEqual(2, xs_string_array_index(arr, "c", int32(0), int32(100)))

    def test_xs_string_array_sort(self):
        for size in [0, 1, 2, 5, 50]:
            for reverse in [False, True]:
                data = ["".join(choice("abcAB1") for _ in range(randint(0, 4))) for _ in range(size)]
                arr = xs_array_create_string(int32(size))
                for i, v in enumerate(data):
                    xs_array_set_string(arr, int32(i), v)
                xs_string_array_sort(arr, reverse)
                self.assertEqual(sstr(sorted(data, reverse=reverse)), xs_string_array_to_string(arr))

    def test_xs_string_array_reverse(self):
        for i in range(0, 6):
            data = [f"s{v}" for v in range(i)]
            arr = xs_string_array(*data)
            xs_string_array_reverse(arr)
            self.assertEqual(sstr(list(reversed(data))), xs_string_array_to_string(arr))

    def test_xs_string_array_copy(self):
        data = [f"s{v}" for v in range(6)]
        arr = xs_string_array(*data)
        for start, end in [(0, 6), (2, 4), (-3, 6), (1, -1), (4, 2), (-10, 100)]:
            self.assertEqual(sstr(data[start:end]),
                             xs_string_array_to_string(xs_string_array_copy(arr, int32(start), int32(end))))
        self.assertEqual(sstr(data), xs_string_array_to_string(xs_string_array_copy(arr)))

    def test_xs_string_array_copy_start_past_end(self):
        arr = xs_string_array("a", "b", "c")
        self.assertEqual("[]", xs_string_array_to_string(xs_string_array_copy(arr, int32(5))))
        self.assertEqual("[]", xs_string_array_to_string(xs_string_array_copy(arr, int32(3), int32(10))))

    def test_xs_string_array_copy_is_independent(self):
        arr = xs_string_array("a", "b")
        copy = xs_string_array_copy(arr)
        xs_array_set_string(copy, int32(0), "z")
        self.assertEqual(sstr(["a", "b"]), xs_string_array_to_string(arr))

    def test_xs_string_array_compare(self):
        a = xs_string_array("a", "b")
        self.assertEqual(0, xs_string_array_compare(a, xs_string_array("a", "b")))
        self.assertEqual(-1, xs_string_array_compare(a, xs_string_array("a", "c")))
        self.assertEqual(1, xs_string_array_compare(a, xs_string_array("a")))
        self.assertEqual(-1, xs_string_array_compare(a, xs_string_array("a", "b", "")))

    def test_xs_string_array_min_max(self):
        arr = xs_string_array("b", "C", "a")
        self.assertEqual("C", xs_string_array_min(arr))
        self.assertEqual("b", xs_string_array_max(arr))
        self.assertEqual(c_string_array_success, xs_string_array_last_error())
        empty = xs_string_array()
        self.assertEqual("-1", xs_string_array_min(empty))
        self.assertEqual(c_string_array_index_out_of_range_error, xs_string_array_last_error())
        self.assertEqual("-1", xs_string_array_max(empty))

    def test_xs_string_array_empty_array_operations(self):
        empty = xs_string_array()
        self.assertEqual(c_string_array_generic_error, xs_string_array_index(empty, ""))
        self.assertFalse(xs_string_array_contains(empty, ""))
        self.assertEqual(0, xs_string_array_count(empty, ""))
        self.assertEqual(0, xs_string_array_compare(empty, xs_string_array()))
        self.assertEqual(-1, xs_string_array_compare(empty, xs_string_array("")))
        self.assertEqual(1, xs_string_array_compare(xs_string_array(""), empty))
        xs_string_array_reverse(empty)
        self.assertEqual("[]", xs_string_array_to_string(empty))
        self.assertEqual("[]", xs_string_array_to_string(xs_string_array_copy(empty)))

    def test_xs_string_array_delete(self):
        arr = xs_string_array("a", "b")
        self.assertEqual(c_string_array_success, xs_string_array_delete(arr))
        self.assertEqual(0, xs_array_get_size(arr))


def sstr(lst: list[str]) -> str:
    return "[" + ", ".join('"' + x + '"' for x in lst) + "]"


if __name__ == "__main__":
    unittest.main()
