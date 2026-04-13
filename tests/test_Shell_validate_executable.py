import pytest
from unittest.mock import patch
from cc_shellback_kit import CommandNotFoundError


def test_validate_executable_success(shell_stub):
    """
    Verifies that if shutil.which finds the command,
    it returns the full path.
    """
    # Patch shutil.which to control its behavior during the test
    with patch("shutil.which") as mock_which:
        # Simulate finding the binary at a typical path
        mock_which.return_value = "/usr/bin/ls"

        result = shell_stub._validate_executable("ls")

        # Ensure the returned path matches the mock value
        assert result == "/usr/bin/ls"
        # Verify the mock was called with the correct argument
        mock_which.assert_called_once_with("ls")


def test_validate_executable_not_found(shell_stub):
    """
    Verifies that CommandNotFoundError is raised if the binary does not exist.
    """
    with patch("shutil.which") as mock_which:
        # Simulate that the command is not found in the system PATH
        mock_which.return_value = None

        # Check that the specific exception is raised
        with pytest.raises(CommandNotFoundError) as excinfo:
            shell_stub._validate_executable("comando_fantasma")

        # Validate the error message content
        assert "Command not found: comando_fantasma" in str(excinfo.value)
        mock_which.assert_called_once_with("comando_fantasma")


def test_validate_executable_with_absolute_path(shell_stub):
    """
    Verifies that it works correctly even if the user
    passes an absolute path that exists.
    """
    absolute_path = "/usr/local/bin/python3"
    with patch("shutil.which") as mock_which:
        # Mock returns the same absolute path passed as input
        mock_which.return_value = absolute_path

        result = shell_stub._validate_executable(absolute_path)

        assert result == absolute_path
        mock_which.assert_called_once_with(absolute_path)
