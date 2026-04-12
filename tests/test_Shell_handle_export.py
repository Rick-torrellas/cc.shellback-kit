from cc_shellback_kit import Command


def test_handle_export_adds_variables(shell_stub, mock_observer):
    """Verifica que export KEY=VALUE actualiza el contexto y notifica al observer."""
    # 1. Preparar comando: export USER=admin ID=123
    cmd = Command("export").add_args("USER=admin", "ID=123")

    # 2. Ejecutar
    result = shell_stub.run(cmd)

    # 3. Aserciones de Estado
    assert result.is_success()
    assert shell_stub.context.env["USER"] == "admin"
    assert shell_stub.context.env["ID"] == "123"

    # 4. Aserciones de Observación
    # Se debe llamar a on_context_change por cada variable
    assert mock_observer.on_context_change.call_count == 2
    mock_observer.on_context_change.assert_any_call("env.USER", "admin")
    mock_observer.on_context_change.assert_any_call("env.ID", "123")


def test_handle_export_no_args_returns_current_env(shell_stub):
    """Verifica que export sin argumentos devuelve el string del entorno actual."""
    # Inyectar un entorno previo manualmente
    from dataclasses import replace

    shell_stub.context = replace(shell_stub.context, env={"EXISTING": "data"})

    cmd = Command("export")
    result = shell_stub.run(cmd)

    assert result.is_success()
    assert "{'EXISTING': 'data'}" in result.standard_output


def test_handle_export_malformed_args_ignored(shell_stub):
    """Verifica que argumentos sin '=' sean ignorados según la lógica de _parse_env_vars."""
    # 'INVALID' no tiene '=', 'VALID=yes' sí.
    cmd = Command("export").add_args("INVALID", "VALID=yes")

    result = shell_stub.run(cmd)

    assert result.is_success()
    assert "VALID" in shell_stub.context.env
    assert "INVALID" not in shell_stub.context.env
    assert "Variables actualizadas: 1" in result.standard_output


def test_handle_export_overwrites_existing_variable(shell_stub, mock_observer):
    """Verifica que export sobrescribe valores existentes."""
    # Setup inicial
    shell_stub.run(Command("export").add_args("VAR=old"))

    # Ejecución de sobrescritura
    cmd = Command("export").add_args("VAR=new")
    shell_stub.run(cmd)

    assert shell_stub.context.env["VAR"] == "new"
    mock_observer.on_context_change.assert_called_with("env.VAR", "new")


def test_handle_export_error_notification(shell_stub, mock_observer, monkeypatch):
    """Verifica que errores inesperados durante el parseo se notifiquen."""

    # Forzamos un error en la lógica interna de parseo
    def mock_parse_fail(*args):
        raise ValueError("Simulated Parse Error")

    # Accedemos a la instancia a través del stub
    monkeypatch.setattr(shell_stub, "_parse_env_vars", mock_parse_fail)

    cmd = Command("export").add_args("ANY=thing")
    result = shell_stub.run(cmd)

    assert result.return_code == 1
    assert "Fallo al exportar variables" in result.standard_error
    mock_observer.on_error.assert_called_once()
