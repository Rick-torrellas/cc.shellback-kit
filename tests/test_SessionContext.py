import pytest
from pathlib import Path
from cc_shellback_kit import SessionContext

def test_session_context_default_values():
    """Valida que los valores por defecto se asignen correctamente."""
    context = SessionContext()
    
    # El CWD por defecto debe ser el directorio actual del sistema
    assert context.cwd == Path.cwd()
    # El entorno debe ser un diccionario vacío por defecto
    assert context.env == {}
    # El encoding por defecto debe ser utf-8
    assert context.encoding == "utf-8"

def test_session_context_custom_values():
    """Valida la creación de un contexto con valores personalizados."""
    custom_path = Path("/tmp/test")
    custom_env = {"DEBUG": "1", "USER": "tester"}
    
    context = SessionContext(
        cwd=custom_path,
        env=custom_env,
        encoding="ascii"
    )
    
    assert context.cwd == custom_path
    assert context.env["DEBUG"] == "1"
    assert context.encoding == "ascii"

def test_session_context_immutability():
    """Verifica que el contexto sea inmutable (frozen=True)."""
    context = SessionContext()
    
    # Intentar modificar un atributo debería lanzar una excepción
    with pytest.raises(AttributeError):
        context.encoding = "utf-16"

def test_session_context_with_dataclasses_replace():
    """
    Verifica que se puedan crear copias modificadas usando replace.
    Este es el patrón que usa Shell.py para actualizar el estado.
    """
    from dataclasses import replace
    
    initial_context = SessionContext(encoding="utf-8")
    new_path = Path("/home/user")
    
    # Creamos un nuevo objeto basado en el anterior pero con el CWD cambiado
    updated_context = replace(initial_context, cwd=new_path)
    
    # El nuevo objeto tiene el cambio
    assert updated_context.cwd == new_path
    # El objeto original permanece intacto
    assert initial_context.cwd == Path.cwd()
    # Los valores no mencionados en replace se mantienen
    assert updated_context.encoding == "utf-8"