from ..core import Shell


class Bash(Shell):
    def _format_command(self, executable: str, args: list[str]) -> list[str]:
        # We no longer concatenate [executable] + args here.
        # Just return the args as they are; the base Shell class will handle the rest.
        return args
