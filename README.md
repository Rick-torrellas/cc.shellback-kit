# CapsuleCore shellback

Shellback is a robust, architecturally-agnostic Python library designed to bridge terminal environments (Bash, CMD, PowerShell) with Python scripts. It provides a clean, decoupled abstraction layer to execute system commands while maintaining persistent session state and cross-platform compatibility.

Built with Hexagonal Architecture (Ports and Adapters) principles, Shellback ensures that your domain logic remains independent of the specific shell or operating system being used.

## Usage

```python

from CapsuleCore_shellback import Bash, ConsoleLogger,Command

logger = ConsoleLogger()
mkdir = Command("mkdir").add_args("dir")

with Bash(logger=logger) as sh:
    result = sh.run(mkdir)
    if result.is_success():
        print("Directory created successfully.")
    else:
        print("Error creating directory.")
```        


## Key Features

Agnostic Design: Decouple your application logic from the underlying shell implementation.

Persistent Session State: Maintain working directories (cwd), environment variables, and encodings across multiple executions using SessionContext.

Fluent Command Builder: Construct complex commands with a declarative and chainable API via ArgumentBuilder and Command.

Safe Execution: Automatic validation of executables in the system PATH before execution.

Flexible Logging: Swappable logging backends (Console, Null, or custom) using the Strategy and Null Object patterns.

Pipe-like Syntax: Easy integration between command results using the | operator.

