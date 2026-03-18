import pytest
import subprocess
from unittest.mock import MagicMock, patch
from CapsuleCore_shellback import Shell, CommandNotFoundError  # Ajusta el import


# 1. Implementación mínima para probar la clase abstracta
class ConcreteShell(Shell):
    def _format_command(self, executable: str, args: list[str]) -> list[str]:
        return [executable] + args


@pytest.fixture
def shell():
    mock_logger = MagicMock()
    mock_context = MagicMock()
    return ConcreteShell(logger=mock_logger, context=mock_context)


# 2. Mock del objeto Command
class MockCommand:
    def __init__(self, executable, args):
        self.executable = executable
        self.args = args


def test_shell_run_success(shell):
    command = MockCommand("ls", ["-l"])

    # Mockeamos shutil.which para que siempre encuentre el comando
    with (
        patch("shutil.which", return_value="/bin/ls"),
        patch("subprocess.run") as mock_run,
    ):
        # Configuramos el mock de subprocess
        mock_run.return_value = MagicMock(stdout="archivo.txt", stderr="", returncode=0)

        result = shell.run(command)

        assert result.return_code == 0
        assert result.standard_output == "archivo.txt"
        mock_run.assert_called_once()


def test_shell_command_not_found(shell):
    command = MockCommand("comando_inexistente", [])

    with patch("shutil.which", return_value=None):
        with pytest.raises(CommandNotFoundError):
            shell.run(command)


def test_shell_timeout(shell):
    command = MockCommand("sleep", ["10"])

    with (
        patch("shutil.which", return_value="/bin/sleep"),
        patch(
            "subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="sleep", timeout=1),
        ),
    ):
        with pytest.raises(subprocess.TimeoutExpired):
            shell.run(command, timeout=1)


def test_context_manager(shell):
    # Probamos __enter__ y __exit__
    shell.logger = MagicMock()

    with shell:
        assert shell.logger.info.called

    assert shell.logger.info.called
