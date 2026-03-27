from typing import Optional


class XsConversionError(Exception):
    def __init__(
            self,
            message: str,
            *,
            source_name: Optional[str] = None,
            line: Optional[int] = None,
            column: Optional[int] = None,
            source_line: Optional[str] = None,
            end_column: Optional[int] = None,
    ):
        super().__init__(message)
        self.message = message
        self.source_name = source_name
        self.line = line
        self.column = column
        self.source_line = source_line
        self.end_column = end_column

    def __str__(self) -> str:
        parts = [self.message]
        if self.source_name is not None or self.line is not None or self.column is not None:
            location = self.source_name or "<python>"
            if self.line is not None:
                location += f":{self.line}"
                if self.column is not None:
                    location += f":{self.column}"
            parts.append(f"Location: {location}")
        if self.source_line is not None:
            parts.append(self.source_line)
            caret_column = max((self.column or 1) - 1, 0)
            caret_width = 1
            if self.column is not None and self.end_column is not None and self.end_column > self.column:
                caret_width = self.end_column - self.column
            parts.append(f"{' ' * caret_column}{'^' * caret_width}")
        return "\n".join(parts)
