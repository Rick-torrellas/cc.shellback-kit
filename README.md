# CapsuleCore shellback

Shellback is a robust, architecturally-agnostic Python library designed to bridge terminal environments (Bash, CMD, PowerShell) with Python scripts. It provides a clean, decoupled abstraction layer to execute system commands while maintaining persistent session state and cross-platform compatibility.

Built with Hexagonal Architecture (Ports and Adapters) principles, Shellback ensures that your domain logic remains independent of the specific shell or operating system being used.

## Usage

```python

from pathlib import Path
from capsulecore_shellback.core import Command
from capsulecore_shellback.shells import Bash

# 1. Instanciar la Shell (Bash)
with Bash() as shell:
    # 2. Crear el comando
    cmd = Command("ls").add_args("-la")
    
    # 3. Ejecutar
    result = shell.run(cmd)

    # 4. Leer resultados
    if result.is_success():
        print(f"Salida:\n{result.standard_output}")
        print(f"Tiempo de ejecución: {result.execution_time:.4f}s")
```        

### Ejecutando un Comando

```python
from pathlib import Path
from capsulecore_shellback.core import Command
from capsulecore_shellback.shells import Bash

# 1. Instanciar la Shell (Bash)
with Bash() as shell:
    # 2. Crear el comando
    cmd = Command("ls").add_args("-la")
    
    # 3. Ejecutar
    result = shell.run(cmd)

    # 4. Leer resultados
    if result.is_success():
        print(f"Salida:\n{result.standard_output}")
        print(f"Tiempo de ejecución: {result.execution_time:.4f}s")
```

### Gestión de Argumentos y Flags

```python
from capsulecore_shellback.core import Command

# Construcción fluida de: git commit -m "feat: initial commit" --rebase
git_cmd = (
    Command("git")
    .add_args("commit")
    .add_args("-m", "feat: initial commit")
)
git_cmd.builder.add_flag("rebase")

print(git_cmd.args) 
# Resultado: ['commit', '-m', 'feat: initial commit', '--rebase']
```

### Manejo de Contexto y Directorios

```python
from capsulecore_shellback.shells import Bash

with Bash() as shell:
    # Cambiar de directorio virtualmente
    shell.cd("src")
    
    # El comando se ejecutará dentro de /actual/path/src
    result = shell.run(Command("pwd"))
    print(f"Directorio actual: {result.standard_output.strip()}")
```




## Key Features

Agnostic Design: Decouple your application logic from the underlying shell implementation.

Persistent Session State: Maintain working directories (cwd), environment variables, and encodings across multiple executions using SessionContext.

Fluent Command Builder: Construct complex commands with a declarative and chainable API via ArgumentBuilder and Command.

Safe Execution: Automatic validation of executables in the system PATH before execution.

Flexible Logging: Swappable logging backends (Console, Null, or custom) using the Strategy and Null Object patterns.

Pipe-like Syntax: Easy integration between command results using the | operator.

