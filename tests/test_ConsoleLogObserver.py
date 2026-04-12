import pytest
from cc_shellback_kit import ConsoleLogObserver
from cc_shellback_kit import CommandResult


class TestConsoleLogObserver:
    @pytest.fixture
    def observer(self):
        return ConsoleLogObserver()

    def test_on_command_start_prints_executable_and_args(self, observer, capsys):
        """Verifica que se imprima el comando y sus argumentos al iniciar."""
        executable = "ls"
        final_args = ["ls", "-l", "/home"]

        observer.on_command_start(executable, final_args)

        captured = capsys.readouterr()
        assert "🛠️  Ejecutando: ls -l /home" in captured.out

    def test_on_command_result_success(self, observer, capsys):
        """Verifica el mensaje de éxito cuando el código de retorno es 0."""
        result = CommandResult(
            standard_output="hola", return_code=0, execution_time=0.1234
        )

        observer.on_command_result(result)

        captured = capsys.readouterr()
        assert "✅ OK (0.123s)" in captured.out

    def test_on_command_result_failure_with_error_message(self, observer, capsys):
        """Verifica el mensaje de fallo y la impresión del stderr."""
        result = CommandResult(
            standard_error="Permiso denegado", return_code=1, execution_time=0.005
        )

        observer.on_command_result(result)

        captured = capsys.readouterr()
        assert "❌ FALLO (Código: 1)" in captured.out
        assert "Error: Permiso denegado" in captured.out

    def test_on_command_result_failure_without_stderr(self, observer, capsys):
        """Verifica que no falle si el error no tiene mensaje en stderr."""
        result = CommandResult(standard_error="", return_code=127)

        observer.on_command_result(result)

        captured = capsys.readouterr()
        assert "❌ FALLO (Código: 127)" in captured.out
        # No debería intentar imprimir la línea de "Error:" si está vacío
        assert "Error:" not in captured.out
