from pathlib import Path
from cc_shellback_kit.core import Command


def test_handle_cd_success(shell_stub, tmp_path):
    """Verifies that changing the directory updates the context and notifies the observer."""
    # 1. Prepare a real subdirectory using tmp_path
    subdir = tmp_path / "test_dir"
    subdir.mkdir()

    # Create the 'cd' command with the new directory as an argument
    cmd = Command("cd").add_args(str(subdir))

    # 2. Execute the command
    result = shell_stub.run(cmd)

    # 3. Assertions
    # Verify the command execution was successful
    assert result.is_success()
    # Verify the shell's Current Working Directory (CWD) was updated
    assert shell_stub.context.cwd == subdir.resolve()
    # Verify the observer was notified about the context change
    shell_stub.observer.on_context_change.assert_called_with("cwd", subdir.resolve())


def test_handle_cd_non_existent_directory(shell_stub):
    """Verifies that attempting to change to a non-existent directory returns an error."""
    # Store the initial CWD to verify it doesn't change later
    initial_cwd = shell_stub.context.cwd
    fake_path = "/path/that/does/not/exist/in/the/universe"

    # Create and run the command with a non-existent path
    cmd = Command("cd").add_args(fake_path)
    result = shell_stub.run(cmd)

    # 3. Assertions
    # The command should fail
    assert not result.is_success()
    assert result.return_code == 1
    # Check for the specific error message in stderr
    assert "Directory not found" in result.standard_error
    # Ensure the CWD remained unchanged
    assert shell_stub.context.cwd == initial_cwd
    # Verify the observer was notified of the error
    shell_stub.observer.on_error.assert_called()


def test_handle_cd_home_by_default(shell_stub):
    """Verifies that 'cd' without arguments points to the user's HOME."""
    # Create the command without any arguments
    cmd = Command("cd")

    result = shell_stub.run(cmd)

    # Verify success and that the path resolved to the user's home directory
    assert result.is_success()
    assert shell_stub.context.cwd == Path.home().resolve()


def test_handle_cd_relative_path(shell_stub, tmp_path):
    """Verifies that relative paths are resolved correctly with respect to the current CWD."""
    # Setup structure: tmp_path/folder_a/folder_b
    dir_a = tmp_path / "folder_a"
    dir_b = dir_a / "folder_b"
    dir_b.mkdir(parents=True)

    # Step 1: Navigate into folder_a using an absolute path
    shell_stub.run(Command("cd").add_args(str(dir_a)))

    # Step 2: Navigate into folder_b using a relative path
    result = shell_stub.run(Command("cd").add_args("folder_b"))

    # Assert that the relative path was resolved correctly based on the previous directory
    assert result
