from xs_converter.symbols import xs_ignore


def converted() -> None:
    x: int = 1


@xs_ignore
def skipped() -> None:
    x: int = 2


def also_converted() -> int:
    return 42
