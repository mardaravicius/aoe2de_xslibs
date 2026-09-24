from numpy import int32, float32

from xs_converter.functions import xs_array_create_int, xs_array_set_int, xs_array_get_int, xs_get_random_number, \
    bit_and, bit_or, bit_xor, bit_cast_to_float, bit_lsh, bit_rsh
from xs_converter.symbols import XsConst

_c_mt_n: XsConst[int32] = int32(624)
_c_mt_m: XsConst[int32] = int32(397)
_c_mt_nm: int32 = int32(-1)
_c_mt_w: XsConst[int32] = int32(32)
_c_mt_r: XsConst[int32] = int32(31)
_c_mt_w2: XsConst[int32] = int32(30)
_c_mt_matrix_a: int32 = int32(-1)
_c_mt_upper_mask: int32 = int32(-1)
_c_mt_lower_mask: int32 = int32(-1)
_c_mt_a: int32 = int32(-1)
_c_mt_u: XsConst[int32] = int32(11)
_c_mt_s: XsConst[int32] = int32(7)
_c_mt_t: XsConst[int32] = int32(15)
_c_mt_l: XsConst[int32] = int32(18)
_c_mt_b: int32 = int32(-1)
_c_mt_c: XsConst[int32] = int32(-272236544)
_c_mt_f: int32 = int32(-1)
_c_mt_int_max: int32 = int32(-1)
_c_mt_float_1_as_int: int32 = int32(-1)

_mt_seed_not_set: bool = True
_mt_state_array: int32 = int32(-1)
_mt_state_index: int32 = int32(0)


def _xs_bit_shift_right_logical(x: int32 = int32(0), n: int32 = int32(0)) -> int32:
    if x < 0:
        x += bit_lsh(-1, 31)
        x = bit_rsh(x, n)
        return x + bit_lsh(1, int32(31) - n)
    return bit_rsh(x, n)


def xs_bit_shift_right_logical(x: int32 = int32(0), n: int32 = int32(0)) -> int32:
    if n < 0 or n >= 32:
        return int32(0)
    return _xs_bit_shift_right_logical(x, n)


def xs_mt_seed(seed: int32 = int32(0)) -> None:
    global _mt_state_array, _c_mt_matrix_a, _c_mt_upper_mask, _c_mt_lower_mask, _c_mt_a, _c_mt_b, _c_mt_f, \
        _mt_state_index, _mt_seed_not_set, _c_mt_nm, _c_mt_int_max, _c_mt_float_1_as_int
    if _mt_state_array < 0:
        _c_mt_matrix_a = int32(-1727483681)
        _c_mt_upper_mask = bit_lsh(int32(-1), _c_mt_r)
        _c_mt_lower_mask = _xs_bit_shift_right_logical(int32(-1), _c_mt_w - _c_mt_r)
        _c_mt_a = int32(-1727483681)
        _c_mt_b = int32(-1658038656)
        _c_mt_f = int32(1812433253)
        _c_mt_nm = _c_mt_n - _c_mt_m
        _mt_state_array = xs_array_create_int(_c_mt_n, 0, "_mtStateArray")
        _c_mt_int_max = int32(2147483647)
        _c_mt_float_1_as_int = int32(1065353216)
    xs_array_set_int(_mt_state_array, 0, seed)
    i: int32 = int32(1)
    while i < _c_mt_n:
        seed = _c_mt_f * bit_xor(seed, _xs_bit_shift_right_logical(seed, _c_mt_w2)) + i
        xs_array_set_int(_mt_state_array, i, seed)
        i += 1
    _mt_state_index = int32(0)
    _mt_seed_not_set = False


def xs_mt_random() -> int32:
    global _mt_state_index

    if _mt_seed_not_set:
        xs_mt_seed(
            bit_rsh(xs_get_random_number(), int32(4)) +
            bit_lsh(bit_rsh(xs_get_random_number(), int32(4)), int32(11)) +
            bit_lsh(bit_rsh(xs_get_random_number(), int32(5)), int32(22))
        )

    k: int32 = _mt_state_index

    j: int32 = k - (_c_mt_n - 1)
    if j < 0:
        j += _c_mt_n

    x: int32 = bit_or(
        bit_and(xs_array_get_int(_mt_state_array, k), _c_mt_upper_mask),
        bit_and(xs_array_get_int(_mt_state_array, j), _c_mt_lower_mask),
    )

    xa: int32 = _xs_bit_shift_right_logical(x, int32(1))
    if bit_and(x, int32(1)) != 0:
        xa = bit_xor(xa, _c_mt_a)

    j = k - _c_mt_nm
    if j < 0:
        j += _c_mt_n

    x = bit_xor(xs_array_get_int(_mt_state_array, j), xa)
    xs_array_set_int(_mt_state_array, k, x)
    k += 1

    if k >= _c_mt_n:
        k = int32(0)
    _mt_state_index = k

    y: int32 = bit_xor(x, _xs_bit_shift_right_logical(x, _c_mt_u))
    y = bit_xor(y, bit_and(bit_lsh(y, _c_mt_s), _c_mt_b))
    y = bit_xor(y, bit_and(bit_lsh(y, _c_mt_t), _c_mt_c))
    return bit_xor(y, _xs_bit_shift_right_logical(y, _c_mt_l))


def xs_mt_random_float() -> float32:
    bits: int32 = bit_or(bit_and(xs_mt_random(), _c_mt_int_max) // int32(256), _c_mt_float_1_as_int)
    return bit_cast_to_float(bits) - float32(1.0)


def xs_mt_random_bool() -> bool:
    return xs_mt_random() > -1


def xs_mt_random_uniform_range(start: int32 = int32(0), end: int32 = int32(999999999)) -> int32:
    if end <= start:
        return int32(-1)

    dst: int32 = end - start
    if dst == 1:
        return start

    dst_m: int32 = dst - 1
    if bit_and(dst, dst_m) == 0:
        return bit_and(xs_mt_random(), dst_m) + start

    if dst > 0:
        while True:
            r: int32 = _xs_bit_shift_right_logical(xs_mt_random(), int32(1))
            c: int32 = r % dst

            if r + dst_m - c >= 0:
                return c + start

    while True:
        rr: int32 = xs_mt_random()
        if rr >= start and rr < end:
            return rr
    return int32(-1)
