# cc-shellback-kit



[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Version](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Rick-torrellas/cc-shellback-kit/badges/version.json)
[![CI CD](https://github.com/Rick-torrellas/cc-shellback-kit/actions/workflows/main.yaml/badge.svg)](https://github.com/Rick-torrellas/cc-shellback-kit/actions/workflows/main.yaml)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Download](https://img.shields.io/github/v/release/Rick-torrellas/cc-shellback-kit?label=Download&color=orange)](https://github.com/Rick-torrellas/cc-shellback-kit/releases)
[![docs](https://img.shields.io/badge/docs-read_now-blue?style=flat-square)](https://rick-torrellas.github.io/cc-shellback-kit/)
[![Ask DeepWiki](https://img.shields.io/badge/DeepWiki-Documentation-blue?logo=gitbook&logoColor=white)](https://deepwiki.com/Rick-torrellas/cc-shellback-kit)


💊⚛️

Shellback is a robust, architecturally-agnostic Python library designed to bridge terminal environments (Bash, CMD, PowerShell) with Python scripts. It provides a clean, decoupled abstraction layer to execute system commands while maintaining persistent session state and cross-platform compatibility.

Built with Hexagonal Architecture (Ports and Adapters) principles, Shellback ensures that your domain logic remains independent of the specific shell or operating system being used.

---

## 📍 Contents

* [Installation](#installation)
* [Usage](#usage)
* [Architecture Components](#architecture-components)
* [License](#license)
* [Key Features](#key-features)

---

## Installation

You can install cc-shellback-kit using pip:

```bash
pip install cc.shellback-kit
```

## Usage

```python
from cc_shellback_kit import Bash, ConsoleLogObserver, Command

observer = ConsoleLogObserver()

with Bash(observer=observer) as shell:
    
    cmd_list = Command("ls").add_args("-la")
    result = shell.run(cmd_list)
    
    if result.is_success():
        print(f"Files found:\n{result.standard_output}")

    shell.run(Command("cd").add_args("/tmp"))
    
    shell.run(Command("pwd"))

    shell.run(Command("export").add_args("APP_STAGE=development", "DEBUG=true"))
```

### Monitoring with Observers

Use the MultiObserver to log activity to both the console and a JSON audit file simultaneously.

```python
from cc_shellback_kit import MultiObserver, ConsoleLogObserver, JSONFileObserver,Bash, Command

audit_log = JSONFileObserver("audit.json")
console = ConsoleLogObserver()
monitor = MultiObserver([audit_log, console])

with Bash(observer=monitor) as shell:
    shell.run(Command("mkdir").add_args("test_folder"))
    shell.run(Command("cd").add_args("test_folder"))
    shell.run(Command("touch").add_args("hello.txt"))
```

### Fluent Argument Builder

The ArgumentBuilder handles lists and types automatically:

```python
cmd = Command("apt-get").add_args("install", ["git", "vim", "tmux"], "-y")
# Generates: ['apt-get', 'install', 'git', 'vim', 'tmux', '-y']
```

### Error Handling

The CommandResult object provides detailed information about failed executions:

```python
result = shell.run(Command("wrong_cmd"))
if not result.is_success():
    print(f"Error {result.return_code}: {result.standard_error}")
```

---

## ✨ Key Features

* **Hexagonal Architecture**: Decouples core logic from shell-specific implementations, allowing for easy extension to new shells or platforms.
* Persistent Session State: Keeps track of your Current Working Directory (cwd) and environment variables across multiple command executions.
* Plug-and-Play Observers: Built-in support for console logging, file logging, JSON auditing, or multi-channel notifications.
* Fluent API: Easily build complex commands with the ArgumentBuilder using a method-chaining interface.
* Safe Argument Handling: Automatic cleaning, flattening, and formatting of arguments to prevent common shell injection issues.
* Cross-Platform Compatibility: Works seamlessly on Windows, macOS, and Linux with support for Bash, CMD, and PowerShell.

## 🧪 Architecture Components

* Shell: The engine. It manages the lifecycle and coordinates between the SessionContext and the OS.
* Command: A value object representing what to run.
* CommandResult: Data class containing stdout, stderr, exit_code, and execution_time.
* ShellObserver: An interface to hook into events like on_command_start or on_error.

## 📄 License

This project is licensed under the MIT License.

