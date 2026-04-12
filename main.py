from src.cc_shellback_kit import Bash, ConsoleLogger, Command

logger = ConsoleLogger()
mkdir = Command("mkdir").add_args("olis")

with Bash(logger=logger) as sh:
    result = sh.run(mkdir)
    print(result.standard_output)
