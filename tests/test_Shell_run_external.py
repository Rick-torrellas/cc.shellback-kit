import pytest
import subprocess
from unittest.mock import MagicMock, patch
from cc_shellback_kit import Command, CommandResult


def test_run_external_success(shell_stub, mock_observer):
    """Verifica que un comando externo exitoso notifica correctamente y devuelve el resultado."""
    cmd = Command("ls").add_args("-la")

    # Mockeamos shutil.which para que parezca que el comando existe
    # Mockeamos subprocess.run para simular una ejecución exitosa
    with (
        patch("shutil.which", return_value="/usr/bin/ls"),
        patch("subprocess.run") as mock_run,
    ):
        mock_run.return_value = MagicMock(
            stdout="file1\nfile2", stderr="", returncode=0
        )

        result = shell_stub.run(cmd)

        # Verificaciones de ejecución
        assert result.is_success()
        assert result.standard_output == "file1\nfile2"
        assert result.return_code == 0

        # Verificación de Observers
        mock_observer.on_command_start.assert_called_once_with(
            "ls", ["/usr/bin/ls", "-la"]
        )
        mock_observer.on_command_result.assert_called_once()
        assert isinstance(
            mock_observer.on_command_result.call_args[0][0], CommandResult
        )


def test_run_external_command_not_found(shell_stub, mock_observer):
    """Verifica el manejo de error cuando el binario no existe."""
    cmd = Command("invalid_cmd")

    with patch("shutil.which", return_value=None):
        result = shell_stub.run(cmd)

    assert result.return_code == 127
    assert "Comando no encontrado" in result.standard_error
    mock_observer.on_error.assert_called_once()


def test_run_external_timeout(shell_stub, mock_observer):
    """Verifica que el timeout de subprocess se captura y notifica."""
    cmd = Command("sleep").add_args("10")

    with (
        patch("shutil.which", return_value="/usr/bin/sleep"),
        patch(
            "subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd=["sleep"], timeout=1.0),
        ),
    ):
        result = shell_stub.run(cmd, timeout=1.0)

    assert "Tiempo de espera agotado" in result.standard_error
    mock_observer.on_error.assert_called_once()


def test_run_external_unexpected_exception(shell_stub, mock_observer):
    """Verifica que errores inesperados se notifican y relanzan."""
    cmd = Command("ls")

    with (
        patch("shutil.which", return_value="/usr/bin/ls"),
        patch("subprocess.run", side_effect=OSError("Permiso denegado")),
    ):
        with pytest.raises(OSError):
            shell_stub.run(cmd)

    # Obtenemos los argumentos de la última llamada a on_error
    # args[0] es el mensaje, args[1] es la excepción
    args, _ = mock_observer.on_error.call_args

    assert args[0] == "Error de ejecución inesperado"
    assert isinstance(args[1], OSError)
    assert str(args[1]) == "Permiso denegado"
