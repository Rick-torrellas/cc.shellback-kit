from pathlib import Path
from ..core import Shell,SessionContext


class Bash(Shell):
    def _format_command(self, executable: str, args: list[str]) -> list[str]:
        # En Bash, usualmente es directo, pero aquí podríamos manejar
        # escapes específicos si fuera necesario.
        return [executable] + args

    def cd(self, path: str | Path):
        """Actualiza el contexto virtualmente."""
        new_path = (self.context.cwd / path).resolve()
        if new_path.exists() and new_path.is_dir():
            # Re-instanciar el contexto (es inmutable por el dataclass frozen)
            self.context = SessionContext(
                cwd=new_path, 
                env=self.context.env, 
                encoding=self.context.encoding
            )
        else:
            raise FileNotFoundError(f"Directory {new_path} not found")