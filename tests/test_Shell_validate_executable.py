import pytest
from unittest.mock import patch
from cc_shellback_kit import CommandNotFoundError

def test_validate_executable_success(shell_stub):
    """
    Verifica que si shutil.which encuentra el comando, 
    devuelve la ruta completa.
    """
    with patch("shutil.which") as mock_which:
        # Simulamos que encuentra el binario en una ruta típica
        mock_which.return_value = "/usr/bin/ls"
        
        result = shell_stub._validate_executable("ls")
        
        assert result == "/usr/bin/ls"
        mock_which.assert_called_once_with("ls")

def test_validate_executable_not_found(shell_stub):
    """
    Verifica que se lanza CommandNotFoundError si el binario no existe.
    """
    with patch("shutil.which") as mock_which:
        # Simulamos que no encuentra nada
        mock_which.return_value = None
        
        with pytest.raises(CommandNotFoundError) as excinfo:
            shell_stub._validate_executable("comando_fantasma")
        
        assert "Comando no encontrado: comando_fantasma" in str(excinfo.value)
        mock_which.assert_called_once_with("comando_fantasma")

def test_validate_executable_with_absolute_path(shell_stub):
    """
    Verifica que funciona correctamente incluso si el usuario 
    pasa una ruta absoluta que existe.
    """
    absolute_path = "/usr/local/bin/python3"
    with patch("shutil.which") as mock_which:
        mock_which.return_value = absolute_path
        
        result = shell_stub._validate_executable(absolute_path)
        
        assert result == absolute_path
        mock_which.assert_called_once_with(absolute_path)