from typing import Any, Optional

class ArgumentBuilder:
    """Builds command-line argument lists with configurable flag style."""
    
    def __init__(self, style: str = "unix"):
        """Initialize the argument builder with the specified flag style.
        
        Args:
            style: Flag style - "unix" for --flag format or "ms" for /flag format
        """
        self._args = []
        self.style = style

    def add_flag(self, name: str, value: Optional[Any] = None):
        """Add a flag with optional value to the argument list.
        
        Args:
            name: The flag name without prefix
            value: Optional value to associate with the flag
            
        Returns:
            self for method chaining
        """
        prefix = "--" if self.style == "unix" else "/"
        if value is None:
            self._args.append(f"{prefix}{name}")
        else:
            self._args.extend([f"{prefix}{name}", str(value)])
        return self
        
    def build(self) -> list[str]:
        """Return the constructed argument list."""
        return self._args