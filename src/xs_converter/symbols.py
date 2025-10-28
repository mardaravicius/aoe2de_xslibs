import dataclasses
from typing import _SpecialForm, Optional

from numpy import float32, arange, int32


@dataclasses.dataclass
class XsVector:
    x: float32
    y: float32
    z: float32


@_SpecialForm
def XsStatic(self):
    pass


@_SpecialForm
def XsConst(self):
    pass


@_SpecialForm
def XsExtern(self):
    pass


@_SpecialForm
def XsExternConst(self):
    pass


def xs_rule(group: str = None, active: bool = False, high_frequency: bool = False, run_immediately: bool = False,
            min_interval: Optional[int] = None, max_interval: Optional[int] = None, priority: Optional[int] = None):
    def xs_rule_inner(function):
        return function

    return xs_rule_inner


def i32range(start =  None, *args, **kwargs):
    return arange(start, *args, **kwargs, dtype=int32)

def f32range(start =  None, *args, **kwargs):
    return arange(start, *args, **kwargs, dtype=float32)
