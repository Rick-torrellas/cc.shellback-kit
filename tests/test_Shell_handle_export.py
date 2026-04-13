from cc_shellback_kit import Command


def test_handle_export_adds_variables(shell_stub, mock_observer):
    """Verify that export KEY=VALUE updates the context and notifies the observer."""
    # 1. Prepare command: export USER=admin ID=123
    cmd = Command("export").add_args("USER=admin", "ID=123")

    # 2. Execute
    result = shell_stub.run(cmd)

    # 3. State Assertions
    assert result.is_success()
    assert shell_stub.context.env["USER"] == "admin"
    assert shell_stub.context.env["ID"] == "123"

    # 4. Observation Assertions
    # on_context_change should be called for each variable
    assert mock_observer.on_context_change.call_count == 2
    mock_observer.on_context_change.assert_any_call("env.USER", "admin")
    mock_observer.on_context_change.assert_any_call("env.ID", "123")


def test_handle_export_no_args_returns_current_env(shell_stub):
    """Verify that export without arguments returns the current environment string."""
    # Manually inject a previous environment
    from dataclasses import replace

    shell_stub.context = replace(shell_stub.context, env={"EXISTING": "data"})

    cmd = Command("export")
    result = shell_stub.run(cmd)

    assert result.is_success()
    assert "{'EXISTING': 'data'}" in result.standard_output


def test_handle_export_malformed_args_ignored(shell_stub):
    """Verify that arguments without '=' are ignored according to _parse_env_vars logic."""
    # 'INVALID' lacks '=', 'VALID=yes' has it.
    cmd = Command("export").add_args("INVALID", "VALID=yes")

    result = shell_stub.run(cmd)

    assert result.is_success()
    assert "VALID" in shell_stub.context.env
    assert "INVALID" not in shell_stub.context.env
    assert "Variables updated: 1" in result.standard_output


def test_handle_export_overwrites_existing_variable(shell_stub, mock_observer):
    """Verify that export overwrites existing values."""
    # Initial setup
    shell_stub.run(Command("export").add_args("VAR=old"))

    # Execute overwrite
    cmd = Command("export").add_args("VAR=new")
    shell_stub.run(cmd)

    assert shell_stub.context.env["VAR"] == "new"
    mock_observer.on_context_change.assert_called_with("env.VAR", "new")


def test_handle_export_error_notification(shell_stub, mock_observer, monkeypatch):
    """Verify that unexpected errors during parsing are notified."""

    # Force an error in the internal parsing logic
    def mock_parse_fail(*args):
        raise ValueError("Simulated Parse Error")

    # Access the instance through the stub
    monkeypatch.setattr
