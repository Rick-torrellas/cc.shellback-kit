from .ArgumentBuilder import ArgumentBuilder

class Command:
    """Representa un comando ejecutable con sus argumentos."""

    def __init__(self, executable: str):
        self.executable = executable
        self.builder = ArgumentBuilder()

    def add_args(self, *args) -> "Command":
        """
        Añade argumentos posicionales. 
        Soporta elementos sueltos o listas gracias al nuevo builder.
        """
        for arg in args:
            self.builder.add_arg(arg)
        return self

    @property
    def args(self) -> list[str]:
        """Obtiene la lista de argumentos construida y validada."""
        return self.builder.build()