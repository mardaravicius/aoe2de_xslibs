import random
import unittest

from numpy import int32

from xs.functions import xs_bit_shift_right, xs_bit_shift_left, xs_bit_not, xs_bit_and, xs_bit_xor, xs_bit_or


class FunctionsTest(unittest.TestCase):

    def test_right_shift(self):
        for n in range(100000):
            a = int32(random.randint(-2147483648, 2147483647))
            if random.randint(0, 1) == 1:
                b = int32(random.randint(-1, 33))
            else:
                b = int32(random.randint(-2147483648, 2147483647))
            expected = int32(a) >> int32(b)
            actual = xs_bit_shift_right(int32(a), int32(b))
            self.assertEqual(expected, actual, f"{a} >> {b}")

    def test_right_shift_edges(self):
        edges = [-2147483648, -2147483647, 2147483647, 2147483646, 0, 1, -1, 2, -2]
        for a in edges:
            for b in list(range(-32, 64)) + edges:
                expected = int32(a) >> int32(b)
                actual = xs_bit_shift_right(int32(a), int32(b))
                self.assertEqual(expected, actual, f"{a} >> {b}")

    def test_left_shift(self):
        for n in range(100000):
            a = int32(random.randint(-2147483648, 2147483647))
            if random.randint(0, 1) == 1:
                b = int32(random.randint(-1, 33))
            else:
                b = int32(random.randint(-2147483648, 2147483647))
            expected = int32(a) << int32(b)
            actual = xs_bit_shift_left(int32(a), int32(b))
            self.assertEqual(expected, actual, f"{a} << {b}")

    def test_left_shift_edges(self):
        edges = [-2147483648, -2147483647, 2147483647, 2147483646, 0, 1, -1, 2, -2]
        for a in edges:
            for b in list(range(-32, 64)) + edges:
                expected = int32(a) << int32(b)
                actual = xs_bit_shift_left(int32(a), int32(b))
                self.assertEqual(expected, actual, f"{a} << {b}")

    def test_not(self):
        for n in range(100000):
            n = int32(random.randint(-2147483648, 2147483647))
            expected = ~int32(n)
            actual = xs_bit_not(int32(n))
            self.assertEqual(expected, actual, f"~{n}")

    def test_not_edges(self):
        edges = [-2147483648, -2147483647, 2147483647, 2147483646, 0, 1, -1, 2, -2]
        for n in edges:
            expected = ~int32(n)
            actual = xs_bit_not(int32(n))
            self.assertEqual(expected, actual, f"~{n}")

    def test_and(self):
        for n in range(100000):
            a = int32(random.randint(-2147483648, 2147483647))
            b = int32(random.randint(-2147483648, 2147483647))
            expected = int32(a) & int32(b)
            actual = xs_bit_and(int32(a), int32(b))
            self.assertEqual(expected, actual, f"{a} & {b}")

    def test_and_edges(self):
        edges = [-2147483648, -2147483647, 2147483647, 2147483646, 0, 1, -1, 2, -2]
        for a in edges:
            for b in edges:
                expected = int32(a) & int32(b)
                actual = xs_bit_and(int32(a), int32(b))
                self.assertEqual(expected, actual, f"{a} & {b}")

    def test_xor(self):
        for n in range(100000):
            a = int32(random.randint(-2147483648, 2147483647))
            b = int32(random.randint(-2147483648, 2147483647))
            expected = int32(a) ^ int32(b)
            actual = xs_bit_xor(int32(a), int32(b))
            self.assertEqual(expected, actual, f"{a} ^ {b}")

    def test_xor_edges(self):
        edges = [-2147483648, -2147483647, 2147483647, 2147483646, 0, 1, -1, 2, -2]
        for a in edges:
            for b in edges:
                expected = int32(a) ^ int32(b)
                actual = xs_bit_xor(int32(a), int32(b))
                self.assertEqual(expected, actual, f"{a} ^ {b}")

    def test_or(self):
        for n in range(100000):
            a = int32(random.randint(-2147483648, 2147483647))
            b = int32(random.randint(-2147483648, 2147483647))
            expected = int32(a) | int32(b)
            actual = xs_bit_or(int32(a), int32(b))
            self.assertEqual(expected, actual, f"{a} | {b}")

    def test_or_edges(self):
        edges = [-2147483648, -2147483647, 2147483647, 2147483646, 0, 1, -1, 2, -2]
        for a in edges:
            for b in edges:
                expected = int32(a) | int32(b)
                actual = xs_bit_or(int32(a), int32(b))
                self.assertEqual(expected, actual, f"{a} ^ {b}")
