from unittest.mock import patch
from CapsuleCore_shellback.capsule import Command


def test_shell_virtual_cd_updates_context(shell, tmp_path):
    """Verifica que el comando virtual 'cd' cambie el directorio de trabajo."""
    # Usamos tmp_path (fixture de pytest) para simular un directorio real
    new_path = tmp_path / "projects"
    new_path.mkdir()

    cmd = Command("cd").add_args(str(new_path))
    result = shell.run(cmd)

    assert result.is_success()
    assert shell.context.cwd == new_path.resolve()


def test_shell_virtual_export_updates_env(shell):
    """Verifica que 'export' muta las variables de entorno en el contexto."""
    cmd = Command("export").add_args("VERSION=1.0.0")
    shell.run(cmd)

    assert "VERSION" in shell.context.env
    assert shell.context.env["VERSION"] == "1.0.0"


def test_shell_external_command_execution(shell, mock_subprocess, spy_observer):
    """Valida el flujo completo de un comando real (ls)."""
    cmd = Command("ls").add_args("-la")

    result = shell.run(cmd)

    # Verificar que el adapter (subprocess) recibió los datos correctos
    mock_subprocess.assert_called_once()
    _, kwargs = mock_subprocess.call_args
    assert kwargs["cwd"] == shell.context.cwd

    # Verificar que el observador fue notificado
    spy_observer.on_command_start.assert_called_once_with("ls", ["ls", "-la"])
    spy_observer.on_command_result.assert_called_once()

    assert result.standard_output == "output de prueba"


def test_shell_command_not_found(shell, spy_observer):
    """Verifica el error 127 cuando el ejecutable no existe."""
    # Forzamos que shutil.which no encuentre el comando
    with patch("shutil.which", return_value=None):
        cmd = Command("comando_inexistente")
        result = shell.run(cmd)

        assert result.return_code == 127
        assert "Comando no encontrado" in result.standard_error
        spy_observer.on_error.assert_called()


def test_shell_custom_timeout(shell, mock_subprocess):
    """Verifica que se respete el timeout pasado al método run."""
    cmd = Command("sleep").add_args("10")
    shell.run(cmd, timeout=5.0)

    _, kwargs = mock_subprocess.call_args
    assert kwargs["timeout"] == 5.0


def test_shell_observer_context_change(shell, spy_observer):
    """Verifica que el observador capte cambios de contexto (CWD/Env)."""
    cmd = Command("export").add_args("USER=rick")
    shell.run(cmd)

    # Ajustamos a lo que el código realmente está enviando
    spy_observer.on_context_change.assert_called_with("env.USER", "rick")
