import pytest
import json
from CapsuleCore_shellback import CommandResult


def test_command_result_success_state():
    """Verifica que is_success identifique correctamente códigos de salida."""
    result_ok = CommandResult(return_code=0)
    result_error = CommandResult(return_code=1)
    result_not_found = CommandResult(return_code=127)

    assert result_ok.is_success() is True
    assert result_error.is_success() is False
    assert result_not_found.is_success() is False


def test_command_result_json_parsing():
    """Verifica la conversión de stdout a diccionario/lista."""
    data = {"status": "ok", "items": [1, 2, 3]}
    result = CommandResult(standard_output=json.dumps(data))

    parsed = result.json()
    assert parsed["status"] == "ok"
    assert len(parsed["items"]) == 3
    assert isinstance(parsed, dict)


def test_command_result_json_error():
    """Verifica que falle si el stdout no es JSON válido."""
    result = CommandResult(standard_output="No soy un JSON")

    with pytest.raises(json.JSONDecodeError):
        result.json()


def test_command_result_pipe_operator():
    """Verifica que el operador | retorne el stdout (comportamiento de pipe)."""
    expected_output = "lista_de_archivos.txt"
    result = CommandResult(standard_output=expected_output)

    # En la implementación actual, result | Any devuelve el string de stdout
    piped_data = result | "grep algo"

    assert piped_data == expected_output


def test_command_result_defaults():
    """Verifica que los valores por defecto sean coherentes."""
    result = CommandResult()

    assert result.standard_output == ""
    assert result.standard_error == ""
    assert result.return_code == 0
    assert result.command_sent == []
    assert isinstance(result.execution_time, float)
