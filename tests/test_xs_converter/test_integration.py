import unittest

from xs_converter.constants import XsConstants
from xs_converter.functions import (
    xs_set_player_attribute,
    xs_player_attribute,
    xs_get_game_time,
    xs_effect_amount,
    xs_get_player_civilization,
    xs_chat_data,
)
from xs_converter.macro import macro_pass_value, macro_repeat_with_iterable
from xs_converter.symbols import XsConst, XsStatic, XsVector

from tests.test_xs_converter.helpers import _convert
from xs_converter.functions import vector


class IntegrationTest(unittest.TestCase):
    def test_full_function_converts(self):
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

        expected = (
            "void xsTestFunction() {\n"
            "    const int cIntegerVar = 123;\n"
            "    static int staticIntegerVar = 123;\n"
            "    float floatVar = (2.2 * 12.45) + 1.1;\n"
            "    float ff = floatVar;\n"
            '    string stringVar = "hello xs" + "asd";\n'
            "    bool boolVar = true;\n"
            "    vector vec = vector(1.1, 2.2, 3.3);\n"
            "    int resource1 = 400;\n"
            "    int resource2 = 411;\n"
            "    int longInt = -214748364 * 10 - 8;\n"
            '    string s = ("long_int=" + longInt + ", ff=" + ff + ", bool_var=" + boolVar + ", string_var=" + stringVar + ", vec=" + vec);\n'
            "    xsSetPlayerAttribute(1, resource2, 40.0);\n"
            "    xsSetPlayerAttribute(2, resource2, 41.0);\n"
            "    xsSetPlayerAttribute(3, resource2, 42.0);\n"
            "    xsSetPlayerAttribute(5, resource2, 43.0);\n"
            "    xsSetPlayerAttribute(8, resource2, 44.0);\n"
            "    xsSetPlayerAttribute(1, resource1, xsPlayerAttribute(1, resource1) + 1.0);\n"
            "    if (0 < xsGetGameTime()) {\n"
            "        return;\n"
            "    }\n"
            "    if (xsPlayerAttribute(2, resource2) > 10) {\n"
            "        xsSetPlayerAttribute(2, resource2, 10.0);\n"
            "    } else if (xsPlayerAttribute(2, resource2) == 0) {\n"
            "        xsSetPlayerAttribute(2, resource2, 1.0);\n"
            "    } else {\n"
            "    }\n"
            "    for (p = 3; < 9) {\n"
            "        xsEffectAmount(0, 1, 2, 40.0, p);\n"
            "    }\n"
            "    int to = 2;\n"
            "    int p2 = 9;\n"
            "    while (p2 >= to) {\n"
            "        xsEffectAmount(0, 1, 2, 40.0, p2);\n"
            "        p2 = p2 - 2;\n"
            "    }\n"
            "    while (xsGetGameTime() > 1000) {\n"
            "        xsSetPlayerAttribute(3, 422, xsPlayerAttribute(3, 422) + 10.0);\n"
            "    }\n"
            "    switch (xsGetPlayerCivilization(4)) {\n"
            "        case 1: {\n"
            "            return;\n"
            "        }\n"
            "        case cBritons: {\n"
            "            xsEffectAmount(cSetAttribute, 101, cAttack, 123.0, 4);\n"
            "        }\n"
            "        default: {\n"
            "            xsEffectAmount(cSetAttribute, 101, cAttack, 456.0, 4);\n"
            "        }\n"
            "    }\n"
            "    int so = 3;\n"
            "}\n"
        )
        self.assertEqual(
            expected,
            _convert(
                xs_test_function,
                resource1=400,
                players=[(1, 40.0), (2, 41.0), (3, 42.0), (5, 43.0), (8, 44.0)],
            ),
        )


if __name__ == "__main__":
    unittest.main()
