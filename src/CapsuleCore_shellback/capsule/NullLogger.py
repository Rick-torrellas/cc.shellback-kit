from ..core import Logger


class NullLogger(Logger):
    """
    'Null Object' pattern implementation.
    Performs no actions, allowing the Shell to function without constant null checks.
    """

    def info(self, message: str):
        """No-op informational logging."""
        pass

    def debug(self, message: str):
        """No-op debug logging."""
        pass

    def warning(self, message: str):
        """No-op warning logging."""
        pass

    def error(self, message: str):
        """No-op error logging."""
        pass
