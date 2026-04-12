from unittest.mock import patch, MagicMock
from cc_shellback_kit.core import Command


def test_run_virtual_builtin_cd(shell_stub, tmp_path):
    """Verifica que 'cd' cambie el contexto de la Shell sin ejecutar procesos externos."""
    # Crear un directorio real para el test
    target_dir = tmp_path / "projects"
    target_dir.mkdir()

    cmd = Command("cd").add_args(str(target_dir))

    result = shell_stub.run(cmd)

    assert result.is_success()
    assert shell_stub.context.cwd == target_dir.resolve()
    # Verificar que el observer fue notificado del cambio de contexto
    shell_stub.observer.on_context_change.assert_called_with(
        "cwd", target_dir.resolve()
    )


def test_run_virtual_builtin_export(shell_stub):
    """Verifica que 'export' actualice las variables de entorno en el contexto."""
    cmd = Command("export").add_args("VERSION=1.0.0", "DEBUG=true")

    result = shell_stub.run(cmd)

    assert result.is_success()
    assert shell_stub.context.env["VERSION"] == "1.0.0"
    assert shell_stub.context.env["DEBUG"] == "true"
    # Verificar notificaciones al observer
    assert shell_stub.observer.on_context_change.call_count == 2


def test_run_external_command_success(shell_stub):
    """Verifica la ejecución exitosa de un comando del sistema (mockeado)."""
    cmd = Command("ls").add_args("-la")

    # Mockeamos shutil.which para que encuentre el binario y subprocess.run para el resultado
    with (
        patch("shutil.which", return_value="/usr/bin/ls"),
        patch("subprocess.run") as mock_run,
    ):
        mock_run.return_value = MagicMock(
            stdout="file1.txt\nfile2.txt", stderr="", returncode=0
        )

        result = shell_stub.run(cmd)

        assert result.is_success()
        assert "file1.txt" in result.standard_output
        mock_run.assert_called_once()
        # Verificar que se notificó el inicio y fin del comando al observer
        shell_stub.observer.on_command_start.assert_called()
        shell_stub.observer.on_command_result.assert_called_with(result)


def test_run_external_command_not_found(shell_stub):
    """Verifica el manejo de error cuando un comando no existe en el sistema."""
    cmd = Command("comando_fantasma")

    with patch("shutil.which", return_value=None):
        result = shell_stub.run(cmd)

        assert not result.is_success()
        assert result.return_code == 127
        assert "Comando no encontrado" in result.standard_error
        # El observer debe recibir la notificación de error
        shell_stub.observer.on_error.assert_called()


def test_run_with_custom_timeout(shell_stub):
    """Verifica que el timeout se pase correctamente al ejecutor externo."""
    cmd = Command("sleep").add_args("10")
    custom_timeout = 5.0

    with (
        patch("shutil.which", return_value="/usr/bin/sleep"),
        patch("subprocess.run") as mock_run,
    ):
        shell_stub.run(cmd, timeout=custom_timeout)

        # Extraer los kwargs de la llamada a subprocess.run
        _, kwargs = mock_run.call_args
        assert kwargs["timeout"] == custom_timeout
