import pytest
from unittest.mock import MagicMock
from cc_shellback_kit import CommandResult
from cc_shellback_kit import MultiObserver
from cc_shellback_kit import ShellObserver


@pytest.fixture
def mock_observers():
    """Creates a list of two mocked observers."""
    obs1 = MagicMock(spec=ShellObserver)
    obs2 = MagicMock(spec=ShellObserver)
    return [obs1, obs2]


@pytest.fixture
def multi_observer(mock_observers):
    """Instantiates the MultiObserver with the mocks."""
    return MultiObserver(observers=mock_observers)


def test_multi_observer_propagates_session_start(multi_observer, mock_observers):
    # Execution
    multi_observer.on_session_start("Bash")

    # Verification
    for obs in mock_observers:
        obs.on_session_start.assert_called_once_with("Bash")


def test_multi_observer_propagates_command_start(multi_observer, mock_observers):
    # Test data
    exe = "ls"
    args = ["ls", "-la"]

    # Execution
    multi_observer.on_command_start(exe, args)

    # Verification
    for obs in mock_observers:
        obs.on_command_start.assert_called_once_with(exe, args)


def test_multi_observer_propagates_command_result(multi_observer, mock_observers):
    # Test data
    result = CommandResult(standard_output="hola", return_code=0)

    # Execution
    multi_observer.on_command_result(result)

    # Verification
    for obs in mock_observers:
        obs.on_command_result.assert_called_once_with(result)


def test_multi_observer_propagates_context_change(multi_observer, mock_observers):
    # Execution
    multi_observer.on_context_change("cwd", "/tmp")

    # Verification
    for obs in mock_observers:
        obs.on_context_change.assert_called_once_with("cwd", "/tmp")


def test_multi_observer_add_observer_dynamically():
    """Verifies that observers can be added after initialization."""
    multi = MultiObserver()
    new_obs = MagicMock(spec=ShellObserver)

    multi.add_observer(new_obs)
    multi.on_error("test error")

    new_obs.on_error.assert_called_once_with("test error", None)


def test_multi_observer_empty_by_default():
    """Ensures it does not crash if no observers are registered."""
    multi = MultiObserver()
    # It should not raise any exceptions
    multi.on_session_start("TestShell")
    multi.on_command_result(CommandResult())
