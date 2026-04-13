from dataclasses import dataclass, field
import json
from typing import Any


@dataclass
class CommandResult:
    """Encapsulates the output of an executed command."""

    # Captured output from the command's stdout
    standard_output: str = ""
    # Captured error messages from the command's stderr
    standard_error: str = ""
    # The exit status code (0 usually indicates success)
    return_code: int = 0
    # Total duration of the command execution in seconds
    execution_time: float = 0.0
    # The original command arguments sent for execution
    command_sent: list[str] = field(default_factory=list)

    def is_success(self) -> bool:
        """Returns True if the command executed successfully."""
        # Checks if the return code is exactly 0
        return self.return_code == 0

    def json(self) -> Any:
        """Parses the standard output as JSON."""
        # Converts the raw string output into a Python dictionary or list
        return json.loads(self.standard_output)

    def __or__(self, next_command: Any) -> str:
        """Enables pipe syntax."""
        # Allows the use of the '|' operator to pass output to another process
        return self.standard_output
