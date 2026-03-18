from .ArgumentBuilder import ArgumentBuilder


class Command:
    """Represents a command with its executable and configurable arguments."""

    def __init__(self, executable: str):
        """Initialize a command with the specified executable.

        Args:
            executable: The command executable name or path
        """
        self.executable = executable
        self.builder = ArgumentBuilder()

    def add_args(self, *args):
        """Add positional arguments to the command.

        Args:
            *args: Variable number of argument strings to append

        Returns:
            self for method chaining
        """
        for arg in args:
            self.builder._args.append(arg)
        return self

    @property
    def args(self):
        """Get the fully constructed argument list."""
        return self.builder.build()
