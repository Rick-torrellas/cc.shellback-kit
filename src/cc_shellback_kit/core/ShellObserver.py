from abc import ABC
from typing import Any

from .CommandResult import CommandResult


class ShellObserver(ABC):  # Can inherit from ABC if you want to mark it as a base class
    """
    Base interface for observing Shell lifecycle events.

    This class acts as a 'toolbox' of hooks. Methods have empty default
    implementations to allow child classes to override only the specific
    events they are interested in capturing.
    """

    def on_session_start(self, shell_name: str):
        """
        Triggered when entering the Shell context ('with' block).
        Useful for initializing logging resources or telemetry.
        """
        pass

    def on_session_end(self, shell_name: str, error: Exception = None):
        """
        Triggered when exiting the Shell context.
        Allows logging whether the session ended cleanly or due to an exception.
        """
        pass

    def on_context_change(self, key: str, value: Any):
        """
        Triggered when a state command (Virtual Builtin) mutates the context.
        Example: changes in the CWD (Working Directory) or environment variables.
        """
        pass

    def on_command_start(self, executable: str, final_args: list[str]):
        """
        Triggered just before sending an effect command to the operating system.
        Provides the final arguments exactly as they will be executed by the adapter.
        """
        pass

    def on_command_result(self, result: "CommandResult"):
        """
        Triggered after receiving the response from an effect command.
        Allows reacting to the return code, stdout, and stderr.
        """
        pass

    def on_error(self, message: str, error: Exception = None):
        """
        Triggered when a controlled or unexpected error occurs within the Core.
        Acts as an error sink to keep business logic clean.
        """
        pass
