from ..core import CommandResult, ShellObserver


class ConsoleLogObserver(ShellObserver):
    """Displays in the console what is happening in real time."""

    def on_command_start(self, executable, final_args):
        # Notify the user which command is currently being executed
        print(f"🛠️  Executing: {' '.join(final_args)}")

    def on_command_result(self, result: CommandResult):
        # Check if the command finished successfully
        if result.is_success():
            # Print success status and the total execution time in seconds
            print(f"✅ OK ({result.execution_time:.3f}s)")
        else:
            # Print failure status and the specific return code from the process
            print(f"❌ FAIL (Code: {result.return_code})")
            # If there is detailed error output, print it after stripping whitespace
            if result.standard_error:
                print(f"   Error: {result.standard_error.strip()}")
