import ast
import inspect
import textwrap
import unittest

from xs_converter.constants import XsConstants
from xs_converter.converter import PythonToXsConverter, XsContext
from xs_converter.functions import (
    vector,
    xs_set_player_attribute,
    xs_player_attribute,
    xs_get_game_time,
    xs_effect_amount,
    xs_get_player_civilization,
    xs_chat_data,
    xs_array_get_int,
)
from xs_converter.macro import macro_pass_value, macro_repeat_with_iterable
from xs_converter.symbols import XsConst, XsStatic, XsExtern, XsExternConst, XsVector, xs_rule
from numpy import int32, float32
from typing import List, cast


def _parse_dedented(fn):
    source = textwrap.dedent(inspect.getsource(fn))
    module = ast.parse(source)
    assert len(module.body) == 1 and isinstance(module.body[0], ast.FunctionDef)
    return module.body[0]


def _convert(*functions, indent=True, root_flags=None, **kwargs) -> str:
    """Convert one or more Python functions to XS script.

    By default the first function is treated as root (matching to_xs_script
    behaviour).  Override per-function with ``root_flags``.
    """
    xs = ""
    for i, fn in enumerate(functions):
        root = (i == 0) if root_flags is None else root_flags[i]
        converter = PythonToXsConverter(indent, kwargs)
        fn_ast = _parse_dedented(fn)
        xs += converter.to_xs_function_definition(fn_ast, XsContext(), root)
        if i < len(functions) - 1:
            xs += converter.nl
    return xs
