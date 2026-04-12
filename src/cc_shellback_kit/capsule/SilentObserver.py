from ..core import ShellObserver


class SilentObserver(ShellObserver):
    """No hace nada. Ideal para scripts de producción donde no quieres ruido."""

    pass
