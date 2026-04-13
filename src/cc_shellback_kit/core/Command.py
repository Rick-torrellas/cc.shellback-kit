from .ArgumentBuilder import ArgumentBuilder


class Command:
    """Represents an executable command with its arguments."""

    def __init__(self, executable: str):
        # Initialize the command with the path/name of the executable
        self.executable = executable
        # Initialize the helper builder to manage command-line arguments
        self.builder = ArgumentBuilder()

    def add_args(self, *args) -> "Command":
        """
        Adds positional arguments.
        Supports individual items or lists thanks to the new builder.
        """
        # Iterate through provided arguments and add them via the builder
        for arg in args:
            self.builder.add_arg(arg)
        # Return self to allow method chaining (fluent interface)
        return self

    @property
    def args(self) -> list[str]:
        """Gets the constructed and validated list of arguments."""
        # Delegate the final list generation to the builder's build method
        return self.builder.build()
