from ..core import ShellObserver


class SilentObserver(ShellObserver):
    """Does nothing. Ideal for production scripts where you don't want noise."""

    pass
