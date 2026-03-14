from typing import Any, Optional

class ArgumentBuilder:
    def __init__(self, style: str = "unix"):
        self._args = []
        self.style = style # "unix" para --flag o "ms" para /flag

    def add_flag(self, name: str, value: Optional[Any] = None):
        prefix = "--" if self.style == "unix" else "/"
        if value is None:
            self._args.append(f"{prefix}{name}")
        else:
            self._args.extend([f"{prefix}{name}", str(value)])
        return self
        
    def build(self) -> list[str]:
        return self._args