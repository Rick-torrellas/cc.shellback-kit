import pytest
from cc_shellback_kit import Command


def test_bash_format_command(bash_shell):
    """Verifica que Bash no altere los argumentos (la lógica de unión está en Shell)."""
    # Bash._format_command según tu archivo solo devuelve los args
    result = bash_shell._format_command("ls", ["-l", "-a"])
    assert result == ["-l", "-a"]


def test_bash_run_external_success(bash_shell, mock_observer):
    """Prueba la ejecución de un comando real (ls o dir) y la notificación al observer."""
    cmd = Command("echo").add_args("Hola Mundo")
    result = bash_shell.run(cmd)

    assert result.is_success()
    assert "Hola Mundo" in result.standard_output
    # Verificar que el observer fue notificado
    mock_observer.on_command_start.assert_called_once()
    mock_observer.on_command_result.assert_called_once()


def test_bash_command_not_found(bash_shell, mock_observer):
    """Verifica el comportamiento cuando el binario no existe."""
    cmd = Command("comando_que_no_existe_12345")
    result = bash_shell.run(cmd)

    assert result.return_code == 127
    assert "Comando no encontrado" in result.standard_error
    mock_observer.on_error.assert_called_once()


def test_bash_virtual_cd(bash_shell, tmp_path, mock_observer):
    """Verifica que el comando virtual 'cd' cambie el contexto de la sesión."""
    subdir = tmp_path / "test_dir"
    subdir.mkdir()

    cmd = Command("cd").add_args(str(subdir))
    result = bash_shell.run(cmd)

    assert result.is_success()
    assert bash_shell.context.cwd == subdir
    # Verificar que se notificó el cambio de contexto
    mock_observer.on_context_change.assert_called_with("cwd", subdir)


def test_bash_virtual_export(bash_shell, mock_observer):
    """Verifica que 'export' actualice las variables de entorno en el contexto."""
    cmd = Command("export").add_args("VERSION=1.0.0", "DEBUG=true")
    result = bash_shell.run(cmd)

    assert result.is_success()
    assert bash_shell.context.env["VERSION"] == "1.0.0"
    assert bash_shell.context.env["DEBUG"] == "true"
    # Verificar que se notificó cada cambio
    assert mock_observer.on_context_change.call_count == 2


def test_bash_session_hooks(bash_shell, mock_observer):
    """Prueba que los hooks de inicio y fin de sesión funcionen con el context manager."""
    with bash_shell as sh:
        sh.run(Command("echo").add_args("test"))

    mock_observer.on_session_start.assert_called_once_with("Bash")
    mock_observer.on_session_end.assert_called_once()


@pytest.mark.timeout(2)
def test_bash_timeout(bash_shell):
    """Verifica que el timeout funcione correctamente (usando sleep)."""
    # Nota: Este test depende de que 'sleep' esté disponible en el sistema
    cmd = Command("sleep").add_args("5")

    # Ejecutamos con un timeout corto
    result = bash_shell.run(cmd, timeout=0.1)

    assert result.return_code == 1
    assert "Tiempo de espera agotado" in result.standard_error
