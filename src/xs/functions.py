from numpy import int32

from xs_converter.functions import xs_array_create_int, xs_array_set_int, xs_array_get_int
from xs_converter.symbols import XsStatic

_powers: int32 = int32(-1)

def xs_bit_shift_left(x: int32, n: int32) -> int32:
    if n < 0 or n >= 32:
        return int32(0)
    result: int32 = x
    i: int32 = int32(0)
    while i < n:
        result *= 2
        i += 1
    return result


def xs_bit_shift_arithmetic_right(x: int32, n: int32) -> int32:
    if n < 0 or n >= 32:
        if x < 0:
            return int32(-1)
        return int32(0)
    result: int32 = x
    i: int32 = int32(0)
    while i < n:
        result //= 2
        i += 1
    return result


def xs_bit_shift_logical_right(x: int32, n: int32) -> int32:
    if n < 0 or n >= 32:
        return int32(0)
    i: int32 = int32(0)
    result: int32 = x
    if x < 0:
        result = x + int32(-2147483648)
        while i < n:
            result //= 2
            i += 1
        powers: int32 = _get_powers()
        p: int32 = xs_array_get_int(powers, 31 - n)
        result += p
    else:
        while i < n:
            result //= 2
            i += 1
    return result


def xs_bit_not(n: int32) -> int32:
    return (n * -1) - 1


def _get_powers() -> int32:
    global _powers
    if _powers == -1:
        _powers = xs_array_create_int(32, 1)
        for i in range(1, 32):
            xs_array_set_int(_powers, i, int32(xs_array_get_int(_powers, i - 1)) * 2)
    return _powers


def _get_bit(x: int32, i: int32, powers: int32) -> int32:
    mod: int32 = xs_array_get_int(powers, i + 1)
    b: int32 = (x % mod) // xs_array_get_int(powers, i)
    if b < 0:
        b += 2
    return b


def _set_bit(bit: int32, i: int32, powers: int32) -> int32:
    return bit * xs_array_get_int(powers, i)


def xs_bit_and(a: int32, b: int32) -> int32:
    powers: int32 = _get_powers()
    res: int32 = int32(0)
    for i in range(0, 31):
        abit: int32 = _get_bit(a, i, powers)
        bbit: int32 = _get_bit(b, i, powers)
        bit: int32 = abit * bbit
        res += _set_bit(bit, i, powers)
    if a < 0 and b < 0:
        res += -2147483648
    return res


def xs_bit_xor(a: int32, b: int32) -> int32:
    powers: int32 = _get_powers()
    res: int32 = int32(0)
    for i in range(0, 31):
        abit: int32 = _get_bit(a, i, powers)
        bbit: int32 = _get_bit(b, i, powers)
        bit: int32 = (abit + bbit) % 2
        res += _set_bit(bit, i, powers)
    if (a < 0 and b >= 0) or (a >= 0 and b < 0):
        res += -2147483648
    return res


def xs_bit_or(a: int32, b: int32) -> int32:
    powers: int32 = _get_powers()
    res: int32 = int32(0)
    for i in range(0, 31):
        abit: int32 = _get_bit(a, i, powers)
        bbit: int32 = _get_bit(b, i, powers)
        bit: int32 = abit + bbit - abit * bbit
        res += _set_bit(bit, i, powers)
    if a < 0 or b < 0:
        res += -2147483648
    return res


def xs_unsigned_multiply(a: int32, b: int32) -> int32:
    a_hi: int32 = xs_bit_shift_logical_right(a, int32(16))
    a_lo: int32 = xs_bit_and(a, int32(65535))
    b_hi: int32 = xs_bit_shift_logical_right(b, int32(16))
    b_lo: int32 = xs_bit_and(b, int32(65535))

    res_lo: int32 = a_lo * b_lo
    res_mid: int32 = a_hi * b_lo + a_lo * b_hi

    return res_lo + xs_bit_shift_left(res_mid, int32(16))


_n: int32 = int32(624)
_m: int32 = int32(397)
_w: int32 = int32(32)
_r: int32 = int32(31)
_matrix_a: int32 = int32(-1727483681)
_upper_mask: int32 = int32(-2147483648)
_lower_mask: int32 = int32(2147483647)

_a: int32 = int32(-1727483681)
_u: int32 = int32(11)
_s: int32 = int32(7)
_t: int32 = int32(15)
_l: int32 = int32(18)
_b: int32 = int32(-1658038656)
_c: int32 = int32(-272236544)
_f: int32 = int32(1812433253)

_state_array: int32 = int32(-1)
_state_index: int32 = int32(0)


def xs_mersenne_twister_seed(seed: int32) -> None:
    global _state_array, _state_index, _upper_mask, _lower_mask
    if _state_array < 0:
        _state_array = int32(xs_array_create_int(_n, 0))
    xs_array_set_int(_state_array, 0, seed)
    i: int32 = int32(1)
    while (i < _n):
        seed = _f * xs_bit_xor(seed, xs_bit_shift_logical_right(seed, (_w - 2))) + i
        xs_array_set_int(_state_array, i, seed)
        i += 1
    _state_index = int32(0)


def xs_mersenne_twister_random() -> int32:
    global _state_index, _state_index

    k: int32 = _state_index

    j: int32 = k - (_n - 1)
    if j < 0:
        j += _n

    x: int32 = xs_bit_or(
        xs_bit_and(xs_array_get_int(_state_array, k), _upper_mask),
        xs_bit_and(xs_array_get_int(_state_array, j), _lower_mask),
    )

    xa: int32 = xs_bit_shift_logical_right(x, int32(1))
    if (xs_bit_and(x, int32(1)) != 0):
        xa = xs_bit_xor(xa, _a)

    j = k - (_n - _m)
    if j < 0:
        j += _n

    x = xs_bit_xor(xs_array_get_int(_state_array, j), xa)
    xs_array_set_int(_state_array, k, x)
    k += 1

    if k >= _n:
        k = int32(0)
    _state_index = k

    y: int32 = xs_bit_xor(x, xs_bit_shift_logical_right(x, _u))
    y = xs_bit_xor(y, xs_bit_and(xs_bit_shift_left(y, _s), _b))
    y = xs_bit_xor(y, xs_bit_and(xs_bit_shift_left(y, _t), _c))
    z: int32 = xs_bit_xor(y, xs_bit_shift_logical_right(y, _l))

    return z


def xs_mersenne_twister_random_uniform_range(start: int32, end: int32) -> int32:
    range: int32 = end - start
    if range <= 0:
        return int32(-1)

    if xs_bit_and(range, (range - 1)) == 0:
        return start + xs_bit_and(xs_mersenne_twister_random(), (range - 1))

    threshold: int32 = (-1 * range) % range

    while True:
        r: int32 = xs_mersenne_twister_random()
        unsigned_r: int32 = r + int32(-2147483648)
        if unsigned_r >= threshold:
            result: int32 = unsigned_r % range
            return start + result
