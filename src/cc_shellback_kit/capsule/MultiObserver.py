from typing import List, Any
from ..core import ShellObserver, CommandResult


class MultiObserver(ShellObserver):
    """
    Patrón Composite: Permite registrar múltiples observadores y
    notificar a todos ellos de cada evento de la Shell.
    """

    def __init__(self, observers: List[ShellObserver] = None):
        self.observers = observers or []

    def add_observer(self, observer: ShellObserver):
        self.observers.append(observer)

    def on_session_start(self, shell_name: str):
        for o in self.observers:
            o.on_session_start(shell_name)

    def on_session_end(self, shell_name: str, error: Exception = None):
        for o in self.observers:
            o.on_session_end(shell_name, error)

    def on_context_change(self, key: str, value: Any):
        for o in self.observers:
            o.on_context_change(key, value)

    def on_command_start(self, executable: str, final_args: List[str]):
        for o in self.observers:
            o.on_command_start(executable, final_args)

    def on_command_result(self, result: CommandResult):
        for o in self.observers:
            o.on_command_result(result)

    def on_error(self, message: str, error: Exception = None):
        for o in self.observers:
            o.on_error(message, error)
