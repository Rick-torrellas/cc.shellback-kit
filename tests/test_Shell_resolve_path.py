from pathlib import Path

def test_resolve_path_relative(shell_stub, session_context):
    """Debe resolver una ruta relativa basándose en el CWD del contexto."""
    # Preparamos el argumento
    folder_name = "test_folder"
    args = [folder_name]
    
    resolved = shell_stub._resolve_path(args)
    
    # La ruta esperada es context.cwd / folder_name
    expected = (session_context.cwd / folder_name).resolve()
    assert resolved == expected

def test_resolve_path_absolute(shell_stub):
    """Debe respetar una ruta absoluta ignorando el CWD actual."""
    absolute_str = "/tmp/data" if Path("/tmp").exists() else "C:\\Windows"
    args = [absolute_str]
    
    resolved = shell_stub._resolve_path(args)
    
    assert resolved == Path(absolute_str).resolve()
    assert resolved.is_absolute()

def test_resolve_path_home_default(shell_stub):
    """Debe devolver el Home del usuario si la lista de argumentos está vacía."""
    args = []
    
    resolved = shell_stub._resolve_path(args)
    
    expected = Path.home().resolve()
    assert resolved == expected

def test_resolve_path_with_tilde(shell_stub):
    """Debe expandir el símbolo ~ correctamente."""
    args = ["~/documents"]
    
    resolved = shell_stub._resolve_path(args)
    
    expected = Path("~").expanduser().resolve() / "documents"
    assert resolved == expected

def test_resolve_path_complex_relative(shell_stub, session_context):
    """Debe manejar navegación por niveles (..) correctamente."""
    # Creamos una estructura: /tmp/base/subdir -> ../other
    args = ["../other"]
    
    resolved = shell_stub._resolve_path(args)
    
    # Debe subir un nivel desde el CWD de la fixture y añadir 'other'
    expected = (session_context.cwd.parent / "other").resolve()
    assert resolved == expected