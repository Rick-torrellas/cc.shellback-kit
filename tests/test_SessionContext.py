import pytest
from pathlib import Path
from dataclasses import FrozenInstanceError
from CapsuleCore_shellback import SessionContext  # Asegúrate de importar correctamente


def test_session_context_defaults():
    """Verifica que los valores por defecto se asignan correctamente."""
    ctx = SessionContext()

    assert ctx.cwd == Path.cwd()
    assert ctx.env == {}
    assert ctx.encoding == "utf-8"


def test_session_context_custom_values():
    """Verifica la asignación de valores personalizados."""
    custom_cwd = Path("/tmp")
    custom_env = {"KEY": "VALUE"}

    ctx = SessionContext(cwd=custom_cwd, env=custom_env, encoding="ascii")

    assert ctx.cwd == custom_cwd
    assert ctx.env == custom_env
    assert ctx.encoding == "ascii"


def test_session_context_immutability():
    """Verifica que no se puedan modificar los atributos (frozen=True)."""
    ctx = SessionContext()

    with pytest.raises(FrozenInstanceError):
        ctx.encoding = "latin-1"
