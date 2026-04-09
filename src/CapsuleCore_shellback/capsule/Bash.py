from ..core import Shell


class Bash(Shell):
    """Implementación específica para Bash."""

    def _format_command(self, executable: str, args: list[str]) -> list[str]:
        # Aquí podrías añadir lógica si Bash necesitara prefijos especiales
        # como ['bash', '-c', ...] pero por ahora es directo.
        return [executable] + args
