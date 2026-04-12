import logging
from pathlib import Path
from ..core import ShellObserver, CommandResult


class FileLogObserver(ShellObserver):
    """Guarda toda la actividad de la Shell en un archivo físico."""

    def __init__(self, log_path: str = "shell_activity.log"):
            self.log_path = Path(log_path)

            self.logger = logging.getLogger("ShellFileLogger")
            self.logger.setLevel(logging.INFO)
            self.logger.propagate = False  # Evita que los logs salgan por consola en los tests

            if self.logger.handlers:
                for h in self.logger.handlers[:]:
                    h.close()
                    self.logger.removeHandler(h)

            # Ahora creamos el nuevo handler con la ruta correcta
            handler = logging.FileHandler(self.log_path, encoding="utf-8")
            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            handler.setFormatter(formatter) 
            self.logger.addHandler(handler)

    def on_session_start(self, shell_name: str):
        self.logger.info(f"=== INICIO DE SESIÓN: {shell_name} ===")

    def on_session_end(self, shell_name: str, error: Exception = None):
        if error:
            self.logger.error(f"=== FIN DE SESIÓN CON ERROR: {error} ===")
        else:
            self.logger.info("=== FIN DE SESIÓN EXITOSO ===")

    def on_command_start(self, executable: str, final_args: list[str]):
        cmd_str = " ".join(final_args)
        self.logger.info(f"EJECUTANDO: {cmd_str}")

    def on_command_result(self, result: CommandResult):
        status = "SUCCESS" if result.is_success() else f"FAILED({result.return_code})"
        self.logger.info(
            f"RESULTADO: {status} | "
            f"DURACIÓN: {result.execution_time:.4f}s | "
            f"STDOUT: {result.standard_output.strip()[:100]}..."
        )

    def on_error(self, message: str, error: Exception = None):
        self.logger.error(f"ERROR DEL SISTEMA: {message} | Detalle: {error}")
