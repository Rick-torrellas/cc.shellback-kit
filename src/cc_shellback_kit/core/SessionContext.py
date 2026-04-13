from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict


@dataclass(frozen=True)
class SessionContext:
    """Maintains persistent state across Shell executions."""

    # The current working directory, defaults to the system's current path
    cwd: Path = field(default_factory=Path.cwd)

    # A dictionary to store environment variables for the session
    env: Dict[str, str] = field(default_factory=dict)

    # Character encoding for the session, defaults to UTF-8
    encoding: str = "utf-8"
