from pathlib import Path


def test_resolve_path_relative(shell_stub, session_context):
    """Should resolve a relative path based on the context's CWD."""
    # Prepare the argument
    folder_name = "test_folder"
    args = [folder_name]

    resolved = shell_stub._resolve_path(args)

    # Expected path is context.cwd / folder_name
    expected = (session_context.cwd / folder_name).resolve()
    assert resolved == expected


def test_resolve_path_absolute(shell_stub):
    """Should respect an absolute path while ignoring the current CWD."""
    # Define an absolute path depending on the operating system
    absolute_str = "/tmp/data" if Path("/tmp").exists() else "C:\\Windows"
    args = [absolute_str]

    resolved = shell_stub._resolve_path(args)

    assert resolved == Path(absolute_str).resolve()
    assert resolved.is_absolute()


def test_resolve_path_home_default(shell_stub):
    """Should return the user's Home directory if the argument list is empty."""
    args = []

    resolved = shell_stub._resolve_path(args)

    expected = Path.home().resolve()
    assert resolved == expected


def test_resolve_path_with_tilde(shell_stub):
    """Should correctly expand the tilde (~) symbol."""
    args = ["~/documents"]

    resolved = shell_stub._resolve_path(args)

    expected = Path("~").expanduser().resolve() / "documents"
    assert resolved == expected


def test_resolve_path_complex_relative(shell_stub, session_context):
    """Should correctly handle level navigation (..)."""
    # Create a structure: e.g., /tmp/base/subdir -> ../other
    args = ["../other"]

    resolved = shell_stub._resolve_path(args)

    # It should go up one level from the fixture's CWD and append 'other'
    expected = (session_context.cwd.parent / "other").resolve()
    assert resolved == expected
