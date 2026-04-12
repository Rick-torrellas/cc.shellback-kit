from cc_shellback_kit import Command


def test_parse_env_vars_correct_format(shell_stub):
    """Verifica que los argumentos clave=valor se parseen correctamente."""
    args = ["VAR1=value1", "VAR2=value2", "VAR3=multiple=equals"]

    # Acceso al método protegido para validación unitaria
    result = shell_stub._parse_env_vars(args)

    assert result == {"VAR1": "value1", "VAR2": "value2", "VAR3": "multiple=equals"}


def test_parse_env_vars_invalid_format(shell_stub):
    """Verifica que los argumentos sin el signo '=' sean ignorados."""
    args = ["INVALID_VAR", "VALID=yes", "ANOTHER_INVALID"]

    result = shell_stub._parse_env_vars(args)

    assert result == {"VALID": "yes"}
    assert "INVALID_VAR" not in result


def test_parse_env_vars_empty_list(shell_stub):
    """Verifica el comportamiento con una lista vacía."""
    result = shell_stub._parse_env_vars([])
    assert result == {}


def test_handle_export_integration(shell_stub):
    """
    Test de integración: Verifica que el comando 'export' use
    _parse_env_vars y actualice el contexto.
    """
    cmd = Command("export")
    cmd.add_args("DATABASE_URL=postgres://localhost", "DEBUG=True")

    # Ejecutamos a través del dispatcher principal
    shell_stub.run(cmd)

    # Verificamos que el contexto de la shell se haya actualizado
    assert shell_stub.context.env["DATABASE_URL"] == "postgres://localhost"
    assert shell_stub.context.env["DEBUG"] == "True"

    # Verificamos que el observer fue notificado del cambio de contexto
    # (Se llama una vez por cada variable)
    assert shell_stub.observer.on_context_change.called
