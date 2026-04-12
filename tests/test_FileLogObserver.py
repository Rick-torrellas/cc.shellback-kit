import pytest
from cc_shellback_kit import FileLogObserver
from cc_shellback_kit import CommandResult


@pytest.fixture
def log_file(tmp_path):
    """Crea una ruta temporal para el archivo de log."""
    return tmp_path / "test_shell.log"


@pytest.fixture
def observer(log_file):
    """Instancia el observador con la ruta temporal."""
    return FileLogObserver(log_path=str(log_file))


def test_on_session_start_writes_to_file(observer, log_file):
    observer.on_session_start("Bash")

    # Si sigue fallando, añade esta línea para forzar el cierre antes de leer:
    for h in observer.logger.handlers:
        h.flush()  # noqa: E701

    content = log_file.read_text(encoding="utf-8")
    assert "=== INICIO DE SESIÓN: Bash ===" in content


def test_on_command_start_logs_full_command(observer, log_file):
    # Act
    observer.on_command_start("ls", ["ls", "-la", "/tmp"])

    # Assert
    content = log_file.read_text(encoding="utf-8")
    assert "EJECUTANDO: ls -la /tmp" in content


def test_on_command_result_success(observer, log_file):
    # Arrange
    result = CommandResult(
        standard_output="file1.txt\nfile2.txt", return_code=0, execution_time=0.12345
    )

    # Act
    observer.on_command_result(result)

    # Assert
    content = log_file.read_text(encoding="utf-8")
    assert "RESULTADO: SUCCESS" in content
    assert "DURACIÓN: 0.1235s" in content  # Verificamos redondeo
    assert "STDOUT: file1.txt" in content


def test_on_command_result_failure(observer, log_file):
    # Arrange
    result = CommandResult(
        standard_error="Permission denied", return_code=1, execution_time=0.05
    )

    # Act
    observer.on_command_result(result)

    # Assert
    content = log_file.read_text(encoding="utf-8")
    assert "RESULTADO: FAILED(1)" in content


def test_on_error_logs_exception_details(observer, log_file):
    # Arrange
    error = ValueError("Conexión perdida")

    # Act
    observer.on_error("Error crítico de red", error)

    # Assert
    content = log_file.read_text(encoding="utf-8")
    assert "ERROR DEL SISTEMA: Error crítico de red" in content
    assert "Detalle: Conexión perdida" in content


def test_on_session_end_with_error(observer, log_file):
    # Act
    observer.on_session_end("Bash", error=RuntimeError("Crash"))

    # Assert
    content = log_file.read_text(encoding="utf-8")
    assert "ERROR" in content
    assert "=== FIN DE SESIÓN CON ERROR: Crash ===" in content


def test_on_session_end_clean(observer, log_file):
    # Act
    observer.on_session_end("Bash")

    # Assert
    content = log_file.read_text(encoding="utf-8")
    assert "=== FIN DE SESIÓN EXITOSO ===" in content
