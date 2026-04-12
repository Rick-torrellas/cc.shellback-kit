from cc_shellback_kit import CommandResult


def test_notify_error_notifies_observer(shell_stub, mock_observer):
    """Verifica que el error se reporte correctamente al observer."""
    error_msg = "Error de prueba"
    custom_exception = ValueError("Algo salió mal")

    # Ejecutamos el método interno
    shell_stub._notify_error(error_msg, error=custom_exception)

    # Verificamos que el observer recibió la señal
    mock_observer.on_error.assert_called_once_with(error_msg, custom_exception)


def test_notify_error_returns_failed_command_result(shell_stub):
    """Verifica que se devuelva un CommandResult con el código de error y mensaje."""
    error_msg = "Fallo crítico"
    expected_code = 127

    result = shell_stub._notify_error(error_msg, return_code=expected_code)

    # Verificamos la estructura del resultado
    assert isinstance(result, CommandResult)
    assert result.return_code == expected_code
    assert result.standard_error == error_msg
    assert result.is_success() is False


def test_notify_error_defaults(shell_stub):
    """Verifica el comportamiento por defecto (sin excepción ni código explícito)."""
    error_msg = "Error genérico"

    result = shell_stub._notify_error(error_msg)

    # Por defecto el return_code es 1
    assert result.return_code == 1
    assert result.standard_error == error_msg
    assert result.standard_output == ""
