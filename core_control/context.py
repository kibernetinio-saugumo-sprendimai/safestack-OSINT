from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict
from core_control.policy import Policy

import uuid


@dataclass
class Context:
    """
    Execution context for a single OSINT run.

    This object MUST be passed to every module.
    It contains state, policy, and metadata — but NO logic.
    """

    # What we are investigating (domain, IP, email, etc.)
    target: str

    # Execution mode: passive, deep, custom
    mode: str

    # Security / ethical policy (what is allowed)
    policy: Policy

    # Auto-generated fields
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    started_at: datetime = field(default_factory=datetime.utcnow)

    # Free-form metadata (user, notes, tags, etc.)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        # Backward compatibility: allow dict-based policy
        if isinstance(self.policy, dict):
            self.policy = Policy(**self.policy)
