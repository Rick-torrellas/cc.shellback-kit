import pytest
from pathlib import Path
from cc_shellback_kit import SessionContext


def test_session_context_default_values():
    """Validate that default values are correctly assigned."""
    context = SessionContext()

    # The default CWD should be the system's current working directory
    assert context.cwd == Path.cwd()
    # The environment should be an empty dictionary by default
    assert context.env == {}
    # The default encoding should be utf-8
    assert context.encoding == "utf-8"


def test_session_context_custom_values():
    """Validate the creation of a context with custom values."""
    custom_path = Path("/tmp/test")
    custom_env = {"DEBUG": "1", "USER": "tester"}

    context = SessionContext(cwd=custom_path, env=custom_env, encoding="ascii")

    assert context.cwd == custom_path
    assert context.env["DEBUG"] == "1"
    assert context.encoding == "ascii"


def test_session_context_immutability():
    """Verify that the context is immutable (frozen=True)."""
    context = SessionContext()

    # Attempting to modify an attribute should raise an AttributeError
    with pytest.raises(AttributeError):
        context.encoding = "utf-16"


def test_session_context_with_dataclasses_replace():
    """
    Verify that modified copies can be created using the 'replace' function.
    This is the pattern used by Shell.py to update the state.
    """
    from dataclasses import replace

    initial_context = SessionContext(encoding="utf-8")
    new_path = Path("/home/user")

    # Create a new object based on the previous one but with a changed CWD
    updated_context = replace(initial_context, cwd=new_path)

    # The new object contains the change
    assert updated_context.cwd == new_path
    # The original object remains untouched
    assert initial_context.cwd == Path.cwd()
    # Values not specified in 'replace' are maintained
    assert updated_context.encoding == "utf-8"
