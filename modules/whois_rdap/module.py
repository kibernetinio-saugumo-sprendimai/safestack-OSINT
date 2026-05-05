from typing import Dict, Any, Optional

try:
    import requests
except ImportError:
    requests = None


class WhoisRDAPModule:
    """
    Real RDAP lookup using rdap.org with IANA bootstrap fallback.
    """

    RDAP_PRIMARY = "https://rdap.org/domain/{}"
    IANA_BOOTSTRAP = "https://data.iana.org/rdap/dns.json"

    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout

    def run(self, target: str) -> Dict[str, Any]:
        if requests is None:
            return {
                "target": target,
                "error": "missing_dependency",
                "reason": "Missing dependency: requests. Install with pip install requests",
            }

        # 1) Try rdap.org
        try:
            data = self._fetch(self.RDAP_PRIMARY.format(target))
            return self._normalize(target, data, source="rdap.org")
        except Exception:
            pass

        # 2) Bootstrap fallback
        try:
            base = self._bootstrap_base(target)
            if not base:
                raise RuntimeError("No RDAP base found via bootstrap")

            data = self._fetch(f"{base}/domain/{target}")
            return self._normalize(target, data, source="bootstrap")
        except Exception as exc:
            return {
                "target": target,
                "error": "rdap_failed",
                "reason": str(exc),
            }

    def _fetch(self, url: str) -> Dict[str, Any]:
        resp = requests.get(
            url,
            headers={"Accept": "application/rdap+json"},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()

    def _bootstrap_base(self, domain: str) -> Optional[str]:
        tld = domain.rsplit(".", 1)[-1].lower()
        resp = requests.get(self.IANA_BOOTSTRAP, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()

        for entry in data.get("services", []):
            tlds, bases = entry
            if tld in tlds and bases:
                return bases[0].rstrip("/")
        return None

    def _normalize(self, target: str, data: Dict[str, Any], source: str) -> Dict[str, Any]:
        registrar = {}
        for ent in data.get("entities", []):
            roles = ent.get("roles", [])
            if "registrar" in roles:
                vcard = ent.get("vcardArray", [])
                registrar = self._vcard_to_dict(vcard)
                break

        return {
            "target": target,
            "handle": data.get("handle"),
            "status": data.get("status", []),
            "registrar": {
                "name": registrar.get("fn") or registrar.get("org"),
                "iana_id": registrar.get("ianaId"),
            },
            "registration": {
                "created": self._event_date(data, "registration"),
                "expires": self._event_date(data, "expiration"),
            },
            "source": source,
        }

    def _event_date(self, data: Dict[str, Any], event_action: str) -> Optional[str]:
        for ev in data.get("events", []):
            if ev.get("eventAction") == event_action:
                return ev.get("eventDate")
        return None

    def _vcard_to_dict(self, vcard) -> Dict[str, Any]:
        # vcardArray format: ["vcard", [[key, params, type, value], ...]]
        result = {}
        if len(vcard) != 2:
            return result
        for item in vcard[1]:
            if len(item) == 4:
                key, _, _, value = item
                result[key] = value
        return result
