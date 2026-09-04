from typing import Dict, Any


class PassiveDNSModule:
    """
    Live DNS resolver. This performs a network query and is not passive-history DNS.
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
            return self._error(target, reason="timeout")

        except dns.exception.DNSException as exc:
            return self._error(target, reason=str(exc))

    def _error(self, target: str, reason: str) -> Dict[str, Any]:
        return {
            "target": target,
            "records": [],
            "error": "dns_failed",
            "reason": reason,
            "source": "local_dns"
        }
