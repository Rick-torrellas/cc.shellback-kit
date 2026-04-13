import pytest
from cc_shellback_kit import Command, CommandNotFoundError


def test_command_not_found_exception_message():
    """
    Test that the exception stores the correct message when initialized.
    """
    message = "The binary 'non_existent_exe' was not found in PATH"
    exc = CommandNotFoundError(message)
    assert str(exc) == message


def test_bash_raises_command_not_found(bash_shell):
    """
    Verify that the Shell implementation (Bash) raises CommandNotFoundError
    when attempting to run a non-existent executable.
    """
    invalid_cmd = Command("this_binary_does_not_exist_12345")

    # In your current Shell.py implementation, _run_external catches this
    # and redirects it to _notify_error/Observer.
    # If you want the exception to bubble up, you'd test for pytest.raises.
    # Given your Shell.py logic, it returns a CommandResult with code 127.

    result = bash_shell.run(invalid_cmd)

    assert result.return_code == 127
    assert "not found" in result.standard_error


def test_shell_validation_logic(shell_stub):
    """
    Test the internal _validate_executable logic directly if necessary.
    """
    with pytest.raises(CommandNotFoundError) as excinfo:
        # We simulate the internal call that triggers the lookup
        shell_stub._validate_executable("invalid_command_name")

    assert "Command not found" in str(excinfo.value)


def test_exception_inheritance():
    """
    Ensure CommandNotFoundError inherits from Exception for proper catching.
    """
    assert issubclass(CommandNotFoundError, Exception)
