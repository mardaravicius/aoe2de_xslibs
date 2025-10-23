from numpy import int32

from xs_converter.converter import PythonToXsConverter
from xs_converter.functions import xs_array_create_int, xs_array_set_int, xs_array_get_int, xs_get_random_number
from xs_converter.symbols import XsConst

_bit_operator_powers: int32 = int32(-1)
_c_bit_operator_int_min_value: int32 = int32(-1)

_c_mt_n: int32 = int32(624)
_c_mt_m: int32 = int32(397)
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
    _c_bit_operator_int_min_value: int32 = int32(-1)

    _c_mt_n: XsConst[int32] = int32(624)
    _c_mt_m: XsConst[int32] = int32(397)
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


def xs_bit_shift_left(x: int32 = int32(0), n: int32 = int32(0)) -> int32:
    if n < 0 or n >= 32:
        return int32(0)
    powers: int32 = _xs_bit_operator_get_powers()
    x *= xs_array_get_int(powers, n)
    return x


def xs_bit_shift_right_arithmetic(x: int32 = int32(0), n: int32 = int32(0)) -> int32:
    if n < 0 or n >= 32:
        if x < 0:
            return int32(-1)
        return int32(0)
    powers: int32 = _xs_bit_operator_get_powers()
    p: int32 = 0
    if n == 31:
        p = xs_array_get_int(powers, 30)
        x = x // p // 2
    else:
        p = xs_array_get_int(powers, n)
        x //= p
    return x


def xs_bit_shift_right_logical(x: int32 = int32(0), n: int32 = int32(0)) -> int32:
    global _c_bit_operator_int_min_value
    if n < 0 or n >= 32:
        return int32(0)
    powers: int32 = _xs_bit_operator_get_powers()
    p: int32 = 0
    if x < 0:
        if _c_bit_operator_int_min_value == -1:
            _c_bit_operator_int_min_value = int32(-2147483648)
        x = x + _c_bit_operator_int_min_value
        if n == 31:
            p = xs_array_get_int(powers, 30)
            x = x // p // 2
        else:
            p = xs_array_get_int(powers, n)
            x //= p
        p = xs_array_get_int(powers, 31 - n)
        x += p
    else:
        if n == 31:
            p = xs_array_get_int(powers, 30)
            x = x // p // 2
        else:
            p = xs_array_get_int(powers, n)
            x //= p
    return x


def xs_bit_not(n: int32 = int32(0)) -> int32:
    return (n * -1) - 1


def _xs_bit_operator_get_powers() -> int32:
    global _bit_operator_powers
    if _bit_operator_powers == -1:
        _bit_operator_powers = xs_array_create_int(32, 1)
        for i in range(1, 32):
            xs_array_set_int(_bit_operator_powers, i, int32(xs_array_get_int(_bit_operator_powers, i - 1)) * 2)
    return _bit_operator_powers


def _xs_get_bit(x: int32 = int32(0), i: int32 = int32(0), powers: int32 = int32(-1)) -> int32:
    mod: int32 = xs_array_get_int(powers, i + 1)
    b: int32 = (x % mod) // xs_array_get_int(powers, i)
    if b < 0:
        b += 2
    return b


def _xs_set_bit(bit: int32 = int32(0), i: int32 = int32(0), powers: int32 = int32(-1)) -> int32:
    return bit * xs_array_get_int(powers, i)


def xs_bit_and(a: int32 = int32(0), b: int32 = int32(0)) -> int32:
    global _c_bit_operator_int_min_value
    powers: int32 = _xs_bit_operator_get_powers()
    res: int32 = int32(0)
    for i in range(0, 31):
        abit: int32 = _xs_get_bit(a, i, powers)
        bbit: int32 = _xs_get_bit(b, i, powers)
        bit: int32 = abit * bbit
        res += _xs_set_bit(bit, i, powers)
    if a < 0 and b < 0:
        if _c_bit_operator_int_min_value == -1:
            _c_bit_operator_int_min_value = int32(-2147483648)
        res += _c_bit_operator_int_min_value
    return res


def xs_bit_xor(a: int32 = int32(0), b: int32 = int32(0)) -> int32:
    global _c_bit_operator_int_min_value
    powers: int32 = _xs_bit_operator_get_powers()
    res: int32 = int32(0)
    for i in range(0, 31):
        abit: int32 = _xs_get_bit(a, i, powers)
        bbit: int32 = _xs_get_bit(b, i, powers)
        bit: int32 = (abit + bbit) % 2
        res += _xs_set_bit(bit, i, powers)
    if (a < 0 and b >= 0) or (a >= 0 and b < 0):
        if _c_bit_operator_int_min_value == -1:
            _c_bit_operator_int_min_value = int32(-2147483648)
        res += _c_bit_operator_int_min_value
    return res


def xs_bit_or(a: int32 = int32(0), b: int32 = int32(0)) -> int32:
    global _c_bit_operator_int_min_value
    powers: int32 = _xs_bit_operator_get_powers()
    res: int32 = int32(0)
    for i in range(0, 31):
        abit: int32 = _xs_get_bit(a, i, powers)
        bbit: int32 = _xs_get_bit(b, i, powers)
        bit: int32 = abit + bbit - abit * bbit
        res += _xs_set_bit(bit, i, powers)
    if a < 0 or b < 0:
        if _c_bit_operator_int_min_value == -1:
            _c_bit_operator_int_min_value = int32(-2147483648)
        res += _c_bit_operator_int_min_value
    return res


def xs_mersenne_twister_seed(seed: int32 = int32(0)) -> None:
    global _mt_state_array, _c_mt_matrix_a, _c_mt_upper_mask, _c_mt_lower_mask, _c_mt_a, _c_mt_b, _c_mt_f, _mt_state_index, _mt_seed_set
    if _mt_state_array < 0:
        _c_mt_matrix_a = int32(-1727483681)
        _c_mt_upper_mask = int32(-2147483648)
        _c_mt_lower_mask = int32(2147483647)
        _c_mt_a = int32(-1727483681)
        _c_mt_b = int32(-1658038656)
        _c_mt_f = int32(1812433253)
        _mt_state_array = int32(xs_array_create_int(_c_mt_n, 0))
    xs_array_set_int(_mt_state_array, 0, seed)
    i: int32 = int32(1)
    while i < _c_mt_n:
        seed = _c_mt_f * xs_bit_xor(seed, xs_bit_shift_right_logical(seed, (_c_mt_w - 2))) + i
        xs_array_set_int(_mt_state_array, i, seed)
        i += 1
    _mt_state_index = int32(0)
    _mt_seed_set = True


def xs_mersenne_twister_random() -> int32:
    global _mt_state_index, _mt_state_index

    if not _mt_seed_set:
        xs_mersenne_twister_seed(xs_get_random_number() * 65536 + xs_get_random_number())

    k: int32 = _mt_state_index

    j: int32 = k - (_c_mt_n - 1)
    if j < 0:
        j += _c_mt_n

    x: int32 = xs_bit_or(
        xs_bit_and(xs_array_get_int(_mt_state_array, k), _c_mt_upper_mask),
        xs_bit_and(xs_array_get_int(_mt_state_array, j), _c_mt_lower_mask),
    )

    xa: int32 = xs_bit_shift_right_logical(x, int32(1))
    if (xs_bit_and(x, int32(1)) != 0):
        xa = xs_bit_xor(xa, _c_mt_a)

    j = k - (_c_mt_n - _c_mt_m)
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
    z: int32 = xs_bit_xor(y, xs_bit_shift_right_logical(y, _c_mt_l))

    return z


def xs_mersenne_twister_random_uniform_range(start: int32 = int32(0), end: int32 = int32(999999999)) -> int32:
    global _c_bit_operator_int_min_value
    range: int32 = end - start
    if range <= 0:
        return int32(-1)

    if xs_bit_and(range, (range - 1)) == 0:
        return start + xs_bit_and(xs_mersenne_twister_random(), (range - 1))

    threshold: int32 = (-1 * range) % range

    if _c_bit_operator_int_min_value == -1:
        _c_bit_operator_int_min_value = int32(-2147483648)

    while True:
        r: int32 = xs_mersenne_twister_random()
        unsigned_r: int32 = r + _c_bit_operator_int_min_value
        if unsigned_r >= threshold:
            result: int32 = unsigned_r % range
            return start + result


def functions(include_test: bool = False) -> (str, str):
    constants_function_xs = PythonToXsConverter.to_xs_script(
        constants,
        indent=True,
    )
    constants_xs = (constants_function_xs[constants_function_xs.find("int"):constants_function_xs.rfind("}")]
                    .strip()
                    .replace("    ", "")
                    ) + "\n\n"
    xs = constants_xs + PythonToXsConverter.to_xs_script(
        _xs_bit_operator_get_powers,
        _xs_get_bit,
        _xs_set_bit,
        xs_bit_shift_left,
        xs_bit_shift_right_logical,
        xs_bit_shift_right_arithmetic,
        xs_bit_not,
        xs_bit_and,
        xs_bit_or,
        xs_bit_xor,
        xs_mersenne_twister_seed,
        xs_mersenne_twister_random,
        xs_mersenne_twister_random_uniform_range,
        indent=True,
    )
    print(xs)
    return (xs, "functions")


if __name__ == '__main__':
    functions()
