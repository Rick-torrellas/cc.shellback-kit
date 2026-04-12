import pytest
import json
from cc_shellback_kit import CommandResult


def test_command_result_initialization():
    """Verifica que los valores por defecto se asignen correctamente."""
    result = CommandResult()
    assert result.standard_output == ""
    assert result.standard_error == ""
    assert result.return_code == 0
    assert result.execution_time == 0.0
    assert result.command_sent == []


def test_is_success_true():
    """Verifica que is_success() sea True cuando el código de retorno es 0."""
    result = CommandResult(return_code=0)
    assert result.is_success() is True


def test_is_success_false():
    """Verifica que is_success() sea False cuando el código de retorno no es 0."""
    result = CommandResult(return_code=1)
    assert result.is_success() is False

    result_error = CommandResult(return_code=127)
    assert result_error.is_success() is False


def test_json_parsing_success():
    """Verifica que el método json() parsee correctamente un string JSON."""
    data = {"status": "ok", "items": [1, 2, 3]}
    json_str = json.dumps(data)
    result = CommandResult(standard_output=json_str)

    assert result.json() == data
    assert result.json()["status"] == "ok"


def test_json_parsing_failure():
    """Verifica que el método json() lance un error con salida no válida."""
    result = CommandResult(standard_output="No soy un JSON")
    with pytest.raises(json.JSONDecodeError):
        result.json()


def test_pipe_operator_syntax():
    """
    Verifica el comportamiento del operador pipe (|).
    Según la implementación, debe devolver el stdout del comando anterior.
    """
    stdout_content = "datos de salida"
    result = CommandResult(standard_output=stdout_content)

    # En la implementación actual: CommandResult | Any -> str (standard_output)
    output = result | "otro_comando"

    assert output == stdout_content
    assert isinstance(output, str)


def test_complex_result_data():
    """Verifica la consistencia de un objeto con todos los campos llenos."""
    cmd = ["ls", "-la"]
    result = CommandResult(
        standard_output="total 0\n",
        standard_error="warning: low disk space",
        return_code=0,
        execution_time=0.1234,
        command_sent=cmd,
    )

    assert result.command_sent == cmd
    assert "total" in result.standard_output
    assert "warning" in result.standard_error
    assert result.execution_time == 0.1234
