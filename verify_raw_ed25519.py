#!/usr/bin/env python3
"""Verify a SafeStack raw Ed25519 v1 detached signature."""

import argparse
import base64
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import ed25519


def read_public_key(path: Path) -> bytes:
    lines = [line.strip() for line in path.read_text(encoding="ascii").splitlines() if line.strip()]
    raw = base64.b64decode(lines[-1], validate=True)
    if len(raw) != 32:
        raise ValueError("public key must decode to 32 bytes")
    return raw


def read_signature(path: Path) -> bytes:
    lines = [line.strip() for line in path.read_text(encoding="ascii").splitlines() if line.strip()]
    raw = base64.b64decode(lines[-1], validate=True)
    if len(raw) != 64:
        raise ValueError("signature must decode to 64 bytes")
    return raw


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", required=True, type=Path)
    parser.add_argument("--signature", required=True, type=Path)
    parser.add_argument("--public-key", default=Path("safestack.pub"), type=Path)
    args = parser.parse_args()

    public_key = ed25519.Ed25519PublicKey.from_public_bytes(read_public_key(args.public_key))
    public_key.verify(read_signature(args.signature), args.message.read_bytes())
    print("Signature verified: SafeStack raw Ed25519 v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
