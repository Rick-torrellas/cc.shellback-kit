from cc_shellback_kit import Command


def test_shell_notifies_observer_on_command(bash_shell, mock_observer):
    """Verifica que la shell llame a los métodos del observer durante el ciclo de vida."""
    # Define a simple command to execute
    cmd = Command("ls")

    # Use the shell as a context manager to trigger session_start and session_end hooks
    with bash_shell:
        # Execute the command within the shell
        bash_shell.run(cmd)

    # Verify that the observer's lifecycle methods were called in the expected sequence
    assert mock_observer.on_session_start.called
    assert mock_observer.on_command_start.called
    assert mock_observer.on_command_result.called
    assert mock_observer.on_session_end.called


def test_shell_notifies_context_change(bash_shell, mock_observer, tmp_path):
    """Verifica que 'cd' notifique el cambio de contexto."""
    # Prepare a 'cd' command with a temporary directory path as an argument
    cmd = Command("cd").add_args(str(tmp_path))

    # Execute the directory change command
    bash_shell.run(cmd)

    # Verify that the observer was notified specifically about the CWD (Current Working Directory) change
    mock_observer.on_context_change.assert_called_with("cwd", tmp_path)
