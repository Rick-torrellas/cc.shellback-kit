from abc import ABC, abstractmethod
import shutil
import time
import subprocess
from .Logger import Logger # Asumiendo que usas tu interfaz de Logger
from ..capsule import NullLogger
from .SessionContext import SessionContext
from .CommandResult import CommandResult
from typing import Optional

class CommandNotFoundError(Exception):
    """Lanzada cuando el binario no existe en el PATH."""
    pass

class Shell(ABC):
    def __init__(self, context: Optional[SessionContext] = None, 
                 logger: Optional[Logger] = None, 
                 default_timeout: float = 30.0):
        self.context = context or SessionContext()
        self.logger = logger or NullLogger()
        self.default_timeout = default_timeout

    @abstractmethod
    def _format_command(self, executable: str, args: list[str]) -> list[str]:
        """Cada shell hija decide cómo formatear la lista final (Strategy)."""
        pass

    def __enter__(self):
        self.logger.info(f"Iniciando sesión de {self.__class__.__name__}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.error(f"Sesión finalizada con error: {exc_val}")
        else:
            self.logger.info(f"Sesión de {self.__class__.__name__} finalizada correctamente")
        # No retornamos True para que las excepciones sigan propagándose si ocurren

    def run(self, command, timeout: Optional[float] = None) -> CommandResult:
        """
        Método 'Template' que coordina la ejecución.
        """
        executable = command.executable
        args = command.args # El ArgumentBuilder ya devuelve una lista
        
        # 1. Lazy Check de binario
        if not shutil.which(executable):
            self.logger.error(f"Command not found: {executable}")
            raise CommandNotFoundError(f"The executable '{executable}' was not found in PATH.")

        # 2. Preparación según la Shell específica
        final_args = self._format_command(executable, args)
        
        self.logger.debug(f"Executing: {' '.join(final_args)} in {self.context.cwd}")
        
        start_time = time.perf_counter()
        
        try:
            process = subprocess.run(
                final_args,
                cwd=self.context.cwd,
                env={**self.context.env}, # Merge de env actual
                capture_output=True,
                text=True,
                encoding=self.context.encoding,
                timeout=timeout or self.default_timeout
            )
            
            execution_time = time.perf_counter() - start_time
            
            result = CommandResult(
                standard_output=process.stdout,
                standard_error=process.stderr,
                return_code=process.returncode,
                execution_time=execution_time,
                command_sent=final_args
            )
            
            if result.is_success():
                self.logger.info(f"Success: {executable}")
            else:
                self.logger.warning(f"Failed: {executable} with code {result.return_code}")
                
            return result

        except subprocess.TimeoutExpired as e:
            self.logger.error(f"Timeout after {self.default_timeout}s")
            raise e