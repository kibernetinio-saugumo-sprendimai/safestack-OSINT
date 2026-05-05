from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class Result:
    """
    Normalized result returned by every OSINT module.

    This structure is machine-first.
    No formatting, no printing, no side effects.
    """

    # Module identifier (e.g. dns.passive, ip.whois)
    module: str

    # Target that was investigated
    target: str

    # Actual OSINT data (module-specific)
    data: Dict[str, Any]

    # Confidence score (0.0 – 1.0)
    confidence: float

    # Data sources used by the module
    sources: List[str] = field(default_factory=list)

    # Result creation timestamp
    timestamp: datetime = field(default_factory=datetime.utcnow)
