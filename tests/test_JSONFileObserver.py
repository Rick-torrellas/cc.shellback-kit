import json
import pytest
from pathlib import Path
from cc_shellback_kit import Command, CommandResult
from cc_shellback_kit import JSONFileObserver


@pytest.fixture
def json_log_path(tmp_path):
    """Provides a temporary path for the JSON file."""
    return tmp_path / "test_audit.json"


@pytest.fixture
def observer(json_log_path):
    """Instance of the observer pointing to the temporary file."""
    return JSONFileObserver(log_path=str(json_log_path))


def test_json_observer_records_command_result(observer, json_log_path):
    # 1. Prepare a mock command result
    result = CommandResult(
        standard_output="Hello World",
        standard_error="",
        return_code=0,
        execution_time=0.1234,
        command_sent=["echo", "Hello World"],
    )

    # 2. Simulate the event
    observer.on_command_result(result)

    # 3. Verify file content
    with open(json_log_path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    assert len(logs) == 1
    entry = logs[0]
    assert entry["event"] == "command_executed"
    assert entry["success"] is True
    assert entry["command"] == ["echo", "Hello World"]
    assert entry["duration"] == 0.1234


def test_json_observer_records_context_change(observer, json_log_path):
    # Simulate directory change
    new_cwd = Path("/tmp/test")
    observer.on_context_change("cwd", new_cwd)

    with open(json_log_path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    assert len(logs) == 1
    assert logs[0]["event"] == "context_mutation"
    assert logs[0]["change"] == {"cwd": str(new_cwd)}


def test_json_observer_records_error(observer, json_log_path):
    # Simulate a system error
    error_msg = "Command not found"
    exception = Exception("File not found")

    observer.on_error(error_msg, exception)

    with open(json_log_path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    assert logs[0]["event"] == "internal_error"
    assert logs[0]["message"] == error_msg
    assert "File not found" in logs[0]["exception"]


def test_integration_with_shell(bash_shell, json_log_path):
    """
    Integration test: Verifies that when using the real Shell,
    the JSONFileObserver captures events automatically.
    """
    # Inject the JSON observer into the shell fixture
    observer = JSONFileObserver(log_path=str(json_log_path))
    bash_shell.observer = observer

    # Execute state and effect commands
    cmd_cd = Command("cd").add_args("/")
    bash_shell.run(cmd_cd)

    cmd_echo = Command("echo").add_args("test")
    bash_shell.run(cmd_echo)

    with open(json_log_path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    # There should be 2 entries: one for the cd (context_mutation) and one for the echo (command_executed)
    events = [log["event"] for log in logs]
    assert "context_mutation" in events
    assert "command_executed" in events
