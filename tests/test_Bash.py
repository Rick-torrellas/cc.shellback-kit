import pytest
from pathlib import Path
from unittest.mock import MagicMock
from dataclasses import replace

# Importamos las clases necesarias
# Nota: He usado la ruta completa basada en tu salida de pytest anterior
from CapsuleCore_shellback import Bash
from CapsuleCore_shellback import SessionContext


@pytest.fixture
def mock_context():
    """Crea un SessionContext simulado con un path base."""
    # Usamos una carpeta temporal real para que .resolve() y .exists() funcionen
    return SessionContext(cwd=Path("/tmp"), env={"PATH": "/usr/bin"}, encoding="utf-16")


@pytest.fixture
def set_cwd(bash_shell):
    """Fixture para actualizar el cwd de forma segura."""

    def _set_cwd(path):
        bash_shell.context = replace(bash_shell.context, cwd=path)
        return bash_shell

    return _set_cwd


@pytest.fixture
def bash_shell(mock_context):
    """Instancia la clase Bash inyectando mocks para evitar errores de dependencias."""
    # Creamos un mock para el logger.
    # Al pasar esto, el __init__ de Shell NO usará NullLogger()
    mock_logger = MagicMock()

    return Bash(context=mock_context, logger=mock_logger)


class TestBashShell:
    @pytest.mark.uno
    def test_format_command(self, bash_shell):
        """Verifica que los comandos se concatenen correctamente para Bash."""
        executable = "grep"
        args = ["-i", "pattern"]
        result = bash_shell._format_command(executable, args)

        assert result == ["grep", "-i", "pattern"]

    @pytest.mark.dos
    def test_cd_success(self, bash_shell, tmp_path):
        """Prueba un cambio de directorio exitoso usando una carpeta real temporal."""
        # Creamos una carpeta física en el sistema temporal de pytest
        target_dir = tmp_path / "subdir"
        target_dir.mkdir()

        # Seteamos el contexto inicial usando replace para respetar la inmutabilidad
        bash_shell.context = replace(bash_shell.context, cwd=tmp_path)

        # Ejecutamos el cambio de directorio
        bash_shell.cd("subdir")

        # Verificaciones
        assert bash_shell.context.cwd == target_dir.resolve()
        assert (
            bash_shell.context.encoding == "utf-16"
        )  # Verifica que mantuvo el estado previo

    @pytest.mark.tres
    def test_cd_not_found_raises_error(self, bash_shell):
        """Verifica que se lance FileNotFoundError si la ruta no existe."""
        with pytest.raises(FileNotFoundError) as excinfo:
            bash_shell.cd("ruta_fantasma_que_no_existe")

        assert "not found" in str(excinfo.value)

    @pytest.mark.cuatro
    def test_cd_is_not_a_directory(self, bash_shell, set_cwd, tmp_path):
        """Verifica que falle si intentamos hacer CD a un archivo en lugar de una carpeta."""
        fake_file = tmp_path / "not_a_dir.txt"
        fake_file.touch()

        # Usamos el fixture para actualizar el estado inmutable
        set_cwd(tmp_path)

        with pytest.raises(FileNotFoundError):
            bash_shell.cd("not_a_dir.txt")
