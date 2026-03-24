import os

g: int = 99


def foo(x: int = 0) -> None:
    y: int = x + g
