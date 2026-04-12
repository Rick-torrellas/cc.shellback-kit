import json
import pytest
from pathlib import Path
from cc_shellback_kit import Command, CommandResult
from cc_shellback_kit import JSONFileObserver

@pytest.fixture
def json_log_path(tmp_path):
    """Proporciona una ruta temporal para el archivo JSON."""
    return tmp_path / "test_audit.json"

@pytest.fixture
def observer(json_log_path):
    """Instancia del observador apuntando al archivo temporal."""
    return JSONFileObserver(log_path=str(json_log_path))

def test_json_observer_records_command_result(observer, json_log_path):
    # 1. Preparar un resultado de comando ficticio
    result = CommandResult(
        standard_output="Hello World",
        standard_error="",
        return_code=0,
        execution_time=0.1234,
        command_sent=["echo", "Hello World"]
    )

    # 2. Simular el evento
    observer.on_command_result(result)

    # 3. Verificar el contenido del archivo
    with open(json_log_path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    assert len(logs) == 1
    entry = logs[0]
    assert entry["event"] == "command_executed"
    assert entry["success"] is True
    assert entry["command"] == ["echo", "Hello World"]
    assert entry["duration"] == 0.1234

def test_json_observer_records_context_change(observer, json_log_path):
    # Simular cambio de directorio
    new_cwd = Path("/tmp/test")
    observer.on_context_change("cwd", new_cwd)

    with open(json_log_path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    assert len(logs) == 1
    assert logs[0]["event"] == "context_mutation"
    assert logs[0]["change"] == {"cwd": str(new_cwd)}

def test_json_observer_records_error(observer, json_log_path):
    # Simular un error del sistema
    error_msg = "Comando no encontrado"
    exception = Exception("File not found")
    
    observer.on_error(error_msg, exception)

    with open(json_log_path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    assert logs[0]["event"] == "internal_error"
    assert logs[0]["message"] == error_msg
    assert "File not found" in logs[0]["exception"]

def test_integration_with_shell(bash_shell, json_log_path):
    """
    Test de integración: Verifica que al usar la Shell real, 
    el JSONFileObserver capture los eventos automáticamente.
    """
    # Inyectamos el JSON observer en la shell de la fixture
    observer = JSONFileObserver(log_path=str(json_log_path))
    bash_shell.observer = observer

    # Ejecutamos comandos de estado y de efecto
    cmd_cd = Command("cd").add_args("/")
    bash_shell.run(cmd_cd)
    
    cmd_echo = Command("echo").add_args("test")
    bash_shell.run(cmd_echo)

    with open(json_log_path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    # Debería haber 2 entradas: una por el cd (context_mutation) y otra por el echo (command_executed)
    events = [log["event"] for log in logs]
    assert "context_mutation" in events
    assert "command_executed" in events