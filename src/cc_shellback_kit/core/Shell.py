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
    """Raised when the binary does not exist in the PATH."""

    pass


class Shell(ABC):
    def __init__(
        self,
        context: Optional[SessionContext] = None,
        observer: Optional[ShellObserver] = None,
        default_timeout: float = 30.0,
    ):
        """
        Initializes the Shell instance with execution context,
        observation capabilities, and a default command timeout.
        """
        # Set the session context (holds environment variables, working directory, etc.)
        self.context = context or SessionContext()

        # Set the observer to track shell events or outputs
        self.observer = observer or ShellObserver()

        # Define the maximum time allowed for command execution
        self.default_timeout = default_timeout

        # Virtual built-in command map (State Management)
        # These commands are intercepted and handled by the shell itself
        # rather than being passed to the operating system's sub-processes.
        self._virtual_builtins: Dict[str, Callable] = {
            "cd": self._handle_cd,  # Manages directory changes within the context
            "export": self._handle_export,  # Manages environment variable updates
        }

    @abstractmethod
    def _format_command(self, executable: str, args: list[str]) -> list[str]:
        """Each child shell determines the technical syntax (Bash, PowerShell, etc.)."""
        pass

    def run(self, command, timeout: Optional[float] = None) -> CommandResult:
        """Main dispatcher: decides if the command is a State or Execution command."""
        executable = command.executable

        # 1. Is it a State (Virtual) command?
        if executable in self._virtual_builtins:
            return self._virtual_builtins[executable](command)

        # 2. External execution (Effect-based)
        return self._run_external(command, timeout)

    def __enter__(self):
        self.observer.on_session_start(self.__class__.__name__)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.observer.on_session_end(self.__class__.__name__, exc_val)

    # --- Manejadores de Estado (Comandos Virtuales) ---

    def _handle_cd(self, command) -> CommandResult:
        try:
            # Resolve the target path from the command arguments
            new_path = self._resolve_path(command.args)

            # Validate if the path exists and is a directory
            if not new_path.exists() or not new_path.is_dir():
                return self._notify_error(f"Directory not found: {new_path}")

            # Update the current working directory in the context using a functional replace
            self.context = replace(self.context, cwd=new_path)
            # Notify the observer about the change in the working directory
            self.observer.on_context_change("cwd", new_path)

            # Return success result with the updated path message
            return CommandResult(
                standard_output=f"Changed to: {new_path}", return_code=0
            )
        except Exception as e:
            # Catch unexpected errors during the directory change process
            return self._notify_error("Critical error in cd", e)

    def _handle_export(self, command) -> CommandResult:
        # If no arguments are provided, return the current environment variables as a string
        if not command.args:
            return CommandResult(standard_output=str(self.context.env), return_code=0)

        try:
            # Parse the provided arguments into a dictionary of environment variable updates
            updates = self._parse_env_vars(command.args)
            # Create a new environment dictionary merging current variables with updates
            new_env = {**self.context.env, **updates}

            # Notify the observer for every variable that was changed
            for key, value in updates.items():
                self.observer.on_context_change(f"env.{key}", value)

            # Update the context with the new environment dictionary
            self.context = replace(self.context, env=new_env)
            return CommandResult(
                standard_output=f"Variables updated: {len(updates)}", return_code=0
            )
        except Exception as e:
            # Handle and notify errors occurring during the export process
            return self._notify_error("Failed to export variables", e)

    # --- Lógica de Ejecución Externa ---

    def _run_external(self, command, timeout: Optional[float]) -> CommandResult:
        """Prepares and executes a process in the Operating System."""
        try:
            # 1. Preparation and validation of the executable
            full_path = self._validate_executable(command.executable)

            # 2. HELPER: Ensure consistency of final arguments
            # Use ArgumentBuilder to flatten any residual lists
            builder = ArgumentBuilder()
            builder.add_arg(full_path)
            builder.add_arg(self._format_command(command.executable, command.args))
            final_args = builder.build()

            # 3. Pre-execution notification
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
            return self._notify_error(f"Timeout expired after {timeout}s")
        except Exception as e:
            # Unhandled error is notified and re-raised if necessary
            self.observer.on_error("Unexpected execution error", e)
            raise e

    # --- Helpers de Soporte ---

    def _validate_executable(self, executable: str) -> str:
        # Use shutil.which to find the full path of the executable in the system's PATH
        full_path = shutil.which(executable)

        # If the executable is not found, raise a CommandNotFoundError with an English message
        if not full_path:
            raise CommandNotFoundError(f"Command not found: {executable}")

        # Return the absolute path to the executable
        return full_path

    def _resolve_path(self, args: list[str]) -> Path:
        # Get the path string from arguments; default to the user's home directory if args is empty
        path_str = args[0] if args else str(Path.home())

        # Create a Path object and expand the '~' symbol to the full home directory path
        target = Path(path_str).expanduser()

        # If the path is relative, join it with the current working directory (cwd) and resolve it
        if not target.is_absolute():
            return (self.context.cwd / target).resolve()

        # If the path is already absolute, simply resolve it (to handle symlinks or '..' components)
        return target.resolve()

    def _parse_env_vars(self, args: list[str]) -> Dict[str, str]:
        # Initialize an empty dictionary to store the parsed environment variables
        updates = {}

        # Iterate through each string in the provided list of arguments
        for arg in args:
            # Check if the argument contains an equals sign, indicating a key-value pair
            if "=" in arg:
                # Split the string at the first '=' into exactly two parts: key and value
                key, value = arg.split("=", 1)

                # Assign the value to the corresponding key in the dictionary
                updates[key] = value

        # Return the dictionary containing all successfully parsed variables
        return updates

    def _notify_error(
        self, message: str, error: Exception = None, return_code: int = 1
    ) -> CommandResult:
        # Trigger the observer's error handler with the provided message and exception
        self.observer.on_error(message, error)

        # Return a CommandResult object containing the error message and the exit status code
        return CommandResult(standard_error=message, return_code=return_code)
