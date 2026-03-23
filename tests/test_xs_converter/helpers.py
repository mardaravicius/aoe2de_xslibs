import ast
import inspect
import subprocess
import tempfile
import textwrap

from xs_converter.converter import PythonToXsConverter, XsContext


def _parse_dedented(fn):
    source = textwrap.dedent(inspect.getsource(fn))
    module = ast.parse(source)
    assert len(module.body) == 1 and isinstance(module.body[0], ast.FunctionDef)
    return module.body[0]


_xs_check_tmpfile = tempfile.NamedTemporaryFile(mode="w", suffix=".xs", delete=False)
_xs_check_tmpfile.close()


def _xs_check(xs: str) -> None:
    """Validate XS source with xs-check. Raises AssertionError on failure."""
    with open(_xs_check_tmpfile.name, "w") as f:
        f.write(xs)
    result = subprocess.run(
        ["xs-check", _xs_check_tmpfile.name, "--ignores", "DiscardedFn"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(f"xs-check failed:\n{result.stdout}{result.stderr}")


def _convert(*functions, indent=True, root_flags=None, **kwargs) -> str:
    """Convert one or more Python functions to XS script and validate with xs-check.

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
    _xs_check(xs)
    return xs
