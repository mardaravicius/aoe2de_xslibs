from dataclasses import dataclass, field


@dataclass(frozen=True)
class XsContext:
    depth: int = 0
    replacements: dict[str, str] = field(default_factory=dict)

    def indented(self) -> "XsContext":
        return XsContext(self.depth + 1, self.replacements)

    def with_replacements(self, replacements: dict[str, str]) -> "XsContext":
        return XsContext(self.depth, replacements)
