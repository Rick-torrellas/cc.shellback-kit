from unittest.mock import patch, MagicMock
from cc_shellback_kit.core import Command


def test_run_virtual_builtin_cd(shell_stub, tmp_path):
    """Verifica que 'cd' cambie el contexto de la Shell sin ejecutar procesos externos."""
    # Create a physical directory for the test
    target_dir = tmp_path / "projects"
    target_dir.mkdir()

    # Define the 'cd' command with the target directory as an argument
    cmd = Command("cd").add_args(str(target_dir))

    # Execute the command through the shell stub
    result = shell_stub.run(cmd)

    # Validate that the command succeeded and the shell's working directory updated
    assert result.is_success()
    assert shell_stub.context.cwd == target_dir.resolve()

    # Verify that the observer was notified of the context change (CWD update)
    shell_stub.observer.on_context_change.assert_called_with(
        "cwd", target_dir.resolve()
    )


def test_run_virtual_builtin_export(shell_stub):
    """Verifica que 'export' actualice las variables de entorno en el contexto."""
    # Define an 'export' command to set environment variables
    cmd = Command("export").add_args("VERSION=1.0.0", "DEBUG=true")

    result = shell_stub.run(cmd)

    # Validate success and ensure variables are stored in the shell context
    assert result.is_success()
    assert shell_stub.context.env["VERSION"] == "1.0.0"
    assert shell_stub.context.env["DEBUG"] == "true"

    # Verify the observer was notified twice (once for each variable set)
    assert shell_stub.observer.on_context_change.call_count == 2


def test_run_external_command_success(shell_stub):
    """Verifica la ejecución exitosa de un comando del sistema (mockeado)."""
    # Define a standard system command (ls -la)
    cmd = Command("ls").add_args("-la")

    # Mock 'shutil.which' to simulate finding the binary and 'subprocess.run' for execution
    with (
        patch("shutil.which", return_value="/usr/bin/ls"),
        patch("subprocess.run") as mock_run,
    ):
        # Configure the mock to return a successful execution result
        mock_run.return_value = MagicMock(
            stdout="file1.txt\nfile2.txt", stderr="", returncode=0
        )

        result = shell_stub.run(cmd)

        # Assertions for output correctness and process execution
        assert result.is_success()
        assert "file1.txt" in result.standard_output
        mock_run.assert_called_once()

        # Verify observer notifications for command lifecycle (start and result)
        shell_stub.observer.on_command_start.assert_called()
        shell_stub.observer.on_command_result.assert_called_with(result)


def test_run_external_command_not_found(shell_stub):
    """Verifica el manejo de error cuando un comando no existe en el sistema."""
    # Define a command that does not exist
    cmd = Command("comando_fantasma")

    # Simulate 'shutil.which' failing to find the executable path
    with patch("shutil.which", return_value=None):
        result = shell_stub.run(cmd)

        # Assert that the shell returns a 127 error code (Standard for 'Command not found')
        assert not result.is_success()
        assert result.return_code == 127
        assert "Command not found" in result.standard_error

        # Ensure the observer's error handler was triggered
        shell_stub.observer.on_error.assert_called()


def test_run_with_custom_timeout(shell_stub):
    """Verifica que el timeout se pase correctamente al ejecutor externo."""
    # Define a command that would normally take a long time
    cmd = Command("sleep").add_args("10")
    custom_timeout = 5.0

    with (
        patch("shutil.which", return_value="/usr/bin/sleep"),
        patch("subprocess.run") as mock_run,
    ):
        # Run the command with an explicit timeout parameter
        shell_stub.run(cmd, timeout=custom_timeout)

        # Extract the keyword arguments passed to the subprocess call
        _, kwargs = mock_run.call_args
        # Verify that the custom timeout was correctly propagated to the system call
        assert kwargs["timeout"] == custom_timeout
