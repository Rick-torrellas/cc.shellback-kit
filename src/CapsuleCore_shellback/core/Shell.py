from abc import ABC, abstractmethod
import shutil
import time
import subprocess
from typing import Optional, Dict, Callable
from .SessionContext import SessionContext
from .CommandResult import CommandResult
from .ShellObserver import ShellObserver


class CommandNotFoundError(Exception):
    """Lanzada cuando el binario no existe en el PATH."""

    pass


class Shell(ABC):
    def __init__(
        self,
        context: Optional[SessionContext] = None,
        observer: Optional[ShellObserver] = None,
        default_timeout: float = 30.0,
    ):
        self.context = context or SessionContext()
        self.observer = observer or ShellObserver()
        self.default_timeout = default_timeout

        # Mapa de comandos virtuales (de estado)
        self._virtual_builtins: Dict[str, Callable] = {
            "cd": self._handle_cd,
            "export": self._handle_export,
        }

    @abstractmethod
    def _format_command(self, executable: str, args: list[str]) -> list[str]:
        """Cada shell hija decide la sintaxis técnica."""
        pass

    def run(self, command, timeout: Optional[float] = None) -> CommandResult:
        """Dispatcher principal: decide si el comando es de Estado o de Efecto."""
        executable = command.executable

        # 1. ¿Es un comando de Estado (Virtual)?
        if executable in self._virtual_builtins:
            return self._virtual_builtins[executable](command)

        # 2. Es un comando de Efecto (Real)
        return self._run_external(command, timeout)

    # --- Manejadores de Estado (Comandos Virtuales) ---

    def _handle_cd(self, command) -> CommandResult:
        try:
            path_str = command.args[0] if command.args else "~"
            # Resolver ruta (simplificado, asumiendo pathlib)
            new_path = (self.context.cwd / path_str).resolve()

            if not new_path.exists() or not new_path.is_dir():
                raise FileNotFoundError(f"Directorio no encontrado: {new_path}")

            # Mutación del contexto (creando nueva instancia por ser frozen)
            self.context = SessionContext(
                cwd=new_path, env=self.context.env, encoding=self.context.encoding
            )

            self.observer.on_context_change("cwd", new_path)
            return CommandResult(standard_output=f"CWD: {new_path}", return_code=0)

        except Exception as e:
            self.observer.on_error("Error en comando virtual cd", e)
            return CommandResult(standard_error=str(e), return_code=1)

    def _handle_export(self, command) -> CommandResult:
        # Ejemplo: export KEY=VALUE
        try:
            for arg in command.args:
                key, value = arg.split("=", 1)
                new_env = {**self.context.env, key: value}
                self.context = SessionContext(cwd=self.context.cwd, env=new_env)
                self.observer.on_context_change(f"env.{key}", value)

            return CommandResult(return_code=0)
        except Exception as e:
            return CommandResult(standard_error=f"Export fallido: {e}", return_code=1)

    # --- Manejador de Efecto (Comandos Reales) ---

    def _run_external(self, command, timeout) -> CommandResult:
        executable = command.executable
        if not shutil.which(executable):
            msg = f"Comando no encontrado: {executable}"
            self.observer.on_error(msg)
            return CommandResult(standard_error=msg, return_code=127)

        final_args = self._format_command(executable, command.args)
        self.observer.on_command_start(executable, final_args)

        start_time = time.perf_counter()
        try:
            process = subprocess.run(
                final_args,
                cwd=self.context.cwd,
                env={**self.context.env},
                capture_output=True,
                text=True,
                encoding=self.context.encoding,
                timeout=timeout or self.default_timeout,
            )

            result = CommandResult(
                standard_output=process.stdout,
                standard_error=process.stderr,
                return_code=process.returncode,
                execution_time=time.perf_counter() - start_time,
                command_sent=final_args,
            )
            self.observer.on_command_result(result)
            return result
        except Exception as e:
            self.observer.on_error("Error de ejecución externa", e)
            raise e
