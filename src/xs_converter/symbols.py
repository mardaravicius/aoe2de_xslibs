import dataclasses
from typing import _SpecialForm, Optional


@dataclasses.dataclass
class XsVector:
    x: float
    y: float
    z: float


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
