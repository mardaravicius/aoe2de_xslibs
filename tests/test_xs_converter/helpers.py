import subprocess
import tempfile
import types

from xs_converter.converter import PythonToXsConverter


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


def convert_file(module, indent=True, **kwargs) -> str:
    xs = PythonToXsConverter.to_xs_file(module, indent=indent, **kwargs)
    _xs_check(xs)
    return xs


def module_from_source(source: str) -> types.ModuleType:
    """Create a module whose inspect.getsource returns the given source."""
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False)
    f.write(source)
    f.close()
    mod = types.ModuleType("_fake")
    mod.__file__ = f.name
    return mod


def convert(*functions, indent=True, **kwargs) -> str:
    """Convert one or more Python functions to XS script and validate with xs-check."""
    xs = PythonToXsConverter.to_xs_script(*functions, indent=indent, **kwargs)
    _xs_check(xs)
    return xs
