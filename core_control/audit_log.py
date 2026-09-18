import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from core_control.safeio import append_no_follow


class AuditLogger:
    """
    Handles persistent, structured logging of framework actions
    for auditability and accountability.
    """

    def __init__(self, log_dir: str = "logs/audit"):
        self.log_dir = Path(log_dir)
        self._ensure_log_dir()

    def _ensure_log_dir(self):
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True, exist_ok=True)

    def log_execution(self, target: str, module_name: str, status: str, result_summary: Dict[str, Any]):
        """
        Log a single module execution event.
        """
        log_file = self.log_dir / \
            f"audit_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "target": target,
            "module": module_name,
            "status": status,
            "summary": result_summary
        }

        append_no_follow(log_file, (json.dumps(entry, sort_keys=True) + "\n").encode())

    def log_system_event(self, event_type: str, details: str):
        """
        Log system-wide events (e.g. policy violations, startup).
        """
        log_file = self.log_dir / "system_events.jsonl"

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "details": details
        }

        append_no_follow(log_file, (json.dumps(entry, sort_keys=True) + "\n").encode())
