import pytest
from unittest.mock import MagicMock, patch
from CapsuleCore_shellback import ShellObserver, Bash


@pytest.fixture
def mock_subprocess():
    with patch("subprocess.run") as mocked_run:
        # Configuramos un retorno por defecto exitoso
        mocked_run.return_value = MagicMock(
            stdout="output de prueba", stderr="", returncode=0
        )
        yield mocked_run


@pytest.fixture
def mock_binaries():
    with patch("shutil.which") as mocked_which:
        # Simulamos que cualquier comando que busquemos existe en /usr/bin/
        mocked_which.side_effect = lambda x: f"/usr/bin/{x}"
        yield mocked_which


@pytest.fixture
def spy_observer():
    # Creamos un mock que hereda de la interfaz para asegurar compatibilidad
    observer = MagicMock(spec=ShellObserver)
    return observer


@pytest.fixture
def shell(mock_subprocess, mock_binaries, spy_observer):
    return Bash(observer=spy_observer)
