# tests/test_silent_observer.py
import pytest
from cc_shellback_kit import Command
from cc_shellback_kit import SilentObserver


def test_silent_observer_execution_flow(bash_shell, tmp_path):
    """
    Verifies that the SilentObserver does not interfere with execution
    and supports all hooks without errors.
    """
    # 1. Instantiate the silent observer and assign it to the shell
    observer = SilentObserver()
    bash_shell.observer = observer

    # 2. Test full lifecycle (Context Manager)
    # This triggers on_session_start and on_session_end
    try:
        with bash_shell as sh:
            # 3. Test effect command (External execution)
            # This triggers on_command_start and on_command_result
            cmd_echo = Command("echo").add_args("hola")
            result = sh.run(cmd_echo)

            assert result.is_success()
            assert "hola" in result.standard_output

            # 4. Test state command (Virtual Builtin)
            # This triggers on_context_change (cwd)
            cmd_cd = Command("cd").add_args(str(tmp_path))
            sh.run(cmd_cd)

            assert sh.context.cwd == tmp_path

            # 5. Test error handling
            # This triggers on_error
            cmd_error = Command("comando_inexistente_xyz")
            res_err = sh.run(cmd_error)

            assert res_err.return_code == 127

    except Exception as e:
        pytest.fail(f"SilentObserver raised an unexpected exception: {e}")


def test_silent_observer_direct_calls():
    """
    Pure unit test: invoke methods directly to ensure signatures
    match the base interface and perform no actions (no-op).
    """
    observer = SilentObserver()

    # If any of these fail, it indicates that the signature in SilentObserver
    # or its base class ShellObserver has changed incorrectly.
    assert observer.on_session_start("Bash") is None
    assert observer.on_context_change("key", "value") is None
    assert observer.on_command_start("ls", ["ls", "-la"]) is None
    assert observer.on_error("error message", Exception("test")) is None
