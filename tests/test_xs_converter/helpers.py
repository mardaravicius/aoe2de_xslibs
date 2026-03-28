import re
import subprocess
import tempfile
import types

from xs_converter.converter import PythonToXsConverter


_xs_check_tmpfile = tempfile.NamedTemporaryFile(mode="w", suffix=".xs", delete=False)
_xs_check_tmpfile.close()
_generated_name_re = re.compile(r"\b(?P<prefix>temp|header)[0-9a-f]{8}\b")


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


def _normalize_generated_names(xs: str) -> str:
    mapping = {}
    next_index = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal next_index
        name = match.group(0)
        if name not in mapping:
            mapping[name] = f"{match.group('prefix')}{next_index:08x}"
            next_index += 1
        return mapping[name]

    return _generated_name_re.sub(repl, xs)


def convert_file_raw(module, indent=True, **kwargs) -> str:
    xs = PythonToXsConverter.to_xs_file(module, indent=indent, **kwargs)
    _xs_check(xs)
    return xs


def convert_file(module, indent=True, **kwargs) -> str:
    return _normalize_generated_names(convert_file_raw(module, indent=indent, **kwargs))


def module_from_source(source: str) -> types.ModuleType:
    """Create a module whose inspect.getsource returns the given source."""
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False)
    f.write(source)
    f.close()
    mod = types.ModuleType("_fake")
    mod.__file__ = f.name
    return mod


def convert_raw(*functions, indent=True, **kwargs) -> str:
    """Convert one or more Python functions to XS script and validate with xs-check."""
    xs = PythonToXsConverter.to_xs_script(*functions, indent=indent, **kwargs)
    _xs_check(xs)
    return xs


def convert(*functions, indent=True, **kwargs) -> str:
    return _normalize_generated_names(convert_raw(*functions, indent=indent, **kwargs))


def convert_for_script_call_raw(function, indent=True, suffix=None, **kwargs) -> str:
    """Convert a single Python function to XS script-for-script-call output and validate with xs-check."""
    xs = PythonToXsConverter.to_xs_script_for_script_call(
        function,
        indent=indent,
        suffix=suffix,
        **kwargs,
    )
    _xs_check(xs)
    return xs


def convert_for_script_call(function, indent=True, suffix=None, **kwargs) -> str:
    return _normalize_generated_names(
        convert_for_script_call_raw(function, indent=indent, suffix=suffix, **kwargs),
    )


def extract_script_call_library_name(xs: str) -> str:
    match = re.match(r"^void (header[0-9a-f]{8})\(\)", xs)
    if match is None:
        raise AssertionError(f"Could not find script call library prelude in:\n{xs}")
    return match.group(1)


def extract_generated_names(xs: str) -> list[str]:
    names = []
    seen = set()
    for match in _generated_name_re.finditer(xs):
        name = match.group(0)
        if name in seen:
            continue
        seen.add(name)
        names.append(name)
    return names
