import random
import unittest

import numpy
from numpy import int32, uint32

from xs.functions import xs_bit_shift_right_arithmetic, xs_bit_shift_left, xs_bit_not, xs_bit_and, xs_bit_xor, \
    xs_bit_or, \
    xs_mt_seed, xs_mt_random, xs_bit_shift_right_logical, \
    xs_mt_random_uniform_range


class FunctionsTest(unittest.TestCase):

    def test_right_shift_arithmetic(self):
        for n in range(100000):
            a = int32(random.randint(-2147483648, 2147483647))
            if random.randint(0, 1) == 1:
                b = int32(random.randint(-1, 33))
            else:
                b = int32(random.randint(-2147483648, 2147483647))
            expected = int32(a) >> int32(b)
            actual = xs_bit_shift_right_arithmetic(int32(a), int32(b))
            self.assertEqual(expected, actual, f"{a} >> {b}")

    def test_right_shift_arithmetic_edges(self):
        edges = [-2147483648, -2147483647, 2147483647, 2147483646, 0, 1, -1, 2, -2]
        for a in edges:
            for b in list(range(-32, 64)) + edges:
                expected = int32(a) >> int32(b)
                actual = xs_bit_shift_right_arithmetic(int32(a), int32(b))
                self.assertEqual(expected, actual, f"{a} >> {b}")

    def test_right_shift_logical(self):
        for n in range(100000):
            a = int32(random.randint(-2147483648, 2147483647))
            if random.randint(0, 1) == 1:
                b = int32(random.randint(-1, 33))
            else:
                b = int32(random.randint(-2147483648, 2147483647))
            expected = int32(uint32(int32(a)) >> uint32(int32(b)))
            actual = xs_bit_shift_right_logical(int32(a), int32(b))
            self.assertEqual(expected, actual, f"{a} >>> {b}")

    def test_right_shift_logical_edges(self):
        edges = [-2147483648, -2147483647, 2147483647, 2147483646, 0, 1, -1, 2, -2]
        for a in edges:
            for b in list(range(-32, 64)) + edges:
                expected = int32(uint32(int32(a)) >> uint32(int32(b)))
                actual = xs_bit_shift_right_logical(int32(a), int32(b))
                self.assertEqual(expected, actual, f"{a} >>> {b}")

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

    def test_unsigned_multiply(self):
        for n in range(100000):
            a = random.randint(0, 4294967295)
            b = random.randint(0, 4294967295)
            ua = uint32(a)
            ub = uint32(b)
            # aa = xs_unsigned_multiply(int32(ua), int32(ub))

            ia = int32(ua)
            ib = int32(ub)
            r = ia * ib
            actual = uint32(r)
            expected = ua * ub

            self.assertEqual(expected, actual, f"{a} * {b}")

    def test_random_uniform_in_range(self):
        xs_mt_seed(int32(1))

        for _ in range(1000):
            s = int32(random.randint(-2147483648, 2147483647))
            e = int32(random.randint(s, 2147483647))
            r = xs_mt_random_uniform_range(s, e)
            if s == e:
                self.assertEqual(-1, r)
            else:
                self.assertGreaterEqual(r, s, f"[{s}, {e}]")
                self.assertLess(r, e, f"[{s}, {e}]")

    def test_random_uniform_is_uniform(self):
        with numpy.errstate(over='ignore'):
            seed = int32(random.randint(-2147483648, 2147483647))
            xs_mt_seed(seed)

            d = random.randint(1, 200)
            s = random.randint(-2147483648, 2147483647 - d)
            e = random.randint(s + 1, s + d - 1)
            r = e - s
            loops = 10000
            avg_items = loops // r

            results = {}
            for i in range(s, e):
                results[i] = 0
            for _ in range(loops):
                res = xs_mt_random_uniform_range(int32(s), int32(e))
                results[res] += 1
            results = sorted(list(results.items()), key=lambda t: t[1])
            for number, occurrences in results:
                self.assertGreaterEqual(occurrences, avg_items * 0.67,
                                        f"{seed=}, {s=}, {e=}, {number=}, {occurrences=}")
                self.assertLessEqual(occurrences, avg_items * 1.33, f"{seed=}, {s=}, {e=}, {number=}, {occurrences=}")

    def test_random(self):
        random.seed(1)
        xs_mt_seed(int32(1))

        for _ in range(200):
            r = int32(uint32(random.getrandbits(32)))
            print(r)
            r2 = xs_mt_random()
            print(r2)

        self.assertEqual(1, 1)
