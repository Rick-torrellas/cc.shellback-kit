from typing import List, Any
from ..core import ShellObserver, CommandResult


class MultiObserver(ShellObserver):
    """
    Composite Pattern: Allows registering multiple observers and
    notifying all of them of each Shell event.
    """

    def __init__(self, observers: List[ShellObserver] = None):
        self.observers = observers or []

    def add_observer(self, observer: ShellObserver):
        # Adds a new observer to the list
        self.observers.append(observer)

    def on_session_start(self, shell_name: str):
        # Notifies all observers that the session has started
        for o in self.observers:
            o.on_session_start(shell_name)

    def on_session_end(self, shell_name: str, error: Exception = None):
        # Notifies all observers that the session has ended
        for o in self.observers:
            o.on_session_end(shell_name, error)

    def on_context_change(self, key: str, value: Any):
        # Notifies all observers of a context change
        for o in self.observers:
            o.on_context_change(key, value)

    def on_command_start(self, executable: str, final_args: List[str]):
        # Notifies all observers that a command is starting execution
        for o in self.observers:
            o.on_command_start(executable, final_args)

    def on_command_result(self, result: CommandResult):
        # Notifies all observers of the command execution result
        for o in self.observers:
            o.on_command_result(result)

    def on_error(self, message: str, error: Exception = None):
        # Notifies all observers when an error occurs
        for o in self.observers:
            o.on_error(message, error)
