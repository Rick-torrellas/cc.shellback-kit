# CapsuleCore shellback

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Version](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Rick-torrellas/cc-shellback-kit/badges/version.json)
[![CI CD](https://github.com/Rick-torrellas/cc-shellback-kit/actions/workflows/main.yaml/badge.svg)](https://github.com/Rick-torrellas/cc-shellback-kit/actions/workflows/main.yaml)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Download](https://img.shields.io/github/v/release/Rick-torrellas/cc-shellback-kit?label=Download&color=orange)](https://github.com/Rick-torrellas/cc-shellback-kit/releases)
[![Ask DeepWiki](https://img.shields.io/badge/DeepWiki-Documentation-blue?logo=gitbook&logoColor=white)](https://deepwiki.com/Rick-torrellas/cc-shellback-kit)

Shellback is a robust, architecturally-agnostic Python library designed to bridge terminal environments (Bash, CMD, PowerShell) with Python scripts. It provides a clean, decoupled abstraction layer to execute system commands while maintaining persistent session state and cross-platform compatibility.

Built with Hexagonal Architecture (Ports and Adapters) principles, Shellback ensures that your domain logic remains independent of the specific shell or operating system being used.

---



## Usage

```python
from cc_shellback_kit import Bash, ConsoleLogObserver, Command, SessionContext

# 1. Configuramos el observador para ver la actividad en consola
observer = ConsoleLogObserver()

# 2. Iniciamos la Shell usando el manejador de contexto (with)
with Bash(observer=observer) as shell:
    
    # --- EJECUCIÓN DE COMANDOS EXTERNOS ---
    # Creamos un comando simple: 'ls -la'
    cmd_list = Command("ls").add_args("-la")
    result = shell.run(cmd_list)
    
    if result.is_success():
        print(f"Archivos encontrados:\n{result.standard_output}")

    # --- MANEJO DE ESTADO (VIRTUAL BUILT-INS) ---
    # Cambiamos de directorio (esto afecta al SessionContext, no solo al proceso)
    shell.run(Command("cd").add_args("/tmp"))
    
    # Verificamos el cambio ejecutando un 'pwd'
    shell.run(Command("pwd"))

    # --- VARIABLES DE ENTORNO ---
    # Exportamos una variable que persistirá durante este bloque 'with'
    shell.run(Command("export").add_args("APP_STAGE=development", "DEBUG=true"))
```


