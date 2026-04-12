from pathlib import Path
from cc_shellback_kit.core import Command

def test_handle_cd_success(shell_stub, tmp_path):
    """Verifica que el cambio de directorio actualice el contexto y notifique al observer."""
    # 1. Preparar un subdirectorio real
    subdir = tmp_path / "test_dir"
    subdir.mkdir()
    
    cmd = Command("cd").add_args(str(subdir))
    
    # 2. Ejecutar
    result = shell_stub.run(cmd)
    
    # 3. Aserciones
    assert result.is_success()
    assert shell_stub.context.cwd == subdir.resolve()
    # Verificar que se notificó al observer del cambio de contexto
    shell_stub.observer.on_context_change.assert_called_with("cwd", subdir.resolve())

def test_handle_cd_non_existent_directory(shell_stub):
    """Verifica que intentar cambiar a un directorio que no existe devuelva un error."""
    initial_cwd = shell_stub.context.cwd
    fake_path = "/path/que/no/existe/en/el/universo"
    
    cmd = Command("cd").add_args(fake_path)
    result = shell_stub.run(cmd)
    
    # 3. Aserciones
    assert not result.is_success()
    assert result.return_code == 1
    assert "no encontrado" in result.standard_error
    assert shell_stub.context.cwd == initial_cwd  # El CWD no debe haber cambiado
    # Verificar que se notificó el error
    shell_stub.observer.on_error.assert_called()

def test_handle_cd_home_by_default(shell_stub):
    """Verifica que 'cd' sin argumentos apunte al HOME del usuario."""
    cmd = Command("cd") # Sin argumentos
    
    result = shell_stub.run(cmd)
    
    assert result.is_success()
    assert shell_stub.context.cwd == Path.home().resolve()

def test_handle_cd_relative_path(shell_stub, tmp_path):
    """Verifica que las rutas relativas se resuelvan correctamente respecto al CWD actual."""
    # Estructura: tmp_path/folder_a/folder_b
    dir_a = tmp_path / "folder_a"
    dir_b = dir_a / "folder_b"
    dir_b.mkdir(parents=True)
    
    # Primero entramos a folder_a
    shell_stub.run(Command("cd").add_args(str(dir_a)))
    
    # Ahora entramos a folder_b usando ruta relativa
    result = shell_stub.run(Command("cd").add_args("folder_b"))
    
    assert result.is_success()
    assert shell_stub.context.cwd == dir_b.resolve()