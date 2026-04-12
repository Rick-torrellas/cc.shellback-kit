from ..core import CommandResult, ShellObserver


class ConsoleLogObserver(ShellObserver):
    """Muestra en consola lo que está pasando en tiempo real."""

    def on_command_start(self, executable, final_args):
        print(f"🛠️  Ejecutando: {' '.join(final_args)}")

    def on_command_result(self, result: CommandResult):
        if result.is_success():
            print(f"✅ OK ({result.execution_time:.3f}s)")
        else:
            print(f"❌ FALLO (Código: {result.return_code})")
            if result.standard_error:
                print(f"   Error: {result.standard_error.strip()}")
