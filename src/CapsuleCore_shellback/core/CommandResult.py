from dataclasses import dataclass, field
import json
from typing import Any

@dataclass
class CommandResult:
    """Encapsulates the output of an executed command."""
    standard_output: str = ""
    standard_error: str = ""
    return_code: int = 0
    execution_time: float = 0.0
    command_sent: list[str] = field(default_factory=list)

    def is_success(self) -> bool:
        """Returns True if the command executed successfully."""
        return self.return_code == 0

    def json(self) -> Any:
        """Parses the standard output as JSON."""
        return json.loads(self.standard_output)
    
    def __or__(self, next_command: Any) -> str:
        """Enables pipe syntax."""
        return self.standard_output