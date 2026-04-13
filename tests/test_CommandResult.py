import pytest
import json
from cc_shellback_kit import CommandResult


def test_command_result_initialization():
    """Verify that default values are correctly assigned."""
    result = CommandResult()
    assert result.standard_output == ""
    assert result.standard_error == ""
    assert result.return_code == 0
    assert result.execution_time == 0.0
    assert result.command_sent == []


def test_is_success_true():
    """Verify that is_success() returns True when the return code is 0."""
    result = CommandResult(return_code=0)
    assert result.is_success() is True


def test_is_success_false():
    """Verify that is_success() returns False when the return code is not 0."""
    result = CommandResult(return_code=1)
    assert result.is_success() is False

    result_error = CommandResult(return_code=127)
    assert result_error.is_success() is False


def test_json_parsing_success():
    """Verify that the json() method correctly parses a JSON string."""
    data = {"status": "ok", "items": [1, 2, 3]}
    json_str = json.dumps(data)
    result = CommandResult(standard_output=json_str)

    assert result.json() == data
    assert result.json()["status"] == "ok"


def test_json_parsing_failure():
    """Verify that the json() method raises an error with invalid output."""
    result = CommandResult(standard_output="No soy un JSON")
    # Expecting a JSONDecodeError when parsing invalid strings
    with pytest.raises(json.JSONDecodeError):
        result.json()


def test_pipe_operator_syntax():
    """
    Verify the behavior of the pipe operator (|).
    According to the implementation, it should return the stdout of the previous command.
    """
    stdout_content = "datos de salida"
    result = CommandResult(standard_output=stdout_content)

    # In the current implementation: CommandResult | Any -> str (standard_output)
    output = result | "otro_comando"

    assert output == stdout_content
    assert isinstance(output, str)


def test_complex_result_data():
    """Verify the consistency of an object with all fields populated."""
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
