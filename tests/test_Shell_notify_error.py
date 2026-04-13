from cc_shellback_kit import CommandResult


def test_notify_error_notifies_observer(shell_stub, mock_observer):
    """Verify that the error is correctly reported to the observer."""
    # Define test data and a custom exception
    error_msg = "Error de prueba"
    custom_exception = ValueError("Algo salió mal")

    # Execute the internal notify method
    shell_stub._notify_error(error_msg, error=custom_exception)

    # Verify that the observer's on_error method was called with the expected arguments
    mock_observer.on_error.assert_called_once_with(error_msg, custom_exception)


def test_notify_error_returns_failed_command_result(shell_stub):
    """Verify that a CommandResult is returned with the specific error code and message."""
    error_msg = "Fallo crítico"
    expected_code = 127

    # Call the method with a specific return code
    result = shell_stub._notify_error(error_msg, return_code=expected_code)

    # Validate the structure and content of the resulting CommandResult object
    assert isinstance(result, CommandResult)
    assert result.return_code == expected_code
    assert result.standard_error == error_msg
    assert result.is_success() is False


def test_notify_error_defaults(shell_stub):
    """Verify default behavior when no exception or explicit return code is provided."""
    error_msg = "Error genérico"

    # Call the method with only the error message
    result = shell_stub._notify_error(error_msg)

    # Check that it defaults to return_code 1 and empty standard output
    assert result.return_code == 1
    assert result.standard_error == error_msg
    assert result.standard_output == ""
