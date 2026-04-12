import json
import time
from pathlib import Path
from typing import Any, List, Optional, Dict
from ..core import ShellObserver, CommandResult


class JSONFileObserver(ShellObserver):
    """
    Registra toda la actividad de la Shell en un archivo JSON.
    Ideal para auditoría técnica y análisis de datos posterior.
    """

    def __init__(self, log_path: str = "shell_audit.json"):
        self.log_path = Path(log_path)
        # Inicializamos el archivo si no existe
        if not self.log_path.exists():
            self._write_logs([])

    def _read_logs(self) -> List[Dict[str, Any]]:
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError, FileNotFoundError:
            return []

    def _write_logs(self, logs: List[Dict[str, Any]]):
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)

    def _append_entry(self, entry: Dict[str, Any]):
        logs = self._read_logs()
        logs.append(entry)
        self._write_logs(logs)

    def on_command_result(self, result: CommandResult):
        entry = {
            "timestamp": time.time(),
            "event": "command_executed",
            "command": result.command_sent,
            "success": result.is_success(),
            "exit_code": result.return_code,
            "duration": round(result.execution_time, 4),
            "stdout_len": len(result.standard_output),
            "stderr": result.standard_error.strip() if result.standard_error else None,
        }
        self._append_entry(entry)

    def on_context_change(self, key: str, value: Any):
        entry = {
            "timestamp": time.time(),
            "event": "context_mutation",
            "change": {key: str(value)},
        }
        self._append_entry(entry)

    def on_error(self, message: str, error: Optional[Exception] = None):
        entry = {
            "timestamp": time.time(),
            "event": "internal_error",
            "message": message,
            "exception": str(error) if error else None,
        }
        self._append_entry(entry)
