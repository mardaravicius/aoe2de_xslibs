from numpy import int32

from xs_converter.functions import xs_array_create_int, xs_array_set_int, xs_array_get_int
from xs_converter.symbols import XsStatic


def xs_bit_shift_left(x: int32, n: int32) -> int32:
    if n == 0:
        return x
    if n < 0 or n >= 32:
        return int32(0)
    result: int32 = x
    i: int32 = int32(0)
    while i < n:
        result *= 2
        i += 1
    return result


def xs_bit_shift_right(x: int32, n: int32) -> int32:
    if n == 0:
        return x
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


def xs_bit_not(n: int32) -> int32:
    return (n * -1) - 1


def _compute_powers() -> int32:
    arr: XsStatic[int32] = -1
    if arr == -1:
        arr = xs_array_create_int(32, 1)
        for i in range(1, 32):
            xs_array_set_int(arr, i, int32(xs_array_get_int(arr, i - 1)) * 2)
    return arr


def _get_bit(x: int32, i: int32, powers: int32) -> int32:
    mod: int32 = xs_array_get_int(powers, i + 1)
    b: int32 = (x % mod) // xs_array_get_int(powers, i)
    if b < 0:
        b += 2
    return b


def _set_bit(bit: int32, i: int32, powers: int32) -> int32:
    return bit * xs_array_get_int(powers, i)


def xs_bit_and(a: int32, b: int32) -> int32:
    powers = _compute_powers()
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
    powers = _compute_powers()
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
    powers = _compute_powers()
    res: int32 = int32(0)
    for i in range(0, 31):
        abit: int32 = _get_bit(a, i, powers)
        bbit: int32 = _get_bit(b, i, powers)
        bit: int32 = abit + bbit - abit * bbit
        res += _set_bit(bit, i, powers)
    if a < 0 or b < 0:
        res += -2147483648
    return res

