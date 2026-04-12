from abc import ABC, abstractmethod
import shutil
import time
import subprocess
from pathlib import Path
from dataclasses import replace
from typing import Optional, Dict, Callable

# Importaciones del Core
from .SessionContext import SessionContext
from .CommandResult import CommandResult
from .ShellObserver import ShellObserver
from .ArgumentBuilder import ArgumentBuilder


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

        # Mapa de comandos virtuales (Manejo de Estado)
        self._virtual_builtins: Dict[str, Callable] = {
            "cd": self._handle_cd,
            "export": self._handle_export,
        }

    @abstractmethod
    def _format_command(self, executable: str, args: list[str]) -> list[str]:
        """Cada shell hija decide la sintaxis técnica (Bash, PowerShell, etc)."""
        pass

    def run(self, command, timeout: Optional[float] = None) -> CommandResult:
        """Dispatcher principal: decide si el comando es de Estado o de Ejecución."""
        executable = command.executable

        # 1. ¿Es un comando de Estado (Virtual)?
        if executable in self._virtual_builtins:
            return self._virtual_builtins[executable](command)

        # 2. Ejecución externa (De Efecto)
        return self._run_external(command, timeout)

    def __enter__(self):
        self.observer.on_session_start(self.__class__.__name__)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.observer.on_session_end(self.__class__.__name__, exc_val)

    # --- Manejadores de Estado (Comandos Virtuales) ---

    def _handle_cd(self, command) -> CommandResult:
        try:
            new_path = self._resolve_path(command.args)

            if not new_path.exists() or not new_path.is_dir():
                return self._notify_error(f"Directorio no encontrado: {new_path}")

            self.context = replace(self.context, cwd=new_path)
            self.observer.on_context_change("cwd", new_path)

            return CommandResult(standard_output=f"Cambiado a: {new_path}", return_code=0)
        except Exception as e:
            return self._notify_error("Error crítico en cd", e)

    def _handle_export(self, command) -> CommandResult:
        if not command.args:
            return CommandResult(standard_output=str(self.context.env), return_code=0)

        try:
            updates = self._parse_env_vars(command.args)
            new_env = {**self.context.env, **updates}

            for key, value in updates.items():
                self.observer.on_context_change(f"env.{key}", value)

            self.context = replace(self.context, env=new_env)
            return CommandResult(
                standard_output=f"Variables actualizadas: {len(updates)}", 
                return_code=0
            )
        except Exception as e:
            return self._notify_error("Fallo al exportar variables", e)

    # --- Lógica de Ejecución Externa ---

    def _run_external(self, command, timeout: Optional[float]) -> CommandResult:
        """Prepara y ejecuta un proceso en el Sistema Operativo."""
        try:
            # 1. Preparación y validación del ejecutable
            full_path = self._validate_executable(command.executable)
            
            # 2. HELPER: Garantizamos consistencia de argumentos finales
            # Usamos el ArgumentBuilder para aplanar cualquier lista residual
            builder = ArgumentBuilder()
            builder.add_arg(full_path)
            builder.add_arg(self._format_command(command.executable, command.args))
            final_args = builder.build()

            # 3. Notificación previa a la ejecución
            self.observer.on_command_start(command.executable, final_args)

            start_time = time.perf_counter()
            
            process = subprocess.run(
                final_args,
                cwd=self.context.cwd,
                env=self.context.env,
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

        except CommandNotFoundError as e:
            return self._notify_error(str(e), return_code=127)
        except subprocess.TimeoutExpired:
            return self._notify_error(f"Tiempo de espera agotado tras {timeout}s")
        except Exception as e:
            # Error no controlado se notifica y se relanza si es necesario
            self.observer.on_error("Error de ejecución inesperado", e)
            raise e

    # --- Helpers de Soporte ---

    def _validate_executable(self, executable: str) -> str:
        """Verifica si el binario existe en el sistema."""
        full_path = shutil.which(executable)
        if not full_path:
            raise CommandNotFoundError(f"Comando no encontrado: {executable}")
        return full_path

    def _resolve_path(self, args: list[str]) -> Path:
        path_str = args[0] if args else str(Path.home())
        target = Path(path_str).expanduser()

        if not target.is_absolute():
            return (self.context.cwd / target).resolve()
        return target.resolve()
    
    def _parse_env_vars(self, args: list[str]) -> Dict[str, str]:
        updates = {}
        for arg in args:
            if "=" in arg:
                key, value = arg.split("=", 1)
                updates[key] = value
        return updates

    def _notify_error(self, message: str, error: Exception = None, return_code: int = 1) -> CommandResult:
        """Estandariza la notificación de errores y la respuesta."""
        self.observer.on_error(message, error)
        return CommandResult(standard_error=message, return_code=return_code)