import json
import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any


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
        os.chmod(self.log_dir, 0o700)

    def log_execution(self, target: str, module_name: str, status: str, result_summary: Dict[str, Any]):
        """
        Log a single module execution event.
        """
        log_file = self.log_dir / \
            f"audit_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.jsonl"

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target_sha256": hashlib.sha256(target.lower().encode("utf-8")).hexdigest(),
            "module": module_name,
            "status": status,
            "summary": result_summary
        }

        fd = os.open(log_file, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        with os.fdopen(fd, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def log_system_event(self, event_type: str, details: str):
        """
        Log system-wide events (e.g. policy violations, startup).
        """
        log_file = self.log_dir / "system_events.jsonl"

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "details": details
        }

        fd = os.open(log_file, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        with os.fdopen(fd, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
