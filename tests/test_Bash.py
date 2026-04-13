import pytest
from cc_shellback_kit import Command


def test_bash_format_command(bash_shell):
    """Verify that Bash does not alter the arguments (joining logic resides in Shell)."""
    # Bash._format_command according to your file only returns the args
    result = bash_shell._format_command("ls", ["-l", "-a"])
    assert result == ["-l", "-a"]


def test_bash_run_external_success(bash_shell, mock_observer):
    """Test the execution of a real command (ls or dir) and observer notification."""
    cmd = Command("echo").add_args("Hola Mundo")
    result = bash_shell.run(cmd)

    assert result.is_success()
    assert "Hola Mundo" in result.standard_output
    # Verify that the observer was notified
    mock_observer.on_command_start.assert_called_once()
    mock_observer.on_command_result.assert_called_once()


def test_bash_command_not_found(bash_shell, mock_observer):
    """Verify behavior when the binary does not exist."""
    cmd = Command("comando_que_no_existe_12345")
    result = bash_shell.run(cmd)

    assert result.return_code == 127
    assert "Command not found" in result.standard_error
    mock_observer.on_error.assert_called_once()


def test_bash_virtual_cd(bash_shell, tmp_path, mock_observer):
    """Verify that the virtual 'cd' command changes the session context."""
    subdir = tmp_path / "test_dir"
    subdir.mkdir()

    cmd = Command("cd").add_args(str(subdir))
    result = bash_shell.run(cmd)

    assert result.is_success()
    assert bash_shell.context.cwd == subdir
    # Verify that the context change was notified
    mock_observer.on_context_change.assert_called_with("cwd", subdir)


def test_bash_virtual_export(bash_shell, mock_observer):
    """Verify that 'export' updates the environment variables in the context."""
    cmd = Command("export").add_args("VERSION=1.0.0", "DEBUG=true")
    result = bash_shell.run(cmd)

    assert result.is_success()
    assert bash_shell.context.env["VERSION"] == "1.0.0"
    assert bash_shell.context.env["DEBUG"] == "true"
    # Verify that each change was notified
    assert mock_observer.on_context_change.call_count == 2


def test_bash_session_hooks(bash_shell, mock_observer):
    """Test that session start and end hooks work with the context manager."""
    with bash_shell as sh:
        sh.run(Command("echo").add_args("test"))

    mock_observer.on_session_start.assert_called_once_with("Bash")
    mock_observer.on_session_end.assert_called_once()


@pytest.mark.timeout(2)
def test_bash_timeout(bash_shell):
    """Verify that timeout works correctly (using sleep)."""
    # Note: This test depends on 'sleep' being available on the system
    cmd = Command("sleep").add_args("5")

    # Execute with a short timeout
    result = bash_shell.run(cmd, timeout=0.1)

    assert result.return_code == 1
    assert "Timeout expired" in result.standard_error
