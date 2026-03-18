import json
from CapsuleCore_shellback import CommandResult


def test_command_result_success():
    # Probando inicialización y éxito
    res = CommandResult(return_code=0, standard_output="ok")
    assert res.is_success() is True


def test_command_result_failure():
    # Probando fallo
    res = CommandResult(return_code=1, standard_error="error fatal")
    assert res.is_success() is False


def test_json_parsing():
    # Probando lectura de JSON
    data = {"id": 1, "task": "deploy"}
    res = CommandResult(standard_output=json.dumps(data))

    assert res.json() == data
    assert res.json()["task"] == "deploy"


def test_pipe_behavior():
    # Probando el operador |
    res = CommandResult(standard_output="pipeline_data")
    result = res | "some_next_command"
    assert result == "pipeline_data"


def test_default_values():
    # Verificando que los defaults funcionen correctamente
    res = CommandResult()
    assert res.return_code == 0
    assert res.command_sent == []  # Verifica que la lista sea nueva para cada objeto
