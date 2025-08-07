from typing import Generic, TypeVar, Type

T = TypeVar('T')


class RepeatMacro(Generic[T]):
    def __enter__(self) -> T:
        pass

    def __exit__(self, exception_type, exception_value, exception_traceback):
        pass


def macro_pass_value(variable_name: str, t: Type[T]) -> T:
    pass


def macro_repeat_with_iterable(iterable: str, t: Type[T]) -> RepeatMacro[T]:
    pass
