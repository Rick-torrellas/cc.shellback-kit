from pathlib import Path
from ..core import Shell, SessionContext


class Bash(Shell):
    """Bash shell implementation with path navigation support."""
    
    def _format_command(self, executable: str, args: list[str]) -> list[str]:
        """Formats a command for Bash execution.
        
        Args:
            executable: The command executable name or path
            args: List of command arguments
            
        Returns:
            List containing the executable and arguments formatted for Bash
        """
        return [executable] + args

    def cd(self, path: str | Path):
        """Virtually updates the shell context by changing the current working directory.
        
        Args:
            path: Target directory path relative to current working directory
            
        Raises:
            FileNotFoundError: If the resolved path doesn't exist or is not a directory
            
        Note:
            Creates a new SessionContext instance due to frozen dataclass immutability
        """
        new_path = (self.context.cwd / path).resolve()
        if new_path.exists() and new_path.is_dir():
            self.context = SessionContext(
                cwd=new_path, 
                env=self.context.env, 
                encoding=self.context.encoding
            )
        else:
            raise FileNotFoundError(f"Directory {new_path} not found")