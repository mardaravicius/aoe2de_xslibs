from xs_converter.constants import XsConstants
from xs_converter.converter import PythonToXsConverter
from xs_converter.functions import vector, xs_set_player_attribute, xs_player_attribute, xs_get_game_time, \
    xs_effect_amount, xs_get_player_civilization
from xs_converter.macro import macro_pass_value, macro_repeat_with_iterable
from xs_converter.symbols import XsConst, XsStatic, XsVector, xs_rule


def xs_test_function() -> None:
    c_integer_var: XsConst[int] = 123
    static_integer_var: XsStatic[int] = 123
    float_var: float = 2.2 * 12.45 + 1.1
    ff: float = float_var
    string_var: str = "hello xs" + "asd"
    bool_var: bool = True
    vec: XsVector = vector(1.1, 2.2, 3.3)
    resource_1: int = macro_pass_value("resource1", int)
    resource_2: int = 411
    long_int: int = -2_147_483_648
    s: str = f"{long_int=}, {ff=}, {bool_var=}, {string_var=}, {vec=}"

    with macro_repeat_with_iterable("players", tuple[int, int]) as (player_number, res):
        xs_set_player_attribute(player_number, resource_2, res)

    xs_set_player_attribute(1, resource_1, xs_player_attribute(1, resource_1) + 1.0)

    if 0 < xs_get_game_time():
        return
    if xs_player_attribute(2, resource_2) > 10:
        xs_set_player_attribute(2, resource_2, 10.0)
    elif xs_player_attribute(2, resource_2) == 0:
        xs_set_player_attribute(2, resource_2, 1.0)
    else:
        pass

    for p in range(3, 9):
        xs_effect_amount(0, 1, 2, 40.0, p)

    to: int = 2
    for p2 in range(9, to - 1, -2):
        xs_effect_amount(0, 1, 2, 40.0, p2)

    while xs_get_game_time() > 1000:
        xs_set_player_attribute(3, 422, xs_player_attribute(3, 422) + 10.0)

    match xs_get_player_civilization(4):
        case 1:
            return
        case XsConstants.c_britons:
            xs_effect_amount(XsConstants.c_set_attribute, 101, XsConstants.c_attack, 123.0, 4)
        case _:
            xs_effect_amount(XsConstants.c_set_attribute, 101, XsConstants.c_attack, 456.0, 4)

    so: int = 3


@xs_rule(active=True, high_frequency=False, priority=21, min_interval=1, max_interval=2)
def xs_test_rule() -> None:
    xs_set_player_attribute(1, 20, 33.3)


def main():
    print(PythonToXsConverter.to_xs_script(xs_test_function, xs_test_rule, indent=True, resource1=400,
                                           players=[(1, 40.0), (2, 41.0), (3, 42.0), (5, 43.0), (8, 44.0)]))


if __name__ == '__main__':
    main()
