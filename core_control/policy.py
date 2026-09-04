from __future__ import annotations

import fnmatch
import ipaddress
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Policy:
    """Explicit allow-list policy. Empty or omitted lists deny execution."""

    allowed_modes: List[str]
    module_modes: Dict[str, List[str]]
    allowed_modules: List[str]
    denied_modules: List[str]
    allowed_targets: List[str]
    notes: str = ""

    def validate(self) -> None:
        for name in ("allowed_modes", "allowed_modules", "denied_modules", "allowed_targets"):
            value = getattr(self, name)
            if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
                raise ValueError(f"{name} must be a non-empty list of strings")
        if not self.allowed_modes or not self.allowed_modules or not self.allowed_targets:
            raise ValueError("allowed_modes, allowed_modules and allowed_targets must be explicit and non-empty")
        if not isinstance(self.module_modes, dict):
            raise ValueError("module_modes must be a dict")
        for module, modes in self.module_modes.items():
            if not isinstance(module, str) or not isinstance(modes, list) or not modes:
                raise ValueError("module_modes entries must contain a module and one or more modes")
        missing_modes = set(self.allowed_modules) - set(self.module_modes)
        if missing_modes:
            raise ValueError(f"allowed modules require explicit module_modes: {sorted(missing_modes)}")
        overlap = set(self.allowed_modules) & set(self.denied_modules)
        if overlap:
            raise ValueError(f"modules cannot be both allowed and denied: {sorted(overlap)}")

    def allows_target(self, target: str) -> bool:
        normalized = target.strip().rstrip(".").lower()
        if not normalized:
            return False
        try:
            address = ipaddress.ip_address(normalized)
        except ValueError:
            address = None

        for entry in self.allowed_targets:
            candidate = entry.strip().lower()
            if address is not None:
                try:
                    if address in ipaddress.ip_network(candidate, strict=False):
                        return True
                except ValueError:
                    if candidate == normalized:
                        return True
            elif candidate == normalized or (candidate.startswith("*.") and fnmatch.fnmatch(normalized, candidate)):
                return True
        return False
