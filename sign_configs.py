import argparse
from pathlib import Path

from core_control.reporting.signing import Signer


def main() -> int:
    parser = argparse.ArgumentParser(description="Create SafeStack raw Ed25519 v1 signatures")
    parser.add_argument("--signing-key", required=True, type=Path)
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent
    key_path = args.signing_key.resolve(strict=True)
    if project_root == key_path or project_root in key_path.parents:
        raise SystemExit("private signing key must be outside the repository")

    signer = Signer(key_path.read_text(encoding="ascii").strip())
    for name in args.files:
        path = Path(name).resolve(strict=True)
        if not signer.sign_report(str(path)):
            print(f"[FAILED] {path}")
            return 1
        print(f"[SIGNED] {path}.sig")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
