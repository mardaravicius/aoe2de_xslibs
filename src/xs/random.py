from numpy import int32, float32

from xs_converter.functions import xs_get_random_number, bit_cast_to_float
from xs_converter.symbols import XsConst

_c_xo_splitmix32_a: int32 = int32(-1)
_c_xo_splitmix32_b: XsConst[int32] = int32(569420461)
_c_xo_splitmix32_c: int32 = int32(-1)
_c_xo_int_max: int32 = int32(-1)
_c_xo_float_1_as_int: int32 = int32(-1)

_xo_splitmix32_s: int32 = int32(0)
_xo_s0: int32 = int32(0)
_xo_s1: int32 = int32(0)
_xo_s2: int32 = int32(0)
_xo_s3: int32 = int32(0)
_xo_seed_not_set: bool = True


def _xo_bit_shift_right_logical(x: int32 = int32(-1), n: int32 = int32(-1)) -> int32:
    if x < 0:
        x += int32(-1) << int32(31)
        x >>= n
        return x + (int32(1) << int32(31) - n)
    return x >> n


def _xo_rotl(x: int32 = int32(-1), k: int32 = int32(-1)) -> int32:
    return x << k | _xo_bit_shift_right_logical(x, int32(32) - k)


def _xo_splitmix32() -> int32:
    global _xo_splitmix32_s
    _xo_splitmix32_s += _c_xo_splitmix32_a
    z: int32 = _xo_splitmix32_s
    z ^= _xo_bit_shift_right_logical(z, int32(16))
    z *= _c_xo_splitmix32_b
    z ^= _xo_bit_shift_right_logical(z, int32(15))
    z *= _c_xo_splitmix32_c
    z ^= _xo_bit_shift_right_logical(z, int32(15))
    return z


def xs_xo_seed(seed: int32 = int32(0)) -> None:
    global _xo_s0, _xo_s1, _xo_s2, _xo_s3, _xo_seed_not_set, _c_xo_splitmix32_a, _c_xo_splitmix32_b, \
        _c_xo_splitmix32_c, _c_xo_int_max, _c_xo_float_1_as_int, _xo_splitmix32_s
    if _c_xo_splitmix32_a < 0:
        _c_xo_splitmix32_a = int32(-1640531527)
        _c_xo_splitmix32_c = int32(1935289751)
        _c_xo_int_max = int32(2147483647)
        _c_xo_float_1_as_int = int32(1065353216)
    _xo_splitmix32_s = seed
    _xo_s0 = _xo_splitmix32()
    _xo_s1 = _xo_splitmix32()
    _xo_s2 = _xo_splitmix32()
    _xo_s3 = _xo_splitmix32()

    if _xo_s0 == 0 and _xo_s1 == 0 and _xo_s2 == 0 and _xo_s3 == 0:
        _xo_s0 = int32(1)

    _xo_seed_not_set = False


def xs_xo_random() -> int32:
    global _xo_s0, _xo_s1, _xo_s2, _xo_s3, _xo_seed_not_set
    if _xo_seed_not_set:
        xs_xo_seed(
            (xs_get_random_number() >> int32(4)) +
            (xs_get_random_number() >> int32(4) << int32(11)) +
            (xs_get_random_number() >> int32(5) << int32(22))
        )
    result: int32 = _xo_rotl(_xo_s1 * int32(5), int32(7)) * int32(9)

    t: int32 = _xo_s1 << int32(9)

    _xo_s2 ^= _xo_s0
    _xo_s3 ^= _xo_s1
    _xo_s1 ^= _xo_s2
    _xo_s0 ^= _xo_s3

    _xo_s2 ^= t

    _xo_s3 = _xo_rotl(_xo_s3, int32(11))

    return result


def xs_xo_random_float() -> float32:
    bits: int32 = (xs_xo_random() & _c_xo_int_max) // int32(256) | _c_xo_float_1_as_int
    return bit_cast_to_float(bits) - float32(1.0)


def xs_xo_random_bool() -> bool:
    return xs_xo_random() > -1


def xs_xo_random_uniform_range(start: int32 = int32(0), end: int32 = int32(999999999)) -> int32:
    if end <= start:
        return int32(-1)

    dst: int32 = end - start
    if dst == 1:
        return start

    dst_m: int32 = dst - 1
    if dst & dst_m == 0:
        return (xs_xo_random() & dst_m) + start

    if dst > 0:
        while True:
            r: int32 = _xo_bit_shift_right_logical(xs_xo_random(), int32(1))
            c: int32 = r % dst

            if r + dst_m - c >= 0:
                return c + start

    while True:
        rr: int32 = xs_xo_random()
        if rr >= start and rr < end:
            return rr
    return int32(-1)
