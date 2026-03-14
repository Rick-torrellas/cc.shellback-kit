from dataclasses import dataclass
from typing import Any
import json


@dataclass
class CommandResult:
    """Encapsulates the output of an executed command."""
    standand_output: str
    standand_error: str
    return_code: int
    execution_time: float
    command_sent: list[str]

    def is_success(self) -> bool:
        """Returns True if the command executed successfully (return code 0)."""
        return self.return_code == 0

    def json(self) -> Any:
        """Parses the standard output as JSON and returns the deserialized object."""
        return json.loads(self.standand_output)
    
    def __or__(self, next_command):
        """Enables pipe syntax (sh.run(cmd1) | sh.run(cmd2)) for chaining command results by returning the standard output."""
        return self.standand_output