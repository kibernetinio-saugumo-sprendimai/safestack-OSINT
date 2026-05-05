from typing import List, Dict
from core_control.result import Result


class RiskEngine:
    """
    Aggregates module results and computes
    target-level confidence, flags and human-readable hints.
    """

    @staticmethod
    def compute_target_confidence(results: List[Result]) -> float:
        if not results:
            return 0.0

        values = [r.confidence for r in results if r.confidence is not None]
        if not values:
            return 0.0

        return round(sum(values) / len(values), 3)

    @staticmethod
    def extract_flags(results: List[Result]) -> Dict[str, bool]:
        flags = {
            "no_tls": True,
            "multiple_ips": False,
            "whois_private": False,
        }

        for r in results:
            if r.module == "tls.info":
                flags["no_tls"] = False

            if r.module == "dns.passive":
                records = r.data.get("records", [])
                if len(records) >= 4:
                    flags["multiple_ips"] = True

            if r.module == "whois.rdap":
                registrar = r.data.get("registrar", {})
                if not registrar or registrar.get("name") in (None, "", "REDACTED"):
                    flags["whois_private"] = True

        return flags

    @staticmethod
    def generate_hints(flags: Dict[str, bool]) -> List[str]:
        """
        Convert flags into human-readable explanations.
        """
        hints: List[str] = []

        if flags.get("no_tls"):
            hints.append(
                "No TLS detected – traffic may be unencrypted or downgraded.")
        else:
            hints.append("TLS is present and active.")

        if flags.get("multiple_ips"):
            hints.append(
                "Multiple IP addresses detected – likely CDN usage or load balancing."
            )

        if flags.get("whois_private"):
            hints.append(
                "WHOIS information is limited or anonymized."
            )
        else:
            hints.append(
                "WHOIS registrar information is present and identifiable."
            )

        return hints
