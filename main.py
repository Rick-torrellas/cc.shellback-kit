from src.shellback import Bash, ConsoleLogger,Command

logger = ConsoleLogger()
mkdir = Command("mkdir").add_args("olis")

with Bash(logger=logger) as sh:
    sh.run(mkdir)