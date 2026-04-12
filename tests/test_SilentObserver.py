# tests/test_silent_observer.py
import pytest
from cc_shellback_kit import Command
from cc_shellback_kit import SilentObserver

def test_silent_observer_execution_flow(bash_shell, tmp_path):
    """
    Verifica que el SilentObserver no interfiera en la ejecución 
    y soporte todos los hooks sin errores.
    """
    # 1. Instanciar el observador silencioso y asignarlo a la shell
    observer = SilentObserver()
    bash_shell.observer = observer

    # 2. Testear ciclo de vida completo (Context Manager)
    # Esto dispara on_session_start y on_session_end
    try:
        with bash_shell as sh:
            # 3. Testear comando de efecto (Ejecución externa)
            # Esto dispara on_command_start y on_command_result
            cmd_echo = Command("echo").add_args("hola")
            result = sh.run(cmd_echo)
            
            assert result.is_success()
            assert "hola" in result.standard_output

            # 4. Testear comando de estado (Virtual Builtin)
            # Esto dispara on_context_change (cwd)
            cmd_cd = Command("cd").add_args(str(tmp_path))
            sh.run(cmd_cd)
            
            assert sh.context.cwd == tmp_path

            # 5. Testear manejo de errores
            # Esto dispara on_error
            cmd_error = Command("comando_inexistente_xyz")
            res_err = sh.run(cmd_error)
            
            assert res_err.return_code == 127
            
    except Exception as e:
        pytest.fail(f"SilentObserver lanzó una excepción inesperada: {e}")

def test_silent_observer_direct_calls():
    """
    Test unitario puro: invocar los métodos directamente para asegurar 
    que las firmas coinciden con la interfaz base y no hacen nada.
    """
    observer = SilentObserver()
    
    # Si alguno de estos fallara, significaría que la firma en SilentObserver
    # o su clase base ShellObserver ha cambiado incorrectamente.
    assert observer.on_session_start("Bash") is None
    assert observer.on_context_change("key", "value") is None
    assert observer.on_command_start("ls", ["ls", "-la"]) is None
    assert observer.on_error("error message", Exception("test")) is None