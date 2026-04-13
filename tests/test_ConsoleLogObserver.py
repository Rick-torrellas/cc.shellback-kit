import pytest
from cc_shellback_kit import ConsoleLogObserver
from cc_shellback_kit import CommandResult


class TestConsoleLogObserver:
    # Pytest fixture to provide a fresh ConsoleLogObserver instance for each test
    @pytest.fixture
    def observer(self):
        return ConsoleLogObserver()

    def test_on_command_start_prints_executable_and_args(self, observer, capsys):
        """Verify that the command and its arguments are printed when starting."""
        executable = "ls"
        final_args = ["ls", "-l", "/home"]

        observer.on_command_start(executable, final_args)

        # Capture stdout/stderr to verify the console output
        captured = capsys.readouterr()
        assert "🛠️  Executing: ls -l /home\n" in captured.out

    def test_on_command_result_success(self, observer, capsys):
        """Verify the success message when the return code is 0."""
        result = CommandResult(
            standard_output="hola", return_code=0, execution_time=0.1234
        )

        observer.on_command_result(result)

        captured = capsys.readouterr()
        assert "✅ OK (0.123s)" in captured.out

    def test_on_command_result_failure_with_error_message(self, observer, capsys):
        """Verify the failure message and the printing of stderr."""
        result = CommandResult(
            standard_error="Permiso denegado", return_code=1, execution_time=0.005
        )

        observer.on_command_result(result)

        captured = capsys.readouterr()
        assert "❌ FAIL (Code: 1)" in captured.out
        assert "Error: Permiso denegado" in captured.out

    def test_on_command_result_failure_without_stderr(self, observer, capsys):
        """Verify it doesn't crash if the error has no message in stderr."""
        result = CommandResult(standard_error="", return_code=127)

        observer.on_command_result(result)

        captured = capsys.readouterr()
        assert "❌ FAIL (Code: 127)" in captured.out
        # It should not attempt to print the "Error:" line if stderr is empty
        assert "Error:" not in captured.out
