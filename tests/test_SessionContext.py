import pytest
from pathlib import Path
from CapsuleCore_shellback import SessionContext


def test_session_context_default_values():
    """Verifica que los valores por defecto se asignen correctamente."""
    context = SessionContext()

    assert isinstance(context.cwd, Path)
    assert context.cwd == Path.cwd()
    assert context.env == {}
    assert context.encoding == "utf-8"


def test_session_context_custom_values():
    """Verifica la asignación de valores personalizados."""
    custom_path = Path("/tmp")
    custom_env = {"DEBUG": "1", "USER": "test_user"}
    custom_encoding = "latin-1"

    context = SessionContext(cwd=custom_path, env=custom_env, encoding=custom_encoding)

    assert context.cwd == custom_path
    assert context.env["DEBUG"] == "1"
    assert context.encoding == "latin-1"


def test_session_context_immutability():
    """
    Verifica que la clase sea inmutable (frozen=True).
    Cualquier intento de modificar un atributo debe lanzar FrozenInstanceError.
    """
    context = SessionContext()

    with pytest.raises(
        AttributeError
    ):  # En dataclasses frozen, lanza AttributeError al intentar setear
        context.encoding = "ascii"

    with pytest.raises(AttributeError):
        context.cwd = Path("/bin")


def test_session_context_env_is_isolated():
    """Verifica que el diccionario de entorno no sea compartido entre instancias."""
    ctx1 = SessionContext(env={"VAR": "1"})
    ctx2 = SessionContext()

    assert "VAR" not in ctx2.env
    assert ctx1.env is not ctx2.env


def test_session_context_repr():
    """Verifica que la representación en cadena sea legible (útil para debugging)."""
    context = SessionContext(encoding="utf-16")
    repr_str = repr(context)

    assert "SessionContext" in repr_str
    assert "encoding='utf-16'" in repr_str
