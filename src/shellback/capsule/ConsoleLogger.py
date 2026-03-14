import sys
from datetime import datetime
from ..core import Logger

class ConsoleLogger(Logger):
    """
    Implementación que imprime en la salida estándar con colores y timestamps.
    Ideal para desarrollo y scripts interactivos.
    """
    # Códigos ANSI para colores
    COLORS = {
        "DEBUG": "\033[94m",    # Azul
        "INFO": "\033[92m",     # Verde
        "WARNING": "\033[93m",  # Amarillo
        "ERROR": "\033[91m",    # Rojo
        "RESET": "\033[0m"      # Reset
    }

    def _log(self, level: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = self.COLORS.get(level, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]
        
        # Formato: [14:30:05] [INFO] Mensaje
        print(f"[{timestamp}] {color}[{level}]{reset} {message}", file=sys.stderr)

    def info(self, message: str):
        self._log("INFO", message)

    def debug(self, message: str):
        self._log("DEBUG", message)

    def warning(self, message: str):
        self._log("WARNING", message)

    def error(self, message: str):
        self._log("ERROR", message)