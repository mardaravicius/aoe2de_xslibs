from collections.abc import Iterable, Iterator, Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

_MACRO_BINDINGS: ContextVar[dict[str, Any]] = ContextVar("_MACRO_BINDINGS", default={})


@contextmanager
def macro_bindings(bindings: Mapping[str, Any] | None = None, /, **kwargs: Any) -> Iterator[None]:
    merged = dict(_MACRO_BINDINGS.get())
    if bindings is not None:
        merged.update(bindings)
    merged.update(kwargs)
    token = _MACRO_BINDINGS.set(merged)
    try:
        yield
    finally:
        _MACRO_BINDINGS.reset(token)

def macro_pass_value(variable_name: str) -> Any:
    return _evaluate_macro_reference(variable_name, _MACRO_BINDINGS.get())


def macro_repeat(variable_name: str) -> Iterable[Any]:
    value = _evaluate_macro_reference(variable_name, _MACRO_BINDINGS.get())
    if not isinstance(value, Iterable):
        raise TypeError(
            f"macro_repeat reference {variable_name!r} resolved to {value!r} "
            f"({type(value).__name__}), expected an iterable."
        )
    return value


def _evaluate_macro_reference(reference: str, bindings: Mapping[str, Any]) -> Any:
    try:
        return bindings[reference]
    except KeyError as exc:
        raise KeyError(f"Macro reference {reference!r} is not bound in the current macro_bindings scope.") from exc
