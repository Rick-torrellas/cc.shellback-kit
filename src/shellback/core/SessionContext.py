from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

@dataclass(frozen=True)
class SessionContext:
    """Mantiene el estado persistente entre ejecuciones de la Shell."""
    cwd: Path = field(default_factory=Path.cwd)
    env: Dict[str, str] = field(default_factory=dict)
    encoding: str = "utf-8"