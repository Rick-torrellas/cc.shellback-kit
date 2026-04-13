from cc_shellback_kit import FileLogObserver, Bash
from cc_shellback_kit import Command


def test_file_log_observer_lifecycle(tmp_path, session_context):
    """
    Test that FileLogObserver creates a log file and records
    session start, command execution, and session end.
    """
    # 1. Setup: Create a temporary log file path
    log_file = tmp_path / "test_activity.log"
    observer = FileLogObserver(log_path=str(log_file))

    # 2. Execution: Use the shell with the observer
    with Bash(context=session_context, observer=observer) as shell:
        cmd = Command("echo").add_args("hello_world")
        shell.run(cmd)

    # 3. Assertions
    assert log_file.exists(), "Log file should be created"

    log_content = log_file.read_text(encoding="utf-8")

    # Check for session lifecycle markers
    assert "=== SESSION START: Bash ===" in log_content
    assert "=== SESSION ENDED SUCCESSFULLY ===" in log_content

    # Check for command execution details
    assert "EXECUTING:" in log_content
    assert "echo hello_world" in log_content
    assert "RESULT: SUCCESS" in log_content
    assert "STDOUT: hello_world" in log_content


def test_file_log_observer_error_logging(tmp_path, session_context):
    log_file = tmp_path / "test_error.log"
    observer = FileLogObserver(log_path=str(log_file))

    shell = Bash(context=session_context, observer=observer)
    shell.run(Command("invalid_binary_xyz"))

    log_content = log_file.read_text(encoding="utf-8")

    # Cambia la aserción para buscar lo que realmente escribe on_error
    assert "SYSTEM ERROR: Command not found: invalid_binary_xyz" in log_content
    # Elimina o cambia el assert de FAILED(127) si no esperas que se ejecute el comando


def test_file_log_observer_propagation_disabled():
    """
    Verify that the logger does not propagate to avoid polluting console output.
    """
    observer = FileLogObserver("dummy.log")
    assert observer.logger.propagate is False
