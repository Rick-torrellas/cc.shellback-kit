from abc import ABC
from typing import Any

from .CommandResult import CommandResult


class ShellObserver(ABC):  # Puede heredar de ABC si quieres marcarla como base
    """
    Interfaz base para la observación de eventos del ciclo de vida de la Shell.

    Esta clase actúa como una 'caja de herramientas' de hooks. Los métodos
    tienen una implementación vacía por defecto para permitir que las
    clases hijas solo sobrescriban los eventos que les interesa capturar.
    """

    def on_session_start(self, shell_name: str):
        """
        Se dispara al entrar en el contexto de la Shell (bloque 'with').
        Útil para inicializar recursos de logging o telemetría.
        """
        pass

    def on_session_end(self, shell_name: str, error: Exception = None):
        """
        Se dispara al salir del contexto de la Shell.
        Permite registrar si la sesión terminó de forma limpia o por una excepción.
        """
        pass

    def on_context_change(self, key: str, value: Any):
        """
        Se dispara cuando un comando de estado (Virtual Builtin) muta el contexto.
        Ejemplo: cambios en el CWD (Directorio de trabajo) o variables de entorno.
        """
        pass

    def on_command_start(self, executable: str, final_args: list[str]):
        """
        Se dispara justo antes de enviar un comando de efecto al sistema operativo.
        Proporciona los argumentos finales tal cual serán ejecutados por el adaptador.
        """
        pass

    def on_command_result(self, result: "CommandResult"):
        """
        Se dispara tras recibir la respuesta de un comando de efecto.
        Permite reaccionar al código de retorno, stdout y stderr.
        """
        pass

    def on_error(self, message: str, error: Exception = None):
        """
        Se dispara cuando ocurre un error controlado o inesperado dentro del Core.
        Funciona como un sumidero de errores para evitar que la lógica de negocio se ensucie.
        """
        pass
