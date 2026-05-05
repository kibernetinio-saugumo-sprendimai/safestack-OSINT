import socket
import ssl
import hashlib
from typing import Dict, Any, List


class TLSInfoModule:
    """
    Real TLS information extractor using stdlib.
    Tries multiple ports automatically.
    """

    DEFAULT_PORTS: List[int] = [443, 8443, 9443]

    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout

    def run(self, target: str) -> Dict[str, Any]:
        last_error = None

        for port in self.DEFAULT_PORTS:
            try:
                return self._probe_tls(target, port)
            except Exception as exc:
                last_error = exc
                continue

        return {
            "target": target,
            "error": "tls_failed",
            "reason": str(last_error),
        }

    def _probe_tls(self, host: str, port: int) -> Dict[str, Any]:
        context = ssl.create_default_context()

        with socket.create_connection((host, port), timeout=self.timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert_bin = ssock.getpeercert(binary_form=True)
                cert = ssock.getpeercert()

                fingerprint = hashlib.sha256(cert_bin).hexdigest()

                return {
                    "target": host,
                    "port": port,
                    "tls": {
                        "protocol": ssock.version(),
                        "cipher": ssock.cipher()[0],
                        "certificate": {
                            "subject": self._fmt_name(cert.get("subject")),
                            "issuer": self._fmt_name(cert.get("issuer")),
                            "not_before": cert.get("notBefore"),
                            "not_after": cert.get("notAfter"),
                            "fingerprint_sha256": fingerprint,
                        },
                    },
                    "source": "local_tls"
                }

    def _fmt_name(self, name) -> str:
        if not name:
            return ""
        return ", ".join(
            f"{k}={v}" for item in name for k, v in item
        )
