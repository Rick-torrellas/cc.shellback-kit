from cc_shellback_kit import Command


def test_shell_notifies_observer_on_command(bash_shell, mock_observer):
    """Verifica que la shell llame a los métodos del observer durante el ciclo de vida."""
    cmd = Command("ls")

    # Ejecutamos dentro del contexto para disparar session_start/end
    with bash_shell:
        bash_shell.run(cmd)

    # Verificamos llamadas en orden
    assert mock_observer.on_session_start.called
    assert mock_observer.on_command_start.called
    assert mock_observer.on_command_result.called
    assert mock_observer.on_session_end.called


def test_shell_notifies_context_change(bash_shell, mock_observer, tmp_path):
    """Verifica que 'cd' notifique el cambio de contexto."""
    cmd = Command("cd").add_args(str(tmp_path))

    bash_shell.run(cmd)

    # El observer debe haber recibido la notificación del cambio de CWD
    mock_observer.on_context_change.assert_called_with("cwd", tmp_path)
