import sys
from datetime import datetime
from ..core import Logger


class ConsoleLogger(Logger):
    """
    Logger implementation that prints to standard output with colors and timestamps.
    Ideal for development and interactive scripts.
    """

    # ANSI color codes for terminal output formatting
    COLORS = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "RESET": "\033[0m",  # Reset to default
    }

    def _log(self, level: str, message: str):
        """Internal logging method that formats and outputs colored log messages to stderr."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = self.COLORS.get(level, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]

        # Format: [14:30:05] [INFO] Message
        print(f"[{timestamp}] {color}[{level}]{reset} {message}", file=sys.stderr)

    def info(self, message: str):
        """Log an informational message."""
        self._log("INFO", message)

    def debug(self, message: str):
        """Log a debug message."""
        self._log("DEBUG", message)

    def warning(self, message: str):
        """Log a warning message."""
        self._log("WARNING", message)

    def error(self, message: str):
        """Log an error message."""
        self._log("ERROR", message)
