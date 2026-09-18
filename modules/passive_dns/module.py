from typing import Dict, Any


class PassiveDNSModule:
    """
    Real passive DNS resolver with fallback.
    """

    def __init__(self, timeout: float = 3.0):
        self.timeout = timeout

    def run(self, target: str) -> Dict[str, Any]:
        try:
            import dns.resolver
            import dns.exception
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Missing dependency: dnspython. Install with `pip install dnspython`"
            ) from exc

        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = ["1.1.1.1", "8.8.8.8"]
        resolver.timeout = self.timeout
        resolver.lifetime = self.timeout

        records = []

        try:
            answers = resolver.resolve(target, "A")
            for rdata in answers:
                records.append({
                    "type": "A",
                    "value": rdata.to_text()
                })

            return {
                "target": target,
                "records": records,
                "source": "local_dns"
            }

        except dns.resolver.NXDOMAIN:
            return {
                "target": target,
                "records": [],
                "error": "NXDOMAIN",
                "source": "local_dns"
            }

        except dns.exception.Timeout:
            return self._fallback(target, reason="timeout")

        except dns.exception.DNSException as exc:
            return self._fallback(target, reason=str(exc))

    def _fallback(self, target: str, reason: str) -> Dict[str, Any]:
        return {
            "target": target,
            "records": [],
            "error": "DNS_UNAVAILABLE",
            "note": f"DNS lookup unavailable ({reason}); no records returned",
            "source": "stub"
        }
