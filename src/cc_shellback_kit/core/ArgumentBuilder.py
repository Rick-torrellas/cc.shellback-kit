from typing import Any, List


class ArgumentBuilder:
    """Garantiza la consistencia de los argumentos para el Sistema Operativo."""

    def __init__(self, style: str = "unix"):
        self._args: List[str] = []
        self.style = style

    def add_arg(self, value: Any) -> "ArgumentBuilder":
        """Aplana listas/tuplas y convierte todo a string, ignorando vacíos."""
        if isinstance(value, (list, tuple)):
            for item in value:
                self.add_arg(item)
        elif value is not None:
            val_str = str(value).strip()
            if val_str:
                self._args.append(val_str)
        return self

    def add_flag(self, name: str, value: Any = None) -> "ArgumentBuilder":
        prefix = "--" if self.style == "unix" else "/"
        clean_name = name.strip().replace(" ", "_")
        self.add_arg(f"{prefix}{clean_name}")
        if value is not None:
            self.add_arg(value)
        return self

    def build(self) -> List[str]:
        return self._args
