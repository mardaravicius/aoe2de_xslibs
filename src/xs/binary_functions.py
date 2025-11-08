from numpy import int32

from xs_converter.converter import PythonToXsConverter
from xs_converter.functions import xs_array_create_int, xs_array_set_int, xs_array_get_int, xs_get_random_number
from xs_converter.symbols import XsConst

_bit_operator_powers: int32 = int32(-1)

_c_mt_n: int32 = int32(624)
_c_mt_m: int32 = int32(397)
_c_mt_nm: int32 = int32(-1)
_c_mt_w: int32 = int32(32)
_c_mt_r: int32 = int32(31)
_c_mt_matrix_a: int32 = int32(-1)
_c_mt_upper_mask: int32 = int32(-1)
_c_mt_lower_mask: int32 = int32(-1)
_c_mt_a: int32 = int32(--1)
_c_mt_u: int32 = int32(11)
_c_mt_s: int32 = int32(7)
_c_mt_t: int32 = int32(15)
_c_mt_l: int32 = int32(18)
_c_mt_b: int32 = int32(-1)
_c_mt_c: int32 = int32(-272236544)
_c_mt_f: int32 = int32(-1)

_mt_seed_set: bool = False
_mt_state_array: int32 = int32(-1)
_mt_state_index: int32 = int32(0)


def constants() -> None:
    _bit_operator_powers: int32 = int32(-1)

    _c_mt_n: XsConst[int32] = int32(624)
    _c_mt_m: XsConst[int32] = int32(397)
    _c_mt_nm: int32 = int32(-1)
    _c_mt_w: XsConst[int32] = int32(32)
    _c_mt_r: XsConst[int32] = int32(31)
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

    _mt_seed_set: bool = False
    _mt_state_array: int32 = int32(-1)
    _mt_state_index: int32 = int32(0)


def _xs_bit_get_powers() -> int32:
    global _bit_operator_powers
    if _bit_operator_powers == -1:
        _bit_operator_powers = xs_array_create_int(32, 1, "_bitOperatorPowers")
        for i in range(1, 32):
            xs_array_set_int(_bit_operator_powers, i, xs_array_get_int(_bit_operator_powers, i - 1) * 2)
    return _bit_operator_powers


def _xs_bit_shift_right_divide(x: int32 = int32(-1), n: int32 = int32(-1), powers: int32 = int32(-1)) -> int32:
    if n == 31:
        if x < 0:
            return int32(-1)
        return int32(0)
    return x // xs_array_get_int(powers, n)


def xs_bit_shift_left(x: int32 = int32(0), n: int32 = int32(0)) -> int32:
    if n < 0 or n >= 32:
        return int32(0)
    return x * xs_array_get_int(_xs_bit_get_powers(), n)


def xs_bit_shift_right_arithmetic(x: int32 = int32(0), n: int32 = int32(0)) -> int32:
    if n < 0 or n >= 32:
        if x < 0:
            return int32(-1)
        return int32(0)
    return _xs_bit_shift_right_divide(x, n, _xs_bit_get_powers())


def xs_bit_shift_right_logical(x: int32 = int32(0), n: int32 = int32(0)) -> int32:
    if n < 0 or n >= 32:
        return int32(0)
    powers: int32 = _xs_bit_get_powers()
    if x < 0:
        x += xs_array_get_int(powers, 31)
        x = _xs_bit_shift_right_divide(x, n, powers)
        return x + xs_array_get_int(powers, 31 - n)
    return _xs_bit_shift_right_divide(x, n, powers)


def xs_bit_not(n: int32 = int32(0)) -> int32:
    return (n * -1) - 1


def xs_bit_and(a: int32 = int32(0), b: int32 = int32(0)) -> int32:
    powers: int32 = _xs_bit_get_powers()
    res: int32 = int32(0)
    for i in range(0, 32):
        m: int32 = xs_array_get_int(powers, 31 - i)
        if a * m < 0 and b * m < 0:
            res += int32(1) * xs_array_get_int(powers, i)
    return res


def xs_bit_xor(a: int32 = int32(0), b: int32 = int32(0)) -> int32:
    powers: int32 = _xs_bit_get_powers()
    res: int32 = int32(0)
    for i in range(0, 32):
        m: int32 = xs_array_get_int(powers, 31 - i)
        an: int32 = a * m
        bn: int32 = b * m
        if (an < 0 and bn >= 0) or (an >= 0 and bn < 0):
            res += int32(1) * xs_array_get_int(powers, i)
    return res


def xs_bit_or(a: int32 = int32(0), b: int32 = int32(0)) -> int32:
    powers: int32 = _xs_bit_get_powers()
    res: int32 = int32(0)
    for i in range(0, 32):
        m: int32 = xs_array_get_int(powers, 31 - i)
        if a * m < 0 or b * m < 0:
            res += int32(1) * xs_array_get_int(powers, i)
    return res


def xs_mt_seed(seed: int32 = int32(0)) -> None:
    global _mt_state_array, _c_mt_matrix_a, _c_mt_upper_mask, _c_mt_lower_mask, _c_mt_a, _c_mt_b, _c_mt_f, \
        _mt_state_index, _mt_seed_set, _c_mt_nm
    if _mt_state_array < 0:
        _c_mt_matrix_a = int32(-1727483681)
        _c_mt_upper_mask = xs_bit_shift_left(int32(-1), _c_mt_r)
        _c_mt_lower_mask = xs_bit_shift_right_logical(int32(-1), _c_mt_w - _c_mt_r)
        _c_mt_a = int32(-1727483681)
        _c_mt_b = int32(-1658038656)
        _c_mt_f = int32(1812433253)
        _c_mt_nm = _c_mt_n - _c_mt_m
        _mt_state_array = xs_array_create_int(_c_mt_n, 0, "_mtStateArray")
    xs_array_set_int(_mt_state_array, 0, seed)
    i: int32 = int32(1)
    while i < _c_mt_n:
        seed = _c_mt_f * xs_bit_xor(seed, xs_bit_shift_right_logical(seed, (_c_mt_w - 2))) + i
        xs_array_set_int(_mt_state_array, i, seed)
        i += 1
    _mt_state_index = int32(0)
    _mt_seed_set = True


def xs_mt_random() -> int32:
    global _mt_state_index, _mt_state_index

    if not _mt_seed_set:
        xs_mt_seed(xs_get_random_number() * 65536 + xs_get_random_number())

    k: int32 = _mt_state_index

    j: int32 = k - (_c_mt_n - 1)
    if j < 0:
        j += _c_mt_n

    x: int32 = xs_bit_or(
        xs_bit_and(xs_array_get_int(_mt_state_array, k), _c_mt_upper_mask),
        xs_bit_and(xs_array_get_int(_mt_state_array, j), _c_mt_lower_mask),
    )

    xa: int32 = xs_bit_shift_right_logical(x, int32(1))
    if xs_bit_and(x, int32(1)) != 0:
        xa = xs_bit_xor(xa, _c_mt_a)

    j = k - _c_mt_nm
    if j < 0:
        j += _c_mt_n

    x = xs_bit_xor(xs_array_get_int(_mt_state_array, j), xa)
    xs_array_set_int(_mt_state_array, k, x)
    k += 1

    if k >= _c_mt_n:
        k = int32(0)
    _mt_state_index = k

    y: int32 = xs_bit_xor(x, xs_bit_shift_right_logical(x, _c_mt_u))
    y = xs_bit_xor(y, xs_bit_and(xs_bit_shift_left(y, _c_mt_s), _c_mt_b))
    y = xs_bit_xor(y, xs_bit_and(xs_bit_shift_left(y, _c_mt_t), _c_mt_c))
    return xs_bit_xor(y, xs_bit_shift_right_logical(y, _c_mt_l))


def xs_mt_random_uniform_range(start: int32 = int32(0), end: int32 = int32(999999999)) -> int32:
    if end <= start:
        return int32(-1)

    dist: int32 = end - start
    if dist == 1:
        return start

    distm: int32 = dist - 1
    if xs_bit_and(dist, distm) == 0:
        return xs_bit_and(xs_mt_random(), distm) + start

    if dist > 0:
        while True:
            r: int32 = xs_bit_shift_right_logical(xs_mt_random(), int32(1))
            c: int32 = r % dist

            if r + distm - c >= 0:
                return c + start

    while True:
        rr: int32 = xs_mt_random()
        if rr >= start and rr < end:
            return rr
    return int32(-1)


def functions(include_test: bool = False) -> tuple[str, str]:
    constants_function_xs = PythonToXsConverter.to_xs_script(
        constants,
        indent=True,
    )
    constants_xs = (constants_function_xs[constants_function_xs.find("int"):constants_function_xs.rfind("}")]
                    .strip()
                    .replace("    ", "")
                    ) + "\n\n"
    xs = constants_xs + PythonToXsConverter.to_xs_script(
        _xs_bit_get_powers,
        _xs_bit_shift_right_divide,
        xs_bit_shift_right_logical,
        xs_bit_shift_right_arithmetic,
        xs_bit_shift_left,
        xs_bit_not,
        xs_bit_and,
        xs_bit_or,
        xs_bit_xor,
        xs_mt_seed,
        xs_mt_random,
        xs_mt_random_uniform_range,
        indent=True,
    )
    print(xs)
    return xs, "binaryFunctions"


if __name__ == "__main__":
    functions()
