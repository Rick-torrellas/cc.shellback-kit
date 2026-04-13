# cc-shellback-kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Version](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Rick-torrellas/cc-shellback-kit/badges/version.json)
[![CI CD](https://github.com/Rick-torrellas/cc-shellback-kit/actions/workflows/main.yaml/badge.svg)](https://github.com/Rick-torrellas/cc-shellback-kit/actions/workflows/main.yaml)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Download](https://img.shields.io/github/v/release/Rick-torrellas/cc-shellback-kit?label=Download&color=orange)](https://github.com/Rick-torrellas/cc-shellback-kit/releases)
[![Ask DeepWiki](https://img.shields.io/badge/DeepWiki-Documentation-blue?logo=gitbook&logoColor=white)](https://deepwiki.com/Rick-torrellas/cc-shellback-kit)
[![docs](https://img.shields.io/badge/docs-read_now-blue?style=flat-square)](https://rick-torrellas.github.io/cc-shellback-kit/)

Shellback is a robust, architecturally-agnostic Python library designed to bridge terminal environments (Bash, CMD, PowerShell) with Python scripts. It provides a clean, decoupled abstraction layer to execute system commands while maintaining persistent session state and cross-platform compatibility.

Built with Hexagonal Architecture (Ports and Adapters) principles, Shellback ensures that your domain logic remains independent of the specific shell or operating system being used.

---

## 📍 Contents

* [Installation](#installation)
* [Usage](#usage)

---

## Installation

You can install cc-shellback-kit using pip:

```bash
pip install cc.shellback-kit
```

## Usage

```python
from cc_shellback_kit import Bash, ConsoleLogObserver, Command

# 1. We configure the observer to see the activity in the console
observer = ConsoleLogObserver()

# 2. We start the Shell using the context manager (with)
with Bash(observer=observer) as shell:
    
    # --- EXECUTION OF EXTERNAL COMMANDS ---
    # We create a simple command: 'ls -la'
    cmd_list = Command("ls").add_args("-la")
    result = shell.run(cmd_list)
    
    if result.is_success():
        print(f"Files found:\n{result.standard_output}")

    # --- STATE MANAGEMENT (VIRTUAL BUILT-INS) ---
    # We change directory (this affects the SessionContext, not just the process)
    shell.run(Command("cd").add_args("/tmp"))
    
    # We verify the change by running 'pwd'
    shell.run(Command("pwd"))

    # --- ENVIRONMENT VARIABLES ---
    # We export a variable that will persist during this 'with' block
    shell.run(Command("export").add_args("APP_STAGE=development", "DEBUG=true"))
```


