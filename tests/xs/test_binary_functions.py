import os
import random
import subprocess
import unittest
from pathlib import Path

from numpy import uint32

from xs.binary_functions import *

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
        for n in range(10000):
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
        for n in range(10000):
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
        for n in range(10000):
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

    def test_random_uniform_in_range(self):
        xs_mt_seed(int32(random.randint(-2147483648, 2147483647)))

        for _ in range(1000):
            s = int32(random.randint(-2147483648, 2147483647))
            e = int32(random.randint(s, 2147483647))
            r = xs_mt_random_uniform_range(s, e)
            if e <= s:
                self.assertEqual(-1, r, f"[{s}, {e}]")
            else:
                self.assertGreaterEqual(r, s, f"[{s}, {e}]")
                self.assertLess(r, e, f"[{s}, {e}]")

    def test_random_uniform_in_range_edges(self):
        xs_mt_seed(int32(random.randint(-2147483648, 2147483647)))
        edges = [-2147483648, -2147483647, 2147483647, 2147483646, 0, 1, -1, 2, -2]
        for s in edges:
            for e in edges:
                r = xs_mt_random_uniform_range(int32(s), int32(e))
                if e <= s:
                    self.assertEqual(-1, r)
                else:
                    self.assertGreaterEqual(r, s, f"[{s}, {e}]")
                    self.assertLess(r, e, f"[{s}, {e}]")

    def test_random_uniform_is_uniform(self):
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
            self.assertGreaterEqual(occurrences, avg_items * 0.7,
                                    f"{seed=}, {s=}, {e=}, {number=}, {occurrences=}")
            self.assertLessEqual(occurrences, avg_items * 1.3, f"{seed=}, {s=}, {e=}, {number=}, {occurrences=}")

    def test_random(self):
        curr_dir = os.getcwd()
        curr_dir = curr_dir[:curr_dir.find("aoe2de_xslibs") + len("aoe2de_xslibs")]
        c_dir = Path(curr_dir) / "tests/c"
        if os.name == 'nt':
            c_dir = str(c_dir)
            c = str(c_dir).find(":")
            c_dir = c_dir[:c-1] + c_dir[c-1:c].lower() + c_dir[c:]
            c_dir = "/mnt/" + c_dir.replace("\\", "/").replace(":", "")
            cpp_path = str(c_dir + "/mt.cpp")
            exec_path = str(c_dir + "/mt")
            result = subprocess.run(["wsl", "--exec", "g++", cpp_path, "-o", exec_path, "-O3"])
        else:
            cpp_path = str(c_dir / "mt.cpp")
            exec_path = str(c_dir / "mt")
            result = subprocess.run(['g++', cpp_path, "-o", exec_path, "-O3"])
        if result.returncode != 0:
            raise Exception(f"g++ failed with return code {result.returncode}")
        attempts = 10
        random_iterations = 500
        for _ in range(attempts):
            seed = int32(random.randint(-2147483648, 2147483647))
            if os.name == "nt":
                result = subprocess.run(["wsl", "--exec", exec_path, str(seed), str(random_iterations)], stdout=subprocess.PIPE)
            else:
                result = subprocess.run([exec_path, str(seed), str(random_iterations)], stdout=subprocess.PIPE)
            if result.returncode != 0:
                raise Exception(f"mt failed with return code {result.returncode}")
            expected_results = result.stdout.decode("utf-8").split("\n")
            expected_results = [int32(x.strip()) for x in expected_results if len(x.strip()) > 0]
            xs_mt_seed(seed)
            actual_results = []
            for _ in range(random_iterations):
                actual_results.append(xs_mt_random())
            self.assertEqual(actual_results, expected_results, f"{seed=}, {random_iterations=}")
