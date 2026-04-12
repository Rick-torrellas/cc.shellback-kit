from ..core import Shell


class Bash(Shell):
    def _format_command(self, executable: str, args: list[str]) -> list[str]:
        # Ya no concatenamos [executable] + args aquí.
        # Solo devolvemos los args tal cual, la Shell base hará el resto.
        return args
