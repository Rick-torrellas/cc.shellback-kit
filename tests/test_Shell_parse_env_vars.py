from cc_shellback_kit import Command


def test_parse_env_vars_correct_format(shell_stub):
    """Verify that key=value arguments are parsed correctly."""
    args = ["VAR1=value1", "VAR2=value2", "VAR3=multiple=equals"]

    # Accessing the protected method for unit validation
    result = shell_stub._parse_env_vars(args)

    assert result == {"VAR1": "value1", "VAR2": "value2", "VAR3": "multiple=equals"}


def test_parse_env_vars_invalid_format(shell_stub):
    """Verify that arguments without the '=' sign are ignored."""
    args = ["INVALID_VAR", "VALID=yes", "ANOTHER_INVALID"]

    result = shell_stub._parse_env_vars(args)

    assert result == {"VALID": "yes"}
    assert "INVALID_VAR" not in result


def test_parse_env_vars_empty_list(shell_stub):
    """Verify behavior with an empty list."""
    result = shell_stub._parse_env_vars([])
    assert result == {}


def test_handle_export_integration(shell_stub):
    """
    Integration test: Verify that the 'export' command uses
    _parse_env_vars and updates the context.
    """
    cmd = Command("export")
    cmd.add_args("DATABASE_URL=postgres://localhost", "DEBUG=True")

    # Execute through the main dispatcher
    shell_stub.run(cmd)

    # Verify that the shell context has been updated
    assert shell_stub.context.env["DATABASE_URL"] == "postgres://localhost"
    assert shell_stub.context.env["DEBUG"] == "True"

    # Verify that the observer was notified of the context change
    # (Called once for each variable)
    assert shell_stub.observer.on_context_change.called
