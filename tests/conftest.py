# conftest.py
import pytest
from unittest.mock import MagicMock

# Asegúrate de que las rutas de importación coincidan con tu nueva estructura
from cc_shellback_kit.core import Shell, ShellObserver, SessionContext
from cc_shellback_kit.capsule import Bash


class ShellStub(Shell):
    """Implementación mínima para testear la clase base Shell."""

    def _format_command(self, executable: str, args: list[str]) -> list[str]:
        # Simplemente devolvemos los argumentos para verificar la lógica de aplanamiento
        return args


@pytest.fixture
def mock_observer():
    """Fixture que proporciona un observer mockeado para verificar llamadas."""
    return MagicMock(spec=ShellObserver)


@pytest.fixture
def session_context(tmp_path):
    """Fixture para un contexto de sesión controlado con un CWD temporal."""
    return SessionContext(cwd=tmp_path)


@pytest.fixture
def shell_stub(mock_observer, session_context):
    """Proporciona una instancia de ShellStub lista para testear."""
    return ShellStub(context=session_context, observer=mock_observer)


@pytest.fixture
def bash_shell(mock_observer, session_context):
    """Proporciona una instancia real de la implementación Bash."""
    return Bash(context=session_context, observer=mock_observer)
