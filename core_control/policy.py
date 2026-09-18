from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class Policy:
    """
    Execution policy for OSINT operations.

    This object defines WHAT is allowed,
    not HOW it is enforced.
    """

    # Allowed execution modes (e.g. passive, deep)
    allowed_modes: Optional[List[str]] = None

    # Per-module allowed execution modes
    module_modes: Optional[Dict[str, List[str]]] = None

    # Explicitly allowed module names (allow-list)
    allowed_modules: Optional[List[str]] = None

    # Explicitly denied module names (deny-list)
    denied_modules: Optional[List[str]] = None

    # Optional target allow-list (domains, IPs, etc.)
    allowed_targets: Optional[List[str]] = None

    # Optional notes / metadata (for audit)
    notes: str = ""

    def validate(self):
        if self.allowed_modes is not None and not isinstance(self.allowed_modes, list):
            raise ValueError("allowed_modes must be a list")

        if self.allowed_modules is not None and not isinstance(self.allowed_modules, list):
            raise ValueError("allowed_modules must be a list")

        if self.denied_modules is not None and not isinstance(self.denied_modules, list):
            raise ValueError("denied_modules must be a list")

        if self.module_modes is not None and not isinstance(self.module_modes, dict):
            raise ValueError("module_modes must be a dict")

        if self.allowed_targets is not None and not isinstance(self.allowed_targets, list):
            raise ValueError("allowed_targets must be a list")
