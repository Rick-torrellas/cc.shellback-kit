import pytest
import subprocess
from unittest.mock import MagicMock, patch
from cc_shellback_kit import Command, CommandResult


def test_run_external_success(shell_stub, mock_observer):
    """Verify that a successful external command notifies correctly and returns the result."""
    # Initialize command with arguments
    cmd = Command("ls").add_args("-la")

    # Mock shutil.which to simulate the command exists in the system path
    # Mock subprocess.run to simulate a successful execution without actual OS calls
    with (
        patch("shutil.which", return_value="/usr/bin/ls"),
        patch("subprocess.run") as mock_run,
    ):
        # Configure the mock to return a successful execution object
        mock_run.return_value = MagicMock(
            stdout="file1\nfile2", stderr="", returncode=0
        )

        result = shell_stub.run(cmd)

        # Execution Assertions: Check if result matches expected mock data
        assert result.is_success()
        assert result.standard_output == "file1\nfile2"
        assert result.return_code == 0

        # Observer Assertions: Ensure the observer pattern is triggered correctly
        mock_observer.on_command_start.assert_called_once_with(
            "ls", ["/usr/bin/ls", "-la"]
        )
        mock_observer.on_command_result.assert_called_once()
        # Verify the first argument passed to on_command_result is a CommandResult instance
        assert isinstance(
            mock_observer.on_command_result.call_args[0][0], CommandResult
        )


def test_run_external_command_not_found(shell_stub, mock_observer):
    """Verify error handling when the binary does not exist in the system."""
    cmd = Command("invalid_cmd")

    # Simulate shutil.which failing to find the executable
    with patch("shutil.which", return_value=None):
        result = shell_stub.run(cmd)

    # Check for standard shell 'command not found' exit code (127)
    assert result.return_code == 127
    assert "Command not found" in result.standard_error
    mock_observer.on_error.assert_called_once()


def test_run_external_timeout(shell_stub, mock_observer):
    """Verify that subprocess timeout is captured and notified appropriately."""
    cmd = Command("sleep").add_args("10")

    with (
        patch("shutil.which", return_value="/usr/bin/sleep"),
        # Force subprocess.run to raise a TimeoutExpired exception
        patch(
            "subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd=["sleep"], timeout=1.0),
        ),
    ):
        result = shell_stub.run(cmd, timeout=1.0)

    # Validate that the timeout was handled and logged in standard error
    assert "Timeout expired" in result.standard_error
    mock_observer.on_error.assert_called_once()


def test_run_external_unexpected_exception(shell_stub, mock_observer):
    """Verify that unexpected system errors are notified and then re-raised."""
    cmd = Command("ls")

    with (
        patch("shutil.which", return_value="/usr/bin/ls"),
        # Simulate a system-level error like permission issues
        patch("subprocess.run", side_effect=OSError("Permiso denegado")),
    ):
        # The runner should notify the observer but still raise the exception for the caller
        with pytest.raises(OSError):
            shell_stub.run(cmd)

    # Extract arguments from the last call to on_error
    # args[0] is the error message string, args[1] is the exception object
    args, _ = mock_observer.on_error.call_args

    assert args[0] == "Unexpected execution error"
    assert isinstance(args[1], OSError)
    assert str(args[1]) == "Permiso denegado"
