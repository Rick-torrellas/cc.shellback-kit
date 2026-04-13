import logging
from pathlib import Path
from ..core import ShellObserver, CommandResult


class FileLogObserver(ShellObserver):
    """Saves all Shell activity to a physical file."""

    def __init__(self, log_path: str = "shell_activity.log"):
        # Initialize the path where the log file will be stored
        self.log_path = Path(log_path)

        # Configure the internal logger
        self.logger = logging.getLogger("ShellFileLogger")
        self.logger.setLevel(logging.INFO)

        # Prevent logs from propagating to the console (useful for clean test output)
        self.logger.propagate = False

        # Clear any existing handlers to prevent duplicate logging
        if self.logger.handlers:
            for h in self.logger.handlers[:]:
                h.close()
                self.logger.removeHandler(h)

        # Create a new file handler with UTF-8 encoding
        handler = logging.FileHandler(self.log_path, encoding="utf-8")
        # Define the log format: Timestamp | Severity | Message
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def on_session_start(self, shell_name: str):
        # Log the beginning of a new shell session
        self.logger.info(f"=== SESSION START: {shell_name} ===")

    def on_session_end(self, shell_name: str, error: Exception = None):
        # Log session termination, specifying if it was successful or caused by an error
        if error:
            self.logger.error(f"=== SESSION ENDED WITH ERROR: {error} ===")
        else:
            self.logger.info("=== SESSION ENDED SUCCESSFULLY ===")

    def on_command_start(self, executable: str, final_args: list[str]):
        # Record the exact command string being executed
        cmd_str = " ".join(final_args)
        self.logger.info(f"EXECUTING: {cmd_str}")

    def on_command_result(self, result: CommandResult):
        # Determine the status based on the command's return code
        status = "SUCCESS" if result.is_success() else f"FAILED({result.return_code})"
        # Log the result, execution time, and a snippet of the standard output
        self.logger.info(
            f"RESULT: {status} | "
            f"DURATION: {result.execution_time:.4f}s | "
            f"STDOUT: {result.standard_output.strip()[:100]}..."
        )

    def on_error(self, message: str, error: Exception = None):
        # Log system-level errors and exception details
        self.logger.error(f"SYSTEM ERROR: {message} | Detail: {error}")
