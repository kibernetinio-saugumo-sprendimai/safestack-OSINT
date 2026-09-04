import base64
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False


class Signer:
    """
    Handles SafeStack raw Ed25519 v1 signatures.

    This format is not Minisign and must be verified with the repository's
    verify_raw_ed25519.py helper.
    """

    def __init__(self, private_key_hex: str = None):
        self.private_key_hex = private_key_hex

    def sign_report(self, report_path: str):
        """
        Sign the report at the given path.
        Returns True if successful.
        """
        if not self.private_key_hex:
            return False

        if not HAS_CRYPTO:
            return False

        try:
            # Convert hex key to bytes
            private_bytes = bytes.fromhex(self.private_key_hex)
            privkey = ed25519.Ed25519PrivateKey.from_private_bytes(
                private_bytes)

            # Read report data
            with open(report_path, "rb") as f:
                data = f.read()

            # Sign
            signature = privkey.sign(data)

            sig_path = Path(str(report_path) + ".sig")

            # For "Root of Trust" we use a simple header + base64 signature
            with open(sig_path, "w") as f:
                f.write("untrusted comment: safestack raw ed25519 signature v1\n")
                f.write(base64.b64encode(signature).decode() + "\n")

            return True
        except Exception:
            return False
